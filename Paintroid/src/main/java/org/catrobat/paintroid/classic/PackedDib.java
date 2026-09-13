/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.RandomAccessFile;

/** Streaming packed-DIB validation and BMP wrapping; no Android or full-image allocation.
 * Layout: https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapv5header
 * Masks/palettes: https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapinfoheader
 * Only packed RGB colour tables are supported; Windows palette-handle indices need external state.
 */
public final class PackedDib {
    private PackedDib() { }
    private static boolean headerSize(long n) {
        return n == 12 || n == 40 || n == 52 || n == 56 || n == 108 || n == 124;
    }
    private static long little(RandomAccessFile in, int count) throws IOException {
        long n = 0;
        for (int i = 0; i < count; i++) {
            int b = in.read();
            if (b < 0) throw new IOException("Truncated DIB header or pixel data.");
            n |= (long) b << (8 * i);
        }
        return n;
    }
    private static long at(RandomAccessFile in, long offset, int count) throws IOException {
        in.seek(offset); return little(in, count);
    }
    private static void put(OutputStream out, long n, int count) throws IOException {
        for (int i = 0; i < count; i++) out.write((int) (n >>> (8 * i)) & 255);
    }
    private static void put(byte[] out, int offset, long n) {
        for (int i = 0; i < 4; i++) out[offset + i] = (byte) (n >>> (8 * i));
    }
    /** Signature detection intentionally recognizes truncated files, so validation reports the failure. */
    public static boolean isDib(File file) throws IOException {
        try (RandomAccessFile in = new RandomAccessFile(file, "r")) {
            return in.length() >= 4 && headerSize(little(in, 4));
        }
    }
    private static IOException invalid(String detail) { return new IOException("Invalid DIB: " + detail + "."); }
    private static void mask(long mask, long allowed, boolean required) throws IOException {
        if (mask == 0) { if (required) throw invalid("missing colour mask"); return; }
        long shifted = mask >>> Long.numberOfTrailingZeros(mask);
        if ((mask & ~allowed) != 0 || (shifted & (shifted + 1)) != 0)
            throw invalid("colour masks must contain contiguous bits within the pixel");
    }
    private static void copy(RandomAccessFile in, OutputStream out, long start, long count) throws IOException {
        in.seek(start); byte[] buffer = new byte[65536];
        while (count > 0) {
            int n = in.read(buffer, 0, (int) Math.min(buffer.length, count));
            if (n < 0) throw invalid("truncated pixel data");
            out.write(buffer, 0, n); count -= n;
        }
    }
    private static int octet(RandomAccessFile in, long end) throws IOException {
        if (in.getFilePointer() >= end) throw invalid("truncated RLE data");
        return (int) little(in, 1);
    }
    private static void index(int value, long colours) throws IOException {
        if (value >= colours) throw invalid("palette index outside the colour table");
    }
    private static void rle(RandomAccessFile in, long start, long length, int bits,
                            int width, int height, long colours) throws IOException {
        in.seek(start); long end = start + length; int x = 0, y = 0;
        while (in.getFilePointer() < end) {
            int count = octet(in, end), value = octet(in, end);
            if (count != 0) {
                if (y >= height || count > width - x) throw invalid("RLE run outside the image");
                if (bits == 8) index(value, colours);
                else { index(value >>> 4, colours); if (count > 1) index(value & 15, colours); }
                x += count;
            } else if (value == 0) {
                if (y >= height) throw invalid("RLE row outside the image");
                x = 0; y++;
            } else if (value == 1) return;
            else if (value == 2) {
                int dx = octet(in, end), dy = octet(in, end);
                if (dx > width - x || dy >= height - y) throw invalid("RLE delta outside the image");
                x += dx; y += dy;
            } else {
                if (y >= height || value > width - x) throw invalid("RLE literal outside the image");
                int bytes = bits == 8 ? value : (value + 1) / 2;
                for (int i = 0; i < bytes; i++) {
                    int b = octet(in, end);
                    if (bits == 8) index(b, colours);
                    else { index(b >>> 4, colours); if (i * 2 + 1 < value) index(b & 15, colours); }
                }
                if ((bytes & 1) != 0) octet(in, end);
                x += value;
            }
        }
        throw invalid("missing RLE end marker");
    }

    /** Add a valid BMP file header without changing original pixels, palettes, or colour meaning. */
    public static void toBmp(File file, OutputStream out) throws IOException {
        try (RandomAccessFile in = new RandomAccessFile(file, "r")) {
            long length = in.length(), header = little(in, 4);
            if (!headerSize(header)) throw new IOException("Unsupported DIB header version.");
            if (length < header) throw invalid("truncated header");
            int width, signedHeight, bits, planes;
            long compression = 0, imageSize = 0, colours = 0;
            if (header == 12) {
                width = (int) little(in, 2); signedHeight = (int) little(in, 2);
                planes = (int) little(in, 2); bits = (int) little(in, 2);
            } else {
                width = (int) little(in, 4); signedHeight = (int) little(in, 4);
                planes = (int) little(in, 2); bits = (int) little(in, 2);
                compression = little(in, 4); imageSize = little(in, 4); colours = at(in, 32, 4);
            }
            if (width <= 0 || signedHeight == 0 || signedHeight == Integer.MIN_VALUE || planes != 1)
                throw invalid("dimensions or plane count");
            if (bits != 1 && bits != 4 && bits != 8 && bits != 16 && bits != 24 && bits != 32)
                throw new IOException("Unsupported DIB pixel depth (expected 1, 4, 8, 16, 24 or 32 bits).");
            if (header == 12 && bits != 1 && bits != 4 && bits != 8 && bits != 24)
                throw new IOException("Unsupported OS/2 DIB pixel depth.");
            int height = Math.abs(signedHeight);
            boolean bitfields = compression == 3 || compression == 6;
            boolean compressed = compression == 1 || compression == 2;
            if (compression != 0 && !bitfields && !compressed)
                throw new IOException("Unsupported DIB compression (RGB, bitfields and RLE4/RLE8 are supported).");
            if ((bitfields && bits != 16 && bits != 32) || (compression == 1 && bits != 8) ||
                    (compression == 2 && bits != 4) || (compressed && signedHeight < 0))
                throw invalid("compression does not match pixel depth or orientation");
            if (header >= 108) {
                long space = at(in, 56, 4);
                // Match the existing BMP guard before changing any container bytes.
                if (space != 0x73524742L && space != 0x57696e20L)
                    throw new LegacyColourMetadata.UnsupportedColour();
            }
            int externalMasks = bitfields && header == 40 ? (compression == 6 ? 16 : 12) : 0;
            if (compression == 6 && header == 52) throw invalid("alpha bitfields require an alpha mask");
            if (bits <= 8) {
                if (colours == 0) colours = 1L << bits;
                if (colours > (1L << bits)) throw invalid("colour table too large for the pixel depth");
            }
            long offset = header + externalMasks + colours * (header == 12 ? 3 : 4);
            if (offset > length) throw invalid("truncated colour masks or palette");
            if (bitfields) {
                long red = at(in, 40, 4), green = little(in, 4), blue = little(in, 4);
                long alpha = header >= 56 || compression == 6 ? little(in, 4) : 0;
                long allowed = (1L << bits) - 1;
                mask(red, allowed, true); mask(green, allowed, true); mask(blue, allowed, true);
                mask(alpha, allowed, compression == 6);
                if ((red & green) != 0 || (red & blue) != 0 || (green & blue) != 0 ||
                        (alpha & (red | green | blue)) != 0) throw invalid("overlapping colour masks");
            }
            if (compressed) {
                long size = imageSize == 0 ? length - offset : imageSize;
                if (size > length - offset) throw invalid("truncated RLE pixel data");
                rle(in, offset, size, bits, width, height, colours);
            } else {
                long stride = (((long) width * bits + 31) / 32) * 4;
                if (stride > (length - offset) / height) throw invalid("truncated scanlines");
                if (imageSize != 0 && (imageSize < stride * height || imageSize > length - offset))
                    throw invalid("pixel-size field does not fit the scanlines");
            }
            // Normalize extended mask headers and Windows CE alpha-bitfields to V4 for Skia.
            boolean normalize = header == 52 || header == 56 || compression == 6;
            long extra = normalize ? 108 - header - externalMasks : 0;
            if (length + extra > 0xffffffffL - 14) throw new IOException("DIB exceeds the 4 GiB BMP decoder container limit.");
            out.write('B'); out.write('M'); put(out, length + extra + 14, 4);
            put(out, 0, 4); put(out, offset + extra + 14, 4);
            if (normalize) {
                byte[] expanded = new byte[108];
                in.seek(0); in.readFully(expanded, 0, (int) Math.min(header, 108));
                if (externalMasks > 0) in.readFully(expanded, 40, externalMasks);
                put(expanded, 0, 108); put(expanded, 56, 0x73524742L);
                if (compression == 6) put(expanded, 16, 3);
                out.write(expanded); copy(in, out, header + externalMasks, length - header - externalMasks);
            } else copy(in, out, 0, length);
        }
    }
}
