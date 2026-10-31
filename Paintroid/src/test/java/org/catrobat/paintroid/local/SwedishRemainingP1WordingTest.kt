/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Color
import android.os.Looper
import android.view.View
import android.widget.EditText
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
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale

/** Compiled messages and real consumers; no installed-rendering or fluency claim. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
class SwedishRemainingP1WordingTest {
    private lateinit var beforeResources: Resources
    private lateinit var swedish: Context

    @Before fun useSwedish() {
        beforeResources = PaintApplication.currentResources
        val app = RuntimeEnvironment.getApplication() as Context
        swedish = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("sv"))
        })
        PaintApplication.currentResources = swedish.resources
    }

    @After fun restoreResources() {
        PaintApplication.currentResources = beforeResources
    }

    private fun currentExpectedMessage(key: String, historical: String): String {
        if (key != "ui_no_resize_fits_decoder_memory") return historical
        require(historical == "Även med minsta möjliga utdatabild ryms inte bildavkodarens arbetsbuffertar inom den nuvarande minnesbudgeten. Avbryt och använd en mindre källbild.") {
            "Unrecognized historical Swedish warning"
        }
        val oracle = JSONObject(File("../translations/source-review/memory-warning-successors-20261023.json").readText())
        val accepted = oracle.getJSONObject("values").getJSONObject("sv").getString(key)
        assertEquals("Independently accepted Swedish warning", "Även med minsta möjliga utdatastorlek kan den här bilden inte läsas in för redigering inom de nuvarande minnesgränserna. Avbryt och använd en mindre källbild.", accepted)
        return accepted
    }

    @Test fun warningSuccessorOnlyReplacesTheReviewedHistoricalKey() {
        val values = JSONObject(File("../tools/fixtures/current_localization/swedish_remaining_p1_wording.json").readText()).getJSONObject("values")
        var successors = 0
        for (key in values.keys()) {
            val historical = values.getJSONObject(key).getString("sv")
            val expected = currentExpectedMessage(key, historical)
            if (key == "ui_no_resize_fits_decoder_memory") {
                successors++
                assertNotEquals(historical, expected)
                assertThrows(IllegalArgumentException::class.java) {
                    currentExpectedMessage(key, historical + " changed")
                }
            } else {
                assertEquals("Unmapped fixture value $key", historical, expected)
            }
        }
        assertEquals(1, successors)
        assertEquals("unrelated", currentExpectedMessage("unknown_key", "unrelated"))
    }

    @Test fun allAcceptedCompleteMessagesResolveFromCompiledSwedishResources() {
        val fixture = JSONObject(File("../tools/fixtures/current_localization/swedish_remaining_p1_wording.json").readText())
        val values = fixture.getJSONObject("values")
        assertEquals(148, values.length())
        for (key in values.keys()) {
            val id = swedish.resources.getIdentifier(key, "string", swedish.packageName)
            assertNotEquals("Missing compiled resource $key", 0, id)
            val expected = currentExpectedMessage(key, values.getJSONObject(key).getString("sv")).replace("\\n", "\n")
            assertEquals("Complete Swedish resource $key", expected, swedish.getString(id))
        }

    }

    @Test fun numericEntryUsesCompleteRangeErrorsAndCancelDoesNotChangeTheValue() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        val changes = mutableListOf<Int>()
        var shown: AlertDialog? = null
        try {
            val slider = NumericSlider(activity, ui(R.string.ui_tolerance), 7, 1, 100) { changes.add(it) }
            activity.setContentView(slider)
            assertEquals("Tolerans: 7", slider.number.text.toString())
            assertEquals("Tolerans: 7. Tryck för att ange ett tal.", slider.number.contentDescription.toString())
            repeat(2) {
                assertTrue(slider.number.performClick())
                shadowOf(Looper.getMainLooper()).idle()
                val dialog = checkNotNull(ShadowAlertDialog.getLatestAlertDialog()); shown = dialog
                assertEquals("Tolerans", shadowOf(dialog).title.toString())
                assertEquals("Ange ett heltal från 1 till 100.", shadowOf(dialog).message.toString())
                val input = dialog.window!!.decorView.findViewWithTag<EditText>("numeric_input")
                for (invalid in listOf("0", "101", "1.5", "")) {
                    input.setText(invalid)
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
                    assertEquals("Ange ett tal från 1 till 100.", input.error.toString())
                    assertTrue(dialog.isShowing)
                    assertEquals(6, slider.slider.progress)
                    assertTrue(changes.isEmpty())
                }
                input.setText("42")
                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(dialog.isShowing)
                assertEquals("Tolerans: 7", slider.number.text.toString())
                assertTrue(changes.isEmpty())
            }
            slider.number.performClick()
            shadowOf(Looper.getMainLooper()).idle()
            val dialog = checkNotNull(ShadowAlertDialog.getLatestAlertDialog()); shown = dialog
            dialog.window!!.decorView.findViewWithTag<EditText>("numeric_input").setText("42")
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertFalse(dialog.isShowing)
            assertEquals(listOf(42), changes)
            assertEquals("Tolerans: 42", slider.number.text.toString())
            assertEquals("Tolerans: 42. Tryck för att ange ett tal.", slider.number.contentDescription.toString())
        } finally {
            shown?.dismiss(); controller.pause().stop().destroy()
        }
    }

    @Test fun colourTargetsDescribeAndInvokeTheirOwnForegroundOrBackgroundAction() {
        val button = ColourStatusButton(swedish)
        var foregroundEdits = 0; var backgroundEdits = 0
        button.editForeground = { foregroundEdits++ }
        button.editBackground = { backgroundEdits++ }
        val foreground = button.findViewWithTag<View>("foreground_colour")
        val background = button.findViewWithTag<View>("background_colour")
        for ((fg, bg) in listOf(Color.RED to Color.BLUE, Color.BLACK to Color.WHITE)) {
            button.foreground = fg; button.backgroundColour = bg; button.refresh()
            val fgHex = String.format(Locale.ROOT, "#%06X", fg and 0xffffff)
            val bgHex = String.format(Locale.ROOT, "#%06X", bg and 0xffffff)
            assertEquals("Förgrundsfärg $fgHex. Redigera färg.", foreground.contentDescription.toString())
            assertEquals("Bakgrundsfärg $bgHex. Redigera färg.", background.contentDescription.toString())
            assertTrue(foreground.performClick())
            assertEquals(backgroundEdits + 1, foregroundEdits)
            assertTrue(background.performClick())
            assertEquals(foregroundEdits, backgroundEdits)
        }
        assertEquals(2, foregroundEdits); assertEquals(2, backgroundEdits)
    }
}
