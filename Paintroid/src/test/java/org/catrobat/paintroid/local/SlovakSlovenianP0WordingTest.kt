/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.CheckBox
import android.widget.EditText
import android.widget.Spinner
import android.content.Context
import android.content.ContextWrapper
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Color
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
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
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.io.IOException
import java.util.Locale

/** Bounded compiled wording and real memory/recovery/encoding consumers, not whole-locale acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [CommonsPngFailureShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class SlovakSlovenianP0WordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String

    // Current compiled labels are used for actual control binding.
    private fun expected(tag: String, key: String) = PriorityWordingExpectations.resourceText(tag,key)

    @Before fun rememberLanguage() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        previousTag = AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
        CommonsPngFailureShadow.resetFailure()
    }

    @After fun restoreLanguage() {
        CommonsPngFailureShadow.resetFailure()
        AppLanguage.select(RuntimeEnvironment.getApplication(), previousTag)
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    private fun forEachLocale(check: (String, Activity) -> Unit) {
        for (tag in listOf("sk", "sl")) {
            val controller = Robolectric.buildActivity(Activity::class.java)
            val activity = controller.get()
            activity.setTheme(R.style.ClassicPaintTheme)
            controller.setup()
            try {
                AppLanguage.select(activity, tag)
                AppLanguage.refresh(activity)
                assertEquals(tag, AppLanguage.selectedTag(activity))
                Locale.setDefault(Locale.US) // Resource locale must win over a mismatched process locale.
                check(tag, activity)
            } finally {
                CommonsPngFailureShadow.resetFailure()
                AppLanguage.select(activity, previousTag)
                AppLanguage.refresh(activity)
                controller.pause().stop().destroy()
                PaintApplication.currentResources = previousResources
                Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun realFormatPanelUpdatesDescriptionsRejectsInvalidNamesAndCancelsRepeatedly() = forEachLocale { tag, activity ->
        repeat(2) { attempt ->
            var confirmations = 0
            var cancellations = 0
            // Production Share exposes all formats; both flags are also set by the real File-menu action.
            val dialog = SaveOptionsDialog(activity, ExportOptions(format = ImageFormat.GIF), share = true,
                confirm = { confirmations++ }, cancel = { cancellations++ },
                initialFilename = "drawing 100%.png", export = true).show()
            try {
                val root = dialog.window!!.decorView
                val spinner = checkNotNull(root.findViewWithTag<Spinner>("export_format"))
                val explanation = checkNotNull(root.findViewWithTag<FlowTextView>("export_description"))
                val quality = checkNotNull(root.findViewWithTag<NumericSlider>("export_quality"))
                val lossless = checkNotNull(root.findViewWithTag<CheckBox>("export_lossless"))
                val dither = checkNotNull(root.findViewWithTag<CheckBox>("export_dither"))
                val filename = checkNotNull(root.findViewWithTag<EditText>("export_filename"))
                assertEquals(PriorityWordingExpectations.resourceText(tag,"save20_file_format"), spinner.contentDescription.toString())
                assertEquals(PriorityWordingExpectations.resourceText(tag,"ui_choose_location"), dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(if (tag == "sk") "Zrušiť" else "Prekliči",
                    dialog.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                fun select(format: ImageFormat, key: String) {
                    spinner.setSelection(ImageFormat.values().indexOf(format))
                    shadowOf(Looper.getMainLooper()).idle()
                    assertEquals(format.label, spinner.selectedItem.toString())
                    assertEquals(expected(tag, key), explanation.text.toString())
                    assertEquals(View.VISIBLE, explanation.visibility)
                }
                select(ImageFormat.GIF, "save20_gif_description")
                assertEquals(View.VISIBLE, dither.visibility)
                assertEquals(View.GONE, quality.visibility)
                select(ImageFormat.JPEG, "save20_lossy_quality_description")
                assertEquals(View.GONE, dither.visibility)
                assertEquals(View.GONE, lossless.visibility)
                assertEquals(View.VISIBLE, quality.visibility)
                select(ImageFormat.WEBP, "ui_higher_quality_usually_makes_a_larger_file_lossless")
                assertEquals(View.VISIBLE, lossless.visibility)
                assertTrue(lossless.isChecked)
                assertEquals(View.GONE, quality.visibility)
                lossless.performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(lossless.isChecked)
                assertEquals(View.VISIBLE, quality.visibility)
                assertEquals(expected(tag, "ui_higher_quality_usually_makes_a_larger_file_lossless"), explanation.text.toString())
                select(ImageFormat.ASCII_ART, "formats22_ascii_description")
                assertEquals(View.VISIBLE, root.findViewWithTag<View>("export_ascii_controls").visibility)
                assertEquals(View.GONE, quality.visibility)
                filename.setText("folder/bad-name.txt")
                repeat(2) {
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
                    shadowOf(Looper.getMainLooper()).idle()
                    assertEquals(expected(tag, "save20_invalid_name"), filename.error.toString())
                    assertTrue(dialog.isShowing)
                    assertEquals(0, confirmations)
                    assertEquals(0, cancellations)
                }
                if (attempt == 0) dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick() else dialog.cancel()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(dialog.isShowing)
                assertEquals(0, confirmations)
                assertEquals(1, cancellations)
            } finally { dialog.dismiss() }
        }
    }
    @Test fun actualSaveExportSharePanelsKeepDistinctMessagesAndRepeatedCancel() = forEachLocale { tag, activity ->
        fun texts(view: View): List<String> =
            (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
                (if (view is ViewGroup) (0 until view.childCount).flatMap { texts(view.getChildAt(it)) } else emptyList())
        val save = expected(tag, "ui_save_explanation23")
        val export = expected(tag, "ui_export_explanation23")
        val share = expected(tag, "ui_share_explanation34")
        for ((sharing, exporting, message) in listOf(Triple(false, false, save),
                Triple(false, true, export), Triple(true, true, share))) repeat(2) {
            var confirmations = 0
            var cancellations = 0
            val dialog = SaveOptionsDialog(activity, ExportOptions(), share = sharing,
                confirm = { confirmations++ }, cancel = { cancellations++ }, export = exporting).show()
            try {
                val displayed = texts(dialog.window!!.decorView)
                assertTrue(displayed.contains(message))
                for (other in listOf(save, export, share).filter { it != message }) assertFalse(displayed.contains(other))
                assertEquals(if (sharing) expected(tag, "ui_save_and_share_41edb4")
                    else ui(if (exporting) R.string.ui_export_as23 else R.string.save20_title), shadowOf(dialog).title.toString())
                assertTrue(displayed.contains(PriorityWordingExpectations.resourceText(tag,"save20_file_format")))
                assertEquals(PriorityWordingExpectations.resourceText(tag,"ui_choose_location"), dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(if (tag == "sk") "Zrušiť" else "Prekliči", dialog.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(dialog.isShowing)
                assertEquals(0, confirmations)
                assertEquals(1, cancellations)
            } finally { dialog.dismiss() }
        }
    }

    @Test fun realSubstitutionsKeepMixedFrameCountsAndFailureReasonsLiteral() = forEachLocale { tag, _ ->
        val format = "GIF 100%"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_unknown"), format),
            ui(R.string.formats22_animation_unknown, format))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_message"), format, String.format(Locale.forLanguageTag(tag),PriorityWordingExpectations.resourceText(tag,"formats22_at_least_frames"),2)),
            ui(R.string.formats22_animation_message, format, ui(R.string.formats22_at_least_frames, 2)))
        val filename = "drawing 100%.png"
        val detail = "provider 50% unavailable"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_saved"), filename), ui(R.string.ui_saved, filename))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_the_image_was_saved_but_android_could_not"), detail),
            ui(R.string.ui_the_image_was_saved_but_android_could_not, detail))
        assertEquals(if (tag == "sk") "Uložiť" else "Shrani", ui(R.string.ui_save))
        assertEquals(if (tag == "sk") "Uložiť ako…" else "Shrani kot…", ui(R.string.save20_title))
        assertEquals(PriorityWordingExpectations.resourceText(tag,"ui_save_your_changes"), ui(R.string.ui_save_your_changes))
        assertEquals(expected(tag, "ui_save_and_share_41edb4") + "…", ui(R.string.ui_save_and_share))
    }

}
