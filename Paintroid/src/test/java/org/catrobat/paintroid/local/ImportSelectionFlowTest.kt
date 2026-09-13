/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.graphics.Rect
import android.os.Looper
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
import java.io.File
import java.util.Base64
import java.util.concurrent.AbstractExecutorService
import java.util.concurrent.TimeUnit

/** Test the user's decision and staged-file ownership, beyond container sniffing. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ImportSelectionFlowTest {
    private lateinit var controller: ActivityController<Activity>
    private lateinit var activity: Activity
    private lateinit var directory: File
    private lateinit var worker: QueuedWorker
    private var selection: ImportSelection? = null
    private var selected: ImportedImage? = null
    private var cancelled = 0
    private var failure: Throwable? = null

    @Before fun start() {
        controller = Robolectric.buildActivity(Activity::class.java)
        activity = controller.setup().get()
        directory = File(activity.cacheDir, "import-selection-${System.nanoTime()}").apply { mkdirs() }
        worker = QueuedWorker()
    }

    @After fun stop() {
        selection?.dispose()
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        worker.drain()
        if (!activity.isDestroyed) controller.pause().stop().destroy()
        directory.deleteRecursively()
    }

    private fun begin(file: File) {
        selection = ImportSelection(activity, worker, { 0L }, { selected = it }, { cancelled++ }, { failure = it })
        selection!!.start(file, "provider-name.bin")
        worker.runNext()
        assertNull(failure)
    }

    private fun warning() = checkNotNull(ShadowAlertDialog.getLatestAlertDialog()).also {
        assertTrue(it.isShowing)
        assertNull("Pixels must not be imported before the user's decision", selected)
    }

    @Test fun animatedGifWaitsForApprovalThenTransfersTheStagedFileToItsOwner() {
        val file = File(directory, "source.image").apply { writeBytes(Base64.getDecoder().decode(GIF)) }
        begin(file)
        val dialog = warning()
        assertTrue(shadowOf(dialog).message.toString().contains("GIF"))
        assertTrue(shadowOf(dialog).message.toString().contains("3"))
        assertTrue(file.exists())
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        worker.drain()
        assertNull(failure)
        assertEquals(0, cancelled)
        assertEquals(ImageDimensions(1, 1), selected!!.dimensions)
        assertEquals(0, selected!!.pageIndex)
        assertEquals(file, selected!!.file)
        assertFalse(dialog.isShowing)
        selection!!.dispose()
        assertTrue("The completed selection no longer owns the caller's file", file.exists())
    }

    @Test fun base64AnimationGetsTheSameWarningAndCancelLeavesTheProviderOriginalIntact() {
        val original = File(directory, "provider.txt").apply { writeText("data:image/gif;base64,$GIF\n") }
        val bytes = original.readBytes()
        val staged = File(directory, "staged.image")
        original.inputStream().use { ImportFiles.copy(it, staged) }
        begin(staged)
        val dialog = warning()
        assertArrayEquals(Base64.getDecoder().decode(GIF), staged.readBytes())
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
        worker.drain()
        assertEquals(1, cancelled)
        assertNull(selected)
        assertNull(failure)
        assertFalse(staged.exists())
        assertArrayEquals(bytes, original.readBytes())
    }

    @Test fun apngAndAnimatedWebpShowWarningsAndBackCancelsWithoutImporting() {
        for ((name, encoded) in listOf("APNG" to APNG, "WebP" to WEBP)) {
            val staged = File(directory, "$name.image").apply { writeBytes(Base64.getDecoder().decode(encoded)) }
            begin(staged)
            val dialog = warning()
            assertTrue(shadowOf(dialog).message.toString().contains(name))
            dialog.cancel()
            worker.drain()
            assertFalse(staged.exists())
            assertNull(selected)
            assertNull(failure)
        }
        assertEquals(2, cancelled)
    }

    @Test fun disposalWhileInspectionIsQueuedSuppressesCallbacksAndDeletesTheStagedFile() {
        val staged = File(directory, "abandoned.image").apply { writeBytes(Base64.getDecoder().decode(GIF)) }
        selection = ImportSelection(activity, worker, { 0L }, { selected = it }, { cancelled++ }, { failure = it })
        selection!!.start(staged, "abandoned.gif")
        selection!!.dispose()
        worker.drain()
        assertFalse(staged.exists())
        assertNull(selected)
        assertNull(failure)
        assertEquals(0, cancelled)
        assertFalse(ShadowAlertDialog.getLatestAlertDialog()?.isShowing == true)
    }

    @Test fun selectedAssemblyPageSurvivesCropUndoAndReloadWhileOldProjectsDefaultToFirstPage() {
        val folder = File(directory, "assembly")
        val model = ImageAssembly(folder)
        val file = File(folder, "document.image").apply { writeText("original remains on disk") }
        val item = AssemblyImage("page", file, "scan.tiff", null, ImageDimensions(60, 80), pageIndex = 2)
        model.add(listOf(item))
        model.crop("page", Rect(5, 6, 50, 70))
        model.place("page", Attachment(null, null))
        model.undo()
        assertEquals(2, model.image("page").pageIndex)
        model.redo()
        val reopened = ImageAssembly(folder)
        assertEquals(2, reopened.image("page").pageIndex)
        assertEquals(Rect(5, 6, 50, 70), reopened.image("page").crop)
        assertEquals(model.layout(), reopened.layout())
        val stateFile = File(folder, "project.json")
        val state = org.json.JSONObject(stateFile.readText())
        state.getJSONArray("images").getJSONObject(0).remove("page")
        state.put("version", 2)
        stateFile.writeText(state.toString())
        assertEquals(0, ImageAssembly(folder).image("page").pageIndex)
        assertTrue(file.exists())
    }

    /** Separate worker thread with explicit boundaries, so cancellation races are deterministic. */
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
        // Same tiny, independent fixtures used by the on-device static-decoder checks.
        private const val GIF = "R0lGODlhAQABAIAAAAAAAP///yH5BAAKAAAALAAAAAABAAEAgAAAAP///wICRAEAIfkEAAoAAAAsAAAAAAEAAQCAAAAA////AgJMAQAh+QQACgAAACwAAAAAAQABAIAAAAD///8CAkQBADs="
        private const val APNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACGFjVEwAAAADAAAAAM7tusAAAAAaZmNUTAAAAAAAAAABAAAAAQAAAAAAAAAAAAEACgAAWn8w0AAAAA1JREFUeJxj+M/A8B8ABQAB/4mZPR0AAAAaZmNUTAAAAAEAAAABAAAAAQAAAAAAAAAAAAEACgAAwQzaBAAAABFmZEFUAAAAAnicY2Bg+P8fAAMCAf/1e6XXAAAAGmZjVEwAAAADAAAAAQAAAAEAAAAAAAAAAAABAAoAACyaCe0AAAARZmRBVAAAAAR4nGP4z8DwHwAFAAH/YlfY0gAAAABJRU5ErkJggg=="
        private const val WEBP = "UklGRrQAAABXRUJQVlA4WAoAAAACAAAAAAAAAAAAQU5JTQYAAAAAAAAAAABBTk1GKAAAAAAAAAAAAAAAAAAAAGQAAAJWUDhMDwAAAC8AAAAABxD9j/4HIqL/AQBBTk1GKAAAAAAAAAAAAAAAAAAAAGQAAAJWUDhMDwAAAC8AAAAABxDR//4HIqL/AQBBTk1GKAAAAAAAAAAAAAAAAAAAAGQAAAJWUDhMDwAAAC8AAAAABxD9j/4HIqL/AQA="
    }
}
