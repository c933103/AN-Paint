/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.res.Configuration
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.PaintApplication
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File
import java.util.Locale

/** Complete compiled values; this dormant resource is not the active Help dialog. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
class SwedishLegacyManualTest {
    private val data by lazy {
        JSONObject(File("../tools/fixtures/current_localization/swedish_legacy_manual_successor.json").readText())
    }
    private fun display(field: String)=data.getString(field).replace("\\n", "\n").replace("\\'", "'")

    @Test fun completeSwedishManualResolvesInTheSelectedAppLanguageWithoutEnglishFallback() {
        val app=RuntimeEnvironment.getApplication()
        val previousTag=AppLanguage.selectedTag(app)
        val previousResources=PaintApplication.currentResources
        val previousLocale=Locale.getDefault()
        val controller=Robolectric.buildActivity(Activity::class.java)
        val activity=controller.setup().get()
        try {
            AppLanguage.select(activity,"sv");AppLanguage.refresh(activity)
            assertEquals("sv",AppLanguage.selectedTag(activity))
            val actual=activity.getString(R.string.ui_the_arrow_on_the_left_directly_below_the)
            assertEquals(display("swedish"),actual)
            assertEquals(10,actual.split("\n\n").size)
            assertNotEquals(display("source"),actual)
            assertNotEquals(actual,activity.getString(R.string.ui_help23))
            assertEquals("Huvud",activity.getString(R.string.ui_main23))
            assertTrue(actual.contains("Fästa bilder kan flyttas för att fylla luckan."))
            assertTrue(actual.contains("befintliga ritytan"))
            assertTrue(actual.contains("Visa > Förstoringsglas kan du aktivera"))
        } finally {
            controller.pause().stop().destroy()
            AppLanguage.select(app,previousTag)
            PaintApplication.currentResources=previousResources
            Locale.setDefault(previousLocale)
        }
    }

    @Test fun completeDefaultManualCompilesIncludingLiteralPercentAndParagraphs() {
        // An unmatched language isolates values/, rather than an existing regional
        // English catalogue with its separately retained historical translation.
        val app=RuntimeEnvironment.getApplication()
        val context=app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale("zz"))
        })
        val actual=context.getString(R.string.ui_the_arrow_on_the_left_directly_below_the)
        assertEquals(display("source"),actual)
        assertEquals(10,actual.split("\n\n").size)
        assertTrue(actual.contains("100%"))
        assertTrue(actual.contains("that tab's controls"))
        assertNotEquals(display("previous_source"),actual)
        assertTrue(actual.contains("selection edits can be undone"))
        assertFalse(actual.contains("one undoable selection edit"))
    }
}
