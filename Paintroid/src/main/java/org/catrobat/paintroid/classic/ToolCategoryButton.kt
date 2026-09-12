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
    BRUSH(R.string.ui_category_brush,listOf(PaintTool.PENCIL,PaintTool.BRUSH,PaintTool.WATERCOLOR,PaintTool.SPRAY)),
    SELECTION(R.string.ui_category_selection,listOf(PaintTool.SELECT,PaintTool.LASSO)),
    INSERT(R.string.ui_category_insert,listOf(PaintTool.LINE,PaintTool.CURVE,PaintTool.RECTANGLE,PaintTool.ROUND_RECT,
        PaintTool.ELLIPSE,PaintTool.POLYGON,PaintTool.HEART,PaintTool.STAR,PaintTool.ARROW,PaintTool.TEXT));
    companion object { fun forTool(tool: PaintTool)=values().firstOrNull {tool in it.tools} }
}

class ToolCategoryButton(context: Context,val category: ToolCategory,var selectedTool: PaintTool,private val down: Boolean): View(context) {
    var expanded=false
    private var glyphTool=selectedTool
    private var glyph=CopyleftIcon(context,toolIcon(selectedTool))
    private val openGlyph=CopyleftIcon(context,if(down) R.drawable.breeze_down else R.drawable.breeze_right)
    private val closeGlyph=CopyleftIcon(context,if(down) R.drawable.breeze_up else R.drawable.breeze_left)
    init {isClickable=true;isFocusable=true;refresh()}
    fun refresh() {
        if(glyphTool!=selectedTool) {glyphTool=selectedTool;glyph=CopyleftIcon(context,toolIcon(selectedTool))}
        contentDescription=context.getString(if(expanded) R.string.ui_collapse_tool_category else R.string.ui_expand_tool_category,
            context.getString(category.labelId),selectedTool.label)
        if(android.os.Build.VERSION.SDK_INT>=26) tooltipText=contentDescription
        invalidate()
    }
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val d=resources.displayMetrics.density
        val p=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=if(isSelected) EditorColours.primaryContainer else EditorColours.surfaceContainer}
        canvas.drawRect(d,d,width-d,height-d,p)
        p.style=Paint.Style.STROKE;p.strokeWidth=d;p.color=if(expanded) EditorColours.primary else EditorColours.outlineVariant
        canvas.drawRect(d,d,width-d,height-d,p)
        val foreground=if(isSelected) EditorColours.onPrimaryContainer else EditorColours.onSurface
        val size=minOf(32*d,width-18*d)
        glyph.draw(canvas,3*d,5*d,3*d+size,5*d+size,foreground)
        (if(expanded) closeGlyph else openGlyph).draw(canvas,width-16*d,14*d,width-2*d,28*d,foreground)
        p.style=Paint.Style.FILL;p.color=foreground;p.typeface=Typeface.DEFAULT_BOLD;p.textSize=10*d
        val label=context.getString(category.labelId)
        p.textSize*=minOf(1f,(width-6*d)/p.measureText(label))
        canvas.drawText(label,(width-p.measureText(label))/2,height-5*d,p)
    }
    override fun drawableStateChanged() {super.drawableStateChanged();invalidate()}
    override fun performClick(): Boolean {super.performClick();return true}
}
