/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.Dialog
import android.content.Context
import android.content.res.Configuration
import android.graphics.Insets
import android.graphics.Rect
import android.os.Build
import android.os.Looper
import android.view.InputDevice
import android.view.MotionEvent
import android.view.View
import android.view.WindowInsets
import android.view.accessibility.AccessibilityNodeInfo
import android.widget.EditText
import android.widget.FrameLayout
import androidx.core.view.AccessibilityDelegateCompat
import androidx.core.view.ViewCompat
import androidx.core.view.accessibility.AccessibilityNodeInfoCompat
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
import java.time.Duration
import java.util.Locale

/** Real child hierarchy, input dispatch and framework accessibility. Simulated IME
 * insets exercise the layout contract, not an installed keyboard/TalkBack session.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[26,30,35],qualifiers="w420dp-h680dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class VerticalTooltipOverlayTest {
    class TooltipActivity: Activity() {
        override fun attachBaseContext(base: Context) {
            super.attachBaseContext(base.createConfigurationContext(Configuration(base.resources.configuration).apply {setLocale(Locale.forLanguageTag("mn-Mong"))}))
        }
    }
    private lateinit var controller: ActivityController<TooltipActivity>
    private lateinit var anchor: View
    private lateinit var layout: FrameLayout
    private lateinit var saved: Configuration
    private lateinit var previous: Locale
    private val activity get()=controller.get()
    private val host get()=activity.findViewById<FrameLayout>(android.R.id.content)
    private val longText=("ᠮᠣᠩᠭᠣᠯ\u202fᠤ 12345678901234567890 中文 ").repeat(35)
    private fun overlay()=host.findViewWithTag<VerticalTooltipOverlay>(VerticalTooltipOverlay.TAG)
    private fun advance(ms: Long=32)=shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(ms))
    @Before fun attach() {
        previous=Locale.getDefault();Locale.setDefault(Locale.ENGLISH)
        controller=Robolectric.buildActivity(TooltipActivity::class.java).setup()
        saved=Configuration(activity.resources.configuration)
        layout=FrameLayout(activity)
        anchor=View(activity).apply {isClickable=true;contentDescription="original label"}
        layout.addView(anchor,FrameLayout.LayoutParams(80,60).apply {leftMargin=100;topMargin=100})
        activity.setContentView(layout);controller.visible().windowFocusChanged(true);advance()
        assertTrue(anchor.isAttachedToWindow)
        assertEquals("mn-Mong",activity.resources.configuration.locales[0].toLanguageTag())
        Locale.setDefault(Locale.ENGLISH)
        assertEquals(Locale.ENGLISH,Locale.getDefault())
    }
    @Suppress("DEPRECATION")
    @After fun cleanup() {
        controller.close();advance(0)
        activity.resources.updateConfiguration(saved,activity.resources.displayMetrics)
        Locale.setDefault(previous)
    }
    private fun show(text: String=longText): VerticalTooltipOverlay {
        LocaleTooltip.set(anchor,text)
        assertTrue(anchor.performLongClick());advance()
        return requireNotNull(overlay())
    }
    @Test fun shortTooltipUsesResourceContextNativeHoverDelayExitAndTimeout() {
        LocaleTooltip.set(anchor,"ᠮᠣᠩᠭᠣᠯ")
        assertNull(anchor.tooltipText)
        hover(MotionEvent.ACTION_HOVER_ENTER)
        advance(100);assertNull(overlay())
        advance(1000)
        val first=requireNotNull(overlay())
        assertFalse(first.persistent)
        assertSame(host,first.parent)
        assertEquals("ᠮᠣᠩᠭᠣᠯ",first.card.viewport.message.text.toString())
        hover(MotionEvent.ACTION_HOVER_EXIT);assertNull(overlay())
        hover(MotionEvent.ACTION_HOVER_ENTER);advance(1000);assertNotNull(overlay())
        advance(3600);assertNull(overlay())
        hover(MotionEvent.ACTION_HOVER_EXIT);hover(MotionEvent.ACTION_HOVER_ENTER)
        layout.removeView(anchor);advance(1000);assertNull(overlay())
    }
    @Test fun unchangedCaptionRefreshPreservesPendingHoverAndPersistentCardButRealChangesReplaceIt() {
        LocaleTooltip.set(anchor,longText)
        hover(MotionEvent.ACTION_HOVER_ENTER)
        repeat(3) {advance(100);LocaleTooltip.set(anchor,String(longText.toCharArray()))}
        advance(1000)
        val shown=requireNotNull(overlay())
        assertTrue(shown.persistent)
        LocaleTooltip.set(anchor,longText)
        advance(10000);assertSame(shown,overlay())
        LocaleTooltip.set(anchor,longText+" changed");advance(0)
        assertNull(overlay());assertFalse(shown.isAttachedToWindow)
        assertTrue(anchor.performLongClick());advance()
        assertEquals(longText+" changed",requireNotNull(overlay()).card.viewport.message.text.toString())
    }
    @Test fun overflowKeepsFullAccessibleTextUntilDismissReplacementOrWindowLoss() {
        val first=show()
        assertTrue(first.persistent)
        assertNull(LocaleTooltipWindowTest.popup(anchor))
        assertEquals("original label",anchor.createAccessibilityNodeInfo().contentDescription.toString())
        assertEquals(longText,first.card.viewport.message.createAccessibilityNodeInfo().text.toString())
        if(Build.VERSION.SDK_INT>=28) {
            val info=anchor.createAccessibilityNodeInfo()
            assertEquals(longText,info.tooltipText.toString())
            assertTrue(info.actionList.contains(AccessibilityNodeInfo.AccessibilityAction.ACTION_HIDE_TOOLTIP))
        }
        hover(MotionEvent.ACTION_HOVER_EXIT);advance(20000);assertSame(first,overlay())
        val second=show("中文 ".repeat(100))
        assertFalse(first.isAttachedToWindow);assertNotSame(first,second)
        advance(20000);assertSame(second,overlay())
        assertTrue(second.card.dismissControl.performClick());assertNull(overlay())
        val third=show()
        controller.windowFocusChanged(false);advance(0)
        assertNull(overlay());assertFalse(third.isAttachedToWindow)
        controller.windowFocusChanged(true)
        show();layout.removeView(anchor);advance(0);assertNull(overlay())
    }
    @Test fun restoringHorizontalAndClearingRestoreDelegateAndExplicitHelpWithoutStaleTriggers() {
        val existing=object: AccessibilityDelegateCompat() {
            override fun onInitializeAccessibilityNodeInfo(host: View,info: AccessibilityNodeInfoCompat) {
                super.onInitializeAccessibilityNodeInfo(host,info);info.contentDescription="delegated label"
            }
        }
        ViewCompat.setAccessibilityDelegate(anchor,existing)
        var helped=0
        LocaleTooltip.setHelpAction(anchor) {helped++;true}
        LocaleTooltip.set(anchor,longText)
        assertTrue(anchor.performLongClick());assertEquals(1,helped);assertNull(overlay())
        assertEquals("delegated label",anchor.createAccessibilityNodeInfo().contentDescription.toString())
        if(Build.VERSION.SDK_INT>=28) {
            assertTrue(anchor.performAccessibilityAction(AccessibilityNodeInfo.AccessibilityAction.ACTION_SHOW_TOOLTIP.id,null));advance()
            assertNotNull(overlay())
        }
        select("vi-Hani");LocaleTooltip.set(anchor,"𡨸喃");advance(0)
        assertNull(overlay());assertEquals("𡨸喃",anchor.tooltipText.toString())
        assertTrue(anchor.performLongClick());assertEquals(2,helped);assertNull(overlay())
        assertEquals("delegated label",anchor.createAccessibilityNodeInfo().contentDescription.toString())
        select("mn-Mong");LocaleTooltip.set(anchor,longText)
        LocaleTooltip.set(anchor,null)
        assertTrue(anchor.performLongClick());assertEquals(3,helped)
        hover(MotionEvent.ACTION_HOVER_ENTER);advance(1000);assertNull(overlay())
        assertNull(anchor.tooltipText)
        assertEquals("delegated label",anchor.createAccessibilityNodeInfo().contentDescription.toString())
        val ordinary=View(activity)
        LocaleTooltip.set(ordinary,longText);LocaleTooltip.set(ordinary,"")
        assertFalse(ordinary.isLongClickable)
    }
    @Test fun touchesOutsideKeepDrawingGestureAndFittingTooltipNeverConsumesInput() {
        val actions=mutableListOf<Int>()
        layout.setOnTouchListener {_,event ->actions.add(event.actionMasked);true}
        val over=show()
        dispatch(host,MotionEvent.ACTION_DOWN,5f,5f)
        dispatch(host,MotionEvent.ACTION_MOVE,over.card.left+10f,over.card.top+10f)
        dispatch(host,MotionEvent.ACTION_UP,over.card.left+10f,over.card.top+10f)
        assertEquals(listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_MOVE,MotionEvent.ACTION_UP),actions)
        actions.clear()
        dispatch(host,MotionEvent.ACTION_DOWN,over.card.left+10f,over.card.top+10f)
        dispatch(host,MotionEvent.ACTION_UP,5f,5f)
        assertTrue(actions.isEmpty())
        val fit=show("1")
        assertFalse(fit.persistent)
        dispatch(host,MotionEvent.ACTION_DOWN,fit.card.left+10f,fit.card.top+10f)
        dispatch(host,MotionEvent.ACTION_UP,fit.card.left+10f,fit.card.top+10f)
        assertEquals(listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP),actions)
    }
    @Test @Config(sdk=[30,35]) fun imeAndCutoutInsetsBoundCardWithoutStealingEditorFocusAndAnchorChangesReposition() {
        val field=EditText(activity)
        layout.addView(field,FrameLayout.LayoutParams(100,60).apply {topMargin=30})
        field.requestFocus();advance()
        val over=show()
        assertSame(field,activity.currentFocus)
        val insets=WindowInsets.Builder().setInsets(WindowInsets.Type.systemBars(),Insets.of(0,24,0,0))
            .setInsets(WindowInsets.Type.displayCutout(),Insets.of(30,0,0,0))
            .setInsets(WindowInsets.Type.ime(),Insets.of(0,0,0,260)).build()
        over.dispatchApplyWindowInsets(insets);advance()
        val safe=over.safeBounds()
        assertTrue(safe.contains(Rect(over.card.left,over.card.top,over.card.right,over.card.bottom)))
        val location=IntArray(2);over.getLocationInWindow(location)
        assertTrue(location[1]+over.card.bottom<=activity.window.decorView.height-260)
        assertSame(field,activity.currentFocus)
        val before=over.card.top
        (anchor.layoutParams as FrameLayout.LayoutParams).topMargin=350
        anchor.requestLayout();advance();advance()
        assertTrue(over.card.top!=before || over.card.bottom==safe.bottom-16)
        assertTrue(over.safeBounds().contains(Rect(over.card.left,over.card.top,over.card.right,over.card.bottom)))
    }
    @Test @Config(sdk=[30,35],fontScale=2f) fun impossibleImeHeightDefersSameTooltipAndRevealsItWhenSpaceReturns() {
        val shown=show()
        val insets=WindowInsets.Builder().setInsets(WindowInsets.Type.ime(),Insets.of(0,0,0,activity.window.decorView.height-60)).build()
        shown.dispatchApplyWindowInsets(insets);advance()
        assertTrue(shown.card.deferred);assertEquals(View.INVISIBLE,shown.card.visibility)
        advance(20000);assertSame(shown,overlay())
        shown.dispatchApplyWindowInsets(WindowInsets.Builder().build());advance()
        assertFalse(shown.card.deferred);assertEquals(View.VISIBLE,shown.card.visibility)
        assertSame(shown,overlay())
        assertEquals(longText,shown.card.viewport.message.text.toString())
        assertTrue(shown.card.dismissControl.bottom<=shown.card.height-shown.card.paddingBottom)
        assertTrue(shown.card.dismissControl.performClick());assertNull(overlay())
    }
    @Test fun visibilityDispatchDoesNotMutateSiblingArrayAndOldDeferredCleanupCannotRemoveReplacement() {
        val old=show()
        var siblingNotified=false
        layout.addView(object: View(activity) {
            override fun onWindowVisibilityChanged(visibility: Int) {
                super.onWindowVisibilityChanged(visibility)
                if(visibility==GONE) LocaleTooltip.set(anchor,longText+" updated during visibility dispatch")
            }
        })
        host.addView(object: View(activity) {
            override fun onWindowVisibilityChanged(visibility: Int) {
                super.onWindowVisibilityChanged(visibility)
                if(visibility==GONE) siblingNotified=true
            }
        })
        activity.window.decorView.dispatchWindowVisibilityChanged(View.GONE)
        assertTrue(siblingNotified)
        assertSame(host,old.parent)
        advance(0);assertNull(old.parent)
        activity.window.decorView.dispatchWindowVisibilityChanged(View.VISIBLE)
        val first=show()
        first.dismissAfterDispatch()
        val replacement=show("中文 ".repeat(120))
        advance(0);assertSame(replacement,overlay());assertNull(first.parent)
    }
    @Test fun dialogOwnerAndRecreationCannotLeakAnOldTooltip() {
        val dialog=Dialog(activity)
        val button=View(activity)
        dialog.setContentView(button,FrameLayout.LayoutParams(100,100))
        try {
            dialog.show();dialog.window!!.setLayout(320,500);advance()
            LocaleTooltip.set(button,longText);assertTrue(button.performLongClick());advance()
            val content=dialog.window!!.decorView.findViewById<FrameLayout>(android.R.id.content)
            val old=requireNotNull(content.findViewWithTag<VerticalTooltipOverlay>(VerticalTooltipOverlay.TAG))
            assertNull(overlay());assertSame(content,old.parent)
            dialog.dismiss();advance(0);assertNull(old.parent)
            dialog.show();advance();assertNull(content.findViewWithTag<VerticalTooltipOverlay>(VerticalTooltipOverlay.TAG))
        } finally {dialog.dismiss();advance(0)}
        val old=show();controller.recreate();advance()
        assertFalse(old.isAttachedToWindow);assertNull(old.parent)
    }
    @Suppress("DEPRECATION") private fun select(tag: String) {
        activity.resources.updateConfiguration(Configuration(activity.resources.configuration).apply {setLocale(Locale.forLanguageTag(tag))},activity.resources.displayMetrics)
    }
    private fun hover(action: Int) {
        val root=activity.window.decorView
        val origin=IntArray(2);root.getLocationInWindow(origin)
        val position=IntArray(2);anchor.getLocationInWindow(position)
        val pointer=MotionEvent.PointerProperties().apply {id=0;toolType=MotionEvent.TOOL_TYPE_STYLUS}
        val point=MotionEvent.PointerCoords().apply {
            x=(position[0]-origin[0]+30).toFloat();y=(position[1]-origin[1]+30).toFloat()
        }
        val event=MotionEvent.obtain(0,0,action,1,arrayOf(pointer),arrayOf(point),0,0,1f,1f,0,0,InputDevice.SOURCE_STYLUS,0)
        try {root.dispatchGenericMotionEvent(event)} finally {event.recycle()}
    }
    private fun dispatch(view: View,action: Int,x: Float,y: Float) {
        val event=MotionEvent.obtain(0,0,action,x,y,0)
        try {assertTrue(view.dispatchTouchEvent(event))} finally {event.recycle()}
    }
}
