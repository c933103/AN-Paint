/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.res.Configuration
import android.graphics.Rect
import android.os.SystemClock
import android.view.MotionEvent
import android.view.View
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** Framework measurement and gesture tests, not an installed-device or pixel claim. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class VerticalFeedbackViewTest {
    private val tags=listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")
    private fun context(tag: String): Context {
        val app=RuntimeEnvironment.getApplication() as Context
        return app.createConfigurationContext(Configuration(app.resources.configuration).apply {setLocale(Locale.forLanguageTag(tag))})
    }
    private fun layout(view: View,width: Int,height: Int) {
        view.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(height,View.MeasureSpec.AT_MOST))
        view.layout(0,0,view.measuredWidth,view.measuredHeight)
    }
    @Test @Config(fontScale=1f) fun normalPortrait()=checkProfiles(280,380,1f)
    @Test @Config(fontScale=2f) fun largePortrait()=checkProfiles(280,380,2f)
    @Test @Config(fontScale=1f,qualifiers="w640dp-h320dp-land-mdpi") fun normalLandscape()=checkProfiles(580,250,1f)
    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-mdpi") fun largeLandscape()=checkProfiles(580,250,2f)
    private fun checkProfiles(width: Int,height: Int,scale: Float) {
        for(tag in tags) {
            val context=context(tag)
            assertEquals(scale,context.resources.configuration.fontScale,0f)
            val value=("ᠮᠣᠩᠭᠣᠯ\u202fᠤ Unicode 👩🏽‍💻 中文 1234567890 ").repeat(30)
            val card=VerticalFeedbackCard(context,value,"test") {}
            layout(card,width,height)
            val view=card.viewport
            assertEquals(value,view.message.text.toString())
            assertEquals(value,view.message.createAccessibilityNodeInfo().text.toString())
            assertNull(view.message.ellipsize)
            assertTrue("Bounded $tag/$scale",card.height<=height)
            assertTrue(card.hasOverflow)
            assertTrue(view.message.width>view.columns.width)
            val end=(view.message.width-view.columns.width).coerceAtLeast(0)
            val rightToLeft=VerticalText.uiDirection(context)==TextDirection.VERTICAL_RL
            assertEquals("Reading start $tag",if(rightToLeft) end else 0,view.columns.scrollX)
            val button=card.dismissControl
            assertEquals(View.VISIBLE,button.visibility)
            assertEquals(context.getString(org.catrobat.paintroid.R.string.ui_done),card.done.text.toString())
            val node=button.createAccessibilityNodeInfo()
            assertEquals(card.done.text.toString(),(if(button===card.done) node.text else node.contentDescription).toString())
            val fixed=Rect(button.left,button.top,button.right,button.bottom)
            view.columns.scrollTo(end,0);assertEquals(end,view.columns.scrollX)
            view.columns.scrollTo(0,0)
            swipe(view,view.width*.8f,view.height*.5f,view.width*.2f,view.height*.5f)
            assertTrue("Real horizontal gesture $tag",view.columns.scrollX>0)
            assertEquals(fixed,Rect(button.left,button.top,button.right,button.bottom))
            assertTrue(button.bottom<=card.height-card.paddingBottom)
            assertTrue(button.top>=view.bottom)
            // A narrower, shorter viewport must keep every character and both rails.
            layout(card,width/2,height-40)
            assertEquals(value,view.message.text.toString())
            assertTrue(card.height<=height-40)
            assertTrue(card.hasOverflow)
        }
    }
    @Test @Config(fontScale=2f) fun joinedWordsAndNumericRunsRemainVerticallyReachableByGesture() {
        for(tag in tags) for(text in listOf("ᠮᠣᠩᠭᠣᠯ\u202fᠤ".repeat(35),"1234567890".repeat(35),"A\u00a0B\u2007C".repeat(35))) {
            val view=VerticalFeedbackView(context(tag),text).apply {maximumHeightPx=100}
            layout(view,240,100)
            assertTrue("Indivisible run height $tag",view.message.height>view.height)
            swipe(view,100f,85f,100f,15f)
            assertTrue("Real vertical gesture $tag",view.scrollY>0)
            view.scrollTo(0,view.columns.height)
            assertEquals(view.columns.height-view.height,view.scrollY)
            assertEquals(text,view.message.text.toString())
            val wrapped=VerticalText.wrapLabel(text,view.message.paint,100f,VerticalText.uiDirection(view.context))
            assertEquals("No inserted break inside shaped/numeric run",text,wrapped)
        }
    }
    @Test @Config(fontScale=2f) fun constrainedCardUsesNamed44dpIconThenDefersAndReappearsWithoutLosingMessage() {
        val text="ᠮᠣᠩᠭᠣᠯ\u202fᠤ ".repeat(80)
        var dismissed=0
        val card=VerticalFeedbackCard(context("mn-Mong"),text,"test") {dismissed++}
        layout(card,240,100)
        assertTrue(card.persistent);assertFalse(card.deferred)
        assertSame(card.compactDone,card.dismissControl)
        assertEquals(44,card.compactDone.width);assertEquals(44,card.compactDone.height)
        assertEquals(card.context.getString(org.catrobat.paintroid.R.string.ui_done),card.compactDone.contentDescription)
        assertTrue(card.compactDone.bottom<=card.height)
        assertTrue(card.compactDone.top>=card.viewport.bottom)
        layout(card,240,70)
        assertTrue(card.deferred);assertEquals(View.INVISIBLE,card.visibility)
        assertTrue(card.persistent)
        assertEquals(text,card.viewport.message.text.toString())
        layout(card,240,240)
        assertFalse(card.deferred);assertEquals(View.VISIBLE,card.visibility)
        assertTrue(card.dismissControl.bottom<=card.height-card.paddingBottom)
        assertTrue(card.dismissControl.performClick());assertEquals(1,dismissed)
    }
    @Test @Config(fontScale=2f) fun narrowTallEmojiCaptionUsesACompleteNamedIconInsteadOfClippingColumns() {
        val card=VerticalFeedbackCard(context("qaa-Zsye-XV"),"中文 ".repeat(100),"test") {}
        layout(card,44,260)
        assertFalse(card.deferred);assertTrue(card.persistent)
        assertSame(card.compactDone,card.dismissControl)
        assertEquals(44,card.compactDone.width);assertEquals(44,card.compactDone.height)
        assertTrue(card.compactDone.left>=0);assertTrue(card.compactDone.right<=card.width)
        assertEquals(card.context.getString(org.catrobat.paintroid.R.string.ui_done),card.compactDone.createAccessibilityNodeInfo().contentDescription)
    }
    @Test fun onceOverflowingReflowToFitKeepsExplicitDismissal() {
        val card=VerticalFeedbackCard(context("en-XV"),"One two three four five six seven eight nine ten","test") {}
        layout(card,80,140)
        assertTrue(card.persistent)
        layout(card,2000,500)
        assertFalse(card.hasOverflow)
        assertTrue(card.persistent)
        assertEquals(View.VISIBLE,card.dismissControl.visibility)
    }
    @Test fun aFittingMessageDoesNotReserveAnUnnecessaryDismissAction() {
        for(tag in tags) {
            val card=VerticalFeedbackCard(context(tag),"1","test") {}
            layout(card,280,250)
            assertFalse(card.hasOverflow)
            assertEquals(View.GONE,card.done.visibility)
        }
    }
    companion object {
        internal fun swipe(view: View,x1: Float,y1: Float,x2: Float,y2: Float) {
            val start=SystemClock.uptimeMillis()
            fun send(action: Int,x: Float,y: Float,time: Long) {
                val event=MotionEvent.obtain(start,time,action,x,y,0)
                try {assertTrue(view.dispatchTouchEvent(event))} finally {event.recycle()}
            }
            send(MotionEvent.ACTION_DOWN,x1,y1,start)
            for(i in 1..8) send(MotionEvent.ACTION_MOVE,x1+(x2-x1)*i/8,y1+(y2-y1)*i/8,start+i*20)
            send(MotionEvent.ACTION_UP,x2,y2,start+200)
        }
    }
}
