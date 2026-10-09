/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import kotlin.math.ceil

/** Absolute SVG document dimensions, already converted to CSS pixels by the parser. */
internal object SvgOriginalSize {
    data class Pixels(val width: Int, val height: Int)

    fun pixels(width: Double, height: Double): Pixels {
        fun dimension(value: Double): Int {
            require(value.isFinite() && value > 0) {
                "The SVG does not declare a usable original size. No canvas-based size was substituted."
            }
            // Bitmap dimensions are integral. Cover a fractional final pixel instead of clipping it.
            val pixels = ceil(value)
            require(pixels <= Int.MAX_VALUE.toDouble()) {
                "The original SVG size exceeds Android bitmap dimensions. No resizing was applied."
            }
            return pixels.toInt()
        }
        return Pixels(dimension(width), dimension(height))
    }
}
