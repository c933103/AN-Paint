/* AN Paint, 2026. GNU AGPL-3.0-or-later. Real Android codecs + synthetic ICC/HDR fixtures. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.Rect
import android.os.Build
import android.util.Base64
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.io.IOException
import kotlin.math.abs

@RunWith(AndroidJUnit4::class)
class PlatformColourImportTest {
    private val context get()=InstrumentationRegistry.getInstrumentation().targetContext
    private val assets get()=InstrumentationRegistry.getInstrumentation().context.assets
    private val budget=256L*1024*1024
    private fun fixture(name: String): File = File.createTempFile("colour-fixture-",".image",context.cacheDir).apply {
        writeBytes(Base64.decode(assets.open("colour-fixtures/$name.b64").bufferedReader().use { it.readText() },Base64.DEFAULT))
    }
    private fun decode(file: File,target: ImageDimensions?=null): Bitmap {
        val source=ImportedImage(file,"colour fixture")
        return source.decode(ImportPlan.create(source.dimensions,target?:source.dimensions),budget)
    }
    private fun expected(index: Int): Int {
        val p=JSONObject(assets.open("colour-fixtures/platform-expected.json").bufferedReader().use { it.readText() }).getJSONArray("p3_srgb").getJSONArray(index)
        return Color.rgb(p.getInt(0),p.getInt(1),p.getInt(2))
    }
    private fun closeColour(expected: Int,actual: Int,tolerance: Int=3) {
        listOf(Color.red(expected) to Color.red(actual),Color.green(expected) to Color.green(actual),Color.blue(expected) to Color.blue(actual)).forEach {
            assertTrue("Expected ${Integer.toHexString(expected)}, got ${Integer.toHexString(actual)}",abs(it.first-it.second)<=tolerance)
        }
    }
    private fun canonical(image: Bitmap) {
        assertEquals(Bitmap.Config.ARGB_8888,image.config)
        if(Build.VERSION.SDK_INT>=26) assertTrue(image.colorSpace!!.isSrgb)
        if(Build.VERSION.SDK_INT>=34) assertFalse(image.hasGainmap())
    }
    @Test fun p3IccPng16ConvertsBeforeQuantizationAndKeepsAlpha() {
        val file=fixture("platform-p3-alpha16.png")
        try {
            if(Build.VERSION.SDK_INT>=26) {
                val colour=PlatformImageColour.read(file)
                val raw=colour.withDecodeFile(file) { BitmapFactory.decodeFile(it.path,colour.options(1)) }
                try { assertEquals("16-bit PNG must reach colour conversion in F16",Bitmap.Config.RGBA_F16,raw.config) }
                finally { raw.recycle() }
            }
            val image=decode(file)
            try {
                canonical(image);closeColour(expected(0),image.getPixel(4,4))
                closeColour(expected(1),image.getPixel(12,4))
                assertTrue(abs(128-Color.alpha(image.getPixel(12,4)))<=1)
                assertEquals(0,Color.alpha(image.getPixel(20,4)))
            } finally { image.recycle() }
            assertFalse(file.parentFile!!.listFiles()!!.any { it.name.startsWith("colour-input-") })
        } finally { file.delete() }
    }
    @Test fun jpegAndWebpIccAreConvertedExactlyOnce() {
        for(name in listOf("platform-p3.jpg","platform-p3.webp")) {
            val file=fixture(name)
            try {
                val image=decode(file)
                try { canonical(image);for(i in listOf(0,1,3)) closeColour(expected(i),image.getPixel(i*8+4,4),4) }
                finally { image.recycle() }
            } finally { file.delete() }
        }
    }
    @Test fun transparentPixelsCompositeAgainstDocumentBackgroundAfterResize() {
        val file=fixture("platform-p3-alpha16.png")
        val history=File(context.cacheDir,"colour-history-${System.nanoTime()}")
        val document=PaintDocument(1,1,history)
        try {
            val image=decode(file,ImageDimensions(16,4));canonical(image)
            val before=image.getPixel(6,2);val background=Color.rgb(40,80,120)
            document.background=background;document.replace(image)
            val result=document.bitmap
            assertEquals(background,result.getPixel(10,2));assertFalse(result.hasAlpha())
            val alpha=Color.alpha(before)/255.0
            fun mix(a: Int,b: Int)=(a*alpha+b*(1-alpha)).toInt()
            closeColour(Color.rgb(mix(Color.red(before),40),mix(Color.green(before),80),mix(Color.blue(before),120)),result.getPixel(6,2),2)
            assertEquals(255,Color.alpha(result.getPixel(6,2)))
        } finally { document.close();history.deleteRecursively();file.delete() }
    }
    @Test fun assemblyCropUsesSameColourConversionAndWhiteBackground() {
        val file=fixture("platform-p3-alpha16.png")
        try {
            val item=AssemblyImage("p3",file,"P3 PNG",null,ImageDimensions(32,8),Rect(8,0,24,8))
            val renderer=AssemblyRenderer(context,listOf(item),mapOf(item.id to Rect(0,0,16,8)),0)
            val image=renderer.render(renderer.original)
            try {
                canonical(image);assertFalse(image.hasAlpha());assertEquals(Color.WHITE,image.getPixel(12,4))
                val p=expected(1)
                closeColour(Color.rgb((Color.red(p)+255)/2,(Color.green(p)+255)/2,(Color.blue(p)+255)/2),image.getPixel(4,4),3)
            } finally { image.recycle() }
        } finally { file.delete() }
    }
    @Test fun linear16AndPqPngRenderWithTransferAndHighlightDetail() {
        val linear=fixture("platform-linear16.png");val pq=fixture("platform-pq16.png");val priority=fixture("platform-pq-priority16.png")
        try {
            val a=decode(linear);val b=decode(pq);val c=decode(priority)
            try {
                canonical(a);canonical(b);canonical(c)
                closeColour(Color.rgb(188,188,188),a.getPixel(20,4),2)
                val shades=(0..3).map { Color.red(b.getPixel(it*8+4,4)) }
                assertTrue("PQ highlights clipped or transfer ignored: $shades",shades.zipWithNext().all { it.first<it.second })
                assertTrue("PQ SDR midtone must not be raw PQ code",shades[1]>150)
                for(i in 0..3) assertEquals(b.getPixel(i*8+4,4),c.getPixel(i*8+4,4))
            } finally { a.recycle();b.recycle();c.recycle() }
        } finally { linear.delete();pq.delete();priority.delete() }
    }
    @Test fun pngGammaAndChromaticitiesUseSameConversionOnEveryAndroidVersion() {
        val gamma=fixture("platform-gamma-linear16.png");val chroma=fixture("platform-gamma-chroma16.png")
        try {
            val a=decode(gamma);val b=decode(chroma)
            try {
                canonical(a);canonical(b);closeColour(Color.rgb(188,188,188),a.getPixel(20,4),2)
                closeColour(expected(0),b.getPixel(4,4),3);closeColour(expected(1),b.getPixel(12,4),3)
                assertTrue(abs(128-Color.alpha(b.getPixel(12,4)))<=1)
            } finally { a.recycle();b.recycle() }
        } finally { gamma.delete();chroma.delete() }
    }
    @Test fun malformedColourMetadataFailsWithoutModifyingSourceOrLeakingCopies() {
        val file=fixture("platform-p3-alpha16.png")
        try {
            val bytes=file.readBytes()
            val signature="iCCP".toByteArray(Charsets.US_ASCII).toList()
            val index=bytes.toList().windowed(4).indexOf(signature)
            assertTrue(index>0);bytes[index+8]=(bytes[index+8].toInt() xor 1).toByte()
            file.writeBytes(bytes)
            try { ImportedImage(file,"damaged profile");fail("A corrupt colour chunk was ignored") }
            catch(_: IOException) {}
            assertArrayEquals(bytes,file.readBytes())
            assertFalse(file.parentFile!!.listFiles()!!.any { it.name.startsWith("colour-input-") })
        } finally { file.delete() }
    }
    @Test fun colourMemoryIncludesF16AndConversionAndRejectsInsufficientBudget() {
        val file=fixture("platform-p3-alpha16.png")
        try {
            val source=ImportedImage(file,"P3 PNG");val plan=ImportPlan.create(source.dimensions,source.dimensions)
            assertTrue(source.estimatedBytes(plan,0)>=8L*1024*1024+source.dimensions.pixels*16)
            try { source.decode(plan,1024);fail("Colour conversion ignored memory admission") } catch(_: ImageSizeException) {}
            assertFalse(file.parentFile!!.listFiles()!!.any { it.name.startsWith("colour-input-") })
        } finally { file.delete() }
    }
}
