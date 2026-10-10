/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Color
import android.util.AtomicFile
import org.catrobat.paintroid.classic.AutosaveStore
import org.catrobat.paintroid.classic.EditorStartup
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
import java.io.FileOutputStream
import java.io.IOException
import java.util.concurrent.Callable
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executor
import java.util.concurrent.Executors
import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],manifest=Config.NONE)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AutosaveStartupRecoveryTest {
    @get:Rule val temporary=TemporaryFolder()
    private class Queue: Executor {
        val tasks=LinkedBlockingQueue<Runnable>()
        override fun execute(command: Runnable) {tasks.add(command)}
        fun next() {checkNotNull(tasks.poll(5,TimeUnit.SECONDS)).run()}
    }
    private fun image(colour: Int)=Bitmap.createBitmap(7,5,Bitmap.Config.ARGB_8888).apply {eraseColor(colour)}
    private fun metadata(text: String)=JSONObject().put("version",1).put("filename",text)

    @Test fun queuedDurableWriteKeepsStartupPendingWhileMainSentinelAndCancellationRun() {
        val directory=temporary.newFolder();val writer=AutosaveStore(directory);val reader=AutosaveStore(directory)
        val writes=Queue();val main=Queue();val worker=Executors.newSingleThreadExecutor()
        val started=CountDownLatch(1);val disposed=CountDownLatch(1)
        val pixels=image(Color.BLUE)
        writer.submitWrite(writes) {writer.write(pixels,null,metadata("latest 作品"))}
        val startup=EditorStartup(worker,main,load={started.countDown();reader.recover {reader.read {_,_->}}},
            release={it.value.image.recycle();disposed.countDown()},receive={fail("Destroyed startup published")})
        try {
            startup.start();assertTrue(started.await(5,TimeUnit.SECONDS))
            var sentinel=false;main.execute {sentinel=true};main.next();assertTrue(sentinel)
            startup.cancel();assertFalse(writer.file.exists())
            writes.next();assertTrue(disposed.await(5,TimeUnit.SECONDS))
            val draft=reader.read {_,_->}
            try {assertEquals(Color.BLUE,draft.image.getPixel(2,3));assertEquals("latest 作品",draft.metadata.getString("filename"))}
            finally {draft.image.recycle()}
            assertTrue(main.tasks.isEmpty())
        } finally {worker.shutdown();assertTrue(worker.awaitTermination(10,TimeUnit.SECONDS));pixels.recycle()}
    }

    @Test fun finalLifecycleRegistrationNeverWaitsForAnActiveRecoveryRead() {
        val store=AutosaveStore(temporary.newFolder());val threads=Executors.newFixedThreadPool(2);val writes=Queue()
        val entered=CountDownLatch(1);val finish=CountDownLatch(1)
        try {
            val reading=threads.submit(Callable {store.recover {entered.countDown();check(finish.await(10,TimeUnit.SECONDS));"old snapshot"}})
            assertTrue(entered.await(5,TimeUnit.SECONDS))
            threads.submit {store.submitWrite(writes) {}}.get(2,TimeUnit.SECONDS)
            finish.countDown();val snapshot=reading.get(5,TimeUnit.SECONDS)
            assertFalse("Registered but unexecuted work invalidates publication",store.isCurrent(snapshot))
            writes.next();assertFalse("Admission revision predates the final intent",store.isCurrent(snapshot))
        } finally {finish.countDown();threads.shutdown();assertTrue(threads.awaitTermination(10,TimeUnit.SECONDS))}
    }

    @Test fun completingANewerWriteRejectsTheQueuedOlderRecoveryResult() {
        val store=AutosaveStore(temporary.newFolder());val blue=image(Color.BLUE);val magenta=image(Color.MAGENTA)
        try {
            store.write(blue,null,metadata("old"))
            val first=store.recover {store.read {_,_->}}
            store.write(magenta,null,metadata("new 作品"))
            try {assertFalse(store.isCurrent(first));assertEquals(Color.BLUE,first.value.image.getPixel(0,0))}
            finally {first.value.image.recycle()}
            val latest=store.recover {store.read {_,_->}}
            try {assertTrue(store.isCurrent(latest));assertEquals(Color.MAGENTA,latest.value.image.getPixel(0,0));assertEquals("new 作品",latest.value.metadata.getString("filename"))}
            finally {latest.value.image.recycle()}
        } finally {blue.recycle();magenta.recycle()}
    }

    @Test fun abandonedFailedRecoveryKeepsOriginalAndCompleteSeparateCopy() {
        val store=AutosaveStore(temporary.newFolder());val original="retained unreadable draft 作品".toByteArray()
        store.file.writeBytes(original)
        val snapshot=store.recover {
            try {store.read {_,_->};fail("Corrupt draft must fail")} catch(_: Exception) {}
            store.preserveForRecovery(retainOriginal=true)
        }
        assertArrayEquals(original,store.file.readBytes());assertArrayEquals(original,snapshot.value.readBytes())
        assertTrue(store.isCurrent(snapshot));assertTrue(AutosaveStore(store.file.parentFile!!).exists())
        val pixels=image(Color.BLUE)
        try {
            store.write(pixels,null,metadata("replacement"))
            assertArrayEquals(original,snapshot.value.readBytes());assertFalse(store.isCurrent(snapshot))
        } finally {pixels.recycle()}
    }
    @Test fun explicitSyncFailurePreservesOldDraftAndPreventsPostWriteRetirement() {
        val store=AutosaveStore(temporary.newFolder());val old=image(Color.BLUE);val newer=image(Color.MAGENTA)
        var originalStream: FileOutputStream?=null
        try {
            store.write(old,null,metadata("durable old draft"));val before=store.file.readBytes()
            ReflectionHelpers.setField(store,"atomic",object: AtomicFile(store.file) {
                override fun startWrite(): FileOutputStream {
                    val stream=super.startWrite();originalStream=stream
                    return object: FileOutputStream(stream.fd) {
                        // All ZIP bytes are written; only the subsequent explicit fd.sync fails.
                        override fun flush() {super.flush();super.close()}
                    }
                }
            })
            var retired=false
            try {
                store.submitWrite(Executor {it.run()}) {store.write(newer,null,metadata("new draft"));retired=true}
                fail("A sync failure must not report a durably adopted replacement")
            } catch(_: IOException) {}
            assertFalse("No post-write credit retirement after failed durability",retired)
            assertArrayEquals(before,store.file.readBytes())
            val restored=AutosaveStore(store.file.parentFile!!).read {_,_->}
            try {assertEquals(Color.BLUE,restored.image.getPixel(2,3));assertEquals("durable old draft",restored.metadata.getString("filename"))}
            finally {restored.image.recycle()}
        } finally {runCatching {originalStream?.close()};old.recycle();newer.recycle()}
    }

}
