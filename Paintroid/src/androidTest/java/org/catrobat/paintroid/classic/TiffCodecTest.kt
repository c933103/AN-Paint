/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Rect
import android.util.Base64
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.io.IOException
import java.nio.ByteBuffer
import java.nio.ByteOrder
import kotlin.math.abs

/** Runs the packaged TIFF codec against fixtures written independently of it. */
@RunWith(AndroidJUnit4::class)
class TiffCodecTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext
    private val assets get() = InstrumentationRegistry.getInstrumentation().context.assets
    private val budget = 256L * 1024 * 1024
    private val manifest by lazy {
        JSONObject(assets.open("tiff-fixtures/expected.json").bufferedReader().use { it.readText() })
            .getJSONObject("fixtures")
    }

    private fun source() = Bitmap.createBitmap(37, 29, Bitmap.Config.ARGB_8888).apply {
        for (y in 0 until height) for (x in 0 until width) {
            setPixel(x, y, Color.rgb((x * 17 + y * 3) % 256, (x * 5 + y * 29) % 256, (x * 11 + y * 7) % 256))
        }
        setHasAlpha(false)
    }

    private fun withFixture(name: String, check: (File) -> Unit) {
        // A provider may report an unrelated filename; detection must inspect bytes.
        val file = File.createTempFile("tiff-fixture-", ".bin", context.cacheDir)
        try {
            val encoded = assets.open("tiff-fixtures/$name.tif.b64").bufferedReader().use { it.readText() }
            file.writeBytes(Base64.decode(encoded, Base64.DEFAULT))
            check(file)
        } finally { file.delete() }
    }

    private fun expectedSize(name: String) = manifest.getJSONObject(name).let {
        ImageDimensions(it.getInt("width"), it.getInt("height"))
    }

    private fun assertFixture(name: String, output: Bitmap, crop: Rect? = null) {
        val expected = manifest.getJSONObject(name)
        val width = expected.getInt("width")
        val region = crop ?: Rect(0, 0, width, expected.getInt("height"))
        val pixels = expected.getJSONArray("rgba")
        val tolerance = expected.getInt("tolerance")
        for (y in 0 until output.height) for (x in 0 until output.width) {
            val sx = region.left + x * region.width() / output.width
            val sy = region.top + y * region.height() / output.height
            val pixel = pixels.getJSONArray(sy * width + sx)
            val actual = output.getPixel(x, y)
            val channels = intArrayOf(Color.red(actual), Color.green(actual), Color.blue(actual), Color.alpha(actual))
            for (channel in channels.indices) {
                val allowed = if (channel == 3) 0 else tolerance
                assertTrue("$name pixel $x,$y channel $channel: expected ${pixel.getInt(channel)}, got ${channels[channel]}",
                    abs(channels[channel] - pixel.getInt(channel)) <= allowed)
            }
        }
    }

    private fun checkFixtures(names: List<String>) {
        for (name in names) withFixture(name) { file ->
            assertTrue("TIFF signature: $name", TiffCodec.isTiff(file))
            val size = expectedSize(name)
            assertEquals("Dimensions: $name", size, TiffCodec.dimensions(file))
            val decoded = TiffCodec.decode(file, size, budget)
            try {
                assertEquals(size.width, decoded.width); assertEquals(size.height, decoded.height)
                assertFixture(name, decoded)
            } finally { decoded.recycle() }
        }
    }

    @Test fun uncompressedAndDeflateExportsPreserveAllOpaquePixels() {
        val input = source()
        try {
            for (compressed in listOf(false, true)) {
                val file = File.createTempFile("tiff-roundtrip-", ".bin", context.cacheDir)
                try {
                    TiffCodec.encode(input, file, compressed, budget)
                    assertTrue(TiffCodec.isTiff(file))
                    assertEquals(ImageDimensions(37, 29), TiffCodec.dimensions(file))
                    // The encoded Compression tag must match the chosen Save as setting.
                    assertEquals(if (compressed) 8 else 1, compressionTag(file))
                    val output = TiffCodec.decode(file, ImageDimensions(37, 29), budget)
                    try {
                        for (y in 0 until input.height) for (x in 0 until input.width)
                            assertEquals("compressed=$compressed $x,$y", input.getPixel(x,y), output.getPixel(x,y))
                    } finally { output.recycle() }
                } finally { file.delete() }
            }
        } finally { input.recycle() }
    }

    @Test fun independentlyEncodedEndianBigTiffStripsTilesAndPlanarSamplesImportExactly() {
        checkFixtures(listOf("strips-le", "strips-be", "bigtiff-le", "bigtiff-be", "planar-separate",
            "deflate-strips", "tiles-deflate", "tiles-planar-deflate"))
    }

    @Test fun independentLzwPredictorPackBitsAndCcittFixturesImportExactly() {
        checkFixtures(listOf("lzw", "lzw-predictor", "packbits", "ccitt-group3", "ccitt-group4"))
    }

    @Test fun jpegCompressedTiffMatchesIndependentHostDecoder() {
        checkFixtures(listOf("jpeg"))
    }

    @Test fun packedGrayscalePalettesAndSixteenBitSamplesHaveCorrectSampleInterpretation() {
        checkFixtures((listOf(1, 2, 4, 8).flatMap { listOf("gray$it-black", "gray$it-white") }) +
            listOf("palette4", "palette8", "gray16", "rgb16-be", "rgb16-planar"))
    }

    @Test fun linearRgbAndGrayIccProfilesConvertSixteenBitSamplesBeforeQuantization() {
        checkFixtures(listOf("linear-rgb16-icc", "linear-gray16-icc"))
    }

    @Test fun associatedAndUnassociatedAlphaRemainCorrectAfterPremultiplication() {
        checkFixtures(listOf("alpha-associated", "alpha-unassociated", "alpha16-unassociated"))
    }

    @Test fun allEightOrientationsApplyToPixelsDimensionsCropsAndResizing() {
        for (orientation in 1..8) {
            val name = "orientation-$orientation"
            checkFixtures(listOf(name))
            withFixture(name) { file ->
                val size = expectedSize(name)
                val crop = Rect(2, 3, size.width - 2, size.height - 3)
                for (target in listOf(ImageDimensions(crop.width(), crop.height()), ImageDimensions(5,4), ImageDimensions(30,28))) {
                    val output = TiffCodec.decode(file, target, budget, crop)
                    try {
                        assertEquals(target.width, output.width); assertEquals(target.height, output.height)
                        assertFixture(name, output, crop)
                    } finally { output.recycle() }
                }
            }
        }
    }

    @Test fun croppedTiledImagesIncludePartialEdgeTilesAndScaleFromOriginalPixels() {
        for (name in listOf("tiles-deflate", "tiles-planar-deflate")) withFixture(name) { file ->
            val crop = Rect(13, 12, 35, 19)
            for (target in listOf(ImageDimensions(22,7), ImageDimensions(11,3))) {
                val output = TiffCodec.decode(file, target, budget, crop)
                try { assertFixture(name, output, crop) } finally { output.recycle() }
            }
        }
    }

    @Test fun sharedImportRecognizesTiffBySignatureAndUsesFirstPage() {
        for (name in listOf("strips-le", "bigtiff-be", "multipage", "orientation-6")) withFixture(name) { file ->
            val imported = ImportedImage(file, "provider.bin")
            val size = expectedSize(name)
            assertEquals(size, imported.dimensions)
            val output = imported.decode(ImportPlan.create(size,size), budget)
            try { assertFixture(name, output) } finally { output.recycle() }
        }
    }

    @Test fun selectedTiffPagesHaveIndependentDimensionsOrientationAndCropPixels() {
        withFixture("multipage") { file ->
            assertEquals(2,TiffCodec.pageCount(file))
            assertEquals(ImageDimensions(7,3),TiffCodec.dimensions(file,pageIndex=1))
            val page=TiffCodec.decode(file,ImageDimensions(7,3),budget,pageIndex=1)
            try { for(y in 0 until 3) for(x in 0 until 7) assertEquals(Color.RED,page.getPixel(x,y)) }
            finally { page.recycle() }
        }
        for(name in listOf("multipage-classic-be","multipage-bigtiff-le","multipage-bigtiff-be")) withFixture(name) { file ->
            assertEquals(3,TiffCodec.pageCount(file))
            assertEquals(ImageDimensions(19,13),TiffCodec.dimensions(file))
            assertEquals(ImageDimensions(3,7),TiffCodec.dimensions(file,pageIndex=1))
            assertEquals(ImageDimensions(2,2),TiffCodec.dimensions(file,pageIndex=2))
            assertTrue(TiffCodec.decodeWorkingBytes(file,ImageDimensions(3,7),pageIndex=1)>3L*7*4)
            for(region in listOf(Rect(0,0,3,7),Rect(1,1,3,6))) {
                val size=if(region.left==0) ImageDimensions(3,7) else ImageDimensions(4,5)
                val page=TiffCodec.decode(file,size,budget,crop=region,pageIndex=1)
                try {
                    for(y in 0 until size.height) for(x in 0 until size.width) {
                        val displayedX=region.left+x*region.width()/size.width
                        val displayedY=region.top+y*region.height()/size.height
                        val sx=displayedY; val sy=2-displayedX
                        assertEquals("$name second page $x,$y",
                            Color.rgb((sx*17+sy*3)%256,(sx*5+sy*29)%256,(sx*11+sy*7)%256),page.getPixel(x,y))
                    }
                } finally { page.recycle() }
            }
            val last=TiffCodec.decode(file,ImageDimensions(2,2),budget,pageIndex=2)
            try { for(y in 0..1) for(x in 0..1) assertEquals(Color.GREEN,last.getPixel(x,y)) }
            finally { last.recycle() }
        }
    }

    @Test fun nonexistentAndNegativeTiffPageIndexesFailWithoutChangingTheFile() {
        withFixture("multipage") { file ->
            val original=file.readBytes()
            for(index in listOf(-1,2,4096)) {
                try { TiffCodec.dimensions(file,index); fail("Accepted page $index") }
                catch(_:IOException) { }
                try { TiffCodec.decode(file,ImageDimensions(1,1),budget,pageIndex=index).recycle(); fail("Decoded page $index") }
                catch(_:IOException) { }
            }
            assertArrayEquals(original,file.readBytes())
        }
    }

    @Test fun invalidOrExcessiveTiffPageChainsRejectBeforeShowingAPageCount() {
        for(name in listOf("invalid-page-cycle","invalid-page-chain","too-many-pages")) withFixture(name) { file ->
            try { TiffCodec.pageCount(file); fail("Counted $name as a usable document") }
            catch(error:IOException) { assertNotNull(error.message) }
            try { TiffCodec.dimensions(file); fail("Accepted first page of $name") }
            catch(_:IOException) { }
        }
    }

    @Test fun unsupportedAndDamagedFilesRejectWithoutAcceptingPartialPixels() {
        for (name in listOf("invalid-magic", "invalid-offset", "truncated", "unsupported-cmyk", "unsupported-lab", "unsupported-float",
            "unsupported-transfer-function", "invalid-icc", "mismatched-gray-icc")) {
            withFixture(name) { file ->
                val before = file.readBytes()
                try {
                    val size = TiffCodec.dimensions(file)
                    val output = TiffCodec.decode(file, size, budget)
                    output.recycle()
                    fail("Accepted $name")
                } catch (expected: IOException) {
                    assertNotNull(expected.message)
                }
                assertArrayEquals("Decoder changed $name", before, file.readBytes())
            }
        }
    }

    @Test fun constrainedDecodePreservesSourceAndCanRecoverWithSufficientBudget() {
        withFixture("tiles-deflate") { file ->
            val size = expectedSize("tiles-deflate")
            val before = file.readBytes()
            assertTrue(TiffCodec.decodeWorkingBytes(file,size) > size.width.toLong()*size.height*4)
            try {
                val output = TiffCodec.decode(file,size,1)
                output.recycle(); fail("Ignored decode budget")
            } catch (_: OutOfMemoryError) { }
            assertArrayEquals(before, file.readBytes())
            val output = TiffCodec.decode(file,size,budget)
            try { assertFixture("tiles-deflate",output) } finally { output.recycle() }
        }
    }

    @Test fun constrainedEncodePreservesDestinationAndSourceAndCanRecover() {
        val input = source()
        val before = IntArray(input.width*input.height)
        input.getPixels(before,0,input.width,0,0,input.width,input.height)
        try {
            for (compressed in listOf(false,true)) {
                val file = File.createTempFile("tiff-existing-", ".tif", context.cacheDir)
                try {
                    file.writeText("previous destination")
                    try { TiffCodec.encode(input,file,compressed,1); fail("Ignored encode budget") }
                    catch (_: OutOfMemoryError) { }
                    assertEquals("previous destination",file.readText())
                    assertFalse(input.isRecycled)
                    val after = IntArray(before.size)
                    input.getPixels(after,0,input.width,0,0,input.width,input.height)
                    assertArrayEquals(before,after)
                    TiffCodec.encode(input,file,compressed,budget)
                    assertEquals(ImageDimensions(input.width,input.height),TiffCodec.dimensions(file))
                } finally { file.delete() }
            }
        } finally { input.recycle() }
    }

    @Test fun transparentEncodeRejectsBeforeOverwritingDestination() {
        val input = Bitmap.createBitmap(4,3,Bitmap.Config.ARGB_8888).apply { eraseColor(Color.TRANSPARENT) }
        val file = File.createTempFile("tiff-transparent-", ".tif", context.cacheDir)
        try {
            file.writeText("previous destination")
            try { TiffCodec.encode(input,file,true,budget); fail("Transparent TIFF export must use the exporter's background compositing") }
            catch (_: IOException) { }
            assertEquals("previous destination",file.readText())
            assertFalse(input.isRecycled); assertEquals(Color.TRANSPARENT,input.getPixel(0,0))
        } finally { input.recycle(); file.delete() }
    }

    private fun compressionTag(file: File): Int {
        val bytes = file.readBytes()
        val buffer = ByteBuffer.wrap(bytes).order(if (bytes[0] == 'I'.code.toByte()) ByteOrder.LITTLE_ENDIAN else ByteOrder.BIG_ENDIAN)
        assertEquals("Export should use classic TIFF",42,buffer.getShort(2).toInt() and 65535)
        val ifd = buffer.getInt(4)
        val count = buffer.getShort(ifd).toInt() and 65535
        for (i in 0 until count) {
            val entry = ifd+2+i*12
            if ((buffer.getShort(entry).toInt() and 65535) == 259) return buffer.getShort(entry+8).toInt() and 65535
        }
        fail("No TIFF Compression tag")
        return -1
    }
}
