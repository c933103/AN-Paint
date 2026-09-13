/* AN Paint, 2026. GNU AGPL-3.0-or-later.
 * libtiff/libjpeg-turbo authors and terms: legal/TIFF_NOTICES.txt.
 */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Rect
import java.io.File

/** TIFF page import and opaque RGB TIFF export on every supported Android API. */
object TiffCodec {
    private object Native {
        init { System.loadLibrary("anpaint_tiff") }
        external fun pageCount(path: String): Int
        external fun info(path: String, pageIndex: Int): LongArray
        external fun decode(path: String, image: Bitmap, left: Int, top: Int, right: Int, bottom: Int, budget: Long, pageIndex: Int)
        external fun encode(image: Bitmap, path: String, compressed: Boolean, budget: Long)
    }

    /** Detect classic TIFF and BigTIFF in either byte order, independent of the filename. */
    fun isTiff(file: File): Boolean = file.inputStream().use { input ->
        val header = ByteArray(4)
        if (input.read(header) != header.size) return@use false
        (header[0] == 73.toByte() && header[1] == 73.toByte() && header[3] == 0.toByte() &&
            (header[2] == 42.toByte() || header[2] == 43.toByte())) ||
            (header[0] == 77.toByte() && header[1] == 77.toByte() && header[2] == 0.toByte() &&
                (header[3] == 42.toByte() || header[3] == 43.toByte()))
    }

    /** Main TIFF directories, bounded to 4096 pages; malformed directory chains fail explicitly. */
    fun pageCount(file: File): Int = Native.pageCount(file.path)

    /** Page indexes are zero-based. Dimensions include that page's TIFF orientation. */
    fun dimensions(file: File, pageIndex: Int = 0): ImageDimensions = Native.info(file.path, pageIndex).let {
        ImageDimensions(it[0].toInt(), it[1].toInt())
    }

    /** Includes the largest source strip/tile, native codec work, metadata and output bitmap. */
    fun decodeWorkingBytes(file: File, size: ImageDimensions, pageIndex: Int = 0): Long {
        val nativeBytes = Native.info(file.path, pageIndex)[2]
        val pixels = size.width.toLong() * size.height
        return if (pixels > (Long.MAX_VALUE - nativeBytes) / 4) Long.MAX_VALUE else nativeBytes + pixels * 4
    }

    /** Crops use the displayed orientation; scaling uses the same samples as full-image imports. */
    fun decode(file: File, size: ImageDimensions, budget: Long, crop: Rect? = null, pageIndex: Int = 0): Bitmap {
        if (decodeWorkingBytes(file, size, pageIndex) > budget)
            throw OutOfMemoryError("TIFF decoding exceeds the available image memory budget")
        val output = Bitmap.createBitmap(size.width, size.height, Bitmap.Config.ARGB_8888)
        try {
            Native.decode(file.path, output, crop?.left ?: 0, crop?.top ?: 0, crop?.right ?: -1, crop?.bottom ?: -1, budget, pageIndex)
            return output
        } catch (error: Throwable) {
            output.recycle()
            throw error
        }
    }

    /** Lossless Deflate or uncompressed, single-page classic TIFF; failed saves preserve the destination. */
    fun encode(image: Bitmap, file: File, compressed: Boolean, budget: Long) {
        Native.encode(image, file.path, compressed, budget)
    }
}
