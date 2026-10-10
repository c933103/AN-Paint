/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.ActivityManager
import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.Locale
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executor
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean

/** Real Activity wiring: no startup-ready setter, test-only synchronous path or skipped recovery. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class ClassicStartupRecoveryTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val credit=ImageCredit("https://example.org/current.png","Current artwork 作品\nArtist 作者 👩🏽‍🎨")
    private fun pixels(colour: Int)=Bitmap.createBitmap(7,5,Bitmap.Config.ARGB_8888).apply {eraseColor(colour)}
    private fun metadata(value: ImageCredit=credit)=JSONObject().put("version",1).put("filename","Current drawing").put("dirty",true)
        .put("image_credits",JSONObject().put("committed",ImageCredit.write(listOf(value))).put("floating",JSONArray()).put("selection_sources_known",true))
    @Before fun clean() {
        AutosaveStore(context.filesDir).exists()
        listOf("classic-autosave.zip","classic-autosave.zip.bak","classic-autosave.zip.new","classic-recovery.png")
            .forEach {File(context.filesDir,it).delete()}
    }
    private class Queue: Executor {
        val tasks=LinkedBlockingQueue<Runnable>()
        override fun execute(command: Runnable) {tasks.add(command)}
        fun release() {while(true) (tasks.poll() ?: return).run()}
    }
    /** The watchdog only prevents a broken implementation from hanging the test process.
     * Passing requires onCreate to return before it releases the explicitly queued writer.
     */
    private inner class PendingWrite(private val corrupt: ByteArray?=null,private val writeDraft: Boolean=true): AutoCloseable {
        val store=AutosaveStore(context.filesDir)
        private val writes=Queue()
        private val image=pixels(Color.BLUE)
        private val watchdog=Executors.newSingleThreadExecutor()
        init {store.submitWrite(writes) {if(writeDraft) {if(corrupt==null) store.write(image,null,metadata()) else store.file.writeBytes(corrupt)}}}
        fun create(state: Bundle?=null,visible: Boolean=true): ActivityController<ClassicPaintActivity> {
            val returned=CountDownLatch(1);val timedOut=AtomicBoolean()
            watchdog.execute {if(!returned.await(5,TimeUnit.SECONDS)) {timedOut.set(true);writes.release()}}
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
            try {controller.create(state).start().resume();if(visible) controller.visible()}
            finally {returned.countDown()}
            assertFalse("Activity creation waited for the blocked autosave",timedOut.get())
            assertFalse(controller.get().startupReady)
            return controller
        }
        fun release() {writes.release()}
        override fun close() {release();watchdog.shutdown();assertTrue(watchdog.awaitTermination(10,TimeUnit.SECONDS));image.recycle()}
    }
    private fun worker(activity: ClassicPaintActivity)=ReflectionHelpers.getField<ExecutorService>(activity,"worker")
    private fun joinWorker(activity: ClassicPaintActivity) {worker(activity).submit {}.get(10,TimeUnit.SECONDS)}
    private fun destroy(controller: ActivityController<ClassicPaintActivity>) {
        if(!controller.get().isDestroyed) controller.pause().stop().destroy()
        assertTrue(worker(controller.get()).awaitTermination(10,TimeUnit.SECONDS))
        shadowOf(Looper.getMainLooper()).idle()
    }
    private fun assertDrawing(activity: ClassicPaintActivity,value: ImageCredit=credit,colour: Int=Color.BLUE) {
        assertTrue(activity.startupReady);assertEquals(7,activity.document.bitmap.width);assertEquals(5,activity.document.bitmap.height)
        assertEquals(colour,activity.document.bitmap.getPixel(2,3));assertEquals(listOf(value),activity.document.imageCredits)
    }

    @Test fun blockedStartupAllowsMainSentinelConfigurationStopBackAndDestroyWithoutSavingBlank() {
        PendingWrite().use {pending ->
            val controller=pending.create();val activity=controller.get()
            assertNotNull(checkNotNull(activity.findViewById<View>(android.R.id.content)).findViewWithTag<View>("editor_startup"))
            var sentinel=false;Handler(Looper.getMainLooper()).post {sentinel=true};shadowOf(Looper.getMainLooper()).idle()
            assertTrue("Main callback ran while write stayed queued",sentinel)
            activity.onConfigurationChanged(Configuration(activity.resources.configuration))
            controller.pause().stop();activity.onBackPressed();assertTrue(activity.isFinishing);controller.destroy()
            assertFalse("No placeholder was written by loading lifecycle",pending.store.file.exists())
            pending.release();assertTrue(worker(activity).awaitTermination(10,TimeUnit.SECONDS));shadowOf(Looper.getMainLooper()).idle()
            val draft=pending.store.read {_,_->}
            try {assertEquals(Color.BLUE,draft.image.getPixel(2,3));assertEquals(listOf(credit),ImageCredit.read(draft.metadata.getJSONObject("image_credits").getJSONArray("committed")))}
            finally {draft.image.recycle()}
        }
    }

    @Test fun loadingCaptionUsesBundledFontsAndExistingVerticalFlow() {
        val previous=AppLanguage.selectedTag(context);val oldLocale=Locale.getDefault()
        try {
            for(tag in listOf("vi-Hani","wuu-Hans","mn-Mong","en-XV")) {
                AppLanguage.select(context,tag)
                PendingWrite().use {pending ->
                    val controller=pending.create()
                    try {
                        val activity=controller.get()
                        val label=activity.window.decorView.findViewWithTag<FlowTextView>("editor_startup_label")
                        assertNotNull(tag,label);assertTrue(label.text.isNotBlank());assertEquals(label.text,label.contentDescription)
                        assertEquals(activity.getString(org.catrobat.paintroid.R.string.ui_please_wait_for_the_current_operation),label.text.toString())
                        LocaleTypography.typeface(activity)?.let {assertSame(tag,it,label.typeface)}
                        if(tag=="mn-Mong" || tag=="en-XV") assertEquals(TextDirection.VERTICAL_LR,VerticalText.uiDirection())
                        assertTrue(label.columnHeightDp in 96..240)
                    } finally {
                        controller.pause().stop().destroy();pending.release()
                        assertTrue(worker(controller.get()).awaitTermination(10,TimeUnit.SECONDS));shadowOf(Looper.getMainLooper()).idle()
                    }
                }
            }
        } finally {AppLanguage.select(context,previous);Locale.setDefault(oldLocale)}
    }

    @Test fun failedStartupKeepsAStableErrorWithoutSpinnerAutosaveOrLostDraft() {
        PendingWrite().use {pending ->
            val controller=pending.create();val activity=controller.get()
            val manager=activity.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
            val previous=ActivityManager.MemoryInfo();manager.getMemoryInfo(previous)
            try {
                // Exercise the real worker's allocation policy, with no production test branch.
                shadowOf(manager).setMemoryInfo(ActivityManager.MemoryInfo().apply {totalMem=1024L*1024;availMem=1;threshold=1})
                pending.release();joinWorker(activity);shadowOf(Looper.getMainLooper()).idle()
                assertFalse(activity.startupReady);assertNotNull(activity.lastIoError)
                val label=activity.window.decorView.findViewWithTag<FlowTextView>("editor_startup_label")
                assertTrue(label.text.toString().contains(activity.lastIoError!!))
                assertNull(activity.window.decorView.findViewWithTag<View>("editor_startup_progress"))
                val message=label.text.toString()
                activity.onConfigurationChanged(Configuration(activity.resources.configuration))
                assertEquals(message,activity.window.decorView.findViewWithTag<FlowTextView>("editor_startup_label").text.toString())
                assertNull(activity.window.decorView.findViewWithTag<View>("editor_startup_progress"))
                assertFalse(ReflectionHelpers.getField<Boolean>(activity,"autosaveReady"))
                activity.onBackPressed();assertTrue(activity.isFinishing)
            } finally {shadowOf(manager).setMemoryInfo(previous);pending.release();destroy(controller)}
            val draft=pending.store.read {_,_->}
            try {assertEquals(Color.BLUE,draft.image.getPixel(2,3));assertEquals(listOf(credit),ImageCredit.read(draft.metadata.getJSONObject("image_credits").getJSONArray("committed")))}
            finally {draft.image.recycle()}
        }
    }

    @Test fun anotherRecreationKeepsRawRetryExportStateAndPendingGalleryOwnership() {
        PendingWrite().use {pending ->
            val rawToken="credit-edit-00000000-0000-0000-0000-000000000001.json"
            val first=pending.create(Bundle().apply {putString("main_credit_session",rawToken);putString("gallery_credit_session","expected-owner");putInt("export_quality",73)})
            first.get().onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,Intent().putExtra(CreditEditSession.EXTRA_SESSION,"wrong-owner"))
            val state=Bundle();first.saveInstanceState(state).pause().stop().destroy()
            assertEquals(rawToken,state.getString("main_credit_session"));assertEquals("expected-owner",state.getString("gallery_credit_session"))
            assertEquals(73,state.getInt("export_quality"));assertEquals(1,state.getParcelableArrayList<Bundle>("startup_events")!!.size)
            val second=pending.create(state)
            try {
                pending.release();awaitEditorStartup(second.get());assertDrawing(second.get())
                val after=Bundle();second.saveInstanceState(after)
                assertEquals("Failed raw-session restore still offers retry",rawToken,after.getString("main_credit_session"))
                assertEquals("expected-owner",after.getString("gallery_credit_session"))
                assertEquals(73,after.getInt("export_quality"));assertNull(after.getParcelableArrayList<Bundle>("startup_events"))
            } finally {pending.release();destroy(second);assertTrue(worker(first.get()).awaitTermination(10,TimeUnit.SECONDS))}
        }
    }

    @Test fun acceptedGalleryResultWaitsForRecoveredPixelsAndCorrectSourceAssociation() {
        val session=CreditEditSession.create(context.filesDir,listOf(credit),CreditEditContext.ledgerOnly(listOf(credit)))
        val edited=credit.copy(text="Saved attribution 保存 👩🏽‍🎨")
        session.edit(credit.source,edited.text) {ImageCreditArchive.retainAccepted(context,it)}
        PendingWrite().use {pending ->
            val controller=pending.create(Bundle().apply {putString("gallery_credit_session",session.token)})
            try {
                controller.get().onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,Activity.RESULT_OK,session.result())
                assertFalse(controller.get().startupReady);assertTrue(CreditEditSession.open(context.filesDir,session.token).accepted)
                pending.release();awaitEditorStartup(controller.get());assertDrawing(controller.get(),edited)
                val state=Bundle();controller.saveInstanceState(state);assertNull(state.getString("gallery_credit_session"))
            } finally {pending.release();destroy(controller);session.discard()}
        }
    }

    @Test fun newIntentDuringLoadingSurvivesRecreationAndWaitsForSaveChangesDecision() {
        PendingWrite().use {pending ->
            val first=pending.create()
            val latest=Intent(Intent.ACTION_VIEW,Uri.parse("content://startup.fixture/newer-image"))
            first.newIntent(latest)
            val state=Bundle();first.saveInstanceState(state).pause().stop().destroy()
            assertEquals(latest.data,state.getParcelableArrayList<Bundle>("startup_events")!!.single().getParcelable<Intent>("data")!!.data)
            val second=pending.create(state)
            try {
                pending.release();awaitEditorStartup(second.get());assertDrawing(second.get())
                val confirmation=ShadowAlertDialog.getLatestAlertDialog();assertTrue(confirmation.isShowing)
                // Waiting for the user's replacement decision leaves the recovered drawing intact.
                assertEquals(Color.BLUE,second.get().document.bitmap.getPixel(2,3))
            } finally {pending.release();destroy(second);assertTrue(worker(first.get()).awaitTermination(10,TimeUnit.SECONDS))}
        }
    }

    private fun deliverStartupWithoutTraversal(activity: ClassicPaintActivity) {
        joinWorker(activity)
        val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
        while(!activity.startupReady && System.nanoTime()<deadline) shadowOf(Looper.getMainLooper()).runOneTask()
        assertTrue(activity.startupReady)
        assertFalse("This regression must inspect the actual pre-traversal window",ReflectionHelpers.getField<Boolean>(activity,"initialCanvasSized"))
    }

    @Test fun explicitArchiveResultsBeforeAndAfterPublicationWaitForInitialSizing() {
        val later=credit.copy(source="https://example.org/second.png",text="Second explicitly selected source")
        val last=credit.copy(source="https://example.org/third.png",text="Third selection while autosave is busy")
        val retained=ImageCreditArchive.retainAccepted(context,listOf(credit,later,last))
        PendingWrite(writeDraft=false).use {pending ->
            val controller=pending.create(visible=false);val activity=controller.get()
            val finishSave=CountDownLatch(1)
            try {
                activity.onActivityResult(ClassicPaintActivity.LEGACY_CREDITS,Activity.RESULT_OK,
                    Intent().putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(credit)))
                pending.release();deliverStartupWithoutTraversal(activity)
                activity.onActivityResult(ClassicPaintActivity.LEGACY_CREDITS,Activity.RESULT_OK,
                    Intent().putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(later)))
                assertTrue("No attribution is attached before the pending initial newImage",activity.document.imageCredits.isEmpty())
                val state=Bundle();controller.saveInstanceState(state)
                assertEquals(2,state.getParcelableArrayList<Bundle>("startup_events")!!.size)
                // A real queued autosave owns busy while first sizing relinquishes its
                // listener. Later results must not overtake or discard this startup backlog.
                val saveBlocked=CountDownLatch(1)
                worker(activity).execute {saveBlocked.countDown();check(finishSave.await(10,TimeUnit.SECONDS))}
                assertTrue(saveBlocked.await(5,TimeUnit.SECONDS))
                ReflectionHelpers.callInstanceMethod<Unit>(activity,"saveDraftIfReady");assertTrue(activity.busy)
                controller.visible();shadowOf(Looper.getMainLooper()).idle()
                assertTrue(ReflectionHelpers.getField<Boolean>(activity,"initialCanvasSized"))
                activity.onActivityResult(ClassicPaintActivity.LEGACY_CREDITS,Activity.RESULT_OK,
                    Intent().putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(last)))
                assertTrue(activity.document.imageCredits.isEmpty())
                val busyState=Bundle();controller.saveInstanceState(busyState)
                assertEquals(3,busyState.getParcelableArrayList<Bundle>("startup_events")!!.size)
                finishSave.countDown()
                val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
                while(activity.busy && System.nanoTime()<deadline) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
                shadowOf(Looper.getMainLooper()).idle();assertFalse(activity.busy)
                assertEquals(listOf(credit,later,last),activity.document.imageCredits)
                val width=activity.document.bitmap.width;val height=activity.document.bitmap.height
                activity.paintCanvas.layout(0,0,420,620)
                assertEquals(width,activity.document.bitmap.width);assertEquals(height,activity.document.bitmap.height)
                assertEquals(listOf(credit,later,last),activity.document.imageCredits)
            } finally {finishSave.countDown();pending.release();destroy(controller);ImageCreditArchive.releaseAccepted(context,retained)}
        }
    }

    @Test fun fastExternalImportAfterPublicationCannotBeOverwrittenByInitialSizing() {
        val source=File(context.cacheDir,"startup-fast-import.png")
        val image=Bitmap.createBitmap(13,9,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)}
        try {source.outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {image.recycle()}
        PendingWrite(writeDraft=false).use {pending ->
            val controller=pending.create(visible=false);val activity=controller.get()
            try {
                pending.release();deliverStartupWithoutTraversal(activity)
                controller.newIntent(Intent(Intent.ACTION_VIEW,Uri.fromFile(source)))
                assertFalse("The import must remain queued before sizing",activity.busy)
                val state=Bundle();controller.saveInstanceState(state)
                assertEquals(Uri.fromFile(source),state.getParcelableArrayList<Bundle>("startup_events")!!.single().getParcelable<Intent>("data")!!.data)
                controller.visible();shadowOf(Looper.getMainLooper()).idle()
                assertTrue(ReflectionHelpers.getField<Boolean>(activity,"initialCanvasSized"))
                val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
                while(activity.busy && System.nanoTime()<deadline) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
                shadowOf(Looper.getMainLooper()).idle();assertFalse(activity.busy);assertNull(activity.lastIoError)
                assertEquals(13,activity.document.bitmap.width);assertEquals(9,activity.document.bitmap.height)
                assertEquals(Color.MAGENTA,activity.document.bitmap.getPixel(2,3))
                activity.paintCanvas.layout(0,0,420,620)
                assertEquals(13,activity.document.bitmap.width);assertEquals(9,activity.document.bitmap.height)
                assertEquals(Color.MAGENTA,activity.document.bitmap.getPixel(2,3))
            } finally {pending.release();destroy(controller);source.delete()}
        }
    }

    @Test fun interleavedStartupIntentsAndResultsKeepDispatchOrderAcrossRecreation() {
        fun fixture(name: String,width: Int,height: Int,colour: Int): File {
            val file=File(context.cacheDir,name)
            val image=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888).apply {eraseColor(colour)}
            try {file.outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {image.recycle()}
            return file
        }
        val firstImage=fixture("startup-order-first.png",13,9,Color.RED)
        val secondImage=fixture("startup-order-second.png",17,11,Color.MAGENTA)
        val later=credit.copy(source="https://example.org/later.png",text="Later explicit attribution")
        val retained=ImageCreditArchive.retainAccepted(context,listOf(credit,later))
        PendingWrite(writeDraft=false).use {pending ->
            val first=pending.create(visible=false)
            first.newIntent(Intent(Intent.ACTION_VIEW,Uri.fromFile(firstImage)))
            first.get().onActivityResult(ClassicPaintActivity.LEGACY_CREDITS,Activity.RESULT_OK,
                Intent().putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(credit)))
            first.newIntent(Intent(Intent.ACTION_VIEW,Uri.fromFile(secondImage)))
            first.get().onActivityResult(ClassicPaintActivity.LEGACY_CREDITS,Activity.RESULT_OK,
                Intent().putExtra(LegacyImageCreditsActivity.EXTRA_SELECTED_TOKEN,ImageCreditArchive.selectionToken(later)))
            val state=Bundle();first.saveInstanceState(state).pause().stop().destroy()
            val events=state.getParcelableArrayList<Bundle>("startup_events")!!
            assertEquals(listOf("intent","result","intent","result"),events.map {it.getString("kind")})
            assertEquals(Uri.fromFile(firstImage),events[0].getParcelable<Intent>("data")!!.data)
            assertEquals(Uri.fromFile(secondImage),events[2].getParcelable<Intent>("data")!!.data)
            val second=pending.create(state,visible=false);val activity=second.get()
            try {
                pending.release();deliverStartupWithoutTraversal(activity)
                val replay=Bundle();second.saveInstanceState(replay)
                assertEquals(events.map {it.getString("kind")},replay.getParcelableArrayList<Bundle>("startup_events")!!.map {it.getString("kind")})
                val observed=mutableListOf<Pair<Int,List<ImageCredit>>>()
                val changed=activity.document.changed
                activity.document.changed={changed();observed.add(activity.document.bitmap.width to activity.document.imageCredits.toList())}
                second.visible()
                val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(10)
                fun pendingCount()=ReflectionHelpers.getField<MutableList<Bundle>>(activity,"pendingStartupEvents").size
                while((activity.busy || pendingCount()>0) && System.nanoTime()<deadline) {shadowOf(Looper.getMainLooper()).idle();Thread.sleep(5)}
                shadowOf(Looper.getMainLooper()).idle();assertFalse(activity.busy);assertEquals(0,pendingCount());assertNull(activity.lastIoError)
                var after=-1
                for(expected in listOf(13 to emptyList(),13 to listOf(credit),17 to emptyList(),17 to listOf(later))) {
                    val next=(after+1 until observed.size).firstOrNull {observed[it]==expected}
                    assertNotNull("Missing dispatch-ordered document state $expected in $observed",next);after=next!!
                }
                assertEquals(17,activity.document.bitmap.width);assertEquals(11,activity.document.bitmap.height)
                assertEquals(Color.MAGENTA,activity.document.bitmap.getPixel(2,3));assertEquals(listOf(later),activity.document.imageCredits)
            } finally {
                pending.release();destroy(second);assertTrue(worker(first.get()).awaitTermination(10,TimeUnit.SECONDS))
                ImageCreditArchive.releaseAccepted(context,retained);firstImage.delete();secondImage.delete()
            }
        }
    }

    @Test fun newerArtworkWrittenBeforeMainDeliveryReplacesTheStalePrivateSnapshot() {
        PendingWrite().use {pending ->
            val controller=pending.create()
            val replacement=credit.copy(text="Newer credits 新しい")
            val newest=pixels(Color.MAGENTA)
            try {
                pending.release();joinWorker(controller.get());assertFalse(controller.get().startupReady)
                pending.store.write(newest,null,metadata(replacement))
                awaitEditorStartup(controller.get());assertDrawing(controller.get(),replacement,Color.MAGENTA)
            } finally {pending.release();newest.recycle();destroy(controller)}
        }
    }

    @Test fun destroyAfterFailedRecoveryBeforeUiDeliveryRetainsOriginalForNextOwner() {
        val original="retained corrupt original 作品".toByteArray()
        PendingWrite(original).use {pending ->
            val controller=pending.create()
            pending.release();joinWorker(controller.get());assertFalse(controller.get().startupReady)
            destroy(controller)
            assertArrayEquals(original,pending.store.file.readBytes())
            assertTrue(pending.store.recoveryCopies().any {it.readBytes().contentEquals(original)})
            assertTrue(AutosaveStore(context.filesDir).exists())
        }
    }

    @Test fun stopWhileWaitingStillCompletesRecoveryAndBackgroundDurability() {
        PendingWrite().use {pending ->
            val controller=pending.create();controller.pause().stop()
            try {
                pending.release();awaitEditorStartup(controller.get(),requireLayout=false);assertDrawing(controller.get())
                joinWorker(controller.get());shadowOf(Looper.getMainLooper()).idle()
                val draft=pending.store.read {_,_->}
                try {assertEquals(Color.BLUE,draft.image.getPixel(2,3));assertEquals(listOf(credit),ImageCredit.read(draft.metadata.getJSONObject("image_credits").getJSONArray("committed")))}
                finally {draft.image.recycle()}
            } finally {pending.release();controller.destroy();assertTrue(worker(controller.get()).awaitTermination(10,TimeUnit.SECONDS))}
        }
    }
}
