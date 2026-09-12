/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.Rect
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.io.IOException

/** Tests the shipped Java encoders against Android's real decoders and assembly fallback. */
@RunWith(AndroidJUnit4::class)
class LegacyCodecTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext
    private val budget = 256L * 1024 * 1024
    private fun source() = Bitmap.createBitmap(19,13,Bitmap.Config.ARGB_8888).apply {
        for(y in 0 until height) for(x in 0 until width) {
            val n=(x+y*width)%247
            setPixel(x,y,Color.rgb(n,(n*37)%256,(n*19)%256))
        }
        setHasAlpha(false)
    }
    @Test fun bmpAndGifRoundTripThroughPlatformAndSharedImportWithExactSmallPalettes() {
        val input=source()
        try { for(format in listOf(ImageFormat.BMP,ImageFormat.GIF)) {
            // An unhelpful provider name does not determine format detection.
            val file=File.createTempFile("legacy-roundtrip-",".bin",context.cacheDir)
            try {
                ImageExporter.encode(input,file,ExportOptions(format),budget)
                val source=ImportedImage(file,"provider.bin")
                assertEquals(ImageDimensions(19,13),source.dimensions)
                val decoded=source.decode(ImportPlan.create(source.dimensions,source.dimensions),budget)
                try {for(y in 0 until 13) for(x in 0 until 19) assertEquals("${format.label} $x,$y",input.getPixel(x,y),decoded.getPixel(x,y))}
                finally {decoded.recycle()}
                val platform=BitmapFactory.decodeFile(file.path)
                assertNotNull(platform);platform!!.recycle()
            } finally {file.delete()}
        }} finally {input.recycle()}
    }
    @Test fun bmpAndGifAssemblyCropsUseOriginalPixelsWithAvailableDecoder() {
        val input=source()
        try {for(format in listOf(ImageFormat.BMP,ImageFormat.GIF)) {
            val file=File.createTempFile("legacy-crop-",format.extension,context.cacheDir)
            try {
                ImageExporter.encode(input,file,ExportOptions(format),budget)
                val item=AssemblyImage("one",file,file.name,null,ImageDimensions(19,13),Rect(3,2,14,10),Attachment(null,null))
                val renderer=AssemblyRenderer(context,listOf(item),mapOf("one" to Rect(0,0,11,8)),0)
                val crop=renderer.render(ImageDimensions(11,8))
                try {for(y in 0 until 8) for(x in 0 until 11) assertEquals("${format.label} crop $x,$y",input.getPixel(x+3,y+2),crop.getPixel(x,y))}
                finally {crop.recycle()}
            } finally {file.delete()}
        }} finally {input.recycle()}
    }
    @Test fun failedBudgetPreservesExistingDestinationAndSourcePixels() {
        val input=source()
        try {for(format in listOf(ImageFormat.BMP,ImageFormat.GIF)) {
            val file=File.createTempFile("legacy-existing-",format.extension,context.cacheDir)
            try {
                file.writeText("previous file")
                val before=input.getPixel(7,4)
                try {ImageExporter.encode(input,file,ExportOptions(format),1000);fail("Expected budget rejection")}
                catch(expected: IOException) {assertNotNull(expected.message)}
                assertEquals("previous file",file.readText());assertEquals(before,input.getPixel(7,4));assertFalse(input.isRecycled)
            } finally {file.delete()}
        }} finally {input.recycle()}
    }
}
