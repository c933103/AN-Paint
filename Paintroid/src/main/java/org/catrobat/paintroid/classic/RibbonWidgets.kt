/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.StateListDrawable
import android.view.Gravity
import android.view.accessibility.AccessibilityNodeInfo
import android.widget.Button
import android.widget.ScrollView
import android.widget.TextView
import kotlin.math.ceil

/** Native text buttons retain their platform appearance. Vertical captions have their own measurements. */
open class FlowButton(context: Context): Button(context) {
    var columnHeightDp=144
    protected var icon: android.graphics.drawable.Drawable?=null
    protected fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
    init {
        isAllCaps=false;gravity=Gravity.CENTER;textSize=13f
        minWidth=0;minimumWidth=0;minHeight=0;minimumHeight=0
        VerticalText.uiTypeface(context)?.let {typeface=it}
    }
    fun labelledIcon(resource: Int,size: Int=32) {
        icon=context.getDrawable(resource)?.mutate()?.apply {setBounds(0,0,dp(size),dp(size))}
        if(!VerticalText.uiVertical()) setCompoundDrawables(null,icon,null,null)
        compoundDrawablePadding=dp(3);requestLayout();invalidate()
    }
    protected open fun caption()=VerticalText.wrapLabel(text.toString(),paint,dp(columnHeightDp).toFloat())
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        if(!VerticalText.uiVertical()) {super.onMeasure(widthMeasureSpec,heightMeasureSpec);return}
        val box=VerticalText.bounds(caption(),paint,VerticalText.uiDirection(),GlyphOrientation.MIXED,1f)
        val iconWidth=icon?.bounds?.width()?.plus(dp(8)) ?: 0
        val w=ceil(box.width()).toInt()+iconWidth+paddingLeft+paddingRight
        val h=maxOf(ceil(box.height()).toInt(),icon?.bounds?.height() ?: 0)+paddingTop+paddingBottom
        setMeasuredDimension(resolveSize(maxOf(dp(44),w),widthMeasureSpec),resolveSize(maxOf(dp(44),h),heightMeasureSpec))
    }
    override fun onDraw(canvas: Canvas) {
        icon?.setColorFilter(if(isEnabled) currentTextColor else EditorColours.disabledOnSurface,PorterDuff.Mode.SRC_IN)
        if(!VerticalText.uiVertical()) {super.onDraw(canvas);return}
        val p=Paint(paint).apply {color=if(isEnabled) currentTextColor else EditorColours.disabledOnSurface}
        val label=caption();val box=VerticalText.bounds(label,p,VerticalText.uiDirection(),GlyphOrientation.MIXED,1f)
        val iw=icon?.bounds?.width() ?: 0;val gap=if(iw>0) dp(8) else 0
        val left=(width-box.width()-iw-gap)/2f
        val textFirst=VerticalText.uiDirection()==TextDirection.VERTICAL_RL
        icon?.let {canvas.save();canvas.translate(if(textFirst) left+box.width()+gap else left,(height-it.bounds.height())/2f);it.draw(canvas);canvas.restore()}
        canvas.save();canvas.translate(if(textFirst) left else left+iw+gap,(height-box.height())/2f)
        VerticalText.draw(canvas,label,p,VerticalText.uiDirection(),GlyphOrientation.MIXED);canvas.restore()
    }
}

/** Original square tool tiles and small bold captions, confined to ribbon panels. */
open class PanelToolButton(context: Context): FlowButton(context) {
    companion object {
        fun tileSize(context: Context): Int {
            val metrics=context.resources.displayMetrics
            val scale=context.resources.configuration.fontScale.coerceAtLeast(1f)
            return ((if(VerticalText.uiVertical()) 112 else 96)*metrics.density*scale+.5f).toInt()
        }
    }
    var disclosure: Boolean?=null
    var disclosureBeside=false
    init {
        textSize=10f;typeface=VerticalText.uiTypeface(context) ?: Typeface.DEFAULT_BOLD
        // The activity theme supplies textAlignment=viewStart; gravity alone cannot override it.
        textAlignment=TEXT_ALIGNMENT_CENTER;gravity=Gravity.CENTER
        if(!VerticalText.uiVertical()) {maxLines=3;ellipsize=android.text.TextUtils.TruncateAt.END}
        setPadding(dp(6),dp(5),dp(6),dp(5));columnHeightDp=112
        fun tile(selected: Boolean)=GradientDrawable().apply {
            setColor(if(selected) EditorColours.primaryContainer else EditorColours.surfaceContainer)
            setStroke(dp(1),if(selected) EditorColours.primary else EditorColours.outlineVariant)
        }
        background=StateListDrawable().apply {
            addState(intArrayOf(android.R.attr.state_selected),tile(true))
            addState(intArrayOf(android.R.attr.state_pressed),tile(true));addState(intArrayOf(),tile(false))
        }
        setTextColor(EditorColours.onSurface)
    }
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        // One square size for every tool, including vertical scripts and larger fonts.
        // Captions wrap within the tile; their length must never size an individual button.
        val side=minOf(resolveSize(tileSize(context),widthMeasureSpec),resolveSize(tileSize(context),heightMeasureSpec))
        columnHeightDp=((side-paddingTop-paddingBottom)/resources.displayMetrics.density).toInt()
        super.onMeasure(MeasureSpec.makeMeasureSpec(side,MeasureSpec.EXACTLY),MeasureSpec.makeMeasureSpec(side,MeasureSpec.EXACTLY))
    }
    override fun caption(): String {
        val full=super.caption()
        if(width<=0 || height<=0) return full
        val availableWidth=width-paddingLeft-paddingRight-(icon?.bounds?.width()?.plus(dp(8)) ?: 0)
        val availableHeight=height-paddingTop-paddingBottom
        fun fits(label: String): Boolean {
            val box=VerticalText.bounds(label,paint,VerticalText.uiDirection(),GlyphOrientation.MIXED,1f)
            return box.width()<=availableWidth && box.height()<=availableHeight
        }
        if(fits(full)) return full
        // Retain natural glyph size and shaping; unusually long labels use an
        // ellipsis inside the tile, with the full caption available to accessibility/tooltip.
        val clusters=VerticalText.clusters(text.toString()).toMutableList()
        while(clusters.isNotEmpty()) {
            clusters.removeAt(clusters.lastIndex)
            val label=VerticalText.wrapLabel(clusters.joinToString("").trimEnd()+"…",paint,availableHeight.toFloat())
            if(fits(label)) return label
        }
        return "…"
    }
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        disclosure?.let {expanded ->
            val glyph=CopyleftIcon(context,if(disclosureBeside) {
                if(expanded) org.catrobat.paintroid.R.drawable.breeze_left else org.catrobat.paintroid.R.drawable.breeze_right
            } else if(expanded) org.catrobat.paintroid.R.drawable.breeze_up else org.catrobat.paintroid.R.drawable.breeze_down)
            glyph.draw(canvas,width-dp(16).toFloat(),dp(3).toFloat(),width-dp(2).toFloat(),dp(17).toFloat(),EditorColours.onSurface)
        }
    }
}

/** The tool drawer scrolls within the height left by the naturally measured primary rail. */
internal class RibbonPanel(context: Context,private val maximum: Int,private val sideLayout: Boolean=false): android.widget.LinearLayout(context) {
    init {orientation=if(sideLayout) HORIZONTAL else VERTICAL;isBaselineAligned=false}
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        if(!sideLayout && childCount>=2) {
            val primary=getChildAt(0)
            primary.measure(getChildMeasureSpec(widthMeasureSpec,paddingLeft+paddingRight,primary.layoutParams.width),MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED))
            getChildAt(1).layoutParams.height=(maximum-primary.measuredHeight-paddingTop-paddingBottom).coerceAtLeast((44*resources.displayMetrics.density).toInt())
        }
        super.onMeasure(widthMeasureSpec,heightMeasureSpec)
    }
}

/** Tabs share their naturally tallest height so the selected edge meets one common panel boundary. */
internal open class EqualHeightRail(context: Context,private val sideLayout: Boolean=false): android.widget.LinearLayout(context) {
    init {isBaselineAligned=false;orientation=if(sideLayout) VERTICAL else HORIZONTAL}
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        super.onMeasure(widthMeasureSpec,heightMeasureSpec)
        val tallest=(0 until childCount).maxOfOrNull {getChildAt(it).measuredHeight} ?: 0
        for(i in 0 until childCount) getChildAt(i).let {it.measure(MeasureSpec.makeMeasureSpec(it.measuredWidth,MeasureSpec.EXACTLY),MeasureSpec.makeMeasureSpec(tallest,MeasureSpec.EXACTLY))}
        val margins=(0 until childCount).map {val p=getChildAt(it).layoutParams as android.view.ViewGroup.MarginLayoutParams;p.topMargin+p.bottomMargin}
        setMeasuredDimension(measuredWidth,resolveSize(tallest*(if(sideLayout) childCount else 1)+paddingTop+paddingBottom+
            (if(sideLayout) margins.sum() else margins.maxOrNull() ?: 0),heightMeasureSpec))
    }
}

internal class TabStrip(context: Context,sideLayout: Boolean=false): EqualHeightRail(context,sideLayout)

/** An attached tab with a selected edge; never a boxed command button. */
class RibbonTab(context: Context,private val sideLayout: Boolean=false): FlowButton(context) {
    init {background=null;textAlignment=TEXT_ALIGNMENT_CENTER;textSize=13f;minimumHeight=dp(44);minHeight=dp(44);setPadding(dp(if(VerticalText.uiVertical()) 12 else 16),dp(8),dp(if(VerticalText.uiVertical()) 12 else 16),dp(9));columnHeightDp=88;setTextColor(EditorColours.onSurface)}
    override fun onDraw(canvas: Canvas) {
        val p=Paint(Paint.ANTI_ALIAS_FLAG)
        if(isSelected) {p.color=EditorColours.surfaceContainer;canvas.drawRect(0f,0f,width.toFloat(),height.toFloat(),p)}
        p.color=if(isSelected) EditorColours.primary else EditorColours.outlineVariant
        val edge=dp(if(isSelected) 3 else 1).toFloat()
        if(sideLayout) canvas.drawRect(width-edge,0f,width.toFloat(),height.toFloat(),p)
        else canvas.drawRect(0f,height-edge,width.toFloat(),height.toFloat(),p)
        super.onDraw(canvas)
    }
    override fun onInitializeAccessibilityNodeInfo(info: AccessibilityNodeInfo) {
        super.onInitializeAccessibilityNodeInfo(info);info.className="android.app.ActionBar\$Tab";info.isSelected=isSelected
    }
}

/** Vertical prose wraps into columns at its original size, scrolled by its container. */
class FlowTextView(context: Context): TextView(context) {
    var columnHeightDp=240
    init {VerticalText.uiTypeface(context)?.let {typeface=it};setTextColor(EditorColours.onSurface)}
    private fun caption(height: Int)=VerticalText.wrapLabel(text.toString(),paint,height.toFloat().coerceAtLeast(paint.fontSpacing))
    private var columnHeight=0
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        if(!VerticalText.uiVertical()) {super.onMeasure(widthMeasureSpec,heightMeasureSpec);return}
        val preferred=(columnHeightDp*resources.displayMetrics.density).toInt()
        columnHeight=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) preferred else minOf(preferred,MeasureSpec.getSize(heightMeasureSpec)-paddingTop-paddingBottom)
        val box=VerticalText.bounds(caption(columnHeight),paint,VerticalText.uiDirection(),GlyphOrientation.MIXED,1f)
        setMeasuredDimension(resolveSize(ceil(box.width()).toInt()+paddingLeft+paddingRight,widthMeasureSpec),
            resolveSize(ceil(box.height()).toInt()+paddingTop+paddingBottom,heightMeasureSpec))
    }
    override fun onDraw(canvas: Canvas) {
        if(!VerticalText.uiVertical()) {super.onDraw(canvas);return}
        canvas.save();canvas.translate(paddingLeft.toFloat(),paddingTop.toFloat())
        VerticalText.draw(canvas,caption(columnHeight),Paint(paint).apply {color=currentTextColor},VerticalText.uiDirection(),GlyphOrientation.MIXED)
        canvas.restore()
    }
}

/** Start at the first reading column in right-to-left vertical scripts. */
internal class ColumnScrollView(context: Context): android.widget.HorizontalScrollView(context) {
    private var positioned=false
    override fun onLayout(changed: Boolean,left: Int,top: Int,right: Int,bottom: Int) {
        super.onLayout(changed,left,top,right,bottom)
        if(!positioned && childCount>0 && width>0) {
            positioned=true
            if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL) scrollTo((getChildAt(0).width-width+paddingLeft+paddingRight).coerceAtLeast(0),0)
        }
    }
}

internal class LimitedScrollView(context: Context,private val maximum: Int): ScrollView(context) {
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val limit=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) maximum else minOf(maximum,MeasureSpec.getSize(heightMeasureSpec))
        super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(limit,MeasureSpec.AT_MOST))
    }
}
