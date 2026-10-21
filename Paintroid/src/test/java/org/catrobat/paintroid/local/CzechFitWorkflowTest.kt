/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Rect
import android.os.Looper
import android.os.SystemClock
import android.util.TypedValue
import android.view.MotionEvent
import android.view.View
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
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.util.Locale
import java.util.concurrent.TimeUnit

/** Mounted native layout and root-dispatched input, not an installed-device claim. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CzechFitWorkflowTest {
    @Test @Config(fontScale=1f) fun normalPortraitFitPreservesFullCaptionAndCanvas()=checkFit("portrait-1x")
    @Test @Config(fontScale=2f) fun enlargedPortraitFitPreservesFullCaptionAndCanvas()=checkFit("portrait-2x")
    @Test @Config(fontScale=1f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun normalLandscapeFitPreservesFullCaptionAndCanvas()=checkFit("landscape-1x")
    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun enlargedLandscapeFitPreservesFullCaptionAndCanvas()=checkFit("landscape-2x")

    private fun settle()=shadowOf(Looper.getMainLooper()).idleFor(50,TimeUnit.MILLISECONDS)
    private fun checkFit(profile: String) {
        val app=RuntimeEnvironment.getApplication() as Context
        val oldTag=AppLanguage.selectedTag(app);val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        app.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        app.getSharedPreferences("classic-ui",0).edit().clear().commit()
        AppLanguage.select(app,"cs")
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity=controller.setup().visible().windowFocusChanged(true).get()
        try {
            awaitEditorStartup(activity);settle()
            assertEquals("cs",AppLanguage.selectedTag(activity))
            assertEquals("cs",activity.resources.configuration.locales[0].language)
            assertEquals("cs",Locale.getDefault().language)
            val root=activity.window.decorView
            val fit=root.findViewWithTag<TextView>("zoom_fit_view")
            val caption="Přizpůsobit obrázek oknu"
            assertEquals(caption,fit.text.toString())
            assertEquals(caption,fit.contentDescription.toString())
            assertEquals(caption,activity.getString(R.string.ui_fit_entire_canvas_in_view))
            assertEquals("Never shrink the caption",TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_SP,
                13f,fit.resources.displayMetrics),fit.textSize,0f)
            val layout=requireNotNull(fit.layout)
            val directory=File("build/reports/czech-workflows/fit").apply {mkdirs()}
            val visible=Rect();val isVisible=fit.getLocalVisibleRect(visible)
            val receipt=JSONObject().put("profile",profile).put("sdk",RuntimeEnvironment.getApiLevel())
                .put("locale",Locale.getDefault().toLanguageTag()).put("font_scale",fit.resources.configuration.fontScale)
                .put("caption",fit.text.toString()).put("accessible",fit.contentDescription.toString())
                .put("width",fit.width).put("height",fit.height).put("text_size_px",fit.textSize)
                .put("layout_height",layout.height).put("line_count",layout.lineCount)
                .put("visible",visible.toShortString()).put("canvas_width",activity.paintCanvas.width)
                .put("canvas_height",activity.paintCanvas.height)
            File(directory,"$profile.json").writeText(receipt.toString(2)+"\n")
            val screenshot=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
            try {root.draw(Canvas(screenshot));File(directory,"$profile.png").outputStream().use {
                assertTrue(screenshot.compress(Bitmap.CompressFormat.PNG,100,it))
            }} finally {screenshot.recycle()}
            assertTrue("Fit control visible",isVisible)
            assertTrue("Full native hit target",visible.contains(Rect(0,0,fit.width,fit.height)))
            assertTrue("Complete caption lines",layout.lineCount>0)
            assertEquals(caption.length,layout.getLineEnd(layout.lineCount-1))
            for(line in 0 until layout.lineCount) {
                assertEquals("No ellipsis",0,layout.getEllipsisCount(line))
                assertTrue("No horizontal clipping",layout.getLineLeft(line)>=-1 && layout.getLineRight(line)<=layout.width+1)
            }
            assertTrue("Full Fit caption height: ${layout.height} > ${fit.height-fit.totalPaddingTop-fit.totalPaddingBottom}",
                layout.height<=fit.height-fit.totalPaddingTop-fit.totalPaddingBottom)
            for(tag in listOf("zoom_out","zoom_slider","zoom_in")) {
                val control=root.findViewWithTag<View>(tag);val bounds=Rect()
                assertTrue("$tag visible",control.getLocalVisibleRect(bounds))
                assertTrue("$tag complete",bounds.contains(Rect(0,0,control.width,control.height)))
                assertTrue("$tag keeps useful width",control.width>=40*control.resources.displayMetrics.density)
            }
            assertTrue("Canvas remains usable",activity.paintCanvas.width>=100*fit.resources.displayMetrics.density &&
                activity.paintCanvas.height>=80*fit.resources.displayMetrics.density)
            activity.document.newImage(120,80);activity.document.bitmap.setPixel(20,30,android.graphics.Color.BLUE)
            activity.document.markSaved();activity.paintCanvas.fit();settle()
            val fitted=activity.paintCanvas.zoom
            activity.paintCanvas.zoomAt(fitted*2);settle()
            assertNotEquals(fitted,activity.paintCanvas.zoom)
            val point=IntArray(2);val origin=IntArray(2)
            fit.getLocationOnScreen(point);root.getLocationOnScreen(origin)
            val x=(point[0]-origin[0]+fit.width/2).toFloat();val y=(point[1]-origin[1]+fit.height/2).toFloat()
            val now=SystemClock.uptimeMillis()
            for((index,action) in listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP).withIndex()) {
                MotionEvent.obtain(now,now+index*16,action,x,y,0).also {event ->
                    try {assertTrue("Root-dispatched Fit tap",root.dispatchTouchEvent(event))} finally {event.recycle()}
                }
            }
            settle()
            assertEquals("Tap fits the document",fitted,activity.paintCanvas.zoom,0.001f)
            assertEquals(android.graphics.Color.BLUE,activity.document.bitmap.getPixel(20,30))
            assertFalse("Zoom does not edit the document",activity.document.dirty)
            assertFalse(activity.document.canUndo)
        } finally {
            controller.pause().stop()
            val until=System.nanoTime()+15_000_000_000L
            while(activity.busy && System.nanoTime()<until) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(10)}
            controller.destroy()
            AppLanguage.select(app,oldTag);PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)
        }
    }
}
