/* AN Paint, 2026. GNU AGPL-3.0-or-later.
 * Original streaming BMP/GIF encoders, based on the public file-format specifications.
 * GIF format and service mark: CompuServe Incorporated.
 */
package org.catrobat.paintroid.classic;

import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** No Android dependency: encode rows with bounded scratch space, never a second full image. */
public final class LegacyImageEncoder {
    private LegacyImageEncoder() { }
    public interface Rows { void read(int y, int[] pixels); }
    public static final class Failure extends IOException {
        public final int reason;
        Failure(int reason, String message) { super(message); this.reason = reason; }
    }

    private static void check(int width, int height, long budget, long scratch) throws IOException {
        long pixels = (long) width * height;
        if (width <= 0 || height <= 0 || pixels > (Integer.MAX_VALUE - 8L) / 4 ||
                scratch > budget || pixels * 4 > budget - scratch) {
            throw new Failure(0, "The image and encoding buffers exceed the export memory budget.");
        }
    }
    private static void little(OutputStream out, long number, int count) throws IOException {
        for (int i = 0; i < count; i++) out.write((int) (number >>> (i * 8)) & 255);
    }

    /** BITMAPINFOHEADER, uncompressed BGR, padded scanlines stored bottom first. */
    public static void bmp(int width, int height, Rows rows, OutputStream out, long budget) throws IOException {
        long stride = ((long) width * 3 + 3) & ~3L;
        long bytes = stride * height;
        check(width, height, budget, stride + (long) width * 4 + 65536);
        if (stride > Integer.MAX_VALUE - 8 || bytes > 0xffffffffL - 54)
            throw new Failure(1, "The image exceeds the BMP file-size limit.");
        out.write('B'); out.write('M'); little(out, bytes + 54, 4);
        little(out, 0, 4); little(out, 54, 4); little(out, 40, 4);
        little(out, width, 4); little(out, height, 4); little(out, 1, 2); little(out, 24, 2);
        little(out, 0, 4); little(out, bytes, 4);
        little(out, 0, 4); little(out, 0, 4); little(out, 0, 4); little(out, 0, 4);
        int[] pixels = new int[width]; byte[] row = new byte[(int) stride];
        for (int y = height - 1; y >= 0; y--) {
            rows.read(y, pixels);
            for (int x = 0, i = 0; x < width; x++) {
                int colour = pixels[x];
                row[i++] = (byte) colour; row[i++] = (byte) (colour >>> 8); row[i++] = (byte) (colour >>> 16);
            }
            out.write(row);
        }
    }

    private static int bucket(int colour) {
        return ((colour >>> 9) & 0x7c00) | ((colour >>> 6) & 0x3e0) | ((colour >>> 3) & 31);
    }
    private static int channel(int colour, int shift) { return (colour >>> shift) & 255; }

    private static final class ColourBox {
        final List<Integer> bins;
        final int axis;
        final long weight;
        final int range;
        ColourBox(List<Integer> bins, int[] counts) {
            this.bins = bins;
            int[] lo = {31, 31, 31}, hi = {0, 0, 0}; long population = 0;
            for (int bin : bins) {
                population += counts[bin];
                for (int axis = 0; axis < 3; axis++) {
                    int value = (bin >>> ((2 - axis) * 5)) & 31;
                    lo[axis] = Math.min(lo[axis], value); hi[axis] = Math.max(hi[axis], value);
                }
            }
            int chosen = 0;
            for (int axis = 1; axis < 3; axis++) if (hi[axis] - lo[axis] > hi[chosen] - lo[chosen]) chosen = axis;
            axis = chosen; range = hi[chosen] - lo[chosen]; weight = population;
        }
    }
    private static int[] palette(int[] counts, long[][] sums) {
        List<Integer> bins = new ArrayList<>();
        for (int i = 0; i < counts.length; i++) if (counts[i] != 0) bins.add(i);
        List<ColourBox> boxes = new ArrayList<>(); boxes.add(new ColourBox(bins, counts));
        while (boxes.size() < 256) {
            ColourBox chosen = null;
            for (ColourBox box : boxes) if (box.bins.size() > 1 &&
                    (chosen == null || box.weight * box.range > chosen.weight * chosen.range)) chosen = box;
            if (chosen == null) break;
            final int shift = (2 - chosen.axis) * 5;
            Collections.sort(chosen.bins, (a, b) -> Integer.compare((a >>> shift) & 31, (b >>> shift) & 31));
            long half = (chosen.weight + 1) / 2, population = 0; int cut = 0;
            do { population += counts[chosen.bins.get(cut++)]; }
            while (cut < chosen.bins.size() - 1 && population < half);
            boxes.remove(chosen);
            boxes.add(new ColourBox(new ArrayList<>(chosen.bins.subList(0, cut)), counts));
            boxes.add(new ColourBox(new ArrayList<>(chosen.bins.subList(cut, chosen.bins.size())), counts));
        }
        int[] result = new int[boxes.size()];
        for (int i = 0; i < result.length; i++) {
            ColourBox box = boxes.get(i); int colour = 0;
            for (int axis = 0; axis < 3; axis++) {
                long total = 0;
                for (int bin : box.bins) total += sums[axis][bin];
                colour |= (int) ((total + box.weight / 2) / box.weight) << ((2 - axis) * 8);
            }
            result[i] = colour;
        }
        return result;
    }
    private static int nearest(int rgb, int[] palette) {
        int r = channel(rgb, 16), g = channel(rgb, 8), b = channel(rgb, 0);
        int best = 0, distance = Integer.MAX_VALUE;
        for (int i = 0; i < palette.length; i++) {
            int dr = r - channel(palette[i], 16), dg = g - channel(palette[i], 8), db = b - channel(palette[i], 0);
            int d = 3 * dr * dr + 4 * dg * dg + 2 * db * db;
            if (d < distance) { best = i; distance = d; }
        }
        return best;
    }

    /** One still frame, exact palette for <=256 distinct colours; otherwise weighted median-cut + optional Floyd–Steinberg dithering. */
    public static void gif(int width, int height, Rows rows, OutputStream out, long budget, boolean dither) throws IOException {
        if (width > 65535 || height > 65535) throw new Failure(2, "GIF dimensions cannot exceed 65,535 pixels per side.");
        // Histogram, boxed median-cut lists, LZW table, row and two RGB error rows.
        check(width, height, budget, 8L * 1024 * 1024 + (long) width * 28);
        int[] pixels = new int[width], counts = new int[32768]; long[][] sums = new long[3][32768];
        Map<Integer, Integer> exact = new LinkedHashMap<>(); boolean exactPalette = true;
        for (int y = 0; y < height; y++) {
            rows.read(y, pixels);
            for (int pixel : pixels) {
                int rgb = pixel & 0xffffff;
                if (exactPalette && !exact.containsKey(rgb)) {
                    if (exact.size() < 256) exact.put(rgb, exact.size()); else { exactPalette = false; exact.clear(); }
                }
                int bin = bucket(rgb); counts[bin]++;
                sums[0][bin] += channel(rgb, 16); sums[1][bin] += channel(rgb, 8); sums[2][bin] += channel(rgb, 0);
            }
        }
        int[] palette;
        if (exactPalette) { palette = new int[exact.size()]; for (Map.Entry<Integer, Integer> entry : exact.entrySet()) palette[entry.getValue()] = entry.getKey(); }
        else palette = palette(counts, sums);
        int[] lookup = new int[32768]; Arrays.fill(lookup, -1);
        int bits = 1; while ((1 << bits) < palette.length) bits++;
        out.write(new byte[] {'G', 'I', 'F', '8', '7', 'a'});
        little(out, width, 2); little(out, height, 2);
        out.write(0x80 | 0x70 | (bits - 1)); out.write(0); out.write(0);
        for (int i = 0; i < (1 << bits); i++) {
            int rgb = i < palette.length ? palette[i] : 0;
            out.write(channel(rgb, 16)); out.write(channel(rgb, 8)); out.write(channel(rgb, 0));
        }
        out.write(0x2c); little(out, 0, 2); little(out, 0, 2);
        little(out, width, 2); little(out, height, 2); out.write(0);
        Lzw codes = new Lzw(out, Math.max(2, bits));
        boolean diffuse = dither && !exactPalette;
        int[] current = diffuse ? new int[(width + 2) * 3] : null;
        int[] next = diffuse ? new int[(width + 2) * 3] : null;
        for (int y = 0; y < height; y++) {
            rows.read(y, pixels);
            for (int x = 0; x < width; x++) {
                int rgb = pixels[x] & 0xffffff;
                if (diffuse) {
                    int adjusted = 0;
                    for (int axis = 0; axis < 3; axis++) adjusted |= Math.max(0, Math.min(255,
                            channel(rgb, (2 - axis) * 8) + Math.round(current[(x + 1) * 3 + axis] / 16f))) << ((2 - axis) * 8);
                    rgb = adjusted;
                }
                int index;
                if (exactPalette) index = exact.get(rgb);
                else {
                    int bin = bucket(rgb); index = lookup[bin];
                    if (index < 0) {
                        int centre = (((bin >>> 10) * 8 + 4) << 16) | ((((bin >>> 5) & 31) * 8 + 4) << 8) | ((bin & 31) * 8 + 4);
                        index = nearest(centre, palette); lookup[bin] = index;
                    }
                }
                codes.pixel(index);
                if (diffuse) for (int axis = 0; axis < 3; axis++) {
                    int error = channel(rgb, (2 - axis) * 8) - channel(palette[index], (2 - axis) * 8);
                    current[(x + 2) * 3 + axis] += error * 7;
                    next[x * 3 + axis] += error * 3;
                    next[(x + 1) * 3 + axis] += error * 5;
                    next[(x + 2) * 3 + axis] += error;
                }
            }
            if (diffuse) { int[] swap = current; current = next; next = swap; Arrays.fill(next, 0); }
        }
        codes.finish(); out.write(0x3b);
    }

    /** GIF little-endian variable-width LZW with dictionary reset at 4096 entries. */
    private static final class Lzw {
        final OutputStream out; final int minimum, clear, end;
        final Map<Integer, Integer> table = new HashMap<>(8192);
        final byte[] block = new byte[255];
        int next, width, prefix = -1, accumulator, bitCount, blockLength;
        Lzw(OutputStream out, int minimum) throws IOException {
            this.out = out; this.minimum = minimum; clear = 1 << minimum; end = clear + 1;
            reset(); out.write(minimum); code(clear);
        }
        void reset() { table.clear(); next = end + 1; width = minimum + 1; }
        void pixel(int value) throws IOException {
            if (prefix < 0) { prefix = value; return; }
            int key = (prefix << 8) | value; Integer found = table.get(key);
            if (found != null) { prefix = found; return; }
            code(prefix);
            if (next < 4096) {
                if (next == (1 << width)) width++;
                table.put(key, next++);
            } else { code(clear); reset(); }
            prefix = value;
        }
        void code(int code) throws IOException {
            accumulator |= code << bitCount; bitCount += width;
            while (bitCount >= 8) { data(accumulator & 255); accumulator >>>= 8; bitCount -= 8; }
        }
        void data(int value) throws IOException {
            block[blockLength++] = (byte) value;
            if (blockLength == 255) flush();
        }
        void flush() throws IOException { if (blockLength != 0) { out.write(blockLength); out.write(block, 0, blockLength); blockLength = 0; } }
        void finish() throws IOException {
            if (prefix >= 0) { code(prefix); if (next == (1 << width) && width < 12) width++; }
            code(end); if (bitCount > 0) data(accumulator & 255); flush(); out.write(0);
        }
    }
}
