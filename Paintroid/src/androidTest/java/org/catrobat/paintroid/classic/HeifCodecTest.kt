/* AN Paint, 2026. AGPL-3.0-or-later. Native codecs run on Android. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.Rect
import android.os.Build
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.io.IOException
import kotlin.math.abs

@RunWith(AndroidJUnit4::class)
class HeifCodecTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext
    private val budget = 256L * 1024 * 1024
    private fun file(format: String) = File.createTempFile("native-heif-", ".$format", context.cacheDir)
    private fun pattern(width: Int, height: Int) = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888).apply {
        for (y in 0 until height) for (x in 0 until width) setPixel(x, y, Color.rgb((x * 19 + y) % 256, (x + y * 17) % 256, (x * 3 + y * 11) % 256))
        setHasAlpha(false)
    }
    private fun gradient(width: Int, height: Int) = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888).apply {
        for (y in 0 until height) for (x in 0 until width) setPixel(x, y, Color.rgb(x * 255 / maxOf(1, width - 1), y * 255 / maxOf(1, height - 1), 128))
        setHasAlpha(false)
    }
    private fun assertPixels(expected: Bitmap, actual: Bitmap) {
        assertEquals(expected.width, actual.width); assertEquals(expected.height, actual.height)
        val a = IntArray(expected.width); val b = IntArray(actual.width)
        for (y in 0 until expected.height) {
            expected.getPixels(a, 0, a.size, 0, y, a.size, 1)
            actual.getPixels(b, 0, b.size, 0, y, b.size, 1)
            assertArrayEquals("Row $y", a, b)
        }
    }
    @Test fun avifLosslessPreservesEveryRgbPixelIncludingOddDimensions() {
        val input = pattern(67, 49); val target = file("avif")
        try {
            HeifCodec.encode(input, target, "avif", 100, true, budget)
            assertTrue(HeifCodec.isHeif(target)); assertEquals(ImageDimensions(67, 49), HeifCodec.dimensions(target))
            val output = HeifCodec.decode(target, ImageDimensions(67, 49), budget)
            try { assertPixels(input, output) } finally { output.recycle() }
        } finally { input.recycle(); target.delete() }
    }
    @Test fun avifTiledRoundTripAndCrossTileCropKeepExactPixels() {
        for (size in listOf(ImageDimensions(2057, 17), ImageDimensions(17, 2057))) {
            val input = pattern(size.width, size.height); val target = file("avif")
            try {
                HeifCodec.encode(input, target, "avif", 100, true, budget)
                assertEquals(size, HeifCodec.dimensions(target))
                val output = HeifCodec.decode(target, size, budget)
                try { assertPixels(input, output) } finally { output.recycle() }
                val crop = if (size.width > size.height) Rect(1007, 2, 1045, 15) else Rect(2, 1007, 15, 1045)
                for (scale in listOf(1, 2)) {
                    val cropSize = ImageDimensions(crop.width() * scale, crop.height() * scale)
                    val cropped = HeifCodec.decode(target, cropSize, budget, crop)
                    try {
                        for (y in 0 until cropSize.height) for (x in 0 until cropSize.width)
                            assertEquals(input.getPixel(crop.left + x / scale, crop.top + y / scale), cropped.getPixel(x, y))
                    } finally { cropped.recycle() }
                }
            } finally { input.recycle(); target.delete() }
        }
    }
    @Test fun heicAndAvifQualityControlsProduceDecodableOpaqueImages() {
        for (format in listOf("heic", "avif")) {
            val input = gradient(96, 64); val low = file(format); val high = file(format)
            try {
                HeifCodec.encode(input, low, format, 25, false, budget)
                HeifCodec.encode(input, high, format, 95, false, budget)
                assertTrue(HeifCodec.isHeif(high)); assertFalse(low.readBytes().contentEquals(high.readBytes()))
                assertEquals(ImageDimensions(96, 64), HeifCodec.dimensions(high))
                val output = HeifCodec.decode(high, ImageDimensions(24, 16), budget)
                try {
                    for (y in 0 until 16) for (x in 0 until 24) {
                        val expected = input.getPixel(x * 4, y * 4); val actual = output.getPixel(x, y)
                        assertEquals(255, Color.alpha(actual))
                        assertTrue("$format red $x,$y", abs(Color.red(expected) - Color.red(actual)) <= 20)
                        assertTrue("$format green $x,$y", abs(Color.green(expected) - Color.green(actual)) <= 20)
                    }
                } finally { output.recycle() }
                if ((format == "heic" && Build.VERSION.SDK_INT >= 28) || (format == "avif" && Build.VERSION.SDK_INT >= 34)) {
                    val platform = BitmapFactory.decodeFile(high.path)
                    assertNotNull("Android's independent decoder must accept $format output", platform)
                    try { assertEquals(96, platform.width); assertEquals(64, platform.height) } finally { platform.recycle() }
                }
            } finally { input.recycle(); low.delete(); high.delete() }
        }
    }
    @Test fun heicExportKeepsLongOddImageDimensionsAcrossTiles() {
        for (size in listOf(ImageDimensions(2057, 17), ImageDimensions(17, 2057))) {
            val input = gradient(size.width, size.height); val target = file("heic")
            try {
                HeifCodec.encode(input, target, "heic", 95, false, budget)
                assertEquals(size, HeifCodec.dimensions(target))
                val output = HeifCodec.decode(target, size, budget)
                try {
                    for (y in 0 until size.height step 4) for (x in 0 until size.width step 4) {
                        assertEquals(255, Color.alpha(output.getPixel(x, y)))
                        assertTrue(abs(Color.red(input.getPixel(x, y)) - Color.red(output.getPixel(x, y))) <= 22)
                        assertTrue(abs(Color.green(input.getPixel(x, y)) - Color.green(output.getPixel(x, y))) <= 22)
                    }
                } finally { output.recycle() }
            } finally { input.recycle(); target.delete() }
        }
    }
    @Test fun malformedFilesAndInsufficientWorkingMemoryFailBeforeEditing() {
        val input = pattern(32, 24); val target = file("avif"); val original = input.getPixel(16, 12)
        try {
            target.writeBytes(byteArrayOf(0, 0, 0, 16, 102, 116, 121, 112, 97, 118, 105, 102, 0, 0, 0, 0))
            try { HeifCodec.dimensions(target); fail("Malformed AVIF accepted") } catch (_: IOException) { }
            try { HeifCodec.encode(input, target, "avif", 95, false, 1); fail("Encoder ignored budget") } catch (_: OutOfMemoryError) { }
            HeifCodec.encode(input, target, "avif", 100, true, budget)
            try { HeifCodec.decode(target, ImageDimensions(8, 6), 1); fail("Decoder ignored source work buffers") } catch (_: OutOfMemoryError) { }
            assertEquals(original, input.getPixel(16, 12)); assertFalse(input.isRecycled)
        } finally { input.recycle(); target.delete() }
    }
}
