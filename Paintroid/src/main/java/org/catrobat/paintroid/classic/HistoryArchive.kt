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
    const val MAX_INDEX_BYTES = 4 * 1024 * 1024
    fun manifest(snapshot: RasterHistory.Snapshot): JSONObject {
        val credits=(snapshot.undo+snapshot.redo).flatMap {it.imageCredits}.distinct()
        val creditIndex=credits.withIndex().associate {it.value to it.index}
        return JSONObject().put("version",1).put("image_credit_catalog",ImageCredit.write(credits)).apply {
            for((name,stack) in listOf("undo" to snapshot.undo,"redo" to snapshot.redo)) {
                require(stack.size<=32768) { ui(org.catrobat.paintroid.R.string.ui_invalid_autosave_metadata) }
                put(name,JSONArray().apply {stack.forEach {entry ->
                    put(JSONObject().put("width",entry.width).put("height",entry.height).put("sha256","0".repeat(64))
                        .put("image_credits",JSONArray(entry.imageCredits.map {creditIndex.getValue(it)})))
                }})
            }
        }
    }
    fun validate(snapshot: RasterHistory.Snapshot) = validateManifest(manifest(snapshot))
    fun validateManifest(manifest: JSONObject) {
        require(manifest.getInt("version")==1)
        require(manifest.getJSONArray("undo").length()<=32768 && manifest.getJSONArray("redo").length()<=32768)
        require(manifest.toString().toByteArray(Charsets.UTF_8).size<=MAX_INDEX_BYTES) {
            ui(org.catrobat.paintroid.R.string.ui_invalid_autosave_metadata)
        }
    }
    private fun hex(bytes: ByteArray)=bytes.joinToString("") {"%02x".format(it.toInt() and 255)}
    fun write(zip: ZipOutputStream,snapshot: RasterHistory.Snapshot) {
        validate(snapshot)
        val manifest=manifest(snapshot)
        for((name,stack) in listOf("undo" to snapshot.undo,"redo" to snapshot.redo)) {
            val entries=manifest.getJSONArray(name)
            stack.forEachIndexed {index,entry ->
                val path="history/$name/$index.rgba"
                val digest=MessageDigest.getInstance("SHA-256")
                zip.putNextEntry(ZipEntry(path))
                entry.file.inputStream().buffered().use {input ->
                    val buffer=ByteArray(32768)
                    while(true) {val n=input.read(buffer);if(n<0)break;zip.write(buffer,0,n);digest.update(buffer,0,n)}
                }
                zip.closeEntry()
                entries.getJSONObject(index).put("sha256",hex(digest.digest()))
            }
        }
        zip.putNextEntry(ZipEntry("history/index.json"));zip.write(manifest.toString().toByteArray(Charsets.UTF_8));zip.closeEntry()
    }
    fun read(zip: ZipFile,history: RasterHistory): RasterHistory.Snapshot {
        val index=zip.getEntry("history/index.json") ?: return RasterHistory.Snapshot()
        if(index.size !in 1..MAX_INDEX_BYTES.toLong()) throw IOException("Invalid draft history index")
        val manifest=zip.getInputStream(index).use {JSONObject(BoundedJson.read(it,MAX_INDEX_BYTES))}
        require(manifest.getInt("version")==1)
        val credits=ImageCredit.read(manifest.optJSONArray("image_credit_catalog"),deduplicate=false)
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
                    }.also {imported.add(it)}.let {snapshot ->
                        val refs=info.optJSONArray("image_credits")
                        snapshot.copy(imageCredits=if(refs==null) emptyList() else (0 until refs.length()).map {credits[refs.getInt(it)]})
                    }
                }
            }
            return RasterHistory.Snapshot(stack("undo"),stack("redo"))
        } catch(error: Throwable) {imported.forEach {history.discard(it)};throw error}
    }
}
