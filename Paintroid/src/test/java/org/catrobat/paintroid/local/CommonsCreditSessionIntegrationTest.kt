/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Looper
import android.webkit.WebView
import android.widget.Button
import android.widget.EditText
import org.catrobat.paintroid.classic.CommonsAttribution
import org.catrobat.paintroid.classic.CreditEditContext
import org.catrobat.paintroid.classic.CreditEditSession
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.ImageCreditArchive
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
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import java.net.HttpURLConnection
import java.util.concurrent.TimeUnit

/** A failed Commons insertion must not overwrite an independently accepted credit result. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
class CommonsCreditSessionIntegrationTest {
    @Test fun failedCommonsImportRetainsAcceptedDocumentCreditAndItsSessionToken() {
        val context=RuntimeEnvironment.getApplication() as Context
        val original=ImageCredit("https://example.org/already-in-drawing.png","Original source credit")
        val revised=original.copy(text="Accepted creator correction\nChanges: cropped; 日本語; 𠀀")
        val session=CreditEditSession.create(context.filesDir,listOf(original),CreditEditContext.ledgerOnly(listOf(original)))
        val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.svg"
        val page="https://commons.wikimedia.org/wiki/File:Test_map.svg"
        val intent=Intent(context,MediaGalleryActivity::class.java)
            .putExtra("gallery_provider",IllustrationSource.COMMONS.name)
            .putExtra(CreditEditSession.EXTRA_SESSION,session.token)
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,intent)
        val gallery=controller.setup().get()
        var acceptedSnapshot: String?=null
        try {
            gallery.window.decorView.findViewWithTag<Button>("gallery_edit_credits").performClick()
            shadowOf(Looper.getMainLooper()).idle()
            val dialog=ShadowAlertDialog.getLatestAlertDialog()
            dialog.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText(revised.text)
            dialog.window!!.decorView.findViewWithTag<Button>("gallery_credit_done").performClick()
            val saved=CreditEditSession.open(context.filesDir,session.token)
            assertTrue(saved.accepted)
            assertEquals(listOf(revised),saved.credits)
            acceptedSnapshot=saved.acceptedSnapshot
            assertFalse(dialog.isShowing)

            var calls=0
            var disconnected=false
            gallery.openConnection={url ->
                calls++
                object: HttpURLConnection(url) {
                    override fun connect()=Unit
                    override fun usingProxy()=false
                    override fun disconnect() {disconnected=true}
                    override fun getResponseCode()=503
                    override fun getInputStream(): java.io.InputStream=error("An HTTP failure must not read image bytes")
                }
            }
            val web=ReflectionHelpers.getField<WebView>(gallery,"web")
            val action=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
                .appendQueryParameter("source",source).appendQueryParameter("page",page)
                .appendQueryParameter("title","Test map").build()
            assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,action.toString()))
            val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
            while(gallery.downloading && System.nanoTime()<deadline) {
                shadowOf(Looper.getMainLooper()).idle()
                Thread.sleep(5)
            }
            shadowOf(Looper.getMainLooper()).idle()
            assertFalse("Commons failure must complete",gallery.downloading)
            assertEquals(1,calls)
            assertTrue(disconnected)
            assertFalse(gallery.isFinishing)
            assertNull(CommonsAttribution.cached(context,source))

            gallery.window.decorView.findViewWithTag<Button>("gallery_done").performClick()
            assertEquals(Activity.RESULT_OK,shadowOf(gallery).resultCode)
            val result=shadowOf(gallery).resultIntent
            assertEquals(session.token,result.getStringExtra(CreditEditSession.EXTRA_SESSION))
            assertFalse(result.hasExtra("gallery_file"))
            val returned=CreditEditSession.open(context.filesDir,result.getStringExtra(CreditEditSession.EXTRA_SESSION)!!)
            assertEquals(listOf(revised),returned.credits)
            assertEquals(saved.revision,returned.revision)
            assertEquals(acceptedSnapshot,returned.acceptedSnapshot)
            assertEquals(listOf(revised),ImageCreditArchive.records(context).map {it.credit})
        } finally {
            controller.pause().stop().destroy()
            session.discard()
            acceptedSnapshot?.let {ImageCreditArchive.releaseAccepted(context,it)}
        }
    }
}
