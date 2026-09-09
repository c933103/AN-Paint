/* Pocket Paint Local additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import java.io.*
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.util.UUID
import java.util.zip.Deflater
import java.util.zip.DeflaterOutputStream
import java.util.zip.InflaterInputStream

/** Lossless disk snapshots. The transfer buffer stays small at any image size. */
class RasterHistory(parent: File) : Closeable {
    data class Entry(val file: File, val width: Int, val height: Int)
    private val directory = File(parent, "session-${UUID.randomUUID()}")

    fun capture(bitmap: Bitmap): Entry {
        if (!directory.isDirectory && !directory.mkdirs()) throw IOException("Cannot create the undo cache. Free some device storage and try again.")
        val file = File.createTempFile("undo-", ".rgba", directory)
        val deflater = Deflater(Deflater.BEST_SPEED)
        try {
            DataOutputStream(DeflaterOutputStream(BufferedOutputStream(file.outputStream()), deflater)).use { out ->
                out.writeInt(0x50504c34); out.writeInt(bitmap.width); out.writeInt(bitmap.height)
                val bytes = ByteArray(32 * 1024)
                val integers = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN).asIntBuffer()
                val pixels = IntArray(bytes.size / 4)
                for (y in 0 until bitmap.height) {
                    var x = 0
                    while (x < bitmap.width) {
                        val count = minOf(pixels.size, bitmap.width - x)
                        bitmap.getPixels(pixels, 0, count, x, y, count, 1)
                        integers.clear(); integers.put(pixels, 0, count)
                        out.write(bytes, 0, count * 4); x += count
                    }
                }
            }
            return Entry(file, bitmap.width, bitmap.height)
        } catch (error: Throwable) {
            file.delete(); throw error
        } finally { deflater.end() }
    }

    fun restore(entry: Entry, current: Bitmap): Bitmap {
        // Validate the compressed stream before modifying the current image.
        // A reclaimed or damaged cache entry must not leave a partially restored canvas.
        read(entry, null)
        val output = if (current.width == entry.width && current.height == entry.height) current
            else Bitmap.createBitmap(entry.width, entry.height, Bitmap.Config.ARGB_8888)
        try { read(entry, output); return output }
        catch (error: Throwable) { if (output !== current) output.recycle(); throw error }
    }

    private fun read(entry: Entry, bitmap: Bitmap?) {
        DataInputStream(InflaterInputStream(BufferedInputStream(entry.file.inputStream()))).use { input ->
            if (input.readInt() != 0x50504c34 || input.readInt() != entry.width || input.readInt() != entry.height)
                throw IOException("The undo cache is damaged.")
            val bytes = ByteArray(32 * 1024)
            val integers = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN).asIntBuffer()
            val pixels = IntArray(bytes.size / 4)
            for (y in 0 until entry.height) {
                var x = 0
                while (x < entry.width) {
                    val count = minOf(pixels.size, entry.width - x)
                    input.readFully(bytes, 0, count * 4)
                    if (bitmap != null) {
                        integers.clear(); integers.get(pixels, 0, count)
                        bitmap.setPixels(pixels, 0, count, x, y, count, 1)
                    }
                    x += count
                }
            }
            if (input.read() != -1) throw IOException("Unexpected data in the undo cache.")
        }
    }

    fun discard(entry: Entry) { entry.file.delete() }
    override fun close() { directory.deleteRecursively() }
}
