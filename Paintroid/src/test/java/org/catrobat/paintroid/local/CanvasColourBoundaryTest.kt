/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.ColorSpace
import java.nio.ByteBuffer
import java.nio.ByteOrder
import org.catrobat.paintroid.classic.PaintDocument
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CanvasColourBoundaryTest {
    @Test fun insertedTransparencyCompositesOntoExistingPixelsAndUndoRestoresThem() {
        val image=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888)
        image.eraseColor(Color.argb(128,200,40,0))
        image.setPixel(1,1,Color.TRANSPARENT)
        val document=PaintDocument(4,4,RuntimeEnvironment.getApplication().cacheDir)
        try {
            document.background=Color.WHITE
            document.bitmap.eraseColor(Color.GREEN)
            assertTrue(document.paste(image,true))
            assertEquals(128,Color.alpha(document.selectionImage()!!.getPixel(0,0)))
            document.finishSelection()
            assertFalse(document.bitmap.hasAlpha())
            assertEquals(Color.GREEN,document.bitmap.getPixel(1,1))
            val pixel=document.bitmap.getPixel(0,0)
            assertEquals(100.0,Color.red(pixel).toDouble(),1.0)
            assertEquals(147.0,Color.green(pixel).toDouble(),1.0)
            assertEquals(0,Color.blue(pixel))
            document.undo()
            assertEquals(Color.GREEN,document.bitmap.getPixel(0,0))
        } finally {document.close();if(!image.isRecycled)image.recycle()}
    }
    @Test fun mutableLinearFloatInputBecomesSrgbEightBitAndCompositesAlpha() {
        val image=Bitmap.createBitmap(2,2,Bitmap.Config.RGBA_F16,true,ColorSpace.get(ColorSpace.Named.LINEAR_SRGB))
        // Straight linear red 0.5 at alpha 0.5; stored premultiplied red is 0.25.
        val data=ByteBuffer.allocate(32).order(ByteOrder.nativeOrder())
        repeat(4) { data.putShort(0x3400);data.putShort(0);data.putShort(0);data.putShort(0x3800) }
        data.rewind();image.copyPixelsFromBuffer(data)
        val document=PaintDocument(2,2,RuntimeEnvironment.getApplication().cacheDir)
        try {
            document.background=Color.WHITE
            document.replace(image)
            assertEquals(Bitmap.Config.ARGB_8888,document.bitmap.config)
            assertTrue(document.bitmap.colorSpace!!.isSrgb)
            assertFalse(document.bitmap.hasAlpha())
            val pixel=document.bitmap.getPixel(0,0)
            assertEquals(255,Color.alpha(pixel))
            assertEquals(221.5,Color.red(pixel).toDouble(),2.0)
            assertEquals(127.5,Color.green(pixel).toDouble(),2.0)
            assertEquals(127.5,Color.blue(pixel).toDouble(),2.0)
        } finally {document.close();if(!image.isRecycled)image.recycle()}
    }
}
