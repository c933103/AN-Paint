/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Rect
import android.graphics.pdf.PdfDocument
import android.system.Os
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.IOException
import java.util.Locale

/** Uses real Android PDF writing/rendering, not a shadow returning invented pixels. */
@RunWith(AndroidJUnit4::class)
class PdfCodecTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext
    private val budget = 128L * 1024 * 1024

    private fun withDocument(action: (File) -> Unit) {
        val file = File.createTempFile("pdf-fixture-", ".bin", context.cacheDir)
        try {
            val document = PdfDocument()
            try {
                val landscape = document.startPage(PdfDocument.PageInfo.Builder(72, 48, 1).create())
                landscape.canvas.drawRect(0f, 0f, 18f, 24f, Paint().apply { color = Color.RED })
                landscape.canvas.drawRect(36f, 0f, 54f, 24f, Paint().apply { color = Color.argb(128, 0, 255, 0) })
                document.finishPage(landscape)
                val portrait = document.startPage(PdfDocument.PageInfo.Builder(48, 72, 2).create())
                portrait.canvas.drawRect(0f, 36f, 24f, 72f, Paint().apply { color = Color.BLUE })
                document.finishPage(portrait)
                file.outputStream().use { document.writeTo(it) }
            } finally { document.close() }
            action(file)
        } finally { file.delete() }
    }

    private fun assertOpaqueRgb(expected: Int, actual: Int, tolerance: Int = 0) {
        assertEquals(255, Color.alpha(actual))
        for (channel in listOf<(Int) -> Int>(Color::red, Color::green, Color::blue))
            assertTrue("Expected $expected, got $actual", kotlin.math.abs(channel(expected) - channel(actual)) <= tolerance)
    }

    private fun expectInvalid(action: () -> Unit) {
        try { action(); fail("Expected a readable PDF rejection") }
        catch (expected: IOException) { assertFalse(expected.message.isNullOrBlank()) }
    }

    @Test fun generatedMultipageDocumentUsesSelectedPageAnd144DpiDimensions() = withDocument { file ->
        assertTrue(PdfCodec.isPdf(file))
        assertEquals(2, PdfCodec.pageCount(file))
        assertEquals(ImageDimensions(144, 96), PdfCodec.dimensions(file))
        assertEquals(ImageDimensions(96, 144), PdfCodec.dimensions(file, 1))
        val first = PdfCodec.decode(file, PdfCodec.dimensions(file), budget)
        val second = PdfCodec.decode(file, PdfCodec.dimensions(file, 1), budget, pageIndex = 1)
        try {
            assertOpaqueRgb(Color.RED, first.getPixel(12, 12))
            assertOpaqueRgb(Color.WHITE, first.getPixel(120, 80))
            assertOpaqueRgb(Color.BLUE, second.getPixel(12, 120))
            assertOpaqueRgb(Color.WHITE, second.getPixel(12, 12))
            assertFalse(first.hasAlpha()); assertFalse(second.hasAlpha())
            assertEquals(Bitmap.DENSITY_NONE, first.density)
            assertOpaqueRgb(Color.rgb(127, 255, 127), first.getPixel(84, 12), 1)
        } finally { first.recycle(); second.recycle() }
    }

    @Test fun scalingAndSourcePixelCropRenderWithoutChangingPageOrientation() = withDocument { file ->
        val full = PdfCodec.decode(file, ImageDimensions(144, 96), budget)
        val half = PdfCodec.decode(file, ImageDimensions(72, 48), budget)
        val crop = Rect(12, 8, 120, 80)
        val cropped = PdfCodec.decode(file, ImageDimensions(108, 72), budget, crop)
        val scaledCrop = PdfCodec.decode(file, ImageDimensions(54, 36), budget, crop)
        val blueCrop = PdfCodec.decode(file, ImageDimensions(24, 36), budget, Rect(0, 72, 48, 144), 1)
        try {
            assertOpaqueRgb(Color.RED, half.getPixel(4, 4))
            assertOpaqueRgb(Color.WHITE, half.getPixel(60, 40))
            for (y in 0 until cropped.height) for (x in 0 until cropped.width)
                assertEquals("Full/crop pixel $x,$y", full.getPixel(x + crop.left, y + crop.top), cropped.getPixel(x, y))
            assertOpaqueRgb(Color.RED, scaledCrop.getPixel(2, 2))
            assertOpaqueRgb(Color.WHITE, scaledCrop.getPixel(50, 30))
            assertOpaqueRgb(Color.BLUE, blueCrop.getPixel(12, 18))
        } finally { full.recycle(); half.recycle(); cropped.recycle(); scaledCrop.recycle(); blueCrop.recycle() }
    }

    @Test fun tileRenderingUsesTheSameCoordinatesAsTheWholePage() = withDocument { file ->
        val full = PdfCodec.decode(file, ImageDimensions(144, 96), budget)
        try {
            for (region in listOf(Rect(0, 0, 72, 48), Rect(72, 0, 144, 48), Rect(0, 48, 72, 96), Rect(72, 48, 144, 96))) {
                val tile = PdfCodec.decode(file, ImageDimensions(region.width(), region.height()), budget, region)
                try { for (y in 0 until tile.height) for (x in 0 until tile.width)
                    assertEquals(full.getPixel(region.left + x, region.top + y), tile.getPixel(x, y))
                } finally { tile.recycle() }
            }
        } finally { full.recycle() }
    }

    @Test fun selectedPageOpensAsEditablePixelsWithoutChangingThePdf() = withDocument { file ->
        val original = file.readBytes()
        val imported = ImportedImage(file, "provider.bin", pageIndex = 1)
        assertEquals(ImageDimensions(96, 144), imported.dimensions)
        val plan = ImportPlan.create(imported.dimensions, imported.dimensions)
        val decoded = imported.decode(plan, budget)
        val document = PaintDocument(8, 8, File(context.cacheDir, "pdf-edit-${System.nanoTime()}"))
        try {
            document.replace(decoded) // Ownership passes to the editable document.
            assertOpaqueRgb(Color.BLUE, document.bitmap.getPixel(12, 120))
            document.checkpoint()
            document.bitmap.setPixel(12, 120, Color.MAGENTA)
            document.edited()
            assertTrue(document.dirty)
            assertOpaqueRgb(Color.MAGENTA, document.bitmap.getPixel(12, 120))
            document.undo()
            assertOpaqueRgb(Color.BLUE, document.bitmap.getPixel(12, 120))
            assertArrayEquals(original, file.readBytes())
        } finally { document.close(); if (!decoded.isRecycled) decoded.recycle() }
    }

    @Test fun assemblyCropRetainsTheSelectedPageInsteadOfFallingBackToPageOne() = withDocument { file ->
        val item = AssemblyImage("pdf-page-two", file, file.name, null, ImageDimensions(96, 144),
            Rect(0, 72, 48, 144), Attachment(null, null), pageIndex = 1)
        val output = AssemblyRenderer(context, listOf(item), mapOf(item.id to Rect(0, 0, 48, 72)), 0)
            .render(ImageDimensions(48, 72))
        try {
            assertEquals(48, output.width); assertEquals(72, output.height)
            assertOpaqueRgb(Color.BLUE, output.getPixel(12, 18))
            assertOpaqueRgb(Color.BLUE, output.getPixel(36, 54))
        } finally { output.recycle() }
    }

    @Test fun invalidPagesCropsAndInsufficientBudgetFailWithoutChangingTheInput() = withDocument { file ->
        val original = file.readBytes()
        expectInvalid { PdfCodec.dimensions(file, -1) }
        expectInvalid { PdfCodec.dimensions(file, 2) }
        expectInvalid { PdfCodec.decodeWorkingBytes(file, ImageDimensions(1, 1), 2) }
        for (crop in listOf(Rect(-1, 0, 10, 10), Rect(0, 0, 145, 96), Rect(4, 4, 4, 8)))
            expectInvalid { PdfCodec.decode(file, ImageDimensions(8, 8), budget, crop).recycle() }
        val size = ImageDimensions(144, 96)
        val required = PdfCodec.decodeWorkingBytes(file, size)
        assertTrue(required > size.pixels * 4)
        try { PdfCodec.decode(file, size, required - 1).recycle(); fail("Expected memory admission rejection") }
        catch (expected: OutOfMemoryError) { assertFalse(expected.message.isNullOrBlank()) }
        assertArrayEquals(original, file.readBytes())
        assertEquals(2, PdfCodec.pageCount(file))
    }

    @Test fun descriptorsCloseAfterRepeatedSuccessAndPageFailures() = withDocument { file ->
        fun openHandles(): Int = File("/proc/self/fd").listFiles()!!.count { descriptor ->
            try { Os.readlink(descriptor.path) == file.canonicalPath } catch (_: Exception) { false }
        }
        val before = openHandles()
        repeat(12) {
            assertEquals(2, PdfCodec.pageCount(file))
            PdfCodec.decode(file, ImageDimensions(12, 8), budget).recycle()
            expectInvalid { PdfCodec.decode(file, ImageDimensions(12, 8), budget, pageIndex = 2).recycle() }
            expectInvalid { PdfCodec.decode(file, ImageDimensions(12, 8), budget, crop = Rect(0, 0, 0, 0)).recycle() }
        }
        assertEquals(before, openHandles())
    }

    @Test fun malformedPdfIsDetectedByItsBytesAndConstructorFailureDoesNotLeakDescriptors() {
        val file = File.createTempFile("pdf-malformed-", ".bin", context.cacheDir)
        try {
            file.writeText("%PDF-1.7\nThis is deliberately not a PDF object graph.\n%%EOF\n")
            assertTrue(PdfCodec.isPdf(file))
            val before = File("/proc/self/fd").listFiles()!!.count { descriptor ->
                try { Os.readlink(descriptor.path) == file.canonicalPath } catch (_: Exception) { false }
            }
            repeat(12) { expectInvalid { PdfCodec.pageCount(file) } }
            val after = File("/proc/self/fd").listFiles()!!.count { descriptor ->
                try { Os.readlink(descriptor.path) == file.canonicalPath } catch (_: Exception) { false }
            }
            assertEquals(before, after)
            file.writeText("Not a document")
            assertFalse(PdfCodec.isPdf(file))
            expectInvalid { PdfCodec.pageCount(file) }
            file.writeBytes(byteArrayOf())
            assertFalse(PdfCodec.isPdf(file))
            expectInvalid { PdfCodec.pageCount(file) }
        } finally { file.delete() }
    }

    @Test fun pdfRotationMetadataChangesDisplayedDimensionsAndRasterDirection() {
        // Original tiny fixture, independently written without PdfDocument: the
        // stored 72x48 point page has a red lower-left square and Rotate=90.
        val file = File.createTempFile("pdf-rotated-", ".bin", context.cacheDir)
        try {
            val content = "1 0 0 rg 0 0 18 24 re f\n"
            val objects = listOf(
                "<< /Type /Catalog /Pages 2 0 R >>",
                "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
                "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 72 48] /Rotate 90 /Resources << >> /Contents 4 0 R >>",
                "<< /Length ${content.toByteArray(Charsets.US_ASCII).size} >>\nstream\n${content}endstream")
            val bytes = ByteArrayOutputStream()
            fun write(value: String) { bytes.write(value.toByteArray(Charsets.US_ASCII)) }
            write("%PDF-1.4\n")
            val offsets = objects.mapIndexed { index, body -> bytes.size().also { write("${index + 1} 0 obj\n$body\nendobj\n") } }
            val xref = bytes.size()
            write("xref\n0 5\n0000000000 65535 f \n")
            offsets.forEach { write(String.format(Locale.ROOT, "%010d 00000 n \n", it)) }
            write("trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n$xref\n%%EOF\n")
            file.writeBytes(bytes.toByteArray())
            assertEquals(ImageDimensions(96, 144), PdfCodec.dimensions(file))
            val output = PdfCodec.decode(file, ImageDimensions(96, 144), budget)
            try {
                assertOpaqueRgb(Color.RED, output.getPixel(12, 12))
                assertOpaqueRgb(Color.WHITE, output.getPixel(80, 120))
            } finally { output.recycle() }
        } finally { file.delete() }
    }
}
