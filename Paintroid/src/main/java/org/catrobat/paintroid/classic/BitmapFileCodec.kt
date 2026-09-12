/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import org.catrobat.paintroid.R
import java.io.File
import java.io.IOException

/** Streaming BMP/GIF exports replace a destination only after encoding succeeds. */
object BitmapFileCodec {
    fun encode(image: Bitmap, file: File, gif: Boolean, dither: Boolean, budget: Long) {
        val temporary = File.createTempFile("bitmap-export-", ".tmp", file.absoluteFile.parentFile)
        try {
            temporary.outputStream().buffered().use { output ->
                val rows = LegacyImageEncoder.Rows { y, row -> image.getPixels(row, 0, image.width, 0, y, image.width, 1) }
                if (gif) LegacyImageEncoder.gif(image.width, image.height, rows, output, budget, dither)
                else LegacyImageEncoder.bmp(image.width, image.height, rows, output, budget)
            }
            if (!temporary.renameTo(file)) throw IOException(ui(R.string.save20_destination_error))
        } catch (error: LegacyImageEncoder.Failure) {
            throw IOException(ui(when(error.reason) {
                1 -> R.string.save20_bmp_size_limit
                2 -> R.string.save20_gif_size_limit
                else -> R.string.save20_encoding_budget
            }),error)
        } finally { temporary.delete() }
    }
}
