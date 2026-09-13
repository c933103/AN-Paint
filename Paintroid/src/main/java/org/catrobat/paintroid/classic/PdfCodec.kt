/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Matrix
import android.graphics.Rect
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import org.catrobat.paintroid.R
import java.io.File
import java.io.IOException

/** Raster import through Android's PDF renderer (API 21+), with no bundled PDF engine.
 * Pages and crop coordinates use 144 dpi: one PDF point is two source pixels.
 * Call from a worker thread: opening a PDF may parse substantial document data.
 */
object PdfCodec {
    private class PdfImportException(message: String, cause: Throwable? = null) : IOException(message, cause)

    private const val PIXELS_PER_POINT = 2
    private const val MAX_PAGES = 4096
    private const val MAX_PAGE_POINTS = 500_000
    private const val MAX_FILE_BYTES = 512L * 1024 * 1024
    private const val RENDER_RESERVE = 32L * 1024 * 1024

    /** A filename or provider MIME type need not identify the copied input correctly. */
    fun isPdf(file: File): Boolean = file.inputStream().use { input ->
        // PDF readers accept a header within the first 1024 bytes.
        val header = ByteArray(1024)
        var count = 0
        while (count < header.size) {
            val read = input.read(header, count, header.size - count)
            if (read <= 0) break
            count += read
        }
        (0..count - 8).any { offset ->
            header[offset] == '%'.code.toByte() && header[offset + 1] == 'P'.code.toByte() &&
                header[offset + 2] == 'D'.code.toByte() && header[offset + 3] == 'F'.code.toByte() &&
                header[offset + 4] == '-'.code.toByte() && header[offset + 5] in '1'.code.toByte()..'2'.code.toByte() &&
                header[offset + 6] == '.'.code.toByte() && header[offset + 7] in '0'.code.toByte()..'9'.code.toByte()
        }
    }

    fun pageCount(file: File): Int = withRenderer(file) { checkedPageCount(it) }

    fun dimensions(file: File, pageIndex: Int = 0): ImageDimensions = withPage(file, pageIndex) { page ->
        pageDimensions(page)
    }

    /** Admission estimate includes output, document bytes and native rendering headroom.
     * PdfRenderer offers no native allocator limit; this is an estimate, not a hard
     * bound on PDFium's internal allocations for complex/embedded compressed objects.
     */
    fun decodeWorkingBytes(file: File, size: ImageDimensions, pageIndex: Int = 0): Long {
        dimensions(file, pageIndex) // Validate the selected page, without rasterizing it.
        return workingBytes(file, size)
    }

    /** Render a selected page/crop directly into its requested bitmap; never allocate
     * a full-page intermediate for assembly tiles. Crop edges use source pixel space.
     */
    fun decode(file: File, size: ImageDimensions, budget: Long, crop: Rect? = null, pageIndex: Int = 0): Bitmap {
        if (size.pixels > ImageMemoryPolicy.MAX_BITMAP_PIXELS || workingBytes(file, size) > budget)
            throw OutOfMemoryError(ui(R.string.formats22_pdf_memory))
        return withPage(file, pageIndex) { page ->
            val source = pageDimensions(page)
            val region = crop?.let { Rect(it) } ?: Rect(0, 0, source.width, source.height)
            if (region.left < 0 || region.top < 0 || region.right > source.width || region.bottom > source.height ||
                region.left >= region.right || region.top >= region.bottom)
                throw PdfImportException(ui(R.string.formats22_pdf_crop))
            val output = Bitmap.createBitmap(size.width, size.height, Bitmap.Config.ARGB_8888)
            try {
                output.density = Bitmap.DENSITY_NONE
                output.eraseColor(Color.WHITE)
                val scaleX = size.width.toFloat() / region.width()
                val scaleY = size.height.toFloat() / region.height()
                val transform = Matrix().apply {
                    setValues(floatArrayOf(
                        PIXELS_PER_POINT * scaleX, 0f, -region.left * scaleX,
                        0f, PIXELS_PER_POINT * scaleY, -region.top * scaleY,
                        0f, 0f, 1f))
                }
                page.render(output, null, transform, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                output.setHasAlpha(false)
                output
            } catch (error: Throwable) {
                output.recycle()
                throw error
            }
        }
    }

    private fun workingBytes(file: File, size: ImageDimensions): Long {
        val documentBytes = file.length()
        if (documentBytes <= 0 || documentBytes > MAX_FILE_BYTES)
            throw PdfImportException(ui(R.string.formats22_pdf_file_size))
        // Guard the pixel-byte multiplication before adding native/document work.
        if (size.pixels > (Long.MAX_VALUE - RENDER_RESERVE - documentBytes * 2) / 4) return Long.MAX_VALUE
        return size.pixels * 4 + documentBytes * 2 + RENDER_RESERVE
    }

    private fun pageDimensions(page: PdfRenderer.Page): ImageDimensions {
        val width = page.width
        val height = page.height
        if (width !in 1..MAX_PAGE_POINTS || height !in 1..MAX_PAGE_POINTS)
            throw PdfImportException(ui(R.string.formats22_pdf_dimensions))
        return ImageDimensions(width * PIXELS_PER_POINT, height * PIXELS_PER_POINT)
    }

    private fun checkedPageCount(renderer: PdfRenderer): Int = renderer.pageCount.also {
        if (it !in 1..MAX_PAGES) throw PdfImportException(ui(R.string.formats22_pdf_page_count, MAX_PAGES))
    }

    private fun <T> withPage(file: File, pageIndex: Int, action: (PdfRenderer.Page) -> T): T = withRenderer(file) { renderer ->
        val count = checkedPageCount(renderer)
        if (pageIndex !in 0 until count) throw PdfImportException(ui(R.string.formats22_pdf_page_index))
        val page = renderer.openPage(pageIndex)
        try { action(page) } finally { page.close() }
    }

    private fun <T> withRenderer(file: File, action: (PdfRenderer) -> T): T {
        if (file.length() !in 1..MAX_FILE_BYTES) throw PdfImportException(ui(R.string.formats22_pdf_file_size))
        if (!isPdf(file)) throw PdfImportException(ui(R.string.formats22_pdf_invalid))
        try {
            val descriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
            val renderer = try { PdfRenderer(descriptor) } catch (error: Throwable) {
                // Constructor failure does not give us a renderer to close.
                try { descriptor.close() } catch (closeError: Throwable) { error.addSuppressed(closeError) }
                throw error
            }
            // A successfully created renderer owns and closes its descriptor.
            try { return action(renderer) } finally { renderer.close() }
        } catch (error: SecurityException) {
            throw PdfImportException(ui(R.string.formats22_pdf_encrypted), error)
        } catch (error: IllegalArgumentException) {
            throw PdfImportException(ui(R.string.formats22_pdf_invalid), error)
        } catch (error: IOException) {
            // Keep our specific page/size messages; native failures get a usable explanation.
            if (error is PdfImportException) throw error
            throw PdfImportException(ui(R.string.formats22_pdf_invalid), error)
        }
    }
}
