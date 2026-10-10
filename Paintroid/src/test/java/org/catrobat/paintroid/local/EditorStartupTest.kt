/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.catrobat.paintroid.classic.EditorStartup
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executor
import java.util.concurrent.Executors
import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

class EditorStartupTest {
    private class Queue: Executor {
        val tasks=LinkedBlockingQueue<Runnable>()
        override fun execute(command: Runnable) {tasks.add(command)}
        fun next() {checkNotNull(tasks.poll(5,TimeUnit.SECONDS)).run()}
    }
    @Test fun mainRemainsResponsiveUntilWorkerOwnedRecoveryCompletes() {
        val main=Queue();val worker=Executors.newSingleThreadExecutor()
        val entered=CountDownLatch(1);val release=CountDownLatch(1)
        var delivered=false;var sentinel=false
        val startup=EditorStartup(worker,main,load={entered.countDown();check(release.await(10,TimeUnit.SECONDS));"draft"},release={},receive={assertEquals("draft",it.getOrThrow());delivered=true})
        try {
            startup.start();assertTrue(entered.await(5,TimeUnit.SECONDS))
            main.execute {sentinel=true};main.next()
            assertTrue(sentinel);assertFalse(delivered)
            release.countDown();main.next();assertTrue(delivered)
        } finally {release.countDown();worker.shutdown();assertTrue(worker.awaitTermination(10,TimeUnit.SECONDS))}
    }
    @Test fun destroyDuringRecoveryReleasesOnceWithoutAnyUiDelivery() {
        val main=Queue();val worker=Executors.newSingleThreadExecutor()
        val entered=CountDownLatch(1);val release=CountDownLatch(1);val disposed=CountDownLatch(1)
        val count=AtomicInteger()
        val startup=EditorStartup(worker,main,load={entered.countDown();check(release.await(10,TimeUnit.SECONDS));"draft"},release={count.incrementAndGet();disposed.countDown()},receive={fail("Destroyed owner received recovery")})
        try {
            startup.start();assertTrue(entered.await(5,TimeUnit.SECONDS));startup.cancel();release.countDown()
            assertTrue(disposed.await(5,TimeUnit.SECONDS));assertEquals(1,count.get());assertTrue(main.tasks.isEmpty())
        } finally {release.countDown();worker.shutdown();assertTrue(worker.awaitTermination(10,TimeUnit.SECONDS))}
    }
    @Test fun destroyAfterWorkerCompletionBeforeUiDeliveryTransfersDisposalBackToWorker() {
        val main=Queue();val worker=Queue();var releases=0
        val startup=EditorStartup(worker,main,load={"draft"},release={releases++},receive={fail("Cancelled queued delivery ran")})
        startup.start();worker.next();startup.cancel()
        assertEquals(0,releases);main.next();worker.next();assertEquals(1,releases)
        startup.cancel();assertEquals(0,worker.tasks.size)
    }
    @Test fun destructionBeforeQueuedLoadDoesNotReadOrPublishAnyDraft() {
        val main=Queue();val worker=Queue()
        val startup=EditorStartup<String>(worker,main,load={fail("Cancelled startup read storage");"unused"},
            release={fail("Nothing was allocated")},receive={fail("Cancelled startup published")})
        startup.start();startup.cancel();worker.next();assertTrue(main.tasks.isEmpty())
    }
    @Test fun failedLoadIsReportedWithoutInventingARecoveredDocument() {
        val main=Queue();val worker=Queue();val error=java.io.IOException("retained draft")
        var failure: Throwable?=null
        val startup=EditorStartup<String>(worker,main,load={throw error},release={fail("No result to release")},receive={failure=it.exceptionOrNull()})
        startup.start();worker.next();main.next();assertSame(error,failure)
    }
}
