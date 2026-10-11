/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.content.res.Configuration
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.*

/** Keep each region scrollable when large text exceeds a small dialog window.
 * The heading/actions have bounded viewports, never bounded text or line counts.
 * The central region retains at least the remaining 40% at the maximum sizes.
 */
internal class ResponsiveDialogLayout(context: Context): LinearLayout(context) {
    init {orientation=VERTICAL;setBackgroundColor(EditorColours.surface)}
    fun region(view: View,fraction: Float,tagName: String) {
        addView(RegionScrollView(context,fraction).apply {tag=tagName;addView(view)},LayoutParams(-1,-2))
    }
    fun body(view: View) {addView(view,LayoutParams(-1,-2,1f))}
    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig)
        requestLayout()
    }
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val maximum=(resources.configuration.screenHeightDp*resources.displayMetrics.density*.88f).toInt()
        val available=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) maximum else minOf(maximum,MeasureSpec.getSize(heightMeasureSpec))
        for(i in 0 until childCount) (getChildAt(i) as? RegionScrollView)?.windowLimit=available
        super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(available,MeasureSpec.AT_MOST))
    }
    private class RegionScrollView(context: Context,private val fraction: Float): ScrollView(context) {
        var windowLimit=Int.MAX_VALUE
        override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
            val maximum=(minOf(windowLimit.toFloat(),resources.configuration.screenHeightDp*resources.displayMetrics.density*.88f)*fraction).toInt()
            val available=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) maximum else minOf(maximum,MeasureSpec.getSize(heightMeasureSpec))
            super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(available,MeasureSpec.AT_MOST))
        }
    }
}

/** Use a row only when every caption fits naturally; otherwise use full-width rows.
 * Native Button instances/listeners are retained, including validation overrides.
 */
internal class ResponsiveDialogActions(context: Context): LinearLayout(context) {
    init {gravity=Gravity.END;isBaselineAligned=false}
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val available=(MeasureSpec.getSize(widthMeasureSpec)-paddingLeft-paddingRight).coerceAtLeast(0)
        var desired=0
        for(i in 0 until childCount) {
            val child=getChildAt(i)
            if(child.visibility==View.GONE) continue
            child.measure(MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED),MeasureSpec.makeMeasureSpec(0,MeasureSpec.UNSPECIFIED))
            desired+=child.measuredWidth
        }
        orientation=if(MeasureSpec.getMode(widthMeasureSpec)!=MeasureSpec.UNSPECIFIED && desired>available) VERTICAL else HORIZONTAL
        for(i in 0 until childCount) {
            val child=getChildAt(i);val width=if(orientation==VERTICAL) -1 else -2
            val params=child.layoutParams as LayoutParams
            if(params.width!=width || params.height!=-2) {params.width=width;params.height=-2;child.layoutParams=params}
        }
        super.onMeasure(widthMeasureSpec,heightMeasureSpec)
    }
    fun action(button: Button) {
        VerticalUi.detach(button)
        button.setSingleLine(false);button.maxLines=Int.MAX_VALUE;button.ellipsize=null
        addView(button,LayoutParams(-2,-2))
    }
}

/** An About-only custom title inside the otherwise unchanged native AlertDialog.
 * Cap the viewport, not the caption; native lists/buttons retain their own layout. */
internal class ResponsiveDialogTitle(context: Context,title: CharSequence): ScrollView(context) {
    init {
        tag="dialog_title_scroll"
        fun dp(n: Int)=(n*resources.displayMetrics.density+.5f).toInt()
        addView(TextView(context).apply {
            tag="dialog_title";text=title;textSize=20f;setTextColor(EditorColours.onSurface)
            setPadding(dp(24),dp(16),dp(24),dp(12))
        })
    }
    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig);requestLayout()
    }
    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        val maximum=(resources.configuration.screenHeightDp*resources.displayMetrics.density*.22f).toInt()
        val available=if(MeasureSpec.getMode(heightMeasureSpec)==MeasureSpec.UNSPECIFIED) maximum else minOf(maximum,MeasureSpec.getSize(heightMeasureSpec))
        super.onMeasure(widthMeasureSpec,MeasureSpec.makeMeasureSpec(available,MeasureSpec.AT_MOST))
    }
}

/** Notice-only column rails retain the reader's distance from the reading start.
 * Capture before native layout can clamp scrollX to a changed viewport range. */
internal class ResponsiveDialogColumns(context: Context): HorizontalScrollView(context) {
    private var previousRange: Int?=null
    override fun onLayout(changed: Boolean,left: Int,top: Int,right: Int,bottom: Int) {
        val rightToLeft=VerticalText.uiDirection()==TextDirection.VERTICAL_RL
        val offset=previousRange?.let {if(rightToLeft) (it-scrollX).coerceAtLeast(0) else scrollX} ?: 0
        super.onLayout(changed,left,top,right,bottom)
        if(childCount==0 || width<=0) return
        val range=(getChildAt(0).width-width+paddingLeft+paddingRight).coerceAtLeast(0)
        // Native input-focus navigation takes priority over a touch reader's offset.
        val focused=findFocus()
        if((focused==null || focused===this) && (previousRange==null || previousRange!=range)) {
            scrollTo((if(rightToLeft) range-offset else offset).coerceIn(0,range),0)
        }
        previousRange=range
    }
}
