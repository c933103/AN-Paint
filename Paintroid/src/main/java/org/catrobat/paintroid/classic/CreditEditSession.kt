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
    var draft: GalleryCredits.EditorDraft?=null, var accepted: Boolean=false, var revision: Long=0, var acceptedSnapshot: String?=null, var edits: List<ImageCredit> = emptyList(), private var omittedDraft: Boolean=false) {
    private val atomic get()=AtomicFile(resolve(directory,token))
    private val lock get()=locks.getOrPut(resolve(directory,token).absolutePath) {Any()}
    val hasDraft: Boolean get()=draft!=null || omittedDraft
    private fun validatedContext(source: String,text: String): CreditEditContext {
        // A text alone larger than the existing drawing envelope cannot become a valid edit.
        // Refuse before prospective JSON copies; this is the format's existing limit.
        require(CreditSessionJson.fitsInline(text,AutosaveStore.MAX_METADATA_BYTES))
        return context.edited(listOf(ImageCredit(source,text)))
    }
    fun validateEdit(source: String,text: String) {CreditSessionJson.withResources {validatedContext(source,text)}}
    data class AdoptionReceipt(val revision: Long,val snapshotToken: String)
    val adoptionReceipt: AdoptionReceipt? get()=acceptedSnapshot?.let {AdoptionReceipt(revision,it)}
    fun edit(source: String,text: String,retainAccepted: (List<ImageCredit>)->String) = synchronized(lock) {CreditSessionJson.withResources {
        val nextContext=validatedContext(source,text)
        val nextCredits=credits.map {if(it.source==source) it.copy(text=text) else it}
        val nextDraft=GalleryCredits.EditorDraft(source,text)
        val nextEdits=(edits.filter {it.source!=source}+ImageCredit(source,text))
        val snapshotToken=retainAccepted(nextCredits)
        write(nextCredits,nextContext,nextDraft,true,revision+1,snapshotToken=snapshotToken,changedCredits=nextEdits) // Durability precedes any Saved/Copy/RESULT_OK signal.
        credits=nextCredits;context=nextContext;draft=nextDraft;accepted=true;revision++;acceptedSnapshot=snapshotToken;edits=nextEdits
        Unit
    }}
    fun saveDraft(value: GalleryCredits.EditorDraft?) = synchronized(lock) {CreditSessionJson.withResources {
        val adopted=write(credits,context,value,accepted,revision);draft=value;omittedDraft=false
        if(value==null && accepted && adopted>=revision) atomic.delete()
    }}
    private fun write(values: List<ImageCredit>,constraints: CreditEditContext,field: GalleryCredits.EditorDraft?,saved: Boolean,
        nextRevision: Long=revision,adoptedOverride: Long?=null,snapshotToken: String?=acceptedSnapshot,changedCredits: List<ImageCredit> = edits): Long = CreditSessionJson.withResources {
        // An autosave worker can mark adoption while the dialog remains open. Preserve that
        // receipt when later raw-field snapshots are written from the UI instance.
        val existing=resolve(directory,token)
        val previousAdopted=if(existing.isFile || File(existing.path+".bak").isFile)
            CreditSessionJson.receipt(atomic).optLong("adopted_revision",-1) else -1
        val adopted=maxOf(previousAdopted,adoptedOverride ?: -1)

        val json=JSONObject().put("version",1).put("credits",ImageCredit.write(values))
            .put("context",constraints.json()).put("accepted",saved).put("revision",nextRevision).put("adopted_revision",adopted).put("accepted_snapshot",snapshotToken).put("edits",ImageCredit.write(changedCredits))
        field?.let {json.put("draft",JSONObject().put("source",it.source).put("text",it.text))}
        CreditSessionJson.write(atomic,directory,json)
        adopted
    }
    fun result()=Intent().putExtra(EXTRA_SESSION,token).apply {
        try {CreditSessionJson.withResources {
            val values=ImageCredit.write(credits)
            if(CreditSessionJson.fitsInline(values,INLINE_BYTES)) putExtra("document_image_credits",values.toString())
        }} catch(_: java.io.IOException) { /* The durable token is authoritative. */ }
    }
    fun saveState(state: Bundle) {
        state.remove("document_image_credits")
        state.remove("image_credit_editor_source");state.remove("image_credit_editor_draft")
        state.putString(EXTRA_SESSION,token)
        state.putBoolean("document_image_credits_edited",accepted)
        try {CreditSessionJson.withResources {
        val values=ImageCredit.write(credits)
        if(CreditSessionJson.fitsInline(values,INLINE_BYTES)) state.putString("document_image_credits",values.toString())
        draft?.let {
            if(CreditSessionJson.fitsInline(JSONObject().put("source",it.source).put("text",it.text),INLINE_BYTES)) {
                state.putString("image_credit_editor_source",it.source)
                state.putString("image_credit_editor_draft",it.text)
            }
        }
        }} catch(_: java.io.IOException) {
            // Optional Binder copies are never required to reopen the private session.
            state.remove("document_image_credits")
            state.remove("image_credit_editor_source");state.remove("image_credit_editor_draft")
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
        val current=CreditSessionJson.receipt(atomic)
        require(current.getInt("version")==1)
        if(current.optLong("revision")!=expectedRevision) return@synchronized false
        if(!current.optBoolean("has_draft")) atomic.delete()
        else CreditSessionJson.adopt(atomic,directory,maxOf(expectedRevision,current.optLong("adopted_revision",-1)))
        true // A raw draft survives. Explicit dismissal can clean it once this revision is adopted.
    }
    companion object {
        const val EXTRA_SESSION="image_credit_session"
        const val INLINE_BYTES=16*1024 // Transport/offload threshold only, never an acceptance limit.
        private val locks=java.util.concurrent.ConcurrentHashMap<String,Any>()
        private val valid=Regex("credit-edit-[0-9a-f-]{36}\\.json")
        fun inline(text: String)=CreditSessionJson.fitsInline(text,INLINE_BYTES)
        private fun resolve(directory: File,token: String): File {
            require(valid.matches(token))
            return File(directory,token)
        }
        fun create(directory: File,credits: List<ImageCredit>,context: CreditEditContext): CreditEditSession = CreditSessionJson.withResources {
            val result=CreditEditSession(directory,"credit-edit-${UUID.randomUUID()}.json",credits,context)
            result.write(credits,context,null,false)
            result
        }
        fun open(directory: File,token: String,restoreDraft: Boolean=true): CreditEditSession = synchronized(locks.getOrPut(resolve(directory,token).absolutePath) {Any()}) {CreditSessionJson.withResources {
            val json=CreditSessionJson.read(AtomicFile(resolve(directory,token)),if(restoreDraft)null else
                setOf("version","credits","context","accepted","revision","accepted_snapshot","edits"))
            require(json.getInt("version")==1)
            CreditEditSession(directory,token,ImageCredit.read(json.getJSONArray("credits")),
                CreditEditContext.read(json.getJSONObject("context")),json.optJSONObject("draft")?.let {
                    GalleryCredits.EditorDraft(it.getString("source"),it.getString("text"))
                },json.optBoolean("accepted"),json.optLong("revision"),json.optString("accepted_snapshot").takeIf {it.isNotEmpty()},ImageCredit.read(json.optJSONArray("edits")),!restoreDraft && json.optBoolean("has_draft"))
        }}
    }
}
