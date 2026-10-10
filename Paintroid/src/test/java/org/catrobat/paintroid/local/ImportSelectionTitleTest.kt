/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.os.Looper
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.ByteArrayOutputStream
import java.io.File
import java.util.Base64
import java.util.Locale
import java.util.concurrent.AbstractExecutorService
import java.util.concurrent.TimeUnit

/** A01: exercise the production scanner -> dialog -> decision path, not a copied title function. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ImportSelectionTitleTest {
    private lateinit var controller: ActivityController<Activity>
    private lateinit var activity: Activity
    private lateinit var directory: File
    private lateinit var worker: QueuedWorker
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    private lateinit var previousResources: android.content.res.Resources
    private var selection: ImportSelection? = null
    private var selected: ImportedImage? = null
    private var selectedCalls = 0
    private var cancelled = 0
    private var failure: Throwable? = null

    @Before fun start() {
        controller = Robolectric.buildActivity(Activity::class.java)
        activity = controller.setup().get()
        previousLocale = Locale.getDefault()
        previousTag = AppLanguage.selectedTag(activity)
        previousResources = PaintApplication.currentResources
        language("en-US")
        directory = File(activity.cacheDir, "import-title-${System.nanoTime()}").apply { mkdirs() }
        worker = QueuedWorker()
    }

    @After fun stop() {
        selection?.dispose()
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        worker.drain()
        AppLanguage.select(activity, previousTag)
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
        if (!activity.isDestroyed) controller.pause().stop().destroy()
        directory.deleteRecursively()
    }

    private fun language(tag: String) {
        AppLanguage.select(activity, tag)
        AppLanguage.refresh(activity)
    }

    private fun begin(bytes: ByteArray, expectedInfo: AnimationInfo?): File {
        selection?.dispose()
        selected = null; selectedCalls = 0; cancelled = 0; failure = null
        val file = File.createTempFile("source-", ".unrelated-extension", directory).apply { writeBytes(bytes) }
        assertEquals("Fixture must exercise the intended production scanner state", expectedInfo, AnimationInfo.inspect(file))
        selection = ImportSelection(activity, worker, { 0L },
            { selected = it; selectedCalls++ }, { cancelled++ }, { failure = it })
        selection!!.start(file, "provider-name.bin")
        worker.runNext()
        assertNull(failure)
        return file
    }

    private fun warning(title: String, message: String, positive: String = "Open still image"): AlertDialog {
        val dialog = checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
        assertTrue(dialog.isShowing)
        assertEquals(title, shadowOf(dialog).title.toString())
        assertEquals(message, shadowOf(dialog).message.toString())
        assertEquals(positive, dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
        assertEquals(ui(R.string.ui_cancel), dialog.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
        assertNull("No selection before a decision", selected)
        assertEquals(0, selectedCalls)
        return dialog
    }

    private fun confirmedMessage(format: String, count: String, poster: Boolean = false) =
        ui(R.string.formats22_animation_message, format, count) + "\n\n" +
            ui(if (poster) R.string.formats22_animation_poster else R.string.formats22_animation_still)

    private fun cancel(dialog: AlertDialog, file: File, dismiss: Boolean = false) {
        if (dismiss) dialog.cancel() else dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
        worker.drain()
        assertFalse(dialog.isShowing)
        assertEquals(1, cancelled)
        assertEquals(0, selectedCalls)
        assertNull(selected)
        assertNull(failure)
        assertFalse(file.exists())
    }

    @Test fun zeroAndOneProvenFramesUseNeutralTitleAndOnlyTheUncertainBody() {
        val fixtures = listOf(
            cappedGif(0) to AnimationInfo("GIF", 0, false, false),
            cappedGif(1) to AnimationInfo("GIF", 1, false, false),
            cappedPng() to AnimationInfo("PNG", 0, false, false)
        )
        for ((bytes, info) in fixtures) {
            val file = begin(bytes, info)
            val dialog = warning("Open still image", ui(R.string.formats22_animation_unknown, info.format))
            cancel(dialog, file, dismiss = info.frameCount == 1)
        }
    }

    @Test fun exactGifAndWebpKeepTheConfirmedTitleAndOpenFirstImageExactlyOnce() {
        for ((format, encoded) in listOf("GIF" to GIF, "WebP" to WEBP)) {
            val file = begin(decode(encoded), AnimationInfo(format, 3, true, false))
            val dialog = warning("Animated image", confirmedMessage(format, "3"))
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            worker.drain(); worker.drain()
            assertEquals(1, selectedCalls)
            assertEquals(0, selected!!.pageIndex)
            assertEquals(file, selected!!.file)
            assertEquals(0, cancelled)
            assertNull(failure)
            assertFalse(dialog.isShowing)
            selection!!.dispose()
            assertTrue("Ownership has transferred to the selected-image caller", file.exists())
        }
    }

    @Test fun provenLowerBoundKeepsConfirmedTitleAndAtLeastCount() {
        val file = begin(cappedGif(2), AnimationInfo("GIF", 2, false, false))
        cancel(warning("Animated image", confirmedMessage("GIF", ui(R.string.formats22_at_least_frames, 2))), file)
    }

    @Test fun bothApngDefaultImageOutcomesKeepConfirmedTitleAndTheirOwnBody() {
        for ((poster, encoded) in listOf(false to APNG, true to APNG_POSTER)) {
            val file = begin(decode(encoded), AnimationInfo("APNG", 3, true, poster))
            cancel(warning("Animated image", confirmedMessage("APNG", "3", poster)), file)
        }
    }

    @Test fun brazilianPortugueseUsesTheExistingNeutralAndConfirmedTitles() {
        language("pt-BR")
        var file = begin(cappedGif(0), AnimationInfo("GIF", 0, false, false))
        cancel(warning("Abrir imagem estática", ui(R.string.formats22_animation_unknown, "GIF"), "Abrir imagem estática"), file)
        file = begin(decode(APNG_POSTER), AnimationInfo("APNG", 3, true, true))
        cancel(warning("Imagem animada", confirmedMessage("APNG", "3", true), "Abrir imagem estática"), file)
    }

    @Test fun incompleteWelshCatalogueRetainsDefaultEnglishFallback() {
        // cy is offered but has no animation-warning keys at this candidate's base.
        language("cy")
        val file = begin(cappedPng(), AnimationInfo("PNG", 0, false, false))
        val message = "This PNG is too complex to confirm whether it contains multiple frames. " +
            "AN Paint will open only a still image and will not preserve any animation."
        cancel(warning("Open still image", message), file)
    }

    @Test fun ordinarySingleFrameInputsStillBypassTheWarning() {
        for (encoded in listOf(STILL_GIF, STILL_PNG)) {
            val file = begin(decode(encoded), null)
            worker.drain()
            assertFalse(ShadowAlertDialog.getLatestAlertDialog()?.isShowing == true)
            assertEquals(1, selectedCalls)
            assertEquals(0, selected!!.pageIndex)
            assertEquals(file, selected!!.file)
            assertEquals(0, cancelled)
            assertNull(failure)
        }
    }

    @Test fun uncertainOpenStillTransfersTheFirstImageExactlyOnce() {
        val file = begin(cappedGif(1), AnimationInfo("GIF", 1, false, false))
        val dialog = warning("Open still image", ui(R.string.formats22_animation_unknown, "GIF"))
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        worker.drain(); worker.drain()
        assertEquals(1, selectedCalls)
        assertEquals(0, selected!!.pageIndex)
        assertEquals(file, selected!!.file)
        assertEquals(0, cancelled)
        assertNull(failure)
        selection!!.dispose()
        assertTrue(file.exists())
    }

    @Test fun disposalAfterUncertainApprovalSuppressesQueuedSelection() {
        val file = begin(cappedGif(1), AnimationInfo("GIF", 1, false, false))
        val dialog = warning("Open still image", ui(R.string.formats22_animation_unknown, "GIF"))
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        selection!!.dispose()
        worker.drain()
        assertEquals(0, selectedCalls)
        assertEquals(0, cancelled)
        assertNull(failure)
        assertFalse(file.exists())
    }

    private fun cappedGif(provenFrames: Int): ByteArray = ByteArrayOutputStream().apply {
        write(decode(GIF_HEADER))
        repeat(provenFrames) { write(decode(GIF_FRAME)) }
        // The real scanner's work cap is 100,000 blocks, not a mocked result.
        repeat(100_001) { write(byteArrayOf(0x21, 0xfe.toByte(), 1, 0x78, 0)) }
        repeat((2 - provenFrames).coerceAtLeast(0)) { write(decode(GIF_FRAME)) }
        write(0x3b)
    }.toByteArray()

    private fun cappedPng(): ByteArray = ByteArrayOutputStream().apply {
        val still = decode(STILL_PNG)
        write(still, 0, 33) // signature and IHDR
        // Empty ancillary tEXt chunks; CRC is real, though skipped by the scanner.
        repeat(100_001) { write(byteArrayOf(0, 0, 0, 0, 0x74, 0x45, 0x58, 0x74, 0x96.toByte(), 0x42, 0xc5.toByte(), 0x85.toByte())) }
        write(still, 33, still.size - 33)
    }.toByteArray()

    private fun decode(encoded: String) = Base64.getDecoder().decode(encoded)

    private class QueuedWorker : AbstractExecutorService() {
        private val queue = java.util.ArrayDeque<Runnable>()
        private var stopped = false
        override fun execute(command: Runnable) { check(!stopped); queue.addLast(command) }
        override fun shutdown() { stopped = true }
        override fun shutdownNow(): MutableList<Runnable> = queue.toMutableList().also { queue.clear(); stopped = true }
        override fun isShutdown() = stopped
        override fun isTerminated() = stopped && queue.isEmpty()
        override fun awaitTermination(timeout: Long, unit: TimeUnit) = isTerminated()
        fun runNext() {
            assertFalse("Expected queued import work", queue.isEmpty())
            val job = queue.removeFirst()
            var error: Throwable? = null
            val thread = Thread { try { job.run() } catch (caught: Throwable) { error = caught } }
            thread.start(); thread.join(10_000)
            assertFalse("Import worker did not finish", thread.isAlive)
            error?.let { throw AssertionError("Import worker failed", it) }
            shadowOf(Looper.getMainLooper()).idle()
        }
        fun drain() {
            shadowOf(Looper.getMainLooper()).idle()
            repeat(20) { if (queue.isEmpty()) return; runNext() }
            fail("Import worker did not settle")
        }
    }

    companion object {
        private const val GIF_HEADER = "R0lGODlhAQABAIAAAAAAAP///w=="
        private const val GIF_FRAME = "LAAAAAABAAEAAAICRAEA"
        private const val STILL_GIF = "R0lGODlhAQABAIAAAAAAAP///yH5BAAKAAAALAAAAAABAAEAAAICRAEAOw=="
        private const val STILL_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/iZk9HQAAAABJRU5ErkJggg=="
        private const val GIF = "R0lGODlhAQABAIAAAAAAAP///yH5BAAKAAAALAAAAAABAAEAgAAAAP///wICRAEAIfkEAAoAAAAsAAAAAAEAAQCAAAAA////AgJMAQAh+QQACgAAACwAAAAAAQABAIAAAAD///8CAkQBADs="
        private const val APNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACGFjVEwAAAADAAAAAM7tusAAAAAaZmNUTAAAAAAAAAABAAAAAQAAAAAAAAAAAAEACgAAWn8w0AAAAA1JREFUeJxj+M/A8B8ABQAB/4mZPR0AAAAaZmNUTAAAAAEAAAABAAAAAQAAAAAAAAAAAAEACgAAwQzaBAAAABFmZEFUAAAAAnicY2Bg+P8fAAMCAf/1e6XXAAAAGmZjVEwAAAADAAAAAQAAAAEAAAAAAAAAAAABAAoAACyaCe0AAAARZmRBVAAAAAR4nGP4z8DwHwAFAAH/YlfY0gAAAABJRU5ErkJggg=="
        private const val APNG_POSTER = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACGFjVEwAAAADAAAAAM7tusAAAAANSURBVHicY2D4z/AfAAQBAf9x60flAAAAGmZjVEwAAAAAAAAAAQAAAAEAAAAAAAAAAAABAAoAAFp/MNAAAAARZmRBVAAAAAF4nGP4z8DwHwAFAAH/5vS2vwAAABpmY1RMAAAAAgAAAAEAAAABAAAAAAAAAAAAAQAKAAC36eM5AAAAEWZkQVQAAAADeJxjYGD4/x8AAwIB/2h0RKEAAAAaZmNUTAAAAAQAAAABAAAAAQAAAAAAAAAAAAEACgAAWiORQwAAABFmZEFUAAAABXicY/jPwPAfAAUAAf//WDmkAAAAAElFTkSuQmCC"
        private const val WEBP = "UklGRrQAAABXRUJQVlA4WAoAAAACAAAAAAAAAAAAQU5JTQYAAAAAAAAAAABBTk1GKAAAAAAAAAAAAAAAAAAAAGQAAAJWUDhMDwAAAC8AAAAABxD9j/4HIqL/AQBBTk1GKAAAAAAAAAAAAAAAAAAAAGQAAAJWUDhMDwAAAC8AAAAABxDR//4HIqL/AQBBTk1GKAAAAAAAAAAAAAAAAAAAAGQAAAJWUDhMDwAAAC8AAAAABxD9j/4HIqL/AQA="
    }
}
