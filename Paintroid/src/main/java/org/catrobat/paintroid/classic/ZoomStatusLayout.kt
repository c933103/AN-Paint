/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.text.Layout
import android.view.View
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import kotlin.math.ceil

/** Natural-size Fit text, with a fixed scrolling status viewport for long captions.
 * Footer height depends on caption/configuration, never on a changing status message.
 * The ordinary compact status/cursor path remains owned by the Activity.
 */
internal class ZoomStatusLayout(context: Context): LinearLayout(context) {
    var isStatusScrollable=false; private set
    var onCompactStatus: (() -> Unit)?=null
    private var refreshCompactAfterLayout=false
    private fun dp(value: Int)=(value*resources.displayMetrics.density+.5f).toInt()

    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        if(childCount==2) {
            val status=findViewWithTag<TextView>("status_text")
            val zoom=getChildAt(1) as LinearLayout
            val fit=zoom.findViewWithTag<TextView>("zoom_fit_view")
            val slider=zoom.findViewWithTag<View>("zoom_slider")
            val available=(MeasureSpec.getSize(widthMeasureSpec)-paddingLeft-paddingRight).coerceAtLeast(0)
            val caption=fit.transformationMethod?.getTransformation(fit.text,fit) ?: fit.text
            val desiredFit=maxOf(dp(44),ceil(Layout.getDesiredWidth(caption,fit.paint)).toInt()+
                fit.compoundPaddingLeft+fit.compoundPaddingRight)
            // Never give a longer Fit caption width previously owned by status.
            // Compact: 40dp icons, 108dp slider, and at least 64dp status.
            val stacked=desiredFit>dp(44) || desiredFit+dp(188+64)>available
            if(stacked!=isStatusScrollable) {
                isStatusScrollable=stacked
                if(stacked) {
                    removeView(status)
                    val viewport=ScrollView(context).apply {
                        tag="status_viewport";isFillViewport=true
                        addView(status,ScrollView.LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.WRAP_CONTENT))
                    }
                    status.maxLines=Int.MAX_VALUE
                    addView(viewport,0,LayoutParams(LayoutParams.MATCH_PARENT,dp(44)))
                } else {
                    val viewport=getChildAt(0) as ScrollView
                    viewport.removeView(status);removeView(viewport)
                    addView(status,0,LayoutParams(0,dp(44),1f))
                    // Refresh after layout, when status.width is its new compact width.
                    refreshCompactAfterLayout=true
                }
            }
            orientation=if(stacked) VERTICAL else HORIZONTAL
            (zoom.layoutParams as LayoutParams).apply {
                width=if(stacked) LayoutParams.MATCH_PARENT else LayoutParams.WRAP_CONTENT
                height=LayoutParams.WRAP_CONTENT
            }
            (slider.layoutParams as LayoutParams).apply {
                width=if(stacked) 0 else dp(108)
                weight=if(stacked) 1f else 0f
            }
            // Reserve 64dp slider and both 40dp icons. Wrap, never shrink sp.
            val maximum=if(stacked) (available-dp(144)).coerceAtLeast(dp(44)) else Int.MAX_VALUE
            if(fit.maxWidth!=maximum) fit.maxWidth=maximum
        }
        super.onMeasure(widthMeasureSpec,heightMeasureSpec)
    }

    override fun onLayout(changed: Boolean,left: Int,top: Int,right: Int,bottom: Int) {
        super.onLayout(changed,left,top,right,bottom)
        if(refreshCompactAfterLayout && !isStatusScrollable) {
            refreshCompactAfterLayout=false
            onCompactStatus?.invoke()
        }
    }
}
