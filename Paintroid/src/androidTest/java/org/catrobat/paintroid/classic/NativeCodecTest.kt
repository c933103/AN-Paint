/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Rect
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
        val input=Bitmap.createBitmap(2057,17,Bitmap.Config.ARGB_8888)
        val file=File.createTempFile("codec-chunks-",".jxl",context.cacheDir)
        try {
            for(y in 0 until input.height) for(x in 0 until input.width)
                input.setPixel(x,y,Color.rgb((x*19+y)%256,(x+y*17)%256,(x*3+y*11)%256))
            input.setHasAlpha(false)
            JxlCodec.encode(input,file,100,true,budget)
            val output=JxlCodec.decode(file,ImageDimensions(2057,17),budget)
            try {
                for(y in 0 until input.height) for(x in 0 until input.width)
                    assertEquals("Pixel $x,$y",input.getPixel(x,y),output.getPixel(x,y))
            } finally {output.recycle()}
        } finally {input.recycle();file.delete()}
    }
}
