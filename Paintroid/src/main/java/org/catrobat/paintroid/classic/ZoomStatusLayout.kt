/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.view.View
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

/** Status and corner zoom controls always share one row. Long status messages
 * scroll inside their own fixed viewport, without resizing the canvas.
 */
internal class ZoomStatusLayout(context: Context): LinearLayout(context) {
    val isStatusScrollable get()=childCount==2
    private fun dp(value: Int)=(value*resources.displayMetrics.density+.5f).toInt()
    init {orientation=HORIZONTAL;isBaselineAligned=false}

    /** Build the stable hierarchy before the first measure or status update. */
    fun bind(status: TextView,zoom: LinearLayout) {
        check(childCount==0)
        status.maxLines=Int.MAX_VALUE
        val viewport=ScrollView(context).apply {
            tag="status_viewport";isFillViewport=true
            addView(status,FrameLayout.LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.WRAP_CONTENT))
        }
        addView(viewport,LayoutParams(0,dp(44),1f))
        addView(zoom,LayoutParams(LayoutParams.WRAP_CONTENT,dp(44)))
    }

    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        if(childCount==2) {
            val zoom=getChildAt(1) as LinearLayout
            val slider=zoom.findViewWithTag<View>("zoom_slider")
            val available=(MeasureSpec.getSize(widthMeasureSpec)-paddingLeft-paddingRight).coerceAtLeast(0)
            // Reserve status space beside the three buttons. The slider never
            // stretches across the footer in either orientation.
            (slider.layoutParams as LayoutParams).apply {
                width=(available-dp(124+64)).coerceIn(dp(64),dp(108));weight=0f
            }
        }
        super.onMeasure(widthMeasureSpec,heightMeasureSpec)
    }
}
