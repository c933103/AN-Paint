/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.json.JSONArray
import org.json.JSONObject

/** Original attribution text stays with the document, independent of the current UI language. */
data class ImageCredit(val source: String, val text: String) {
    companion object {
        fun write(credits: Collection<ImageCredit>) = JSONArray().apply {
            credits.forEach { put(JSONObject().put("source",it.source).put("text",it.text)) }
        }
        fun read(values: JSONArray?, deduplicate: Boolean = true): List<ImageCredit> = buildList {
            if(values!=null) for(i in 0 until values.length()) {
                val value=values.optJSONObject(i) ?: continue
                val source=value.optString("source")
                if(source.isNotBlank()) add(ImageCredit(source,value.optString("text")))
            }
        }.let {if(deduplicate) it.distinctBy {credit -> credit.source} else it}
        fun text(credits: Collection<ImageCredit>) = credits.map {it.text}.filter {it.isNotBlank()}.joinToString("\n\n")
    }
}
