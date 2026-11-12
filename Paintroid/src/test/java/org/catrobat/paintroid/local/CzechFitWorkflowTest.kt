/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Rect
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import android.text.Editable
import android.text.TextWatcher
import android.util.DisplayMetrics
import android.util.TypedValue
import android.view.Display
import android.view.MotionEvent
import android.view.View
import android.widget.ScrollView
import android.widget.SeekBar
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowDisplayManager
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.Locale
import java.util.concurrent.TimeUnit

/** Mounted NATIVE layout/root input. Synthetic image/status fixtures; not an installed-device claim. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CzechFitWorkflowTest {
    @Test @Config(fontScale=1f) fun normalPortraitFitPreservesFullCaptionAndCanvas()=checkFit("portrait-1x",1f,320,640)
    @Test @Config(fontScale=2f) fun enlargedPortraitFitPreservesFullCaptionAndCanvas()=checkFit("portrait-2x",2f,320,640)
    @Test @Config(fontScale=1f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun normalLandscapeFitPreservesFullCaptionAndCanvas()=checkFit("landscape-1x",1f,640,320)
    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun enlargedLandscapeFitPreservesFullCaptionAndCanvas()=checkFit("landscape-2x",2f,640,320)
    @Test @Config(fontScale=1f) fun compactEnglishFooterRetainsStatusBesideZoom()=withEditor("en-US") {activity,_ ->
        assertTrue(activity.window.decorView.findViewWithTag<View>("status_text").parent is ScrollView)
        exerciseZoom(activity)
    }
    @Test @Config(fontScale=1f) fun rtlFooterRetainsReachableZoom()=withEditor("ar") {activity,_ ->
        assertEquals(View.LAYOUT_DIRECTION_RTL,activity.window.decorView.layoutDirection)
        exerciseZoom(activity)
    }
    @Test @Config(fontScale=1f) fun verticalFooterRetainsOriginalIconAndStatusRail()=withEditor("mn-Mong") {activity,_ ->
        val root=activity.window.decorView
        assertTrue(root.findViewWithTag<View>("zoom_fit_view") is ActionButton)
        assertNotNull(root.findViewWithTag<View>("vertical_status_rail"))
        assertNull(root.findViewWithTag<View>("status_viewport"))
        exerciseZoom(activity)
    }

    @Test @Config(fontScale=1f) fun canvasResizeRefreshesStatusAfterTheNativeTraversal()=withEditor("cs") {activity,_ ->
        val canvas=activity.paintCanvas
        val status=activity.window.decorView.findViewWithTag<TextView>("status_text")
        awaitStatusLayout(status)
        val parent=canvas.parent as View
        val padding=Rect(parent.paddingLeft,parent.paddingTop,parent.paddingRight,parent.paddingBottom)
        val originalHeight=canvas.height
        var resized=false;var updates=0;var updatesDuringLayout=0
        val resize=View.OnLayoutChangeListener {_,left,top,right,bottom,oldLeft,oldTop,oldRight,oldBottom ->
            if(right-left!=oldRight-oldLeft || bottom-top!=oldBottom-oldTop) resized=true
        }
        val watcher=object: TextWatcher {
            override fun beforeTextChanged(text: CharSequence?,start: Int,count: Int,after: Int)=Unit
            override fun onTextChanged(text: CharSequence?,start: Int,before: Int,count: Int) {
                updates++;if(status.isInLayout) updatesDuringLayout++
            }
            override fun afterTextChanged(text: Editable?)=Unit
        }
        canvas.addOnLayoutChangeListener(resize);status.addTextChangedListener(watcher)
        try {
            // Change an actual parent constraint. Native measure/layout must
            // resize the canvas and invoke its real onSizeChanged -> fit path.
            parent.setPadding(padding.left,padding.top,padding.right,padding.bottom+16)
            settle();awaitStatusLayout(status)
            assertTrue("Native canvas size callback ran",resized)
            assertEquals(originalHeight-16,canvas.height)
            assertTrue("Canvas sizing refreshed the visible status",updates>0)
            assertEquals("Status text must not change inside native layout",0,updatesDuringLayout)
            val expected=activity.getString(R.string.ui_px,canvas.tool.label,canvas.zoomStatusLabel(),
                activity.document.bitmap.width,activity.document.bitmap.height,
                ReflectionHelpers.getField<UiMessage>(activity,"draftStatus").text())
            assertEquals(expected,status.text.toString())
            assertEquals(expected,requireNotNull(status.layout).text.toString())
        } finally {
            canvas.removeOnLayoutChangeListener(resize);status.removeTextChangedListener(watcher)
            parent.setPadding(padding.left,padding.top,padding.right,padding.bottom);settle()
        }
    }

    private fun settle()=shadowOf(Looper.getMainLooper()).idleFor(50,TimeUnit.MILLISECONDS)
    private fun withEditor(tag: String,check: (ClassicPaintActivity,ActivityController<ClassicPaintActivity>)->Unit) {
        val app=RuntimeEnvironment.getApplication() as Context
        val oldTag=AppLanguage.selectedTag(app);val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        app.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        app.getSharedPreferences("classic-ui",0).edit().clear().commit()
        AppLanguage.select(app,tag)
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity=controller.setup().visible().windowFocusChanged(true).get()
        try {
            awaitEditorStartup(activity);settle()
            // This is an isolated geometry/input fixture, not a draft-persistence test.
            // Quiesce real writes before injecting status values or document pixels.
            ReflectionHelpers.setField(activity,"autosaveReady",false)
            ReflectionHelpers.getField<Handler>(activity,"autosaveHandler").removeCallbacks(
                ReflectionHelpers.getField<Runnable>(activity,"saveDraft"))
            val quietUntil=System.nanoTime()+15_000_000_000L
            while(activity.busy && System.nanoTime()<quietUntil) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
            assertFalse("Startup/autosave must quiesce before synthetic fixtures",activity.busy)
            assertEquals(tag,AppLanguage.selectedTag(activity))
            assertEquals(Locale.forLanguageTag(tag).language,activity.resources.configuration.locales[0].language)
            assertEquals(Locale.forLanguageTag(tag).language,Locale.getDefault().language)
            check(activity,controller)
        } finally {
            ReflectionHelpers.setField(activity,"autosaveReady",true)
            controller.pause().stop()
            val until=System.nanoTime()+15_000_000_000L
            while(activity.busy && System.nanoTime()<until) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
            controller.destroy()
            AppLanguage.select(app,oldTag);PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)
        }
    }
    private fun checkFit(profile: String,scale: Float,width: Int,height: Int)=withEditor("cs") {activity,controller ->
        assertProfile(activity,scale,width,height)
        checkCaption(activity,profile)
        exerciseZoom(activity)
        checkStatusTransitions(activity)
        // Real same-Activity configuration dispatch plus Display-backed window resize.
        // No fabricated child bounds, visible rectangles or synthetic recreation.
        val original=Configuration(activity.resources.configuration)
        val metrics=DisplayMetrics().apply {setTo(activity.resources.displayMetrics)}
        val rotated=Configuration(original).apply {
            screenWidthDp=height;screenHeightDp=width
            orientation=if(width<height) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT
        }
        val changedMetrics=DisplayMetrics().apply {setTo(metrics);widthPixels=(height*density).toInt();heightPixels=(width*density).toInt()}
        try {
            controller.configurationChange(rotated,changedMetrics,original.diff(rotated))
            ShadowDisplayManager.changeDisplay(Display.DEFAULT_DISPLAY,"+w${height}dp-h${width}dp-${if(width<height) "land" else "port"}")
            controller.visible();settle()
            assertSame(activity,controller.get())
            assertProfile(activity,scale,height,width)
            assertEquals(Color.BLUE,activity.document.bitmap.getPixel(20,30))
            assertFalse(activity.document.dirty)
            checkCaption(activity,"$profile-rotated")
            exerciseZoom(activity,false)
            checkStatusTransitions(activity)
        } finally {
            controller.configurationChange(original,metrics,rotated.diff(original))
            ShadowDisplayManager.changeDisplay(Display.DEFAULT_DISPLAY,"+w${width}dp-h${height}dp-${if(width<height) "port" else "land"}")
            controller.visible();settle()
        }
    }
    private fun assertProfile(activity: ClassicPaintActivity,scale: Float,width: Int,height: Int) {
        val config=activity.resources.configuration
        assertEquals(scale,config.fontScale,0f)
        assertEquals(width,config.screenWidthDp);assertEquals(height,config.screenHeightDp)
        assertEquals(if(width<height) Configuration.ORIENTATION_PORTRAIT else Configuration.ORIENTATION_LANDSCAPE,config.orientation)
        val root=activity.window.decorView;val visible=Rect()
        assertTrue(root.getLocalVisibleRect(visible));assertEquals(root.width,visible.width());assertEquals(root.height,visible.height())
        assertEquals("Actual native window width",(width*activity.resources.displayMetrics.density).toInt(),root.width)
        assertEquals("Actual native window height",(height*activity.resources.displayMetrics.density).toInt(),root.height)
    }
    private fun checkCaption(activity: ClassicPaintActivity,profile: String) {
        val root=activity.window.decorView
        val fit=root.findViewWithTag<View>("zoom_fit_view")
        val caption=activity.getString(R.string.ui_fit_entire_canvas_in_view)
        assertTrue(fit is ActionButton)
        assertEquals(caption,fit.contentDescription.toString())
        val visible=Rect()
        assertTrue("$profile: Fit visible",fit.getLocalVisibleRect(visible))
        assertTrue("Full hit target",visible.contains(Rect(0,0,fit.width,fit.height)))
        val footer=root.findViewWithTag<android.widget.LinearLayout>("status_bar")
        val controls=root.findViewWithTag<View>("zoom_controls")
        val status=root.findViewWithTag<View>("status_viewport")
        assertEquals(android.widget.LinearLayout.HORIZONTAL,footer.orientation)
        assertTrue("Corner zoom shares status row",controls.top==status.top && controls.width<footer.width)
        assertTrue("Canvas remains usable",activity.paintCanvas.width>=100*fit.resources.displayMetrics.density && activity.paintCanvas.height>=80*fit.resources.displayMetrics.density)
    }
    private fun exerciseZoom(activity: ClassicPaintActivity,newImage: Boolean=true) {
        val root=activity.window.decorView;val canvas=activity.paintCanvas
        if(newImage) {activity.document.newImage(120,80);activity.document.bitmap.setPixel(20,30,Color.BLUE);activity.document.markSaved()}
        for(tag in listOf("zoom_out","zoom_slider","zoom_in","zoom_fit_view")) {
            val control=root.findViewWithTag<View>(tag);val bounds=Rect()
            assertTrue("$tag visible",control.getLocalVisibleRect(bounds))
            assertTrue("$tag full native hit target",bounds.contains(Rect(0,0,control.width,control.height)))
            val minDp=if(tag=="zoom_slider" && !VerticalText.uiVertical(activity)) 64 else 40
            assertTrue("$tag useful width",control.width>=minDp*control.resources.displayMetrics.density)
        }
        val fit=root.findViewWithTag<View>("zoom_fit_view")
        tap(root,fit);settle();assertImageFits(canvas)
        val fitted=canvas.zoom;val slider=root.findViewWithTag<SeekBar>("zoom_slider")
        tap(root,root.findViewWithTag("zoom_in"));settle();assertTrue(canvas.zoom>fitted)
        assertEquals(canvas.sliderForZoom(),slider.progress)
        tap(root,root.findViewWithTag("zoom_out"));settle();assertEquals(fitted,canvas.zoom,.001f)
        val before=slider.progress
        swipe(root,slider,.25f,.5f,.75f,.5f);settle()
        assertNotEquals("Native slider gesture changes progress",before,slider.progress)
        assertEquals(canvas.sliderForZoom(),slider.progress)
        assertEquals(canvas.zoomForSlider(slider.progress),canvas.zoom,.01f)
        tap(root,fit);settle();assertImageFits(canvas)
        assertEquals(fitted,canvas.zoom,.001f)
        assertEquals(Color.BLUE,activity.document.bitmap.getPixel(20,30));assertFalse(activity.document.dirty);assertFalse(activity.document.canUndo)
    }
    private fun assertImageFits(canvas: PaintCanvas) {
        val a=canvas.toScreen(0f,0f);val b=canvas.toScreen(canvas.document.bitmap.width.toFloat(),canvas.document.bitmap.height.toFloat())
        val scrollbar=20*canvas.resources.displayMetrics.density
        assertTrue("Image left/top inside drawable viewport",a.x>=canvas.rulerInset && a.y>=canvas.rulerInset)
        assertTrue("Image right/bottom inside drawable viewport",b.x<=canvas.width-scrollbar+.01f && b.y<=canvas.height-scrollbar+.01f)
    }
    private fun checkStatusTransitions(activity: ClassicPaintActivity) {
        val root=activity.window.decorView;val canvas=activity.paintCanvas
        val footer=root.findViewWithTag<View>("status_bar")
        val status=root.findViewWithTag<TextView>("status_text")
        val viewport=root.findViewWithTag<ScrollView>("status_viewport")
        assertSame(viewport,status.parent);assertEquals(Int.MAX_VALUE,status.maxLines)
        awaitStatusLayout(status)
        val geometry=listOf(footer.width,footer.height,canvas.width,canvas.height)
        val draft=ReflectionHelpers.getField<UiMessage>(activity,"draftStatus")
        val longStatus=("Koncept nebyl uložen. Použijte příkaz Uložit. ").repeat(12)
        try {
            for((index,message) in listOf("Hotovo",longStatus,"Koncept uložen","Pracuje se…",longStatus).withIndex()) {
                activity.paintCanvas.setCursorMode(index%2==1)
                ReflectionHelpers.setField(activity,"draftStatus",UiMessage.Literal(message))
                ReflectionHelpers.setField(activity,"busy",index==3)
                ReflectionHelpers.setField(activity,"autosaving",index==3)
                ReflectionHelpers.callInstanceMethod<Unit>(activity,"updateStatus")
                val expected=if(index==3) activity.getString(R.string.ui_autosaving_draft)
                    else activity.getString(R.string.ui_px,canvas.tool.label,canvas.zoomStatusLabel(),
                        activity.document.bitmap.width,activity.document.bitmap.height,message)
                assertEquals("Complete selected status resource with fixture values",expected,status.text.toString())
                awaitStatusLayout(status)
                val layout=requireNotNull(status.layout)
                assertEquals(expected,layout.text.toString())
                assertTrue("Native status has lines",layout.lineCount>0)
                assertEquals("All UTF-16 status text is laid out",expected.length,layout.getLineEnd(layout.lineCount-1))
                for(line in 0 until layout.lineCount) assertEquals("Status line $line is not ellipsized",0,layout.getEllipsisCount(line))
                assertTrue("Complete native status height is retained",
                    status.height>=status.compoundPaddingTop+layout.height+status.compoundPaddingBottom)
                val node=status.createAccessibilityNodeInfo()
                try {assertEquals("Complete accessible status",expected,node.text.toString())} finally {node.recycle()}
                assertEquals("Status/cursor transitions must not resize canvas",geometry,listOf(footer.width,footer.height,canvas.width,canvas.height))
                assertEquals(Int.MAX_VALUE,status.maxLines)
            }
            assertTrue("Long status genuinely exceeds viewport: ${status.height} > ${viewport.height}",status.height>viewport.height)
            val viewportPoint=IntArray(2);val rootPoint=IntArray(2)
            viewport.getLocationOnScreen(viewportPoint);root.getLocationOnScreen(rootPoint)
            // A drag starts in the short status rail, but the captured pointer
            // can continue up into the canvas. Restricting every swipe to 80%
            // of 44dp loses touch slop repeatedly and imposes an artificial
            // travel ceiling on enlarged text. Keep the same 80-gesture bound
            // and stay inside the actual window, without programmatic scrolling.
            val endOffset=maxOf(-2f*viewport.height,1f-(viewportPoint[1]-rootPoint[1]))
            assertTrue("The window has room above the status rail for a native drag",endOffset<0f)
            var gestures=0
            repeat(80) {
                if(viewport.canScrollVertically(1)) {
                    val previous=viewport.scrollY
                    swipe(root,viewport,.5f,.9f,.5f,endOffset/viewport.height);settle();gestures++
                    assertTrue("Captured status drag advances: $previous -> ${viewport.scrollY}",
                        viewport.scrollY>previous || !viewport.canScrollVertically(1))
                }
            }
            assertFalse("Native gestures reach the final status line: gestures=$gestures, "+
                "scrollY=${viewport.scrollY}, content=${status.height}, viewport=${viewport.height}",viewport.canScrollVertically(1))
            val layout=requireNotNull(status.layout) {"Status lost native layout: ${status.width}×${status.height}; viewport ${viewport.width}×${viewport.height}"}
            assertTrue(layout.getLineBottom(layout.lineCount-1)<=viewport.scrollY+viewport.height)
            assertEquals(geometry,listOf(footer.width,footer.height,canvas.width,canvas.height))
            assertEquals("The captured status drag must not draw on the canvas",Color.BLUE,
                activity.document.bitmap.getPixel(20,30))
            assertFalse(activity.document.dirty);assertFalse(activity.document.canUndo)
        } finally {
            ReflectionHelpers.setField(activity,"draftStatus",draft)
            ReflectionHelpers.setField(activity,"busy",false);ReflectionHelpers.setField(activity,"autosaving",false)
            activity.paintCanvas.setCursorMode(false);ReflectionHelpers.callInstanceMethod<Unit>(activity,"updateStatus");settle()
        }
    }
    private fun awaitStatusLayout(status: TextView) {
        // setText invalidates the native Layout until the mounted window's next
        // traversal. A fixed sleep can leave old geometry paired with new text.
        // Do not measure/layout the child or force a window resize to repair it.
        fun ready()=status.isAttachedToWindow && !status.isLayoutRequested &&
            status.layout?.text?.toString()==status.text.toString()
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(3)
        while(!ready() && System.nanoTime()<deadline) {
            shadowOf(Looper.getMainLooper()).idleFor(16,TimeUnit.MILLISECONDS)
            if(!ready()) Thread.sleep(1)
        }
        assertTrue("Native status traversal did not finish: ${status.width}×${status.height}; "+
            "attached=${status.isAttachedToWindow}; layoutRequested=${status.isLayoutRequested}; "+
            "layout=${status.layout}; rootLayoutRequested=${status.rootView.isLayoutRequested}",ready())
    }
    private fun tap(root: View,view: View)=gesture(root,view,listOf(Triple(MotionEvent.ACTION_DOWN,.5f,.5f),Triple(MotionEvent.ACTION_UP,.5f,.5f)))
    private fun swipe(root: View,view: View,x0: Float,y0: Float,x1: Float,y1: Float) {
        val points=mutableListOf(Triple(MotionEvent.ACTION_DOWN,x0,y0))
        for(i in 1..8) points.add(Triple(MotionEvent.ACTION_MOVE,x0+(x1-x0)*i/8,y0+(y1-y0)*i/8))
        points.add(Triple(MotionEvent.ACTION_UP,x1,y1));gesture(root,view,points)
    }
    private fun gesture(root: View,view: View,points: List<Triple<Int,Float,Float>>) {
        val point=IntArray(2);val origin=IntArray(2);view.getLocationOnScreen(point);root.getLocationOnScreen(origin)
        val now=SystemClock.uptimeMillis()
        for((index,p) in points.withIndex()) MotionEvent.obtain(now,now+index*16,p.first,
            point[0]-origin[0]+view.width*p.second,point[1]-origin[1]+view.height*p.third,0).also {event ->
            try {assertTrue("Root-dispatched ${view.tag} input",root.dispatchTouchEvent(event))} finally {event.recycle()}
        }
        shadowOf(Looper.getMainLooper()).idleFor((points.size*16+20).toLong(),TimeUnit.MILLISECONDS)
    }
}
