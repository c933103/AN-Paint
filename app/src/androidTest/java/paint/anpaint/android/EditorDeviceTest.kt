/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later. */
package paint.anpaint.android

import android.app.Activity
import android.app.Dialog
import android.app.Instrumentation
import android.app.LocaleManager
import android.content.ClipData
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
import android.os.Build
import android.os.Looper
import android.os.LocaleList
import android.os.SystemClock
import android.view.MotionEvent
import android.view.KeyEvent
import android.view.View
import android.view.ViewGroup
import android.view.inspector.WindowInspector
import android.widget.EditText
import android.widget.ListView
import android.widget.ScrollView
import android.widget.TextView
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
import androidx.test.uiautomator.UiScrollable
import androidx.test.uiautomator.UiSelector
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.ClassicPaintActivity
import org.catrobat.paintroid.classic.ImageFormat
import org.catrobat.paintroid.classic.ImageDimensions
import org.catrobat.paintroid.classic.HeifCodec
import org.catrobat.paintroid.classic.JxlCodec
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
    private var originalLanguageTag=""
    private val lifecycleCallback=ActivityLifecycleCallback { observed,stage ->
        // Android's app-locale change can recreate the Activity even when its
        // ordinary configuration callback is handled. Never keep a dead editor.
        if(observed is ClassicPaintActivity && stage==Stage.CREATED) activity=observed
    }
    private val fixtures=mutableListOf<File>()

    private class ExternalActivities : Instrumentation.ActivityMonitor() {
        val requests=CopyOnWriteArrayList<Intent>()
        val nextResult=AtomicReference<Intent?>()
        override fun onStartActivity(intent: Intent): Instrumentation.ActivityResult? {
            val isPicker=intent.action==Intent.ACTION_OPEN_DOCUMENT || intent.action==Intent.ACTION_GET_CONTENT || intent.action==Intent.ACTION_CREATE_DOCUMENT
            val isGallery=intent.component?.className==MediaGalleryActivity::class.java.name
            if(!isPicker && intent.action!=Intent.ACTION_CHOOSER && !isGallery) return null
            requests.add(Intent(intent))
            val result=if(isPicker || isGallery) nextResult.getAndSet(null) else null
            return Instrumentation.ActivityResult(if(result==null) Activity.RESULT_CANCELED else Activity.RESULT_OK,result)
        }
    }

    @Before fun launchInstalledApp() {
        assertEquals("paint.anpaint.android",context.packageName)
        originalLanguageTag=if(Build.VERSION.SDK_INT>=33)
            context.getSystemService(LocaleManager::class.java).applicationLocales.toLanguageTags()
        else context.getSharedPreferences("app-language",0).getString("language-tag","").orEmpty()
        instrumentation.runOnMainSync {ActivityLifecycleMonitorRegistry.getInstance().addLifecycleCallback(lifecycleCallback)}
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
        dismissClipboardOverlay()
    }

    @After fun closeInstalledApp() {
        try {
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
        } finally {
            // A failed assertion/teardown must not leave a monitor intercepting the
            // next test's picker results or leak a vertical locale into its layout.
            if(::monitor.isInitialized) instrumentation.removeMonitor(monitor)
            instrumentation.runOnMainSync {ActivityLifecycleMonitorRegistry.getInstance().removeLifecycleCallback(lifecycleCallback)}
            restoreOriginalLanguage()
            fixtures.forEach {it.delete()}
            if(::activity.isInitialized) dismissClipboardOverlay()
        }
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
        otherImage(text(R.string.ui_from_device34))
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
            menu("File",text(R.string.save20_title))
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
            menu("File",text(if(!format.isDerivedExport) R.string.save20_title else R.string.ui_export_as23))
            assertTrue(device.findObject(UiSelector().className("android.widget.Spinner")).click())
            tapFormatChoice(format.label)
            // Confirm the popup actually completed selection. Ignoring a failed
            // UiObject.click can leave it covering the destination button.
            val selected=device.findObject(UiSelector().className("android.widget.Spinner")
                .childSelector(UiSelector().text(format.label)))
            assertTrue("${format.label} is selected in the closed spinner",selected.waitForExists(5000))
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

    @Test fun cursorPositionsUntilVisibleStartControlEnablesRealTouchDrawing() {
        menu("View",text(R.string.ui_cursor_drawing32))
        onMain {
            val toggle=it.window.decorView.findViewWithTag<View>("cursor_mode_enabled")
            assertTrue(toggle is android.widget.Button);assertFalse(toggle is android.widget.CompoundButton)
            val cursor=it.window.decorView.findViewWithTag<View>("command_View_2")
            val grid=it.window.decorView.findViewWithTag<View>("command_View_1")
            assertEquals(cursor.width,cursor.height);assertEquals(grid.height,cursor.height)
        }
        click("cursor_mode_enabled")
        onMain {
            assertTrue("Enabling keeps the options drawer open",it.window.decorView.findViewWithTag<View>("cursor_options").isShown)
            val control=it.window.decorView.findViewWithTag<View>("cursor_draw_toggle")
            assertEquals((64*it.resources.displayMetrics.density+.5f).toInt(),control.height)
        }
        onMain {assertEquals(text(R.string.ui_disable_cursor_drawing33),it.window.decorView.findViewWithTag<android.widget.Button>("cursor_mode_enabled").text.toString())}
        onMain {assertTrue(it.paintCanvas.cursorMode);assertFalse(it.paintCanvas.cursorDrawing);it.document.foreground=Color.RED;it.document.strokeWidth=4f}
        // Inject through Android's input dispatcher instead of calling the
        // canvas handler directly; verify a line, not merely an undo entry/dot.
        val coordinates=IntArray(4)
        onMain {
            val location=IntArray(2);it.paintCanvas.getLocationOnScreen(location)
            val from=it.paintCanvas.toScreen(20f,20f);val to=it.paintCanvas.toScreen(40f,40f)
            coordinates[0]=location[0]+from.x.toInt();coordinates[1]=location[1]+from.y.toInt()
            coordinates[2]=location[0]+to.x.toInt();coordinates[3]=location[1]+to.y.toInt()
        }
        assertTrue(device.swipe(coordinates[0],coordinates[1],coordinates[2],coordinates[3],20))
        instrumentation.waitForIdleSync()
        onMain {assertFalse(it.document.canUndo);for(y in 0 until 100) for(x in 0 until 100) assertEquals(Color.WHITE,it.document.bitmap.getPixel(x,y))}
        clickText(text(R.string.ui_cursor_start31))
        onMain {assertTrue("Start keeps settings open",it.window.decorView.findViewWithTag<View>("cursor_options").isShown)}
        assertTrue(device.swipe(coordinates[2],coordinates[3],coordinates[0],coordinates[1],20))
        instrumentation.waitForIdleSync()
        var drawn=IntArray(0)
        onMain {
            assertTrue(it.document.canUndo);assertTrue(it.paintCanvas.cursorDrawing)
            drawn=IntArray(10000).also {pixels ->it.document.bitmap.getPixels(pixels,0,100,0,0,100,100)}
            val ink=drawn.indices.filter {index ->drawn[index]==Color.RED}
            assertTrue("Cursor must produce a visible line",ink.isNotEmpty())
            assertTrue("Movement must paint beyond the initial dot",ink.maxOf {index ->index%100}-ink.minOf {index ->index%100}>10)
        }
        clickText(text(R.string.ui_cursor_stop31))
        onMain {assertTrue("Stop keeps settings open",it.window.decorView.findViewWithTag<View>("cursor_options").isShown)}
        drag(20f,20f,30f,20f);drag(20f,20f,20f,20f)
        onMain {
            assertFalse(it.paintCanvas.cursorDrawing)
            val moved=IntArray(10000);it.document.bitmap.getPixels(moved,0,100,0,0,100,100)
            assertArrayEquals(drawn,moved)
        }
        click("undo")
        onMain {for(y in 0 until 100) for(x in 0 until 100) assertEquals(Color.WHITE,it.document.bitmap.getPixel(x,y))}
        onMain {
            assertTrue(it.paintCanvas.cursorMagnifier)
            val root=it.window.decorView
            assertTrue(root.findViewWithTag<View>("cursor_settings_panel").isShown)
            assertNull(root.findViewWithTag<View>("cursor_controls"))
            assertNull(root.findViewWithTag<View>("cursor_brush"))
            val tip=it.document.brushTip
            root.findViewWithTag<android.widget.Spinner>("cursor_shape").setSelection(1)
            assertEquals(tip,it.document.brushTip)
        }
        click("cursor_magnifier_enabled")
        onMain {assertFalse(it.paintCanvas.cursorMagnifier);it.paintCanvas.zoomAt(5f)}
        click("zoom_fit_view")
        onMain {
            val centre=it.paintCanvas.toScreen(50f,50f)
            val inset=20*it.resources.displayMetrics.density
            assertEquals((it.paintCanvas.width-inset)/2,centre.x,1f)
            assertEquals((it.paintCanvas.height-inset)/2,centre.y,1f)
        }
    }

    @Test fun tappingCursorWithAndroidInputTogglesDrawingWithoutLeavingADot() {
        menu("View",text(R.string.ui_cursor_drawing32));click("cursor_mode_enabled")
        fun tapCursor() {
            awaitState("ready to tap cursor") {!it.busy}
            val target=IntArray(2)
            onMain {
                val state=it.paintCanvas.draftState()
                val cursor=it.paintCanvas.toScreen(state.getDouble("cursor_x").toFloat(),state.getDouble("cursor_y").toFloat())
                it.paintCanvas.getLocationOnScreen(target)
                target[0]+=cursor.x.toInt();target[1]+=cursor.y.toInt()
            }
            assertTrue(device.click(target[0],target[1]));instrumentation.waitForIdleSync()
        }
        tapCursor()
        onMain {
            assertTrue(it.paintCanvas.cursorDrawing);assertFalse(it.document.canUndo)
            assertEquals(text(R.string.ui_cursor_stop31),it.window.decorView.findViewWithTag<View>("cursor_draw_toggle").contentDescription.toString())
        }
        tapCursor()
        onMain {
            assertFalse(it.paintCanvas.cursorDrawing);assertFalse(it.document.canUndo)
            for(y in 0 until 100) for(x in 0 until 100) assertEquals(Color.WHITE,it.document.bitmap.getPixel(x,y))
        }
    }

    @Test fun saveAsJpegXlAndSubsequentSavePreserveEveryCanvasPixel() {
        val width=257;val height=193
        val expected=IntArray(width*height) {i ->val x=i%width;val y=i/width;Color.rgb((x*13+y*7)%256,(x*3+y*29)%256,(x*19+y*5)%256)}
        onMain {
            it.document.newImage(width,height)
            it.document.bitmap.setPixels(expected,0,width,0,0,width,height)
            it.document.edited();it.paintCanvas.fit()
        }
        val destination=fixture("device-lossless.jxl")
        monitor.nextResult.set(resultFor(destination))
        menu("File",text(R.string.save20_title))
        assertTrue(device.findObject(UiSelector().className("android.widget.Spinner")).click())
        assertTrue(device.findObject(UiSelector().text("JPEG XL")).click())
        val lossless=device.findObject(UiSelector().text(text(R.string.ui_lossless_jpeg_xl)))
        assertTrue(lossless.exists());assertTrue(lossless.isChecked)
        positive()
        awaitState("Lossless JPEG XL saved through File Save as") {!it.busy && destination.length()>0}
        assertEquals("image/jxl",monitor.requests.last {it.action==Intent.ACTION_CREATE_DOCUMENT}.type)
        fun checkPixels() {
            assertTrue(JxlCodec.isJxl(destination))
            assertEquals(ImageDimensions(width,height),JxlCodec.dimensions(destination))
            val decoded=JxlCodec.decode(destination,ImageDimensions(width,height),256L*1024*1024)
            try {
                val actual=IntArray(expected.size);decoded.getPixels(actual,0,width,0,0,width,height)
                assertArrayEquals("Every RGB pixel must survive the application's save workflow",expected,actual)
            } finally {decoded.recycle()}
        }
        checkPixels()
        val pickerCount=monitor.requests.count {it.action==Intent.ACTION_CREATE_DOCUMENT}
        expected[0]=Color.MAGENTA
        onMain {assertFalse(it.document.dirty);assertNull(it.lastIoError);it.document.bitmap.setPixel(0,0,Color.MAGENTA);it.document.edited()}
        menu("File",text(R.string.ui_save))
        awaitState("Save updates the original lossless JPEG XL destination") {!it.busy && !it.document.dirty}
        assertEquals(pickerCount,monitor.requests.count {it.action==Intent.ACTION_CREATE_DOCUMENT})
        checkPixels()
    }

    @Test fun lossyJpegXlAndAvifQualityControlsChangeTheEncodedImage() {
        onMain {a ->for(y in 0 until 100) for(x in 0 until 100) a.document.bitmap.setPixel(x,y,Color.rgb((x*13+y*7)%256,(x*3+y*29)%256,(x*19+y*5)%256))}
        for(format in listOf(ImageFormat.JPEG_XL,ImageFormat.AVIF)) {
            val outputs=mutableListOf<ByteArray>()
            for(quality in listOf(20,95)) {
                val destination=fixture("quality-${format.name}-$quality${format.extension}")
                monitor.nextResult.set(resultFor(destination))
                menu("File",text(R.string.save20_title))
                assertTrue(device.findObject(UiSelector().className("android.widget.Spinner")).click())
                assertTrue(device.findObject(UiSelector().text(format.label)).click())
                val lossless=device.findObject(UiSelector().className("android.widget.CheckBox").textContains(format.label))
                assertTrue(lossless.exists());if(lossless.isChecked) assertTrue(lossless.click())
                val qualityButton=device.findObject(UiSelector().className("android.widget.Button").textContains(text(R.string.ui_quality)))
                assertTrue(qualityButton.waitForExists(5000));assertTrue(qualityButton.click())
                setNumber(quality.toString());positive();positive()
                awaitState("${format.label} quality $quality image") {!it.busy && destination.length()>0}
                val decoded=if(format==ImageFormat.JPEG_XL) JxlCodec.decode(destination,ImageDimensions(100,100),256L*1024*1024)
                    else HeifCodec.decode(destination,ImageDimensions(100,100),256L*1024*1024)
                try {assertEquals(100,decoded.width);assertEquals(100,decoded.height)} finally {decoded.recycle()}
                onMain {assertNull(it.lastIoError);assertFalse(it.document.dirty)}
                outputs.add(destination.readBytes())
            }
            assertFalse("${format.label} must use the chosen quality",outputs[0].contentEquals(outputs[1]))
            assertTrue("${format.label} high quality retains more of this detailed pattern",outputs[1].size>outputs[0].size)
        }
    }

    private fun otherImage(label: String) {
        click("menu_Draw")
        onMain {editor ->
            val category=editor.window.decorView.findViewWithTag<ToolCategoryButton>("category_INSERT")
            if(!category.expanded) assertTrue(category.performClick())
        }
        click("insert_other_images");clickText(label)
    }

    @Test fun galleryMenuStartsTheCreditedGalleryActivityWithoutRequiringASeparateEditor() {
        otherImage(text(R.string.ui_catrobat_sticker_gallery))
        awaitState("gallery launch") {monitor.requests.any {request -> request.component?.className==MediaGalleryActivity::class.java.name}}
        val gallery=monitor.requests.single {it.component?.className==MediaGalleryActivity::class.java.name}
        assertEquals(context.packageName,gallery.component!!.packageName)
        onMain {assertEquals(100,it.document.bitmap.width);assertNull(it.lastIoError)}
    }

    @Test @SdkSuppress(minSdkVersion=29)
    fun insertedCreditsStayCollapsedAndCopyExactlyFromSaveAndExport() {
        checkSaveAndExportCredits(insertCreditedGalleryFixture())
    }

    @Test @SdkSuppress(minSdkVersion=29)
    fun insertedCreditsRemainOriginalAndCopyableAfterChoosingVerticalEnglish() {
        val expected=insertCreditedGalleryFixture()
        try {
            chooseAppLanguage("en-XV")
            awaitState("vertical English workspace") {
                it.resources.configuration.locales[0].toLanguageTag()=="en-XV" &&
                    it.window.decorView.findViewWithTag<View>("vertical_status_rail")?.isShown==true
            }
            onMain {
                assertEquals("Canvas width survives locale recreation",100,it.document.bitmap.width)
                assertEquals("Canvas height survives locale recreation",100,it.document.bitmap.height)
                assertEquals(Color.WHITE,it.document.bitmap.getPixel(0,0))
                val selection=it.document.selection
                assertNotNull("Floating insertion survives locale recreation",selection)
                assertEquals(3,selection!!.image.width);assertEquals(2,selection.image.height)
                assertEquals(Color.MAGENTA,selection.image.getPixel(0,0))
                assertEquals(0f,selection.rect.left,0f);assertEquals(0f,selection.rect.top,0f)
                assertEquals(3f,selection.rect.right,0f);assertEquals(2f,selection.rect.bottom,0f)
            }
            checkSaveAndExportCredits(expected,vertical=true)
        } finally {
            var dialogOpen=false;onMain {dialogOpen=creditDialogRoot()!=null}
            if(dialogOpen) {
                instrumentation.sendKeyDownUpSync(KeyEvent.KEYCODE_BACK)
                awaitState("credit dialog dismissed before locale restoration") {creditDialogRoot()==null}
            }
            restoreOriginalLanguage()
        }
    }

    private fun insertCreditedGalleryFixture(): String {
        // Substitute the remote gallery result only. The installed activity still
        // validates the source, decodes the file, inserts it and retains its credit.
        val source="https://catrobat.org/wp-content/uploads/2025/01/Needle_Yellow.png"
        val title="Artwork 作品"
        val author="Artist 作者 👩🏽‍🎨"
        val authorUrl="https://example.org/artist"
        val licence="https://creativecommons.org/licenses/by-sa/4.0/"
        val file=File(context.cacheDir,"gallery-device-credit.png").also {it.delete();fixtures.add(it)}
        val image=Bitmap.createBitmap(3,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)}
        try {file.outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {image.recycle()}
        var expected=""
        onMain {
            expected=listOf(it.getString(R.string.gallery_credit_title,title),
                it.getString(R.string.gallery_credit_publisher),it.getString(R.string.gallery_credit_source,source),
                it.getString(R.string.gallery_credit_gallery,MediaGalleryActivity.GALLERY),
                it.getString(R.string.gallery_credit_licence,licence),author,authorUrl).joinToString("\n")
        }
        monitor.nextResult.set(Intent().putExtra("gallery_file",file.name).putExtra("gallery_source",source)
            .putExtra("gallery_provider","CATROBAT").putExtra("gallery_title",title)
            .putExtra("gallery_author",author).putExtra("gallery_author_url",authorUrl).putExtra("gallery_licence",licence))
        otherImage(activityText(R.string.ui_catrobat_sticker_gallery))
        awaitState("credited gallery image inserted") {!it.busy && it.document.selection?.floating==true}
        onMain {
            assertEquals(100,it.document.bitmap.width);assertEquals(100,it.document.bitmap.height)
            assertEquals(3,it.document.selection!!.image.width);assertEquals(2,it.document.selection!!.image.height)
            assertEquals(Color.MAGENTA,it.document.selection!!.image.getPixel(0,0))
            assertEquals(listOf(source),it.document.imageCredits.map {credit -> credit.source})
            assertEquals(listOf(expected),it.document.imageCredits.map {credit -> credit.text})
            assertNull(it.lastIoError)
        }
        assertFalse("The decoded temporary gallery file is removed",file.exists())
        return expected
    }

    @android.annotation.TargetApi(29)
    private fun checkSaveAndExportCredits(expected: String,vertical: Boolean=false) {
        val requestsBefore=monitor.requests.size
        onMain {
            assertEquals("Inserted attribution survives the current activity",listOf(expected),it.document.imageCredits.map {credit ->credit.text})
            assertNotNull("The credited inserted image is still pending",it.document.selection)
        }
        for(title in listOf(R.string.save20_title,R.string.ui_export_as23)) {
            android.util.Log.i("EditorDeviceTest","Checking credit panel ${activityText(title)}, vertical=$vertical")
            menu("File",activityText(title))
            awaitState("credit-panel dialog layout") {creditDialogRoot()?.height?.let {height ->height>0}==true}
            onMain {
                val root=creditDialogRoot()!!
                if(vertical) assertNotNull("Vertical Save/Export form",root.findViewWithTag<View>("vertical_save_form"))
                val details=root.findViewWithTag<View>("export_credit_details")
                assertNotNull("Save/Export includes the retained document credits",details)
                assertEquals("Each panel starts collapsed",View.GONE,details.visibility)
                assertFalse(root.findViewWithTag<View>("export_copy_credits").isShown)
                (it.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager)
                    .setPrimaryClip(ClipData.newPlainText("test sentinel","not copied"))
            }
            // Seeding the sentinel also opens the Android 13+ SystemUI preview.
            // Remove it before real taps so it cannot intercept Expand or Copy.
            dismissClipboardOverlay(waitForAppearance=true)
            onMain {
                val clip=(it.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).primaryClip
                assertEquals("Dismissing the sentinel preview preserves its value","not copied",clip!!.getItemAt(0).text.toString())
                assertNotNull("Dismissing the sentinel preview leaves Save/Export open",creditDialogRoot())
            }
            tapCreditDialogControl("export_toggle_credits")
            onMain {
                val root=creditDialogRoot()!!
                assertEquals(View.VISIBLE,root.findViewWithTag<View>("export_credit_details").visibility)
                val field=root.findViewWithTag<TextView>("export_credit_text")
                assertEquals("Original attribution is retained character for character",expected,field.text.toString())
                assertTrue("Native text remains selectable",field.isTextSelectable)
            }
            tapCreditDialogControl("export_copy_credits")
            onMain {
                val clip=(it.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).primaryClip
                assertNotNull(clip);assertEquals(1,clip!!.itemCount)
                assertEquals("Copy reaches the real Android clipboard",expected,clip.getItemAt(0).text.toString())
                assertNotNull("Copy leaves the dialog open",creditDialogRoot())
                assertNotNull("Copy does not commit the pending image",it.document.selection)
            }
            dismissClipboardOverlay(waitForAppearance=true)
            onMain {
                val clip=(it.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).primaryClip
                assertEquals("Dismissing the system preview preserves copied attribution",expected,clip!!.getItemAt(0).text.toString())
                assertNotNull("Dismissing the preview leaves Save/Export open",creditDialogRoot())
            }
            assertEquals("Expand and Copy must not launch a destination or share activity",requestsBefore,monitor.requests.size)
            tapCreditDialogControl("export_toggle_credits")
            onMain {assertEquals(View.GONE,creditDialogRoot()!!.findViewWithTag<View>("export_credit_details").visibility)}
            val cancel=device.findObject(UiSelector().resourceId("android:id/button2"))
            assertTrue("Cancel is visible",cancel.waitForExists(5000))
            val cancelBounds=cancel.visibleBounds
            assertFalse(cancelBounds.isEmpty)
            // A dismissal may not emit UiObject.click's acknowledgement even
            // when Android handled it. Verify the actual resulting window state.
            assertTrue(device.click(cancelBounds.centerX(),cancelBounds.centerY()))
            awaitState("Cancel dismissed Save/Export") {creditDialogRoot()==null}
            onMain {assertNull(creditDialogRoot());assertNotNull(it.document.selection);assertNull(it.lastIoError)}
            assertEquals("Cancellation must not launch a destination",requestsBefore,monitor.requests.size)
            // Expansion is local to one dialog; reopening starts collapsed again.
            menu("File",activityText(title))
            awaitState("reopened credit panel") {creditDialogRoot()!=null}
            onMain {assertEquals(View.GONE,creditDialogRoot()!!.findViewWithTag<View>("export_credit_details").visibility)}
            instrumentation.sendKeyDownUpSync(KeyEvent.KEYCODE_BACK)
            awaitState("Back dismissed Save/Export") {creditDialogRoot()==null}
            onMain {assertNull(creditDialogRoot());assertNotNull(it.document.selection)}
            assertEquals("Back must not confirm Save/Export",requestsBefore,monitor.requests.size)
        }
    }

    @android.annotation.TargetApi(29)
    private fun creditDialogRoot(): View?=WindowInspector.getGlobalWindowViews().lastOrNull {
        it.isShown && it.findViewWithTag<View>("export_filename")!=null
    }

    @android.annotation.TargetApi(29)
    private fun tapCreditDialogControl(tag: String) {
        onMain {
            val view=creditDialogRoot()!!.findViewWithTag<View>(tag)
            assertTrue("Shown credit control: $tag",view.isShown)
            view.requestRectangleOnScreen(Rect(0,0,view.width,view.height),true)
        }
        instrumentation.waitForIdleSync()
        val bounds=Rect()
        onMain {
            val view=creditDialogRoot()!!.findViewWithTag<View>(tag)
            assertTrue("Reachable credit control: $tag",view.getGlobalVisibleRect(bounds))
            assertTrue("Usable credit-control height: $tag",bounds.height()>=view.height/2)
            offsetToScreen(view,bounds)
        }
        assertTrue("Real input tap: $tag",device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
    }

    @android.annotation.TargetApi(29)
    private fun chooseAppLanguage(tag: String) {
        menu("View",activityText(R.string.ui_languages23))
        val bounds=Rect()
        onMain {
            val tags=it.resources.getStringArray(R.array.app_language_tags).toList()
            assertTrue("Requested locale is selectable: $tag",tag.isEmpty() || tag in tags)
            val index=if(tag.isEmpty()) 0 else tags.indexOf(tag)+1
            val list=localePickerList(tags.size+1)
            list.setSelection(index)
        }
        instrumentation.waitForIdleSync()
        onMain {
            val tags=it.resources.getStringArray(R.array.app_language_tags).toList()
            val index=if(tag.isEmpty()) 0 else tags.indexOf(tag)+1
            val list=localePickerList(tags.size+1)
            val row=list.getChildAt(index-list.firstVisiblePosition)
            assertNotNull("Locale picker row: $tag",row)
            assertTrue("Exact requested locale row: $tag",tag.isEmpty() || (row as TextView).text.toString().endsWith("[$tag]"))
            assertTrue(row.getGlobalVisibleRect(bounds))
            offsetToScreen(row,bounds)
        }
        assertTrue("Choose the visible locale row",device.click(bounds.centerX(),bounds.centerY()))
        instrumentation.waitForIdleSync()
        onMain {
            assertEquals("The real picker selected the requested locale",tag,
                it.getSharedPreferences("app-language",0).getString("language-tag",null))
        }
    }

    private fun restoreOriginalLanguage() {
        instrumentation.runOnMainSync {
            context.getSharedPreferences("app-language",0).edit().putString("language-tag",originalLanguageTag)
                .putBoolean("platform-initialized",true).commit()
            if(Build.VERSION.SDK_INT>=33) context.getSystemService(LocaleManager::class.java)
                .applicationLocales=LocaleList.forLanguageTags(originalLanguageTag)
        }
        instrumentation.waitForIdleSync()
    }

    private fun activityText(id: Int): String {
        var value="";onMain {value=it.getString(id)};return value
    }

    private fun dismissClipboardOverlay(waitForAppearance: Boolean=false) {
        if(Build.VERSION.SDK_INT<33) return
        // Clipboard preview is a separate, nonfocusable SystemUI window. By/UiObject2
        // searches all windows; the old UiSelector only searches the active popup.
        val overlaySelector=By.res("com.android.systemui","clipboard_ui")
        val overlay=if(waitForAppearance) device.wait(Until.findObject(overlaySelector),1500)
            else device.findObject(overlaySelector)
        val showing=instrumentation.uiAutomation.windows.any {it.title?.toString()=="ClipboardOverlay"}
        if(overlay==null && !showing) return
        android.util.Log.i("EditorDeviceTest","Dismissing SystemUI clipboard preview")
        val dismiss=overlay?.findObject(By.res("com.android.systemui","dismiss_button"))
        if(dismiss!=null) {
            val bounds=dismiss.visibleBounds
            assertFalse("Clipboard preview dismiss target",bounds.isEmpty)
            assertTrue("Dismiss only the clipboard preview",device.click(bounds.centerX(),bounds.centerY()))
        }
        // Some platform variants hide the dismiss affordance. Let their bounded
        // preview timeout finish without more taps that could reset that timeout.
        assertTrue("Clipboard preview content is gone",device.wait(Until.gone(overlaySelector),10000)==true)
        awaitState("SystemUI clipboard window removed") {
            instrumentation.uiAutomation.windows.none {window ->window.title?.toString()=="ClipboardOverlay"}
        }
        android.util.Log.i("EditorDeviceTest","SystemUI clipboard preview removed")
    }

    private fun tapFormatChoice(label: String) {
        val bounds=Rect()
        if(Build.VERSION.SDK_INT>=29) {
            var originalSelection=-1
            onMain {
                val list=popupFormatList(label) ?: throw AssertionError("$label popup list")
                originalSelection=creditDialogRoot()!!.findViewWithTag<android.widget.Spinner>("export_format").selectedItemPosition
                val index=(0 until list.count).first {position ->list.getItemAtPosition(position).toString()==label}
                // Scroll only the popup viewport. The Spinner's format changes
                // later through the injected input, not this list highlight.
                list.setSelectionFromTop(index,0)
            }
            awaitState("$label popup row laid out") {popupFormatChoice(label)?.height?.let {height ->height>0}==true}
            onMain {
                val row=popupFormatChoice(label)
                assertNotNull("$label popup row",row)
                row!!.requestRectangleOnScreen(Rect(0,0,row.width,row.height),true)
            }
            instrumentation.waitForIdleSync()
            onMain {
                val row=popupFormatChoice(label)!!
                assertEquals("Scrolling must not select the format",originalSelection,
                    creditDialogRoot()!!.findViewWithTag<android.widget.Spinner>("export_format").selectedItemPosition)
                assertTrue("$label row has a visible native hit target",row.getGlobalVisibleRect(bounds))
                val parentBounds=Rect()
                (row.parent as? View)?.getGlobalVisibleRect(parentBounds)
                offsetToScreen(row,bounds)
                offsetToScreen(row,parentBounds)
                android.util.Log.i("EditorDeviceTest","Format $label rowHeight=${row.height}, screen target=$bounds, parent=$parentBounds")
                assertTrue("$label row is fully reachable after scrolling",bounds.height()>=row.height)
            }
        } else {
            val choice=device.findObject(UiSelector().text(label))
            assertTrue("$label format choice exists",choice.waitForExists(5000))
            bounds.set(choice.visibleBounds)
        }
        assertFalse("$label format choice is visible",bounds.isEmpty)
        assertTrue("$label format tap injected",device.click(bounds.centerX(),bounds.centerY()))
    }

    @android.annotation.TargetApi(29)
    private fun popupFormatList(label: String): ListView? {
        fun find(view: View): ListView? {
            if(view is ListView && view.isShown && (0 until view.count).any {view.getItemAtPosition(it).toString()==label}) return view
            if(view is ViewGroup) for(index in 0 until view.childCount) find(view.getChildAt(index))?.let {return it}
            return null
        }
        return WindowInspector.getGlobalWindowViews().asReversed().firstNotNullOfOrNull {find(it)}
    }

    @android.annotation.TargetApi(29)
    private fun popupFormatChoice(label: String): TextView? {
        fun find(view: View,inList: Boolean=false): TextView? {
            if(inList && view is TextView && view.isShown && view.text.toString()==label) return view
            if(view is ViewGroup) for(index in 0 until view.childCount)
                find(view.getChildAt(index),inList || view is ListView)?.let {return it}
            return null
        }
        return WindowInspector.getGlobalWindowViews().asReversed().firstNotNullOfOrNull {find(it)}
    }

    @android.annotation.TargetApi(29)
    private fun localePickerList(expectedCount: Int): ListView {
        // Native AlertDialog uses a private framework list ID. Locate its
        // visible list by type and the app's actual locale inventory instead.
        fun find(view: View): ListView? {
            if(view is ListView && view.isShown && view.count==expectedCount) return view
            if(view is ViewGroup) for(index in 0 until view.childCount) find(view.getChildAt(index))?.let {return it}
            return null
        }
        return WindowInspector.getGlobalWindowViews().asReversed().firstNotNullOfOrNull {find(it)}
            ?: throw AssertionError("Visible app-language picker list")
    }

    private fun offsetToScreen(view: View,bounds: Rect) {
        // getGlobalVisibleRect is root-relative; injected input uses screen
        // coordinates, including the dialog window's offset from the activity.
        val location=IntArray(2);view.rootView.getLocationOnScreen(location)
        bounds.offset(location[0],location[1])
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
            dismissClipboardOverlay(waitForAppearance=true)
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
            if(view is android.widget.CompoundButton) {
                val before=view.isChecked;view.performClick();assertNotEquals(tag,before,view.isChecked)
            } else assertTrue(tag,view.performClick())
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
