/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Intent
import android.os.Bundle
import android.util.AtomicFile
import org.json.JSONObject
import java.io.File
import java.util.UUID

/** Durable accepted attribution and a separate unfinished field. Tokens never encode filesystem paths. */
internal class CreditEditSession private constructor(private val directory: File, val token: String,
    var credits: List<ImageCredit>, private var context: CreditEditContext,
    var draft: GalleryCredits.EditorDraft?=null, var accepted: Boolean=false, var revision: Long=0, var acceptedSnapshot: String?=null, var edits: List<ImageCredit> = emptyList()) {
    private val atomic get()=AtomicFile(resolve(directory,token))
    private val lock get()=locks.getOrPut(resolve(directory,token).absolutePath) {Any()}
    fun validateEdit(source: String,text: String) {context.edited(listOf(ImageCredit(source,text)))}
    data class AdoptionReceipt(val revision: Long,val snapshotToken: String)
    val adoptionReceipt: AdoptionReceipt? get()=acceptedSnapshot?.let {AdoptionReceipt(revision,it)}
    fun edit(source: String,text: String,retainAccepted: (List<ImageCredit>)->String) = synchronized(lock) {
        val nextContext=context.edited(listOf(ImageCredit(source,text)))
        val nextCredits=credits.map {if(it.source==source) it.copy(text=text) else it}
        val nextDraft=GalleryCredits.EditorDraft(source,text)
        val nextEdits=(edits.filter {it.source!=source}+ImageCredit(source,text))
        val snapshotToken=retainAccepted(nextCredits)
        write(nextCredits,nextContext,nextDraft,true,revision+1,snapshotToken=snapshotToken,changedCredits=nextEdits) // Durability precedes any Saved/Copy/RESULT_OK signal.
        credits=nextCredits;context=nextContext;draft=nextDraft;accepted=true;revision++;acceptedSnapshot=snapshotToken;edits=nextEdits
        Unit
    }
    fun saveDraft(value: GalleryCredits.EditorDraft?) = synchronized(lock) {
        val adopted=write(credits,context,value,accepted,revision);draft=value
        if(value==null && accepted && adopted>=revision) atomic.delete()
    }
    private fun write(values: List<ImageCredit>,constraints: CreditEditContext,field: GalleryCredits.EditorDraft?,saved: Boolean,
        nextRevision: Long=revision,adoptedOverride: Long?=null,snapshotToken: String?=acceptedSnapshot,changedCredits: List<ImageCredit> = edits): Long {
        // An autosave worker can mark adoption while the dialog remains open. Preserve that
        // receipt when later raw-field snapshots are written from the UI instance.
        val existing=resolve(directory,token)
        val previousAdopted=if(existing.isFile || File(existing.path+".bak").isFile)
            atomic.openRead().bufferedReader(Charsets.UTF_8).use {JSONObject(it.readText()).optLong("adopted_revision",-1)} else -1
        val adopted=maxOf(previousAdopted,adoptedOverride ?: -1)

        val json=JSONObject().put("version",1).put("credits",ImageCredit.write(values))
            .put("context",constraints.json()).put("accepted",saved).put("revision",nextRevision).put("adopted_revision",adopted).put("accepted_snapshot",snapshotToken).put("edits",ImageCredit.write(changedCredits))
        field?.let {json.put("draft",JSONObject().put("source",it.source).put("text",it.text))}
        val output=atomic.startWrite()
        try {output.write(json.toString().toByteArray(Charsets.UTF_8));atomic.finishWrite(output)}
        catch(error: Throwable) {atomic.failWrite(output);throw error}
        return adopted
    }
    fun result()=Intent().putExtra(EXTRA_SESSION,token).apply {
        val encoded=ImageCredit.write(credits).toString()
        if(inline(encoded)) putExtra("document_image_credits",encoded)
    }
    fun saveState(state: Bundle) {
        state.remove("document_image_credits")
        state.remove("image_credit_editor_source");state.remove("image_credit_editor_draft")
        state.putString(EXTRA_SESSION,token)
        state.putBoolean("document_image_credits_edited",accepted)
        val encoded=ImageCredit.write(credits).toString()
        if(inline(encoded)) state.putString("document_image_credits",encoded)
        draft?.let {
            if(inline(JSONObject().put("source",it.source).put("text",it.text).toString())) {
                state.putString("image_credit_editor_source",it.source)
                state.putString("image_credit_editor_draft",it.text)
            }
        }
    }
    fun representedBy(metadata: JSONObject,history: RasterHistory.Snapshot): Boolean {
        val state=metadata.optJSONObject("image_credits")
        val written=(ImageCredit.read(state?.optJSONArray("committed"))+ImageCredit.read(state?.optJSONArray("floating"))+
            (history.undo+history.redo).flatMap {it.imageCredits}).toSet()
        return credits.all {it in written}
    }
    /** Only call for explicit discard, or after these accepted credits are durably adopted. */
    fun discard() = synchronized(lock) {atomic.delete()}
    fun retireAfterAdoption(expectedRevision: Long): Boolean = synchronized(lock) {
        val current=open(directory,token)
        if(current.revision!=expectedRevision) return@synchronized false
        if(current.draft==null) atomic.delete()
        else current.write(current.credits,current.context,current.draft,current.accepted,current.revision,expectedRevision)
        true // A raw draft survives. Explicit dismissal can clean it once this revision is adopted.
    }
    companion object {
        const val EXTRA_SESSION="image_credit_session"
        const val INLINE_BYTES=16*1024 // Transport/offload threshold only, never an acceptance limit.
        private val locks=java.util.concurrent.ConcurrentHashMap<String,Any>()
        private val valid=Regex("credit-edit-[0-9a-f-]{36}\\.json")
        fun inline(text: String)=text.toByteArray(Charsets.UTF_8).size<=INLINE_BYTES
        private fun resolve(directory: File,token: String): File {
            require(valid.matches(token))
            return File(directory,token)
        }
        fun create(directory: File,credits: List<ImageCredit>,context: CreditEditContext): CreditEditSession {
            val result=CreditEditSession(directory,"credit-edit-${UUID.randomUUID()}.json",credits,context)
            result.write(credits,context,null,false)
            return result
        }
        fun open(directory: File,token: String): CreditEditSession = synchronized(locks.getOrPut(resolve(directory,token).absolutePath) {Any()}) {
            val json=AtomicFile(resolve(directory,token)).openRead().bufferedReader(Charsets.UTF_8).use {JSONObject(it.readText())}
            require(json.getInt("version")==1)
            CreditEditSession(directory,token,ImageCredit.read(json.getJSONArray("credits")),
                CreditEditContext.read(json.getJSONObject("context")),json.optJSONObject("draft")?.let {
                    GalleryCredits.EditorDraft(it.getString("source"),it.getString("text"))
                },json.optBoolean("accepted"),json.optLong("revision"),json.optString("accepted_snapshot").takeIf {it.isNotEmpty()},ImageCredit.read(json.optJSONArray("edits")))
        }
    }
}
