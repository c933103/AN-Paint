/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later.
 * Original hexagonal colour geometry; no third-party artwork or font assets.
 */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.view.View
import android.view.ViewGroup
import android.view.MotionEvent
import androidx.core.graphics.ColorUtils
import java.util.Locale
import kotlin.math.*

/** 127 chromatic hexagons and 13 greys. Every swatch is a labelled, focusable view. */
class HoneycombPalette(context: Context, private val value: ColourValue, private val changed: () -> Unit) : ViewGroup(context) {
    private data class Cell(val q: Int, val r: Int, val colour: Int, val grey: Boolean = false)
    private val cells = mutableListOf<Cell>()
    init {
        contentDescription = "Honeycomb colour swatches with a greyscale row"
        for (r in -6..6) for (q in max(-6, -r - 6)..min(6, -r + 6)) {
            val ring = maxOf(abs(q), abs(r), abs(-q-r))
            val x = sqrt(3.0) * (q + r / 2.0); val y = 1.5 * r
            val hue = ((atan2(y, x) * 180 / PI + 360) % 360).toFloat()
            val colour = if (ring == 0) Color.WHITE else ColorUtils.HSLToColor(floatArrayOf(hue, 1f, 1f - ring / 12f))
            cells.add(Cell(q, r, colour))
        }
        repeat(13) { i -> val c = (255 * (12 - i) / 12f).roundToInt(); cells.add(Cell(i, 0, Color.rgb(c,c,c), true)) }
        cells.forEachIndexed { index, cell ->
            addView(object : View(context) {
                private val shape = Path()
                private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
                init {
                    tag = "honeycomb_colour_$index"; isFocusable = true; isClickable = true
                    contentDescription = String.format(Locale.ROOT, "Honeycomb colour #%06X", cell.colour and 0xffffff)
                    setOnClickListener { value.rgb(cell.colour); invalidateSelection(); changed() }
                    setOnFocusChangeListener { _, _ -> invalidate() }
                }
                override fun onDraw(canvas: Canvas) {
                    shape.reset()
                    val radius = min(width / sqrt(3f), height / 2f) - 1f
                    for (corner in 0..5) {
                        val angle = (corner * 60 - 90) * PI / 180
                        val x = width / 2f + cos(angle).toFloat() * radius
                        val y = height / 2f + sin(angle).toFloat() * radius
                        if (corner == 0) shape.moveTo(x,y) else shape.lineTo(x,y)
                    }
                    shape.close(); paint.style = Paint.Style.FILL; paint.color = cell.colour; canvas.drawPath(shape,paint)
                    paint.style = Paint.Style.STROKE; paint.strokeWidth = 1f; paint.color = 0xff808080.toInt(); canvas.drawPath(shape,paint)
                    if ((value.colour or 0xff000000.toInt()) == cell.colour || isFocused) {
                        paint.strokeWidth = 5f; paint.color = Color.BLACK; canvas.drawPath(shape,paint)
                        paint.strokeWidth = 2f; paint.color = Color.WHITE; canvas.drawPath(shape,paint)
                    }
                }
                override fun onTouchEvent(event: MotionEvent): Boolean {
                    if (event.actionMasked == MotionEvent.ACTION_DOWN) {
                        val radius = min(width / sqrt(3f), height / 2f) - 1f
                        val dx = abs(event.x - width / 2f); val dy = abs(event.y - height / 2f)
                        if (dx > sqrt(3f) * radius / 2 || dy > radius - dx / sqrt(3f)) return false
                    }
                    return super.onTouchEvent(event)
                }
            })
        }
    }
    fun invalidateSelection() { for (i in 0 until childCount) getChildAt(i).invalidate() }
    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        setMeasuredDimension(MeasureSpec.getSize(widthMeasureSpec), resolveSize((278 * resources.displayMetrics.density).roundToInt(), heightMeasureSpec))
        val radius = min(measuredWidth / (13 * sqrt(3f)), measuredHeight / 24f)
        for (i in 0 until childCount) getChildAt(i).measure(MeasureSpec.makeMeasureSpec((sqrt(3f)*radius).roundToInt(), MeasureSpec.EXACTLY), MeasureSpec.makeMeasureSpec((2*radius).roundToInt(), MeasureSpec.EXACTLY))
    }
    override fun onLayout(changed: Boolean, left: Int, top: Int, right: Int, bottom: Int) {
        val radius = min(width / (13 * sqrt(3f)), height / 24f)
        cells.forEachIndexed { index, cell ->
            val view = getChildAt(index)
            val x = width / 2f + sqrt(3f) * radius * if (cell.grey) cell.q - 6f else cell.q + cell.r / 2f
            val y = if (cell.grey) 22 * radius else 10 * radius + 1.5f * radius * cell.r
            val l = (x - view.measuredWidth / 2f).roundToInt(); val t = (y - view.measuredHeight / 2f).roundToInt()
            view.layout(l,t,l + view.measuredWidth,t + view.measuredHeight)
        }
    }
}
