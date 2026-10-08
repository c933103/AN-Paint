/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.Dialog
import android.content.ContextWrapper
import android.content.res.Configuration
import android.graphics.Insets
import android.graphics.Rect
import android.os.Looper
import android.view.MotionEvent
import android.view.View
import android.widget.FrameLayout
import android.widget.TextView
import android.widget.Toast
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.LocaleTypography
import org.catrobat.paintroid.classic.LocaleNotification
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

/** Binding/lifecycle regressions. Device screenshots still require visual review. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class LocaleNotificationTest {
    private lateinit var controller: ActivityController<Activity>
    private lateinit var previous: Locale
    private val activity get()=controller.get()
    private val host get()=activity.findViewById<FrameLayout>(android.R.id.content)
    private fun notice()=host.findViewWithTag<View>("locale_notification")
    private fun message()=host.findViewWithTag<TextView>("locale_notification_text")
    private fun advance(ms: Long)=shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(ms))
    private fun show(text: String,duration: Int=Toast.LENGTH_SHORT)=LocaleTypography.showMessage(activity,text,duration)

    @Before fun setup() {
        previous=Locale.getDefault()
        Locale.setDefault(Locale.forLanguageTag("vi-Hani"))
        controller=Robolectric.buildActivity(Activity::class.java).setup()
        activity.setContentView(FrameLayout(activity))
        controller.visible().windowFocusChanged(true)
        assertTrue("Lifecycle regressions require a real attached parent",host.isAttachedToWindow)
        ShadowToast.reset()
    }
    @After fun cleanup() {
        controller.close()
        advance(0)
        Locale.setDefault(previous)
        ShadowToast.reset()
    }

    @Test fun currentApiNomMessageUsesBundledFontAndFullResourceThroughWrappedContext() {
        val config=Configuration(activity.resources.configuration).apply {setLocale(Locale.forLanguageTag("vi-Hani"))}
        val text=activity.createConfigurationContext(config).getString(R.string.ui_cursor_pan_move32)
        assertTrue(text.codePoints().anyMatch {it==0x2ABBB})
        LocaleTypography.showMessage(ContextWrapper(ContextWrapper(activity)),text,Toast.LENGTH_LONG)
        assertNotNull(message())
        assertEquals(text,message().text.toString())
        assertSame(LocaleTypography.typeface(activity),message().typeface)
        text.codePoints().filter {it>0xffff}.forEach {point ->
            assertTrue("U+${point.toString(16)}",message().paint.hasGlyph(String(Character.toChars(point))))
        }
        assertNull(ShadowToast.getLatestToast())
    }

    @Test fun aPreviousTimeoutCannotRemoveTheReplacement() {
        show("first")
        val first=notice()
        assertTrue("Replacement must exercise ViewGroup's detach path",first.isAttachedToWindow)
        advance(1000)
        show("𪮻 𡳒",Toast.LENGTH_LONG)
        val second=notice()
        assertNotSame(first,second)
        assertTrue(second.isAttachedToWindow)
        assertFalse(first.isAttachedToWindow)
        assertNull(first.parent)
        advance(1100) // The first message's original deadline has now passed.
        assertSame(second,notice())
        advance(2500)
        assertNull(notice())
    }

    @Test fun hiddenWindowsClearMessagesAndUseSystemToastsInstead() {
        show("visible")
        controller.windowFocusChanged(false)
        assertNotNull("An unfocused but visible in-app window still owns its message",notice())
        val old=notice()
        assertTrue(old.isAttachedToWindow)
        var siblingWasNotified=false
        // AOSP ViewGroup snapshots childCount before traversing its mutable array.
        // Keep a sibling after the notice to detect synchronous child removal.
        val sibling=object: View(activity) {
            override fun onWindowVisibilityChanged(visibility: Int) {
                super.onWindowVisibilityChanged(visibility)
                if(visibility==View.GONE) siblingWasNotified=true
            }
        }
        host.addView(sibling)
        activity.window.decorView.dispatchWindowVisibilityChanged(View.GONE)
        assertTrue(siblingWasNotified)
        // Lifecycle callbacks cancel timers immediately but must not synchronously
        // change the ViewGroup child array that Android is still traversing.
        assertSame(old,notice())
        activity.window.decorView.visibility=View.GONE
        advance(0)
        assertNull(notice())
        controller.pause().stop()
        show("background")
        assertNull(notice())
        assertEquals("background",ShadowToast.getTextOfLatestToast())
    }

    @Test fun attachedTimeoutAndExternalRemovalDoNotReenterViewGroupDetach() {
        show("timeout")
        val timed=notice()
        assertTrue(timed.isAttachedToWindow)
        assertSame(host,timed.parent)
        val childrenWithNotice=host.childCount
        advance(2100)
        assertNull(timed.parent)
        assertFalse(timed.isAttachedToWindow)
        assertEquals(childrenWithNotice-1,host.childCount)
        assertNull(notice())

        show("removed externally",Toast.LENGTH_LONG)
        val removed=notice()
        assertTrue(removed.isAttachedToWindow)
        // Real ViewGroup removal dispatches GONE before parent is cleared.
        // The superseded synchronous visibility->dismiss code recurses here.
        host.removeView(removed)
        assertNull(removed.parent)
        assertFalse(removed.isAttachedToWindow)
        assertEquals(childrenWithNotice-1,host.childCount)
        show("survivor",Toast.LENGTH_LONG)
        val survivor=notice()
        advance(2100)
        assertSame(survivor,notice())
        advance(1500)
        assertNull(notice())
    }

    @Test fun replacementBeforeDeferredVisibilityRemovalKeepsExactlyOneNotice() {
        show("first")
        val first=notice()
        assertTrue(first.isAttachedToWindow)
        first.dispatchWindowVisibilityChanged(View.GONE)
        assertSame(first,notice())
        show("second",Toast.LENGTH_LONG)
        val second=notice()
        assertNotSame(first,second)
        assertNull(first.parent)
        advance(0)
        assertSame(second,notice())
        assertEquals(1,(0 until host.childCount).count {host.getChildAt(it).tag=="locale_notification"})
    }

    @Test fun detachedAndApplicationContextsUseOnlyNormalTextToasts() {
        val detached=TextView(activity)
        LocaleTypography.showMessage(activity,"detached",Toast.LENGTH_SHORT,detached)
        assertNull(notice())
        assertEquals("detached",ShadowToast.getTextOfLatestToast())
        LocaleTypography.showMessage(activity.applicationContext,"application",Toast.LENGTH_SHORT)
        assertNull(notice())
        assertEquals("application",ShadowToast.getTextOfLatestToast())
    }

    @Test fun recreationDetachesOldMessageAndItsTimeoutDoesNotAffectNewWindow() {
        show("old")
        val old=notice()
        advance(1000)
        controller.recreate()
        activity.setContentView(FrameLayout(activity))
        controller.visible().windowFocusChanged(true)
        assertFalse(old.isAttachedToWindow)
        show("new",Toast.LENGTH_LONG)
        val current=notice()
        advance(1100)
        assertSame(current,notice())
        assertEquals("new",message().text.toString())
    }

    @Test fun overlayDoesNotConsumeDrawingInputOrKeyboardFocus() {
        var touches=0
        host.addView(View(activity).apply {setOnTouchListener {_,_->touches++;true}},FrameLayout.LayoutParams(-1,-1))
        show("𪮻 𡳒")
        host.measure(View.MeasureSpec.makeMeasureSpec(600,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(800,View.MeasureSpec.EXACTLY))
        host.layout(0,0,600,800)
        assertFalse(notice().isFocusable)
        assertFalse(message().isFocusable)
        val event=MotionEvent.obtain(0,0,MotionEvent.ACTION_DOWN,300f,750f,0)
        try {assertTrue(host.dispatchTouchEvent(event))} finally {event.recycle()}
        assertEquals(1,touches)
    }

    @Test fun dialogDismissAndReshowCannotRetainAnUntimedNotice() {
        val dialog=Dialog(activity)
        val anchor=TextView(activity)
        dialog.setContentView(anchor)
        dialog.show()
        controller.windowFocusChanged(false)
        dialog.window!!.decorView.dispatchWindowFocusChanged(true)
        try {
            val dialogHost=dialog.window!!.decorView.findViewById<FrameLayout>(android.R.id.content)
            assertTrue(dialogHost.isAttachedToWindow)
            LocaleTypography.showMessage(activity,"𪮻 𡳒",Toast.LENGTH_SHORT,anchor)
            val text=dialogHost.findViewWithTag<TextView>("locale_notification_text")
            val old=dialogHost.findViewWithTag<View>("locale_notification")
            assertTrue(old.isAttachedToWindow)
            assertSame(LocaleTypography.typeface(activity),text.typeface)
            assertNull(notice())
            dialog.dismiss()
            advance(0)
            assertFalse(old.isAttachedToWindow)
            assertNull("Deferred detach cleanup must remove retained dialog children",old.parent)
            assertNull(dialogHost.findViewWithTag<View>("locale_notification"))

            // Android reuses the same Window/content tree on a second show.
            dialog.show()
            dialog.window!!.decorView.dispatchWindowFocusChanged(true)
            assertTrue(dialogHost.isAttachedToWindow)
            assertNull(dialogHost.findViewWithTag<View>("locale_notification"))
            LocaleTypography.showMessage(activity,"new",Toast.LENGTH_SHORT,anchor)
            assertEquals(1,(0 until dialogHost.childCount).count {dialogHost.getChildAt(it).tag=="locale_notification"})
            advance(2100)
            assertNull(dialogHost.findViewWithTag<View>("locale_notification"))
        } finally {
            dialog.dismiss()
            advance(0)
        }
    }

    @Test fun edgeToEdgeAndAlreadyFittedWindowsRespectBarsCutoutsAndImeWithoutDoubleInsets() {
        val insets=Insets.of(20,30,10,200)
        assertEquals(Rect(20,30,10,200),LocaleNotification.insetPadding(insets,0,0,600,800,600,800))
        assertEquals(Rect(0,0,0,0),LocaleNotification.insetPadding(insets,20,30,570,570,600,800))
        assertEquals(Rect(0,0,0,152),LocaleNotification.insetPadding(Insets.of(0,0,0,200),0,0,600,752,600,800))
        assertEquals(Rect(80,0,0,0),LocaleNotification.insetPadding(Insets.of(80,0,0,0),0,0,800,600,800,600))
    }

    @Test fun ordinaryLocalesKeepTheirSystemToastBehavior() {
        for(tag in listOf("vi","ko-KR","ko-KP","ko-Kore-KR","en")) {
            Locale.setDefault(Locale.forLanguageTag(tag))
            show(tag)
            assertNull(notice())
            assertEquals(tag,ShadowToast.getTextOfLatestToast())
        }
    }
}
