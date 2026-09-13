/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import org.catrobat.paintroid.R
import java.io.File
import java.io.IOException

/** Packed Windows DIB import/export, using private scoped BMP wrappers for Android decoding. */
object DibCodec {
    fun isDib(file: File): Boolean = PackedDib.isDib(file)

    fun <T> withBmpFile(file: File, block: (File) -> T): T {
        if (!isDib(file)) return block(file)
        val temporary = File.createTempFile("dib-input-", ".bmp", file.absoluteFile.parentFile)
        try {
            try {
                temporary.outputStream().buffered().use { PackedDib.toBmp(file, it) }
                LegacyColourMetadata.check(temporary)
            } catch (error: LegacyColourMetadata.UnsupportedColour) {
                throw IOException(ui(R.string.save20_unsupported_tagged_colour), error)
            }
            return block(temporary)
        } finally { temporary.delete() }
    }

    fun encode(image: Bitmap, file: File, budget: Long) {
        val temporary = File.createTempFile("dib-export-", ".tmp", file.absoluteFile.parentFile)
        try {
            temporary.outputStream().buffered().use { output ->
                val rows = LegacyImageEncoder.Rows { y, row -> image.getPixels(row, 0, image.width, 0, y, image.width, 1) }
                LegacyImageEncoder.dib(image.width, image.height, rows, output, budget)
            }
            if (!temporary.renameTo(file)) throw IOException(ui(R.string.save20_destination_error))
        } catch (error: LegacyImageEncoder.Failure) {
            if (error.reason == 1) throw IOException(ui(R.string.formats22_dib_size_limit), error)
            throw IOException(ui(R.string.save20_encoding_budget), error)
        } finally { temporary.delete() }
    }
}
