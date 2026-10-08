/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Activity
import android.app.Instrumentation
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Rect
import android.graphics.RectF
import android.os.Handler
import android.os.Looper
import android.os.Build
import android.os.SystemClock
import android.view.KeyEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowInsets
import android.view.inspector.WindowInspector
import android.view.inputmethod.InputMethodManager
import android.webkit.WebView
import android.widget.Button
import android.widget.EditText
import android.widget.ListView
import android.widget.Spinner
import android.widget.TextView
import android.util.Base64
import androidx.core.content.FileProvider
import androidx.lifecycle.Lifecycle
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.runner.lifecycle.ActivityLifecycleCallback
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry
import androidx.test.runner.lifecycle.Stage
import androidx.test.uiautomator.UiDevice
import androidx.test.uiautomator.By
import androidx.test.uiautomator.Until
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.ImageFormat
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.ToolCategoryButton
import org.json.JSONArray
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.util.concurrent.CopyOnWriteArrayList
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

/**
 * Android launches, recreates and finishes the real gallery above the real editor.
 * No gallery ActivityResult or lifecycle callback is synthesized by the test.
 * Only document fixtures, WebView HTML and the external document picker are local.
 * This is installed emulator coverage, not process-death or physical-device proof.
 */
@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=30)
class GalleryDraftDeviceTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val context get()=instrumentation.targetContext
    private val device get()=UiDevice.getInstance(instrumentation)
    private lateinit var scenario: ActivityScenario<ClassicPaintActivity>
    private lateinit var destinations: LocalDestinations
    @Volatile private var editor: ClassicPaintActivity?=null
    @Volatile private var gallery: MediaGalleryActivity?=null
    private val editors=mutableListOf<ClassicPaintActivity>() // Main-thread only.
    private val fixtures=mutableListOf<File>()
    private val sourceA=ImageCredit("https://catrobat.org/wp-content/uploads/2025/01/A_canvas.png",
        "Canvas 作品\nArtist A\nCC BY-SA 4.0\nhttps://example.org/artist-a")
    private val sourceB=ImageCredit("https://catrobat.org/wp-content/uploads/2025/01/B_float.png",
        "Floating Зураг\nArtist B 👩🏽‍🎨\nCC BY-SA 4.0\nhttps://example.org/artist-b")
    private val revisedA=sourceA.text+"\nChanges: cropped; 変更内容: 切り抜き"
    private val floatingPixels=intArrayOf(Color.MAGENTA,Color.CYAN,Color.YELLOW,Color.RED,Color.GREEN,Color.BLUE)
    private val canvasPixels=IntArray(35) {Color.WHITE}.apply {this[0]=Color.RED;this[34]=Color.BLUE}

    private val lifecycle=ActivityLifecycleCallback { activity,stage ->
        if(activity is ClassicPaintActivity || activity is MediaGalleryActivity) android.util.Log.i(
            "GalleryDraftDeviceTest","${activity.javaClass.simpleName}@${System.identityHashCode(activity)} $stage task=${activity.taskId}")
        if(stage==Stage.CREATED) when(activity) {
            is ClassicPaintActivity -> {editor=activity;editors.add(activity)}
            is MediaGalleryActivity -> {
                gallery=activity
                // Do not wait for, inspect or depend on the provider's initial page.
                // Replace it on every real instance, including Android recreation.
                // Subsequent network loads are blocked; no image download is used.
                val web=descendants(activity.window.decorView).filterIsInstance<WebView>().single()
                web.stopLoading();web.settings.blockNetworkLoads=true
                web.loadData("<html><body>Local gallery draft fixture</body></html>","text/html","UTF-8")
            }
        }
    }

    /** The gallery is observed and allowed through. Only SAF destinations are substituted. */
    private class LocalDestinations : Instrumentation.ActivityMonitor() {
        val requests=CopyOnWriteArrayList<Intent>()
        val next=AtomicReference<Intent?>()
        override fun onStartActivity(intent: Intent): Instrumentation.ActivityResult? {
            if(intent.component?.className==MediaGalleryActivity::class.java.name) {
                requests.add(Intent(intent));return null
            }
            if(intent.action!=Intent.ACTION_CREATE_DOCUMENT) return null
            requests.add(Intent(intent))
            val result=next.getAndSet(null)
            return Instrumentation.ActivityResult(if(result==null) Activity.RESULT_CANCELED else Activity.RESULT_OK,result)
        }
    }

    @Before fun launchEditorWithLocalDocument() {
        onMain {ActivityLifecycleMonitorRegistry.getInstance().addLifecycleCallback(lifecycle)}
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        listOf("classic-ui","recent-colours","export").forEach {context.getSharedPreferences(it,0).edit().clear().commit()}
        destinations=LocalDestinations();instrumentation.addMonitor(destinations)
        val launch=checkNotNull(context.packageManager.getLaunchIntentForPackage(context.packageName))
        assertEquals(ClassicPaintActivity::class.java.name,launch.component!!.className)
        scenario=ActivityScenario.launch(launch)
        await("editor layout") {currentEditor().paintCanvas.width>0 && !currentEditor().busy}
        onMain {
            val a=currentEditor();val root=a.window.decorView
            click(root,"menu_Draw")
            val category=root.findViewWithTag<ToolCategoryButton>("category_INSERT")
            if(!category.expanded) assertTrue(category.performClick())
            // Prepare the insertion panel first: switching tools later would commit selection.
            a.document.newImage(7,5);a.document.bitmap.setPixel(6,4,Color.BLUE)
            assertTrue(a.document.paste(Bitmap.createBitmap(1,1,Bitmap.Config.ARGB_8888).apply {
                eraseColor(Color.RED)
            },takeOwnership=true,credits=listOf(sourceA)))
            a.document.finishSelection()
            assertTrue(a.document.paste(Bitmap.createBitmap(3,2,Bitmap.Config.ARGB_8888).apply {
                setPixels(floatingPixels,0,3,0,0,3,2)
            },takeOwnership=true,credits=listOf(sourceB)))
            a.document.selection!!.rect.set(1f,2f,4f,4f);a.document.selection!!.rotation=17f
            a.document.edited();a.paintCanvas.fit()
            assertDocument(listOf(sourceA,sourceB))
        }
        awaitReady()
    }

    @After fun finishActivitiesAndWrites() {
        try {
            onMain {gallery?.takeUnless {it.isDestroyed}?.finish()}
            await("gallery finishes during cleanup") {gallery?.isDestroyed!=false}
            if(::scenario.isInitialized) {
                scenario.moveToState(Lifecycle.State.CREATED)
                awaitReady()
                onMain {currentEditor().finish()}
                await("editor destroyed during cleanup") {currentEditor().isDestroyed}
                scenario.close()
            }
        } finally {
            if(::destinations.isInitialized) instrumentation.removeMonitor(destinations)
            onMain {ActivityLifecycleMonitorRegistry.getInstance().removeLifecycleCallback(lifecycle)}
            fixtures.forEach {it.delete()}
        }
    }

    @Test fun confirmedRecreatedGalleryDraftReturnsToTheCoveredRecreatedEditor() = roundTrip(confirm=true,saveFirst=false)

    @Test fun cancelledRecreatedGalleryDraftKeepsTheOriginalDocumentAndCredits() = roundTrip(confirm=false,saveFirst=false)

    @Test fun savedFirstCreditSurvivesRecreationAndCancellationOfAnEmptySecondDraft() = roundTrip(confirm=false,saveFirst=true)

    private fun roundTrip(confirm: Boolean,saveFirst: Boolean) {
        val original=currentEditor()
        val task=onMain {original.taskId}
        onMain {click(original.window.decorView,"insert_other_images")}
        await("gallery provider picker") {dialogRootWithList()!=null}
        onMain {
            val list=descendants(dialogRootWithList()!!).filterIsInstance<ListView>().single()
            assertTrue(list.performItemClick(null,1,1L)) // Catrobat, following From device.
        }
        await("real gallery resumed over stopped editor") {
            gallery?.let {stage(it)==Stage.RESUMED}==true && stage(currentEditor())==Stage.STOPPED
        }
        awaitReady() // Drain the editor's real onStop autosave before testing recovery.
        onMain {
            assertEquals(task,currentGallery().taskId)
            assertEquals(listOf(sourceA,sourceB),ImageCredit.read(JSONArray(
                currentGallery().intent.getStringExtra("document_image_credits"))))
            assertEquals(1,editors.count {!it.isDestroyed})
        }
        assertEquals(1,destinations.requests.count {it.component?.className==MediaGalleryActivity::class.java.name})
        tap {currentGallery().window.decorView.findViewWithTag("gallery_edit_credits")}
        await("credit editor opened") {creditRoot()!=null}
        onMain {
            val root=creditRoot()!!
            root.findViewWithTag<EditText>("gallery_credit_text").setText(revisedA)
            if(saveFirst) {
                click(root,"gallery_credit_save")
                root.findViewWithTag<Spinner>("gallery_credit_source").setSelection(1)
            }
        }
        if(saveFirst) await("second credit selected") {
            creditRoot()?.findViewWithTag<EditText>("gallery_credit_text")?.text?.toString()==sourceB.text
        }
        val pending=if(saveFirst) "" else revisedA
        onMain {creditRoot()!!.findViewWithTag<EditText>("gallery_credit_text").setText(pending)}
        recreateGallery(pending,if(saveFirst) 1 else 0)

        // Recreate the actual covered Activity; ActivityScenario.recreate() assumes
        // its Activity is resumed. Android, not a direct onActivityResult call,
        // must retain this new instance as the recipient of the gallery result.
        onMain {currentEditor().recreate()}
        await("covered editor recreated under gallery") {
            currentEditor()!==original && original.isDestroyed && stage(currentEditor())==Stage.STOPPED &&
                stage(currentGallery())==Stage.RESUMED
        }
        awaitReady()
        onMain {
            assertEquals(task,currentEditor().taskId);assertEquals(task,currentGallery().taskId)
            assertEquals(1,editors.count {!it.isDestroyed})
            assertDocument(listOf(sourceA,sourceB)) // No result has been delivered yet.
            assertEquals(pending,creditRoot()!!.findViewWithTag<EditText>("gallery_credit_text").text.toString())
            hideKeyboard(creditRoot()!!)
        }
        await("keyboard hidden before dialog action") {creditRoot()?.rootWindowInsets?.isVisible(WindowInsets.Type.ime())!=true}
        if(confirm) tap {creditRoot()!!.findViewWithTag("gallery_credit_done")}
        else instrumentation.sendKeyDownUpSync(KeyEvent.KEYCODE_BACK)
        await("credit dialog dismissed") {creditRoot()==null}
        // A cancelled modal must not reappear after another Activity recreation.
        val oldGallery=currentGallery()
        onMain {oldGallery.recreate()}
        await("gallery recreated after closing modal") {
            currentGallery()!==oldGallery && oldGallery.isDestroyed && stage(currentGallery())==Stage.RESUMED
        }
        onMain {assertNull(creditRoot())}
        val resultRecipient=currentEditor()
        tap {currentGallery().window.decorView.findViewWithTag("gallery_done")}
        await("Android returns to the same recovered editor") {
            currentGallery().isDestroyed && stage(currentEditor())==Stage.RESUMED
        }
        awaitReady()
        val expected=listOf(if(confirm || saveFirst) sourceA.copy(text=revisedA) else sourceA,sourceB)
        onMain {
            assertSame("No second editor was launched to receive the result",resultRecipient,currentEditor())
            assertEquals(task,currentEditor().taskId);assertEquals(1,editors.count {!it.isDestroyed})
            assertDocument(expected)
        }
        scenario.recreate()
        await("returned editor recreated") {currentEditor()!==resultRecipient && resultRecipient.isDestroyed && stage(currentEditor())==Stage.RESUMED}
        awaitReady()
        onMain {assertDocument(expected)}
        checkSaveAndExport(expected)
    }

    private fun recreateGallery(pending: String,index: Int) {
        val old=currentGallery();val oldRoot=onMain {creditRoot()!!}
        onMain {old.recreate()}
        await("gallery and unconfirmed modal recreated by Android") {
            currentGallery()!==old && old.isDestroyed && stage(currentGallery())==Stage.RESUMED && creditRoot()!=null
        }
        onMain {
            assertFalse("Old modal window was removed",oldRoot.isAttachedToWindow)
            val root=creditRoot()!!
            assertEquals(index,root.findViewWithTag<Spinner>("gallery_credit_source").selectedItemPosition)
            assertEquals("Unsaved text is restored verbatim",pending,root.findViewWithTag<EditText>("gallery_credit_text").text.toString())
            assertDocument(listOf(sourceA,sourceB))
        }
    }

    private fun checkSaveAndExport(expected: List<ImageCredit>) {
        val text=expected.filter {it.text.isNotBlank()}.joinToString("\n\n") {it.text}
        val requests=destinations.requests.size
        for(title in listOf(R.string.save20_title,R.string.ui_export_as23)) {
            menu(title)
            onMain {
                val root=saveRoot()!!
                assertEquals(View.GONE,root.findViewWithTag<View>("export_credit_details").visibility)
                clipboard().setPrimaryClip(ClipData.newPlainText("sentinel","not copied"))
            }
            tap {saveRoot()!!.findViewWithTag("export_toggle_credits")}
            onMain {assertEquals(text,saveRoot()!!.findViewWithTag<TextView>("export_credit_text").text.toString())}
            tap {saveRoot()!!.findViewWithTag("export_copy_credits")}
            onMain {assertEquals(text,clipboard().primaryClip!!.getItemAt(0).text.toString())}
            // Keep SystemUI's clipboard preview out of the next native button tap.
            dismissClipboardOverlay()
            tap {saveRoot()!!.findViewById(android.R.id.button2)}
            await("Save/Export cancelled") {saveRoot()==null}
            onMain {assertDocument(expected)}
            assertEquals("Copy and Cancel never request a destination",requests,destinations.requests.size)
        }

        // Exercise real encoders/writers as well as the credit panels. Export
        // commits the floating selection through normal applyPending behavior.
        val rendered=onMain {
            val document=currentEditor().document
            document.bitmap.copy(Bitmap.Config.ARGB_8888,true).also {image ->
                val selection=document.selection!!;val source=document.selectionImage()!!
                try {selection.draw(Canvas(image),source,Paint(Paint.FILTER_BITMAP_FLAG))}
                finally {if(source!==selection.image) source.recycle()}
            }
        }
        val expectedPixels=try {pixels(rendered)} finally {rendered.recycle()}
        for((title,format) in listOf(R.string.ui_export_as23 to ImageFormat.BASE64,R.string.save20_title to ImageFormat.PNG)) {
            val name=if(format==ImageFormat.BASE64) "export.txt" else "save.png"
            val destination=File(File(context.cacheDir,"images").apply {mkdirs()},"gallery-draft-$name").also {
                it.delete();fixtures.add(it)
            }
            val uri=FileProvider.getUriForFile(context,"${context.packageName}.fileprovider",destination)
            destinations.next.set(Intent().setData(uri).addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION))
            menu(title)
            onMain {
                val picker=saveRoot()!!.findViewWithTag<Spinner>("export_format")
                val index=(0 until picker.count).single {picker.getItemAtPosition(it).toString()==format.label}
                picker.setSelection(index)
            }
            instrumentation.waitForIdleSync()
            // This click runs the real SaveOptionsDialog confirm and Android picker result.
            onMain {assertTrue(saveRoot()!!.findViewById<View>(android.R.id.button1).performClick())}
            await("$name written") {!currentEditor().busy && destination.length()>0}
            val output=checkNotNull(if(format==ImageFormat.BASE64) {
                val content=destination.readText().trim()
                assertTrue(content.startsWith("data:image/png;base64,"))
                val bytes=Base64.decode(content.substringAfter(','),Base64.DEFAULT)
                BitmapFactory.decodeByteArray(bytes,0,bytes.size)
            } else BitmapFactory.decodeFile(destination.path))
            try {
                assertEquals(7,output.width);assertEquals(5,output.height)
                assertArrayEquals("$name contains the recovered composition",expectedPixels,pixels(output))
            } finally {output.recycle()}
            onMain {
                assertEquals(expected,currentEditor().document.imageCredits)
                assertEquals(title==R.string.ui_export_as23,currentEditor().document.dirty)
                assertNull(currentEditor().lastIoError);assertNull(currentEditor().lastAutosaveError)
            }
        }
        assertEquals(2,destinations.requests.count {it.action==Intent.ACTION_CREATE_DOCUMENT})
        val outputRequests=destinations.requests.filter {it.action==Intent.ACTION_CREATE_DOCUMENT}
        assertEquals(listOf("text/plain","image/png"),outputRequests.map {it.type})
        assertTrue(outputRequests.all {it.hasCategory(Intent.CATEGORY_OPENABLE)})
    }

    private fun assertDocument(expected: List<ImageCredit>) {
        val a=currentEditor();val document=a.document
        assertEquals(7,document.bitmap.width);assertEquals(5,document.bitmap.height)
        assertArrayEquals(canvasPixels,pixels(document.bitmap))
        val selection=checkNotNull(document.selection)
        assertTrue(selection.floating);assertEquals(RectF(1f,2f,4f,4f),selection.rect)
        assertEquals(17f,selection.rotation,0f);assertEquals(3,selection.image.width);assertEquals(2,selection.image.height)
        assertArrayEquals(floatingPixels,pixels(selection.image));assertEquals(expected,document.imageCredits)
        val state=document.imageCreditsState()
        assertEquals(listOf(expected[0]),ImageCredit.read(state.getJSONArray("committed")))
        assertEquals(listOf(expected[1]),ImageCredit.read(state.getJSONArray("floating")))
        assertTrue(state.getBoolean("selection_sources_known"));assertTrue(document.canUndo)
        assertNull(a.lastIoError);assertNull(a.lastAutosaveError)
    }

    private fun menu(title: Int) {
        awaitReady()
        onMain {
            val a=currentEditor();val root=a.window.decorView
            click(root,"menu_File")
            val command=descendants(root).filterIsInstance<Button>().single {
                it.tag?.toString()?.startsWith("command_")==true && it.text.toString()==a.getString(title)
            }
            assertTrue(command.performClick())
        }
        await("Save/Export panel") {saveRoot()!=null}
    }
    private fun currentEditor()=checkNotNull(editor)
    private fun currentGallery()=checkNotNull(gallery)
    private fun stage(a: Activity)=ActivityLifecycleMonitorRegistry.getInstance().getLifecycleStageOf(a)
    private fun clipboard()=currentEditor().getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    private fun creditRoot()=WindowInspector.getGlobalWindowViews().lastOrNull {it.isShown && it.findViewWithTag<View>("gallery_credit_text")!=null}
    private fun saveRoot()=WindowInspector.getGlobalWindowViews().lastOrNull {it.isShown && it.findViewWithTag<View>("export_filename")!=null}
    private fun dialogRootWithList()=WindowInspector.getGlobalWindowViews().lastOrNull {it.isShown && descendants(it).any {view ->view is ListView}}
    private fun descendants(root: View): List<View> = buildList {
        add(root);if(root is ViewGroup) for(i in 0 until root.childCount) addAll(descendants(root.getChildAt(i)))
    }
    private fun pixels(image: Bitmap)=IntArray(image.width*image.height).also {image.getPixels(it,0,image.width,0,0,image.width,image.height)}
    private fun click(root: View,tag: String) {assertTrue(tag,checkNotNull(root.findViewWithTag<View>(tag)).performClick())}
    private fun hideKeyboard(root: View) {
        (currentGallery().getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager).hideSoftInputFromWindow(root.windowToken,0)
    }
    private fun dismissClipboardOverlay() {
        if(Build.VERSION.SDK_INT<33) return
        val selector=By.res("com.android.systemui","clipboard_ui")
        val overlay=device.wait(Until.findObject(selector),1500)
        overlay?.findObject(By.res("com.android.systemui","dismiss_button"))?.visibleBounds?.let {bounds ->
            assertFalse(bounds.isEmpty);assertTrue(device.click(bounds.centerX(),bounds.centerY()))
        }
        assertTrue(device.wait(Until.gone(selector),10000)==true)
        await("SystemUI clipboard preview removed") {
            instrumentation.uiAutomation.windows.none {it.title?.toString()=="ClipboardOverlay"}
        }
    }
    private fun tap(find: ()->View) {
        onMain {find().let {it.requestRectangleOnScreen(Rect(0,0,it.width,it.height),true)}}
        instrumentation.waitForIdleSync()
        val bounds=onMain {
            val view=find();val local=Rect()
            assertTrue("Control is shown",view.isShown);assertTrue(view.getLocalVisibleRect(local))
            val origin=IntArray(2);view.getLocationOnScreen(origin);local.offset(origin[0],origin[1]);local
        }
        assertTrue(device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
    }
    private fun awaitReady()=await("actual autosave writer idle") {
        val a=currentEditor()
        fun counter(name: String)=ClassicPaintActivity::class.java.getDeclaredField(name).apply {isAccessible=true}.getLong(a)
        !a.busy && counter("draftGeneration")==counter("savedDraftGeneration")
    }
    private fun <T> onMain(action: ()->T): T {
        val result=AtomicReference<T>();val failure=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {result.set(action())} catch(error: Throwable) {failure.set(error)}}
        failure.get()?.let {throw it};return result.get()
    }
    private fun await(description: String,condition: ()->Boolean) {
        val done=CountDownLatch(1);val error=AtomicReference<Throwable?>();val handler=Handler(Looper.getMainLooper())
        val deadline=SystemClock.uptimeMillis()+15000
        val check=object: Runnable {
            override fun run() {
                try {
                    if(condition()) {done.countDown();return}
                    if(SystemClock.uptimeMillis()<deadline) {handler.postDelayed(this,25);return}
                    error.set(AssertionError("Timed out: $description; I/O=${editor?.lastIoError}; autosave=${editor?.lastAutosaveError}"))
                } catch(failure: Throwable) {error.set(failure)}
                done.countDown()
            }
        }
        handler.post(check)
        try {assertTrue(description,done.await(16,TimeUnit.SECONDS));error.get()?.let {throw it}}
        finally {handler.removeCallbacks(check)}
    }
}
