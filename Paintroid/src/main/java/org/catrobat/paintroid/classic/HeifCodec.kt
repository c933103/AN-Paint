/* AN Paint, 2026. GNU AGPL-3.0-or-later.
 * Native dependencies and original authors: legal/HEIF_AVIF_NOTICES.txt.
 */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Rect
import java.io.File

/** Native HEIC and AVIF still-image import/export on every supported Android API. */
object HeifCodec {
    private object Native {
        init { System.loadLibrary("anpaint_heif") }
        external fun convertPngColour(input: Bitmap, output: Bitmap, gamma: Float, chromaticities: FloatArray?)
        external fun info(path: String): IntArray
        external fun convertColour(input: Bitmap, output: Bitmap, icc: ByteArray?, primaries: Int, transfer: Int)
        external fun decode(path: String, target: Bitmap, left: Int, top: Int, right: Int, bottom: Int, budget: Long)
        external fun encode(image: Bitmap, path: String, format: String, quality: Int, lossless: Boolean, budget: Long)
    }

    /** Convert source-encoded samples to an sRGB import bitmap, preserving coverage alpha. */
    fun convertIcc(input: Bitmap, profile: ByteArray): Bitmap = convertColour(input, profile, 1, 13)

    /** RGB cICP data uses full-range samples; HDR is tone-mapped to the SDR editor. */
    fun convertCicp(input: Bitmap, primaries: Int, transfer: Int): Bitmap = convertColour(input, null, primaries, transfer)

    /** PNG gAMA/cHRM conversion when no higher-priority profile is present. */
    fun convertPngColour(input: Bitmap, gamma: Float, chromaticities: FloatArray?): Bitmap {
        val output = Bitmap.createBitmap(input.width, input.height, Bitmap.Config.ARGB_8888)
        try {
            Native.convertPngColour(input, output, gamma, chromaticities)
            return output
        } catch (error: Throwable) {
            output.recycle()
            throw error
        }
    }

    private fun convertColour(input: Bitmap, profile: ByteArray?, primaries: Int, transfer: Int): Bitmap {
        val output = Bitmap.createBitmap(input.width, input.height, Bitmap.Config.ARGB_8888)
        try {
            Native.convertColour(input, output, profile, primaries, transfer)
            return output
        } catch (error: Throwable) {
            output.recycle()
            throw error
        }
    }

    /** Inspect ISO BMFF file brands, including compatible brands, rather than the filename. */
    fun isHeif(file: File): Boolean = file.inputStream().use { input ->
        val header = ByteArray(4096)
        val count = input.read(header)
        if (count < 16 || String(header, 4, 4, Charsets.US_ASCII) != "ftyp") return@use false
        val boxSize = ((header[0].toLong() and 255) shl 24) or ((header[1].toLong() and 255) shl 16) or
            ((header[2].toLong() and 255) shl 8) or (header[3].toLong() and 255)
        val end = minOf(count.toLong(), boxSize).toInt()
        (8..end - 4 step 4).any { offset ->
            offset != 12 && String(header, offset, 4, Charsets.US_ASCII) in setOf(
                "heic", "heix", "hevc", "hevx", "heim", "heis", "hevm", "hevs", "mif1", "msf1", "avif", "avis"
            )
        }
    }

    fun dimensions(file: File): ImageDimensions = Native.info(file.path).let { ImageDimensions(it[0], it[1]) }

    /** Native estimate includes codec work buffers and source tile size, even when output is smaller. */
    fun decodeWorkingBytes(file: File, size: ImageDimensions): Long {
        val dimensions = Native.info(file.path)
        val tilePixels = dimensions[2].toLong() * dimensions[3]
        val outputPixels = size.width.toLong() * size.height
        val reserve = 32L * 1024 * 1024
        if (outputPixels > (Long.MAX_VALUE - reserve) / 4) return Long.MAX_VALUE
        val outputBytes = outputPixels * 4 + reserve
        if (tilePixels > (Long.MAX_VALUE - outputBytes) / 32) return Long.MAX_VALUE
        return tilePixels * 32 + outputBytes
    }

    fun decode(file: File, size: ImageDimensions, budget: Long, crop: Rect? = null): Bitmap {
        if (decodeWorkingBytes(file, size) > budget) throw OutOfMemoryError("HEIC/AVIF decoding exceeds the available image memory budget")
        val output = Bitmap.createBitmap(size.width, size.height, Bitmap.Config.ARGB_8888)
        try {
            Native.decode(file.path, output, crop?.left ?: 0, crop?.top ?: 0, crop?.right ?: -1, crop?.bottom ?: -1, budget)
            return output
        } catch (error: Throwable) {
            output.recycle()
            throw error
        }
    }

    /** HEIC uses quality; AVIF additionally supports exact opaque RGB lossless coding. */
    fun encode(image: Bitmap, file: File, format: String, quality: Int, lossless: Boolean, budget: Long) {
        require(format == "heic" || format == "avif")
        require(!lossless || format == "avif")
        Native.encode(image, file.path, format, quality.coerceIn(1, 100), lossless, budget)
    }
}
