/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import kotlin.math.ceil

/** Absolute SVG document dimensions, already converted to CSS pixels by the parser. */
internal object SvgOriginalSize {
    data class Pixels(val width: Int, val height: Int)

    // Keep this dimension-only helper independent of Android resources. The gallery
    // translates these app-authored failures at the user-facing error boundary.
    enum class Reason { UNUSABLE_ORIGINAL_SIZE, EXCEEDS_BITMAP_DIMENSIONS }
    class SizeException(val reason: Reason) : IllegalArgumentException()

    fun pixels(width: Double, height: Double): Pixels {
        fun dimension(value: Double): Int {
            if (!value.isFinite() || value <= 0) throw SizeException(Reason.UNUSABLE_ORIGINAL_SIZE)
            // Bitmap dimensions are integral. Cover a fractional final pixel instead of clipping it.
            val pixels = ceil(value)
            if (pixels > Int.MAX_VALUE.toDouble()) throw SizeException(Reason.EXCEEDS_BITMAP_DIMENSIONS)
            return pixels.toInt()
        }
        return Pixels(dimension(width), dimension(height))
    }
}
