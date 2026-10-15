/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.res.Resources
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.Implementation
import org.robolectric.annotation.Implements
import java.io.File
import java.io.IOException
import java.util.Locale

/** Real PDF admission/error routing and compiled resources; only renderer creation is injected. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [JapanesePdfFailureTest.FailingRenderer::class])
class JapanesePdfFailureTest {
    private lateinit var resourcesBefore: Resources
    private lateinit var localeBefore: Locale
    private lateinit var file: File
    private val controller = Robolectric.buildActivity(Activity::class.java)
    private lateinit var languageBefore: String

    @Before fun start() {
        val activity = controller.setup().get()
        resourcesBefore = PaintApplication.currentResources
        localeBefore = Locale.getDefault()
        languageBefore = AppLanguage.selectedTag(activity)
        AppLanguage.select(activity, "ja")
        AppLanguage.refresh(activity)
        file = File.createTempFile("pdf-error-", ".pdf", activity.cacheDir)
        FailingRenderer.failure = IOException("Synthetic reader failure, no established cause")
    }

    @After fun stop() {
        file.delete()
        AppLanguage.select(controller.get(), languageBefore)
        PaintApplication.currentResources = resourcesBefore
        Locale.setDefault(localeBefore)
        controller.pause().stop().destroy()
    }

    private fun failureMessage(action: () -> Unit): String {
        try { action(); fail("Expected PDF rejection") }
        catch (error: IOException) { return checkNotNull(error.message) }
        error("PDF was unexpectedly accepted")
    }

    @Test fun invalidSignatureUsesTheFullJapanesePossibilityMessage() {
        file.writeText("This is not a PDF")
        assertFalse(PdfCodec.isPdf(file))
        assertEquals(EXPECTED, failureMessage { PdfCodec.pageCount(file) })
        assertEquals(EXPECTED, PaintApplication.currentResources.getString(R.string.formats22_pdf_invalid))
    }

    @Test fun genericReaderFailuresDoNotStateAProvenCause() {
        file.writeText("%PDF-1.7\nfixture passes signature validation\n")
        assertTrue(PdfCodec.isPdf(file))
        for (failure in listOf(IOException("reader IO"), IllegalArgumentException("reader argument"))) {
            FailingRenderer.failure = failure
            assertEquals(EXPECTED, failureMessage { PdfCodec.pageCount(file) })
        }
    }

    @Test fun encryptionAndFileSizeErrorsKeepTheirSpecificJapaneseMessages() {
        file.writeText("%PDF-1.7\nfixture passes signature validation\n")
        FailingRenderer.failure = SecurityException("password required")
        val encrypted = PaintApplication.currentResources.getString(R.string.formats22_pdf_encrypted)
        assertNotEquals(EXPECTED, encrypted)
        assertEquals(encrypted, failureMessage { PdfCodec.pageCount(file) })
        file.writeBytes(byteArrayOf())
        val size = PaintApplication.currentResources.getString(R.string.formats22_pdf_file_size)
        assertNotEquals(EXPECTED, size)
        assertEquals(size, failureMessage { PdfCodec.pageCount(file) })
    }

    @Implements(PdfRenderer::class)
    class FailingRenderer {
        @Implementation fun __constructor__(descriptor: ParcelFileDescriptor) {
            throw failure
        }
        companion object { var failure: Exception = IOException("reader failure") }
    }

    companion object {
        private const val EXPECTED = "PDFを読み込めませんでした。ファイルが破損しているか、このAndroidバージョンでは対応していない機能が使われている可能性があります。"
    }
}
