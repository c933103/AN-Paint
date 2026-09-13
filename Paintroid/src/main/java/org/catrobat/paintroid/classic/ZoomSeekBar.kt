/* AN Paint zoom control, 2026-09-09. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.widget.SeekBar

/** An unlabelled centre tick marks actual size; the status area shows current zoom. */
class ZoomSeekBar(context: Context) : SeekBar(context) {
    private val ink = Paint(Paint.ANTI_ALIAS_FLAG).apply { color=EditorColours.onSurface;textAlign=Paint.Align.CENTER }
    override fun onDraw(canvas: Canvas) {
        val density=resources.displayMetrics.density
        val centre=paddingLeft+(width-paddingLeft-paddingRight)/2f
        super.onDraw(canvas)
        ink.strokeWidth=density
        canvas.drawLine(centre,height/2f-7*density,centre,height/2f+8*density,ink)
    }
}
