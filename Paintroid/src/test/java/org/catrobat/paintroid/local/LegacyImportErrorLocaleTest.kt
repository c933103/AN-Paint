/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.res.Configuration
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.IOException
import java.util.Locale
import java.util.concurrent.CancellationException

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class LegacyImportErrorLocaleTest {
    private val context get() = RuntimeEnvironment.getApplication()
    private fun folder() = File.createTempFile("import-error-", "", context.cacheDir).apply { delete(); mkdirs() }
    private val emptyIco = byteArrayOf(0, 0, 1, 0, 0, 0)
    private val truncatedDib = byteArrayOf(40, 0, 0, 0)

    private fun rejected(block: () -> Unit): IOException {
        try { block() } catch (error: IOException) { return error }
        throw AssertionError("Expected image rejection")
    }

    @Test fun malformedImagesUseSelectedResourcesAcrossEveryPickerLanguage() {
        val previous = PaintApplication.currentResources
        val directory = folder()
        val ico = File(directory, "empty.ico").apply { writeBytes(emptyIco) }
        val dib = File(directory, "truncated.dib").apply { writeBytes(truncatedDib) }
        try {
            for (tag in context.resources.getStringArray(R.array.app_language_tags)) {
                val config = Configuration(previous.configuration).apply {
                    setLocale(AppLanguage.resourceLocale(Locale.forLanguageTag(tag)))
                }
                PaintApplication.currentResources = context.createConfigurationContext(config).resources
                val expected = ui(R.string.ui_no_readable_image_data)
                // Both ImportSelection consumers (editor and assembly) construct ImportedImage.
                for ((file, cause) in listOf(ico to IcoContainer.InvalidImage::class.java,
                                             dib to PackedDib.InvalidImage::class.java)) {
                    val error = rejected { ImportedImage(file, file.name) }
                    assertEquals(tag, expected, error.message)
                    assertTrue(tag, cause.isInstance(error.cause))
                    assertNotEquals(tag, error.cause!!.message, error.message)
                }
                assertEquals(tag, listOf("empty.ico", "truncated.dib"), directory.list()!!.sorted())
            }
        } finally {
            PaintApplication.currentResources = previous
            directory.deleteRecursively()
        }
    }

    @Test fun parsersRetainTypedTechnicalDiagnosticsWithoutAndroidStrings() {
        val directory = folder()
        try {
            val ico = File(directory, "empty.ico").apply { writeBytes(emptyIco) }
            val dib = File(directory, "truncated.dib").apply { writeBytes(truncatedDib) }
            val icoError = rejected { IcoContainer.best(ico) }
            assertTrue(icoError is IcoContainer.InvalidImage)
            assertEquals("Invalid or unsupported ICO: invalid directory count.", icoError.message)
            val dibError = rejected { PackedDib.toBmp(dib, ByteArrayOutputStream()) }
            assertTrue(dibError is PackedDib.InvalidImage)
            assertEquals("Invalid DIB: truncated header.", dibError.message)
            dib.writeBytes(byteArrayOf(40))
            assertTrue(rejected { PackedDib.toBmp(dib, ByteArrayOutputStream()) } is PackedDib.InvalidImage)
        } finally { directory.deleteRecursively() }
    }

    @Test fun unsupportedDibFeaturesUseTheSameBoundaryAndCleanTheWrapper() {
        val directory = folder()
        try {
            val bytes = ByteArray(40).apply { this[0] = 40; this[4] = 1; this[8] = 1; this[12] = 1; this[14] = 2 }
            val file = File(directory, "unsupported.dib").apply { writeBytes(bytes) }
            val error = rejected { DibCodec.withBmpFile(file) { fail("Unsupported pixels reached consumer") } }
            assertEquals(ui(R.string.ui_no_readable_image_data), error.message)
            assertTrue(error.cause is PackedDib.InvalidImage)
            assertTrue(error.cause!!.message!!.startsWith("Unsupported DIB pixel depth"))
            assertEquals(listOf("unsupported.dib"), directory.list()!!.toList())
        } finally { directory.deleteRecursively() }
    }

    @Test fun consumerStorageCancellationAndProgrammingErrorsAreNotRelabelled() {
        val directory = folder()
        try {
            val bytes = ByteArray(44).apply { this[0] = 40; this[4] = 1; this[8] = 1; this[12] = 1; this[14] = 24 }
            val file = File(directory, "valid.dib").apply { writeBytes(bytes) }
            for (sentinel in listOf(IOException("storage failure"), CancellationException("cancelled"),
                                    IllegalStateException("programming failure"), OutOfMemoryError("memory failure"))) {
                var caught: Throwable? = null
                try { DibCodec.withBmpFile(file) { throw sentinel } } catch (error: Throwable) { caught = error }
                assertSame(sentinel, caught)
                assertEquals(listOf("valid.dib"), directory.list()!!.toList())
            }
            val missing = File(directory, "missing.ico")
            val error = rejected { IcoCodec.dimensions(missing) }
            assertTrue(error is java.io.FileNotFoundException)
            assertNull(error.cause)
        } finally { directory.deleteRecursively() }
    }
}
