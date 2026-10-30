/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.ContextWrapper
import android.content.res.Configuration
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
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.util.Locale

/** Full reviewed values and actual failure/recovery consumers, not native/device acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class DanishNorwegianP0Test {
    private lateinit var previousResources: Resources
    private val fixture by lazy {
        NordicPriorityExpectations.project(JSONObject(File("../tools/fixtures/current_localization/danish_norwegian_p0_wording.json").readText()))
    }
    private fun expected(tag: String, key: String) = fixture.getJSONObject("values")
        .getJSONObject(key).getString(tag).removeSurrounding("\"")

    @Before fun rememberResources() { previousResources = PaintApplication.currentResources }
    @After fun restoreResources() { PaintApplication.currentResources = previousResources }

    private fun forEachLocale(check: (String, Context) -> Unit) {
        val app = RuntimeEnvironment.getApplication() as Context
        for (tag in listOf("da", "no")) {
            val context = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
                setLocale(AppLanguage.resourceLocale(Locale.forLanguageTag(tag)))
            })
            try {
                PaintApplication.currentResources = context.resources
                check(tag, context)
            } finally { PaintApplication.currentResources = previousResources }
        }
    }

    @Test fun all78CompiledValuesAndInheritedValuesRespectFinitePrioritySuccessors() = forEachLocale { tag, context ->
        val values = fixture.getJSONObject("values")
        assertEquals(78, values.length())
        for (key in values.keys()) {
            val id = context.resources.getIdentifier(key, "string", context.packageName)
            assertNotEquals("$tag/$key", 0, id)
            assertEquals("$tag/$key", expected(tag, key), context.getString(id))
        }
        val preserved = fixture.getJSONObject("preserved_values").getJSONObject(tag)
        assertEquals(if (tag == "da") 127 else 115, preserved.length())
        for (key in preserved.keys()) {
            assertFalse("The missing-only batch must not replace $tag/$key", values.has(key))
            val id = context.resources.getIdentifier(key, "string", context.packageName)
            assertNotEquals("$tag/$key", 0, id)
            assertEquals("Inherited $tag/$key", preserved.getJSONObject(key).getString("value").removeSurrounding("\""), context.getString(id))
        }
        assertEquals(NordicPriorityExpectations.display(tag,"save20_file_format"), ui(R.string.save20_file_format))
        assertEquals(if (tag == "da") "Gem ændringer?" else "Lagre endringer?", ui(R.string.ui_save_your_changes))
        assertEquals(NordicPriorityExpectations.display(tag,"ui_load_image"), ui(R.string.ui_load_image))
        assertEquals(String.format(Locale.forLanguageTag(tag),NordicPriorityExpectations.display(tag,"formats22_at_least_frames"),2), ui(R.string.formats22_at_least_frames, 2))
        assertEquals(NordicPriorityExpectations.display(tag,"ui_choose_location"), ui(R.string.ui_choose_location))
        assertEquals("Image assembly…", ui(R.string.ui_image_assembly))
        assertEquals(NordicPriorityExpectations.display(tag,"ui_no_resize_fits_decoder_memory"), ui(R.string.ui_no_resize_fits_decoder_memory))
        assertEquals(PriorityWordingExpectations.residual(tag,"formats22_derived_exported","PNG exported. Your full drawing still has unsaved changes; save a full image copy before replacing it.", "PNG"), ui(R.string.formats22_derived_exported, "PNG"))
        assertEquals(PriorityWordingExpectations.residual(tag,"ui_save_as","Save as PNG", "PNG"), ui(R.string.ui_save_as, "PNG"))
        assertEquals(PriorityWordingExpectations.residual(tag,"ui_save_as_jpeg","Save as JPEG…"), ui(R.string.ui_save_as_jpeg))
        assertEquals(PriorityWordingExpectations.residual(tag,"ui_save_as_jpeg_xl","Save as JPEG XL…"), ui(R.string.ui_save_as_jpeg_xl))
        assertEquals(PriorityWordingExpectations.residual(tag,"ui_save_as_png","Save as PNG…"), ui(R.string.ui_save_as_png))
    }

    @Test fun realMemoryAdmissionFailureFormatsAllArgumentsWithoutClaimingAutomaticResize() = forEachLocale { tag, _ ->
        val mib = 1024L * 1024
        val policy = ImageMemoryPolicy.calculate(256 * mib, 0, 96 * mib, 0, false)
        assertEquals(0L, policy.maxPixels())
        val failure = assertThrows(ImageSizeException::class.java) { policy.check(1000, 2000) }
        val message = String.format(Locale.forLanguageTag(tag), expected(tag, "ui_d_d_pixels_2f_mp_exceeds_the_current"), 1000, 2000, 2.0, 0.0)
        assertEquals(message, failure.message)
        assertTrue(message.contains("1000 × 2000"))
        assertTrue(message.contains("(2,00 MP)")); assertTrue(message.contains("0,00 MP"))
        assertTrue(message.endsWith(if (tag == "da") "Der blev ikke foretaget automatisk skalering." else "Ingen automatisk skalering ble utført."))
        val detail = "provider 100% unavailable"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_the_image_was_saved_but_android_could_not"), detail),
            ui(R.string.ui_the_image_was_saved_but_android_could_not, detail))
    }

    private fun recoveryContext(context: Context, folder: File): Context = object : ContextWrapper(context) {
        override fun getFilesDir(): File = folder
        override fun getCacheDir(): File = File(folder, "cache").apply { mkdirs() }
    }

    @Test fun failedDraftRecoveryReportsPreservationOnlyAfterKeepingItsExactBytes() = forEachLocale { tag, context ->
        val folder = File(context.cacheDir, "$tag-failed-recovery-${System.nanoTime()}").apply { mkdirs() }
        val store = AutosaveStore(folder)
        val original = "deliberately not a ZIP draft".toByteArray()
        store.file.writeBytes(original)
        var recovered: RecoveredEditor? = null
        try {
            recovered = recoverEditor(recoveryContext(context, folder), store).value
            assertFalse(recovered.restored); assertFalse(recovered.autosaveBlocked)
            assertEquals(expected(tag, "ui_previous_draft_kept_for_recovery"), recovered.draftStatus)
            assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_a_separate_recovery_copy_has_been_kept_use"),
                expected(tag, "ui_the_previous_draft_could_not_be_restored")), recovered.recoveryNotice)
            assertArrayEquals(original, store.file.readBytes())
            val copies = store.recoveryCopies()
            assertEquals(1, copies.size)
            assertArrayEquals(original, copies.single().readBytes())
        } finally { recovered?.document?.close(); folder.deleteRecursively() }
    }

    @Test fun recoveredDraftRetainsUnsavedPixelsAndOneFloatingSelectionWithoutSaveAssociation() = forEachLocale { tag, context ->
        val folder = File(context.cacheDir, "$tag-restored-draft-${System.nanoTime()}").apply { mkdirs() }
        val store = AutosaveStore(folder)
        val image = Bitmap.createBitmap(8, 6, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.RED) }
        val floating = Bitmap.createBitmap(3, 2, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.BLUE) }
        var recovered: RecoveredEditor? = null
        try {
            val metadata = JSONObject().put("version", 1).put("dirty", true)
                .put("floating_rect", JSONArray(listOf(1.0, 2.0, 4.0, 4.0))).put("floating_rotation", 0.0)
            store.write(image, floating, metadata)
            recovered = recoverEditor(recoveryContext(context, folder), store).value
            assertTrue(recovered.restored)
            assertTrue("Draft recovery must not mark explicit Save complete", recovered.document.dirty)
            assertNull(recovered.savedTarget); assertNull(recovered.recoveryNotice)
            assertEquals(expected(tag, "ui_draft_restored"), recovered.draftStatus)
            assertEquals(expected(tag, "ui_recovered_image"), recovered.filename)
            assertEquals(8, recovered.document.bitmap.width); assertEquals(6, recovered.document.bitmap.height)
            assertEquals(Color.RED, recovered.document.bitmap.getPixel(0, 0))
            val selected = checkNotNull(recovered.document.selection)
            assertEquals(3, selected.image.width); assertEquals(2, selected.image.height)
            assertEquals(Color.BLUE, selected.image.getPixel(0, 0)); assertTrue(selected.floating)
            assertTrue(store.recoveryCopies().isEmpty())
        } finally { recovered?.document?.close(); image.recycle(); floating.recycle(); folder.deleteRecursively() }
    }
}
