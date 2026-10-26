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
import java.util.Locale

/** Eight reviewed values and real dialog consumers, not native or whole-locale acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class NynorskSaveWordingTest {
    private lateinit var beforeResources: Resources
    private lateinit var beforeLocale: Locale
    private val save = "Vel eit biletformat og innstillingane for komprimering. «Lagra» vil bruka dette filnamnet, denne plasseringa, formatet og innstillingane om att."
    private val export = "Eksporter eit ikon, Base64-tekst eller ASCII-kunst. Eksportering endrar korkje biletet du arbeider med, eller kva fil «Lagra» lagrar til."
    private val share = "Lagra ein kopi på staden du vel, og vel deretter ein app til å dela kopien. Dette endrar ikkje kva fil «Lagra» lagrar til."

    @Before fun useNynorsk() {
        beforeResources = PaintApplication.currentResources
        beforeLocale = Locale.getDefault()
        val app = RuntimeEnvironment.getApplication() as Context
        PaintApplication.currentResources = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("nn"))
        }).resources
        Locale.setDefault(Locale.US)
    }

    @After fun restoreResources() {
        PaintApplication.currentResources = beforeResources
        Locale.setDefault(beforeLocale)
    }

    @Test fun allEightCompleteCompiledValuesPreserveTheFilenameArgumentAndActionNames() {
        assertEquals("Vil du lagra endringane?", ui(R.string.ui_save_your_changes))
        assertEquals("Biletet du arbeider med, har endringar som ikkje er lagra.", ui(R.string.ui_your_current_image_has_unsaved_changes))
        assertEquals("Eksportfila er oppretta. Bruk «Lagra» eller «Lagra som…» til å lagra biletet du arbeider med, før du held fram.", ui(R.string.ui_export_did_not_save23))
        assertEquals("Kunne ikkje lagra biletet", ui(R.string.ui_could_not_save_image))
        assertEquals("teikning 100%.png er lagra", ui(R.string.ui_saved, "teikning 100%.png"))
        assertEquals(export, ui(R.string.ui_export_explanation23))
        assertEquals(save, ui(R.string.ui_save_explanation23))
        assertEquals(share, ui(R.string.ui_share_explanation34))
        assertEquals("Lagra", ui(R.string.ui_save))
        assertEquals("Lagra", ui(R.string.ui_save_a5d0d9))
        assertEquals("Lagra som…", ui(R.string.save20_title))
        assertEquals("Eksporter som…", ui(R.string.ui_export_as23))
        // Unreviewed neighbours retain their intentional canonical fallback.
        assertEquals("Save and share", ui(R.string.ui_save_and_share_41edb4))
    }

    @Test fun actualSaveExportAndSharePanelsShowDistinctWholeMessagesAndCancelWithoutSaving() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var dialog: AlertDialog? = null
        try {
            fun texts(view: View): List<String> =
                (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
                    (if (view is ViewGroup) (0 until view.childCount).flatMap { texts(view.getChildAt(it)) } else emptyList())
            // Share uses export=true in the real menu route; its prose must win over export prose.
            val modes = listOf(Triple(false, false, save), Triple(false, true, export), Triple(true, true, share))
            for ((sharing, exporting, expected) in modes) repeat(2) {
                var confirmed = false
                var cancelled = 0
                val shown = SaveOptionsDialog(activity, ExportOptions(), share = sharing,
                    confirm = { confirmed = true }, cancel = { cancelled++ }, export = exporting).show()
                dialog = shown
                val displayed = texts(shown.window!!.decorView)
                assertTrue(displayed.contains(expected))
                for (other in listOf(save, export, share).filter { it != expected }) assertFalse(displayed.contains(other))
                assertEquals("Avbryt", shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(shown.isShowing)
                assertFalse(confirmed)
                assertEquals(1, cancelled)
            }
        } finally {
            dialog?.dismiss()
            controller.pause().stop().destroy()
        }
    }
}
