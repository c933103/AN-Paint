/*
 * Paintroid: An image manipulation application for Android.
 * Copyright (C) 2010-2022 The Catrobat Team
 * (<http://developer.catrobat.org/credits>)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
// Adapted for AN Paint, 2026. CursorTool at 853ce3c346910ea73aa4de5514f2a76ace1396fb.
package org.catrobat.paintroid.classic

import android.graphics.*
import android.graphics.Paint.Cap
import kotlin.math.max

/** Paintroid's brush-sized circle/square and alternating four-part crosshairs. */
internal class PaintroidCursorOverlay {
    private val linePaint=Paint(Paint.ANTI_ALIAS_FLAG)
    private val toolPosition=PointF()
    private var toolPaint=Paint()
    private var zoom=1f
    private var density=1f
    private var markerScale=1f
    private val cursorToolPrimaryShapeColor=Color.rgb(85,85,85)
    private var cursorToolSecondaryShapeColor=Color.LTGRAY
    fun draw(canvas: Canvas,position: PointF,paint: Paint,scale: Float,pixelDensity: Float,drawing: Boolean,visibilityScale: Float=1f,outlineCap: Cap=paint.strokeCap) {
        toolPosition.set(position);toolPaint=Paint(paint).apply {strokeCap=outlineCap};zoom=scale;density=pixelDensity
        markerScale=visibilityScale.coerceIn(1f,2f)
        cursorToolSecondaryShapeColor=if(drawing) paint.color else Color.LTGRAY
        drawShape(canvas)
    }
    // Keep a compact sight visible at fit-to-image zoom. Brush radius remains in
    // image pixels; neither the visibility setting nor the lens changes the ink.
    private fun getStrokeWidthForZoom(default: Float)=default*density*markerScale/zoom
    private fun drawCircle(
        canvas: Canvas,
        strokeWidth: Float,
        outerCircleRadius: Float,
        innerCircleRadius: Float
    ) {
        canvas.drawCircle(toolPosition.x, toolPosition.y, outerCircleRadius, linePaint)
        linePaint.color = Color.LTGRAY
        canvas.drawCircle(toolPosition.x, toolPosition.y, innerCircleRadius, linePaint)
        linePaint.color = Color.TRANSPARENT
        linePaint.style = Paint.Style.FILL
        canvas.drawCircle(
            toolPosition.x,
            toolPosition.y,
            innerCircleRadius - strokeWidth / 2f,
            linePaint
        )
    }

    private fun drawRect(
        canvas: Canvas,
        strokeWidth: Float,
        outerCircleRadius: Float,
        innerCircleRadius: Float
    ) {
        val strokeRect = RectF(
            toolPosition.x - outerCircleRadius,
            toolPosition.y - outerCircleRadius,
            toolPosition.x + outerCircleRadius,
            toolPosition.y + outerCircleRadius
        )
        canvas.drawRect(strokeRect, linePaint)
        strokeRect.set(
            toolPosition.x - innerCircleRadius,
            toolPosition.y - innerCircleRadius,
            toolPosition.x + innerCircleRadius,
            toolPosition.y + innerCircleRadius
        )
        linePaint.color = Color.LTGRAY
        canvas.drawRect(strokeRect, linePaint)
        linePaint.color = Color.TRANSPARENT
        linePaint.style = Paint.Style.FILL
        strokeRect.set(
            toolPosition.x - innerCircleRadius + strokeWidth / 2f,
            toolPosition.y - innerCircleRadius + strokeWidth / 2f,
            toolPosition.x + innerCircleRadius - strokeWidth / 2f,
            toolPosition.y + innerCircleRadius - strokeWidth / 2f
        )
        canvas.drawRect(strokeRect, linePaint)
    }

    private fun drawShape(canvas: Canvas) {
        val brushStrokeWidth = max(toolPaint.strokeWidth / 2f, 1f)
        val strokeWidth = getStrokeWidthForZoom(DEFAULT_TOOL_STROKE_WIDTH)
        val cursorPartLength = strokeWidth * 2
        val innerCircleRadius = brushStrokeWidth + strokeWidth / 2f
        val outerCircleRadius = innerCircleRadius + strokeWidth
        linePaint.apply {
            color = cursorToolPrimaryShapeColor
            style = Paint.Style.STROKE
            this.strokeWidth = strokeWidth
        }
        val strokeCap = toolPaint.strokeCap
        if (strokeCap == Cap.ROUND) {
            drawCircle(canvas, strokeWidth, outerCircleRadius, innerCircleRadius)
        } else {
            drawRect(canvas, strokeWidth, outerCircleRadius, innerCircleRadius)
        }

        linePaint.style = Paint.Style.FILL
        var startLineLengthAddition = strokeWidth / 2f
        var endLineLengthAddition = cursorPartLength + strokeWidth
        var lineNr = 0
        while (lineNr < CURSOR_LINES) {
            if (lineNr % 2 == 0) {
                linePaint.color = cursorToolSecondaryShapeColor
            } else {
                linePaint.color = cursorToolPrimaryShapeColor
            }

            canvas.drawLine(
                toolPosition.x - outerCircleRadius - startLineLengthAddition,
                toolPosition.y,
                toolPosition.x - outerCircleRadius - endLineLengthAddition,
                toolPosition.y,
                linePaint
            )
            canvas.drawLine(
                toolPosition.x + outerCircleRadius + startLineLengthAddition,
                toolPosition.y,
                toolPosition.x + outerCircleRadius + endLineLengthAddition,
                toolPosition.y,
                linePaint
            )
            canvas.drawLine(
                toolPosition.x,
                toolPosition.y + outerCircleRadius + startLineLengthAddition,
                toolPosition.x,
                toolPosition.y + outerCircleRadius + endLineLengthAddition,
                linePaint
            )
            canvas.drawLine(
                toolPosition.x,
                toolPosition.y - outerCircleRadius - startLineLengthAddition,
                toolPosition.x,
                toolPosition.y - outerCircleRadius - endLineLengthAddition,
                linePaint
            )
            lineNr++
            startLineLengthAddition = strokeWidth / 2f + cursorPartLength * lineNr
            endLineLengthAddition = strokeWidth + cursorPartLength * (lineNr + 1f)
        }
    }


    private companion object {
        const val DEFAULT_TOOL_STROKE_WIDTH=3.5f
        const val CURSOR_LINES=4
    }
}
