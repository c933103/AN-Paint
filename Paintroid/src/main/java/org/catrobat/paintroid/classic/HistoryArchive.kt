/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.security.MessageDigest
import java.util.zip.ZipEntry
import java.util.zip.ZipFile
import java.util.zip.ZipOutputStream

/** Both ordered stacks travel in the same atomic transaction as the canvas and floating selection. */
internal object HistoryArchive {
    private fun hex(bytes: ByteArray)=bytes.joinToString("") {"%02x".format(it.toInt() and 255)}
    fun write(zip: ZipOutputStream,snapshot: RasterHistory.Snapshot) {
        val manifest=JSONObject().put("version",1)
        for((name,stack) in listOf("undo" to snapshot.undo,"redo" to snapshot.redo)) {
            val entries=JSONArray()
            stack.forEachIndexed {index,entry ->
                val path="history/$name/$index.rgba"
                val digest=MessageDigest.getInstance("SHA-256")
                zip.putNextEntry(ZipEntry(path))
                entry.file.inputStream().buffered().use {input ->
                    val buffer=ByteArray(32768)
                    while(true) {val n=input.read(buffer);if(n<0)break;zip.write(buffer,0,n);digest.update(buffer,0,n)}
                }
                zip.closeEntry()
                entries.put(JSONObject().put("width",entry.width).put("height",entry.height).put("sha256",hex(digest.digest())))
            }
            manifest.put(name,entries)
        }
        zip.putNextEntry(ZipEntry("history/index.json"));zip.write(manifest.toString().toByteArray(Charsets.UTF_8));zip.closeEntry()
    }
    fun read(zip: ZipFile,history: RasterHistory): RasterHistory.Snapshot {
        val index=zip.getEntry("history/index.json") ?: return RasterHistory.Snapshot()
        if(index.size !in 1..4L*1024*1024) throw IOException("Invalid draft history index")
        val manifest=zip.getInputStream(index).use {JSONObject(it.bufferedReader().readText())}
        require(manifest.getInt("version")==1)
        val imported=mutableListOf<RasterHistory.Entry>()
        try {
            fun stack(name: String): List<RasterHistory.Entry> {
                val entries=manifest.getJSONArray(name)
                require(entries.length()<=32768)
                return (0 until entries.length()).map {n ->
                    val info=entries.getJSONObject(n)
                    val entry=zip.getEntry("history/$name/$n.rgba") ?: throw IOException("Draft history entry is missing")
                    zip.getInputStream(entry).use {input ->
                        history.importSnapshot(input,info.getInt("width"),info.getInt("height"),info.getString("sha256"))
                    }.also {imported.add(it)}
                }
            }
            return RasterHistory.Snapshot(stack("undo"),stack("redo"))
        } catch(error: Throwable) {imported.forEach {history.discard(it)};throw error}
    }
}
