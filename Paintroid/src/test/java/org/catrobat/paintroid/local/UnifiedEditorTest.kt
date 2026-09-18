/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.graphics.*
import android.net.Uri
import android.os.Looper
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.widget.*
import org.catrobat.paintroid.classic.*
import org.catrobat.paintroid.classic.ImageFormat
import org.junit.Assert.*
import org.junit.*
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.util.Locale

@RunWith(org.robolectric.RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class UnifiedEditorTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private val doc get()=activity.document
    private val board get()=activity.paintCanvas
    private val root get()=activity.window.decorView
    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-")}?.forEach {it.delete()}
        listOf("classic-ui","recent-colours","export").forEach {context.getSharedPreferences(it,0).edit().clear().commit()}
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get()
        doc.newImage(100,100);shadowOf(Looper.getMainLooper()).idleFor(50,java.util.concurrent.TimeUnit.MILLISECONDS);board.fit()
    }
    @After fun stop() {controller.pause().stop();waitIo();controller.destroy()}
    private fun waitIo() {
        val until=System.nanoTime()+10_000_000_000
        do {shadowOf(Looper.getMainLooper()).idle();if(!activity.busy)break;Thread.sleep(10)} while(System.nanoTime()<until)
        assertFalse(activity.busy)
    }
    private fun click(tag: String) {
        val control=root.findViewWithTag<View>(tag)
        if(control is CompoundButton) {val before=control.isChecked;control.performClick();assertNotEquals(before,control.isChecked)}
        else assertTrue(control.performClick())
        shadowOf(Looper.getMainLooper()).idle()
    }
    private fun menu(group: String,label: String) { EditorTestNavigation.named(activity,group,label) }
    private fun event(action: Int,x: Float,y: Float) {
        val p=board.toScreen(x,y);val e=MotionEvent.obtain(0,20,action,p.x,p.y,0)
        board.dispatchTouchEvent(e);e.recycle()
    }
    private fun drag(x: Float,y: Float,x2: Float,y2: Float) {
        event(MotionEvent.ACTION_DOWN,x,y);event(MotionEvent.ACTION_MOVE,(x+x2)/2,(y+y2)/2);event(MotionEvent.ACTION_UP,x2,y2)
    }
    private fun pixels()=IntArray(10000).also {doc.bitmap.getPixels(it,0,100,0,0,100,100)}

    @Test fun addedShapesDrawFilledGeometryAndUndoInOneStep() {
        for(tool in listOf(PaintTool.HEART,PaintTool.STAR,PaintTool.ARROW)) {
            click("tool_${tool.name}");doc.foreground=Color.RED;doc.shapeStyle=1
            drag(15f,15f,80f,80f)
            assertTrue(tool.name,pixels().count {it==Color.RED}>150)
            assertEquals(Color.WHITE,doc.bitmap.getPixel(0,0));click("undo")
            assertTrue(pixels().all {it==Color.WHITE})
        }
    }
    @Test fun brushNumberEntryAcceptsOneHundredAndRejectsOutOfRange() {
        click("tool_BRUSH");click("brush_size_value")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val input=dialog.window!!.decorView.findViewWithTag<EditText>("numeric_input")
        input.setText("101");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertTrue(dialog.isShowing);assertNotNull(input.error)
        input.setText("100");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertFalse(dialog.isShowing);assertEquals(100f,doc.strokeWidth,0f)
        assertEquals(99,root.findViewWithTag<SeekBar>("brush_size").max)
    }
    @Test fun openPolygonConnectsStraightSegmentsWithoutClosingOrFillingThem() {
        click("tool_POLYGON")
        root.findViewWithTag<CheckBox>("polygon_close").performClick()
        shadowOf(Looper.getMainLooper()).idle();assertFalse(board.closePolygon)
        doc.foreground=Color.BLUE;doc.shapeStyle=1;doc.strokeWidth=2f
        for(point in listOf(20f to 20f,80f to 20f,80f to 80f)) {
            event(MotionEvent.ACTION_DOWN,point.first,point.second);event(MotionEvent.ACTION_UP,point.first,point.second)
        }
        click("apply")
        assertEquals(Color.BLUE,doc.bitmap.getPixel(50,20));assertEquals(Color.BLUE,doc.bitmap.getPixel(80,50))
        assertEquals(Color.WHITE,doc.bitmap.getPixel(50,50));assertEquals(Color.WHITE,doc.bitmap.getPixel(70,40))
        click("undo");assertTrue(pixels().all {it==Color.WHITE})
    }
    @Test fun watercolorStrengthBlendsIntoOpaqueCanvasAndUndoRestoresIt() {
        click("tool_WATERCOLOR");doc.strokeWidth=20f;doc.foreground=Color.RED;doc.watercolorStrength=20
        drag(20f,40f,80f,40f);val weak=doc.bitmap.getPixel(50,40)
        assertEquals(255,Color.alpha(weak));assertTrue(Color.green(weak) in 1..254)
        click("undo");doc.watercolorStrength=90;drag(20f,40f,80f,40f)
        assertTrue(Color.green(doc.bitmap.getPixel(50,40))<Color.green(weak));click("undo")
        assertTrue(pixels().all {it==Color.WHITE})
    }
    @Test fun fourRecentCellsKeepDistinctColoursAndStayAfterTheScrollablePalette() {
        for(hex in listOf("FF0000","00FF00","0000FF","FFFF00","00FFFF")) click("colour_$hex")
        assertEquals(listOf(Color.CYAN,Color.YELLOW,Color.BLUE,Color.GREEN),RecentColours(activity).colours)
        assertTrue(root.findViewWithTag<View>("recent_colour_0").contentDescription.toString().contains("#00FFFF"))
        click("recent_colour_2");assertEquals(Color.BLUE,doc.foreground)
        assertEquals(listOf(Color.BLUE,Color.CYAN,Color.YELLOW,Color.GREEN),RecentColours(activity).colours)
        val bar=root.findViewWithTag<ViewGroup>("palette_bar");val recent=root.findViewWithTag<View>("recent_colours")
        assertSame(bar,recent.parent);assertSame(recent,bar.getChildAt(bar.childCount-1))
        activity.onConfigurationChanged(activity.resources.configuration)
        assertEquals(Color.BLUE,RecentColours(activity).colours.first())
    }
    @Test fun cursorDrawMoveSwitchAndFitWorkInTheEditor() {
        menu("View","Cursor drawing");click("cursor_mode_enabled");assertTrue(board.cursorMode)
        assertFalse(board.cursorDrawing)
        val ink=root.findViewWithTag<android.widget.Button>("cursor_draw_toggle")
        assertTrue(ink.isShown);assertEquals("Start drawing",ink.text.toString())
        assertTrue("Enabling keeps cursor settings open",root.findViewWithTag<View>("cursor_options").isShown)
        assertEquals((64*activity.resources.displayMetrics.density+.5f).toInt(),ink.layoutParams.height)
        assertNull(root.findViewWithTag<View>("cursor_draw_enabled"))
        drag(20f,20f,30f,20f);assertFalse(doc.canUndo);assertTrue(pixels().all {it==Color.WHITE})
        ink.performClick();shadowOf(Looper.getMainLooper()).idle();assertTrue(board.cursorDrawing)
        assertTrue("Starting ink keeps cursor settings open",root.findViewWithTag<View>("cursor_options").isShown)
        assertEquals("Stop drawing",ink.text.toString())
        assertTrue(ink.isSelected)
        assertEquals("Pan to start drawing. Tap again to stop drawing.",org.robolectric.shadows.ShadowToast.getTextOfLatestToast())
        assertTrue("Draw toggle overlays the canvas instead of consuming a separate row",ink.parent is FrameLayout)
        event(MotionEvent.ACTION_DOWN,20f,20f);event(MotionEvent.ACTION_UP,20f,20f)
        assertTrue(board.cursorDrawing);assertTrue(doc.canUndo)
        val dot=pixels()
        drag(20f,20f,40f,40f);assertTrue(doc.canUndo);assertFalse(dot.contentEquals(pixels()))
        click("undo");assertArrayEquals(dot,pixels())
        click("undo");assertTrue(pixels().all {it==Color.WHITE})
        // Opening this category leaves brush settings solely under Drawing.
        menu("View","Cursor drawing") // explicitly close it
        menu("View","Cursor drawing") // reopen it, pausing ink
        assertFalse(board.cursorDrawing)
        val settings=root.findViewWithTag<View>("cursor_settings_panel")
        assertTrue(settings.isShown)
        assertNull(root.findViewWithTag<View>("cursor_controls"))
        assertNull(settings.findViewWithTag<View>("cursor_brush_size"))
        assertNull(settings.findViewWithTag<View>("cursor_brush"))
        val brushTip=doc.brushTip;val brushWidth=doc.strokeWidth;val chosenTool=board.tool
        settings.findViewWithTag<Spinner>("cursor_shape").setSelection(1)
        shadowOf(Looper.getMainLooper()).idle()
        assertEquals(1,board.cursorShape);assertEquals(brushTip,doc.brushTip)
        assertEquals(brushWidth,doc.strokeWidth,0f);assertEquals(chosenTool,board.tool)
        val magnifier=settings.findViewWithTag<CheckBox>("cursor_magnifier_enabled")
        assertTrue(board.cursorMagnifier)
        magnifier.performClick();assertFalse(board.cursorMagnifier)
        magnifier.performClick();assertTrue(board.cursorMagnifier)
        settings.findViewWithTag<NumericSlider>("cursor_marker_size").slider.progress=50
        assertEquals(1.5f,board.cursorMarkerScale,0f)
        board.zoomAt(5f);board.fit()
        val centre=board.toScreen(50f,50f)
        val inset=20*activity.resources.displayMetrics.density
        assertEquals((board.width-inset)/2,centre.x,1f);assertEquals((board.height-inset)/2,centre.y,1f)
    }
    @Test fun otherImagesGroupsDeviceAndIllustrationSourcesUnderDrawInsert() {
        click("menu_File")
        val names=EditorTestNavigation.buttons(root.findViewWithTag("panel_File_commands")).map {it.text.toString()}
        assertFalse(names.any {it.contains("Insert image") || it.contains("Catrobat")})
        click("menu_Draw");click("category_INSERT");click("insert_other_images")
        val dialog=ShadowAlertDialog.getLatestAlertDialog()
        assertEquals(listOf("From device…","Catrobat sticker gallery…","Irasutoya","Openclipart"),
            (0 until dialog.listView.count).map {dialog.listView.getItemAtPosition(it).toString()})
        dialog.dismiss()
        assertTrue(MediaGalleryActivity.allowed(Uri.parse("https://catrobat.org/figures-download/")))
        assertFalse(MediaGalleryActivity.allowed(Uri.parse("https://catrobat.org.example.com/x.png")))
    }
    @Test fun jpegQualityIsChosenBeforeFilePickerAndSaveAndShareWritesTheFileFirst() {
        menu("File","Save as…")
        var dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        EditorTestNavigation.format(dialog.window!!.decorView.findViewWithTag<Spinner>("export_format"),ImageFormat.JPEG)
        shadowOf(Looper.getMainLooper()).idle()
        val quality=dialog.window!!.decorView.findViewWithTag<NumericSlider>("export_quality")
        quality.slider.progress=34
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        shadowOf(Looper.getMainLooper()).idle()
        var launch=shadowOf(activity).nextStartedActivityForResult
        assertEquals("image/jpeg",launch.intent.type)
        assertEquals(launch.intent,shadowOf(activity).nextStartedActivity)
        activity.onActivityResult(launch.requestCode,Activity.RESULT_CANCELED,null)
        assertNull(shadowOf(activity).nextStartedActivity)
        menu("File","Save and share…");dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        fun prose(view: View): String = (if(view is android.widget.TextView) view.text.toString() else "")+
            if(view is android.view.ViewGroup) (0 until view.childCount).joinToString(" ") {prose(view.getChildAt(it))} else ""
        val description=prose(dialog.window!!.decorView)
        assertTrue(description.contains("then choose an app to share it"))
        assertFalse(description.contains("Export an icon"))
        EditorTestNavigation.format(dialog.window!!.decorView.findViewWithTag<Spinner>("export_format"),ImageFormat.PNG)
        shadowOf(Looper.getMainLooper()).idle();dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
        launch=shadowOf(activity).nextStartedActivityForResult
        assertEquals(launch.intent,shadowOf(activity).nextStartedActivity)
        val file=File(activity.cacheDir,"share-result.png")
        activity.onActivityResult(launch.requestCode,Activity.RESULT_OK,Intent().setData(Uri.fromFile(file)));waitIo()
        assertTrue(file.isFile);assertNotNull(BitmapFactory.decodeFile(file.path))
        val chooser=shadowOf(activity).nextStartedActivity
        assertEquals(Intent.ACTION_CHOOSER,chooser.action)
        val send=chooser.getParcelableExtra<Intent>(Intent.EXTRA_INTENT)!!
        assertEquals(Intent.ACTION_SEND,send.action);assertEquals("image/png",send.type)
        assertTrue(send.flags and Intent.FLAG_GRANT_READ_URI_PERMISSION!=0);assertNotNull(send.clipData)
    }
    @Test fun localizedDecimalEntryDoesNotChangePersistenceKeysOrToolIdentity() {
        val before=Locale.getDefault()
        try {
            Locale.setDefault(Locale.FRANCE)
            assertEquals(12.5,uiNumber("12,5")!!,0.0);assertNull(uiNumber("12,5x"))
            assertEquals("WATERCOLOR",PaintTool.WATERCOLOR.name)
            assertNotNull(root.findViewWithTag<View>("tool_WATERCOLOR"))
        } finally {Locale.setDefault(before)}
    }
    @Test fun jpegQualityChoiceChangesTheEncodedFileWhileKeepingCanvasPixels() {
        for(y in 0 until 100) for(x in 0 until 100) doc.bitmap.setPixel(x,y,Color.rgb((x*13+y*7)%256,(x*3+y*29)%256,(x*19+y*5)%256))
        val original=pixels()
        fun save(quality: Int): ByteArray {
            menu("File","Save as…")
            val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            EditorTestNavigation.format(dialog.window!!.decorView.findViewWithTag<Spinner>("export_format"),ImageFormat.JPEG)
            shadowOf(Looper.getMainLooper()).idle()
            dialog.window!!.decorView.findViewWithTag<NumericSlider>("export_quality").slider.progress=quality-1
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            val launch=shadowOf(activity).nextStartedActivityForResult
            val output=File(activity.cacheDir,"quality-$quality.jpg")
            activity.onActivityResult(launch.requestCode,Activity.RESULT_OK,Intent().setData(Uri.fromFile(output)));waitIo()
            val decoded=BitmapFactory.decodeFile(output.path)
            assertEquals(100,decoded.width);assertEquals(100,decoded.height);decoded.recycle()
            return output.readBytes()
        }
        val low=save(20);val high=save(95)
        assertTrue(high.size>low.size);assertFalse(low.contentEquals(high));assertArrayEquals(original,pixels())
    }
}
