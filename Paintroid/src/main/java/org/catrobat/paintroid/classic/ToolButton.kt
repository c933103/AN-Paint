/* Pocket Paint Local additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.view.View
import org.catrobat.paintroid.R

/** KDE Breeze artwork under LGPL-3.0-or-later; see artwork/breeze and Icon licences. */
class ToolButton(context: Context, val tool: PaintTool) : View(context) {
    private val glyph = CopyleftIcon(context, toolIcon(tool))
    init {
        contentDescription = tool.label
        isClickable = true; isFocusable = true
        if (android.os.Build.VERSION.SDK_INT >= 26) tooltipText = tool.label
    }
    override fun onDraw(c: Canvas) {
        super.onDraw(c)
        val side=minOf(width,height).toFloat()
        c.save();c.translate((width-side)/2,(height-side)/2);c.scale(side/48f,side/48f)
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = if (isSelected) EditorColours.primaryContainer else EditorColours.surfaceContainer }
        c.drawRect(1f, 1f, 47f, 47f, p)
        p.color = if (isSelected) EditorColours.primary else EditorColours.outlineVariant; p.style = Paint.Style.STROKE; p.strokeWidth = 1f
        c.drawRect(1f, 1f, 47f, 47f, p)
        glyph.draw(c, 5f, 5f, 43f, 43f, if (!isEnabled) EditorColours.disabledOnSurface else if (isSelected) EditorColours.onPrimaryContainer else EditorColours.onSurface)
        c.restore()
    }
    override fun drawableStateChanged() { super.drawableStateChanged(); invalidate() }
    override fun performClick(): Boolean { super.performClick(); return true }
}

internal fun toolIcon(tool: PaintTool): Int = when(tool) {
        PaintTool.LASSO -> R.drawable.breeze_lasso
        PaintTool.SELECT -> R.drawable.breeze_select
        PaintTool.ERASER -> R.drawable.breeze_eraser
        PaintTool.FILL -> R.drawable.breeze_fill
        PaintTool.PICKER -> R.drawable.breeze_picker
        PaintTool.ZOOM -> R.drawable.breeze_navigate
        PaintTool.PENCIL -> R.drawable.breeze_pencil
        PaintTool.BRUSH -> R.drawable.breeze_brush
        PaintTool.WATERCOLOR -> R.drawable.breeze_watercolor
        PaintTool.HEART -> R.drawable.breeze_heart
        PaintTool.STAR -> R.drawable.breeze_star
        PaintTool.ARROW -> R.drawable.breeze_arrow
        PaintTool.SPRAY -> R.drawable.breeze_spray
        PaintTool.TEXT -> R.drawable.breeze_text
        PaintTool.LINE -> R.drawable.breeze_line
        PaintTool.CURVE -> R.drawable.breeze_curve
        PaintTool.RECTANGLE -> R.drawable.breeze_rectangle
        PaintTool.POLYGON -> R.drawable.breeze_polygon
        PaintTool.ELLIPSE -> R.drawable.breeze_ellipse
        PaintTool.ROUND_RECT -> R.drawable.breeze_round_rectangle
}
