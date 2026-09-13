/* AN Paint additions, 2026-09-13. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic;

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.zip.CRC32;

/**
 * Bounded, constant-memory container inspection; never decodes pixels or searches compressed data.
 * This is a warning hint, not an image validator. Unsupported/single-frame/malformed containers
 * return null. At the work cap, a valid prefix returns the proven frame lower bound; a count
 * below two explicitly means animation status is unknown, not that the file is static.
 * Pixel payloads and their CRCs remain the responsibility of the image decoder.
 *
 * Structures: https://www.w3.org/Graphics/GIF/spec-gif89a.txt,
 * https://www.w3.org/TR/png-3/ and
 * https://developers.google.com/speed/webp/docs/riff_container .
 */
public final class AnimationMetadata {
    private AnimationMetadata() { }
    // Chunk headers, GIF subblocks and frame subchunks all consume this shared work budget.
    private static final int MAX_BLOCKS = 100_000;

    public static final class Result {
        public final String format;
        public final int frameCount;
        public final boolean frameCountExact;
        public final boolean pngDefaultImageSeparate;
        private Result(String format, int frames, boolean exact, boolean poster) {
            this.format = format; frameCount = frames;
            frameCountExact = exact; pngDefaultImageSeparate = poster;
        }
    }

    public static Result inspect(File file) {
        try (RandomAccessFile input = new RandomAccessFile(file, "r")) {
            Reader reader = new Reader(input);
            if (reader.length < 6) return null;
            int first = input.readInt();
            int next = input.readUnsignedShort();
            if (first == tag("GIF8") && (next == 0x3961 || next == 0x3761)) return gif(reader);
            if (reader.length < 12) return null;
            if (first == 0x89504e47 && next == 0x0d0a && input.readUnsignedShort() == 0x1a0a)
                return png(reader);
            input.seek(0);
            if (input.readInt() == tag("RIFF")) {
                long end = reader.le32() + 8;
                if (input.readInt() == tag("WEBP") && end >= 12 && end <= reader.length)
                    return webp(reader, end);
            }
        } catch (IOException | SecurityException ignored) {
            // Ordinary decoding reports any actual file error. A warning probe must not block it.
        }
        return null;
    }

    private static Result result(String format, int frames, boolean exact, boolean poster) {
        return frames > 1 ? new Result(format, frames, exact, poster) : null;
    }

    private static Result gif(Reader r) throws IOException {
        RandomAccessFile in = r.input;
        r.require(7, r.length);
        int width = r.le16(), height = r.le16();
        if (width == 0 || height == 0) return null;
        int packed = in.readUnsignedByte(); r.skip(2, r.length);
        if ((packed & 0x80) != 0) r.skip(3L << ((packed & 7) + 1), r.length);
        int frames = 0;
        try {
            while (in.getFilePointer() < r.length) {
                r.block();
                int kind = in.readUnsignedByte();
                if (kind == 0x3b) return result("GIF", frames, true, false);
                if (kind == 0x21) {
                    r.require(1, r.length); in.readUnsignedByte();
                    r.subblocks();
                } else if (kind == 0x2c) {
                    r.require(9, r.length);
                    int x = r.le16(), y = r.le16(), w = r.le16(), h = r.le16();
                    packed = in.readUnsignedByte();
                    if (w == 0 || h == 0 || (long)x + w > width || (long)y + h > height) return null;
                    if ((packed & 0x80) != 0) r.skip(3L << ((packed & 7) + 1), r.length);
                    r.require(1, r.length); int lzw = in.readUnsignedByte();
                    if (lzw < 2 || lzw > 8 || !r.subblocks()) return null;
                    frames++;
                } else return null;
            }
        } catch (ScanLimit limit) { return new Result("GIF", frames, false, false); }
        return null; // Missing trailer, rather than a guessed complete frame count.
    }

    private static Result png(Reader r) throws IOException {
        RandomAccessFile in = r.input;
        r.require(25, r.length);
        if (r.be32() != 13 || in.readInt() != tag("IHDR")) return null;
        byte[] header = r.pngMetadata(tag("IHDR"), 13);
        long width = be32(header, 0), height = be32(header, 4);
        if (width == 0 || height == 0 || width > Integer.MAX_VALUE || height > Integer.MAX_VALUE) return null;
        long declared = 0, sequence = 0;
        int frames = 0;
        boolean idat = false, idatClosed = false, defaultData = false;
        boolean frame = false, frameData = false, frameUsesIdat = false, poster = false;
        try {
            while (in.getFilePointer() < r.length) {
                r.block(); r.require(12, r.length);
                long size = r.be32(); int kind = in.readInt();
                if (size > Integer.MAX_VALUE) return null;
                r.require(size + 4, r.length);
                long end = in.getFilePointer() + size + 4;
                if (kind == tag("IHDR")) return null;
                if (kind != tag("IDAT") && idat) idatClosed = true;
                if (kind == tag("acTL")) {
                    if (declared != 0 || idat || size != 8) return null;
                    byte[] data = r.pngMetadata(kind, 8); declared = be32(data, 0);
                    if (declared == 0 || declared > Integer.MAX_VALUE) return null;
                } else if (kind == tag("fcTL")) {
                    if (size != 26 || (frame && !frameData)) return null;
                    byte[] data = r.pngMetadata(kind, 26);
                    if (be32(data, 0) != sequence++) return null;
                    long w = be32(data, 4), h = be32(data, 8), x = be32(data, 12), y = be32(data, 16);
                    if (w == 0 || h == 0 || w + x > width || h + y > height ||
                        (data[24] & 255) > 2 || (data[25] & 255) > 1) return null;
                    if (!idat && (frame || w != width || h != height || x != 0 || y != 0)) return null;
                    if (frame) frames++;
                    else poster = idat;
                    frame = true; frameData = false; frameUsesIdat = !idat;
                } else if (kind == tag("IDAT")) {
                    if (idatClosed) return null;
                    idat = true;
                    if (size > 0) { defaultData = true; if (frame && frameUsesIdat) frameData = true; }
                } else if (kind == tag("fdAT")) {
                    if (declared == 0 || !idat || !frame || frameUsesIdat || size < 4 || r.be32() != sequence++) return null;
                    if (size > 4) frameData = true;
                } else if (kind == tag("IEND")) {
                    if (size != 0 || !defaultData || !frame || !frameData || declared == 0) return null;
                    r.pngMetadata(kind, 0);
                    frames++;
                    return declared == frames ? result("APNG", frames, true, poster) : null;
                }
                in.seek(end);
            }
        } catch (ScanLimit limit) {
            int found = frames + (frameData ? 1 : 0);
            return declared >= found ? new Result(declared > 0 ? "APNG" : "PNG", found, false, poster) : null;
        }
        return null;
    }

    private static Result webp(Reader r, long end) throws IOException {
        RandomAccessFile in = r.input;
        r.require(18, end);
        if (in.readInt() != tag("VP8X") || r.le32() != 10) return null;
        int flags = in.readUnsignedByte();
        r.skip(3, end);
        long width = r.le24() + 1, height = r.le24() + 1;
        if ((flags & 2) == 0) return null;
        int frames = 0; boolean anim = false;
        try {
            while (in.getFilePointer() < end) {
                r.block(); r.require(8, end);
                int kind = in.readInt(); long size = r.le32();
                r.require(size + (size & 1), end);
                long payloadEnd = in.getFilePointer() + size;
                if (kind == tag("VP8X") || kind == tag("VP8 ") || kind == tag("VP8L")) return null;
                if (kind == tag("ANIM")) {
                    if (anim || frames != 0 || size != 6) return null;
                    anim = true;
                } else if (kind == tag("ANMF")) {
                    if (!anim || size < 24) return null;
                    long x = r.le24() * 2, y = r.le24() * 2, w = r.le24() + 1, h = r.le24() + 1;
                    r.skip(4, payloadEnd); // duration and blending/disposal flags
                    if (w + x > width || h + y > height) return null;
                    boolean bitstream = false, alpha = false;
                    while (in.getFilePointer() < payloadEnd) {
                        r.block(); r.require(8, payloadEnd);
                        int sub = in.readInt(); long length = r.le32();
                        r.require(length + (length & 1), payloadEnd);
                        if (sub == tag("VP8 ") || sub == tag("VP8L")) {
                            if (bitstream || length == 0 || (sub == tag("VP8L") && alpha)) return null;
                            bitstream = true;
                        } else if (sub == tag("ALPH")) {
                            if (alpha || bitstream || length == 0) return null;
                            alpha = true;
                        }
                        r.skip(length + (length & 1), payloadEnd);
                    }
                    if (!bitstream) return null;
                    frames++;
                }
                in.seek(payloadEnd + (size & 1));
            }
            return anim ? result("WebP", frames, true, false) : null;
        } catch (ScanLimit limit) { return new Result("WebP", frames, false, false); }
    }

    private static int tag(String text) {
        return text.charAt(0) << 24 | text.charAt(1) << 16 | text.charAt(2) << 8 | text.charAt(3);
    }
    private static long be32(byte[] data, int at) {
        return (data[at] & 255L) << 24 | (data[at+1] & 255L) << 16 | (data[at+2] & 255L) << 8 | data[at+3] & 255L;
    }
    private static final class ScanLimit extends IOException { }
    private static final class Reader {
        final RandomAccessFile input; final long length; int blocks;
        Reader(RandomAccessFile input) throws IOException { this.input = input; length = input.length(); }
        void block() throws ScanLimit { if (++blocks > MAX_BLOCKS) throw new ScanLimit(); }
        void require(long amount, long end) throws IOException {
            long at = input.getFilePointer();
            if (amount < 0 || at > end || amount > end - at) throw new IOException("Truncated image container");
        }
        void skip(long amount, long end) throws IOException { require(amount, end); input.seek(input.getFilePointer() + amount); }
        int le16() throws IOException { return input.readUnsignedByte() | input.readUnsignedByte() << 8; }
        long le24() throws IOException { return le16() | (long) input.readUnsignedByte() << 16; }
        long le32() throws IOException { return le16() | (long) le16() << 16; }
        long be32() throws IOException { return input.readInt() & 0xffffffffL; }
        boolean subblocks() throws IOException {
            boolean data = false;
            while (true) {
                block(); require(1, length); int size = input.readUnsignedByte();
                if (size == 0) return data;
                data = true; skip(size, length);
            }
        }
        byte[] pngMetadata(int kind, int size) throws IOException {
            byte[] data = new byte[size]; input.readFully(data);
            CRC32 crc = new CRC32();
            crc.update(kind >>> 24); crc.update(kind >>> 16); crc.update(kind >>> 8); crc.update(kind); crc.update(data);
            if (be32() != crc.getValue()) throw new IOException("Invalid PNG control checksum");
            return data;
        }
    }
}
