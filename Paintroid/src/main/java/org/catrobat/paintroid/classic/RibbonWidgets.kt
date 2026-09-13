/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.content.res.ColorStateList
import android.graphics.*
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.StateListDrawable
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.ScrollView

/** Accessible native button with a vertical text drawing path for vertical locales. */
open class FlowButton(context: Context): Button(context) {
    private var icon: android.graphics.drawable.Drawable?=null
    init {
        isAllCaps=false;textSize=12f;gravity=Gravity.CENTER
        minWidth=0;minimumWidth=0;minHeight=0;minimumHeight=0
        setPadding(dp(4),dp(2),dp(4),dp(2));maxLines=3
        VerticalText.uiTypeface(context)?.let {typeface=it}
        fun fill(selected: Boolean)=GradientDrawable().apply {
            setColor(if(selected) EditorColours.primaryContainer else EditorColours.surfaceContainer)
            cornerRadius=dp(4).toFloat();setStroke(dp(1),if(selected) EditorColours.primary else EditorColours.outlineVariant)
        }
        background=StateListDrawable().apply {
            addState(intArrayOf(android.R.attr.state_selected),fill(true));addState(intArrayOf(android.R.attr.state_pressed),fill(true));addState(intArrayOf(),fill(false))
        }
        setTextColor(ColorStateList(arrayOf(intArrayOf(-android.R.attr.state_enabled),intArrayOf()),intArrayOf(EditorColours.disabledOnSurface,EditorColours.onSurface)))
    }
    protected fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
    fun labelledIcon(resource: Int,size: Int=28) {
        icon=context.getDrawable(resource)?.mutate()?.apply {setBounds(0,0,dp(size),dp(size));setColorFilter(EditorColours.onSurface,PorterDuff.Mode.SRC_IN)}
        setCompoundDrawables(null,icon,null,null);compoundDrawablePadding=dp(2)
    }
    override fun onDraw(canvas: Canvas) {
        if(!VerticalText.uiVertical()) {super.onDraw(canvas);return}
        var top=paddingTop.toFloat()
        icon?.let {drawable->canvas.save();canvas.translate((width-drawable.bounds.width())/2f,top);drawable.draw(canvas);canvas.restore();top+=drawable.bounds.height()+dp(2)}
        val p=Paint(paint).apply {color=currentTextColor}
        VerticalText.drawLabel(canvas,text.toString(),p,RectF(paddingLeft.toFloat(),top,width-paddingRight.toFloat(),height-paddingBottom.toFloat()))
    }
}

internal class LimitedScrollView(context: Context,private val maximum: Int): ScrollView(context) {
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val limit=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) maximum else minOf(maximum,MeasureSpec.getSize(heightMeasureSpec))
        super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(limit,MeasureSpec.AT_MOST))
    }
}
