/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.RectF
import org.catrobat.paintroid.R
import java.io.File
import java.io.IOException

/** PNG and classic DIB ICO import; one PNG icon image on export. */
object IcoCodec {
    private const val DECODE_SCRATCH = 24L * 1024 * 1024
    val exportEdges = listOf(16, 24, 32, 48, 64, 128, 256)

    fun isIco(file: File): Boolean = IcoContainer.isIco(file)

    private fun entry(file: File): IcoContainer.Entry = try { IcoContainer.best(file) }
    catch (error: LegacyColourMetadata.UnsupportedColour) {
        throw IOException(ui(R.string.save20_unsupported_tagged_colour), error)
    }

    fun dimensions(file: File): ImageDimensions = entry(file).let { ImageDimensions(it.width, it.height) }

    /** Covers bounded PNG metadata/conversion, the full source icon, ARGB rows and the target. */
    fun decodeWorkingBytes(file: File, size: ImageDimensions): Long {
        val source = dimensions(file)
        return DECODE_SCRATCH + source.pixels * 12 + size.pixels * 4
    }

    fun decode(file: File, size: ImageDimensions, budget: Long): Bitmap {
        val selected = entry(file)
        val source = ImageDimensions(selected.width, selected.height)
        if (size.width > source.width || size.height > source.height)
            throw IOException(ui(R.string.ui_choose_dimensions_no_larger_than_the_original))
        if (DECODE_SCRATCH + source.pixels * 12 + size.pixels * 4 > budget)
            throw IOException(ui(R.string.formats22_ico_decode_budget))
        if (selected.png) {
            val temporary = File.createTempFile("ico-input-", ".png", file.absoluteFile.parentFile)
            try {
                temporary.outputStream().buffered().use { IcoContainer.extractPng(file, selected, it) }
                val imported = ImportedImage(temporary, "icon.png")
                if (imported.dimensions != source) throw IOException(ui(R.string.formats22_ico_dimensions_error))
                return imported.decode(ImportPlan.create(source, size), budget)
            } finally { temporary.delete() }
        }
        val pixels = try { IcoContainer.decodeDib(file, selected) }
        catch (error: LegacyColourMetadata.UnsupportedColour) {
            throw IOException(ui(R.string.save20_unsupported_tagged_colour), error)
        }
        val decoded = Bitmap.createBitmap(source.width, source.height, Bitmap.Config.ARGB_8888)
        var output: Bitmap? = null
        try {
            decoded.density = Bitmap.DENSITY_NONE
            decoded.setHasAlpha(true)
            decoded.setPixels(pixels, 0, source.width, 0, 0, source.width, source.height)
            if (source == size) return decoded
            val target = Bitmap.createBitmap(size.width, size.height, Bitmap.Config.ARGB_8888)
            output = target
            target.density = Bitmap.DENSITY_NONE
            Canvas(target).drawBitmap(decoded, null, RectF(0f, 0f, size.width.toFloat(), size.height.toFloat()),
                Paint(Paint.FILTER_BITMAP_FLAG or Paint.ANTI_ALIAS_FLAG))
            decoded.recycle()
            return target.also { output = null }
        } catch (error: Throwable) {
            decoded.recycle()
            throw error
        } finally { output?.recycle() }
    }

    /** Fit the source into a square icon without stretching; unused space remains transparent. */
    fun encode(image: Bitmap, file: File, edge: Int, budget: Long) {
        if (edge !in exportEdges) throw IOException(ui(R.string.formats22_ico_invalid_size))
        val needed = image.allocationByteCount.toLong() + edge.toLong() * edge * 8 + 4L * 1024 * 1024
        if (needed > budget) throw IOException(ui(R.string.save20_encoding_budget))
        val temporary = File.createTempFile("ico-export-", ".tmp", file.absoluteFile.parentFile)
        var png: File? = null
        var icon: Bitmap? = null
        try {
            val pngFile = File.createTempFile("ico-payload-", ".png", file.absoluteFile.parentFile)
            png = pngFile
            val square = Bitmap.createBitmap(edge, edge, Bitmap.Config.ARGB_8888)
            icon = square
            square.density = Bitmap.DENSITY_NONE
            square.setHasAlpha(true)
            square.eraseColor(0)
            val scale = minOf(edge.toFloat() / image.width, edge.toFloat() / image.height)
            val width = image.width * scale
            val height = image.height * scale
            val left = (edge - width) / 2
            val top = (edge - height) / 2
            Canvas(square).drawBitmap(image, null, RectF(left, top, left + width, top + height),
                Paint(Paint.FILTER_BITMAP_FLAG or Paint.ANTI_ALIAS_FLAG))
            pngFile.outputStream().buffered().use {
                if (!square.compress(Bitmap.CompressFormat.PNG, 100, it))
                    throw IOException(ui(R.string.ui_the_encoder_did_not_finish))
            }
            temporary.outputStream().buffered().use { IcoContainer.writePng(pngFile, edge, edge, it) }
            if (!temporary.renameTo(file)) throw IOException(ui(R.string.save20_destination_error))
        } finally { icon?.recycle(); png?.delete(); temporary.delete() }
    }
}
