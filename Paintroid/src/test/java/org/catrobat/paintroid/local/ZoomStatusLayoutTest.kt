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

/** Isolated native layout transition fixture, not an editor user journey. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w640dp-h640dp-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ZoomStatusLayoutTest {
    @Test fun sameViewReturnsToCompactWithResolvedStatusWidthAndThenStacksAgain() {
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
            var refreshes=0;var compactWidth=0
            footer.onCompactStatus={
                refreshes++;compactWidth=status.width
                assertFalse(footer.isStatusScrollable);assertSame(footer,status.parent)
                assertTrue(status.layoutParams is LinearLayout.LayoutParams)
                status.maxLines=2;status.layoutParams=status.layoutParams.apply {height=44}
            }
            fun settle() {shadowOf(Looper.getMainLooper()).idle();controller.visible();shadowOf(Looper.getMainLooper()).idle()}
            settle()
            assertTrue(footer.isStatusScrollable);assertTrue(status.parent is ScrollView)
            assertEquals(44,(status.parent as View).height);assertEquals(Int.MAX_VALUE,status.maxLines)
            assertEquals(-1,status.layoutParams.width);assertEquals(-2,status.layoutParams.height)
            val originalText=status.text
            footer.layoutParams=footer.layoutParams.apply {width=400};settle()
            assertFalse(footer.isStatusScrollable);assertSame(footer,status.parent)
            assertEquals(1,refreshes);assertEquals(status.width,compactWidth)
            assertTrue("Callback sees narrow compact width, not former 240px viewport",compactWidth in 1 until 240)
            assertEquals(2,status.maxLines);assertEquals(originalText,status.text)
            settle();assertEquals("Callback is transition-only",1,refreshes)
            footer.layoutParams=footer.layoutParams.apply {width=240};settle()
            assertTrue(footer.isStatusScrollable);assertTrue(status.parent is ScrollView)
            assertEquals(44,(status.parent as View).height);assertEquals(Int.MAX_VALUE,status.maxLines)
            assertEquals(1,refreshes);assertEquals(originalText,status.text)
        } finally {controller.pause().stop().destroy()}
    }
}
