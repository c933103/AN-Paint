/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.Context
import android.os.SystemClock
import android.view.InputDevice
import android.view.MotionEvent
import android.view.View
import android.widget.FrameLayout
import android.widget.LinearLayout
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ColumnScrollView
import org.catrobat.paintroid.classic.NumericSlider
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

/** Native ViewGroup dispatch through the real scroll container; no progress setters. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="en-w320dp-h640dp-port-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class NumericSliderGestureTest {
    private lateinit var controller: ActivityController<Activity>
    private lateinit var root: RecordingParent
    private lateinit var scroll: ColumnScrollView
    private lateinit var numeric: NumericSlider
    private val slider get()=numeric.slider
    private lateinit var originalLocale: Locale
    private val events=mutableListOf<Int>()
    private val values=mutableListOf<Int>()
    private var clock=0L
    private var downTime=0L

    private class RecordingParent(context: Context): FrameLayout(context) {
        val requests=mutableListOf<Boolean>()
        override fun requestDisallowInterceptTouchEvent(disallow: Boolean) {
            requests.add(disallow)
            super.requestDisallowInterceptTouchEvent(disallow)
        }
    }

    @Before fun setUp() {
        originalLocale=Locale.getDefault();Locale.setDefault(Locale.ENGLISH)
        controller=Robolectric.buildActivity(Activity::class.java)
        val activity=controller.get().apply {setTheme(R.style.ClassicPaintTheme)}
        controller.setup().visible().windowFocusChanged(true)
        root=RecordingParent(activity)
        numeric=NumericSlider(activity,"Quality",95,1,100) {values.add(it)}
        val content=LinearLayout(activity).apply {
            orientation=LinearLayout.HORIZONTAL
            addView(numeric,LinearLayout.LayoutParams(240,120))
            addView(View(activity),LinearLayout.LayoutParams(660,240))
        }
        scroll=ColumnScrollView(activity).apply {addView(content,FrameLayout.LayoutParams(900,240))}
        root.addView(scroll,FrameLayout.LayoutParams(320,240));activity.setContentView(root)
        root.measure(View.MeasureSpec.makeMeasureSpec(320,View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(240,View.MeasureSpec.EXACTLY))
        root.layout(0,0,320,240)
        assertTrue(slider.isAttachedToWindow);assertTrue(slider.width>0)
        slider.setOnTouchListener {_,event -> events.add(event.actionMasked);false}
        clock=SystemClock.uptimeMillis();root.requests.clear()
    }
    @After fun tearDown() {
        slider.setOnTouchListener(null)
        controller.pause().stop().destroy();Locale.setDefault(originalLocale)
    }

    private fun send(action: Int,x: Float,y: Float): Boolean {
        clock+=20;if(action==MotionEvent.ACTION_DOWN) downTime=clock
        val event=MotionEvent.obtain(downTime,clock,action,x,y,0)
        event.source=InputDevice.SOURCE_TOUCHSCREEN
        return try {root.dispatchTouchEvent(event)} finally {event.recycle()}
    }
    private fun sliderY()=numeric.top+slider.top+slider.height/2f
    private fun thumbX()=numeric.left+slider.left+slider.paddingLeft-slider.thumbOffset+slider.thumb.bounds.centerX().toFloat()
    private fun dragTo(value: Int) {
        events.clear();val before=scroll.scrollX
        val from=thumbX();val to=(numeric.left+slider.left+
            if(value==1) slider.paddingLeft-1 else slider.width-slider.paddingRight+1).toFloat()
        assertTrue(send(MotionEvent.ACTION_DOWN,from,sliderY()))
        assertEquals(true,root.requests.last())
        for(step in 1..12) assertTrue(send(MotionEvent.ACTION_MOVE,from+(to-from)*step/12,sliderY()))
        assertTrue(send(MotionEvent.ACTION_UP,to,sliderY()))
        assertEquals(value,slider.progress+numeric.minimum)
        assertEquals(value,values.last())
        assertEquals(before,scroll.scrollX)
        assertEquals(MotionEvent.ACTION_DOWN,events.first())
        assertEquals(MotionEvent.ACTION_UP,events.last())
        assertFalse(events.contains(MotionEvent.ACTION_CANCEL))
        assertEquals(false,root.requests.last())
        assertFalse(slider.isPressed)
    }
    private fun scrollOutsideSlider() {
        val before=scroll.scrollX
        send(MotionEvent.ACTION_DOWN,280f,220f)
        send(MotionEvent.ACTION_MOVE,240f,220f)
        send(MotionEvent.ACTION_MOVE,160f,220f)
        send(MotionEvent.ACTION_UP,160f,220f)
        assertTrue("Ordinary form scrolling remains available",scroll.scrollX>before)
    }

    @Test fun bothEndpointsRetainNativeGestureAndValueCallback() {dragTo(1);dragTo(100);dragTo(1)}
    @Test fun upReleasesParentForOrdinaryFormScrolling() {dragTo(1);scrollOutsideSlider()}
    @Test fun cancelReleasesParentAndDoesNotInventAnEndpoint() {
        val x=thumbX();send(MotionEvent.ACTION_DOWN,x,sliderY())
        send(MotionEvent.ACTION_MOVE,x-30,sliderY());val value=slider.progress
        send(MotionEvent.ACTION_CANCEL,x-30,sliderY())
        assertEquals(value,slider.progress);assertFalse(slider.isPressed)
        assertEquals(false,root.requests.last());scrollOutsideSlider()
    }
    @Test fun secondaryPointerUpDoesNotReleaseTheLiveGesture() {
        val x=thumbX();val y=sliderY();send(MotionEvent.ACTION_DOWN,x,y)
        fun pointers(action: Int) {
            clock+=20
            val properties=Array(2) {index->MotionEvent.PointerProperties().apply {id=index;toolType=MotionEvent.TOOL_TYPE_FINGER}}
            val coordinates=Array(2) {index->MotionEvent.PointerCoords().apply {this.x=x-index*4;this.y=y;pressure=1f;size=1f}}
            val event=MotionEvent.obtain(downTime,clock,action,2,properties,coordinates,0,0,1f,1f,0,0,
                InputDevice.SOURCE_TOUCHSCREEN,0)
            try {assertTrue(root.dispatchTouchEvent(event))} finally {event.recycle()}
        }
        pointers(MotionEvent.ACTION_POINTER_DOWN or (1 shl MotionEvent.ACTION_POINTER_INDEX_SHIFT))
        pointers(MotionEvent.ACTION_POINTER_UP or (1 shl MotionEvent.ACTION_POINTER_INDEX_SHIFT))
        assertEquals(true,root.requests.last())
        send(MotionEvent.ACTION_MOVE,x-40,y)
        send(MotionEvent.ACTION_UP,x-40,y)
        assertFalse(events.contains(MotionEvent.ACTION_CANCEL));assertEquals(false,root.requests.last())
        assertEquals(0,scroll.scrollX);scrollOutsideSlider()
    }
    @Test fun disablingReleasesCurrentClaimAndDisabledDownDoesNotClaim() {
        val x=thumbX();send(MotionEvent.ACTION_DOWN,x,sliderY())
        slider.isEnabled=false;assertEquals(false,root.requests.last())
        send(MotionEvent.ACTION_CANCEL,x,sliderY());root.requests.clear()
        send(MotionEvent.ACTION_DOWN,x,sliderY())
        assertFalse(root.requests.contains(true))
        send(MotionEvent.ACTION_CANCEL,x,sliderY());scrollOutsideSlider()
    }
    @Test fun detachReleasesClaimEvenWithoutAParentDispatchedCancel() {
        // Direct delivery isolates detach cleanup from ViewGroup's CANCEL path.
        val event=MotionEvent.obtain(clock,clock,MotionEvent.ACTION_DOWN,slider.width/2f,slider.height/2f,0)
        try {assertTrue(slider.onTouchEvent(event))} finally {event.recycle()}
        assertEquals(true,root.requests.last())
        numeric.removeView(slider)
        assertEquals(false,root.requests.last());scrollOutsideSlider()
    }
}
