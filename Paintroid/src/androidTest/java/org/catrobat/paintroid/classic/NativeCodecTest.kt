/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Rect
import androidx.core.graphics.ColorUtils
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
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
        assertEquals(19,catalog.fonts.size)
        assertEquals(10,catalog.fonts.count {it.asset!=null})
        catalog.fonts.forEachIndexed {index,font ->
            assertNotNull(font.name,catalog.face(index))
            font.asset?.let {path -> assertTrue(context.assets.open(path).use {it.readBytes()}.size>1000)}
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
