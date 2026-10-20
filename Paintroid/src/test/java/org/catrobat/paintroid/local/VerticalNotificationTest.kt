/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.Context
import android.content.res.Configuration
import android.graphics.Insets
import android.os.Looper
import android.view.MotionEvent
import android.view.View
import android.view.WindowInsets
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.Toast
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowToast
import java.time.Duration
import java.util.Locale

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class VerticalNotificationTest {
    class NotificationActivity: Activity() {
        override fun attachBaseContext(base: Context) {
            super.attachBaseContext(base.createConfigurationContext(Configuration(base.resources.configuration).apply {setLocale(Locale.forLanguageTag("mn-Mong"))}))
        }
    }
    private lateinit var controller: ActivityController<NotificationActivity>
    private lateinit var previous: Locale
    private lateinit var saved: Configuration
    private lateinit var drawing: FrameLayout
    private val activity get()=controller.get()
    private val host get()=activity.findViewById<FrameLayout>(android.R.id.content)
    private fun notice()=host.findViewWithTag<View>("locale_notification")
    private fun card()=requireNotNull(host.findViewWithTag<VerticalFeedbackCard>("locale_notification_card"))
    private fun advance(ms: Long=32)=shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(ms))
    private fun show(text: String) {LocaleTypography.showMessage(activity,text,Toast.LENGTH_SHORT);advance()}
    @Before fun attach() {
        previous=Locale.getDefault()
        controller=Robolectric.buildActivity(NotificationActivity::class.java).setup()
        saved=Configuration(activity.resources.configuration)
        drawing=FrameLayout(activity);activity.setContentView(drawing)
        controller.visible().windowFocusChanged(true);advance();ShadowToast.reset()
        Locale.setDefault(Locale.ENGLISH)
    }
    @Suppress("DEPRECATION") @After fun cleanup() {
        controller.close();advance(0)
        activity.resources.updateConfiguration(saved,activity.resources.displayMetrics)
        Locale.setDefault(previous);ShadowToast.reset()
    }
    @Test @Config(fontScale=1f) fun normalPortrait()=profiles(1f)
    @Test @Config(fontScale=2f) fun largePortrait()=profiles(2f)
    @Test @Config(fontScale=1f,qualifiers="w640dp-h320dp-land-mdpi") fun normalLandscape()=profiles(1f)
    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-mdpi") fun largeLandscape()=profiles(2f)
    @Suppress("DEPRECATION") private fun profiles(scale: Float) {
        for(tag in listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) {
            activity.resources.updateConfiguration(Configuration(activity.resources.configuration).apply {setLocale(Locale.forLanguageTag(tag))},activity.resources.displayMetrics)
            assertEquals(scale,activity.resources.configuration.fontScale,0f)
            assertNotEquals(Locale.getDefault(),VerticalText.uiLocale(activity))
            val text=("ᠮᠣᠩᠭᠣᠯ\u202fᠤ 👩🏽‍💻 中文 123456789012345678901234567890 ").repeat(30)
            show(text)
            val notice=requireNotNull(notice());val card=card();val body=card.viewport
            assertTrue(card.hasOverflow)
            assertNull(ShadowToast.getLatestToast())
            assertEquals(text,body.message.text.toString())
            assertEquals(text,body.message.createAccessibilityNodeInfo().text.toString())
            assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,body.message.accessibilityLiveRegion)
            assertEquals(activity.getString(org.catrobat.paintroid.R.string.ui_done),card.done.text.toString())
            assertTrue(card.top>=notice.paddingTop)
            assertTrue(card.bottom<=notice.height-notice.paddingBottom)
            val footerY=card.dismissControl.top
            body.columns.scrollTo(0,0)
            VerticalFeedbackViewTest.swipe(body,body.width*.8f,body.height*.5f,body.width*.2f,body.height*.5f)
            assertTrue("Horizontal swipe $tag",body.columns.scrollX>0)
            assertEquals(footerY,card.dismissControl.top)
            advance(10000);assertSame(notice,notice())
            assertTrue(card.dismissControl.performClick());assertNull(notice())
            show("1")
            assertFalse(card().hasOverflow)
            assertEquals(View.GONE,card().done.visibility)
            advance(2100);assertNull(notice())
        }
    }
    @Test fun inputOutsideOverflowAndAllFittingInputRemainWithDrawingWithoutStealingFocus() {
        val actions=mutableListOf<Int>()
        drawing.setOnTouchListener {_,event ->actions.add(event.actionMasked);true}
        val field=EditText(activity)
        drawing.addView(field,FrameLayout.LayoutParams(100,50).apply {leftMargin=100;topMargin=60})
        advance() // Establish a measured, attached input before requesting focus.
        assertTrue(field.requestFocus());advance()
        // Robolectric 4.14.1 shadows Activity.currentFocus with an unrelated
        // manually assigned field. Query the actual framework hierarchy instead.
        assertTrue(field.isFocused)
        assertSame(field,activity.window.decorView.findFocus())
        show("中文 ".repeat(150))
        assertSame(field,activity.window.decorView.findFocus())
        val card=card()
        dispatch(MotionEvent.ACTION_DOWN,5f,5f)
        dispatch(MotionEvent.ACTION_MOVE,card.left+10f,card.top+10f)
        dispatch(MotionEvent.ACTION_UP,card.left+10f,card.top+10f)
        assertEquals(listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_MOVE,MotionEvent.ACTION_UP),actions)
        actions.clear()
        dispatch(MotionEvent.ACTION_DOWN,card.left+10f,card.top+10f)
        dispatch(MotionEvent.ACTION_UP,5f,5f);assertTrue(actions.isEmpty())
        show("1")
        val fit=card()
        dispatch(MotionEvent.ACTION_DOWN,fit.left+10f,fit.top+10f)
        dispatch(MotionEvent.ACTION_UP,fit.left+10f,fit.top+10f)
        assertEquals(listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP),actions)
        assertSame(field,activity.window.decorView.findFocus())
    }
    @Test fun imeResizeKeepsFixedDismissVisibleAndHiddenWindowDropsPersistentMessage() {
        show("1234567890".repeat(80))
        val notice=requireNotNull(notice());val card=card()
        val insets=WindowInsets.Builder().setInsets(WindowInsets.Type.ime(),Insets.of(0,0,0,260)).build()
        notice.dispatchApplyWindowInsets(insets);advance()
        val position=IntArray(2);notice.getLocationInWindow(position)
        assertTrue(position[1]+card.bottom<=activity.window.decorView.height-260)
        assertTrue(card.dismissControl.bottom<=card.height-card.paddingBottom)
        assertTrue(card.viewport.message.height>card.viewport.height)
        VerticalFeedbackViewTest.swipe(card.viewport,20f,card.viewport.height*.8f,20f,card.viewport.height*.2f)
        assertTrue(card.viewport.scrollY>0)
        advance(10000);assertSame(notice,notice())
        activity.window.decorView.dispatchWindowVisibilityChanged(View.GONE)
        advance(0);assertNull(notice());assertNull(notice.parent)
    }
    @Test @Config(fontScale=2f) fun impossibleImeHeightRetainsNotificationUntilVisibleSpaceReturns() {
        val value="ᠮᠣᠩᠭᠣᠯ\u202fᠤ ".repeat(100)
        show(value)
        val notice=requireNotNull(notice());val card=card()
        notice.dispatchApplyWindowInsets(WindowInsets.Builder().setInsets(WindowInsets.Type.ime(),Insets.of(0,0,0,activity.window.decorView.height-60)).build())
        advance();assertTrue(card.deferred);assertEquals(View.INVISIBLE,card.visibility)
        advance(20000);assertSame(notice,notice())
        notice.dispatchApplyWindowInsets(WindowInsets.Builder().build());advance()
        assertFalse(card.deferred);assertEquals(View.VISIBLE,card.visibility)
        assertEquals(value,card.viewport.message.text.toString())
        assertTrue(card.dismissControl.performClick());assertNull(notice())
    }
    private fun dispatch(action: Int,x: Float,y: Float) {
        val event=MotionEvent.obtain(0,0,action,x,y,0)
        try {assertTrue(host.dispatchTouchEvent(event))} finally {event.recycle()}
    }
}
