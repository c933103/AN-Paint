/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local
import org.json.JSONObject
import java.io.File

/** Finite forward binding, never rewriting or reconstructing historical evidence. */
internal object RecoveredTrioPriorityExpectations {
    private val data by lazy { JSONObject(File("../tools/fixtures/current_localization/nynorsk_belarusian_albanian_priority_wording.json").readText()) }
    fun current(tag: String,key: String,previous: String): String {
        val locale=data.getJSONObject("locales").optJSONObject(tag) ?: return previous
        val changed=locale.getJSONArray("changed")
        if((0 until changed.length()).none {changed.getString(it)=="string/$key"}) return previous
        val old=locale.getJSONObject("predecessors").optJSONObject("string/$key") ?: return previous
        require(previous==old.getString("target")) {"$tag/$key previous value differs"}
        return locale.getJSONObject("accepted").getString(key)
    }
    fun compiledDisplay(tag: String,key: String,raw: String): String {
        val inherited = when(tag to key) {
            "sq" to "ui_new_image" -> "Imazh i ri " to "Imazh i ri"
            "sq" to "ui_watercolor" -> "Akuarel " to "Akuarel"
            else -> null
        }
        if(inherited!=null) {
            require(raw==inherited.first) {"$tag/$key inherited raw whitespace binding differs"}
            return inherited.second
        }
        return Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
            when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
        }
    }
    fun display(tag: String,key: String) = compiledDisplay(tag,key,
        data.getJSONObject("locales").getJSONObject(tag).getJSONObject("accepted").getString(key))
}
