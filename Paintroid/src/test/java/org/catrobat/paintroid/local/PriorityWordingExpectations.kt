/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.json.JSONObject
import java.io.File

/** Finite forward bindings; historical fixtures are never edited or reconstructed. */
internal object PriorityWordingExpectations {
    private val locales by lazy {
        JSONObject(File("../tools/fixtures/current_localization/ukrainian_lithuanian_romanian_priority_wording.json").readText()).getJSONObject("locales")
    }
    fun current(tag: String,key: String,previous: String): String {
        val row=locales.optJSONObject(tag)?.getJSONObject("values")?.optJSONObject(key) ?: return previous
        if(row.isNull("previous_target")) return previous
        require(previous==row.getString("previous_target")) { "$tag/$key previous accepted value differs" }
        return row.getString("target")
    }
    fun display(tag: String,key: String): String {
        val data=locales.getJSONObject(tag)
        return (data.getJSONObject("values").optJSONObject(key) ?: data.getJSONObject("context").getJSONObject(key)).getString("display")
    }

    private val residuals by lazy {
        val rows=JSONObject(File("../tools/fixtures/current_localization/reviewed_residuals_20261030.json").readText()).getJSONArray("decisions")
        (0 until rows.length()).map { rows.getJSONObject(it) }.associateBy { it.getString("locale") to it.getString("key") }
    }
    /** Only exact reviewed successors replace an English fallback expectation. */
    fun residual(tag: String,key: String,previous: String,vararg args: Any): String {
        val row=residuals[tag to key] ?: return previous
        require(row.isNull("previous_target")) { "$tag/$key is not a missing-value successor" }
        fun formatted(value: String)=if(args.isEmpty()) value else java.lang.String.format(java.util.Locale.forLanguageTag(tag),value,*args)
        require(previous==formatted(row.getString("source"))) { "$tag/$key previous fallback differs" }
        return formatted(row.getString("target"))
    }
}
