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
import android.widget.EditText
import org.catrobat.paintroid.classic.BlankMapSvg
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.GalleryPage
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
        // Repeated MutationObserver callbacks must not rewrite text/attributes forever.
        assertTrue(js.contains("if(link.textContent!==label)"))
        assertFalse(js.contains("image/2000px/"))
    }

    @Test fun svgOutputHasExactDimensionsSolidStrokeNoAntiAliasingAndWhiteBackground() {
        val context=RuntimeEnvironment.getApplication() as Context
        val input=File.createTempFile("blank-map-", ".svg", context.cacheDir)
        val output=File.createTempFile("blank-map-", ".png", context.cacheDir)
        try {
            input.writeText(svg)
            assertEquals(40.0/24.0, BlankMapSvg.aspectRatio(input),.01)
            BlankMapSvg.render(input,output,80,48)
            val bitmap=BitmapFactory.decodeFile(output.path)
            assertNotNull(bitmap)
            try {
                assertEquals(80,bitmap.width);assertEquals(48,bitmap.height)
                assertEquals(Color.WHITE,bitmap.getPixel(40,24))
                // The dash array cannot introduce a leak along the top border.
                assertEquals(Color.BLACK,bitmap.getPixel(40,8))
                for(y in 0 until bitmap.height) for(x in 0 until bitmap.width) {
                    val color=bitmap.getPixel(x,y)
                    assertEquals("Unexpected transparency at ("+x+","+y+")",255,Color.alpha(color))
                    assertTrue("Anti-aliased fringe at ("+x+","+y+")",
                        color==Color.BLACK || color==Color.WHITE)
                }
            } finally {bitmap.recycle()}
        } finally {input.delete();output.delete()}
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
        while(!ready() && System.nanoTime()<end) {
            shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)
        }
        shadowOf(Looper.getMainLooper()).idle()
        assertTrue("Gallery action timed out",ready())
    }
    private fun gallery()=Robolectric.buildActivity(MediaGalleryActivity::class.java,
        Intent(RuntimeEnvironment.getApplication(),MediaGalleryActivity::class.java)
            .putExtra("gallery_provider",IllustrationSource.COMMONS.name).putExtra("gallery_canvas_width",80)).setup()

    @Test fun galleryDownloadsOriginalSvgAndReturnsRenderedPngOnlyAfterChoosingSize() {
        val controller=gallery();val activity=controller.get()
        try {
            activity.openConnection={Connection(it,ByteArrayInputStream(svg.toByteArray()))}
            val web=ReflectionHelpers.getField<WebView>(activity,"web")
            val link=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
                .appendQueryParameter("source",original).appendQueryParameter("page",page)
                .appendQueryParameter("title","Blank test map").build()
            assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,link.toString()))
            await { !activity.downloading && ShadowAlertDialog.getLatestAlertDialog()?.isShowing==true }
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
            val dialog=ShadowAlertDialog.getLatestAlertDialog()
            val width=dialog.window!!.decorView.findViewWithTag<EditText>("commons_svg_width")
            val height=dialog.window!!.decorView.findViewWithTag<EditText>("commons_svg_height")
            assertEquals("80",width.text.toString())
            width.setText("80");height.setText("48")
            dialog.getButton(android.app.AlertDialog.BUTTON_POSITIVE).performClick()
            await { activity.isFinishing && !activity.downloading }
            assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
            val result=shadowOf(activity).resultIntent
            assertEquals(original,result.getStringExtra("gallery_source"))
            val file=File(activity.cacheDir,result.getStringExtra("gallery_file")!!)
            assertTrue(file.isFile);assertEquals(0x89,file.readBytes()[0].toInt() and 0xff)
            file.delete()
        } finally {if(!activity.isDestroyed)controller.pause().stop().destroy()}
    }

    @Test fun galleryKeepsRasterPixelsAndImportsTransparentAreasAsWhite() {
        val bitmap=Bitmap.createBitmap(2,1,Bitmap.Config.ARGB_8888)
        bitmap.setPixel(0,0,Color.RED);bitmap.setPixel(1,0,Color.TRANSPARENT)
        val bytes=ByteArrayOutputStream().also {bitmap.compress(Bitmap.CompressFormat.PNG,100,it)}.toByteArray()
        bitmap.recycle()
        val controller=gallery();val activity=controller.get()
        try {
            activity.openConnection={Connection(it,ByteArrayInputStream(bytes))}
            val web=ReflectionHelpers.getField<WebView>(activity,"web")
            val link=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
                .appendQueryParameter("source",rasterOriginal).appendQueryParameter("page",rasterPage)
                .appendQueryParameter("title","Raster blank map").build()
            assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,link.toString()))
            await { activity.isFinishing && !activity.downloading }
            val result=shadowOf(activity).resultIntent
            val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
            val main=mainController.get()
            try {
                main.document.background=Color.GREEN;main.document.newImage(2,1)
                main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
                await {!main.busy}
                assertNotNull(main.document.selection)
                main.document.finishSelection()
                assertEquals(Color.RED,main.document.bitmap.getPixel(0,0))
                assertEquals(Color.WHITE,main.document.bitmap.getPixel(1,0))
            } finally {mainController.pause().stop();await {!main.busy};mainController.destroy()}
        } finally {if(!activity.isDestroyed)controller.pause().stop().destroy()}
    }
}
