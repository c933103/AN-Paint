/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import java.io.File
import java.io.IOException
import org.catrobat.paintroid.R

/** Text files containing a raster image, or an ASCII-art rendition of the current image. */
object TextImageCodec {
    fun inspect(file: File): Boolean = TextImageData.inspect(file)

    /** Source and destination may be the same file. The source closes before replacement. */
    fun decodeToFile(file: File, destination: File, maxBytes: Long) {
        replace(destination, "base64-input-") { temporary ->
            file.inputStream().use { input -> temporary.outputStream().buffered().use { output ->
                TextImageData.decode(input, output, maxBytes)
            } }
            val header = ByteArray(32)
            val count = temporary.inputStream().use { it.read(header) }
            if (count < 0 || !TextImageData.imageSignature(header.copyOf(count)))
                throw IOException(ui(R.string.formats22_text_not_image))
        }
    }

    fun encodeBase64(image: Bitmap, file: File, budget: Long) {
        requireBudget(image.allocationByteCount.toLong() + image.width.toLong()*8 + 1024*1024, budget)
        replace(file, "base64-export-") { temporary ->
            temporary.outputStream().buffered().use { output ->
                output.write("data:image/png;base64,".toByteArray(Charsets.US_ASCII))
                val encoded = TextImageData.Base64Output(output)
                if (!image.compress(Bitmap.CompressFormat.PNG, 100, encoded))
                    throw IOException(ui(R.string.ui_the_encoder_did_not_finish))
                encoded.finish()
                output.write('\n'.code)
            }
        }
    }

    fun encodeAscii(image: Bitmap, file: File, columns: Int, invert: Boolean, budget: Long) {
        val rows = TextImageData.asciiRows(image.width, image.height, columns)
        requireBudget(image.allocationByteCount.toLong() + columns.toLong()*rows*4 + columns*8L + 1024*1024, budget)
        val scaled = Bitmap.createScaledBitmap(image, columns, rows, true)
        try {
            replace(file, "ascii-export-") { temporary ->
                temporary.outputStream().buffered().use { output ->
                    TextImageData.ascii(columns, rows, TextImageData.Rows { y, row ->
                        scaled.getPixels(row, 0, columns, 0, y, columns, 1)
                    }, output, invert)
                }
            }
        } finally { if (scaled !== image) scaled.recycle() }
    }

    private fun requireBudget(required: Long, budget: Long) {
        if (required > budget) throw IOException(ui(R.string.save20_encoding_budget))
    }
    private fun replace(destination: File, prefix: String, write: (File) -> Unit) {
        val temporary = File.createTempFile(prefix, ".tmp", destination.absoluteFile.parentFile)
        try {
            write(temporary)
            if (!temporary.renameTo(destination)) throw IOException(ui(R.string.save20_destination_error))
        } finally { temporary.delete() }
    }
}
