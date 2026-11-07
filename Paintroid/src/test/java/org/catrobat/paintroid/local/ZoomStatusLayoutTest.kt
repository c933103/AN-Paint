/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.view.View
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.SeekBar
import android.widget.TextView
import org.catrobat.paintroid.classic.ZoomStatusLayout
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import android.os.Looper

/** Native sizing regression: rotation and caption length never create a second zoom row. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w640dp-h640dp-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ZoomStatusLayoutTest {
    @Test fun sameViewKeepsCornerZoomBesideScrollableStatusAtEveryWidth() {
        val controller=Robolectric.buildActivity(Activity::class.java).setup().visible()
        val activity=controller.get()
        try {
            val holder=FrameLayout(activity)
            val footer=ZoomStatusLayout(activity)
            val status=TextView(activity).apply {tag="status_text";text="Cursor status ".repeat(20);maxLines=2;textSize=11f}
            val zoom=LinearLayout(activity)
            zoom.addView(View(activity),LinearLayout.LayoutParams(40,44))
            zoom.addView(SeekBar(activity).apply {tag="zoom_slider"},LinearLayout.LayoutParams(108,44))
            zoom.addView(View(activity),LinearLayout.LayoutParams(40,44))
            zoom.addView(TextView(activity).apply {tag="zoom_fit_view";text="Fit";textSize=13f;minimumWidth=44;minimumHeight=44},LinearLayout.LayoutParams(-2,-2))
            footer.addView(status,LinearLayout.LayoutParams(0,44,1f));footer.addView(zoom)
            holder.addView(footer,FrameLayout.LayoutParams(240,-2));activity.setContentView(holder)
            fun settle() {shadowOf(Looper.getMainLooper()).idle();controller.visible();shadowOf(Looper.getMainLooper()).idle()}
            for(width in listOf(240,400,640,320)) {
                footer.layoutParams=footer.layoutParams.apply {this.width=width};settle()
                val viewport=footer.getChildAt(0) as ScrollView
                assertTrue(footer.isStatusScrollable)
                assertEquals(LinearLayout.HORIZONTAL,footer.orientation)
                assertEquals(44,footer.height)
                assertEquals(44,viewport.height)
                assertTrue("Status retains its own width",viewport.width>=20)
                assertTrue("Zoom stays in a corner",zoom.width<footer.width)
                assertEquals("Same vertical level",viewport.top,zoom.top)
                assertTrue("Slider never fills the footer",zoom.findViewWithTag<View>("zoom_slider").width in 64..108)
                assertSame(viewport,status.parent)
                assertEquals("Cursor status ".repeat(20),status.text.toString())
                assertEquals(Int.MAX_VALUE,status.maxLines)
            }
        } finally {controller.pause().stop().destroy()}
    }
}
