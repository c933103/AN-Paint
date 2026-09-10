/* AN Paint zoom control, 2026-09-09. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.widget.SeekBar

/** A persistent centre tick labels actual size independently of the current thumb position. */
class ZoomSeekBar(context: Context) : SeekBar(context) {
    private val ink = Paint(Paint.ANTI_ALIAS_FLAG).apply { color=0xff233b4d.toInt();textAlign=Paint.Align.CENTER }
    override fun onDraw(canvas: Canvas) {
        val density=resources.displayMetrics.density
        val centre=paddingLeft+(width-paddingLeft-paddingRight)/2f
        super.onDraw(canvas)
        ink.strokeWidth=density
        canvas.drawLine(centre,height/2f-7*density,centre,height/2f+8*density,ink)
        ink.textSize=10*resources.displayMetrics.scaledDensity
        canvas.drawText(ui(R.string.ui_100),centre,11*density,ink)
    }
}
