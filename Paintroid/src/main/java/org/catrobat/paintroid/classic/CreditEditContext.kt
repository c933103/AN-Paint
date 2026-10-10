/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.json.JSONArray
import org.json.JSONObject

/** A pixel-free prospective-format context, kept in a private session file, never in a Bundle. */
internal class CreditEditContext(private val metadata: JSONObject, private val history: JSONObject) {
    fun json()=JSONObject().put("metadata",metadata).put("history",history)
    fun edited(edits: List<ImageCredit>): CreditEditContext {
        val replacements=edits.associateBy {it.source}
        fun amend(credits: List<ImageCredit>)=credits.map {replacements[it.source] ?: it}
        val nextMetadata=JSONObject(metadata.toString())
        nextMetadata.optJSONObject("image_credits")?.let {state ->
            for(name in listOf("committed","floating")) {
                val values=state.optJSONArray(name) ?: continue
                for(i in 0 until values.length()) values.optJSONObject(i)?.let {value ->
                    replacements[value.optString("source")]?.let {value.put("text",it.text)}
                }
            }
        }
        val nextHistory=JSONObject(history.toString())
        val oldCatalog=ImageCredit.read(history.optJSONArray("image_credit_catalog"),deduplicate=false)
        val revised=amend(oldCatalog)
        val catalog=revised.distinct()
        val index=catalog.withIndex().associate {it.value to it.index}
        nextHistory.put("image_credit_catalog",ImageCredit.write(catalog))
        // Match HistoryArchive's distinct catalog and compact index reassignment exactly.
        for(name in listOf("undo","redo")) {
            val stack=nextHistory.getJSONArray(name)
            for(i in 0 until stack.length()) {
                val entry=stack.getJSONObject(i)
                val refs=entry.optJSONArray("image_credits") ?: JSONArray()
                entry.put("image_credits",JSONArray((0 until refs.length()).map {index.getValue(revised[refs.getInt(it)])}))
            }
        }
        return CreditEditContext(nextMetadata,nextHistory).also {it.validate()}
    }
    fun validate() {
        AutosaveStore.metadataBytes(metadata)
        HistoryArchive.validateManifest(history)
    }
    companion object {
        fun read(json: JSONObject)=CreditEditContext(json.getJSONObject("metadata"),json.getJSONObject("history"))
        fun ledgerOnly(credits: List<ImageCredit>)=CreditEditContext(
            JSONObject().put("version",1).put("image_credits",JSONObject().put("committed",ImageCredit.write(credits))
                .put("floating",JSONArray()).put("selection_sources_known",true)),
            HistoryArchive.manifest(RasterHistory.Snapshot()))
    }
}
