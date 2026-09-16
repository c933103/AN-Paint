/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.*
import org.catrobat.paintroid.classic.CanvasBitmapOverview
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CanvasBitmapOverviewTest {
    @Test fun onePixelStrokesRemainVisibleAtReducedScalesWithoutChangingSourcePixels() {
        val source=Bitmap.createBitmap(256,256,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
        // A continuous staircase line exposes skipped samples in nearest-neighbour reductions.
        for(x in 16..239) {source.setPixel(x,60+x/3,Color.BLACK);source.setPixel(x,181,Color.BLACK)}
        val original=IntArray(256*256).also {source.getPixels(it,0,256,0,0,256,256)}
        CanvasBitmapOverview().use {preview ->
            for(scale in listOf(.75f,.5f,.31f,.125f)) {
                val image=Bitmap.createBitmap(256,256,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
                val canvas=Canvas(image);canvas.translate(.3f,.2f);canvas.scale(scale,scale)
                preview.draw(canvas,source,scale)
                for(x in (24*scale).toInt()..(230*scale).toInt()) {
                    for(row in listOf((60*scale+x/3f).toInt(),(181*scale).toInt())) {
                        assertTrue("No missing segment at scale $scale, column $x, row $row",(row-2..row+2).any {y ->Color.red(image.getPixel(x,y))<254})
                    }
                }
                image.recycle()
            }
        }
        val unchanged=IntArray(original.size).also {source.getPixels(it,0,256,0,0,256,256)}
        assertArrayEquals(original,unchanged);source.recycle()
    }

    @Test fun magnifiedPixelsStayCrispAndCachedOverviewRefreshesAfterAnEdit() {
        val source=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
        CanvasBitmapOverview().use {preview ->
            val image=Bitmap.createBitmap(96,96,Bitmap.Config.ARGB_8888)
            fun render(scale: Float) {image.eraseColor(Color.WHITE);val canvas=Canvas(image);canvas.scale(scale,scale);preview.draw(canvas,source,scale)}
            render(.125f);assertEquals(Color.WHITE,image.getPixel(1,1))
            source.eraseColor(Color.BLACK);render(.125f);assertEquals(Color.BLACK,image.getPixel(1,1))
            source.eraseColor(Color.WHITE);source.setPixel(10,10,Color.BLACK);render(2.5f)
            for(y in 0..79) for(x in 0..79) assertTrue(image.getPixel(x,y) in listOf(Color.WHITE,Color.BLACK))
            assertEquals(Color.BLACK,image.getPixel(26,26));image.recycle()
        }
        source.recycle()
    }
}
