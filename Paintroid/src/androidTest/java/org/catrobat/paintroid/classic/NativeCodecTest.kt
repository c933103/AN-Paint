/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Rect
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.ColorSpace
import android.graphics.Typeface
import android.os.Build
import android.util.Base64
import androidx.core.graphics.ColorUtils
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.json.JSONArray
import java.security.MessageDigest
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.io.IOException

/** These tests run the packaged JNI library on Android, not a simulated decoder. */
@RunWith(AndroidJUnit4::class)
class NativeCodecTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext
    private val budget=256L*1024*1024
    private fun fixture() = Bitmap.createBitmap(64,48,Bitmap.Config.ARGB_8888).apply {
        for(y in 0 until height) for(x in 0 until width) setPixel(x,y,Color.rgb(x*4,y*5,(x*3+y*7)%256))
        setHasAlpha(false)
    }
    @Test fun losslessJxlRoundTripKeepsEveryOpaquePixelAndDimensions() {
        val input=fixture();val file=File.createTempFile("codec-roundtrip-",".jxl",context.cacheDir)
        try {
            JxlCodec.encode(input,file,100,true,budget)
            assertTrue(JxlCodec.isJxl(file));assertEquals(ImageDimensions(64,48),JxlCodec.dimensions(file))
            val output=JxlCodec.decode(file,ImageDimensions(64,48),budget)
            try {
                for(y in 0 until 48) for(x in 0 until 64) assertEquals("Pixel $x,$y",input.getPixel(x,y),output.getPixel(x,y))
            } finally {output.recycle()}
        } finally {input.recycle();file.delete()}
    }
    @Test fun lossyQualityAndReducedDecodeProduceUsableImages() {
        val input=fixture();val low=File.createTempFile("codec-low-",".jxl",context.cacheDir)
        val high=File.createTempFile("codec-high-",".jxl",context.cacheDir)
        try {
            JxlCodec.encode(input,low,30,false,budget);JxlCodec.encode(input,high,95,false,budget)
            assertFalse(low.readBytes().contentEquals(high.readBytes()))
            val reduced=JxlCodec.decode(high,ImageDimensions(16,12),budget)
            try {
                assertEquals(16,reduced.width);assertEquals(12,reduced.height)
                assertEquals(255,Color.alpha(reduced.getPixel(8,6)))
                assertTrue(Color.red(reduced.getPixel(12,6))>Color.red(reduced.getPixel(2,6)))
            } finally {reduced.recycle()}
        } finally {input.recycle();low.delete();high.delete()}
    }
    @Test fun corruptedInputAndInsufficientBudgetFailWithoutChangingTheSourceBitmap() {
        val input=fixture();val before=input.getPixel(31,27)
        val file=File.createTempFile("codec-invalid-",".jxl",context.cacheDir)
        try {
            file.writeBytes(byteArrayOf(-1,10,0,0,0))
            try {JxlCodec.dimensions(file);fail("Invalid JPEG XL accepted")} catch(_: IOException) { }
            try {JxlCodec.encode(input,file,95,true,1);fail("Memory budget ignored")} catch(_: OutOfMemoryError) { }
            assertEquals(before,input.getPixel(31,27));assertFalse(input.isRecycled)
        } finally {input.recycle();file.delete()}
    }
    @Test fun regionDecodePreservesChosenCropAndScalesWithoutAllocatingAFullOutput() {
        val input=fixture();val file=File.createTempFile("codec-region-",".jxl",context.cacheDir)
        try {
            JxlCodec.encode(input,file,100,true,budget)
            for(size in listOf(ImageDimensions(20,16),ImageDimensions(5,4),ImageDimensions(40,32))) {
                val output=JxlCodec.decode(file,size,budget,Rect(10,8,30,24))
                try {
                    for(y in 0 until size.height) for(x in 0 until size.width)
                        assertEquals(input.getPixel(10+x*20/size.width,8+y*16/size.height),output.getPixel(x,y))
                } finally {output.recycle()}
            }
        } finally {input.recycle();file.delete()}
    }
    @Test fun everyAdvertisedBundledFontLoadsItsActualFontFile() {
        val catalog=FontCatalog(context)
        val inventory=context.assets.open("fonts/inventory.json").bufferedReader().use {JSONArray(it.readText())}
        val rows=(0 until inventory.length()).map {inventory.getJSONObject(it)}
        val drawing=rows.filterNot {it.optBoolean("ui_only")}
        assertEquals("Each declared drawing font must be offered exactly once",
            drawing.map {it.getString("id") to it.getString("asset")}.sortedBy {it.first},
            catalog.fonts.filter {it.asset!=null}.map {it.id to it.asset!!}.sortedBy {it.first})
        val systemFamilies=setOf("sans-serif","serif","monospace","sans-serif-light","sans-serif-thin",
            "sans-serif-condensed","sans-serif-medium","cursive","casual")
        assertEquals(systemFamilies,catalog.fonts.filter {it.asset==null}.map {it.family}.toSet())
        assertEquals(systemFamilies.size,catalog.fonts.count {it.asset==null})
        assertEquals(catalog.fonts.size,catalog.fonts.map {it.id}.toSet().size)
        assertTrue(catalog.fonts.any {it.asset=="fonts/notosansmongolian.ttf"})
        catalog.fonts.forEachIndexed {index,font -> assertNotNull(font.name,catalog.face(index))}
        // UI-only subsets are still packaged font assets and must load on Android.
        for(row in rows) {
            val path=row.getString("asset")
            val bytes=context.assets.open(path).use {it.readBytes()}
            assertTrue(path,bytes.size>1000)
            val digest=MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") {"%02x".format(it.toInt() and 255)}
            assertEquals(path,row.getString("sha256"),digest)
            assertNotNull(path,Typeface.createFromAsset(context.assets,path))
        }
    }
    @Test fun losslessEncodingPreservesPixelsAcrossThe2048PixelChunkBoundary() {
        // Include the original failure, its portrait counterpart, and an image
        // spanning multiple tiles in both directions with partial edge tiles.
        for(size in listOf(ImageDimensions(2057,17),ImageDimensions(17,2057),ImageDimensions(2065,2049))) {
            val input=pattern(size);val file=File.createTempFile("codec-chunks-",".jxl",context.cacheDir)
            try {
                JxlCodec.encode(input,file,100,true,budget)
                assertEquals(size,JxlCodec.dimensions(file))
                val output=JxlCodec.decode(file,size,budget)
                try {assertPixels(input,output)} finally {output.recycle()}
                if(size.width>2048 && size.height>2048) {
                    // The crop straddles the tile boundary and includes the last row/column.
                    val crop=Rect(2037,2029,size.width,size.height)
                    val cropped=JxlCodec.decode(file,ImageDimensions(crop.width(),crop.height()),budget,crop)
                    try {
                        for(y in 0 until cropped.height) for(x in 0 until cropped.width)
                            assertEquals("Crop pixel $x,$y",input.getPixel(crop.left+x,crop.top+y),cropped.getPixel(x,y))
                    } finally {cropped.recycle()}
                }
            } finally {input.recycle();file.delete()}
        }
    }
    @Test fun lossyEncodingHandlesLongPortraitAndLandscapeImages() {
        for(size in listOf(ImageDimensions(3073,65),ImageDimensions(65,3073))) {
            val input=Bitmap.createBitmap(size.width,size.height,Bitmap.Config.ARGB_8888)
            val file=File.createTempFile("codec-lossy-chunks-",".jxl",context.cacheDir)
            try {
                val row=IntArray(size.width)
                for(y in 0 until size.height) {
                    for(x in row.indices) row[x]=Color.rgb(x*255/(size.width-1),y*255/(size.height-1),128)
                    input.setPixels(row,0,size.width,0,y,size.width,1)
                }
                input.setHasAlpha(false)
                JxlCodec.encode(input,file,90,false,budget)
                assertEquals(size,JxlCodec.dimensions(file))
                val output=JxlCodec.decode(file,size,budget)
                try {
                    assertEquals(size.width,output.width);assertEquals(size.height,output.height)
                    // JXL quality 90 targets perceptual Butteraugli distance 1,
                    // not a maximum error in each gamma-encoded sRGB channel.
                    // Independent stock libjxl reproduces (13,191,128) ->
                    // (0,192,128): red differs by 13 but CIE76 delta E is <1.
                    // Keep q90, check perceptual colour error over this gradient,
                    // and retain exact per-pixel checks in the lossless tests.
                    val expectedLab=DoubleArray(3);val actualLab=DoubleArray(3)
                    var totalError=0.0;var samples=0;var maxError=0.0;var worst=""
                    for(y in 0 until size.height step 16) for(x in 0 until size.width step 16) {
                        val expected=input.getPixel(x,y);val actual=output.getPixel(x,y)
                        assertEquals(255,Color.alpha(actual))
                        ColorUtils.colorToLAB(expected,expectedLab);ColorUtils.colorToLAB(actual,actualLab)
                        val error=ColorUtils.distanceEuclidean(expectedLab,actualLab)
                        totalError+=error;samples++
                        if(error>maxError) {maxError=error;worst="$x,$y RGB ${Integer.toHexString(expected)} -> ${Integer.toHexString(actual)}"}
                    }
                    assertTrue("${size.width} x ${size.height}: maximum CIE76 delta E $maxError at $worst",maxError<=5.0)
                    assertTrue("${size.width} x ${size.height}: mean CIE76 delta E ${totalError/samples}",totalError/samples<=1.5)
                } finally {output.recycle()}
            } finally {input.recycle();file.delete()}
        }
    }
    @Test fun nativeAllocationFailureLeavesTheBitmapUsableAndAllowsAnotherEncode() {
        val input=pattern(ImageDimensions(513,517));val file=File.createTempFile("codec-budget-",".jxl",context.cacheDir)
        try {
            val before=input.getPixel(512,516)
            // Pass initial bitmap accounting, then exhaust actual native work buffers.
            val constrained=input.allocationByteCount.toLong()+2L*1024*1024
            try {JxlCodec.encode(input,file,100,true,constrained);fail("Native work-buffer budget ignored")}
            catch(_: OutOfMemoryError) { }
            assertFalse(input.isRecycled);assertEquals(before,input.getPixel(512,516))
            JxlCodec.encode(input,file,100,true,budget)
            val output=JxlCodec.decode(file,ImageDimensions(input.width,input.height),budget)
            try {assertPixels(input,output)} finally {output.recycle()}
        } finally {input.recycle();file.delete()}
    }
    @Test fun sixteenBitLinearAndEmbeddedP3IccConvertToSrgbBeforeQuantization() {
        withColourFixture("linear16",16,6) {image ->
            // IEC sRGB transfer function applied to 16-bit LINEAR values
            // 0, .003, .018, .18, .5, 1; copying/truncating the source fails.
            val expected=intArrayOf(0,10,36,118,188,255)
            expected.forEachIndexed {x,v -> assertRgbNear(Color.rgb(v,v,v),image.getPixel(x,0),1)}
        }
        withColourFixture("p3-icc16",16,3) {image ->
            // Independent D65 Display-P3 -> sRGB matrix, gamma 2.2 source
            // and IEC sRGB destination transfer function. Source triplets:
            // (.8,.4,.2), (.2,.6,.4), (.3,.4,.7). Profile is embedded ICC.
            val expected=intArrayOf(Color.rgb(221,94,24),Color.rgb(0,157,97),Color.rgb(67,103,186))
            expected.forEachIndexed {x,c -> assertRgbNear(c,image.getPixel(x,0),2)}
            if(Build.VERSION.SDK_INT>=26) assertEquals(ColorSpace.get(ColorSpace.Named.SRGB),image.colorSpace)
        }
    }
    @Test fun tenBitPqAndHlgAreToneMappedToSdrWithoutClippingAllHighlights() {
        for(name in listOf("pq10","pq10-xyb")) withColourFixture(name,10,8) {image ->
            // BT.2408 EETF for a 1000-nit source, 203-nit target. Neutral
            // source luminances: 0,1,10,50,100,203,400,1000 cd/m2, quantized
            // to actual 10-bit PQ values before encoding. Constants calculated
            // from ST2084 + BT2408 equations, not the decoder being tested.
            val expected=intArrayOf(0,15,63,136,186,229,250,255)
            expected.forEachIndexed {x,v -> assertRgbNear(Color.rgb(v,v,v),image.getPixel(x,0),2)}
            assertTrue(Color.red(image.getPixel(5,0))<Color.red(image.getPixel(6,0)))
            assertTrue(Color.red(image.getPixel(6,0))<Color.red(image.getPixel(7,0)))
        }
        withColourFixture("linear16-hdr",16,8) {image ->
            // The same absolute luminances stored in 16-bit linear RGB with
            // a 1000-nit intensity target, rather than a PQ transfer curve.
            val expected=intArrayOf(0,15,63,136,186,229,250,255)
            expected.forEachIndexed {x,v -> assertRgbNear(Color.rgb(v,v,v),image.getPixel(x,0),2)}
        }
        withColourFixture("pq10-alpha",10,4) {image ->
            val alphas=intArrayOf(0,64,128,255)
            for(x in alphas.indices) assertEquals(alphas[x],Color.alpha(image.getPixel(x,0)))
            // Convert the unassociated 100-nit HDR colour first, then store
            // premultiplied RGBA; premultiplying before tone mapping is wrong.
            for(x in 1..3) assertRgbNear(Color.rgb(186,186,186),image.getPixel(x,0),2)
        }
        withColourFixture("hlg10",10,5) {image ->
            // HLG inverse OETF and reference 1000-nit OOTF (gamma 1.2),
            // then the same BT.2408 203-nit mapping and IEC sRGB encoding
            // as PQ. This matches the HEIF importer, not native libjxl's
            // destination-dependent HLG display adaptation.
            // Encoded HLG values: 0,.25,.5,.75,1 at ten-bit precision.
            val expected=intArrayOf(0,62,137,229,255)
            expected.forEachIndexed {x,v -> assertRgbNear(Color.rgb(v,v,v),image.getPixel(x,0),2)}
        }
        withColourFixture("pq10-chunks",10,1031,Rect(247,0,521,1),ImageDimensions(137,1)) {image ->
            // Source crop crosses the bounded colour-conversion chunk boundary.
            val values=intArrayOf(0,15,63,136,186,229,250,255)
            for(x in 0 until 137) {
                val v=values[(247+x*2)%8]
                assertRgbNear(Color.rgb(v,v,v),image.getPixel(x,0),2)
            }
        }
    }
    @Test fun IccColourConversionPreservesAlphaUntilCompositingOntoChosenBackground() {
        withColourFixture("p3-icc-alpha16",16,4) {image ->
            assertTrue(image.hasAlpha());assertTrue(image.isPremultiplied)
            val alphas=intArrayOf(0,64,128,255)
            for(x in alphas.indices) assertEquals(alphas[x],Color.alpha(image.getPixel(x,0)))
            for(x in 1..3) assertRgbNear(Color.rgb(221,94,24),image.getPixel(x,0),3)
            for(background in intArrayOf(Color.WHITE,Color.rgb(20,80,160))) {
                val flat=Bitmap.createBitmap(4,1,Bitmap.Config.ARGB_8888)
                try {
                    flat.eraseColor(background)
                    Canvas(flat).drawBitmap(image,0f,0f,Paint())
                    for(x in alphas.indices) {
                        val expected=ColorUtils.compositeColors(Color.argb(alphas[x],221,94,24),background)
                        assertEquals(255,Color.alpha(flat.getPixel(x,0)))
                        assertRgbNear(expected,flat.getPixel(x,0),2)
                    }
                    assertEquals(background,flat.getPixel(0,0))
                } finally {flat.recycle()}
            }
        }
    }
    private fun withColourFixture(name: String,bits: Int,width: Int,crop: Rect?=null,size: ImageDimensions=ImageDimensions(width,1),check: (Bitmap)->Unit) {
        val file=File.createTempFile("colour-$name-",".jxl",context.cacheDir)
        try {
            val encoded=InstrumentationRegistry.getInstrumentation().context.assets.open("colour-fixtures/$name.jxl.b64").use {it.readBytes()}
            file.writeBytes(Base64.decode(encoded,Base64.DEFAULT))
            assertEquals("Actual source bit depth",bits,JxlCodec.sourceBitDepth(file))
            assertEquals(ImageDimensions(width,1),JxlCodec.dimensions(file))
            val image=JxlCodec.decode(file,size,budget,crop)
            try {check(image)} finally {image.recycle()}
        } finally {file.delete()}
    }
    private fun assertRgbNear(expected: Int,actual: Int,tolerance: Int) {
        for(shift in intArrayOf(16,8,0))
            assertTrue("RGB ${Integer.toHexString(expected)} -> ${Integer.toHexString(actual)}",kotlin.math.abs(((expected ushr shift) and 255)-((actual ushr shift) and 255))<=tolerance)
    }
    private fun pattern(size: ImageDimensions) = Bitmap.createBitmap(size.width,size.height,Bitmap.Config.ARGB_8888).apply {
        val row=IntArray(width)
        for(y in 0 until height) {
            for(x in row.indices) row[x]=Color.rgb((x*19+y)%256,(x+y*17)%256,(x*3+y*11)%256)
            setPixels(row,0,width,0,y,width,1)
        }
        setHasAlpha(false)
    }
    private fun assertPixels(expected: Bitmap,actual: Bitmap) {
        assertEquals(expected.width,actual.width);assertEquals(expected.height,actual.height)
        val expectedRow=IntArray(expected.width);val actualRow=IntArray(expected.width)
        for(y in 0 until expected.height) {
            expected.getPixels(expectedRow,0,expected.width,0,y,expected.width,1)
            actual.getPixels(actualRow,0,actual.width,0,y,actual.width,1)
            assertArrayEquals("Row $y",expectedRow,actualRow)
        }
    }
}
