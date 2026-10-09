/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.net.Uri
import android.os.Looper
import android.webkit.WebView
import com.caverock.androidsvg.SVG
import com.caverock.androidsvg.SVGParseException
import org.catrobat.paintroid.classic.BlankMapSvg
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.CreditEditSession
import org.catrobat.paintroid.classic.GalleryPage
import org.catrobat.paintroid.classic.ImageDimensions
import org.catrobat.paintroid.classic.ImageMemoryPolicy
import org.catrobat.paintroid.classic.ImageSizeException
import org.catrobat.paintroid.classic.IllustrationPage
import org.catrobat.paintroid.classic.IllustrationSource
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CommonsBlankMapsTest {
    private val page="https://commons.wikimedia.org/wiki/File:Blank_test_map.svg"
    private val original="https://upload.wikimedia.org/wikipedia/commons/a/ab/Blank_test_map.svg"
    private val rasterPage="https://commons.wikimedia.org/wiki/File:Blank_test_map.png"
    private val rasterOriginal="https://upload.wikimedia.org/wikipedia/commons/a/ab/Blank_test_map.png"
    private val svg="""
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="24" viewBox="0 0 40 24">
          <rect x="4" y="4" width="32" height="16" fill="none" stroke="#000000" stroke-width="2" stroke-dasharray="1,7"/>
        </svg>
    """.trimIndent()

    @Test fun commonsOnlyAcceptsOriginalVectorAndRasterFilesAndFilePages() {
        val source=IllustrationSource.COMMONS
        assertTrue(source.home.contains("/wiki/Category:Blank_maps"))
        assertTrue(source.allowsImage(Uri.parse(original)))
        assertTrue(source.allowsImage(Uri.parse(rasterOriginal)))
        assertFalse(source.allowsImage(Uri.parse("https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Blank_test_map.svg/800px-Blank_test_map.svg.png")))
        assertFalse(source.allowsImage(Uri.parse("https://upload.wikimedia.org.evil.example/wikipedia/commons/a/ab/Blank_test_map.svg")))
        assertFalse(source.allowsImage(Uri.parse("http://upload.wikimedia.org/wikipedia/commons/a/ab/Blank_test_map.svg")))
        assertTrue(source.isArtworkPage(Uri.parse(page)))
        assertFalse(source.isArtworkPage(Uri.parse(source.home)))
        val js=IllustrationPage.script(source,"Use image","Copy credit")
        assertTrue(js.contains(".fullMedia a.internal"))
        assertTrue(js.contains(IllustrationPage.USE_SCHEME))
        assertTrue(js.contains(GalleryPage.CREDIT_SCHEME))
        assertTrue(js.contains("if(link.textContent!==label)"))
        assertFalse(js.contains("image/2000px/"))
    }

    private fun withSvg(contents: String,check: (File)->Unit) {
        val context=RuntimeEnvironment.getApplication() as Context
        val source=File.createTempFile("blank-map-",".svg",context.cacheDir)
        try {source.writeText(contents);check(source)} finally {source.delete()}
    }

    @Test fun originalSizeUsesDeclaredWidthAndHeightNotViewBoxCoordinates() =
        withSvg(svg.replace("viewBox=\"0 0 40 24\"","viewBox=\"0 0 400 240\"")) {source ->
            assertEquals(ImageDimensions(40,24),BlankMapSvg.originalDimensions(source))
        }

    @Test fun physicalDimensionsUseCssPixelsRatherThanScreenDensity() =
        withSvg("""<svg xmlns="http://www.w3.org/2000/svg" width="1in" height="2in" viewBox="0 0 40 24"/>""") {source ->
            assertEquals(ImageDimensions(96,192),BlankMapSvg.originalDimensions(source))
        }

    @Test fun unspecifiedOriginalSizeDoesNotBecomeACanvasOrViewBoxPixelSize() =
        withSvg("""<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 40 24"/>""") {source ->
            try {BlankMapSvg.originalDimensions(source);fail("A relative viewport must not be invented as an original size")}
            catch(_: IllegalArgumentException) { }
        }

    @Test fun internalEntitiesCannotProvideOriginalDimensionsOrProduceAnImage() = withSvg("""
        <!DOCTYPE svg [
          <!ENTITY digit "4">
          <!ENTITY originalWidth "&digit;0">
        ]>
        <svg xmlns="http://www.w3.org/2000/svg" width="&originalWidth;" height="24"/>
    """.trimIndent()) {input ->
        val output=File.createTempFile("blank-map-",".png",input.parentFile)
        val previous=SVG.isInternalEntitiesEnabled()
        fun rejected(action: ()->Unit) {
            // Reproduce the library's permissive default before each production entry point.
            // Expansion is deliberately tiny: it would only produce the valid width "40".
            SVG.setInternalEntitiesEnabled(true)
            try {action();fail("Custom entities must not supply an original SVG dimension")}
            catch(_: SVGParseException) { }
            catch(error: IllegalArgumentException) {
                assertFalse("A memory-policy refusal does not prove entity parsing is disabled",error is ImageSizeException)
            }
            assertFalse("Import must disable the parser's internal-entity expansion",SVG.isInternalEntitiesEnabled())
        }
        try {
            rejected {BlankMapSvg.originalDimensions(input)}
            rejected {BlankMapSvg.renderOriginal(input,output,ImageMemoryPolicy.forRuntime())}
            assertEquals("Rejected SVG must not leave a rendered image",0L,output.length())
        } finally {SVG.setInternalEntitiesEnabled(previous);output.delete()}
    }

    @Test fun nestedInternalEntityMarkupCannotAddPixelsToTheBlankMap() {
        // Four small red rectangles exercise nested expansion with a bounded fixture.
        // With entities enabled, the inserted rectangles turn the white map/background red.
        val declarations="""
            <!DOCTYPE svg [
              <!ENTITY red "<rect x='0' y='0' width='40' height='24' fill='#ff0000'/>">
              <!ENTITY twice "&red;&red;">
              <!ENTITY four "&twice;&twice;">
            ]>
        """.trimIndent()
        withSvg(declarations+"\n"+svg.replace("<rect","&four;\n<rect")) {input ->
            val output=File.createTempFile("blank-map-",".png",input.parentFile)
            val previous=SVG.isInternalEntitiesEnabled()
            try {
                SVG.setInternalEntitiesEnabled(true)
                var rejected=false
                try {BlankMapSvg.renderOriginal(input,output,ImageMemoryPolicy.forRuntime())}
                catch(_: SVGParseException) {rejected=true}
                assertFalse("Import must disable the parser's internal-entity expansion",SVG.isInternalEntitiesEnabled())
                if(rejected) assertEquals("Rejected SVG must not leave a rendered image",0L,output.length())
                else {
                    val bitmap=BitmapFactory.decodeFile(output.path)
                    assertNotNull(bitmap)
                    try {assertOriginalHardEdges(bitmap)} finally {bitmap.recycle()}
                }
            } finally {SVG.setInternalEntitiesEnabled(previous);output.delete()}
        }
    }

    private fun assertOriginalHardEdges(bitmap: Bitmap) {
        assertEquals(40,bitmap.width);assertEquals(24,bitmap.height)
        assertEquals(Color.WHITE,bitmap.getPixel(20,12))
        assertEquals(Color.BLACK,bitmap.getPixel(20,4))
        for(y in 0 until bitmap.height) for(x in 0 until bitmap.width) {
            val color=bitmap.getPixel(x,y)
            assertEquals("Unexpected transparency at ("+x+","+y+")",255,Color.alpha(color))
            assertTrue("Unexpected colour or anti-aliased fringe at ("+x+","+y+")",color==Color.BLACK || color==Color.WHITE)
        }
    }

    @Test fun svgOutputHasOriginalDimensionsSolidStrokeNoAntiAliasingAndWhiteBackground() = withSvg(svg) {input ->
        val output=File.createTempFile("blank-map-", ".png", input.parentFile)
        try {
            assertEquals(ImageDimensions(40,24),BlankMapSvg.originalDimensions(input))
            BlankMapSvg.renderOriginal(input,output,ImageMemoryPolicy.forRuntime())
            val bitmap=BitmapFactory.decodeFile(output.path)
            assertNotNull(bitmap)
            try {assertOriginalHardEdges(bitmap)} finally {bitmap.recycle()}
        } finally {output.delete()}
    }

    @Test fun originalSizeIsNotClampedToTenThousandPixels() =
        withSvg("""<svg xmlns="http://www.w3.org/2000/svg" width="12001" height="1"/>""") {input ->
            val output=File.createTempFile("blank-map-",".png",input.parentFile)
            try {
                BlankMapSvg.renderOriginal(input,output,ImageMemoryPolicy.forRuntime())
                val bitmap=BitmapFactory.decodeFile(output.path)
                try {assertEquals(12001,bitmap.width);assertEquals(1,bitmap.height)} finally {bitmap.recycle()}
            } finally {output.delete()}
        }

    @Test fun insufficientMemoryRejectsTheOriginalInsteadOfShrinkingIt() = withSvg(svg) {input ->
        val output=File.createTempFile("blank-map-",".png",input.parentFile)
        try {
            val policy=ImageMemoryPolicy.calculate(0,0,0,0,false)
            try {BlankMapSvg.renderOriginal(input,output,policy);fail("Must not silently resize an original SVG")}
            catch(_: ImageSizeException) {assertEquals(0L,output.length())}
        } finally {output.delete()}
    }

    private class Connection(url: URL,private val data: InputStream): HttpURLConnection(url) {
        override fun connect()=Unit
        override fun disconnect() {data.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=200
        override fun getInputStream()=data
    }

    private fun await(ready: ()->Boolean) {
        val end=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
        while(!ready() && System.nanoTime()<end) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
        shadowOf(Looper.getMainLooper()).idle();assertTrue("Gallery action timed out",ready())
    }
    private fun gallery()=Robolectric.buildActivity(MediaGalleryActivity::class.java,
        Intent(RuntimeEnvironment.getApplication(),MediaGalleryActivity::class.java)
            // Deliberately unrelated to the original. Legacy canvas metadata must not affect rendering.
            .putExtra("gallery_provider",IllustrationSource.COMMONS.name).putExtra("gallery_canvas_width",12345)).setup()

    @Test fun galleryDownloadsAndRendersAtOriginalSizeWithoutAskingForDimensions() {
        val controller=gallery();val activity=controller.get()
        try {
            activity.openConnection={Connection(it,ByteArrayInputStream((if(it.host=="commons.wikimedia.org")
                CommonsTestMetadata.response(original,page) else svg).toByteArray()))}
            val web=ReflectionHelpers.getField<WebView>(activity,"web")
            val link=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
                .appendQueryParameter("source",original).appendQueryParameter("page",page)
                .appendQueryParameter("title","Blank test map").build()
            assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,link.toString()))
            await {activity.isFinishing && !activity.downloading}
            assertFalse("No size-selection dialog is allowed",ShadowAlertDialog.getLatestAlertDialog()?.isShowing==true)
            assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
            val result=shadowOf(activity).resultIntent
            assertEquals(original,result.getStringExtra("gallery_source"))
            val token=result.getStringExtra(CreditEditSession.EXTRA_SESSION)
            assertNotNull("Downloaded image must carry its document credit session",token)
            assertTrue(CreditEditSession.open(activity.filesDir,token!!).credits.isEmpty())
            val file=File(activity.cacheDir,result.getStringExtra("gallery_file")!!)
            try {
                assertTrue(file.isFile)
                val bitmap=BitmapFactory.decodeFile(file.path)
                try {assertEquals(40,bitmap.width);assertEquals(24,bitmap.height)} finally {bitmap.recycle()}
            } finally {file.delete()}
        } finally {if(!activity.isDestroyed)controller.pause().stop().destroy()}
    }

    @Test fun galleryKeepsRasterPixelsAndImportsTransparentAreasAsWhite() {
        val bitmap=Bitmap.createBitmap(2,1,Bitmap.Config.ARGB_8888)
        bitmap.setPixel(0,0,Color.RED);bitmap.setPixel(1,0,Color.TRANSPARENT)
        val bytes=ByteArrayOutputStream().also {bitmap.compress(Bitmap.CompressFormat.PNG,100,it)}.toByteArray()
        bitmap.recycle()
        val controller=gallery();val activity=controller.get()
        try {
            activity.openConnection={Connection(it,ByteArrayInputStream(if(it.host=="commons.wikimedia.org")
                CommonsTestMetadata.response(rasterOriginal,rasterPage).toByteArray() else bytes))}
            val web=ReflectionHelpers.getField<WebView>(activity,"web")
            val link=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
                .appendQueryParameter("source",rasterOriginal).appendQueryParameter("page",rasterPage)
                .appendQueryParameter("title","Raster blank map").build()
            assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,link.toString()))
            await {activity.isFinishing && !activity.downloading}
            val result=shadowOf(activity).resultIntent
            val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
            val main=mainController.get()
            try {
                awaitEditorStartup(main)
                main.document.background=Color.GREEN;main.document.newImage(2,1)
                main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
                await {!main.busy}
                assertNotNull(main.document.selection)
                main.document.finishSelection()
                assertEquals(Color.RED,main.document.bitmap.getPixel(0,0))
                assertEquals(Color.WHITE,main.document.bitmap.getPixel(1,0))
                assertEquals(listOf(rasterOriginal),main.document.imageCredits.map {it.source})
                val credit=main.document.imageCredits.single().text
                assertTrue(credit.contains(rasterPage));assertTrue(credit.contains("by-sa/3.0/"))
                assertFalse("Raster import must not claim SVG rasterisation",credit.contains("antiAlias=false"))
            } finally {mainController.pause().stop();await {!main.busy};mainController.destroy()}
        } finally {if(!activity.isDestroyed)controller.pause().stop().destroy()}
    }
}
