/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.RectF
import android.os.Bundle
import android.os.Looper
import android.view.View
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AutosaveStore
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.IllustrationSource
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.ToolCategoryButton
import org.junit.After
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
import org.json.JSONArray
import java.util.concurrent.Callable
import java.util.concurrent.CountDownLatch
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.Future
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean

/**
 * Composes the actual gallery draft, editor result handling and lifecycle autosave.
 * Only scheduling is controlled: a latch precedes real writes on the real worker.
 * ActivityController and direct result delivery do not certify Android task routing,
 * WebView/network behavior, device clipboard access or physical input.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class GalleryDraftAutosaveCompositionTest {
    private lateinit var editorController: ActivityController<ClassicPaintActivity>
    private lateinit var editor: ClassicPaintActivity
    private var galleryController: ActivityController<MediaGalleryActivity>?=null
    private lateinit var gallery: MediaGalleryActivity
    private lateinit var galleryIntent: Intent
    private var editorResumed=false
    private var editorStopped=false
    private val workers=mutableListOf<ExecutorService>()
    private val gates=mutableListOf<WorkerGate>()
    private val sourceA=ImageCredit("https://catrobat.org/wp-content/uploads/2025/01/A_canvas.png",
        "Canvas 作品\nArtist 作者 A\nCC BY-SA 4.0\nhttps://example.org/artist-a")
    private val sourceB=ImageCredit("https://catrobat.org/wp-content/uploads/2025/01/B_float.png",
        "Floating Зураг\nArtist 作者 B 👩🏽‍🎨\nCC BY-SA 4.0\nhttps://example.org/artist-b")
    private val revisedA=sourceA.text+"\nChanges: cropped; 変更内容: 切り抜き"
    private val floatingPixels=intArrayOf(Color.MAGENTA,Color.CYAN,Color.YELLOW,Color.RED,Color.GREEN,Color.BLUE)
    private val canvasPixels=IntArray(7*5) {Color.WHITE}.apply {this[0]=Color.RED;this[4*7+6]=Color.BLUE}

    private fun idle()=shadowOf(Looper.getMainLooper()).idle()

    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        listOf("classic-ui","recent-colours","export","app-language").forEach {
            context.getSharedPreferences(it,0).edit().clear().commit()
        }
        createEditor()
        // Changing category changes the active tool and commits a floating selection.
        // Prepare navigation before inserting the fixture, exactly as a user can.
        val root=editor.window.decorView
        click(root,"menu_Draw")
        val insert=root.findViewWithTag<ToolCategoryButton>("category_INSERT")
        if(!insert.expanded) assertTrue(insert.performClick())
        idle()
        editor.document.newImage(7,5)
        editor.document.bitmap.setPixel(6,4,Color.BLUE)
        assertTrue(editor.document.paste(Bitmap.createBitmap(1,1,Bitmap.Config.ARGB_8888).apply {
            eraseColor(Color.RED)
        },takeOwnership=true,credits=listOf(sourceA)))
        editor.document.finishSelection()
        assertTrue(editor.document.paste(Bitmap.createBitmap(3,2,Bitmap.Config.ARGB_8888).apply {
            setPixels(floatingPixels,0,3,0,0,3,2)
        },takeOwnership=true,credits=listOf(sourceB)))
        editor.document.selection!!.rect.set(1f,2f,4f,4f)
        editor.document.selection!!.rotation=17f
        editor.document.edited()
        idle()
        assertDocument(listOf(sourceA,sourceB))
    }

    @After fun stop() {
        // Release first, even when an assertion failed, so no writer leaks into another test.
        gates.forEach {it.release.countDown()}
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
        galleryController?.let {if(!it.get().isDestroyed) it.pause().stop().destroy()}
        if(::editor.isInitialized && !editor.isDestroyed) {
            if(editorResumed) editorController.pause()
            if(!editorStopped) editorController.stop()
            editorController.destroy()
        }
        workers.forEach {worker ->
            worker.shutdown()
            assertTrue("Every real editor worker terminates",worker.awaitTermination(10,TimeUnit.SECONDS))
        }
        gates.forEach {it.task.get(1,TimeUnit.SECONDS)}
        idle()
    }

    @Test fun confirmedRestoredDraftWinsOverQueuedOldCreditsAndCopiesFromSaveAndExport() =
        roundTrip(confirm=true,saveFirstSource=false)

    @Test fun cancelledRestoredDraftKeepsOriginalCreditsPixelsAndFloatingSelection() =
        roundTrip(confirm=false,saveFirstSource=false)

    @Test fun savedFirstSourceSurvivesWhileAnEmptySecondSourceDraftIsCancelled() =
        roundTrip(confirm=false,saveFirstSource=true)

    private fun roundTrip(confirm: Boolean,saveFirstSource: Boolean) {
        openGalleryFromEditor()
        val firstGate=gateWorker()
        stopEditor() // Queues the actual initial autosave behind the gate.
        assertTrue(editor.busy)
        assertFalse("Initial draft is queued, not already committed",AutosaveStore(editor.filesDir).file.exists())
        click(gallery.window.decorView,"gallery_edit_credits")
        val dialog=creditDialog()
        val root=dialog.window!!.decorView
        if(saveFirstSource) {
            root.findViewWithTag<EditText>("gallery_credit_text").setText(revisedA)
            click(root,"gallery_credit_save")
            root.findViewWithTag<Spinner>("gallery_credit_source").setSelection(1)
            idle() // Selection commits A through the production listener.
        }
        val pending=if(saveFirstSource) "" else revisedA
        root.findViewWithTag<EditText>("gallery_credit_text").setText(pending)
        val committedInGallery=listOf(if(saveFirstSource) sourceA.copy(text=revisedA) else sourceA,sourceB)
        val galleryState=recreateGallery()
        assertEquals(committedInGallery,ImageCredit.read(JSONArray(galleryState.getString("document_image_credits"))))
        assertEquals(if(saveFirstSource) sourceB.source else sourceA.source,galleryState.getString("image_credit_editor_source"))
        assertEquals(pending,galleryState.getString("image_credit_editor_draft"))
        assertEquals(saveFirstSource,galleryState.getBoolean("document_image_credits_edited"))
        assertEquals(if(saveFirstSource) 1 else 0,creditDialog().window!!.decorView.findViewWithTag<Spinner>("gallery_credit_source").selectedItemPosition)
        assertEquals(pending,creditDialog().window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())

        val editorState=destroyEditor()
        recreateEditorWhileQueued(firstGate,editorState)
        assertDocument(listOf(sourceA,sourceB)) // Gallery edits have not been delivered.

        // Queue an older restored snapshot before applying the real gallery result.
        val secondGate=gateWorker()
        stopEditor()
        assertTrue(editor.busy)
        editorController.restart().start().resume().visible()
        editorResumed=true;editorStopped=false
        if(confirm) click(creditDialog().window!!.decorView,"gallery_credit_done")
        else creditDialog().cancel() // Android dialog Back/cancel callback, not Save.
        val finishedState=recreateGallery()
        assertFalse(finishedState.containsKey("image_credit_editor_source"))
        assertFalse(finishedState.containsKey("image_credit_editor_draft"))
        assertFalse(ShadowAlertDialog.getLatestAlertDialog()?.isShowing==true)
        val expected=if(confirm) listOf(sourceA.copy(text=revisedA),sourceB) else committedInGallery
        assertEquals(expected,ImageCredit.read(JSONArray(finishedState.getString("document_image_credits"))))
        click(gallery.window.decorView,"gallery_done")
        val result=shadowOf(gallery).resultIntent
        val resultCode=shadowOf(gallery).resultCode
        assertEquals(if(confirm || saveFirstSource) Activity.RESULT_OK else Activity.RESULT_CANCELED,resultCode)
        if(confirm || saveFirstSource) {
            assertNotNull(result)
            assertFalse("Editing credits never inserts another image",result.hasExtra("gallery_file"))
        } else assertNull("Pure cancellation returns no edited credits or image",result)
        galleryController!!.pause().stop().destroy();galleryController=null
        editor.onActivityResult(ClassicPaintActivity.GALLERY_IMAGE,resultCode,result)
        assertDocument(expected)
        // Do not drain the older write or its UI completion before destruction.
        assertTrue(editor.busy)
        val finalState=destroyEditor()
        recreateEditorWhileQueued(secondGate,finalState)
        assertDocument(expected)
        assertSaveAndExportClipboard(expected)
    }

    private fun createEditor(state: Bundle?=null) {
        val next=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        workers.add(ReflectionHelpers.getField(next.get(),"worker"))
        try {next.create(state).start().resume().visible()}
        catch(error: Throwable) {
            // An interrupted recovery may have allocated its document without
            // reaching the UI initialization needed by the normal onDestroy path.
            runCatching {next.get().document.close()}.exceptionOrNull()?.let {error.addSuppressed(it)}
            throw error
        }
        editorController=next;editor=next.get()
        editorResumed=true;editorStopped=false
        idle()
        assertNull(editor.lastIoError)
        assertNull(editor.lastAutosaveError)
    }

    private fun stopEditor() {
        editorController.pause().stop();editorResumed=false;editorStopped=true
    }

    private fun destroyEditor(): Bundle {
        val state=Bundle()
        editorController.saveInstanceState(state)
        if(editorResumed) editorController.pause()
        if(!editorStopped) editorController.stop()
        editorResumed=false;editorStopped=true
        editorController.destroy()
        assertTrue(editor.isDestroyed)
        return state
    }

    private fun openGalleryFromEditor() {
        val root=editor.window.decorView
        click(root,"menu_Draw")
        val category=root.findViewWithTag<ToolCategoryButton>("category_INSERT")
        assertTrue("Opening the gallery must not switch tools or commit the fixture",category.expanded)
        click(root,"insert_other_images")
        val picker=ShadowAlertDialog.getLatestAlertDialog()
        val position=IllustrationSource.CATROBAT.ordinal+1
        assertTrue(picker.listView.performItemClick(null,position,position.toLong()))
        idle()
        val launch=shadowOf(editor).nextStartedActivityForResult
        assertNotNull(launch)
        assertEquals(ClassicPaintActivity.GALLERY_IMAGE,launch.requestCode)
        assertEquals(MediaGalleryActivity::class.java.name,launch.intent.component!!.className)
        galleryIntent=launch.intent
        shadowOf(editor).nextStartedActivity // Clear the parallel shadow launch queue.
        assertEquals(listOf(sourceA,sourceB),ImageCredit.read(JSONArray(galleryIntent.getStringExtra("document_image_credits"))))
        galleryController=Robolectric.buildActivity(MediaGalleryActivity::class.java,galleryIntent)
        gallery=galleryController!!.setup().get()
        assertDocument(listOf(sourceA,sourceB))
    }

    private fun recreateGallery(): Bundle {
        val state=Bundle()
        val old=gallery
        val oldDialog=ShadowAlertDialog.getLatestAlertDialog()
        galleryController!!.saveInstanceState(state).pause().stop().destroy()
        assertTrue(old.isDestroyed)
        assertFalse(oldDialog?.isShowing==true)
        galleryController=Robolectric.buildActivity(MediaGalleryActivity::class.java,galleryIntent)
        gallery=galleryController!!.create(state).start().resume().visible().get()
        assertNotSame(old,gallery)
        idle()
        return state
    }

    private class WorkerGate(val release: CountDownLatch,val task: Future<*>)

    private fun gateWorker(): WorkerGate {
        val worker=ReflectionHelpers.getField<ExecutorService>(editor,"worker")
        val entered=CountDownLatch(1);val release=CountDownLatch(1)
        val task=worker.submit {
            entered.countDown()
            check(release.await(60,TimeUnit.SECONDS)) {"Test did not release the real editor worker"}
        }
        return WorkerGate(release,task).also {
            gates.add(it)
            assertTrue("Scheduling gate reached before any autosave",entered.await(5,TimeUnit.SECONDS))
        }
    }

    private fun recreateEditorWhileQueued(gate: WorkerGate,state: Bundle) {
        val creatingThread=Thread.currentThread()
        val finished=AtomicBoolean(false)
        val expired=AtomicBoolean(false)
        val watchdogLock=Any()
        var watchdogArmed=true
        val watchdog=Executors.newSingleThreadScheduledExecutor()
        val timeout=watchdog.schedule(Runnable {
            synchronized(watchdogLock) {
                if(watchdogArmed) {expired.set(true);creatingThread.interrupt()}
            }
        },15,TimeUnit.SECONDS)
        val observer=Executors.newSingleThreadExecutor()
        val waited=observer.submit(Callable {
            try {
                val deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(5)
                while(!finished.get() && System.nanoTime()<deadline) {
                    val frames=creatingThread.stackTrace
                    if(creatingThread.state==Thread.State.WAITING &&
                        frames.any {it.className==AutosaveStore::class.java.name && it.methodName=="exists"} &&
                        frames.any {it.className==ClassicPaintActivity::class.java.name && it.methodName=="onCreate"}) return@Callable true
                    Thread.sleep(2)
                }
                false
            } finally {gate.release.countDown()}
        })
        try {
            // The observer releases only after the actual new onCreate blocks on
            // the queued-write barrier. A missing barrier returns early and fails.
            createEditor(state)
            finished.set(true)
            synchronized(watchdogLock) {watchdogArmed=false;timeout.cancel(false)}
            assertFalse("Replacement recovery exceeded its 15-second watchdog",expired.get())
            assertTrue("Replacement onCreate waits for registered lifecycle writes",waited.get(6,TimeUnit.SECONDS))
            gate.task.get(1,TimeUnit.SECONDS)
        } finally {
            finished.set(true);gate.release.countDown()
            // Object.wait is interruptible, so even a missing notifyAll cannot
            // trap this test in onCreate and prevent its cleanup from running.
            // Serialize disarming and clearing with the interrupt itself: a late
            // watchdog callback must never interrupt cleanup or the next test.
            synchronized(watchdogLock) {
                watchdogArmed=false;timeout.cancel(false)
                if(expired.get()) Thread.interrupted()
            }
            watchdog.shutdownNow();observer.shutdownNow()
            assertTrue(watchdog.awaitTermination(6,TimeUnit.SECONDS))
            assertTrue(observer.awaitTermination(6,TimeUnit.SECONDS))
        }
    }

    private fun assertDocument(expected: List<ImageCredit>) {
        val document=editor.document
        assertEquals(7,document.bitmap.width);assertEquals(5,document.bitmap.height)
        assertArrayEquals("Every committed pixel survives",canvasPixels,pixels(document.bitmap))
        val selection=document.selection
        assertNotNull("No unintended insertion or selection commit",selection)
        assertTrue(selection!!.floating)
        assertEquals(RectF(1f,2f,4f,4f),selection.rect)
        assertEquals(17f,selection.rotation,0f)
        assertEquals(3,selection.image.width);assertEquals(2,selection.image.height)
        assertArrayEquals("Every floating source pixel survives",floatingPixels,pixels(selection.image))
        assertEquals(expected,document.imageCredits)
        val creditState=document.imageCreditsState()
        assertEquals(listOf(expected[0]),ImageCredit.read(creditState.getJSONArray("committed")))
        assertEquals(listOf(expected[1]),ImageCredit.read(creditState.getJSONArray("floating")))
        assertTrue(creditState.getBoolean("selection_sources_known"))
        assertTrue("Persisted undo history remains available",document.canUndo)
        assertNull(editor.lastIoError);assertNull(editor.lastAutosaveError)
    }

    private fun pixels(image: Bitmap)=IntArray(image.width*image.height).also {
        image.getPixels(it,0,image.width,0,0,image.width,image.height)
    }

    private fun assertSaveAndExportClipboard(expected: List<ImageCredit>) {
        val text=expected.joinToString("\n\n") {it.text}
        val clipboard=editor.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        for(title in listOf(R.string.save20_title,R.string.ui_export_as23)) {
            EditorTestNavigation.named(editor,"File",editor.getString(title))
            idle()
            val dialog=ShadowAlertDialog.getLatestAlertDialog()
            val root=dialog.window!!.decorView
            assertEquals(View.GONE,root.findViewWithTag<View>("export_credit_details").visibility)
            clipboard.setPrimaryClip(ClipData.newPlainText("sentinel","not copied"))
            click(root,"export_toggle_credits")
            assertEquals(View.VISIBLE,root.findViewWithTag<View>("export_credit_details").visibility)
            val field=root.findViewWithTag<TextView>("export_credit_text")
            assertEquals(text,field.text.toString());assertTrue(field.isTextSelectable)
            click(root,"export_copy_credits")
            assertEquals(1,clipboard.primaryClip!!.itemCount)
            assertEquals(text,clipboard.primaryClip!!.getItemAt(0).text.toString())
            assertTrue(dialog.isShowing)
            assertNull("Copy does not launch a destination",shadowOf(editor).nextStartedActivityForResult)
            assertTrue(dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick())
            idle();assertFalse(dialog.isShowing)
            assertDocument(expected)
        }
    }

    private fun creditDialog(): AlertDialog=checkNotNull(ShadowAlertDialog.getLatestAlertDialog()).also {
        assertTrue(it.isShowing)
        assertNotNull(it.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text"))
    }

    private fun click(root: View,tag: String) {
        val view=root.findViewWithTag<View>(tag)
        assertNotNull("Production control exists: $tag",view)
        assertTrue("Production click is handled: $tag",view.performClick())
        idle()
    }
}
