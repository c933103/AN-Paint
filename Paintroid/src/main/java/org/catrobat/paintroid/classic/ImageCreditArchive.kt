/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.util.AtomicFile
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.util.UUID
import java.security.MessageDigest

/** Durable unassociated credits, never an implicit replacement for a document ledger. */
internal object ImageCreditArchive {
    data class Record(val token: String,val credit: ImageCredit,val origins: Set<String>)
    data class Contents(val records: List<Record>,val unreadableSnapshots: Int)
    private val lock=Any()
    private val validToken=Regex("[0-9a-f]{64}")
    private fun directory(context: Context)=File(context.filesDir,"retained-image-credits")
    private fun file(context: Context,token: String)=File(directory(context),"$token.json")

    /** Each confirmed edit gets an immutable token. An older autosave cannot release a newer one. */
    fun retainAccepted(context: Context,credits: List<ImageCredit>): String = synchronized(lock) {
        val directory=directory(context)
        if(!directory.isDirectory && !directory.mkdirs()) throw IOException("Cannot retain image credits")
        val token=UUID.randomUUID().toString().replace("-","")+UUID.randomUUID().toString().replace("-","")
        val atomic=AtomicFile(file(context,token))
        val bytes=JSONObject().put("version",1).put("credits",ImageCredit.write(credits))
            .toString().toByteArray(Charsets.UTF_8)
        val stream=atomic.startWrite()
        try {stream.write(bytes);atomic.finishWrite(stream)}
        catch(error: Throwable) {atomic.failWrite(stream);throw error}
        token
    }

    /** Caller must first establish that this exact accepted snapshot was adopted durably. */
    fun releaseAccepted(context: Context,token: String): Unit = synchronized(lock) {
        if(validToken.matches(token)) AtomicFile(file(context,token)).delete()
        Unit
    }

    /** Hash exact UTF-16 code units, including lone surrogates, without a large UTF-8 copy. */
    fun selectionToken(credit: ImageCredit): String {
        val digest=MessageDigest.getInstance("SHA-256")
        fun append(value: String) {
            for(shift in listOf(24,16,8,0))digest.update((value.length ushr shift).toByte())
            for(character in value) {
                digest.update((character.code ushr 8).toByte());digest.update(character.code.toByte())
            }
        }
        append(credit.source);append(credit.text)
        return digest.digest().joinToString("") {"%02x".format(it.toInt() and 255)}
    }

    private fun tokens(context: Context)=directory(context).listFiles().orEmpty()
        .map {it.name.removeSuffix(".bak")}
        .filter {it.endsWith(".json") && validToken.matches(it.removeSuffix(".json"))}
        .map {it.removeSuffix(".json")}.distinct().sorted()

    fun contents(context: Context): Contents = synchronized(lock) {
        val origins=linkedMapOf<ImageCredit,MutableSet<String>>()
        fun add(credit: ImageCredit,origin: String) {origins.getOrPut(credit) {linkedSetOf()}.add(origin)}
        LegacyImageCredits.read(context).forEach {add(it,"legacy:"+LegacyImageCredits.sourceToken(it.source))}
        var unreadable=0
        for(token in tokens(context)) {
            try {
                val snapshot=AtomicFile(file(context,token)).openRead().bufferedReader(Charsets.UTF_8)
                    .use {JSONObject(it.readText())}
                require(snapshot.getInt("version")==1)
                val values=snapshot.getJSONArray("credits")
                val records=(0 until values.length()).map {index ->
                    val value=values.getJSONObject(index)
                    // Do not deduplicate by source or regenerate empty text. Separate accepted
                    // snapshots can contain different approved versions of the same source.
                    val credit=ImageCredit(value.getString("source"),value.getString("text"))
                    credit to "accepted:$token:$index"
                }
                records.forEach {(credit,origin) ->add(credit,origin)}
            } catch(_: Exception) {
                // Keep the original file untouched and surface incomplete recovery in the UI.
                unreadable++
            }
        }
        Contents(origins.map {(credit,receipts) ->Record(selectionToken(credit),credit,receipts.toSet())},unreadable)
    }

    fun records(context: Context): List<Record> = contents(context).records

    fun hasRecords(context: Context): Boolean = synchronized(lock) {
        LegacyImageCredits.hasRecords(context) || tokens(context).isNotEmpty()
    }

    fun find(context: Context,token: String?): ImageCredit? {
        if(token==null || !validToken.matches(token))return null
        return records(context).singleOrNull {it.token==token}?.credit
    }
}
