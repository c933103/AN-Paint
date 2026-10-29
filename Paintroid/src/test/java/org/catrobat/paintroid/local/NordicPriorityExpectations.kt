/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local
import org.json.JSONObject
import java.io.File

/** Finite forward binding, never rewriting or reconstructing historical evidence. */
internal object NordicPriorityExpectations {
    private val data by lazy { JSONObject(File("../tools/fixtures/current_localization/nordic_priority_wording.json").readText()) }
    fun current(tag: String,key: String,previous: String): String {
        val locale=data.getJSONObject("locales").optJSONObject(tag) ?: return previous
        val changed=locale.getJSONArray("changed")
        if((0 until changed.length()).none {changed.getString(it)==key}) return previous
        val old=locale.getJSONObject("predecessors").optJSONObject(key) ?: return previous
        require(previous==old.getString("target")) {"$tag/$key previous value differs"}
        return locale.getJSONObject("accepted").getString(key)
    }
    fun display(tag: String,key: String) = data.getJSONObject("locales").getJSONObject(tag).getJSONObject("accepted").getString(key).removeSurrounding("\"")
    fun project(old: JSONObject): JSONObject {
        val copy=JSONObject(old.toString())
        val values=copy.getJSONObject("values")
        for(key in values.keys()) for(tag in listOf("da","no")) {
            val row=values.getJSONObject(key)
            require(row.getString("default")==data.getJSONObject("sources").getJSONObject(key).getString("source"))
            row.put(tag,current(tag,key,row.getString(tag)))
        }
        for(tag in listOf("da","no")) {
            val rows=copy.getJSONObject("preserved_values").getJSONObject(tag)
            for(key in rows.keys()) {val row=rows.getJSONObject(key);row.put("value",current(tag,key,row.getString("value")))}
        }
        return copy
    }
}
