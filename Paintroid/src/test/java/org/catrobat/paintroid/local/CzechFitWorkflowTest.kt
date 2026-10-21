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
    @Test @Config(fontScale=1f) fun compactEnglishFooterRetainsDirectStatus()=withEditor("en-US") {activity,_ ->
        assertFalse(activity.window.decorView.findViewWithTag<View>("status_text").parent is ScrollView)
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
        val fit=root.findViewWithTag<TextView>("zoom_fit_view")
        val caption="Přizpůsobit obrázek oknu"
        assertEquals(caption,fit.text.toString());assertEquals(caption,fit.contentDescription.toString())
        assertEquals(caption,activity.getString(R.string.ui_fit_entire_canvas_in_view))
        assertEquals("Never shrink the caption",TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_SP,13f,fit.resources.displayMetrics),fit.textSize,0f)
        val layout=requireNotNull(fit.layout)
        val directory=File("build/reports/czech-workflows/fit").apply {mkdirs()}
        val visible=Rect();val isVisible=fit.getLocalVisibleRect(visible)
        val receipt=JSONObject().put("profile",profile).put("sdk",RuntimeEnvironment.getApiLevel())
            .put("locale",Locale.getDefault().toLanguageTag()).put("font_scale",fit.resources.configuration.fontScale)
            .put("caption",fit.text.toString()).put("accessible",fit.contentDescription.toString())
            .put("width",fit.width).put("height",fit.height).put("text_size_px",fit.textSize)
            .put("layout_height",layout.height).put("line_count",layout.lineCount)
            .put("visible",visible.toShortString()).put("canvas_width",activity.paintCanvas.width).put("canvas_height",activity.paintCanvas.height)
        File(directory,"$profile.json").writeText(receipt.toString(2)+"\n")
        val screenshot=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
        try {root.draw(Canvas(screenshot));File(directory,"$profile.png").outputStream().use {assertTrue(screenshot.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {screenshot.recycle()}
        assertTrue("Fit visible",isVisible);assertTrue("Full hit target",visible.contains(Rect(0,0,fit.width,fit.height)))
        assertTrue("Caption lines",layout.lineCount>0);assertEquals(caption.length,layout.getLineEnd(layout.lineCount-1))
        val contentWidth=fit.width-fit.compoundPaddingLeft-fit.compoundPaddingRight
        for(line in 0 until layout.lineCount) {
            assertEquals("No ellipsis",0,layout.getEllipsisCount(line))
            assertTrue("No horizontal clipping",layout.getLineLeft(line)>=-1 && layout.getLineRight(line)<=contentWidth+1)
        }
        assertTrue("Full Fit caption height",layout.height<=fit.height-fit.totalPaddingTop-fit.totalPaddingBottom)
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
        val geometry=listOf(footer.width,footer.height,canvas.width,canvas.height)
        val draft=ReflectionHelpers.getField<String>(activity,"draftStatus")
        val longStatus=("Koncept nebyl uložen. Použijte příkaz Uložit. ").repeat(12)
        try {
            for((index,message) in listOf("Hotovo",longStatus,"Koncept uložen","Pracuje se…",longStatus).withIndex()) {
                activity.paintCanvas.setCursorMode(index%2==1)
                ReflectionHelpers.setField(activity,"draftStatus",message)
                ReflectionHelpers.setField(activity,"busy",index==3)
                ReflectionHelpers.setField(activity,"autosaving",index==3)
                ReflectionHelpers.callInstanceMethod<Unit>(activity,"updateStatus");settle()
                if(index==3) assertEquals(activity.getString(R.string.ui_autosaving_draft),status.text.toString())
                else assertTrue("Intended synthetic status is actually rendered",status.text.toString().contains(message))
                assertEquals("Status/cursor transitions must not resize canvas",geometry,listOf(footer.width,footer.height,canvas.width,canvas.height))
                assertEquals(Int.MAX_VALUE,status.maxLines)
            }
            assertTrue("Long status genuinely exceeds viewport",status.height>viewport.height)
            repeat(80) {
                if(viewport.canScrollVertically(1)) {swipe(root,viewport,.5f,.9f,.5f,.1f);settle()}
            }
            assertFalse("Native gestures reach the final status line",viewport.canScrollVertically(1))
            assertTrue(status.layout.getLineBottom(status.layout.lineCount-1)<=viewport.scrollY+viewport.height)
            assertEquals(geometry,listOf(footer.width,footer.height,canvas.width,canvas.height))
        } finally {
            ReflectionHelpers.setField(activity,"draftStatus",draft)
            ReflectionHelpers.setField(activity,"busy",false);ReflectionHelpers.setField(activity,"autosaving",false)
            activity.paintCanvas.setCursorMode(false);ReflectionHelpers.callInstanceMethod<Unit>(activity,"updateStatus");settle()
        }
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
