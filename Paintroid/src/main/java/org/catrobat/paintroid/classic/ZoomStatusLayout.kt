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
    var isStatusScrollable=false; private set
    private fun dp(value: Int)=(value*resources.displayMetrics.density+.5f).toInt()

    override fun onMeasure(widthMeasureSpec: Int,heightMeasureSpec: Int) {
        orientation=HORIZONTAL
        if(childCount==2) {
            if(!isStatusScrollable) {
                val status=getChildAt(0) as TextView
                removeView(status)
                val viewport=ScrollView(context).apply {
                    tag="status_viewport";isFillViewport=true
                    overScrollMode=View.OVER_SCROLL_IF_CONTENT_SCROLLS
                    addView(status,FrameLayout.LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.WRAP_CONTENT))
                }
                status.maxLines=Int.MAX_VALUE
                addView(viewport,0,LayoutParams(0,dp(44),1f))
                isStatusScrollable=true
            }
            val zoom=getChildAt(1) as LinearLayout
            val slider=zoom.findViewWithTag<View>("zoom_slider")
            val available=(MeasureSpec.getSize(widthMeasureSpec)-paddingLeft-paddingRight).coerceAtLeast(0)
            // 124dp for the three buttons; reserve status space on small screens.
            // The slider never stretches to fill the footer in either orientation.
            (slider.layoutParams as LayoutParams).apply {
                width=(available-dp(124+64)).coerceIn(dp(64),dp(108));weight=0f
            }
            (zoom.layoutParams as LayoutParams).apply {
                width=LayoutParams.WRAP_CONTENT;height=dp(44);weight=0f
            }
        }
        super.onMeasure(widthMeasureSpec,heightMeasureSpec)
    }
}
