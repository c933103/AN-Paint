/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Rect
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.ScrollView

/** Full native labels wrap at their natural font size, including at large system text. */
internal class GalleryActions(context: Context): ViewGroup(context) {
    private data class Cell(val view: View,val x: Int,val y: Int)
    private val cells=mutableListOf<Cell>()
    init {
        if(VerticalText.uiVertical()) layoutDirection=if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL)
            View.LAYOUT_DIRECTION_RTL else View.LAYOUT_DIRECTION_LTR
    }

    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        cells.clear()
        val bounded=MeasureSpec.getMode(widthMeasureSpec)!=MeasureSpec.UNSPECIFIED
        val available=if(bounded) (MeasureSpec.getSize(widthMeasureSpec)-paddingLeft-paddingRight).coerceAtLeast(0) else Int.MAX_VALUE
        var x=0;var y=0;var rowHeight=0;var contentWidth=0
        for(index in 0 until childCount) {
            val child=getChildAt(index)
            if(child.visibility==View.GONE) continue
            child.measure(MeasureSpec.makeMeasureSpec(if(bounded) available else 0,
                if(bounded) MeasureSpec.AT_MOST else MeasureSpec.UNSPECIFIED),
                MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED))
            if(x>0 && child.measuredWidth>available-x) {x=0;y+=rowHeight;rowHeight=0}
            cells.add(Cell(child,x,y))
            x+=child.measuredWidth;rowHeight=maxOf(rowHeight,child.measuredHeight);contentWidth=maxOf(contentWidth,x)
        }
        setMeasuredDimension(resolveSize(contentWidth+paddingLeft+paddingRight,widthMeasureSpec),
            resolveSize(y+rowHeight+paddingTop+paddingBottom,heightMeasureSpec))
    }

    override fun onLayout(changed: Boolean,left: Int,top: Int,right: Int,bottom: Int) {
        val rtl=layoutDirection==View.LAYOUT_DIRECTION_RTL
        for(cell in cells) {
            val x=if(rtl) width-paddingRight-cell.x-cell.view.measuredWidth else paddingLeft+cell.x
            val y=paddingTop+cell.y
            cell.view.layout(x,y,x+cell.view.measuredWidth,y+cell.view.measuredHeight)
        }
    }

    override fun generateDefaultLayoutParams()=LayoutParams(LayoutParams.WRAP_CONTENT,LayoutParams.WRAP_CONTENT)
}

/** Keep a real WebView viewport even when controls exceed a shallow/large-text window. */
internal class GalleryControlsScroll(context: Context): ScrollView(context) {
    private var reveal: View?=null
    init {isSmoothScrollingEnabled=false}

    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val available=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED)
            (resources.configuration.screenHeightDp*resources.displayMetrics.density).toInt()
            else MeasureSpec.getSize(heightMeasureSpec)
        val reserve=minOf((120*resources.displayMetrics.density+.5f).toInt(),available/3)
        super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec((available-reserve).coerceAtLeast(0),MeasureSpec.AT_MOST))
    }

    fun revealStart(view: View) {reveal=view;requestLayout()}

    override fun onLayout(changed: Boolean,left: Int,top: Int,right: Int,bottom: Int) {
        super.onLayout(changed,left,top,right,bottom)
        reveal?.let {view ->
            reveal=null
            if(view.isShown) {
                val box=Rect(0,0,view.width,view.height)
                offsetDescendantRectToMyCoords(view,box)
                // Keep the whole message visible when it fits. An oversized
                // message starts at its beginning, with its full body scrollable.
                if(box.top<scrollY || box.bottom>scrollY+height) scrollTo(0,box.top)
            }
        }
    }
}

internal fun galleryButton(context: Context,label: String,tagName: String,textSizeSp: Float?=null,verticalCaption: Boolean=true,run: ()->Unit)=Button(context).apply {
    text=label;tag=tagName;isAllCaps=false
    setSingleLine(false);maxLines=Int.MAX_VALUE;ellipsize=null
    val minimum=(48*resources.displayMetrics.density+.5f).toInt()
    minWidth=minimum;minimumWidth=minimum;minHeight=minimum;minimumHeight=minimum
    if(textSizeSp!=null) textSize=textSizeSp
    if(verticalCaption) VerticalUi.caption(this,96)
    setOnClickListener {run()}
}

/** A native editable field can grow to fit its hint and wrapped user input. */
internal fun gallerySearchField(context: Context,label: String)=EditText(context).apply {
    id=View.generateViewId();tag="gallery_search";hint=label;textSize=14f
    inputType=android.text.InputType.TYPE_CLASS_TEXT
    setSingleLine(false);setHorizontallyScrolling(false);maxLines=Int.MAX_VALUE
    imeOptions=android.view.inputmethod.EditorInfo.IME_ACTION_SEARCH
    val minimum=(48*resources.displayMetrics.density+.5f).toInt()
    minHeight=minimum;minimumHeight=minimum
}
