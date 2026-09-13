/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import org.catrobat.paintroid.classic.TextImageCodec
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.io.IOException

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class TextImageCodecTest {
    private val context get()=RuntimeEnvironment.getApplication()
    private val budget=64L*1024*1024
    @Test fun base64PngRestoresExactPixelsAndSupportsInPlaceNormalization() {
        val image=Bitmap.createBitmap(9,5,Bitmap.Config.ARGB_8888).apply {
            for(y in 0 until height)for(x in 0 until width)setPixel(x,y,Color.rgb(x*27,y*61,(x+y)*17))
        }
        val file=File.createTempFile("base64-pixels-",".txt",context.cacheDir)
        try {
            TextImageCodec.encodeBase64(image,file,budget)
            assertTrue(file.readText().startsWith("data:image/png;base64,"))
            assertTrue(TextImageCodec.inspect(file))
            TextImageCodec.decodeToFile(file,file,1024*1024)
            assertFalse(TextImageCodec.inspect(file))
            val decoded=BitmapFactory.decodeFile(file.path)
            assertNotNull(decoded)
            try {assertTrue(image.sameAs(decoded))} finally {decoded.recycle()}
        } finally {image.recycle();file.delete()}
    }
    @Test fun invalidPayloadAndSizeLimitKeepOriginalDestinationAndCleanTemporaryFiles() {
        val directory=File(context.cacheDir,"text-image-rejection").apply {deleteRecursively();mkdirs()}
        val file=File(directory,"image.txt")
        try {
            for(text in listOf("data:image/png;base64,aGVsbG8=","data:image/png;base64,AB==")) {
                file.writeText(text)
                try {TextImageCodec.decodeToFile(file,file,1024);fail("Accepted invalid image text")}
                catch(expected: IOException) {assertNotNull(expected.message)}
                assertEquals(text,file.readText());assertEquals(1,directory.listFiles()!!.size)
            }
            val image=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888)
            try {TextImageCodec.encodeBase64(image,file,budget)} finally {image.recycle()}
            val original=file.readBytes()
            try {TextImageCodec.decodeToFile(file,file,1);fail("Exceeded decoded byte limit")}
            catch(expected: IOException) {assertNotNull(expected.message)}
            assertArrayEquals(original,file.readBytes());assertEquals(1,directory.listFiles()!!.size)
        } finally {directory.deleteRecursively()}
    }
    @Test fun asciiUsesChosenWidthAspectAndInversionWithoutChangingSource() {
        val image=Bitmap.createBitmap(80,40,Bitmap.Config.ARGB_8888).apply {
            eraseColor(Color.WHITE)
            for(y in 0 until height)for(x in 0 until 40)setPixel(x,y,Color.BLACK)
        }
        val file=File.createTempFile("ascii-pixels-",".txt",context.cacheDir)
        try {
            TextImageCodec.encodeAscii(image,file,40,false,budget)
            val normal=file.readLines()
            assertEquals(10,normal.size);assertTrue(normal.all {it.length==40})
            assertTrue(normal.all {it.first()=='@' && it.last()==' '})
            TextImageCodec.encodeAscii(image,file,40,true,budget)
            assertTrue(file.readLines().all {it.first()==' ' && it.last()=='@'})
            assertFalse(image.isRecycled);assertEquals(Color.BLACK,image.getPixel(0,0));assertEquals(Color.WHITE,image.getPixel(79,39))
            assertFalse(TextImageCodec.inspect(file))
        } finally {image.recycle();file.delete()}
    }
    @Test fun rejectedExportsPreserveExistingFile() {
        val image=Bitmap.createBitmap(4,4,Bitmap.Config.ARGB_8888)
        val directory=File(context.cacheDir,"text-image-export-failure").apply {deleteRecursively();mkdirs()}
        val file=File(directory,"existing.txt").apply {writeText("old content")}
        try {
            try {TextImageCodec.encodeBase64(image,file,1);fail("Accepted exhausted budget")}
            catch(expected: IOException) {assertEquals("old content",file.readText())}
            try {TextImageCodec.encodeAscii(image,file,40,false,1);fail("Accepted exhausted budget")}
            catch(expected: IOException) {assertEquals("old content",file.readText())}
            assertEquals(1,directory.listFiles()!!.size)
        } finally {image.recycle();directory.deleteRecursively()}
    }
}
