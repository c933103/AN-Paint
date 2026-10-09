/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Looper
import android.view.View
import android.webkit.WebView
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
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
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL
import java.util.Locale
import java.util.concurrent.TimeUnit

/** Real gallery actions and the real SVG parser, with network bytes supplied by a local fixture. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CommonsSvgErrorTranslationTest {
    private val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Size_test.svg"
    private val page="https://commons.wikimedia.org/wiki/File:Size_test.svg"
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val tags=listOf("en-US","fr","ja","ar","vi-Hani","mnc-Mong")

    private class Connection(url: URL,svg: String): HttpURLConnection(url) {
        private val input=ByteArrayInputStream(svg.toByteArray(Charsets.UTF_8))
        override fun connect()=Unit
        override fun disconnect() {input.close()}
        override fun usingProxy()=false
        override fun getResponseCode()=200
        override fun getInputStream()=input
    }

    private fun await(done: ()->Boolean) {
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(12)
        while(!done() && System.nanoTime()<deadline) {
            shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)
        }
        shadowOf(Looper.getMainLooper()).idle()
        assertTrue("The actual gallery operation must finish",done())
    }

    private fun withGallery(tag: String,check: (MediaGalleryActivity)->Unit) {
        val previousTag=AppLanguage.selectedTag(context)
        val previousLocale=Locale.getDefault()
        val previousResources=PaintApplication.currentResources
        AppLanguage.select(context,tag)
        // Fresh wrappers avoid mutating another locale's resource configuration in place.
        PaintApplication.currentResources=AppLanguage.wrap(context).resources
        val controller=Robolectric.buildActivity(MediaGalleryActivity::class.java,
            Intent(context,MediaGalleryActivity::class.java)
                .putExtra("gallery_provider",IllustrationSource.COMMONS.name)).setup()
        try {check(controller.get())}
        finally {
            controller.pause().stop().destroy()
            AppLanguage.select(context,previousTag)
            PaintApplication.currentResources=previousResources
            Locale.setDefault(previousLocale)
        }
    }

    private fun select(activity: MediaGalleryActivity) {
        val web=ReflectionHelpers.getField<WebView>(activity,"web")
        val link=Uri.Builder().scheme(IllustrationPage.USE_SCHEME).authority("insert")
            .appendQueryParameter("source",source).appendQueryParameter("page",page).build()
        assertTrue(shadowOf(web).webViewClient.shouldOverrideUrlLoading(web,link.toString()))
    }

    private fun assertRejected(activity: MediaGalleryActivity,expected: String,operation: ()->Unit) {
        val token=ReflectionHelpers.getField<CreditEditSession>(activity,"creditSession").token
        val previousFiles=activity.cacheDir.listFiles().orEmpty().map {it.name}.toSet()
        operation()
        val status=activity.window.decorView.findViewWithTag<TextView>("gallery_status")
        await {!activity.downloading && status.text.toString()==expected}
        assertEquals(View.VISIBLE,status.visibility)
        assertEquals(expected,status.text.toString())
        assertFalse(activity.isFinishing)
        assertEquals(Activity.RESULT_CANCELED,shadowOf(activity).resultCode)
        assertNull(shadowOf(activity).resultIntent)
        assertFalse("Size failures must not offer a substitute-size dialog",
            ShadowAlertDialog.getLatestAlertDialog()?.isShowing==true)
        assertEquals("Failed import must not leave a temporary image",previousFiles,
            activity.cacheDir.listFiles().orEmpty().map {it.name}.toSet())
        val retained=CreditEditSession.open(activity.filesDir,token)
        assertTrue(retained.credits.isEmpty())
        assertFalse(retained.accepted)
    }

    private fun checkSizeFailure(svg: String,key: Int,english: String) {
        for(tag in tags) withGallery(tag) {activity ->
            val reason=activity.getString(key)
            if(tag in listOf("en-US","vi-Hani","mnc-Mong"))
                assertEquals("Independent source oracle, including explicit incomplete-catalogue fallback",english,reason)
            else assertNotEquals("This representative exact catalogue must resolve its translation",english,reason)
            val expected=activity.getString(R.string.ui_could_not_load_gallery_image,reason)
            var requests=0
            activity.openConnection={url ->
                assertEquals("Original-size failure must precede metadata loading",source,url.toString())
                requests++
                Connection(url,svg)
            }
            // A second explicit user attempt remains an error and must not retain stale files or credit.
            repeat(2) {assertRejected(activity,expected) {select(activity)}}
            assertEquals(2,requests)
        }
    }

    @Test fun unspecifiedOriginalSizeShowsItsLocalizedReasonThroughTheActualGallery() {
        checkSizeFailure("""<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 40 24"/>""",
            R.string.commons_svg_original_size_unavailable,
            "The SVG does not declare a usable original size. No canvas-based size was substituted.")
    }

    @Test fun overflowingOriginalSizeShowsItsLocalizedReasonWithoutResizing() {
        checkSizeFailure("""<svg xmlns="http://www.w3.org/2000/svg" width="2147483648" height="1"/>""",
            R.string.commons_svg_original_size_too_large,
            "The original SVG size exceeds Android bitmap dimensions. No resizing was applied.")
    }

    @Test fun unrelatedExternalDiagnosticsStillPassThroughUnchanged() = withGallery("fr") {activity ->
        val diagnostic="Provider diagnostic Ω: 42%"
        activity.openConnection={throw IOException(diagnostic)}
        assertRejected(activity,activity.getString(R.string.ui_could_not_load_gallery_image,diagnostic)) {
            select(activity)
        }
    }
}
