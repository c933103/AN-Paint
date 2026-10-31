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

/** Shared current-resource consumer binding and activity lifecycle support. */
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
