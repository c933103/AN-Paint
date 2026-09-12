/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.io.IOException

/** Executes the packaged libwebp JNI codec, including on pre-API30 Android. */
@RunWith(AndroidJUnit4::class)
class WebpCodecTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext
    private val budget = 256L * 1024 * 1024
    private fun fixture(width: Int = 67, height: Int = 49) =
        Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888).apply {
            for (y in 0 until height) for (x in 0 until width)
                setPixel(x, y, Color.rgb((x * 4 + y) % 256, (y * 5 + x) % 256, (x * 7 + y * 11) % 256))
            setHasAlpha(false)
        }
    private fun pixelError(source: Bitmap, decoded: Bitmap): Long {
        var error = 0L
        for (y in 0 until source.height) for (x in 0 until source.width) {
            val a = source.getPixel(x, y)
            val b = decoded.getPixel(x, y)
            for (shift in intArrayOf(0, 8, 16)) {
                val delta = ((a ushr shift) and 255) - ((b ushr shift) and 255)
                error += delta * delta
            }
        }
        return error
    }
    @Test fun losslessRoundTripPreservesEveryRgbPixelOddDimensionsAndTheSource() {
        val source = fixture()
        val before = IntArray(source.width * source.height)
        source.getPixels(before, 0, source.width, 0, 0, source.width, source.height)
        val file = File.createTempFile("webp-lossless-", ".webp", context.cacheDir)
        try {
            // Even a low lossy-quality setting must remain exactly lossless.
            WebpCodec.encode(source, file, 5, true, budget)
            val header = file.inputStream().use { stream -> ByteArray(12).also { assertEquals(12, stream.read(it)) } }
            assertEquals("RIFF", String(header, 0, 4, Charsets.US_ASCII))
            assertEquals("WEBP", String(header, 8, 4, Charsets.US_ASCII))
            val decoded = BitmapFactory.decodeFile(file.path) ?: error("Cannot decode native WebP")
            try {
                assertEquals(source.width, decoded.width)
                assertEquals(source.height, decoded.height)
                for (y in 0 until source.height) for (x in 0 until source.width) {
                    assertEquals("Decoded pixel $x,$y", before[y * source.width + x], decoded.getPixel(x, y))
                    assertEquals("Source pixel $x,$y", before[y * source.width + x], source.getPixel(x, y))
                    assertEquals(255, Color.alpha(decoded.getPixel(x, y)))
                }
                assertFalse(source.isRecycled)
            } finally { decoded.recycle() }
        } finally { source.recycle(); file.delete() }
    }
    @Test fun lossyQualityChangesTheFileAndHigherQualityReducesPixelError() {
        val source = fixture(128, 96)
        val low = File.createTempFile("webp-low-", ".webp", context.cacheDir)
        val high = File.createTempFile("webp-high-", ".webp", context.cacheDir)
        try {
            WebpCodec.encode(source, low, 10, false, budget)
            WebpCodec.encode(source, high, 95, false, budget)
            assertFalse(low.readBytes().contentEquals(high.readBytes()))
            val lowImage = BitmapFactory.decodeFile(low.path) ?: error("Cannot decode low quality WebP")
            val highImage = BitmapFactory.decodeFile(high.path) ?: error("Cannot decode high quality WebP")
            try {
                assertEquals(source.width, highImage.width)
                assertEquals(source.height, highImage.height)
                assertTrue(pixelError(source, highImage) < pixelError(source, lowImage))
                assertEquals(255, Color.alpha(highImage.getPixel(17, 23)))
            } finally { lowImage.recycle(); highImage.recycle() }
        } finally { source.recycle(); low.delete(); high.delete() }
    }
    @Test fun memoryAndFormatDimensionLimitsPreserveExistingOutputAndBitmap() {
        val source = fixture()
        val wide = fixture(16384, 1)
        val file = File.createTempFile("webp-limit-", ".webp", context.cacheDir)
        val original = "existing output must survive".toByteArray()
        try {
            file.writeBytes(original)
            val pixel = source.getPixel(13, 17)
            try { WebpCodec.encode(source, file, 90, true, 1); fail("Memory budget ignored") }
            catch (_: OutOfMemoryError) { }
            assertArrayEquals(original, file.readBytes())
            try { WebpCodec.encode(wide, file, 90, false, budget); fail("WebP dimension limit ignored") }
            catch (failure: IOException) { assertTrue(failure.message.orEmpty().contains("16383")) }
            assertArrayEquals(original, file.readBytes())
            assertEquals(pixel, source.getPixel(13, 17))
            assertFalse(source.isRecycled)
            assertFalse(wide.isRecycled)
        } finally { source.recycle(); wide.recycle(); file.delete() }
    }
    @Test fun transparentInputIsRejectedWithoutChangingItsPixelsOrTheDestination() {
        val source = fixture().apply { setHasAlpha(true); setPixel(3, 5, Color.TRANSPARENT) }
        val file = File.createTempFile("webp-opacity-", ".webp", context.cacheDir)
        val original = byteArrayOf(1, 2, 3)
        try {
            file.writeBytes(original)
            try { WebpCodec.encode(source, file, 100, true, budget); fail("Transparent document accepted") }
            catch (failure: IOException) { assertTrue(failure.message.orEmpty().contains("opaque")) }
            assertArrayEquals(original, file.readBytes())
            assertEquals(Color.TRANSPARENT, source.getPixel(3, 5))
        } finally { source.recycle(); file.delete() }
    }
}
