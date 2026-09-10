/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later.
 * Native codec: JPEG XL Project Authors, BSD-3-Clause; see JPEG_XL_NOTICES.txt.
 */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Rect
import java.io.File

object JxlCodec {
    private object Native {
        init {System.loadLibrary("anpaint_jxl")}
        external fun info(path: String): IntArray
        external fun decode(path: String,target: Bitmap,left: Int,top: Int,right: Int,bottom: Int,budget: Long)
        external fun encode(image: Bitmap,path: String,quality: Int,lossless: Boolean,budget: Long)
    }
    fun isJxl(file: File): Boolean = file.inputStream().use {
        val b=ByteArray(12);val n=it.read(b)
        n>=2 && b[0]==0xff.toByte() && b[1]==0x0a.toByte() || n==12 && b.contentEquals(byteArrayOf(0,0,0,12,0x4a,0x58,0x4c,0x20,13,10,-121,10))
    }
    fun dimensions(file: File): ImageDimensions = Native.info(file.path).let {ImageDimensions(it[0],it[1])}
    fun decode(file: File,size: ImageDimensions,budget: Long,crop: Rect? = null): Bitmap {
        val output=Bitmap.createBitmap(size.width,size.height,Bitmap.Config.ARGB_8888)
        try {Native.decode(file.path,output,crop?.left ?: 0,crop?.top ?: 0,crop?.right ?: -1,crop?.bottom ?: -1,budget);return output}
        catch(error: Throwable) {output.recycle();throw error}
    }
    fun encode(image: Bitmap,file: File,quality: Int,lossless: Boolean,budget: Long) = Native.encode(image,file.path,quality.coerceIn(1,100),lossless,budget)
}
