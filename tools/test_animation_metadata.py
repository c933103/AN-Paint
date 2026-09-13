#!/usr/bin/env python3
"""Exercise the production Java animation scanner with self-contained container fixtures."""
import base64
import pathlib
import shutil
import struct
import subprocess
import tempfile
import unittest
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic/AnimationMetadata.java"
JAVA = shutil.which("java") or "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
HARNESS = r'''
import org.catrobat.paintroid.classic.AnimationMetadata;
import java.io.File;
public class ScanAnimation {
    public static void main(String[] paths) throws Exception {
        for(String path:paths) {
            AnimationMetadata.Result r=AnimationMetadata.inspect(new File(path));
            System.out.println(r==null?"none":r.format+"|"+r.frameCount+"|"+r.frameCountExact+"|"+r.pngDefaultImageSeparate);
        }
    }
}
'''
PNG = b"\x89PNG\r\n\x1a\n"

def chunk(name, data):
    return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data))

def png_header():
    return PNG + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))

def ctl(sequence):
    return chunk(b"fcTL", struct.pack(">IIIIIHHBB", sequence, 1, 1, 0, 0, 1, 10, 0, 0))

def pixels(colour):
    return zlib.compress(b"\0" + bytes(colour))

def apng(frames=2, poster=False, empty_data_chunks=False):
    data = png_header() + chunk(b"acTL", struct.pack(">II", frames, 0))
    seq = 0
    if poster:
        data += chunk(b"IDAT", pixels((0, 255, 0, 255)))
    for n in range(frames):
        data += ctl(seq)
        seq += 1
        image = pixels((255 if n % 2 == 0 else 0, 0, 255 if n % 2 else 0, 255))
        if n == 0 and not poster:
            data += chunk(b"IDAT", image)
        else:
            if empty_data_chunks:
                data += chunk(b"fdAT", struct.pack(">I", seq))
                seq += 1
            data += chunk(b"fdAT", struct.pack(">I", seq) + image)
            seq += 1
    return data + chunk(b"IEND", b"")

# A complete 1x1 black/white GIF, using explicit valid LZW clear/index/end codes.
GIF_HEADER = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff"
def gif_frame(white=False, local=False):
    return (b",\0\0\0\0\x01\0\x01\0" + (b"\x80\0\0\0\xff\xff\xff" if local else b"\0") +
            b"\x02\x02" + (b"L" if white else b"D") + b"\x01\0")

def gif(frames=2, local=False):
    return GIF_HEADER + b"".join(b"!\xf9\x04\0\x0a\0\0\0" + gif_frame(i % 2 != 0, local) for i in range(frames)) + b";"

def riff_chunk(name, data):
    return name + struct.pack("<I", len(data)) + data + (b"\0" if len(data) % 2 else b"")

def riff(data):
    return b"RIFF" + struct.pack("<I", len(data) + 4) + b"WEBP" + data

# Real 1x1 red/blue lossless WebP payloads produced by Pillow/libwebp; no dependency
# is needed to run these tests. Outer RIFF headers are removed for frame muxing.
WEBP_PAYLOADS = [base64.b64decode(s)[12:] for s in (
    "UklGRhwAAABXRUJQVlA4TA8AAAAvAAAAAAcQ/Y/+ByKi/wEA",
    "UklGRhwAAABXRUJQVlA4TA8AAAAvAAAAAAcQ0f/+ByKi/wEA",
)]
def webp(frames=2):
    data = riff_chunk(b"VP8X", b"\x02" + b"\0" * 9) + riff_chunk(b"ANIM", b"\0" * 6)
    for i in range(frames):
        data += riff_chunk(b"ANMF", b"\0" * 12 + b"\x64\0\0\x02" + WEBP_PAYLOADS[i % 2])
    return riff(data)

class AnimationMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="anpaint-animation-")
        cls.folder = pathlib.Path(cls.temp.name)
        harness = cls.folder / "ScanAnimation.java"
        harness.write_text(HARNESS)
        subprocess.run([JAVA, "-m", "jdk.compiler/com.sun.tools.javac.Main", "-d", str(cls.folder), str(SOURCE), str(harness)], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def scan(self, *images):
        paths = []
        for n, data in enumerate(images):
            path = self.folder / f"fixture-{n}.unrelated-extension"
            path.write_bytes(data)
            paths.append(str(path))
        return subprocess.run([JAVA, "-cp", str(self.folder), "ScanAnimation", *paths],
                              check=True, capture_output=True, text=True, timeout=12).stdout.splitlines()

    def test_gif_actual_frames_global_and_local_palettes(self):
        self.assertEqual(self.scan(gif(1), gif(2), gif(3, True), gif(2).replace(b"89a", b"87a", 1)),
                         ["none", "GIF|2|true|false", "GIF|3|true|false", "GIF|2|true|false"])

    def test_gif_extensions_and_compressed_bytes_are_not_frame_markers(self):
        decoy = b"!\xfe\x08,;!GIF89\0"
        self.assertEqual(self.scan(GIF_HEADER + decoy + gif_frame() + b";",
                                   GIF_HEADER + decoy + gif_frame() + gif_frame(True) + b";"),
                         ["none", "GIF|2|true|false"])
        # Same marker bytes in one image's LZW subblock are skipped as payload.
        fake_pixels = GIF_HEADER + b",\0\0\0\0\x01\0\x01\0\0\x02\x04,,;;\0;"
        self.assertEqual(self.scan(fake_pixels), ["none"])

    def test_apng_exact_frames_and_separate_default_poster(self):
        self.assertEqual(self.scan(apng(1), apng(2), apng(3, True), apng(2, False, True)),
                         ["none", "APNG|2|true|false", "APNG|3|true|true", "APNG|2|true|false"])

    def test_png_fake_animation_names_inside_data_or_text_do_not_warn(self):
        still = png_header() + chunk(b"tEXt", b"Comment\0acTLfcTLfdAT") + chunk(b"IDAT", pixels((0, 0, 0, 255))) + chunk(b"IEND", b"")
        self.assertEqual(self.scan(still, png_header() + chunk(b"IDAT", b"acTLfcTLfcTLfdAT") + chunk(b"IEND", b"")), ["none", "none"])

    def test_apng_requires_matching_count_sequence_data_and_control_crc(self):
        valid = apng()
        count_bad = valid.replace(chunk(b"acTL", struct.pack(">II", 2, 0)), chunk(b"acTL", struct.pack(">II", 20, 0)))
        sequence_bad = valid.replace(ctl(1), ctl(9))
        crc_bad = bytearray(valid)
        crc_bad[valid.index(b"acTL") + 4] ^= 1
        missing_data = valid.replace(chunk(b"fdAT", struct.pack(">I", 2) + pixels((0, 0, 255, 255))), b"")
        late_control = png_header() + chunk(b"IDAT", pixels((1, 2, 3, 255))) + chunk(b"acTL", struct.pack(">II", 2, 0)) + chunk(b"IEND", b"")
        self.assertEqual(self.scan(count_bad, sequence_bad, bytes(crc_bad), missing_data, late_control), ["none"] * 5)

    def test_webp_requires_animation_flag_header_and_real_frame_subchunks(self):
        self.assertEqual(self.scan(riff(WEBP_PAYLOADS[0]), webp(1), webp(2), webp(3)),
                         ["none", "none", "WebP|2|true|false", "WebP|3|true|false"])
        no_flag = bytearray(webp()); no_flag[20] = 0
        no_anim = webp().replace(riff_chunk(b"ANIM", b"\0" * 6), b"")
        no_anim = no_anim[:4] + struct.pack("<I", len(no_anim) - 8) + no_anim[8:]
        missing_sub = riff(riff_chunk(b"VP8X", b"\x02" + b"\0" * 9) + riff_chunk(b"ANIM", b"\0" * 6) +
                           riff_chunk(b"ANMF", b"\0" * 16 + riff_chunk(b"JUNK", b"ANMFANMF")) * 2)
        self.assertEqual(self.scan(bytes(no_flag), no_anim, missing_sub), ["none"] * 3)

    def test_webp_metadata_and_unknown_frame_subchunks_do_not_count_as_frames(self):
        data = webp(1)[12:] + riff_chunk(b"XMP ", b"ANMFANMFANMF")
        self.assertEqual(self.scan(riff(data)), ["none"])
        padded = webp(2)[12:] + riff_chunk(b"JUNK", b"x")
        self.assertEqual(self.scan(riff(padded)), ["WebP|2|true|false"])

    def test_truncated_headers_chunks_and_frames_return_no_guess(self):
        fixtures = [gif(), apng(), webp()]
        for fixture in fixtures:
            # Every proper prefix is truncated; none can imply a complete container.
            self.assertEqual(self.scan(*(fixture[:n] for n in range(len(fixture)))), ["none"] * len(fixture))
        bad_riff = webp()[:4] + b"\xff" * 4 + webp()[8:]
        bad_png = png_header() + b"\x7f\xff\xff\xffacTL"
        self.assertEqual(self.scan(bad_riff, bad_png, b"not an image", b""), ["none"] * 4)

    def test_work_cap_retains_only_proven_frame_lower_bound(self):
        # 100,000 subblocks/chunks is the production cap, independent of file size.
        trailer = b"!\xfe\x01x\0" * 100_001
        self.assertEqual(self.scan(GIF_HEADER + gif_frame() * 2 + trailer + b";"), ["GIF|2|false|false"])
        self.assertEqual(self.scan(GIF_HEADER + trailer + gif_frame() * 2 + b";"), ["GIF|0|false|false"])
        self.assertEqual(self.scan(GIF_HEADER + gif_frame() + trailer + gif_frame() + b";"), ["GIF|1|false|false"])
        many_chunks = webp(2)[12:] + riff_chunk(b"JUNK", b"") * 100_001
        self.assertEqual(self.scan(riff(many_chunks)), ["WebP|2|false|false"])

    def test_work_cap_before_animation_is_proven_returns_uncertainty_not_static(self):
        junk = chunk(b"tEXt", b"") * 100_001
        animated = apng()
        # The first 53 bytes contain the signature, IHDR and acTL. Later actual
        # frames remain valid but are beyond the deliberately bounded scan.
        self.assertEqual(self.scan(animated[:53] + junk + animated[53:]), ["APNG|0|false|false"])
        ordinary = png_header() + junk + chunk(b"IDAT", pixels((255, 0, 0, 255))) + chunk(b"IEND", b"")
        self.assertEqual(self.scan(ordinary), ["PNG|0|false|false"])
        payload = webp()[12:]
        # VP8X (18 bytes) retains its animation flag, before ANIM/ANMF arrives.
        delayed = riff(payload[:18] + riff_chunk(b"JUNK", b"") * 100_001 + payload[18:])
        self.assertEqual(self.scan(delayed), ["WebP|0|false|false"])
        self.assertEqual(self.scan(gif(frames=1)), ["none"])

    def test_sparse_large_chunk_is_skipped_without_reading_pixel_payload(self):
        path = self.folder / "large-sparse-png.unknown"
        initial = apng()[:-12]
        with path.open("wb") as out:
            out.write(initial)
            out.write(struct.pack(">I", 1 << 30) + b"tEXt")
            out.seek((1 << 30) + 4, 1)  # skipped metadata payload and CRC
            out.write(chunk(b"IEND", b""))
        result = subprocess.run([JAVA, "-Xmx24m", "-cp", str(self.folder), "ScanAnimation", str(path)],
                                check=True, capture_output=True, text=True, timeout=5).stdout.strip()
        self.assertEqual(result, "APNG|2|true|false")

if __name__ == "__main__":
    unittest.main()
