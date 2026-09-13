/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

/** One coordinate model for clamping, thumb drawing and thumb dragging. */
internal data class ViewportAxis(val viewport: Float, val start: Float, val end: Float, val padding: Float) {
    private val length = (end - start).coerceAtLeast(0f)
    private val centred = (viewport - length) / 2f - start
    val fits = length + 2 * padding <= viewport
    val minimum = if (fits) centred else viewport - end - padding
    val maximum = if (fits) centred else -start + padding
    val range get() = (maximum - minimum).coerceAtLeast(0f)
    fun clamp(pan: Float) = if (pan.isFinite()) pan.coerceIn(minimum, maximum) else centred.coerceIn(minimum, maximum)
    fun thumbSize(minimumSize: Float): Float = if (range == 0f) viewport else
        (viewport * viewport / (viewport + range)).coerceIn(minimumSize.coerceAtMost(viewport), viewport)
    fun thumbStart(pan: Float, thumb: Float) = if (range == 0f) 0f else
        (maximum - clamp(pan)) / range * (viewport - thumb)
    fun panForThumb(position: Float, thumb: Float) = if (range == 0f || viewport <= thumb) maximum else
        maximum - (position / (viewport - thumb)).coerceIn(0f, 1f) * range
}
