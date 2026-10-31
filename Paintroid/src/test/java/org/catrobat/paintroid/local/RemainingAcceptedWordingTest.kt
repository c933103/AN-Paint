/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.res.Resources
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.PaintApplication
import org.json.JSONObject
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.Assert.*
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File
import java.util.Locale

/** Exact compiled wording, not native-human or physical-layout certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
class RemainingAcceptedWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private val counts=mapOf("tt-Cyrl" to 11,"tt-Latn" to 11,"br" to 10,"sv" to 1,
        "shn" to 148,"yua" to 60,"ang" to 244,"non" to 254)
    @Before fun remember() {
        previousResources=PaintApplication.currentResources
        previousLocale=Locale.getDefault()
        previousTag=AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }
    @After fun restore() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
        PaintApplication.currentResources=previousResources
        Locale.setDefault(previousLocale)
    }
    @Test fun everyAcceptedValueCompilesAndResolvesForItsOwnSelectedLocale() {
        val decisions=JSONObject(File("../tools/fixtures/current_localization/reviewed_residuals_20261030.json").readText()).getJSONArray("decisions")
        val rows=(0 until decisions.length()).map {decisions.getJSONObject(it)}
        for((tag,count) in counts) {
            val selected=rows.filter {it.getString("locale")==tag}
            assertEquals(tag,count,selected.size)
            val controller=Robolectric.buildActivity(Activity::class.java)
            val activity=controller.setup().get()
            try {
                AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
                assertEquals(tag,AppLanguage.selectedTag(activity))
                for(row in selected) {
                    val key=row.getString("key")
                    val id=activity.resources.getIdentifier(key,"string",activity.packageName)
                    assertNotEquals(key,0,id)
                    val expected=RecoveredTrioPriorityExpectations.compiledDisplay(tag,key,row.getString("target"))
                    assertEquals("$tag/$key",expected,activity.getString(id))
                }
                if(tag=="br") assertEquals("Skeudenn o kenglotañ gant ar prenestr",activity.getString(R.string.ui_fit_image))
                if(tag=="sv") {
                    assertEquals("Huvud",activity.getString(R.string.ui_main23))
                    assertEquals("Förgrundsfärg #000000, bakgrundsfärg #FFFFFF. Vänsterpil: fäll ihop färgpaletten.",
                        activity.getString(R.string.ui_foreground_background_colour_palette,"#000000","#FFFFFF","Vänsterpil: fäll ihop"))
                    assertEquals("Förgrundsfärg #000000, bakgrundsfärg #FFFFFF. Högerpil: fäll ut färgpaletten.",
                        activity.getString(R.string.ui_foreground_background_colour_palette,"#000000","#FFFFFF","Högerpil: fäll ut"))
                }
                if(tag=="shn") assertEquals("ၶိုၼ်ၶိုၼ်း",activity.getString(R.string.ui_undo))
                if(tag=="non") assertEquals(
                    rows.first {it.getString("locale")=="ang" && it.getString("key")=="ui_autosave_is_paused_to_protect_that_draft_use"}.getString("source"),
                    activity.getString(R.string.ui_autosave_is_paused_to_protect_that_draft_use))
            } finally {controller.pause().stop().destroy()}
        }
    }
}
