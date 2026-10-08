/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Activity
import android.app.Instrumentation
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.Rect
import android.os.Build
import android.os.Process
import android.os.SystemClock
import android.util.AtomicFile
import android.view.View
import android.view.ViewGroup
import android.view.inspector.WindowInspector
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry
import androidx.test.runner.lifecycle.Stage
import androidx.test.uiautomator.UiDevice
import androidx.test.uiautomator.UiSelector
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.LegacyImageCreditsActivity
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.ToolCategoryButton
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.security.MessageDigest
import java.util.UUID
import java.util.concurrent.atomic.AtomicReference
import java.util.zip.ZipFile

/** One half of one API35 regression; the host must kill this STILL-LIVE process. */
@android.annotation.TargetApi(35)
@RunWith(AndroidJUnit4::class)
class AcceptedCreditRestartSeedTest {
    @Test fun acceptedGalleryEditRemainsUndeliveredUntilExternalForceStop() {
        val f=AcceptedCreditRestartFixture
        assertEquals("This phase is explicitly partitioned onto API35",35,Build.VERSION.SDK_INT)
        assertEquals("Seed must disable both AndroidX activity-finisher paths","false",
            InstrumentationRegistry.getArguments().getString("waitForActivitiesToComplete"))
        val marker=f.markerFile
        assertTrue("Remove stale seed marker before setup",!marker.exists() || marker.delete())
        val fixture=UUID.randomUUID().toString()
        val source="https://catrobat.org/wp-content/uploads/2025/01/Restart_$fixture.png"
        val expected=f.acceptedText(fixture)
        assertTrue("Exercise private-file transport beyond the 16KiB inline threshold",expected.toByteArray(Charsets.UTF_8).size>16*1024)
        // Intentionally no use/close/finalizer: a normal teardown would deliver
        // Gallery's result and autosave the parent before the host can kill it.
        val scenario=f.launchEditor()
        val editor=f.editor
        f.onMain {
            editor.document.background=Color.WHITE
            editor.document.newImage(37,29)
            editor.document.bitmap.setPixel(5,7,Color.BLUE)
            editor.paintCanvas.fit()
        }
        f.insertFixture(source)
        f.onMain {
            editor.paintCanvas.applyPending()
            editor.document.editImageCredit(source,f.ORIGINAL_TEXT)
            editor.document.markSaved()
            f.assertOriginalDrawing(editor,source)
        }
        f.openGallery()
        val gallery=f.resumed(MediaGalleryActivity::class.java)
        f.await("stopped editor's original autosave") {
            ActivityLifecycleMonitorRegistry.getInstance().getLifecycleStageOf(editor)==Stage.STOPPED && !editor.busy
        }
        f.assertOriginalArchive(source)
        val autosaveDigest=f.digest(File(f.context.filesDir,"classic-autosave.zip"))
        var token=""
        f.onMain {
            token=gallery.intent.getStringExtra("image_credit_session") ?: error("Production Gallery session missing")
            assertTrue(token.matches(Regex("credit-edit-[0-9a-f-]{36}\\.json")))
            assertFalse("Launch must not inline the parent credit ledger",gallery.intent.hasExtra("document_image_credits"))
            f.assertOriginalDrawing(editor,source)
        }
        f.tap("gallery_edit_credits")
        f.onMain {
            val field=f.view("gallery_credit_text") as EditText
            assertEquals(f.ORIGINAL_TEXT,field.text.toString())
            field.setText(expected)
        }
        // Real production Save listener performs validation, immutable retention,
        // session write and RESULT_OK. No accepted-archive API is called by tests.
        f.tap("gallery_credit_save")
        val sessionFile=File(f.context.filesDir,token)
        val session=f.json(sessionFile)
        assertTrue("Save was durably accepted",session.getBoolean("accepted"))
        assertEquals(1L,session.getLong("revision"))
        assertTrue("Parent has not adopted this revision",session.getLong("adopted_revision")<session.getLong("revision"))
        f.assertCreditJson(session,source,expected)
        val snapshot=session.getString("accepted_snapshot")
        assertTrue(snapshot.matches(Regex("[0-9a-f]{64}")))
        val snapshotFile=File(f.context.filesDir,"retained-image-credits/$snapshot.json")
        f.assertCreditJson(f.json(snapshotFile),source,expected)
        f.onMain {
            assertSame(gallery,ActivityLifecycleMonitorRegistry.getInstance().getActivitiesInStage(Stage.RESUMED).single())
            assertEquals(Stage.STOPPED,ActivityLifecycleMonitorRegistry.getInstance().getLifecycleStageOf(editor))
            assertFalse(gallery.isFinishing)
            assertTrue("Save leaves the actual editor dialog open",f.view("gallery_credit_save").isShown)
            assertEquals(expected,(f.view("gallery_credit_text") as EditText).text.toString())
            f.assertOriginalDrawing(editor,source)
        }
        f.assertOriginalArchive(source)
        assertEquals("Acceptance must not rewrite the stopped parent's autosave",autosaveDigest,
            f.digest(File(f.context.filesDir,"classic-autosave.zip")))
        f.writeMarker(JSONObject().put("fixture",fixture).put("source",source)
            .put("pid",Process.myPid()).put("process_start",Process.getStartElapsedRealtime())
            .put("accepted_sha256",f.digest(expected.toByteArray(Charsets.UTF_8)))
            .put("autosave_sha256",autosaveDigest).put("session",token)
            .put("session_sha256",f.digest(sessionFile)).put("snapshot",snapshot)
            .put("snapshot_sha256",f.digest(snapshotFile)))
        // Keep the scenario strongly reachable through completion, with no close.
        assertNotNull(scenario)
    }
}

/** Shared test-only helpers; all production calls below are public APIs. */
@android.annotation.TargetApi(35)
internal object AcceptedCreditRestartFixture {
    const val ORIGINAL_TEXT="Original source credit.\n作者: original only.\n  Preserve whitespace  "
    private val instrumentation get()=InstrumentationRegistry.getInstrumentation()
    val context get()=instrumentation.targetContext
    private val device get()=UiDevice.getInstance(instrumentation)
    val markerFile get()=File(context.filesDir,"accepted-credit-restart-test.json")
    lateinit var editor: ClassicPaintActivity

    fun acceptedText(fixture: String)=buildString {
        append("  Accepted credit for $fixture\n")
        repeat(384) {append("$it: 作者 👩🏽‍🎨 / Ελληνικά / العربية / quote=\"exact\" \\\n")}
        append("Last line has two trailing spaces  \n")
    }
    fun digest(bytes: ByteArray)=MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") {"%02x".format(it.toInt() and 255)}
    fun digest(file: File)=digest(file.readBytes())
    fun json(file: File)=AtomicFile(file).openRead().bufferedReader(Charsets.UTF_8).use {JSONObject(it.readText())}
    fun writeMarker(value: JSONObject) {
        val atomic=AtomicFile(markerFile);val out=atomic.startWrite()
        try {out.write(value.toString().toByteArray(Charsets.UTF_8));atomic.finishWrite(out)}
        catch(error: Throwable) {atomic.failWrite(out);throw error}
    }
    fun onMain(action: ()->Unit) {
        val failure=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {action()} catch(error: Throwable) {failure.set(error)}}
        failure.get()?.let {throw it}
    }
    fun await(description: String,condition: ()->Boolean) {
        val until=SystemClock.uptimeMillis()+10000
        while(true) {
            var ready=false;onMain {ready=condition()}
            if(ready)return
            assertTrue("Timed out: $description",SystemClock.uptimeMillis()<until)
            SystemClock.sleep(25)
        }
    }
    fun launchEditor(): ActivityScenario<ClassicPaintActivity> {
        val launch=context.packageManager.getLaunchIntentForPackage(context.packageName)!!
        assertEquals(ClassicPaintActivity::class.java.name,launch.component!!.className)
        // A new ordinary launcher instance, never a saved Bundle or Gallery result.
        launch.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        val scenario=ActivityScenario.launch<ClassicPaintActivity>(launch)
        scenario.onActivity {editor=it}
        await("ordinary editor ready") {editor.startupReady && !editor.busy && editor.paintCanvas.width>0}
        return scenario
    }
    fun <T: Activity> resumed(type: Class<T>): T {
        var result: T?=null
        await("resumed ${type.simpleName}") {
            result=ActivityLifecycleMonitorRegistry.getInstance().getActivitiesInStage(Stage.RESUMED)
                .firstOrNull {type.isInstance(it)}?.let {type.cast(it)}
            result!=null
        }
        return result!!
    }
    fun view(tag: String): View=WindowInspector.getGlobalWindowViews().asReversed()
        .firstNotNullOfOrNull {root ->root.findViewWithTag<View>(tag)?.takeIf {it.isShown}}
        ?: throw AssertionError("Visible production UI control: $tag")
    fun tap(tag: String) {
        await("visible enabled $tag") {runCatching {view(tag).let {it.height>0 && it.isEnabled && !editor.busy}}.getOrDefault(false)}
        onMain {view(tag).let {it.requestRectangleOnScreen(Rect(0,0,it.width,it.height),true)}}
        instrumentation.waitForIdleSync()
        val bounds=Rect()
        onMain {
            val control=view(tag)
            assertTrue("Enabled $tag",control.isEnabled)
            assertTrue("Visible native target $tag",control.getGlobalVisibleRect(bounds))
            assertTrue("Usable target $tag",bounds.height()>=control.height/2)
            val origin=IntArray(2);control.rootView.getLocationOnScreen(origin)
            bounds.offset(origin[0],origin[1])
        }
        assertTrue("Real input tap $tag",device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
    }
    fun menu(group: String,stringId: Int) {
        tap("menu_$group")
        var tag=""
        onMain {
            val label=editor.getString(stringId)
            fun find(v: View): View? {
                if(v is Button && v.text.toString()==label && v.tag?.toString()?.startsWith("command_")==true)return v
                if(v is ViewGroup)for(i in 0 until v.childCount)find(v.getChildAt(i))?.let {return it}
                return null
            }
            tag=find(editor.window.decorView)?.tag?.toString() ?: error("Menu command $label")
        }
        tap(tag)
    }
    fun openGallery() {
        tap("menu_Draw")
        onMain {
            val category=editor.window.decorView.findViewWithTag<ToolCategoryButton>("category_INSERT")
            if(!category.expanded)assertTrue(category.performClick())
        }
        tap("insert_other_images")
        var label="";onMain {label=editor.getString(R.string.ui_catrobat_sticker_gallery)}
        val choice=device.findObject(UiSelector().text(label))
        assertTrue(choice.waitForExists(5000))
        val bounds=choice.visibleBounds
        assertTrue(device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
    }
    fun positive() {
        val button=device.findObject(UiSelector().resourceId("android:id/button1"))
        assertTrue("Visible dialog positive action",button.waitForExists(5000))
        val bounds=button.visibleBounds
        assertFalse(bounds.isEmpty)
        assertTrue(device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
    }
    fun insertFixture(source: String) {
        val file=File(context.cacheDir,"gallery-restart-fixture.png")
        val bitmap=Bitmap.createBitmap(3,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)}
        try {file.outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {bitmap.recycle()}
        var calls=0
        val monitor=object: Instrumentation.ActivityMonitor() {
            override fun onStartActivity(intent: Intent): Instrumentation.ActivityResult? {
                if(intent.component?.className!=MediaGalleryActivity::class.java.name)return null
                calls++
                return Instrumentation.ActivityResult(Activity.RESULT_OK,Intent()
                    .putExtra("image_credit_session",requireNotNull(intent.getStringExtra("image_credit_session")))
                    .putExtra("gallery_file",file.name).putExtra("gallery_source",source)
                    .putExtra("gallery_provider","CATROBAT").putExtra("gallery_title","Restart fixture"))
            }
        }
        instrumentation.addMonitor(monitor)
        try {openGallery();await("synthetic image inserted") {!editor.busy && editor.document.selection?.floating==true}}
        finally {instrumentation.removeMonitor(monitor)}
        assertEquals("Only insertion is substituted; subsequent Gallery is real",1,calls)
        assertFalse(file.exists())
    }
    fun assertOriginalDrawing(activity: ClassicPaintActivity,source: String) {
        assertEquals(listOf(source),activity.document.imageCredits.map {it.source})
        assertEquals(listOf(ORIGINAL_TEXT),activity.document.imageCredits.map {it.text})
        assertNull(activity.document.selection)
        assertPixels(activity.document.bitmap,37,29) {x,y ->when {
            x<3 && y<2 ->Color.MAGENTA
            x==5 && y==7 ->Color.BLUE
            else ->Color.WHITE
        }}
    }
    fun assertPixels(bitmap: Bitmap,width: Int,height: Int,pixel: (Int,Int)->Int) {
        assertEquals(width,bitmap.width);assertEquals(height,bitmap.height)
        for(y in 0 until height)for(x in 0 until width)assertEquals("pixel ($x,$y)",pixel(x,y),bitmap.getPixel(x,y))
    }
    fun assertOriginalArchive(source: String) {
        ZipFile(File(context.filesDir,"classic-autosave.zip")).use {zip ->
            val metadata=zip.getInputStream(zip.getEntry("draft.json")).bufferedReader(Charsets.UTF_8).use {JSONObject(it.readText())}
            val credits=metadata.getJSONObject("image_credits")
            assertEquals(0,credits.getJSONArray("floating").length())
            val committed=credits.getJSONArray("committed")
            assertEquals(1,committed.length());assertEquals(source,committed.getJSONObject(0).getString("source"))
            assertEquals(ORIGINAL_TEXT,committed.getJSONObject(0).getString("text"))
            val bitmap=zip.getInputStream(zip.getEntry("canvas.png")).use {BitmapFactory.decodeStream(it)}!!
            try {assertPixels(bitmap,37,29) {x,y ->when {x<3 && y<2 ->Color.MAGENTA;x==5 && y==7 ->Color.BLUE;else ->Color.WHITE}}}
            finally {bitmap.recycle()}
        }
    }
    fun assertCreditJson(value: JSONObject,source: String,text: String) {
        assertEquals(1,value.getInt("version"))
        val credits=value.getJSONArray("credits");assertEquals(1,credits.length())
        assertEquals(source,credits.getJSONObject(0).getString("source"))
        assertEquals(text,credits.getJSONObject(0).getString("text"))
    }
    fun openArchive(source: String,expected: String) {
        menu("File",R.string.save20_title)
        tap("export_legacy_credits")
        resumed(LegacyImageCreditsActivity::class.java)
        onMain {
            val picker=view("legacy_credit_source") as Spinner
            val matches=(0 until picker.count).filter {picker.getItemAtPosition(it).toString()==source}
            assertEquals("Unique synthetic source must select exactly its own accepted record",1,matches.size)
            picker.setSelection(matches.single())
        }
        instrumentation.waitForIdleSync()
        val displayed=StringBuilder();var pages=0
        while(true) {
            var more=false
            onMain {
                displayed.append((view("legacy_credit_text") as TextView).text.toString())
                val counter=(view("legacy_credit_page") as TextView).text.toString()
                assertTrue("Page advances exactly once",counter.startsWith("${pages+1} / "))
                more=view("legacy_credit_next").isEnabled
            }
            pages++
            assertTrue("Bound page traversal by independent expected text",pages<=expected.length)
            if(!more)break
            tap("legacy_credit_next")
        }
        assertTrue("Exercise multiple actually displayed archive pages",pages>1)
        assertEquals("All pages preserve exact accepted Unicode and whitespace",expected,displayed.toString())
    }
}
