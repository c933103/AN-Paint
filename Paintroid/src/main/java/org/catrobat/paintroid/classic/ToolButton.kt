/* Pocket Paint Local additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.view.View
import org.catrobat.paintroid.R

/** KDE Breeze artwork under LGPL-3.0-or-later; see artwork/breeze and Icon licences. */
class ToolButton(context: Context, val tool: PaintTool) : PanelToolButton(context) {
    init {text=tool.label;contentDescription=tool.label;labelledIcon(toolIcon(tool));if(android.os.Build.VERSION.SDK_INT>=26) tooltipText=tool.label}
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
