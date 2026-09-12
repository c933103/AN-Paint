/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Looper
import android.webkit.WebView
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
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
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

/** Production WebView selection/download/result path, with only the HTTPS transport substituted. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class GalleryImportTest {
    private lateinit var controller: ActivityController<MediaGalleryActivity>
    private lateinit var gallery: MediaGalleryActivity
    private val asset=Uri.parse("https://catrobat.org/wp-content/uploads/2025/01/Needle_Yellow.png")
    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        context.cacheDir.listFiles()?.filter {it.name.startsWith("gallery-")}?.forEach {it.delete()}
        context.getSharedPreferences("image-credits",0).edit().clear().commit()
        controller=Robolectric.buildActivity(MediaGalleryActivity::class.java)
        gallery=controller.setup().get()
    }
    @After fun stop() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        if(!gallery.isDestroyed) controller.pause().stop().destroy()
        await { !gallery.downloading }
    }
    private fun await(done: ()->Boolean) {
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
        while(!done() && System.nanoTime()<deadline) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
        shadowOf(Looper.getMainLooper()).idle();assertTrue("Background operation timed out",done())
    }
    private fun imageBytes(): ByteArray {
        val image=Bitmap.createBitmap(3,1,Bitmap.Config.ARGB_8888)
        image.setPixel(0,0,Color.RED);image.setPixel(1,0,Color.TRANSPARENT);image.setPixel(2,0,0x800000ff.toInt())
        return ByteArrayOutputStream().also { assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it));image.recycle() }.toByteArray()
    }
    private class Connection(url: URL,private val stream: InputStream,private val code: Int=200,private val location: String?=null): HttpURLConnection(url) {
        @Volatile var disconnected=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true;stream.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=code
        override fun getInputStream()=stream
        override fun getHeaderField(name: String): String?=if(name=="Location") location else null
    }
    private fun selectAsset() {
        val web=ReflectionHelpers.getField<WebView>(gallery,"web")
        assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,asset.toString()))
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        assertTrue(dialog.isShowing);dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        // AlertDialog sends button listeners through its main-thread Handler.
        // Deliver that message before observing the worker state or blocking on
        // the transfer latch; performClick() alone has not started the download.
        shadowOf(Looper.getMainLooper()).idle()
    }
    @Test fun downloadableImageReturnsThroughGalleryAndCompositesOntoExistingPixelsWithSourceCredit() {
        val connection=Connection(URL(asset.toString()),ByteArrayInputStream(imageBytes()))
        gallery.openConnection={connection}
        selectAsset();await { !gallery.downloading }
        assertEquals(Activity.RESULT_OK,shadowOf(gallery).resultCode);assertTrue(connection.disconnected)
        val result=shadowOf(gallery).resultIntent
        assertEquals(asset.toString(),result.getStringExtra("gallery_source"))
        val downloaded=File(gallery.cacheDir,result.getStringExtra("gallery_file")!!);assertTrue(downloaded.isFile)
        val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val main=mainController.setup().get()
        try {
            main.document.background=Color.GREEN;main.document.newImage(3,1)
            main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,result)
            await { !main.busy };assertNull(main.lastIoError)
            assertNotNull(main.document.selection)
            main.document.finishSelection()
            assertEquals(Color.RED,main.document.bitmap.getPixel(0,0))
            assertEquals(Color.GREEN,main.document.bitmap.getPixel(1,0))
            assertEquals(0xff007f80.toInt(),main.document.bitmap.getPixel(2,0))
            assertEquals(setOf(asset.toString()),main.getSharedPreferences("image-credits",0).getStringSet("sources",emptySet()))
            assertFalse(downloaded.exists())
        } finally {mainController.pause().stop();await { !main.busy };mainController.destroy()}
    }
    @Test fun closingGalleryDuringDownloadCannotReturnAnImageOrLeaveItsTemporaryCopy() {
        val started=CountDownLatch(1);val release=CountDownLatch(1)
        val bytes=imageBytes()
        val stream=object: ByteArrayInputStream(bytes) {
            override fun read(buffer: ByteArray,offset: Int,length: Int): Int {
                started.countDown();check(release.await(5,TimeUnit.SECONDS));return super.read(buffer,offset,length)
            }
        }
        val connection=Connection(URL(asset.toString()),stream);gallery.openConnection={connection}
        selectAsset();assertTrue(started.await(5,TimeUnit.SECONDS))
        // Back/Done first calls finish(); destruction can happen after the pending result.
        gallery.finish();release.countDown();await { !gallery.downloading }
        assertEquals(Activity.RESULT_CANCELED,shadowOf(gallery).resultCode)
        assertTrue(connection.disconnected)
        assertTrue(gallery.cacheDir.listFiles()!!.none {it.name.startsWith("gallery-")})
    }
    @Test fun unsupportedRedirectAndCorruptImageNeverProduceAnInsertableResult() {
        val redirect=Connection(URL(asset.toString()),ByteArrayInputStream(byteArrayOf()),302,"https://unrelated.example/image.png")
        var calls=0;gallery.openConnection={calls++;redirect}
        selectAsset();await { !gallery.downloading }
        assertEquals(1,calls);assertTrue(redirect.disconnected);assertFalse(gallery.isFinishing)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(gallery).resultCode)
        val corrupt=Connection(URL(asset.toString()),ByteArrayInputStream("not an image".toByteArray()))
        gallery.openConnection={corrupt};selectAsset();await { !gallery.downloading }
        assertTrue(corrupt.disconnected);assertEquals(Activity.RESULT_CANCELED,shadowOf(gallery).resultCode)
        assertTrue(gallery.cacheDir.listFiles()!!.none {it.name.startsWith("gallery-")})
    }
}
