/* Pocket Paint Local additions, 2026-09-07. GNU AGPL-3.0-or-later.
 * Bounded pixel cache and a one-bit visited map replace full-frame colour arrays.
 */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Color
import java.util.BitSet
import java.util.LinkedHashMap

object ScanlineFill {
    fun fill(bitmap: Bitmap, x: Int, y: Int, colour: Int, tolerance: Float) {
        val width = bitmap.width; val height = bitmap.height
        val original = bitmap.getPixel(x, y)
        val threshold = tolerance.toInt() * tolerance.toInt()
        val visited = BitSet()
        val pixels = PixelCache(bitmap)
        var stack = IntArray(1024); var size = 0
        fun push(index: Int) {
            if (size == stack.size) stack = stack.copyOf(stack.size * 2)
            stack[size++] = index
        }
        fun matches(px: Int, py: Int): Boolean {
            val index = py * width + px
            if (visited[index]) return false
            val value = pixels.get(px, py)
            if (threshold == 0) return value == original
            val a = Color.alpha(value) - Color.alpha(original)
            val r = Color.red(value) - Color.red(original)
            val g = Color.green(value) - Color.green(original)
            val b = Color.blue(value) - Color.blue(original)
            return a * a + r * r + g * g + b * b <= threshold
        }
        push(y * width + x)
        while (size > 0) {
            val seed = stack[--size]; val sy = seed / width; val sx = seed % width
            if (!matches(sx, sy)) continue
            var left = sx; var right = sx
            while (left > 0 && matches(left - 1, sy)) left--
            while (right + 1 < width && matches(right + 1, sy)) right++
            visited.set(sy * width + left, sy * width + right + 1)
            for (px in left..right) pixels.set(px, sy, colour)
            for (row in intArrayOf(sy - 1, sy + 1)) {
                if (row !in 0 until height) continue
                var inRun = false
                for (px in left..right) {
                    if (matches(px, row)) {
                        if (!inRun) push(row * width + px)
                        inRun = true
                    } else inRun = false
                }
            }
        }
        pixels.flush()
    }

    /** Eight row segments of up to 8192 pixels: at most 256 KiB of pixel copies. */
    private class PixelCache(private val bitmap: Bitmap) {
        data class Tile(val x: Int, val y: Int, val width: Int, val height: Int, val pixels: IntArray, var dirty: Boolean = false)
        private val columns = (bitmap.width + 8191) / 8192
        private val tiles = LinkedHashMap<Int, Tile>(8, .75f, true)
        private var previousKey = -1
        private var previous: Tile? = null
        private fun tile(x: Int, y: Int): Tile {
            val key = y * columns + x / 8192
            if (key == previousKey) return previous!!
            var tile = tiles[key]
            if (tile == null) {
                if (tiles.size == 8) {
                    val iterator = tiles.entries.iterator(); val old = iterator.next().value
                    write(old); iterator.remove()
                }
                val tx = x / 8192 * 8192; val ty = y
                val w = minOf(8192, bitmap.width - tx); val h = 1
                tile = Tile(tx, ty, w, h, IntArray(w * h))
                bitmap.getPixels(tile.pixels, 0, w, tx, ty, w, h); tiles[key] = tile
            }
            previousKey = key; previous = tile; return tile
        }
        fun get(x: Int, y: Int): Int { val t = tile(x, y); return t.pixels[(y - t.y) * t.width + x - t.x] }
        fun set(x: Int, y: Int, colour: Int) { val t = tile(x, y); t.pixels[(y - t.y) * t.width + x - t.x] = colour; t.dirty = true }
        private fun write(tile: Tile) {
            if (tile.dirty) { bitmap.setPixels(tile.pixels, 0, tile.width, tile.x, tile.y, tile.width, tile.height); tile.dirty = false }
        }
        fun flush() { tiles.values.forEach { write(it) } }
    }
}
