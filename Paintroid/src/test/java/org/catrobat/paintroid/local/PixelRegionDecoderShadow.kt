/* AN Paint test infrastructure, 2026-09-07. GNU AGPL-3.0-or-later.
 * Robolectric 4.14.1's stock region decoder only allocates blank bitmaps, even
 * in native graphics mode. Small fixtures are decoded with native BitmapFactory, then sampled for these tests;
 * production continues to use Android's BitmapRegionDecoder. This does not
 * constitute physical-device validation of Android's native image codecs.
 */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.BitmapRegionDecoder
import android.graphics.Rect
import org.robolectric.annotation.Implementation
import org.robolectric.annotation.Implements
import org.robolectric.shadow.api.Shadow
import org.robolectric.util.ReflectionHelpers
import java.io.File

@Implements(BitmapRegionDecoder::class)
class PixelRegionDecoderShadow {
    private lateinit var file: File
    companion object {
        @JvmStatic @Implementation fun newInstance(path: String,shareable: Boolean): BitmapRegionDecoder {
            val result=ReflectionHelpers.callConstructor(BitmapRegionDecoder::class.java,ReflectionHelpers.ClassParameter.from(java.lang.Long.TYPE,0L))
            Shadow.extract<PixelRegionDecoderShadow>(result).file=File(path)
            return result
        }
    }
    @Implementation fun getWidth(): Int = bounds().outWidth
    @Implementation fun getHeight(): Int = bounds().outHeight
    private fun bounds() = BitmapFactory.Options().apply { inJustDecodeBounds=true; BitmapFactory.decodeFile(file.path,this) }
    @Implementation fun decodeRegion(region: Rect,options: BitmapFactory.Options): Bitmap {
        val source=BitmapFactory.decodeFile(file.path,BitmapFactory.Options().apply { inScaled=false; inPreferredConfig=Bitmap.Config.ARGB_8888 })
        try {
            val sample=options.inSampleSize.coerceAtLeast(1)
            val width=(region.width()+sample-1)/sample; val height=(region.height()+sample-1)/sample
            val pixels=IntArray(width*height)
            for (y in 0 until height) for (x in 0 until width) pixels[y*width+x]=source.getPixel(region.left+x*sample,region.top+y*sample)
            return Bitmap.createBitmap(pixels,width,height,Bitmap.Config.ARGB_8888)
        } finally { source.recycle() }
    }
    @Implementation fun recycle() = Unit
}
