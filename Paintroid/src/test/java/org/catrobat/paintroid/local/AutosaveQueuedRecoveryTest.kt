/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Color
import android.util.AtomicFile
import org.catrobat.paintroid.classic.AutosaveDraft
import org.catrobat.paintroid.classic.AutosaveStore
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.RasterHistory
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TemporaryFolder
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.util.concurrent.Callable
import java.util.concurrent.CountDownLatch
import java.util.concurrent.ExecutionException
import java.util.concurrent.Executor
import java.util.concurrent.Executors
import java.util.concurrent.Future
import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.RejectedExecutionException
import java.util.concurrent.TimeUnit
import java.util.concurrent.TimeoutException

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AutosaveQueuedRecoveryTest {
    @get:Rule val temporary=TemporaryFolder()
    private class QueuedExecutor: Executor {
        private val tasks=LinkedBlockingQueue<Runnable>()
        override fun execute(command: Runnable) {tasks.add(command)}
        fun runNext() {checkNotNull(tasks.poll(5,TimeUnit.SECONDS)) {"No queued write"}.run()}
    }
    private val credit=ImageCredit("https://example.org/art.png","Original 作品\nArtist 作者 👩🏽‍🎨\nhttps://example.org/artist")
    private fun metadata()=JSONObject().put("version",1)
        .put("image_credits",JSONObject().put("committed",JSONArray())
            .put("floating",ImageCredit.write(listOf(credit))).put("selection_sources_known",true))
        .put("floating_rect",JSONArray(listOf(1,2,4,4))).put("floating_rotation",17)
    private fun pixels(colour: Int)=Bitmap.createBitmap(7,5,Bitmap.Config.ARGB_8888).apply {eraseColor(colour)}
    private fun assertDraft(draft: AutosaveDraft) {
        assertEquals(7,draft.image.width);assertEquals(5,draft.image.height)
        assertEquals(Color.BLUE,draft.image.getPixel(2,3))
        assertNotNull(draft.floating)
        val floating=checkNotNull(draft.floating)
        assertEquals(3,floating.width);assertEquals(2,floating.height)
        assertEquals(Color.MAGENTA,floating.getPixel(0,0))
        assertEquals("[1,2,4,4]",draft.metadata.getJSONArray("floating_rect").toString())
        assertEquals(17,draft.metadata.getInt("floating_rotation"))
        assertEquals(listOf(credit),ImageCredit.read(draft.metadata.getJSONObject("image_credits").getJSONArray("floating")))
    }
    private fun recycle(draft: AutosaveDraft?) {draft?.image?.recycle();draft?.floating?.recycle()}
    private fun assertWaiting(result: Future<*>) {
        try {result.get(200,TimeUnit.MILLISECONDS);fail("Recovery returned before the registered write completed")}
        catch(_: TimeoutException) { /* Queue/latch is controlled explicitly; no production delay. */ }
    }

    @Test fun queuedInitialWriteIsVisibleToReplacementBeforeTheWorkerStarts() = queuedRecovery(false)
    @Test fun queuedWritePreventsReadingAnOlderCommittedDraft() = queuedRecovery(true)

    private fun queuedRecovery(previousDraft: Boolean) {
        val directory=temporary.newFolder()
        val writer=AutosaveStore(directory);val replacement=AutosaveStore(directory)
        val image=pixels(Color.BLUE)
        val floating=Bitmap.createBitmap(3,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)}
        val queue=QueuedExecutor();val threads=Executors.newFixedThreadPool(2)
        var recovery: Future<AutosaveDraft?>?=null
        try {
            if(previousDraft) {
                val old=pixels(Color.RED)
                try {writer.write(old,null,JSONObject().put("version",1))} finally {old.recycle()}
            }
            writer.submitWrite(queue) {writer.write(image,floating,metadata())}
            val started=CountDownLatch(1)
            recovery=threads.submit(Callable {
                started.countDown()
                // Cover read's own barrier as well as the Activity's exists-then-read path.
                if(previousDraft || replacement.exists()) replacement.read {_,_->} else null
            })
            assertTrue(started.await(5,TimeUnit.SECONDS));assertWaiting(recovery)
            threads.submit {queue.runNext()}.get(5,TimeUnit.SECONDS)
            val draft=recovery.get(5,TimeUnit.SECONDS)
            assertNotNull(draft);assertDraft(draft!!)
        } finally {
            threads.shutdownNow();assertTrue(threads.awaitTermination(10,TimeUnit.SECONDS))
            recovery?.takeIf {it.isDone && !it.isCancelled}?.let {recycle(it.get())}
            image.recycle();floating.recycle()
        }
    }

    @Test fun recoveryWaitsForEveryRegisteredWriteIncludingTheFinalLifecycleWrite() {
        val directory=temporary.newFolder();val writer=AutosaveStore(directory)
        val replacement=AutosaveStore(directory);val queue=QueuedExecutor()
        val image=pixels(Color.BLUE);val threads=Executors.newFixedThreadPool(2)
        var result: Future<Boolean>?=null
        try {
            writer.submitWrite(queue) {writer.write(image,null,JSONObject().put("version",1))}
            writer.submitWrite(queue) {writer.write(image,null,JSONObject().put("version",1).put("final",true))}
            val started=CountDownLatch(1)
            result=threads.submit(Callable {started.countDown();replacement.exists()})
            assertTrue(started.await(5,TimeUnit.SECONDS));assertWaiting(result)
            threads.submit {queue.runNext()}.get(5,TimeUnit.SECONDS);assertWaiting(result)
            threads.submit {queue.runNext()}.get(5,TimeUnit.SECONDS)
            assertTrue(result.get(5,TimeUnit.SECONDS))
            val draft=replacement.read {_,_->}
            try {assertTrue(draft.metadata.getBoolean("final"))} finally {recycle(draft)}
        } finally {threads.shutdownNow();assertTrue(threads.awaitTermination(10,TimeUnit.SECONDS));image.recycle()}
    }

    @Test fun rejectedSubmissionReleasesItsIntentAndPreservesTheException() {
        val directory=temporary.newFolder();val writer=AutosaveStore(directory)
        val failure=RejectedExecutionException("closed worker")
        try {writer.submitWrite(Executor {throw failure}) {fail("Rejected task must not run")};fail("Rejection must propagate")}
        catch(error: RejectedExecutionException) {assertSame(failure,error)}
        val reader=Executors.newSingleThreadExecutor()
        try {assertFalse(reader.submit(Callable {AutosaveStore(directory).exists()}).get(5,TimeUnit.SECONDS))}
        finally {reader.shutdownNow();assertTrue(reader.awaitTermination(10,TimeUnit.SECONDS))}
    }

    @Test fun inlineActionFailureReleasesExactlyOnceAndDoesNotCancelALaterIntent() {
        val directory=temporary.newFolder();val writer=AutosaveStore(directory)
        val failure=IOException("inline task failed")
        try {writer.submitWrite(Executor {it.run()}) {throw failure};fail("Failure must propagate")}
        catch(error: IOException) {assertSame(failure,error)}
        val queue=QueuedExecutor();val reader=Executors.newSingleThreadExecutor()
        try {
            writer.submitWrite(queue) { /* A second lifecycle action still owns an intent. */ }
            val started=CountDownLatch(1)
            val recovery=reader.submit(Callable {started.countDown();AutosaveStore(directory).exists()})
            assertTrue(started.await(5,TimeUnit.SECONDS));assertWaiting(recovery)
            queue.runNext();assertFalse(recovery.get(5,TimeUnit.SECONDS))
        } finally {reader.shutdownNow();assertTrue(reader.awaitTermination(10,TimeUnit.SECONDS))}
    }

    @Test fun failedAtomicWriteReleasesRecoveryAndKeepsThePreviousCompleteDraft() {
        val directory=temporary.newFolder();val writer=AutosaveStore(directory)
        val image=pixels(Color.BLUE);val queue=QueuedExecutor();val threads=Executors.newFixedThreadPool(2)
        var recovery: Future<AutosaveDraft>?=null
        try {
            writer.write(image,null,JSONObject().put("version",1).put("original",true))
            val original=writer.file.readBytes()
            val broken=RasterHistory.Snapshot(undo=listOf(RasterHistory.Entry(File(directory,"missing.rgba"),7,5)))
            writer.submitWrite(queue) {writer.write(image,null,JSONObject().put("version",1),broken)}
            val started=CountDownLatch(1)
            recovery=threads.submit(Callable {started.countDown();AutosaveStore(directory).read {_,_->}})
            assertTrue(started.await(5,TimeUnit.SECONDS));assertWaiting(recovery)
            try {threads.submit {queue.runNext()}.get(5,TimeUnit.SECONDS);fail("Missing history must fail the write")}
            catch(error: ExecutionException) {assertTrue(error.cause is IOException)}
            val draft=recovery.get(5,TimeUnit.SECONDS)
            assertEquals(Color.BLUE,draft.image.getPixel(2,3));assertTrue(draft.metadata.getBoolean("original"))
            assertArrayEquals(original,writer.file.readBytes())
            assertFalse(File(writer.file.path+".new").exists())
        } finally {
            threads.shutdownNow();assertTrue(threads.awaitTermination(10,TimeUnit.SECONDS))
            recovery?.takeIf {it.isDone && !it.isCancelled}?.let {recycle(it.get())};image.recycle()
        }
    }

    @Test fun registeringAnotherIntentAndOtherFilesDoNotWaitForBitmapCompression() {
        val directory=temporary.newFolder();val writer=AutosaveStore(directory)
        val other=AutosaveStore(temporary.newFolder())
        val queue=QueuedExecutor();val threads=Executors.newFixedThreadPool(3)
        val image=pixels(Color.BLUE);val writing=CountDownLatch(1);val release=CountDownLatch(1)
        ReflectionHelpers.setField(writer,"atomic",object: AtomicFile(writer.file) {
            override fun startWrite(): FileOutputStream {
                val stream=super.startWrite();writing.countDown()
                try {check(release.await(10,TimeUnit.SECONDS))}
                catch(error: Throwable) {super.failWrite(stream);throw error}
                return stream
            }
        })
        try {
            writer.submitWrite(threads) {writer.write(image,null,JSONObject().put("version",1))}
            assertTrue(writing.await(5,TimeUnit.SECONDS))
            // Registration uses a different monitor from the I/O lock held by the gated writer.
            threads.submit {writer.submitWrite(queue) {}}.get(2,TimeUnit.SECONDS)
            threads.submit {
                other.write(image,null,JSONObject().put("version",1))
                assertTrue(other.exists());val draft=other.read {_,_->}
                try {assertEquals(Color.BLUE,draft.image.getPixel(2,3))} finally {recycle(draft)}
            }.get(2,TimeUnit.SECONDS)
            queue.runNext();release.countDown()
            assertTrue(threads.submit(Callable {AutosaveStore(directory).exists()}).get(5,TimeUnit.SECONDS))
        } finally {
            release.countDown();threads.shutdown();assertTrue(threads.awaitTermination(10,TimeUnit.SECONDS));image.recycle()
        }
    }
}
