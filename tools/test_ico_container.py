#!/usr/bin/env python3
"""Exercise the production ICO container using independent binary fixtures.

The fixture writer deliberately does not call the production codec. Python checks
all decoded pixels, and Pillow independently opens an exported ICO when present.
Only the host JDK and Python standard library are required for the core tests.
"""
import binascii
import io
import pathlib
import shutil
import struct
import subprocess
import tempfile
import unittest
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = shutil.which("java") or "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
SOURCE = ROOT / "Paintroid/src/main/java"
HARNESS = r'''
import org.catrobat.paintroid.classic.IcoContainer;
import java.io.*;
public class IcoFixtureHarness {
    public static void main(String[] args) throws Exception {
        try { run(args); } catch (IOException failure) {
            System.err.println("IOException: " + failure); System.exit(2);
        }
    }
    static void run(String[] args) throws Exception {
        File input = new File(args[1]);
        if (args[0].equals("png-batch")) {
            for (String line : java.nio.file.Files.readAllLines(input.toPath())) {
                String[] fields = line.split("\\t");
                File png = new File(input.getParentFile(), fields[0] + ".png");
                File icon = new File(input.getParentFile(), fields[0] + ".ico");
                int width = Integer.parseInt(fields[1]), height = Integer.parseInt(fields[2]);
                boolean read = false, write = false;
                try {
                    IcoContainer.Entry entry = IcoContainer.best(icon);
                    ByteArrayOutputStream extracted = new ByteArrayOutputStream();
                    IcoContainer.extractPng(icon, entry, extracted);
                    if (!java.util.Arrays.equals(extracted.toByteArray(), java.nio.file.Files.readAllBytes(png.toPath())))
                        throw new AssertionError("extraction changed PNG bytes");
                    read = true;
                } catch (IOException expected) { }
                try {
                    ByteArrayOutputStream exported = new ByteArrayOutputStream();
                    IcoContainer.writePng(png, width, height, exported);
                    if (!java.util.Arrays.equals(exported.toByteArray(), java.nio.file.Files.readAllBytes(icon.toPath())))
                        throw new AssertionError("export changed ICO bytes");
                    write = true;
                } catch (IOException expected) { }
                System.out.println(fields[0] + " " + read + " " + write);
            }
            return;
        }
        if (args[0].equals("sniff")) {
            System.out.println(IcoContainer.isIco(input)); return;
        }
        if (args[0].equals("write")) {
            try (OutputStream out = new FileOutputStream(args[2])) {
                IcoContainer.writePng(input, Integer.parseInt(args[3]), Integer.parseInt(args[4]), out);
            }
            return;
        }
        IcoContainer.Entry entry = IcoContainer.best(input);
        if (args[0].equals("inspect")) {
            System.out.printf("%d %d %d %s %d %d%n", entry.width, entry.height,
                entry.bits, entry.png, entry.offset, entry.length);
        } else if (entry.png) {
            try (OutputStream out = new FileOutputStream(args[2])) {
                IcoContainer.extractPng(input, entry, out);
            }
        } else {
            int[] pixels = IcoContainer.decodeDib(input, entry);
            System.out.printf("%d %d %d%n", entry.width, entry.height, pixels.length);
            for (int pixel : pixels) System.out.printf("%08x%n", pixel);
        }
    }
}
'''


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xffffffff)


def png(width, height):
    """Tiny true RGBA PNG, with an exact checker known outside the Java codec."""
    raw = b"".join(b"\0" + b"".join(bytes((x % 256, y % 256, (x + y) % 256, 128 if x & 1 else 255))
                                  for x in range(width)) for y in range(height))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))



# Adam7 coordinate sets are enumerated from the PNG specification. Gathering
# source samples by coordinates also gives Pillow an independent pixel oracle.
ADAM7 = ((0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4),
         (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2))
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


def sample(x, y, channel, depth):
    return (x * 3 + y * 5 + channel * 7 + 1) & ((1 << depth) - 1)


def png_rows(width, height, depth=8, colour=6, interlace=0, filters=(0,)):
    """Encode real samples, row packing and filters without a production helper.

    Passes with no source coordinates emit no filter byte or rows. Sub-byte
    samples are packed MSB-first and each pass row begins on a byte boundary.
    """
    channels = CHANNELS[colour]
    bytes_per_pixel = max(1, (channels * depth + 7) // 8)
    encoded, row_starts = bytearray(), []
    passes = ADAM7 if interlace else ((0, 0, 1, 1),)
    row_index = 0
    for x_start, y_start, x_step, y_step in passes:
        xs, ys = list(range(x_start, width, x_step)), list(range(y_start, height, y_step))
        if not xs or not ys:
            continue
        previous = b""
        for y in ys:
            samples = [sample(x, y, channel, depth) for x in xs for channel in range(channels)]
            if depth < 8:
                row = bytearray((len(samples) * depth + 7) // 8)
                for index, value in enumerate(samples):
                    bit = index * depth
                    row[bit // 8] |= value << (8 - depth - bit % 8)
            elif depth == 8:
                row = bytearray(samples)
            else:
                row = bytearray(b"".join(struct.pack(">H", value) for value in samples))
            filter_type = filters[row_index % len(filters)]
            row_starts.append(len(encoded))
            encoded.append(filter_type)
            for index, value in enumerate(row):
                left = row[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
                above = previous[index] if previous else 0
                upper_left = previous[index - bytes_per_pixel] if previous and index >= bytes_per_pixel else 0
                if filter_type == 0:
                    prediction = 0
                elif filter_type == 1:
                    prediction = left
                elif filter_type == 2:
                    prediction = above
                elif filter_type == 3:
                    prediction = (left + above) // 2
                else:
                    predictor = left + above - upper_left
                    distances = (abs(predictor - left), abs(predictor - above), abs(predictor - upper_left))
                    prediction = (left, above, upper_left)[distances.index(min(distances))]
                encoded.append((value - prediction) & 255)
            previous = row
            row_index += 1
    return bytes(encoded), row_starts


def png_from_rows(width, height, depth=8, colour=6, interlace=0, raw=None, compressed=None, idat_parts=None):
    if raw is None:
        raw, _ = png_rows(width, height, depth, colour, interlace)
    if compressed is None:
        compressed = zlib.compress(raw)
    if idat_parts is None:
        idat_parts = [compressed]
    palette = b""
    if colour == 3:
        palette = chunk(b"PLTE", b"".join(bytes((index, 255 - index, index // 2)) for index in range(1 << depth)))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, depth, colour, 0, 0, interlace))
            + palette + b"".join(chunk(b"IDAT", part) for part in idat_parts) + chunk(b"IEND", b""))


def ico(entries):
    """Entry tuple: width, height, bits, payload; offsets assembled independently."""
    offset = 6 + 16 * len(entries)
    directory = []
    for width, height, bits, payload in entries:
        directory.append(struct.pack("<BBBBHHII", width % 256, height % 256, 0, 0, 1, bits, len(payload), offset))
        offset += len(payload)
    return struct.pack("<HHH", 0, 1, len(entries)) + b"".join(directory) + b"".join(entry[3] for entry in entries)


def dib(width, height, bits, pixels, mask=None, palette=(), header_size=40, compression=0, masks=(), top_down=False):
    """Construct bottom-up XOR and AND planes, including each plane's own padding."""
    assert len(pixels) == width * height
    if mask is None:
        mask = [False] * len(pixels)
    assert len(mask) == len(pixels)
    header = bytearray(header_size)
    struct.pack_into("<I", header, 0, header_size)
    if header_size == 12:
        struct.pack_into("<HHHH", header, 4, width, height * 2, 1, bits)
    else:
        struct.pack_into("<iiHHI", header, 4, width, height * (-2 if top_down else 2), 1, bits, compression)
        struct.pack_into("<I", header, 32, len(palette))
        if header_size >= 108:
            struct.pack_into("<I", header, 56, 0x73524742)  # Explicit sRGB.
    external_masks = b""
    if masks:
        packed = struct.pack("<" + "I" * len(masks), *masks)
        if header_size == 40:
            external_masks = packed
        else:
            header[40:40 + len(packed)] = packed
    colours = b"".join(bytes((value & 255, (value >> 8) & 255, (value >> 16) & 255))
                        + (b"" if header_size == 12 else b"\0") for value in palette)
    xor_stride = ((width * bits + 31) // 32) * 4
    and_stride = ((width + 31) // 32) * 4
    xor_rows, and_rows = [], []
    for y in (range(height) if top_down else reversed(range(height))):
        row, and_row = bytearray(xor_stride), bytearray(and_stride)
        for x in range(width):
            pixel = pixels[y * width + x]
            if bits == 1:
                row[x // 8] |= pixel << (7 - x % 8)
            elif bits == 4:
                row[x // 2] |= pixel << (4 if x % 2 == 0 else 0)
            elif bits == 8:
                row[x] = pixel
            else:
                row[x * (bits // 8):(x + 1) * (bits // 8)] = pixel.to_bytes(bits // 8, "little")
            if mask[y * width + x]:
                and_row[x // 8] |= 1 << (7 - x % 8)
        xor_rows.append(bytes(row))
        and_rows.append(bytes(and_row))
    return bytes(header) + external_masks + colours + b"".join(xor_rows) + b"".join(and_rows)


class IcoContainerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="anpaint-ico-fixtures-")
        cls.path = pathlib.Path(cls.directory.name)
        harness = cls.path / "IcoFixtureHarness.java"
        harness.write_text(HARNESS)
        subprocess.run([JAVA, "-m", "jdk.compiler/com.sun.tools.javac.Main", "-d", str(cls.path),
                        "-sourcepath", str(SOURCE),
                        str(SOURCE / "org/catrobat/paintroid/classic/IcoContainer.java"), str(harness)],
                       check=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def invoke(self, command, data, *args, reject=False):
        source = self.path / "input.unknown"
        source.write_bytes(data)
        output = self.path / "output.bin"
        result = subprocess.run([JAVA, "-cp", str(self.path), "IcoFixtureHarness", command, str(source),
                                 *([str(output)] if command in ("read", "write") else []), *map(str, args)],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(source.read_bytes(), data, "codec modified input file")
        if reject:
            self.assertNotEqual(result.returncode, 0, "accepted malformed fixture")
            self.assertIn("IOException", result.stderr, result.stderr)
            return None
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip(), output

    def assert_png_batch(self, fixtures):
        """One JVM checks both opening/extraction and saving for every fixture."""
        manifest = self.path / "png-batch.tsv"
        lines = []
        for index, (label, width, height, payload, accepted) in enumerate(fixtures):
            stem = f"batch-{index}"
            (self.path / f"{stem}.png").write_bytes(payload)
            (self.path / f"{stem}.ico").write_bytes(ico([(width, height, 32, payload)]))
            lines.append(f"{stem}\t{width}\t{height}")
        manifest.write_text("\n".join(lines) + "\n")
        result = subprocess.run([JAVA, "-cp", str(self.path), "IcoFixtureHarness", "png-batch", str(manifest)],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        results = result.stdout.splitlines()
        self.assertEqual(len(results), len(fixtures), result.stdout)
        for index, ((label, width, height, payload, accepted), actual) in enumerate(zip(fixtures, results)):
            with self.subTest(fixture=label):
                status = str(accepted).lower()
                self.assertEqual(actual, f"batch-{index} {status} {status}")
                self.assertEqual((self.path / f"batch-{index}.png").read_bytes(), payload)
                self.assertEqual((self.path / f"batch-{index}.ico").read_bytes(), ico([(width, height, 32, payload)]))

    def assert_pixels(self, width, height, bits, payload, expected):
        stdout, _ = self.invoke("read", ico([(width, height, bits, payload)]))
        lines = stdout.splitlines()
        self.assertEqual(lines[0], f"{width} {height} {width * height}")
        actual = [int(pixel, 16) for pixel in lines[1:]]
        # RGB beneath transparent mask bits is unspecified; alpha itself is exact.
        self.assertEqual([pixel if pixel >> 24 else 0 for pixel in actual],
                         [pixel if pixel >> 24 else 0 for pixel in expected])

    def test_sniff_uses_signature_instead_of_extension(self):
        sample = ico([(1, 1, 32, png(1, 1))])
        self.assertEqual(self.invoke("sniff", sample)[0], "true")
        for other in (b"", b"BM1234", b"\0\0\2\0\1\0", png(1, 1)):
            self.assertEqual(self.invoke("sniff", other)[0], "false")

    def test_select_largest_entry_and_extract_exact_png(self):
        payloads = [png(16, 16), png(64, 32), png(32, 32)]
        data = ico([(16, 16, 32, payloads[0]), (64, 32, 32, payloads[1]), (32, 32, 32, payloads[2])])
        fields = self.invoke("inspect", data)[0].split()
        self.assertEqual(fields[:4], ["64", "32", "32", "true"])
        self.assertEqual(list(map(int, fields[4:])), [54 + len(payloads[0]), len(payloads[1])])
        _, output = self.invoke("read", data)
        self.assertEqual(output.read_bytes(), payloads[1])

    def test_palette_1_4_8_bit_and_core_header_with_and_transparency(self):
        palette = [0x112233, 0xaabbcc]
        indices = [0, 1, 0, 1, 0, 1]
        mask = [False, True, False, True, False, False]
        expected = [0 if transparent else 0xff000000 | palette[index] for index, transparent in zip(indices, mask)]
        for bits in (1, 4, 8):
            for header_size in (12, 40, 108, 124):
                with self.subTest(bits=bits, header_size=header_size):
                    table = palette + [0] * ((1 << bits) - 2) if header_size == 12 else palette
                    self.assert_pixels(3, 2, bits, dib(3, 2, bits, indices, mask, table, header_size), expected)

    def test_24_bit_xor_and_mask_orientation_and_padding(self):
        pixels = [0x123456, 0xabcdef, 0x030609, 0x102040, 0x91a2b3, 0xc2d3e4]
        mask = [False, False, True, False, True, False]
        expected = [0 if transparent else value | 0xff000000 for value, transparent in zip(pixels, mask)]
        self.assert_pixels(3, 2, 24, dib(3, 2, 24, pixels, mask), expected)

    def test_16_bit_rgb555_and_rgb565_bitfields(self):
        expected = [0xffff0000, 0xff00ff00, 0xff0000ff]
        self.assert_pixels(3, 1, 16, dib(3, 1, 16, [0x7c00, 0x03e0, 0x001f]), expected)
        for size in (40, 52, 108, 124):
            with self.subTest(header_size=size):
                self.assert_pixels(3, 1, 16,
                                   dib(3, 1, 16, [0xf800, 0x07e0, 0x001f], header_size=size,
                                       compression=3, masks=(0xf800, 0x07e0, 0x001f)), expected)

    def test_16_bit_explicit_alpha_and_and_mask_both_apply(self):
        # Unlike modern 32-bit alpha icons, 16-bit icons keep their AND mask.
        for size in (40, 56, 108):
            with self.subTest(header_size=size):
                payload = dib(3, 1, 16, [0xfc00, 0x83e0, 0x001f], [True, False, False],
                              header_size=size, compression=6,
                              masks=(0x7c00, 0x03e0, 0x001f, 0x8000))
                self.assert_pixels(3, 1, 16, payload, [0, 0xff00ff00, 0])

    def test_32_bit_legacy_zero_alpha_uses_and_mask(self):
        pixels = [0xff0000, 0x00ff00, 0x0000ff, 0xabcdef]
        self.assert_pixels(2, 2, 32, dib(2, 2, 32, pixels, [False, True, False, False]),
                           [0xffff0000, 0, 0xff0000ff, 0xffabcdef])

    def test_32_bit_meaningful_alpha_ignores_and_mask_and_stays_straight(self):
        pixels = [0x80123456, 0x00010203, 0xffabcdef, 0x20102040]
        self.assert_pixels(2, 2, 32, dib(2, 2, 32, pixels, [True] * 4), pixels)
        # Modern PNG-era ICO DIBs can legitimately omit the legacy AND plane.
        self.assert_pixels(2, 2, 32, dib(2, 2, 32, pixels)[:-8], pixels)
        self.invoke("read", ico([(2, 2, 32, dib(2, 2, 32, [0] * 4)[:-8])]), reject=True)

    def test_256_dimension_sentinel_and_export_independent_structure(self):
        for width, height in ((1, 1), (32, 16), (256, 256)):
            with self.subTest(width=width, height=height):
                source = png(width, height)
                _, output = self.invoke("write", source, width, height)
                encoded = output.read_bytes()
                self.assertEqual(struct.unpack_from("<HHH", encoded), (0, 1, 1))
                self.assertEqual(struct.unpack_from("<BBBBHHII", encoded, 6),
                                 (width % 256, height % 256, 0, 0, 1, 32, len(source), 22))
                self.assertEqual(encoded[22:], source)
                _, extracted = self.invoke("read", encoded)
                self.assertEqual(extracted.read_bytes(), source)

    def test_export_opens_with_independent_pillow_ico_decoder(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow is optional; independent structure checks remain active")
        _, output = self.invoke("write", png(32, 16), 32, 16)
        with Image.open(output) as image:
            self.assertEqual(image.format, "ICO")
            self.assertEqual(image.size, (32, 16))
            self.assertEqual(image.convert("RGBA").getpixel((7, 5)), (7, 5, 12, 128))
            self.assertEqual(image.convert("RGBA").getpixel((8, 6)), (8, 6, 14, 255))

    def test_directory_rejects_truncation_bad_offsets_lengths_and_count(self):
        valid = ico([(1, 1, 32, png(1, 1))])
        invalid = [valid[:n] for n in (0, 4, 5, 6, 21, len(valid) - 1)]
        for offset, fmt, value in ((0, "<H", 1), (2, "<H", 2), (4, "<H", 0),
                                   (18, "<I", 0), (18, "<I", 6), (18, "<I", 21),
                                   (18, "<I", 0xffffffff), (14, "<I", 0), (14, "<I", 0xffffffff)):
            changed = bytearray(valid)
            struct.pack_into(fmt, changed, offset, value)
            invalid.append(changed)
        invalid.append(struct.pack("<HHH", 0, 1, 257) + bytes(257 * 16))
        for index, data in enumerate(invalid):
            with self.subTest(case=index):
                self.invoke("read", data, reject=True)

    def test_png_crc_truncation_and_directory_dimension_mismatch(self):
        valid = png(2, 2)
        broken_crc = bytearray(valid)
        broken_crc[29] ^= 1
        for payload in (valid[:32], valid[:-1], bytes(broken_crc)):
            with self.subTest(length=len(payload)):
                self.invoke("read", ico([(2, 2, 32, payload)]), reject=True)
        self.invoke("read", ico([(3, 2, 32, valid)]), reject=True)
        self.invoke("write", valid, 3, 2, reject=True)
        for width, height in ((0, 2), (257, 2), (2, -1)):
            self.invoke("write", valid, width, height, reject=True)

    def test_png_rejects_invalid_ihdr_encoding_fields_with_valid_crc(self):
        valid = png(2, 2)
        for offset, value in ((8, 3), (10, 1), (11, 1), (12, 2)):
            with self.subTest(ihdr_offset=offset):
                header = bytearray(valid[16:29])
                header[offset] = value
                malformed = valid[:8] + chunk(b"IHDR", header) + valid[33:]
                self.invoke("read", ico([(2, 2, 32, malformed)]), reject=True)
                self.invoke("write", malformed, 2, 2, reject=True)

    def test_png_rejects_corrupt_or_incomplete_deflate_with_correct_chunk_crcs(self):
        raw, _ = png_rows(3, 2)
        stream = zlib.compress(raw)
        invalid = [("four arbitrary bytes", bytes((1, 2, 3, 4))), ("empty stream", b"")]
        invalid.extend((f"truncated at {cut}", stream[:cut]) for cut in range(1, len(stream)))
        bad_adler = bytearray(stream)
        bad_adler[-1] ^= 0x80
        invalid.extend((("wrong Adler checksum", bytes(bad_adler)),
                        ("trailing compressed byte", stream + b"\0"),
                        ("trailing arbitrary bytes", stream + b"trailing"),
                        ("second complete zlib stream", stream + zlib.compress(raw)),
                        ("second empty zlib stream", stream + zlib.compress(b"")),
                        ("short decompressed row", zlib.compress(raw[:-1])),
                        ("missing complete row", zlib.compress(raw[:13])),
                        ("extra decompressed byte", zlib.compress(raw + b"\0")),
                        ("extra complete row", zlib.compress(raw + raw[:13]))))
        # Set BTYPE to its reserved value while preserving a legal zlib header.
        bad_block = stream[:2] + bytes((stream[2] | 6,)) + stream[3:]
        invalid.append(("reserved deflate block type", bad_block))
        dictionary_encoder = zlib.compressobj(zdict=raw)
        invalid.append(("preset dictionary", dictionary_encoder.compress(raw) + dictionary_encoder.flush()))
        self.assert_png_batch([(label, 3, 2, png_from_rows(3, 2, compressed=value), False)
                               for label, value in invalid])

    def test_png_rejects_illegal_filter_bytes_and_wrong_adam7_lengths(self):
        fixtures = []
        for interlace in (0, 1):
            raw, starts = png_rows(9, 5, 2, 0, interlace)
            for row, start in enumerate(starts):
                malformed = bytearray(raw)
                malformed[start] = 5 if row % 2 == 0 else 255
                fixtures.append((f"interlace {interlace} row {row} bad filter", 9, 5,
                                 png_from_rows(9, 5, 2, 0, interlace, raw=malformed), False))
            fixtures.extend((f"interlace {interlace} {label}", 9, 5,
                             png_from_rows(9, 5, 2, 0, interlace, raw=value), False)
                            for label, value in (("short data", raw[:-1]), ("extra data", raw + b"\0")))
        # Empty Adam7 passes must not contribute fictitious filter bytes.
        tiny, _ = png_rows(1, 1, 1, 0, 1)
        fixtures.append(("filter bytes for empty Adam7 passes", 1, 1,
                         png_from_rows(1, 1, 1, 0, 1, raw=tiny + bytes(6)), False))
        self.assert_png_batch(fixtures)

    def test_png_accepts_consecutive_split_and_empty_idat_chunks_only(self):
        raw, _ = png_rows(7, 3)
        stream = zlib.compress(raw)
        fixtures = []
        splits = (("single", [stream]), ("empty around stream", [b"", stream, b""]),
                  ("one byte per IDAT", [bytes((value,)) for value in stream]),
                  ("empty interleaved IDAT", [part for value in stream for part in (b"", bytes((value,)), b"")]))
        for label, parts in splits:
            fixtures.append((label, 7, 3, png_from_rows(7, 3, idat_parts=parts), True))
        header = png_from_rows(7, 3).split(chunk(b"IDAT", stream))[0]
        middle = len(stream) // 2
        for label, parts in (("intervening ancillary chunk", [chunk(b"IDAT", stream[:middle]),
                                                              chunk(b"tEXt", b"label\0value"),
                                                              chunk(b"IDAT", stream[middle:])]),
                             ("nonconsecutive empty IDAT", [chunk(b"IDAT", stream),
                                                            chunk(b"tEXt", b"label\0value"), chunk(b"IDAT", b"")]),
                             ("extra data in later IDAT", [chunk(b"IDAT", stream), chunk(b"IDAT", b"\0")]),
                             ("new stream in later IDAT", [chunk(b"IDAT", stream), chunk(b"IDAT", zlib.compress(b""))])):
            fixtures.append((label, 7, 3, header + b"".join(parts) + chunk(b"IEND", b""), False))
        self.assert_png_batch(fixtures)

    def test_png_accepts_all_sample_depths_and_adam7_odd_or_empty_passes(self):
        fixtures = []
        formats = [(0, depth) for depth in (1, 2, 4, 8, 16)] + [(3, depth) for depth in (1, 2, 4, 8)]
        formats += [(colour, depth) for colour in (2, 4, 6) for depth in (8, 16)]
        for colour, depth in formats:
            for interlace in (0, 1):
                for width, height in ((1, 1), (1, 7), (7, 1), (2, 3), (9, 5), (17, 11)):
                    raw, starts = png_rows(width, height, depth, colour, interlace, filters=(0, 1, 2, 3, 4))
                    self.assertTrue(starts)
                    payload = png_from_rows(width, height, depth, colour, interlace, raw=raw)
                    fixtures.append((f"colour {colour} depth {depth} interlace {interlace} {width}x{height}",
                                     width, height, payload, True))
        self.assert_png_batch(fixtures)

    def test_adam7_fixture_pixels_match_independent_pillow_decoder(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow is optional; independent scanline fixtures remain active")
        for width, height in ((1, 1), (1, 7), (7, 1), (2, 3), (9, 5), (17, 11)):
            with self.subTest(width=width, height=height):
                raw, _ = png_rows(width, height, 8, 2, 1, filters=(0, 1, 2, 3, 4))
                payload = png_from_rows(width, height, 8, 2, 1, raw=raw)
                with Image.open(io.BytesIO(payload)) as decoded:
                    self.assertEqual(decoded.size, (width, height))
                    self.assertEqual([decoded.convert("RGB").getpixel((x, y)) for y in range(height) for x in range(width)],
                                     [tuple(sample(x, y, channel, 8) for channel in range(3))
                                      for y in range(height) for x in range(width)])

    def test_dib_rejects_truncated_planes_and_inconsistent_dimensions(self):
        valid = dib(3, 2, 24, [0x123456] * 6)
        for size in (0, 4, 12, 39, 40, 63, len(valid) - 1):
            with self.subTest(length=size):
                self.invoke("read", ico([(3, 2, 24, valid[:size])]), reject=True)
        for offset, fmt, value in ((4, "<i", 2), (8, "<i", 3), (8, "<i", 0),
                                   (12, "<H", 0), (14, "<H", 48), (16, "<I", 1),
                                   (4, "<i", 0x7fffffff), (8, "<i", -2147483648)):
            changed = bytearray(valid)
            struct.pack_into(fmt, changed, offset, value)
            self.invoke("read", ico([(3, 2, 24, changed)]), reject=True)
        # A palette index outside the declared table is invalid, not implicitly black.
        invalid_index = dib(1, 1, 8, [2], palette=[0, 0xffffff])
        self.invoke("read", ico([(1, 1, 8, invalid_index)]), reject=True)


if __name__ == "__main__":
    unittest.main()
