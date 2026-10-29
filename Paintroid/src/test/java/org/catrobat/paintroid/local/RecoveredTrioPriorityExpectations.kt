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
    fun display(tag: String,key: String) = data.getJSONObject("locales").getJSONObject(tag).getJSONObject("accepted").getString(key).removeSurrounding("\"")
}
