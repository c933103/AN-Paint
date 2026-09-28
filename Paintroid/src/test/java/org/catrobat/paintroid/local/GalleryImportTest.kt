/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.ClipboardManager
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.os.Looper
import android.webkit.WebView
import android.widget.Button
import android.widget.EditText
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.GalleryCredits
import org.catrobat.paintroid.classic.IllustrationPage
import org.catrobat.paintroid.classic.IllustrationSource
import org.catrobat.paintroid.classic.GalleryPage
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
import org.robolectric.shadows.ShadowDialog
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
        assertNull("Using a gallery image must not require confirmation",ShadowAlertDialog.getLatestAlertDialog())
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
            assertEquals(listOf(asset.toString()),main.document.imageCredits.map {it.source})
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
    @Test fun imageCreditActionCopiesSpecificSourceWithoutDownloadingOrInventingAnIndividualCreator() {
        gallery.openConnection={error("Copying a credit must not download the image")}
        val web=ReflectionHelpers.getField<WebView>(gallery,"web")
        val action=Uri.Builder().scheme(GalleryPage.CREDIT_SCHEME).authority("copy").appendQueryParameter("source",asset.toString())
            .appendQueryParameter("title","Needle Yellow").build()
        assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,action.toString()))
        val clipboard=gallery.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        val credit=clipboard.primaryClip!!.getItemAt(0).text.toString()
        assertTrue(credit.contains("Needle Yellow"));assertTrue(credit.contains(asset.toString()))
        assertTrue(credit.contains("Publisher: Catrobat project"));assertTrue(credit.contains(GalleryCredits.CC_BY_SA))
        assertFalse(credit.contains("Modified"));assertFalse(gallery.isFinishing)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(gallery).resultCode)
    }
    @Test fun additionalProvidersImportAnExplicitArtworkAndPreserveTheirOwnTerms() {
        for(provider in listOf(IllustrationSource.IRASUTOYA,IllustrationSource.OPENCLIPART)) {
            controller.pause().stop().destroy();await {!gallery.downloading}
            val intent=android.content.Intent(RuntimeEnvironment.getApplication(),MediaGalleryActivity::class.java).putExtra("gallery_provider",provider.name)
            controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,intent);gallery=controller.setup().get()
            val source=if(provider==IllustrationSource.IRASUTOYA) "https://blogger.googleusercontent.com/img/b/art/s740/character_typhoon.png" else "https://openclipart.org/image/2000px/250963"
            val page=if(provider==IllustrationSource.IRASUTOYA) "https://www.irasutoya.com/2026/06/typhoon.html" else "https://openclipart.org/detail/250963/public-domain"
            gallery.openConnection={Connection(it,ByteArrayInputStream(imageBytes()))}
            val web=ReflectionHelpers.getField<WebView>(gallery,"web")
            val use=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
                .appendQueryParameter("source",source).appendQueryParameter("page",page).appendQueryParameter("title","Example artwork")
                .appendQueryParameter("author","Listed artist").appendQueryParameter("author_url","https://example.org/artist")
                .appendQueryParameter("licence","Declared licence https://example.org/terms").build()
            assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,use.toString()));await {!gallery.downloading}
            assertEquals(Activity.RESULT_OK,shadowOf(gallery).resultCode)
            val result=shadowOf(gallery).resultIntent
            assertEquals(provider.name,result.getStringExtra("gallery_provider"));assertEquals(page,result.getStringExtra("gallery_page"))
            assertEquals("Listed artist",result.getStringExtra("gallery_author"))
            assertEquals("https://example.org/artist",result.getStringExtra("gallery_author_url"))
            assertEquals("Declared licence https://example.org/terms",result.getStringExtra("gallery_licence"))
            val credit=GalleryCredits.credit(source,"Example artwork",provider,page)
            assertTrue(credit.contains(page));assertTrue(credit.contains(provider.terms));assertFalse(credit.contains("CC BY-SA"))
            if(provider==IllustrationSource.IRASUTOYA) assertTrue(credit.contains("Takashi Mifune")) else assertTrue(credit.contains("CC0"))
            File(gallery.cacheDir,result.getStringExtra("gallery_file")!!).delete()
        }
    }
    @Test fun illustrationProvidersRejectOtherSourcesHostSpoofingAndNonArtworkFiles() {
        assertTrue(IllustrationSource.IRASUTOYA.allowsImage(Uri.parse("https://1.bp.blogspot.com/art/s800/image.png")))
        assertFalse(IllustrationSource.IRASUTOYA.allowsImage(Uri.parse("https://blogger.googleusercontent.com.evil.example/image.png")))
        assertFalse(IllustrationSource.IRASUTOYA.allowsImage(Uri.parse("http://blogger.googleusercontent.com/image.png")))
        assertFalse(IllustrationSource.OPENCLIPART.allowsImage(Uri.parse("https://openclipart.org/download/250963/art.svg")))
        assertFalse(IllustrationSource.OPENCLIPART.allowsImage(Uri.parse("https://catrobat.org/image.png")))
        assertFalse(IllustrationSource.IRASUTOYA.isArtworkPage(Uri.parse("https://www.irasutoya.com/p/terms.html")))
        assertFalse(IllustrationSource.OPENCLIPART.isArtworkPage(Uri.parse("https://openclipart.org/search/?query=cat")))
    }

    @Test fun editedCreatorAndModificationCreditPersistsAndCopiesForDistribution() {
        var entries=listOf(ImageCredit(asset.toString(),GalleryCredits.credit(asset.toString())))
        val edit: (String,String)->Unit={source,text -> entries=entries.map {if(it.source==source) it.copy(text=text) else it}}
        GalleryCredits.showEditor(gallery,entries,edit);shadowOf(Looper.getMainLooper()).idle()
        val dialog=ShadowDialog.getLatestDialog()
        val field=dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text")
        val credit=GalleryCredits.credit(asset.toString())+"\nCreator: credited artist\nChanges: cropped and recoloured."
        field.setText(credit)
        dialog.window!!.decorView.findViewWithTag<Button>("gallery_credit_copy").performClick()
        val clipboard=gallery.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        assertEquals(credit,clipboard.primaryClip!!.getItemAt(0).text.toString())
        assertEquals(credit,ImageCredit.text(entries))
        dialog.dismiss();GalleryCredits.showEditor(gallery,entries,edit);shadowOf(Looper.getMainLooper()).idle()
        val reopened=ShadowDialog.getLatestDialog()
        assertEquals(credit,reopened.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
        reopened.dismiss()
    }

    @Test fun galleryRecreationReturnsSavedCreditEditsWithoutTurningUneditedBrowsingIntoAnInsertion() {
        val original=ImageCredit(asset.toString(),"Original creator credit")
        val revised="Corrected creator and modifications"
        val intent=android.content.Intent(RuntimeEnvironment.getApplication(),MediaGalleryActivity::class.java)
            .putExtra("document_image_credits",ImageCredit.write(listOf(original)).toString())
        for(edited in listOf(false,true)) {
            controller.pause().stop().destroy()
            controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,intent)
            gallery=controller.setup().get()
            if(edited) {
                gallery.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
                shadowOf(Looper.getMainLooper()).idle()
                val dialog=ShadowAlertDialog.getLatestAlertDialog()
                dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText(revised)
                dialog.window!!.decorView.findViewWithTag<Button>("gallery_credit_done").performClick()
            }
            val saved=Bundle()
            controller.saveInstanceState(saved).pause().stop().destroy()
            controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,intent)
            gallery=controller.create(saved).start().resume().visible().get()
            gallery.window.decorView.findViewWithTag<Button>("gallery_done").performClick()
            assertEquals(if(edited) Activity.RESULT_OK else Activity.RESULT_CANCELED,shadowOf(gallery).resultCode)
            if(edited) {
                val result=shadowOf(gallery).resultIntent
                assertFalse(result.hasExtra("gallery_file"))
                assertEquals(listOf(original.copy(text=revised)),ImageCredit.read(org.json.JSONArray(result.getStringExtra("document_image_credits"))))
            }
        }
    }
}
