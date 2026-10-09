/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.os.Looper
import android.view.InputDevice
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.accessibility.AccessibilityNodeInfo.AccessibilityAction
import android.widget.FrameLayout
import android.widget.TextView
import org.catrobat.paintroid.classic.LocaleTooltip
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
import org.robolectric.util.ReflectionHelpers
import org.robolectric.util.ReflectionHelpers.ClassParameter
import java.time.Duration
import java.util.Locale

/** Real framework TooltipPopup; no replacement popup, timer or listener shadow. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w420dp-h680dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class LocaleTooltipWindowTest {
    private lateinit var controller: ActivityController<Activity>
    private lateinit var previous: Locale
    private lateinit var host: FrameLayout
    private lateinit var anchor: View
    private val activity get()=controller.get()
    private fun advance(ms: Long)=shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(ms))

    @Before fun attach() {
        previous=Locale.getDefault();Locale.setDefault(Locale.forLanguageTag("vi-Hani"))
        controller=Robolectric.buildActivity(Activity::class.java).setup()
        host=FrameLayout(activity)
        anchor=View(activity).apply {isClickable=true;contentDescription="original accessible label"}
        host.addView(anchor,FrameLayout.LayoutParams(80,60).apply {leftMargin=100;topMargin=100})
        activity.setContentView(host);controller.visible().windowFocusChanged(true);advance(32)
        assertTrue(anchor.isAttachedToWindow);assertTrue(anchor.width>0)
        LocaleTooltip.set(anchor,"𡨸喃")
    }
    @After fun detach() {controller.close();advance(0);Locale.setDefault(previous)}

    @Test fun hoverRetainsNativeDelayExitTimeoutAndPendingDetachCancellation() {
        hover(MotionEvent.ACTION_HOVER_MOVE)
        advance(100);assertNull(popup(anchor))
        advance(1000);assertPopupText("𡨸喃")
        hover(MotionEvent.ACTION_HOVER_EXIT);assertNull(popup(anchor))
        hover(MotionEvent.ACTION_HOVER_MOVE);advance(1000);assertPopupText("𡨸喃")
        advance(16000);assertNull(popup(anchor))
        hover(MotionEvent.ACTION_HOVER_MOVE)
        host.removeView(anchor);advance(1000)
        assertNull(popup(anchor));assertFalse(anchor.isAttachedToWindow)
    }

    @Test fun nativeLongPressAndAccessibilityActionsKeepLogicalTextAndClearOnDetach() {
        assertTrue(anchor.performLongClick());assertPopupText("𡨸喃")
        val node=anchor.createAccessibilityNodeInfo()
        assertEquals("original accessible label",node.contentDescription.toString())
        assertEquals("𡨸喃",node.tooltipText.toString())
        assertTrue(node.actionList.contains(AccessibilityAction.ACTION_HIDE_TOOLTIP))
        assertTrue(anchor.performAccessibilityAction(AccessibilityAction.ACTION_HIDE_TOOLTIP.id,null))
        assertNull(popup(anchor))
        assertTrue(anchor.createAccessibilityNodeInfo().actionList.contains(AccessibilityAction.ACTION_SHOW_TOOLTIP))
        assertTrue(anchor.performAccessibilityAction(AccessibilityAction.ACTION_SHOW_TOOLTIP.id,null))
        assertPopupText("𡨸喃")
        val content=popupContent(anchor)!!
        host.removeView(anchor);advance(0)
        assertNull(popup(anchor));assertFalse(content.isAttachedToWindow)
    }

    @Test fun consumedLongPressDoesNotShowADuplicateAndNullOrEmptyClearsNativePopup() {
        var helped=0
        anchor.setOnLongClickListener {helped++;true}
        assertTrue(anchor.performLongClick());assertEquals(1,helped);assertNull(popup(anchor))
        hover(MotionEvent.ACTION_HOVER_MOVE);advance(1000);assertPopupText("𡨸喃")
        LocaleTooltip.set(anchor,null);assertNull(popup(anchor));assertNull(anchor.tooltipText)
        assertEquals("original accessible label",anchor.contentDescription)
        LocaleTooltip.set(anchor,"𡨸喃")
        hover(MotionEvent.ACTION_HOVER_MOVE);advance(1000);assertPopupText("𡨸喃")
        LocaleTooltip.set(anchor,"");assertNull(popup(anchor));assertNull(anchor.tooltipText)
        assertTrue(anchor.performLongClick());assertEquals(2,helped);assertNull(popup(anchor))
    }

    private fun assertPopupText(expected: String) {
        advance(32) // WindowManager attaches the popup on the next traversal.
        val popup=requireNotNull(popup(anchor))
        assertEquals("com.android.internal.view.TooltipPopup",popup.javaClass.name)
        val label=ReflectionHelpers.getField<TextView>(popup,"mMessageView")
        assertEquals(expected,label.text.toString())
        assertTrue(label.text is android.text.Spanned)
        val spans=(label.text as android.text.Spanned).getSpans(0,label.length(),android.text.style.MetricAffectingSpan::class.java)
        assertEquals(1,spans.size)
        val p=android.text.TextPaint(label.paint);spans.single().updateMeasureState(p)
        assertSame(org.catrobat.paintroid.classic.LocaleTypography.typeface(activity),p.typeface)
        assertTrue(popupContent(anchor)!!.isAttachedToWindow)
    }

    private fun hover(action: Int) {
        val root=activity.window.decorView
        val position=IntArray(2);anchor.getLocationInWindow(position)
        val origin=IntArray(2);root.getLocationInWindow(origin)
        val pointer=MotionEvent.PointerProperties().apply {id=0;toolType=MotionEvent.TOOL_TYPE_STYLUS}
        val point=MotionEvent.PointerCoords().apply {
            x=(position[0]-origin[0]+30).toFloat();y=(position[1]-origin[1]+30).toFloat()
        }
        // Stylus hover uses real pointer coordinates. Robolectric 4.14.1 does not model
        // the separate mouse cursor position used by API35 ViewGroup hit testing.
        val event=MotionEvent.obtain(0,0,action,1,arrayOf(pointer),arrayOf(point),0,0,1f,1f,0,0,InputDevice.SOURCE_STYLUS,0)
        // ViewRootImpl routes pointer hover to this framework ViewGroup dispatcher.
        // Reflection reaches the hidden entry point; it does not directly show a popup.
        try {ReflectionHelpers.callInstanceMethod<Boolean>(root,"dispatchTooltipHoverEvent",ClassParameter.from(MotionEvent::class.java,event))}
        finally {event.recycle()}
    }

    companion object {
        internal fun popup(view: View): Any? {
            val info=ReflectionHelpers.getField<Any?>(view,"mTooltipInfo") ?: return null
            return ReflectionHelpers.getField<Any?>(info,"mTooltipPopup")
        }
        internal fun popupContent(view: View): View?=popup(view)?.let {ReflectionHelpers.getField<View>(it,"mContentView")}
    }
}
