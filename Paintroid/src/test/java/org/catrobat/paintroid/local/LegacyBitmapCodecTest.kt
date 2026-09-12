/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.BitmapRegionDecoder
import android.graphics.Color
import android.graphics.Rect
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.Implementation
import org.robolectric.annotation.Implements
import java.io.File
import java.io.IOException

/** BMP/GIF have no region decoder on some Android versions: exercise the bounded full-decode path. */
@Implements(BitmapRegionDecoder::class)
class UnavailableRegionDecoderShadow {
    companion object {
        @JvmStatic @Implementation fun newInstance(path: String,shareable: Boolean): BitmapRegionDecoder = throw IOException("No region codec for this fixture")
    }
}

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],shadows=[UnavailableRegionDecoderShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class LegacyBitmapCodecTest {
    private val context get()=RuntimeEnvironment.getApplication()
    private val budget=256L*1024*1024
    private fun source()=Bitmap.createBitmap(13,9,Bitmap.Config.ARGB_8888).apply {
        for(y in 0 until height) for(x in 0 until width) setPixel(x,y,Color.rgb(x*17,y*23,(x+y)*7))
        setHasAlpha(false)
    }
    @Test fun bmpAndGifOpenInsertAndFallbackCropPreserveEveryPalettePixel() {
        val image=source()
        try {for(format in listOf(ImageFormat.BMP,ImageFormat.GIF)) {
            val file=File.createTempFile("legacy-fixture-",".bin",context.cacheDir)
            val document=PaintDocument(13,9,File(context.cacheDir,"legacy-document-${format.name}"))
            try {
                ImageExporter.encode(image,file,ExportOptions(format),budget)
                val imported=ImportedImage(file,"unknown.bin")
                val decoded=imported.decode(ImportPlan.create(imported.dimensions,imported.dimensions),budget)
                try {
                    document.paste(decoded);document.finishSelection()
                    for(y in 0 until 9) for(x in 0 until 13) {
                        assertEquals(image.getPixel(x,y),decoded.getPixel(x,y))
                        assertEquals(image.getPixel(x,y),document.bitmap.getPixel(x,y))
                    }
                } finally {decoded.recycle()}
                val item=AssemblyImage("one",file,file.name,null,imported.dimensions,Rect(2,1,10,6),Attachment(null,null))
                val output=AssemblyRenderer(context,listOf(item),mapOf("one" to Rect(0,0,8,5)),0).render(ImageDimensions(8,5))
                try {for(y in 0 until 5) for(x in 0 until 8) assertEquals(image.getPixel(x+2,y+1),output.getPixel(x,y))}
                finally {output.recycle()}
            } finally {document.close();file.delete()}
        }} finally {image.recycle()}
    }
    @Test fun failedEncodeKeepsOldFileAndRemovesTemporaryOutput() {
        val image=source()
        val directory=File(context.cacheDir,"legacy-budget-test").apply {deleteRecursively();mkdirs()}
        try {for(format in listOf(ImageFormat.BMP,ImageFormat.GIF)) {
            val file=File(directory,"old"+format.extension).apply {writeText("old content")}
            try {ImageExporter.encode(image,file,ExportOptions(format),1000);fail("Expected rejection")}
            catch(expected: IOException) {assertNotNull(expected.message)}
            assertEquals("old content",file.readText());assertEquals(1,directory.listFiles()!!.size)
            file.delete()
        }} finally {image.recycle();directory.deleteRecursively()}
    }
}
