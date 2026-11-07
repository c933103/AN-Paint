/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R
import org.json.JSONObject

/** Document identity is data; a generated display name belongs to the current UI locale. */
internal sealed class DocumentName {
    object Untitled: DocumentName()
    object Recovered: DocumentName()
    data class Named(val value: String): DocumentName()

    fun text(): String = when(this) {
        Untitled -> ui(R.string.ui_untitled)
        Recovered -> ui(R.string.ui_recovered_image)
        is Named -> value
    }

    fun writeTo(metadata: JSONObject) {
        val identity=JSONObject().put("kind",when(this) {
            Untitled -> "untitled";Recovered -> "recovered";is Named -> "named"
        })
        if(this is Named) {
            identity.put("value",value)
            // Actual names remain readable by earlier versions. Generated names
            // are never serialized as translated text.
            metadata.put("filename",value)
        } else metadata.remove("filename")
        metadata.put("document_name",identity)
    }

    companion object {
        fun read(metadata: JSONObject,savedTarget: SavedTarget?): DocumentName {
            // An explicit save destination always supplies a real name.
            savedTarget?.let {return Named(it.name)}
            metadata.optJSONObject("document_name")?.let {identity ->
                when(identity.optString("kind")) {
                    "untitled" -> return Untitled
                    "recovered" -> return Recovered
                    "named" -> if(identity.has("value")) return Named(identity.getString("value"))
                }
            }
            // Earlier formats stored UI text without a distinct identity. Migrate
            // a recognized placeholder, while explicit named-state stays named.
            val previous=metadata.optString("filename","")
            if(metadata.has("filename_is_placeholder")) {
                if(metadata.optBoolean("filename_is_placeholder")) return Untitled
            } else if(previous==ui(R.string.ui_untitled)) return Untitled
            return if(previous.isEmpty()) Recovered else Named(previous)
        }
    }
}
