/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.AtomicFile
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.util.zip.ZipEntry
import java.util.zip.ZipFile
import java.util.zip.ZipOutputStream

data class AutosaveDraft(val image: Bitmap, val floating: Bitmap?, val metadata: JSONObject)

/** One atomic draft contains pixels and their matching metadata. Sources are never overwritten. */
class AutosaveStore(directory: File) {
    companion object { private val lock=Any() }
    val file = File(directory,"classic-autosave.zip")
    private val atomic = AtomicFile(file)
    fun exists() = file.isFile || File(file.path+".bak").isFile

    /** Move an unreadable draft aside before allowing a new autosave to replace its name. */
    fun preserveForRecovery(): File = synchronized(lock) {
        try { atomic.openRead().close() } catch (_: IOException) { }
        val source=File(file.path+".bak").takeIf { it.isFile } ?: file
        val target=File(file.parentFile,"classic-draft-recovery-${System.currentTimeMillis()}-${java.util.UUID.randomUUID()}.zip")
        if (!source.isFile || !source.renameTo(target)) throw IOException(ui(R.string.ui_the_previous_draft_could_not_be_moved_to))
        target
    }
    fun recoveryCopies(): List<File> = file.parentFile?.listFiles()?.filter {
        it.isFile && it.name.startsWith("classic-draft-recovery-") && it.extension=="zip"
    }?.sortedByDescending { it.lastModified() } ?: emptyList()

    fun write(image: Bitmap, floating: Bitmap?, metadata: JSONObject) = synchronized(lock) {
        val stream=atomic.startWrite()
        try {
            val zip=ZipOutputStream(stream).apply { setLevel(0) }
            fun entry(name: String, action: () -> Unit) {
                zip.putNextEntry(ZipEntry(name)); action(); zip.closeEntry()
            }
            entry("draft.json") { zip.write(metadata.toString().toByteArray(Charsets.UTF_8)) }
            entry("canvas.png") { if (!image.compress(Bitmap.CompressFormat.PNG,100,zip)) throw IOException(ui(R.string.ui_autosave_image_encoding_failed)) }
            if (floating != null) entry("floating.png") {
                if (!floating.compress(Bitmap.CompressFormat.PNG,100,zip)) throw IOException(ui(R.string.ui_autosave_selection_encoding_failed))
            }
            zip.finish(); zip.flush(); atomic.finishWrite(stream)
        } catch (error: Throwable) { atomic.failWrite(stream); throw error }
    }

    fun read(checkSize: (Int,Int) -> Unit): AutosaveDraft = synchronized(lock) {
        atomic.openRead().close() // Recover the previous complete transaction after an interrupted write.
        var image: Bitmap?=null; var floating: Bitmap?=null
        try {
            ZipFile(file).use { zip ->
                val entry=zip.getEntry("draft.json") ?: throw IOException(ui(R.string.ui_autosave_metadata_is_missing))
                require(entry.size in 1..262144) { ui(R.string.ui_invalid_autosave_metadata) }
                val metadata=zip.getInputStream(entry).use { JSONObject(it.bufferedReader().readText()) }
                require(metadata.getInt("version")==1)
                fun decode(name: String): Bitmap {
                    val e=zip.getEntry(name) ?: throw IOException(ui(R.string.ui_autosave_pixels_are_missing))
                    val bounds=BitmapFactory.Options().apply { inJustDecodeBounds=true }
                    zip.getInputStream(e).use { BitmapFactory.decodeStream(it,null,bounds) }
                    checkSize(bounds.outWidth,bounds.outHeight)
                    return zip.getInputStream(e).use {
                        BitmapFactory.decodeStream(it,null,BitmapFactory.Options().apply { inMutable=true; inScaled=false })
                    } ?: throw IOException(ui(R.string.ui_autosave_pixels_could_not_be_read))
                }
                image=decode("canvas.png")
                if (metadata.has("floating_rect")) floating=decode("floating.png")
                return AutosaveDraft(image!!,floating,metadata)
            }
        } catch (error: Throwable) { image?.recycle(); floating?.recycle(); throw error }
    }
}
