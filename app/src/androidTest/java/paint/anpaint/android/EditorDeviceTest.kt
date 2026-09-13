/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Activity
import android.app.Dialog
import android.app.Instrumentation
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.Rect
import android.net.Uri
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import android.view.MotionEvent
import android.view.View
import android.widget.EditText
import android.widget.ScrollView
import android.widget.TextView
import androidx.core.content.FileProvider
import androidx.lifecycle.Lifecycle
import androidx.test.core.app.ActivityScenario
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.uiautomator.UiDevice
import androidx.test.uiautomator.UiScrollable
import androidx.test.uiautomator.UiSelector
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ImageFormat
import org.catrobat.paintroid.classic.LegalInfo
import org.catrobat.paintroid.classic.MediaGalleryActivity
import org.catrobat.paintroid.classic.ToolCategory
import org.catrobat.paintroid.classic.ToolCategoryButton
import org.catrobat.paintroid.classic.PaintTool
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
 * Runs the installed application, real tab panels, bitmap renderer and FileProvider.
 * Only the external picker/recipient/gallery activity is substituted by an Android
 * ActivityMonitor; no drawing, decoding, encoding or app activity is simulated.
 * These emulator tests complement, and do not claim, physical ARM-device testing.
 */
@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=26)
class EditorDeviceTest {
    private val instrumentation=InstrumentationRegistry.getInstrumentation()
    private val context get()=instrumentation.targetContext
    private val device get()=UiDevice.getInstance(instrumentation)
    private lateinit var scenario: ActivityScenario<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private lateinit var monitor: ExternalActivities
    private val fixtures=mutableListOf<File>()

    private class ExternalActivities : Instrumentation.ActivityMonitor() {
        val requests=CopyOnWriteArrayList<Intent>()
        val nextResult=AtomicReference<Intent?>()
        override fun onStartActivity(intent: Intent): Instrumentation.ActivityResult? {
            val isPicker=intent.action==Intent.ACTION_OPEN_DOCUMENT || intent.action==Intent.ACTION_GET_CONTENT || intent.action==Intent.ACTION_CREATE_DOCUMENT
            if(!isPicker && intent.action!=Intent.ACTION_CHOOSER && intent.component?.className!=MediaGalleryActivity::class.java.name) return null
            requests.add(Intent(intent))
            val result=if(isPicker) nextResult.getAndSet(null) else null
            return Instrumentation.ActivityResult(if(result==null) Activity.RESULT_CANCELED else Activity.RESULT_OK,result)
        }
    }

    @Before fun launchInstalledApp() {
        assertEquals("paint.anpaint.android",context.packageName)
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        listOf("classic-ui","recent-colours","export").forEach {context.getSharedPreferences(it,0).edit().clear().commit()}
        monitor=ExternalActivities();instrumentation.addMonitor(monitor)
        val launch=context.packageManager.getLaunchIntentForPackage(context.packageName)
        assertNotNull("Installed AN Paint must have a launcher entry",launch)
        assertEquals(ClassicPaintActivity::class.java.name,launch!!.component!!.className)
        scenario=ActivityScenario.launch(launch)
        scenario.onActivity {activity=it}
        awaitState("initial canvas layout") {it.paintCanvas.width>0 && it.paintCanvas.height>0 && !it.busy}
        onMain {it.document.newImage(100,100);it.document.markSaved();it.paintCanvas.fit()}
    }

    @After fun closeInstalledApp() {
        if(::scenario.isInitialized) {
            // Let onStop's real draft write finish before destroying the activity,
            // so a previous test cannot overwrite the next test's fresh fixture.
            scenario.moveToState(Lifecycle.State.CREATED)
            awaitState("pending save before close") {!it.busy}
            // AndroidX 1.6.1 close() starts its EmptyActivity again even when
            // moveToState(CREATED) already left that helper resumed. No second
            // onResume arrives, so its helper waits the full 45-second timeout.
            // Finish the stopped activity normally, preserving the completed
            // onStop autosave without triggering another stop/save cycle.
            onMain {it.finish()}
            awaitState("activity destroyed after autosave") {it.isDestroyed}
            scenario.close()
        }
        if(::monitor.isInitialized) instrumentation.removeMonitor(monitor)
        fixtures.forEach {it.delete()}
    }

    @Test fun filePickerLoadsOpaqueImageAndInsertionKeepsTheCurrentCanvas() {
        val file=fixture("device-open.png")
        val image=Bitmap.createBitmap(17,11,Bitmap.Config.ARGB_8888).apply {
            eraseColor(Color.TRANSPARENT);setPixel(2,3,Color.RED)
        }
        try {file.outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {image.recycle()}
        onMain {it.document.background=Color.YELLOW}
        monitor.nextResult.set(resultFor(file))
        menu("File",text(R.string.ui_load_image))
        awaitState("picker result decoded") {!it.busy && it.document.bitmap.width==17 && it.document.bitmap.height==11}
        val open=monitor.requests.single {it.action==Intent.ACTION_OPEN_DOCUMENT}
        assertTrue(open.hasCategory(Intent.CATEGORY_OPENABLE))
        assertEquals("*/*",open.type)
        onMain {
            assertEquals(Color.YELLOW,it.document.bitmap.getPixel(0,0))
            assertEquals(Color.RED,it.document.bitmap.getPixel(2,3))
            assertEquals(255,Color.alpha(it.document.bitmap.getPixel(0,0)))
            assertNull(it.lastIoError)
        }
        val permissions=context.packageManager.getPackageInfo(context.packageName,PackageManager.GET_PERMISSIONS).requestedPermissions.orEmpty()
        assertFalse(permissions.contains("android.permission.READ_EXTERNAL_STORAGE"))

        monitor.nextResult.set(resultFor(file))
        menu("File",text(R.string.ui_insert_image_into_canvas))
        awaitState("image inserted as a floating selection") {!it.busy && it.document.selection?.floating==true}
        onMain {
            assertEquals(17,it.document.bitmap.width);assertEquals(11,it.document.bitmap.height)
            assertEquals(17,it.document.selection!!.image.width)
            assertEquals(PaintTool.SELECT,it.paintCanvas.tool)
            assertNull(it.lastIoError)
        }
    }

    @Test fun saveAndShareWritesReadablePngBeforeRequestingTheAndroidChooser() {
        onMain {it.document.bitmap.setPixel(5,7,Color.BLUE)}
        val destination=fixture("device-share.png")
        monitor.nextResult.set(resultFor(destination))
        menu("File",text(R.string.ui_save_and_share))
        clickText("PNG") // Open the format spinner, then explicitly choose PNG.
        clickText("PNG")
        positive()
        awaitState("saved image and share request") {!it.busy && monitor.requests.any {request -> request.action==Intent.ACTION_CHOOSER}}
        val create=monitor.requests.single {it.action==Intent.ACTION_CREATE_DOCUMENT}
        assertEquals("image/png",create.type)
        val chooser=monitor.requests.single {it.action==Intent.ACTION_CHOOSER}
        val send=chooser.getParcelableExtra<Intent>(Intent.EXTRA_INTENT)!!
        assertEquals(Intent.ACTION_SEND,send.action);assertEquals("image/png",send.type)
        assertTrue(send.flags and Intent.FLAG_GRANT_READ_URI_PERMISSION!=0)
        val shared=send.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)!!
        assertEquals("content",shared.scheme)
        assertEquals("${context.packageName}.fileprovider",shared.authority)
        assertEquals(shared,send.clipData!!.getItemAt(0).uri)
        for(uri in listOf(uriFor(destination),shared)) {
            val output=context.contentResolver.openInputStream(uri).use {BitmapFactory.decodeStream(it)}
            assertNotNull(output)
            try {
                assertEquals(100,output!!.width);assertEquals(100,output.height)
                assertEquals(Color.BLUE,output.getPixel(5,7));assertEquals(255,Color.alpha(output.getPixel(0,0)))
            } finally {output?.recycle()}
        }
        onMain {assertFalse(it.document.dirty);assertNull(it.lastIoError)}
    }

    @Test fun jpegQualityChangesOutputAndEveryAdditionalFormatReachesTheCorrectFilePicker() {
        onMain {a ->
            for(y in 0 until 100) for(x in 0 until 100) a.document.bitmap.setPixel(x,y,Color.rgb((x*13+y*7)%256,(x*3+y*29)%256,(x*19+y*5)%256))
        }
        fun jpeg(quality: Int): ByteArray {
            val destination=fixture("device-quality-$quality.jpg")
            monitor.nextResult.set(resultFor(destination))
            menu("File",text(R.string.ui_export_as23))
            device.findObject(UiSelector().className("android.widget.Spinner")).click()
            device.findObject(UiSelector().text("JPEG")).click()
            val qualityButton=device.findObject(UiSelector().className("android.widget.Button").textContains(text(R.string.ui_quality)))
            assertTrue(qualityButton.waitForExists(5000));qualityButton.click()
            setNumber(quality.toString());positive();positive()
            awaitState("JPEG file output") {!it.busy && destination.length()>0}
            val output=BitmapFactory.decodeFile(destination.path)
            assertNotNull(output)
            try {assertEquals(100,output.width);assertEquals(100,output.height)} finally {output?.recycle()}
            return destination.readBytes()
        }
        val low=jpeg(20);val high=jpeg(95)
        assertTrue(high.size>low.size);assertFalse(low.contentEquals(high))
        for(format in ImageFormat.values().filter {it.name in listOf("JPEG_XL","WEBP","HEIC","AVIF","BMP","GIF")}) {
            val before=monitor.requests.count {it.action==Intent.ACTION_CREATE_DOCUMENT}
            menu("File",text(if(format.canSaveLosslessly) R.string.save20_title else R.string.ui_export_as23))
            device.findObject(UiSelector().className("android.widget.Spinner")).click()
            device.findObject(UiSelector().text(format.label)).click()
            val destinationButton=device.findObject(UiSelector().resourceId("android:id/button1"))
            assertTrue("${format.label} destination button exists",destinationButton.waitForExists(5000))
            assertTrue("${format.label} destination button enabled",destinationButton.isEnabled)
            val bounds=destinationButton.visibleBounds
            assertFalse("${format.label} destination button has visible bounds",bounds.isEmpty)
            // The monitor immediately cancels the external picker. UiObject.click()
            // can then report false despite the tap being handled, because its
            // accessibility-event acknowledgement never arrives. Inject the same
            // physical tap and synchronize on the actual picker request below.
            assertTrue("${format.label} destination tap injected",device.click(bounds.centerX(),bounds.centerY()))
            awaitState("${format.label} picker") {monitor.requests.count {request -> request.action==Intent.ACTION_CREATE_DOCUMENT}==before+1}
            val request=monitor.requests.last {it.action==Intent.ACTION_CREATE_DOCUMENT}
            assertEquals(format.mime,request.type)
            assertTrue(request.hasCategory(Intent.CATEGORY_OPENABLE))
            assertTrue(request.getStringExtra(Intent.EXTRA_TITLE)!!.endsWith(format.extension))
        }
        assertTrue(ImageFormat.values().map {it.name}.containsAll(listOf("WEBP","HEIC","AVIF")))
        onMain {assertNull(it.lastIoError);assertEquals(100,it.document.bitmap.width)}
    }

    @Test fun watercolorShapesAndNumericBrushControlsWorkInTheInstalledRenderer() {
        click("tool_BRUSH");click("brush_size_value")
        setNumber("101");positive()
        assertTrue("Out-of-range input must leave the number dialog open",device.findObject(UiSelector().className(EditText::class.java.name)).exists())
        setNumber("100");positive()
        onMain {assertEquals(100f,it.document.strokeWidth,0f)}

        click("tool_WATERCOLOR")
        onMain {it.document.strokeWidth=20f;it.document.foreground=Color.RED;it.document.watercolorStrength=20}
        drag(20f,40f,80f,40f)
        onMain {
            val pixel=it.document.bitmap.getPixel(50,40)
            assertEquals(255,Color.alpha(pixel));assertTrue(Color.green(pixel) in 1..254)
            assertTrue(it.document.canUndo)
        }
        click("undo")
        onMain {assertEquals(Color.WHITE,it.document.bitmap.getPixel(50,40))}
        for(tool in listOf(PaintTool.HEART,PaintTool.STAR,PaintTool.ARROW)) {
            click("tool_${tool.name}")
            onMain {it.document.foreground=Color.RED;it.document.shapeStyle=1}
            drag(15f,15f,80f,80f)
            onMain {
                val pixels=IntArray(10000);it.document.bitmap.getPixels(pixels,0,100,0,0,100,100)
                assertTrue(tool.name,pixels.count {pixel -> pixel==Color.RED}>150)
                assertTrue(pixels.all {pixel -> Color.alpha(pixel)==255})
            }
            click("undo")
            onMain {assertFalse(it.document.canUndo)}
        }
    }

    @Test fun responsiveCategoriesOpenBesideTheToolStripInBothOrientations() {
        fun position(view: View)=IntArray(2).also {view.getLocationOnScreen(it)}
        try {
            for(landscape in listOf(false,true)) {
                val expected=if(landscape) android.content.res.Configuration.ORIENTATION_LANDSCAPE else android.content.res.Configuration.ORIENTATION_PORTRAIT
                onMain {it.requestedOrientation=if(landscape) android.content.pm.ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE else android.content.pm.ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}
                awaitState("responsive toolbox orientation") {it.resources.configuration.orientation==expected && it.paintCanvas.width>0}
                instrumentation.waitForIdleSync()
                for(category in ToolCategory.values()) {
                    onMain {
                        val button=it.window.decorView.findViewWithTag<ToolCategoryButton>("category_${category.name}")
                        if(!button.expanded) assertTrue(button.performClick())
                    }
                    instrumentation.waitForIdleSync()
                    onMain {
                        val root=it.window.decorView
                        val drawer=root.findViewWithTag<View>("tool_scroll")
                        val strip=root.findViewWithTag<View>("primary_tool_scroll")
                        assertTrue(drawer.isShown)
                        if(landscape) {
                            assertEquals(position(strip)[0]+strip.width,position(drawer)[0])
                            assertEquals(position(strip)[1],position(drawer)[1])
                            assertEquals(position(drawer)[0]+drawer.width,position(it.paintCanvas)[0])
                            assertTrue(it.paintCanvas.height>root.height/2)
                        } else {
                            assertEquals(position(strip)[1]+strip.height,position(drawer)[1])
                            assertEquals(root.width,it.paintCanvas.width)
                        }
                        val header=root.findViewWithTag<View>("header_bar")
                        val quick=root.findViewWithTag<View>("quick_actions")
                        assertTrue(position(quick)[1]>=position(header)[1])
                        assertTrue(position(quick)[1]+quick.height<=position(header)[1]+header.height)
                        assertEquals(root.width,position(quick)[0]+quick.width)
                        assertNull(root.findViewWithTag<View>("compact_menu"))
                        for(tab in listOf("View","Draw","File","Edit","Color")) assertTrue(root.findViewWithTag<View>("menu_$tab").isShown)

                    }
                    for(tool in category.tools) {
                        click("tool_${tool.name}")
                        onMain {assertEquals(tool,it.paintCanvas.tool)}
                    }
                    click("category_${category.name}")
                    onMain {assertFalse(it.window.decorView.findViewWithTag<View>("tool_scroll").isShown)}
                }
            }
        } finally {onMain {it.requestedOrientation=android.content.pm.ActivityInfo.SCREEN_ORIENTATION_PORTRAIT}}
    }

    @Test fun cursorDrawingMagnifierAndFitAreAvailableFromTheViewMenu() {
        menu("View",text(R.string.ui_enable_cursor_drawing))
        onMain {assertTrue(it.paintCanvas.cursorMode)}
        drag(20f,20f,30f,20f)
        onMain {assertFalse(it.document.canUndo)}
        drag(20f,20f,20f,20f) // A tap toggles cursor ink on.
        onMain {assertTrue(it.paintCanvas.cursorDrawing)}
        drag(20f,20f,40f,40f)
        onMain {assertTrue(it.document.canUndo)}
        click("undo")
        menu("View",text(R.string.ui_magnified_preview))
        clickText(text(R.string.ui_show_magnified_drawing_preview));positive()
        onMain {assertTrue(it.paintCanvas.magnifiedPreview);it.paintCanvas.zoomAt(5f)}
        click("zoom_fit_view")
        onMain {
            val centre=it.paintCanvas.toScreen(50f,50f)
            val inset=20*it.resources.displayMetrics.density
            assertEquals((it.paintCanvas.width-inset)/2,centre.x,1f)
            assertEquals((it.paintCanvas.height-inset)/2,centre.y,1f)
        }
    }

    @Test fun galleryMenuStartsTheCreditedGalleryActivityWithoutRequiringASeparateEditor() {
        menu("File",text(R.string.ui_catrobat_sticker_gallery))
        awaitState("gallery launch") {monitor.requests.any {request -> request.component?.className==MediaGalleryActivity::class.java.name}}
        val gallery=monitor.requests.single {it.component?.className==MediaGalleryActivity::class.java.name}
        assertEquals(context.packageName,gallery.component!!.packageName)
        onMain {assertEquals(100,it.document.bitmap.width);assertNull(it.lastIoError)}
    }

    @Test fun largestBundledTermsKeepFooterVisibleAndCopyAllTextThroughTheAndroidClipboard() {
        val expected=context.assets.open("legal/THIRD_PARTY_NOTICES.txt").bufferedReader().use {it.readText()}
        assertTrue("Exercise the complete large bundled notice, not a short substitute",expected.length>300000)
        lateinit var dialog: Dialog
        onMain {dialog=LegalInfo.termsDialog(it,text(R.string.ui_third_party_notices),expected);dialog.show()}
        try {
            awaitState("large terms dialog layout") {
                dialog.window!!.decorView.findViewWithTag<View>("terms_actions").height>0
            }
            val footerBounds=Rect()
            onMain {
                val root=dialog.window!!.decorView
                assertEquals(expected,root.findViewWithTag<TextView>("terms_text").text.toString())
                val footer=root.findViewWithTag<View>("terms_actions")
                assertTrue(footer.getGlobalVisibleRect(footerBounds))
                for(tag in listOf("terms_copy","terms_more","terms_done")) {
                    val button=root.findViewWithTag<View>(tag);val visible=Rect()
                    assertSame(footer,button.parent)
                    assertTrue("Visible fixed action: $tag",button.isShown && button.getGlobalVisibleRect(visible))
                    assertTrue("Usable action height: $tag",visible.height()>=button.height/2)
                }
                val scroll=root.findViewWithTag<ScrollView>("terms_scroll")
                assertTrue("Long notice must scroll independently",scroll.canScrollVertically(1))
                scroll.scrollTo(0,scroll.getChildAt(0).height)
            }
            instrumentation.waitForIdleSync()
            onMain {
                val root=dialog.window!!.decorView;val after=Rect()
                assertTrue(root.findViewWithTag<View>("terms_actions").getGlobalVisibleRect(after))
                assertEquals("Scrolling the legal text must not move its actions",footerBounds,after)
                assertTrue(root.findViewWithTag<View>("terms_copy").performClick())
            }
            instrumentation.waitForIdleSync()
            onMain {
                val clipboard=it.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                val clip=clipboard.primaryClip
                assertNotNull("Copy all must reach the system clipboard",clip)
                assertEquals(1,clip!!.itemCount)
                assertEquals("The Android clipboard must contain every displayed character",expected,clip.getItemAt(0).text.toString())
                assertTrue(dialog.window!!.decorView.findViewWithTag<View>("terms_done").performClick())
                assertFalse(dialog.isShowing)
            }
        } finally {onMain {dialog.dismiss()}}
    }

    private fun fixture(name: String)=File(File(context.cacheDir,"images").apply {mkdirs()},name).also {it.delete();fixtures.add(it)}
    private fun uriFor(file: File)=FileProvider.getUriForFile(context,"${context.packageName}.fileprovider",file)
    private fun resultFor(file: File)=Intent().setData(uriFor(file)).addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
    private fun text(id: Int)=context.getString(id)
    private fun onMain(action: (ClassicPaintActivity)->Unit) {
        val failure=AtomicReference<Throwable?>()
        instrumentation.runOnMainSync {try {action(activity)} catch(error: Throwable) {failure.set(error)}}
        failure.get()?.let {throw it}
    }
    private fun click(tag: String) {
        awaitState("ready for $tag") {!it.busy}
        onMain { editor ->
            val activeTab=when {
                tag=="tool_ZOOM"->"View"
                tag.startsWith("tool_") || tag.startsWith("category_")->"Draw"
                tag.startsWith("colour_") || tag in listOf("foreground_colour","background_colour")->"Color"
                else->null
            }
            activeTab?.let {editor.window.decorView.findViewWithTag<View>("menu_$it").performClick()}
            val tool=PaintTool.values().firstOrNull {tag=="tool_${it.name}"}
            tool?.let {ToolCategory.forTool(it)}?.let {category ->
                val button=editor.window.decorView.findViewWithTag<ToolCategoryButton>("category_${category.name}")
                if(!button.expanded) assertTrue(button.performClick())
            }
        }
        instrumentation.waitForIdleSync()
        onMain {
            val view=it.window.decorView.findViewWithTag<View>(tag)
            assertNotNull(tag,view)
            assertTrue("Control is in an expanded panel: $tag",view.isShown)
            view.requestRectangleOnScreen(Rect(0,0,view.width,view.height),true)
        }
        instrumentation.waitForIdleSync()
        onMain {
            val view=it.window.decorView.findViewWithTag<View>(tag)
            assertTrue("Control is visible after scrolling: $tag",view.getGlobalVisibleRect(Rect()))
            assertTrue(tag,view.performClick())
        }
        instrumentation.waitForIdleSync()
    }
    private fun clickText(value: String) {
        val view=device.findObject(UiSelector().text(value))
        assertTrue("Visible control: $value",view.waitForExists(5000));assertTrue(view.click())
        instrumentation.waitForIdleSync()
    }
    private fun menu(group: String,item: String) {
        click("menu_$group")
        var target: View?=null
        onMain {editor ->
            fun locate(view: View): View? {
                if(view is android.widget.Button && view.text.toString()==item && view.tag?.toString()?.startsWith("command_")==true) return view
                if(view is android.view.ViewGroup) for(i in 0 until view.childCount) locate(view.getChildAt(i))?.let {return it}
                return null
            }
            target=locate(editor.window.decorView);assertNotNull(item,target)
        }
        click(target!!.tag.toString())
    }

    private fun positive() {
        val button=device.findObject(UiSelector().resourceId("android:id/button1"))
        assertTrue("Dialog positive button",button.waitForExists(5000));assertTrue(button.click())
        instrumentation.waitForIdleSync()
    }
    private fun setNumber(value: String) {
        val input=device.findObject(UiSelector().className(EditText::class.java.name))
        assertTrue(input.waitForExists(5000));assertTrue(input.setText(value))
    }
    private fun drag(x1: Float,y1: Float,x2: Float,y2: Float) {
        awaitState("ready to draw") {!it.busy}
        onMain {
            val start=SystemClock.uptimeMillis()
            val points=listOf(Triple(MotionEvent.ACTION_DOWN,x1,y1),Triple(MotionEvent.ACTION_MOVE,(x1+x2)/2,(y1+y2)/2),Triple(MotionEvent.ACTION_UP,x2,y2))
            points.forEachIndexed {index,(action,x,y) ->
                val p=it.paintCanvas.toScreen(x,y)
                MotionEvent.obtain(start,start+index*16,action,p.x,p.y,0).also {event -> it.paintCanvas.dispatchTouchEvent(event);event.recycle()}
            }
        }
        instrumentation.waitForIdleSync()
    }
    private fun awaitState(description: String,condition: (ClassicPaintActivity)->Boolean) {
        val done=CountDownLatch(1);val error=AtomicReference<Throwable?>();val handler=Handler(Looper.getMainLooper())
        val until=SystemClock.uptimeMillis()+15000
        val check=object: Runnable {
            override fun run() {
                try {
                    if(condition(activity)) {done.countDown();return}
                    if(SystemClock.uptimeMillis()<until) {handler.postDelayed(this,25);return}
                    error.set(AssertionError("Timed out: $description; last I/O error: ${activity.lastIoError}"))
                } catch(failure: Throwable) {error.set(failure)}
                done.countDown()
            }
        }
        handler.post(check)
        try {assertTrue("Timed out: $description",done.await(16,TimeUnit.SECONDS));error.get()?.let {throw it}}
        finally {handler.removeCallbacks(check)}
    }
}
