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

/** Exact compiled values and real failure/recovery consumers, not native/device acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class NynorskRemainingP0Test {
    private lateinit var beforeResources: Resources
    private lateinit var nynorsk: Context
    private val fixture by lazy {
        JSONObject(File("../tools/fixtures/current_localization/nynorsk_p0_remaining_wording.json").readText())
    }
    private fun expected(key: String) = RecoveredTrioPriorityExpectations.current("nn",key,
        fixture.getJSONObject("values").getJSONObject(key).getString("nn")).removeSurrounding("\"")

    @Before fun useNynorsk() {
        beforeResources = PaintApplication.currentResources
        val app = RuntimeEnvironment.getApplication() as Context
        nynorsk = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("nn"))
        })
        PaintApplication.currentResources = nynorsk.resources
    }
    @After fun restoreResources() { PaintApplication.currentResources = beforeResources }

    @Test fun all72WholeCompiledValuesMatchTheIndependentFixtureAndHeldFallbackStaysEnglish() {
        val values = fixture.getJSONObject("values")
        assertEquals(72, values.length())
        for (key in values.keys()) {
            val id = nynorsk.resources.getIdentifier(key, "string", nynorsk.packageName)
            assertNotEquals(key, 0, id)
            assertEquals(key, expected(key), nynorsk.getString(id))
        }
        assertEquals(RecoveredTrioPriorityExpectations.display("nn","ui_load_image"), ui(R.string.ui_load_image))
        assertEquals(String.format(Locale.forLanguageTag("nn"),RecoveredTrioPriorityExpectations.display("nn","formats22_at_least_frames"),2), ui(R.string.formats22_at_least_frames, 2))
        assertEquals("Save as PNG…", ui(R.string.ui_save_as_png))
        assertEquals(RecoveredTrioPriorityExpectations.display("nn","ui_no_resize_fits_decoder_memory"), ui(R.string.ui_no_resize_fits_decoder_memory))
        assertEquals(expected("ui_history_unavailable34"), ui(R.string.ui_history_unavailable34))
    }

    @Test fun realMemoryAdmissionFailureRetainsAllFourArgumentsAndNoAutomaticResizeClaim() {
        val mib = 1024L * 1024
        val policy = ImageMemoryPolicy.calculate(256 * mib, 0, 96 * mib, 0, false)
        assertEquals(0L, policy.maxPixels())
        val failure = assertThrows(ImageSizeException::class.java) { policy.check(1000, 2000) }
        val message = String.format(Locale.forLanguageTag("nn"), expected("ui_d_d_pixels_2f_mp_exceeds_the_current"), 1000, 2000, 2.0, 0.0)
        assertEquals(message, failure.message)
        assertTrue(message.contains("1000 × 2000 pikslar (2,00 MP)"))
        assertTrue(message.endsWith("Det vart ikkje gjort noka automatisk skalering."))
        val detail = "provider 100% unavailable"
        assertEquals("Biletet vart lagra, men Android kunne ikkje starta deling: $detail", ui(R.string.ui_the_image_was_saved_but_android_could_not, detail))
    }

    private fun recoveryContext(folder: File): Context = object : ContextWrapper(nynorsk) {
        override fun getFilesDir(): File = folder
        override fun getCacheDir(): File = File(folder, "cache").apply { mkdirs() }
    }

    @Test fun unreadableDraftProducesTheReviewedNoticeOnlyAfterPreservingItsExactBytes() {
        val folder = File(nynorsk.cacheDir, "nn-failed-recovery-${System.nanoTime()}").apply { mkdirs() }
        val store = AutosaveStore(folder)
        val original = "deliberately not a ZIP draft".toByteArray()
        store.file.writeBytes(original)
        var recovered: RecoveredEditor? = null
        try {
            recovered = recoverEditor(recoveryContext(folder), store).value
            assertFalse(recovered.restored)
            assertFalse(recovered.autosaveBlocked)
            assertEquals(expected("ui_previous_draft_kept_for_recovery"), recovered.draftStatus)
            assertEquals(String.format(Locale.forLanguageTag("nn"), expected("ui_a_separate_recovery_copy_has_been_kept_use"), expected("ui_the_previous_draft_could_not_be_restored")), recovered.recoveryNotice)
            assertArrayEquals(original, store.file.readBytes())
            val copies = store.recoveryCopies()
            assertEquals(1, copies.size)
            assertArrayEquals(original, copies.single().readBytes())
        } finally { recovered?.document?.close(); folder.deleteRecursively() }
    }

    @Test fun recoveredDraftKeepsUnsavedStatePixelsAndItsOneOptionalFloatingSelection() {
        val folder = File(nynorsk.cacheDir, "nn-restored-draft-${System.nanoTime()}").apply { mkdirs() }
        val store = AutosaveStore(folder)
        val image = Bitmap.createBitmap(8, 6, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.RED) }
        val floating = Bitmap.createBitmap(3, 2, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.BLUE) }
        var recovered: RecoveredEditor? = null
        try {
            val metadata = JSONObject().put("version", 1).put("dirty", true)
                .put("floating_rect", JSONArray(listOf(1.0, 2.0, 4.0, 4.0))).put("floating_rotation", 0.0)
            store.write(image, floating, metadata)
            recovered = recoverEditor(recoveryContext(folder), store).value
            assertTrue(recovered.restored)
            assertTrue("Draft recovery must not mark explicit Save complete", recovered.document.dirty)
            assertNull(recovered.savedTarget)
            assertNull(recovered.recoveryNotice)
            assertEquals(expected("ui_draft_restored"), recovered.draftStatus)
            assertEquals(expected("ui_recovered_image"), recovered.filename)
            assertEquals(8, recovered.document.bitmap.width); assertEquals(6, recovered.document.bitmap.height)
            assertEquals(Color.RED, recovered.document.bitmap.getPixel(0, 0))
            val selected = checkNotNull(recovered.document.selection)
            assertEquals(3, selected.image.width); assertEquals(2, selected.image.height)
            assertEquals(Color.BLUE, selected.image.getPixel(0, 0)); assertTrue(selected.floating)
            assertTrue(store.recoveryCopies().isEmpty())
        } finally { recovered?.document?.close(); image.recycle(); floating.recycle(); folder.deleteRecursively() }
    }
}
