/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Color
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.ByteArrayOutputStream
import java.io.DataOutputStream
import java.io.File
import java.io.IOException
import java.util.zip.CRC32

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class IcoCodecTest {
    private val context get() = RuntimeEnvironment.getApplication()
    private val budget = 256L * 1024 * 1024
    private fun directory() = File.createTempFile("ico-test-", "", context.cacheDir).apply { delete(); mkdirs() }

    @Test fun allExportSizesKeepTheAspectRatioWithTransparentPaddingAndOpenThroughSharedImport() {
        val image = Bitmap.createBitmap(32, 16, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.RED); setHasAlpha(false) }
        val folder = directory()
        try { for (edge in IcoCodec.exportEdges) {
            val file = File(folder, "icon.bin")
            IcoCodec.encode(image, file, edge, budget)
            assertTrue(IcoCodec.isIco(file))
            val imported = ImportedImage(file, "provider.bin")
            assertEquals(ImageDimensions(edge, edge), imported.dimensions)
            val decoded = imported.decode(ImportPlan.create(imported.dimensions, imported.dimensions), budget)
            try {
                assertEquals(0, Color.alpha(decoded.getPixel(edge / 2, 0)))
                assertEquals(0, Color.alpha(decoded.getPixel(edge / 2, edge - 1)))
                assertEquals(Color.RED, decoded.getPixel(edge / 2, edge / 2))
                assertEquals(Color.RED, decoded.getPixel(0, edge / 2))
                assertTrue(decoded.hasAlpha())
            } finally { decoded.recycle() }
            assertEquals(listOf("icon.bin"), folder.listFiles()!!.map { it.name })
        }
            assertFalse(image.isRecycled)
            assertEquals(Color.RED, image.getPixel(0, 0))
        } finally { image.recycle(); folder.deleteRecursively() }
    }

    @Test fun squareIconsRetainEveryPixelAndDibAlphaPassesThroughAndroidBitmapStorage() {
        val image = Bitmap.createBitmap(16, 16, Bitmap.Config.ARGB_8888).apply {
            for (y in 0 until 16) for (x in 0 until 16) setPixel(x, y, Color.rgb(x * 17, y * 17, (x + y) * 8))
            setHasAlpha(false)
        }
        val folder = directory()
        try {
            val file = File(folder, "square.ico")
            IcoCodec.encode(image, file, 16, budget)
            val decoded = IcoCodec.decode(file, ImageDimensions(16, 16), budget)
            try { for (y in 0 until 16) for (x in 0 until 16) assertEquals(image.getPixel(x, y), decoded.getPixel(x, y)) }
            finally { decoded.recycle() }
            // A 2 x 1, 32-bit icon: meaningful alpha takes precedence over the compatibility mask.
            val dib = ByteArray(52)
            fun put(offset: Int, n: Int, bytes: Int = 4) { repeat(bytes) { dib[offset + it] = (n ushr (8 * it)).toByte() } }
            put(0, 40); put(4, 2); put(8, 2); put(12, 1, 2); put(14, 32, 2)
            dib[42] = 255.toByte(); dib[43] = 128.toByte(); dib[45] = 255.toByte(); dib[47] = 255.toByte(); dib[48] = 255.toByte()
            file.writeBytes(byteArrayOf(0, 0, 1, 0, 1, 0, 2, 1, 0, 0, 1, 0, 32, 0, 52, 0, 0, 0, 22, 0, 0, 0) + dib)
            val alpha = IcoCodec.decode(file, ImageDimensions(2, 1), budget)
            try {
                assertEquals(128, Color.alpha(alpha.getPixel(0, 0)))
                assertEquals(255, Color.red(alpha.getPixel(0, 0)))
                assertEquals(Color.GREEN, alpha.getPixel(1, 0))
            } finally { alpha.recycle() }
        } finally { image.recycle(); folder.deleteRecursively() }
    }

    @Test fun rejectedBudgetsAndSizesPreserveDestinationAndSourceWithoutLeakingTemporaryFiles() {
        val folder = directory()
        val image = Bitmap.createBitmap(16, 16, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.BLUE) }
        try {
            val file = File(folder, "old.ico").apply { writeText("old data") }
            for ((edge, memory) in listOf(16 to 1000L, 257 to budget, 17 to budget)) {
                try { IcoCodec.encode(image, file, edge, memory); fail("Expected export rejection") }
                catch (expected: IOException) { assertNotNull(expected.message) }
                assertEquals("old data", file.readText())
                assertEquals(1, folder.listFiles()!!.size)
            }
            IcoCodec.encode(image, file, 16, budget)
            try { IcoCodec.decode(file, ImageDimensions(16, 16), 1000); fail("Expected decode rejection") }
            catch (expected: IOException) { assertNotNull(expected.message) }
            assertEquals(1, folder.listFiles()!!.size)
            assertFalse(image.isRecycled)
            assertEquals(Color.BLUE, image.getPixel(0, 0))
        } finally { image.recycle(); folder.deleteRecursively() }
    }

    @Test fun failedPngDecoderRemovesTheExtractedPrivatePayload() {
        fun chunk(type: String, data: ByteArray): ByteArray = ByteArrayOutputStream().also { bytes ->
            DataOutputStream(bytes).use { out ->
                out.writeInt(data.size); out.writeBytes(type); out.write(data)
                val crc = CRC32().apply { update(type.toByteArray(Charsets.US_ASCII)); update(data) }
                out.writeInt(crc.value.toInt())
            }
        }.toByteArray()
        val ihdr = byteArrayOf(0, 0, 0, 1, 0, 0, 0, 1, 8, 6, 0, 0, 0)
        val png = byteArrayOf(137.toByte(), 80, 78, 71, 13, 10, 26, 10) + chunk("IHDR", ihdr) +
            chunk("IDAT", byteArrayOf(1, 2, 3, 4)) + chunk("IEND", byteArrayOf())
        val folder = directory()
        try {
            val file = File(folder, "broken.ico")
            val header = byteArrayOf(0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 32, 0, 0, 0, 0, 0, 22, 0, 0, 0)
            repeat(4) { header[14 + it] = (png.size ushr (8 * it)).toByte() }
            file.writeBytes(header + png)
            try { IcoCodec.decode(file, ImageDimensions(1, 1), budget); fail("Expected malformed PNG rejection") }
            catch (expected: IOException) { assertNotNull(expected.message) }
            assertEquals(listOf("broken.ico"), folder.listFiles()!!.map { it.name })
        } finally { folder.deleteRecursively() }
    }
}
