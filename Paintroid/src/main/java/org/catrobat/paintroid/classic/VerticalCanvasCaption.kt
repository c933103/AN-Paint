/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.PointF
import android.graphics.RectF

/** A UI caption measured in viewport pixels, never inverse-zoom document units. */
internal class VerticalCanvasCaption(text: String,source: Paint,availableHeight: Float,
                                     private val direction: TextDirection) {
    private val paint=Paint(source).apply {textAlign=Paint.Align.LEFT}
    private val label: String
    val width: Float
    val height: Float

    init {
        require(direction!=TextDirection.HORIZONTAL)
        // Joining-script words may exceed this wrapping target. Measure the
        // returned label; do not split their shaping clusters to force a fit.
        label=VerticalText.wrapLabel(text,paint,availableHeight.coerceAtLeast(paint.fontSpacing),direction)
        val bounds=VerticalText.bounds(label,paint,direction,GlyphOrientation.MIXED,1f)
        width=bounds.width();height=bounds.height()
    }

    fun draw(canvas: Canvas,left: Float,top: Float) {
        canvas.save()
        canvas.translate(left,top)
        VerticalText.draw(canvas,label,paint,direction,GlyphOrientation.MIXED)
        canvas.restore()
    }

    /** Prefer the first reading column next to the grip, then the opposite side.
     * If neither side fits, contain a fitting box without moving the actual grip.
     * Oversized captions keep their text and the caller's existing viewport clip.
     */
    fun beside(grip: PointF,viewport: RectF,gap: Float): PointF {
        val right=grip.x+gap
        val left=grip.x-gap-width
        val preferred=if(direction==TextDirection.VERTICAL_LR) right else left
        val alternate=if(direction==TextDirection.VERTICAL_LR) left else right
        fun fits(x: Float)=x>=viewport.left && x+width<=viewport.right
        val x=when {
            fits(preferred) -> preferred
            fits(alternate) -> alternate
            width<=viewport.width() -> preferred.coerceIn(viewport.left,viewport.right-width)
            else -> viewport.centerX()-width/2
        }
        val y=if(height<=viewport.height()) (grip.y-height/2).coerceIn(viewport.top,viewport.bottom-height)
            else viewport.centerY()-height/2
        return PointF(x,y)
    }
}
