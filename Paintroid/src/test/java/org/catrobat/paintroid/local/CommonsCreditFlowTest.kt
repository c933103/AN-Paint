/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Looper
import android.webkit.WebView
import android.widget.Button
import android.widget.EditText
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowDialog
import org.robolectric.util.ReflectionHelpers
import java.io.ByteArrayInputStream
import java.io.File
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CommonsCreditFlowTest {
    private val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.svg"
    private val page="https://commons.wikimedia.org/wiki/File:Test_map.svg"
    private val svg="""<svg xmlns="http://www.w3.org/2000/svg" width="40" height="24"><rect x="4" y="4" width="30" height="16" fill="none" stroke="black"/></svg>"""
    private val context get()=RuntimeEnvironment.getApplication() as Context
    @Before fun clear() {
        context.getSharedPreferences("image-credits",0).edit().clear().commit()
        context.getSharedPreferences("commons-attribution-v1",0).edit().clear().commit()
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        context.cacheDir.listFiles()?.filter {it.name.startsWith("gallery-")}?.forEach {it.delete()}
    }
    private class Connection(url: URL,private val input: InputStream,private val status: Int=200): HttpURLConnection(url) {
        var disconnected=false
        override fun connect()=Unit
        override fun disconnect() {disconnected=true;input.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=status
        override fun getInputStream()=input
    }
    private fun gallery()=Robolectric.buildActivity(MediaGalleryActivity::class.java,
        Intent(context,MediaGalleryActivity::class.java).putExtra("gallery_provider",IllustrationSource.COMMONS.name)).setup()
    private fun select(activity: MediaGalleryActivity,copy: Boolean=false) {
        val web=ReflectionHelpers.getField<WebView>(activity,"web")
        val action=Uri.Builder().scheme(if(copy) GalleryPage.CREDIT_SCHEME else IllustrationPage.USE_SCHEME)
            .authority(if(copy) "copy" else "insert").appendQueryParameter("source",source)
            .appendQueryParameter("page",page).appendQueryParameter("title","Test blank map").build()
        assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,action.toString()))
    }
    private fun await(done: ()->Boolean) {
        val limit=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
        while(!done() && System.nanoTime()<limit) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
        shadowOf(Looper.getMainLooper()).idle();assertTrue("Operation timed out",done())
    }
    private fun clipboard()=(context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).primaryClip!!.getItemAt(0).text.toString()
    private fun remember() {
        CommonsAttribution.cache(context,CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source))
        GalleryCredits.remember(context,source,IllustrationSource.COMMONS,page,"Test map")
    }
    @Test fun copyFromFileFetchesOnlyMetadataAndDoesNotRecordInsertion() {
        val controller=gallery();val activity=controller.get();var count=0
        try {
            activity.openConnection={url ->
                assertEquals("commons.wikimedia.org",url.host);count++
                Connection(url,ByteArrayInputStream(CommonsTestMetadata.response(source,page).toByteArray()))
            }
            select(activity,copy=true);await {!activity.downloading}
            assertEquals(1,count);assertTrue(clipboard().contains("Mapper A"));assertTrue(clipboard().contains("by-sa/3.0/"))
            assertFalse(clipboard().contains("antiAlias=false"));assertTrue(GalleryCredits.sources(context).isEmpty())
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        } finally {controller.pause().stop().destroy()}
    }
    @Test fun actualGalleryToEditorInsertionRetainsCopyableCreditsAfterReopening() {
        val controller=gallery();val activity=controller.get()
        try {
            activity.openConnection={url ->Connection(url,ByteArrayInputStream((if(url.host=="commons.wikimedia.org")
                CommonsTestMetadata.response(source,page) else svg).toByteArray()))}
            select(activity);await {activity.isFinishing && !activity.downloading}
            assertTrue(GalleryCredits.sources(context).isEmpty())
            val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
            val main=mainController.get()
            try {
                main.document.newImage(40,24)
                main.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,shadowOf(activity).resultIntent)
                await {!main.busy};assertNull(main.lastIoError);assertNotNull(main.document.selection)
                assertEquals(40,main.document.selection!!.image!!.width)
                val credit=GalleryCredits.text(main)
                for(text in listOf("Mapper A","Mapper B","by-sa/3.0/",source,page,"antiAlias=false")) assertTrue(credit.contains(text))
                main.document.finishSelection()
                val reopened=gallery()
                try {
                    reopened.get().openConnection={error("Stored credits must copy offline")}
                    reopened.get().window.decorView.findViewWithTag<Button>("gallery_copy_credits").performClick()
                    assertEquals(credit,clipboard())
                } finally {reopened.pause().stop().destroy()}
            } finally {mainController.pause().stop();await {!main.busy};mainController.destroy()}
        } finally {controller.pause().stop().destroy()}
    }
    @Test fun rotationKeepsTheSameDownloadAndOriginalDimensions() {
        val controller=gallery();val activity=controller.get()
        val started=CountDownLatch(1);val release=CountDownLatch(1);var files=0;var metadata=0
        try {
            activity.openConnection={url ->
                if(url.host=="commons.wikimedia.org") {metadata++;Connection(url,ByteArrayInputStream(CommonsTestMetadata.response(source,page).toByteArray()))}
                else {
                    files++
                    Connection(url,object: ByteArrayInputStream(svg.toByteArray()) {
                        override fun read(buffer: ByteArray,offset: Int,length: Int): Int {
                            started.countDown();check(release.await(8,TimeUnit.SECONDS));return super.read(buffer,offset,length)
                        }
                    })
                }
            }
            select(activity);assertTrue(started.await(5,TimeUnit.SECONDS))
            val landscape=Configuration(activity.resources.configuration).apply {orientation=Configuration.ORIENTATION_LANDSCAPE;screenWidthDp=900;screenHeightDp=412}
            controller.configurationChange(landscape)
            assertSame(activity,controller.get());assertFalse(activity.isDestroyed);assertTrue(activity.downloading)
            release.countDown();await {activity.isFinishing && !activity.downloading}
            assertEquals(1,files);assertEquals(1,metadata)
            val file=File(activity.cacheDir,shadowOf(activity).resultIntent.getStringExtra("gallery_file")!!)
            try {
                val bitmap=BitmapFactory.decodeFile(file.path)
                try {assertEquals(40,bitmap.width);assertEquals(24,bitmap.height)} finally {bitmap.recycle()}
            } finally {file.delete()}
        } finally {release.countDown();controller.pause().stop().destroy()}
    }
    @Test fun emptyUnconfirmedCreditDraftSurvivesRecreationWithoutOverwritingSavedText() {
        remember();val original=GalleryCredits.text(context)
        val controller=gallery()
        try {
            controller.get().window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            ShadowDialog.getLatestDialog().window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText("")
            controller.recreate()
            val dialog=ShadowDialog.getLatestDialog()
            assertTrue(dialog.isShowing)
            assertEquals("",dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
            assertEquals(original,GalleryCredits.text(context))
            dialog.cancel();controller.recreate()
            assertFalse(ShadowDialog.getLatestDialog().isShowing);assertEquals(original,GalleryCredits.text(context))
        } finally {controller.pause().stop().destroy()}
    }
    @Test fun editedCreditIsCopiedExactlyAndSurvivesBothRecreationAndReinsertion() {
        remember();val controller=gallery();val edited="Émilie · かな\nCustom attribution and changes."
        try {
            controller.get().window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            var dialog=ShadowDialog.getLatestDialog()
            dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText(edited)
            controller.recreate();dialog=ShadowDialog.getLatestDialog()
            assertEquals(edited,dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
            dialog.window!!.decorView.findViewWithTag<Button>("gallery_credit_copy").performClick()
            assertEquals(edited,clipboard());assertEquals(edited,GalleryCredits.text(context))
            GalleryCredits.remember(context,source,IllustrationSource.COMMONS,page,"Test map")
            assertEquals(edited,GalleryCredits.text(context));dialog.dismiss()
        } finally {controller.pause().stop().destroy()}
    }
    @Test fun metadataFailureCleansUpTheImageAndDoesNotAddCredits() {
        val controller=gallery();val activity=controller.get()
        try {
            activity.openConnection={url ->Connection(url,ByteArrayInputStream(svg.toByteArray()),if(url.host=="commons.wikimedia.org") 503 else 200)}
            select(activity);await {!activity.downloading}
            assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode);assertFalse(activity.isFinishing)
            assertTrue(GalleryCredits.sources(context).isEmpty())
            assertTrue(activity.cacheDir.listFiles()!!.none {it.name.startsWith("gallery-")})
        } finally {controller.pause().stop().destroy()}
    }
}
