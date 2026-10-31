/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.res.Resources
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.PaintApplication
import org.junit.Assert.assertEquals
import org.robolectric.Robolectric
import org.robolectric.shadows.ShadowAlertDialog
import java.util.Locale
import org.json.JSONObject
import java.io.File

/** Shared consumer resource/lifecycle support; bounded residual bindings remain below. */
internal object PriorityWordingExpectations {
    /** Resolve the current compiled label for an actual consumer-binding assertion. */
    fun resources(tag: String): Resources {
        val context = org.robolectric.RuntimeEnvironment.getApplication()
        val configuration = android.content.res.Configuration(context.resources.configuration)
        configuration.setLocale(AppLanguage.resourceLocale(Locale.forLanguageTag(tag)))
        return context.createConfigurationContext(configuration).resources
    }
    fun resourceText(tag: String,key: String): String {
        val resources = resources(tag)
        val id = resources.getIdentifier(key,"string",org.robolectric.RuntimeEnvironment.getApplication().packageName)
        require(id != 0) { "Missing compiled string $key" }
        return resources.getString(id)
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
        // Reuse the existing raw-resource/display boundary before substituting arguments.
        return formatted(RecoveredTrioPriorityExpectations.compiledDisplay(tag,key,row.getString("target")))
    }

    /** Shared unchanged activity lifecycle; callers retain their own locale scope and assertions. */
    fun forEachLocale(
        tags: List<String>,
        previousResources: Resources,
        previousLocale: Locale,
        previousTag: String,
        check: (String, Activity) -> Unit
    ) {
        for(tag in tags) {
            val controller=Robolectric.buildActivity(Activity::class.java)
            val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup()
            try {
                AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
                assertEquals(tag,AppLanguage.selectedTag(activity))
                // ui() must format using the selected resource locale, not the process default.
                Locale.setDefault(Locale.US)
                check(tag,activity)
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                AppLanguage.select(activity,previousTag);AppLanguage.refresh(activity)
                controller.pause().stop().destroy()
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }
}
