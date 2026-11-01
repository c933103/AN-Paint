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
import java.util.concurrent.TimeUnit

/** Bounded compiled wording and real memory/recovery/encoding consumers, not whole-locale acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [CommonsPngFailureShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CroatianBosnianP0WordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String

    private fun priorityDisplay(tag:String,key:String)=PriorityWordingExpectations.resourceText(tag,key)
    private fun expected(tag: String,key: String)=PriorityWordingExpectations.resourceText(tag,key)
    private fun preserved(tag: String,key: String)=PriorityWordingExpectations.resourceText(tag,key)

    private fun ditherLabel(tag: String)=PriorityWordingExpectations.resourceText(tag,"save20_dither")

    private fun assertDitherControl(box: CheckBox, tag: String, checked: Boolean) {
        awaitUi("$tag GIF dither checkbox attached, shown and laid out") {
            box.isAttachedToWindow && box.isShown && box.isLaidOut &&
                box.width > 0 && box.height > 0 && !box.isLayoutRequested
        }
        assertEquals(ditherLabel(tag), box.text.toString())
        assertEquals(checked, box.isChecked)
        // CheckBox publishes its label as node.text, not contentDescription.
        val node = checkNotNull(box.createAccessibilityNodeInfo()) { "$tag dither node missing" }
        assertEquals(ditherLabel(tag), checkNotNull(node.text) { "$tag dither node text missing" }.toString())
        assertTrue(node.isCheckable)
        assertEquals(checked, node.isChecked)
    }

    private fun formatLabel(tag: String) = preserved(tag, "save20_file_format")

    private fun saveTitle(tag: String) = priorityDisplay(tag,"save20_title")

    private fun chooseLocation(tag: String): String = PriorityWordingExpectations.resourceText(tag,"ui_choose_location")

    private fun awaitUi(label: String, ready: () -> Boolean) {
        val until = System.nanoTime() + TimeUnit.SECONDS.toNanos(3)
        while (!ready() && System.nanoTime() < until) {
            shadowOf(Looper.getMainLooper()).idleFor(16, TimeUnit.MILLISECONDS)
            if (!ready()) Thread.sleep(1)
        }
        assertTrue(label, ready())
    }

    private fun assertDistinctFormatAndFilenameControls(root: View, tag: String) {
        val format = checkNotNull(root.findViewWithTag<Spinner>("export_format"))
        val filename = checkNotNull(root.findViewWithTag<EditText>("export_filename"))
        // Native accessibility nodes require a mounted, laid-out window. Do not
        // replace node assertions with the simpler View property if mounting fails.
        awaitUi("$tag Save dialog and both controls are attached, visible and laid out") {
            root.isAttachedToWindow && root.width > 0 && root.height > 0 && !root.isLayoutRequested &&
                listOf(format, filename).all {
                    it.isAttachedToWindow && it.isShown && it.isLaidOut &&
                        it.width > 0 && it.height > 0 && !it.isLayoutRequested
                }
        }
        val expectedFormat = "Format slike"
        val expectedFilename = "Naziv datoteke"
        assertEquals(expectedFormat, formatLabel(tag))
        assertEquals(expectedFilename, preserved(tag, "save20_file_name"))
        assertEquals(expectedFormat, format.contentDescription.toString())
        assertEquals(expectedFilename, filename.contentDescription.toString())
        val formatNode = checkNotNull(format.createAccessibilityNodeInfo()) {
            "$tag format accessibility node missing after attached, visible layout"
        }
        val filenameNode = checkNotNull(filename.createAccessibilityNodeInfo()) {
            "$tag filename accessibility node missing after attached, visible layout"
        }
        val formatNodeDescription = checkNotNull(formatNode.contentDescription) {
            "$tag format accessibility node has no contentDescription after attached, visible layout"
        }
        val filenameNodeDescription = checkNotNull(filenameNode.contentDescription) {
            "$tag filename accessibility node has no contentDescription after attached, visible layout"
        }
        assertEquals(expectedFormat, formatNodeDescription.toString())
        assertEquals(expectedFilename, filenameNodeDescription.toString())
        assertNotEquals(format.contentDescription, filename.contentDescription)
        fun labels(view: View): List<String> =
            (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
                (if (view is ViewGroup) (0 until view.childCount).flatMap { labels(view.getChildAt(it)) } else emptyList())
        assertTrue("Visible format caption", labels(root).contains(expectedFormat))
        assertTrue("Separate visible filename caption", labels(root).contains(expectedFilename))
    }

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
        for (tag in listOf("hr", "bs")) {
            val controller = Robolectric.buildActivity(Activity::class.java)
            val activity = controller.get()
            activity.setTheme(R.style.ClassicPaintTheme)
            controller.setup().windowFocusChanged(true)
            try {
                AppLanguage.select(activity, tag)
                AppLanguage.refresh(activity)
                assertEquals(tag, AppLanguage.selectedTag(activity))
                assertEquals(tag, activity.resources.configuration.locales[0].language)
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
                assertDistinctFormatAndFilenameControls(root, tag)
                assertEquals(formatLabel(tag), spinner.contentDescription.toString())
                assertEquals(chooseLocation(tag), dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(preserved(tag, "ui_cancel"),
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
    @Test fun gifDitherLabelExplanationStateAndConfirmRemainAtomicAcrossRepeatedRoutes() = forEachLocale { tag, activity ->
        for (initial in listOf(true, false)) for (route in listOf("confirm", "negative", "cancel")) {
            val requests = mutableListOf<SaveRequest>()
            var cancellations = 0
            val dialog = SaveOptionsDialog(activity,
                ExportOptions(format = ImageFormat.GIF, dither = initial), share = true,
                confirm = { requests.add(it) }, cancel = { cancellations++ },
                initialFilename = "drawing.png", export = true).show()
            try {
                val root = dialog.window!!.decorView
                assertDistinctFormatAndFilenameControls(root, tag)
                val spinner = checkNotNull(root.findViewWithTag<Spinner>("export_format"))
                val dither = checkNotNull(root.findViewWithTag<CheckBox>("export_dither"))
                val explanation = checkNotNull(root.findViewWithTag<FlowTextView>("export_description"))
                fun gif(checked: Boolean) {
                    spinner.setSelection(ImageFormat.values().indexOf(ImageFormat.GIF))
                    shadowOf(Looper.getMainLooper()).idle()
                    assertDitherControl(dither, tag, checked)
                    assertEquals(View.VISIBLE, explanation.visibility)
                    assertEquals(expected(tag, "save20_gif_description"), explanation.text.toString())
                }
                gif(initial)
                // CompoundButton toggles before View reports whether a click
                // listener handled the event; that return value is not checked state.
                dither.performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertEquals("$tag dither toggles from $initial through a real click", !initial, dither.isChecked)
                gif(!initial)
                repeat(2) {
                    spinner.setSelection(ImageFormat.values().indexOf(ImageFormat.JPEG))
                    shadowOf(Looper.getMainLooper()).idle()
                    assertEquals(View.GONE, dither.visibility)
                    assertEquals(!initial, dither.isChecked)
                    assertEquals(expected(tag, "save20_lossy_quality_description"), explanation.text.toString())
                    gif(!initial)
                }
                when (route) {
                    "confirm" -> dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
                    "negative" -> dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                    else -> dialog.cancel()
                }
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(dialog.isShowing)
                if (route == "confirm") {
                    assertEquals(1, requests.size)
                    assertEquals(!initial, requests.single().options.dither)
                    assertEquals(ImageFormat.GIF, requests.single().options.format)
                    assertEquals("drawing.gif", requests.single().fileName)
                    assertEquals(0, cancellations)
                } else {
                    assertTrue(requests.isEmpty())
                    assertEquals(1, cancellations)
                }
            } finally { dialog.dismiss() }
        }
    }

    @Test fun realSubstitutionsKeepMixedFrameCountsAndFailureReasonsLiteral() = forEachLocale { tag, _ ->
        val format = "GIF 100%"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_unknown"), format),
            ui(R.string.formats22_animation_unknown, format))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_message"), format, "at least 2"),
            ui(R.string.formats22_animation_message, format, ui(R.string.formats22_at_least_frames, 2)))
        val filename = "drawing 100%.png"
        val detail = "provider 50% unavailable"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_saved"), filename), ui(R.string.ui_saved, filename))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_the_image_was_saved_but_android_could_not"), detail),
            ui(R.string.ui_the_image_was_saved_but_android_could_not, detail))
        assertEquals(preserved(tag, "ui_save"), ui(R.string.ui_save))
        assertEquals(saveTitle(tag), ui(R.string.save20_title))
        assertEquals(preserved(tag, "ui_save_your_changes"), ui(R.string.ui_save_your_changes))
        assertEquals(expected(tag, "ui_save_and_share_41edb4") + "…", ui(R.string.ui_save_and_share))
    }

}
