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
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.io.IOException
import java.util.Locale
import java.util.concurrent.TimeUnit

/** Bounded compiled wording and real memory/recovery/encoding consumers, not whole-locale acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [CommonsPngFailureShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class SerbianP0WordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private val fixture by lazy {
        JSONObject(File("../tools/fixtures/current_localization/serbian_p0_wording.json").readText())
    }

    // Only this batch's simply quote-wrapped reviewed values use this decoder.
    // 337 inherited values/attributes stay exact; the Cyrillic format label has its own reviewed successor.
    private fun expected(tag: String, key: String) = fixture.getJSONObject("values")
        .getJSONObject(key).getString(tag).removeSurrounding("\"")

    private fun preserved(tag: String, key: String) = fixture.getJSONObject("preserved_values")
        .getJSONObject(tag).getJSONObject(key).getString("value").removeSurrounding("\"")

    private fun formatLabel(tag: String): String {
        if (tag != "sr-Cyrl") return preserved(tag, "save20_file_format")
        val successor = fixture.getJSONObject("format_label_successor")
        assertEquals("sr-Cyrl", successor.getString("locale"))
        assertEquals("save20_file_format", successor.getString("key"))
        assertEquals("save20_file_format", successor.getJSONObject("attributes").getString("name"))
        return successor.getString("value").removeSurrounding("\"")
    }

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
        val expectedFormat = if (tag == "sr-Cyrl") "Формат датотеке" else "Format slike"
        val expectedFilename = if (tag == "sr-Cyrl") "Назив датотеке" else "Naziv datoteke"
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
        for (tag in listOf("sr-Cyrl", "sr-Latn")) {
            val controller = Robolectric.buildActivity(Activity::class.java)
            val activity = controller.get()
            activity.setTheme(R.style.ClassicPaintTheme)
            controller.setup().windowFocusChanged(true)
            try {
                AppLanguage.select(activity, tag)
                AppLanguage.refresh(activity)
                assertEquals(tag, AppLanguage.selectedTag(activity))
                assertEquals(Locale.forLanguageTag(tag).script, activity.resources.configuration.locales[0].script)
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

    @Test fun all74CompiledValuesPerLocaleMatchWhileHeldAndP1FallbacksRemainEnglish() = forEachLocale { tag, activity ->
        val values = fixture.getJSONObject("values")
        assertEquals(74, values.length())
        val inherited = fixture.getJSONObject("preserved_values").getJSONObject(tag)
        assertEquals(if (tag == "sr-Cyrl") 169 else 168, inherited.length())
        for (key in values.keys()) {
            assertFalse("The missing-only batch must not replace $tag/$key", inherited.has(key))
            val id = activity.resources.getIdentifier(key, "string", activity.packageName)
            assertNotEquals("$tag/$key", 0, id)
            assertEquals("$tag/$key", expected(tag, key), activity.getString(id))
        }
        // Compiled-only coverage for the separate P0 assembly-floor warning; the
        // paired warning oracle and its P1 companion are not expanded by this test.
        assertEquals(expected(tag, "ui_assembly_source_memory_floor"), ui(R.string.ui_assembly_source_memory_floor))
        assertEquals(expected(tag, "ui_history_unavailable34"), ui(R.string.ui_history_unavailable34))
        assertEquals("Even at the smallest output size, this image cannot be loaded for editing within the current memory limits. Cancel and use a smaller source image.",
            ui(R.string.ui_no_resize_fits_decoder_memory))
        assertEquals(formatLabel(tag), ui(R.string.save20_file_format))
        assertEquals(preserved(tag, "ui_load_image"), ui(R.string.ui_load_image))
        assertEquals("at least 2", ui(R.string.formats22_at_least_frames, 2))
        assertEquals("Choose location…", ui(R.string.ui_choose_location))
        assertEquals("PNG exported. Your full drawing still has unsaved changes; save a full image copy before replacing it.",
            ui(R.string.formats22_derived_exported, "PNG"))
        assertEquals("Save as PNG", ui(R.string.ui_save_as, "PNG"))
        assertEquals("Save as JPEG…", ui(R.string.ui_save_as_jpeg))
        assertEquals("Save as JPEG XL…", ui(R.string.ui_save_as_jpeg_xl))
        assertEquals("Save as PNG…", ui(R.string.ui_save_as_png))
    }

    @Test fun realMemoryAdmissionFailureFormatsAllFourArgumentsBeforeAllocation() = forEachLocale { tag, _ ->
        val mib = 1024L * 1024
        val policy = ImageMemoryPolicy.calculate(256 * mib, 0, 96 * mib, 0, false)
        assertEquals(0L, policy.maxPixels())
        val failure = assertThrows(ImageSizeException::class.java) { policy.check(1000, 2000) }
        val message = String.format(Locale.forLanguageTag(tag),
            expected(tag, "ui_d_d_pixels_2f_mp_exceeds_the_current"), 1000, 2000, 2.0, 0.0)
        assertEquals(message, failure.message)
        assertTrue(message.contains("1000 × 2000"))
        assertTrue(message.contains("(2,00 MP)"))
        assertTrue(message.contains("0,00 MP"))
    }

    private fun recoveryContext(context: Context, folder: File): Context = object : ContextWrapper(context) {
        override fun getFilesDir(): File = folder
        override fun getCacheDir(): File = File(folder, "cache").apply { mkdirs() }
    }

    @Test fun failedDraftRecoveryReportsPreservationOnlyAfterKeepingItsExactBytes() = forEachLocale { tag, activity ->
        val folder = File(activity.cacheDir, "$tag-failed-recovery-${System.nanoTime()}").apply { mkdirs() }
        val store = AutosaveStore(folder)
        val original = "deliberately not a ZIP draft".toByteArray()
        store.file.writeBytes(original)
        var recovered: RecoveredEditor? = null
        try {
            recovered = recoverEditor(recoveryContext(activity, folder), store).value
            assertFalse(recovered.restored)
            assertFalse(recovered.autosaveBlocked)
            assertEquals(expected(tag, "ui_previous_draft_kept_for_recovery"), recovered.draftStatus)
            assertEquals(String.format(Locale.forLanguageTag(tag),
                expected(tag, "ui_a_separate_recovery_copy_has_been_kept_use"),
                expected(tag, "ui_the_previous_draft_could_not_be_restored")), recovered.recoveryNotice)
            assertArrayEquals(original, store.file.readBytes())
            val copies = store.recoveryCopies()
            assertEquals(1, copies.size)
            assertArrayEquals(original, copies.single().readBytes())
        } finally { recovered?.document?.close(); folder.deleteRecursively() }
    }

    @Test fun recoveredDraftRetainsUnsavedPixelsAndOneFloatingSelectionWithoutSaveAssociation() = forEachLocale { tag, activity ->
        val folder = File(activity.cacheDir, "$tag-restored-draft-${System.nanoTime()}").apply { mkdirs() }
        val store = AutosaveStore(folder)
        val image = Bitmap.createBitmap(8, 6, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.RED) }
        val floating = Bitmap.createBitmap(3, 2, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.BLUE) }
        var recovered: RecoveredEditor? = null
        try {
            val metadata = JSONObject().put("version", 1).put("dirty", true)
                .put("floating_rect", JSONArray(listOf(1.0, 2.0, 4.0, 4.0))).put("floating_rotation", 0.0)
            store.write(image, floating, metadata)
            recovered = recoverEditor(recoveryContext(activity, folder), store).value
            assertTrue(recovered.restored)
            assertTrue("Draft recovery must not mark explicit Save complete", recovered.document.dirty)
            assertNull(recovered.savedTarget)
            assertNull(recovered.recoveryNotice)
            assertEquals(expected(tag, "ui_draft_restored"), recovered.draftStatus)
            assertEquals(expected(tag, "ui_recovered_image"), recovered.filename)
            assertEquals(8, recovered.document.bitmap.width)
            assertEquals(6, recovered.document.bitmap.height)
            assertEquals(Color.RED, recovered.document.bitmap.getPixel(0, 0))
            val selected = checkNotNull(recovered.document.selection)
            assertEquals(3, selected.image.width)
            assertEquals(2, selected.image.height)
            assertEquals(Color.BLUE, selected.image.getPixel(0, 0))
            assertTrue(selected.floating)
            assertTrue(store.recoveryCopies().isEmpty())
        } finally { recovered?.document?.close(); image.recycle(); floating.recycle(); folder.deleteRecursively() }
    }

    @Test fun realEncodingFailuresKeepSourcePixelsAndAtomicDerivedDestinations() = forEachLocale { tag, activity ->
        val folder = File(activity.cacheDir, "$tag-encoding-${System.nanoTime()}").apply { mkdirs() }
        val source = Bitmap.createBitmap(2, 2, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.MAGENTA) }
        val original = "previous destination".toByteArray()
        try {
            // Derived encoders reject an insufficient budget before opening a temporary
            // output or invoking PNG compression. Neither path may replace the destination.
            for (format in listOf(ImageFormat.BASE64, ImageFormat.ICO)) {
                val file = File(folder, "output${format.extension}").apply { writeBytes(original) }
                CommonsPngFailureShadow.resetFailure()
                CommonsPngFailureShadow.reject = true
                val error = assertThrows(IOException::class.java) {
                    ImageExporter.encode(source, file, ExportOptions(format), 0)
                }
                assertEquals(expected(tag, "save20_encoding_budget"), error.message)
                assertNull(CommonsPngFailureShadow.rejectedBitmap)
                assertArrayEquals(original, file.readBytes())
                assertEquals(listOf(file.name), folder.listFiles()!!.map { it.name })
                assertTrue(file.delete())
            }
            for (format in listOf(ImageFormat.PNG, ImageFormat.BASE64, ImageFormat.ICO)) {
                val file = File(folder, "output${format.extension}").apply { writeBytes(original) }
                CommonsPngFailureShadow.reject = true
                val error = assertThrows(IOException::class.java) {
                    ImageExporter.encode(source, file, ExportOptions(format), 64L * 1024 * 1024)
                }
                assertEquals(expected(tag, "ui_the_encoder_did_not_finish"), error.message)
                assertNotNull(CommonsPngFailureShadow.rejectedBitmap)
                assertFalse(source.isRecycled)
                assertEquals(Color.MAGENTA, source.getPixel(0, 0))
                // Direct PNG opens/truncates its supplied output; only the derived
                // codecs have the atomic replacement contract asserted here.
                if (format != ImageFormat.PNG) assertArrayEquals(original, file.readBytes())
                assertEquals(listOf(file.name), folder.listFiles()!!.map { it.name })
                assertTrue(file.delete())
                CommonsPngFailureShadow.resetFailure()
            }
            // Disabling the fault must leave an actual successful PNG encoding path.
            val png = File(folder, "success.png")
            ImageExporter.encode(source, png, ExportOptions(ImageFormat.PNG), 64L * 1024 * 1024)
            assertTrue(png.length() > 8)
            assertArrayEquals(byteArrayOf(-119, 80, 78, 71, 13, 10, 26, 10), png.readBytes().copyOf(8))
            assertFalse(source.isRecycled)
            assertEquals(Color.MAGENTA, source.getPixel(0, 0))
        } finally { CommonsPngFailureShadow.resetFailure(); source.recycle(); folder.deleteRecursively() }
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
                assertEquals("Choose location…", dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
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
    @Test fun actualSaveExportSharePanelsKeepDistinctMessagesAndRepeatedCancel() = forEachLocale { tag, activity ->
        fun texts(view: View): List<String> =
            (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
                (if (view is ViewGroup) (0 until view.childCount).flatMap { texts(view.getChildAt(it)) } else emptyList())
        val save = expected(tag, "ui_save_explanation23")
        val export = expected(tag, "ui_export_explanation23")
        val share = preserved(tag, "ui_share_explanation34")
        for ((sharing, exporting, message) in listOf(Triple(false, false, save),
                Triple(false, true, export), Triple(true, true, share))) repeat(2) {
            var confirmations = 0
            var cancellations = 0
            val dialog = SaveOptionsDialog(activity, ExportOptions(), share = sharing,
                confirm = { confirmations++ }, cancel = { cancellations++ }, export = exporting).show()
            try {
                assertDistinctFormatAndFilenameControls(dialog.window!!.decorView, tag)
                val displayed = texts(dialog.window!!.decorView)
                assertTrue(displayed.contains(message))
                for (other in listOf(save, export, share).filter { it != message }) assertFalse(displayed.contains(other))
                assertEquals(if (sharing) expected(tag, "ui_save_and_share_41edb4")
                    else ui(if (exporting) R.string.ui_export_as23 else R.string.save20_title), shadowOf(dialog).title.toString())
                assertTrue(displayed.contains(formatLabel(tag)))
                assertEquals("Choose location…", dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(preserved(tag, "ui_cancel"), dialog.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
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
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_message"), format, "at least 2"),
            ui(R.string.formats22_animation_message, format, ui(R.string.formats22_at_least_frames, 2)))
        val filename = "drawing 100%.png"
        val detail = "provider 50% unavailable"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_saved"), filename), ui(R.string.ui_saved, filename))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_the_image_was_saved_but_android_could_not"), detail),
            ui(R.string.ui_the_image_was_saved_but_android_could_not, detail))
        assertEquals(preserved(tag, "ui_save"), ui(R.string.ui_save))
        assertEquals(preserved(tag, "save20_title"), ui(R.string.save20_title))
        assertEquals(preserved(tag, "ui_save_your_changes"), ui(R.string.ui_save_your_changes))
        assertEquals(expected(tag, "ui_save_and_share_41edb4") + "…", ui(R.string.ui_save_and_share))
    }

}
