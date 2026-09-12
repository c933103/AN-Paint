/* AN Paint, 2026. AGPL-3.0-or-later. Native codecs run on Android. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.Canvas
import android.util.Base64
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
    @Test fun commonImporterAndAssemblyUseNativeAvifWithExactCropPixels() {
        val input = pattern(67,49); val target = file("avif")
        try {
            ImageExporter.encode(input,target,ExportOptions(ImageFormat.AVIF,100,true),budget)
            // The provider's cached filename need not carry the format suffix.
            val generic = File(context.cacheDir,"${target.nameWithoutExtension}.image")
            target.copyTo(generic,true)
            try {
                val source = ImportedImage(generic,"image from provider")
                assertEquals(ImageDimensions(67,49),source.dimensions)
                val policy = ImageMemoryPolicy.forDevice(context)
                val plan = ImportPlan.create(source.dimensions,ImageDimensions(17,13))
                source.checkImport(policy,plan,0)
                val preview = source.decode(plan,policy.workingBytes,0)
                try {
                    for(y in 0 until preview.height) for(x in 0 until preview.width)
                        assertEquals(input.getPixel(x*67/17,y*49/13),preview.getPixel(x,y))
                } finally { preview.recycle() }
                val crop = Rect(10,8,40,32)
                val item = AssemblyImage("native-avif",generic,"image from provider",null,source.dimensions,crop)
                val renderer = AssemblyRenderer(context,listOf(item),mapOf(item.id to Rect(0,0,30,24)),0)
                val result = renderer.render(renderer.original)
                try {
                    for(y in 0 until result.height) for(x in 0 until result.width)
                        assertEquals(input.getPixel(crop.left+x,crop.top+y),result.getPixel(x,y))
                    assertFalse(result.hasAlpha())
                } finally { result.recycle() }
            } finally { generic.delete() }
        } finally { input.recycle(); target.delete() }
    }
    private fun fixture(name: String): File = file("avif").apply {
        val encoded = InstrumentationRegistry.getInstrumentation().context.assets
            .open("colour-fixtures/$name.avif.b64").bufferedReader().use { it.readText() }
        writeBytes(Base64.decode(encoded, Base64.DEFAULT))
    }
    private fun assertRgb(expected: IntArray, actual: Int, tolerance: Int = 3) {
        val rgb = intArrayOf(Color.red(actual),Color.green(actual),Color.blue(actual))
        expected.indices.forEach { assertTrue("Channel $it expected ${expected[it]}, got ${rgb[it]}", abs(expected[it]-rgb[it]) <= tolerance) }
    }
    @Test fun tenBitLinearAvifConvertsTransferBeforeEightBitQuantization() {
        val file = fixture("heif-linear10")
        try {
            val decoded = HeifCodec.decode(file,ImageDimensions(64,32),budget)
            try {
                // Linear-light 18% and 25% are about 118 and 137 in sRGB;
                // merely dropping two bits would give 46 and 64.
                assertRgb(intArrayOf(118,118,118),decoded.getPixel(20,16),2)
                assertRgb(intArrayOf(137,137,137),decoded.getPixel(28,16),2)
                assertRgb(intArrayOf(255,255,255),decoded.getPixel(60,16),1)
            } finally { decoded.recycle() }
        } finally { file.delete() }
    }
    @Test fun tenBitPqAndHlgAvifToneMapHighlightsInsteadOfTreatingHdrAsSrgb() {
        for (name in listOf("heif-pq10","heif-pq10-bitstream","heif-hlg10")) {
            val file=fixture(name)
            try {
                val decoded=HeifCodec.decode(file,ImageDimensions(64,32),budget)
                try {
                    val samples=(0..7).map { Color.red(decoded.getPixel(it*8+4,16)) }
                    assertEquals(0,samples.first()); assertEquals(255,samples.last())
                    samples.zipWithNext().forEach { (a,b) -> assertTrue("$name tonal order: $samples",b>a) }
                    if (name.startsWith("heif-pq10")) {
                        // 100 cd/m2 against a 10,000 cd/m2 source peak mapped
                        // into the 203 cd/m2 SDR target: visibly unlike raw PQ.
                        assertTrue("100-nit patch: $samples",samples[2] in 155..175)
                        assertTrue("400/1000/4000-nit highlights retain distinct levels: $samples",samples[4]<samples[5] && samples[5]<samples[6])
                    }
                    val crop=HeifCodec.decode(file,ImageDimensions(16,16),budget,Rect(16,8,32,24))
                    try { assertEquals(decoded.getPixel(20,16),crop.getPixel(4,8)) } finally { crop.recycle() }
                } finally { decoded.recycle() }
            } finally { file.delete() }
        }
    }
    @Test fun avifIccProfileAndNclxWideGamutAreConvertedToSrgb() {
        val icc=fixture("heif-p3-icc10"); val nclx=fixture("heif-p3-nclx10")
        try {
            val a=HeifCodec.decode(icc,ImageDimensions(64,32),budget)
            val b=HeifCodec.decode(nclx,ImageDimensions(64,32),budget)
            try {
                // Independent LittleCMS reference for Display-P3/gamma2.2
                // source RGB(0.5,0.25,0.75), with allowance for10-bit sampling.
                assertRgb(intArrayOf(139,57,199),a.getPixel(32,16))
                // This variant uses the sRGB transfer in its NCLX profile.
                assertTrue(Color.red(b.getPixel(32,16)) > 132)
                assertTrue(Color.blue(b.getPixel(32,16)) > 182)
                assertNotEquals(a.getPixel(32,16),b.getPixel(32,16))
            } finally { a.recycle();b.recycle() }
        } finally { icc.delete();nclx.delete() }
    }
    @Test fun translucentHighDepthAvifKeepsAlphaUntilChosenBackgroundComposition() {
        val file=fixture("heif-p3-icc-alpha10")
        try {
            val decoded=HeifCodec.decode(file,ImageDimensions(64,32),budget)
            val flattened=Bitmap.createBitmap(64,32,Bitmap.Config.ARGB_8888)
            try {
                assertEquals(0,Color.alpha(decoded.getPixel(4,16)))
                assertEquals(255,Color.alpha(decoded.getPixel(60,16)))
                assertTrue(Color.alpha(decoded.getPixel(28,16)) in 107..111)
                assertRgb(intArrayOf(139,57,199),decoded.getPixel(60,16))
                val background=Color.rgb(20,120,220)
                flattened.eraseColor(background)
                Canvas(flattened).drawBitmap(decoded,0f,0f,null)
                assertEquals(background,flattened.getPixel(4,16))
                val alpha=Color.alpha(decoded.getPixel(28,16))/255.0
                val expected=intArrayOf(139,57,199).mapIndexed { c,v ->
                    (v*alpha+intArrayOf(20,120,220)[c]*(1-alpha)).toInt()
                }.toIntArray()
                assertRgb(expected,flattened.getPixel(28,16),3)
                assertEquals(255,Color.alpha(flattened.getPixel(28,16)))
            } finally { decoded.recycle();flattened.recycle() }
        } finally { file.delete() }
    }

    @Test fun colouredHlgUsesActualPrimariesForDisplayLuminance() {
        val p3=fixture("heif-p3-hlg10")
        val equivalent=fixture("heif-srgb-hlg-equivalent10")
        try {
            val a=HeifCodec.decode(p3,ImageDimensions(64,32),budget)
            val b=HeifCodec.decode(equivalent,ImageDimensions(64,32),budget)
            try {
                // These encode the same scene colours in different primaries.
                // The independently calculated reference fixture catches using
                // BT.2020 luminance weights on P3/sRGB HLG samples.
                for (x in 4 until 64 step 8) {
                    val expected=b.getPixel(x,16)
                    assertRgb(intArrayOf(Color.red(expected),Color.green(expected),Color.blue(expected)),a.getPixel(x,16),1)
                }
            } finally { a.recycle();b.recycle() }
        } finally { p3.delete();equivalent.delete() }
    }

}
