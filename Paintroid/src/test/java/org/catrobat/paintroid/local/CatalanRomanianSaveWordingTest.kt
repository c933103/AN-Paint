/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import java.io.File
import java.util.Locale

/** Twenty bounded reviewed values and real dialog consumers, not whole-locale acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class CatalanRomanianSaveWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale

    // Current compiled labels are used for actual control binding.
    private fun expected(tag: String, key: String) = PriorityWordingExpectations.resourceText(tag,key)

    @Before fun rememberResources() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
    }

    @After fun restoreResources() {
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    private fun forEachLocale(check: (String, Context) -> Unit) {
        val app = RuntimeEnvironment.getApplication() as Context
        for (tag in listOf("ca", "ro")) {
            val context = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
                setLocale(AppLanguage.resourceLocale(Locale.forLanguageTag(tag)))
            })
            try {
                PaintApplication.currentResources = context.resources
                Locale.setDefault(Locale.US)
                check(tag, context)
            } finally {
                PaintApplication.currentResources = previousResources
                Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun formattedSaveArgumentsAndActionAliasesRemainConsistent() = forEachLocale { tag, _ ->
        val filename = "drawing 100%.png"
        val detail = "provider 50% unavailable"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_saved"), filename),
            ui(R.string.ui_saved, filename))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_the_image_was_saved_but_android_could_not"), detail),
            ui(R.string.ui_the_image_was_saved_but_android_could_not, detail))
        assertEquals(ui(R.string.ui_save), ui(R.string.ui_save_a5d0d9))
        assertEquals(ui(R.string.ui_save_and_share_41edb4) + "…", ui(R.string.ui_save_and_share))
    }

}
