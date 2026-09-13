/* AN Paint additions, 2026. GNU AGPL-3.0-or-later.
 * KDE Breeze glyphs: LGPL-3.0-or-later; see artwork/breeze. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Typeface
import android.view.View
import org.catrobat.paintroid.R

/** A category remembers its last tool; opening it also makes that tool active. */
enum class ToolCategory(val labelId: Int,val tools: List<PaintTool>) {
    BRUSH(R.string.ui_drawing23,listOf(PaintTool.PENCIL,PaintTool.BRUSH,PaintTool.WATERCOLOR,PaintTool.SPRAY)),
    SELECTION(R.string.ui_category_selection,listOf(PaintTool.SELECT,PaintTool.LASSO)),
    INSERT(R.string.ui_category_insert,listOf(PaintTool.LINE,PaintTool.CURVE,PaintTool.RECTANGLE,PaintTool.ROUND_RECT,
        PaintTool.ELLIPSE,PaintTool.POLYGON,PaintTool.HEART,PaintTool.STAR,PaintTool.ARROW,PaintTool.TEXT));
    companion object { fun forTool(tool: PaintTool)=values().firstOrNull {tool in it.tools} }
}

class ToolCategoryButton(context: Context,val category: ToolCategory,var selectedTool: PaintTool,private val down: Boolean): PanelToolButton(context) {
    var expanded=false
    init {refresh()}
    fun refresh() {
        text=ui(category.labelId);disclosure=expanded
        labelledIcon(toolIcon(selectedTool))
        contentDescription=ui(if(expanded) R.string.ui_collapse_tool_category else R.string.ui_expand_tool_category,ui(category.labelId),selectedTool.label)
        if(android.os.Build.VERSION.SDK_INT>=26) tooltipText=contentDescription
        invalidate()
    }
}
