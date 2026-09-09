/* AN Paint regression checks, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.*
import android.os.Looper
import android.view.MotionEvent
import android.view.View
import android.widget.CheckBox
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.After
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
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowPopupMenu
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33],qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class SizingAndTrimTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    @Before fun start() {
        val context = RuntimeEnvironment.getApplication() as Context
        File(context.filesDir,"classic-recovery.png").delete()
        File(context.filesDir,"classic-autosave.zip").delete(); File(context.filesDir,"classic-autosave.zip.bak").delete()
        context.getSharedPreferences("classic-ui",Context.MODE_PRIVATE).edit().clear().commit()
        controller = Robolectric.buildActivity(ClassicPaintActivity::class.java); activity = controller.setup().get()
        activity.document.newImage(200,100); activity.paintCanvas.fit()
    }
    @After fun stop() {
        ShadowAlertDialog.getLatestAlertDialog()?.dismiss(); controller.pause().stop()
        val end = System.nanoTime()+10_000_000_000L
        while (activity.busy && System.nanoTime()<end) { shadowOf(Looper.getMainLooper()).idle(); Thread.sleep(10) }
        controller.destroy()
    }
    private fun click(tag: String) { activity.window.decorView.findViewWithTag<View>(tag).performClick(); shadowOf(Looper.getMainLooper()).idle() }
    private fun drag(from: PointF,to: PointF) {
        for ((action,p) in listOf(MotionEvent.ACTION_DOWN to from,MotionEvent.ACTION_MOVE to to,MotionEvent.ACTION_UP to to)) {
            val e = MotionEvent.obtain(0,20,action,p.x,p.y,0); assertTrue(activity.paintCanvas.dispatchTouchEvent(e)); e.recycle()
        }
    }
    @Test fun percentSizingLocksOrSeparatesAxesAndSwitchingUnitsPreservesExactPixels() {
        val controls = DimensionControls(activity,ImageDimensions(1600,2400),ImageDimensions(713,1069))
        repeat(10) { controls.findViewWithTag<View>("size_percent").performClick(); controls.findViewWithTag<View>("size_pixels").performClick() }
        assertEquals(ImageDimensions(713,1069),controls.dimensions)
        controls.findViewWithTag<View>("size_percent").performClick(); controls.widthInput.setText("50")
        assertEquals(ImageDimensions(800,1200),controls.dimensions)
        assertTrue(controls.findViewWithTag<android.widget.RadioButton>("size_percent").isChecked); assertFalse(controls.findViewWithTag<android.widget.RadioButton>("size_pixels").isChecked)
        controls.aspectLock.isChecked = false; controls.heightInput.setText("25")
        assertEquals(ImageDimensions(800,600),controls.dimensions)
        controls.findViewWithTag<View>("size_pixels").performClick(); assertEquals("800",controls.widthInput.text.toString()); assertEquals("600",controls.heightInput.text.toString())
        controls.aspectLock.isChecked = true; controls.widthInput.setText("200")
        assertEquals(ImageDimensions(200,300),controls.dimensions)
    }
    @Test fun fractionalPercentUsesOriginalDimensionsAndInvalidInputsCannotOverflow() {
        val controls = DimensionControls(activity,ImageDimensions(301,199))
        controls.findViewWithTag<View>("size_percent").performClick(); controls.widthInput.setText("33.3333")
        assertEquals(ImageDimensions(100,66),controls.dimensions)
        for (invalid in listOf("0","-1","NaN","1e200","")) { controls.widthInput.setText(invalid); assertNull(invalid,controls.dimensions) }
    }
    @Test fun resizeAndCanvasSizeDialogsSupportPercentAndOptionalRatioLock() {
        click("menu_Image"); ShadowPopupMenu.getLatestPopupMenu().menu.performIdentifierAction(1,0); shadowOf(Looper.getMainLooper()).idle()
        var dialog = ShadowAlertDialog.getLatestAlertDialog() as android.app.AlertDialog
        val root = dialog.window!!.decorView
        root.findViewWithTag<View>("size_percent").performClick(); root.findViewWithTag<android.widget.EditText>("size_width").setText("50")
        render(dialog.window!!.decorView,"size-controls.png")
        dialog.getButton(android.app.AlertDialog.BUTTON_POSITIVE).performClick()
        assertEquals(100,activity.document.bitmap.width); assertEquals(50,activity.document.bitmap.height)
        activity.document.bitmap.setPixel(8,9,0xff00ff00.toInt())
        click("menu_Image"); ShadowPopupMenu.getLatestPopupMenu().menu.performIdentifierAction(2,0); shadowOf(Looper.getMainLooper()).idle()
        dialog = ShadowAlertDialog.getLatestAlertDialog() as android.app.AlertDialog
        dialog.window!!.decorView.findViewWithTag<View>("size_percent").performClick()
        assertFalse(dialog.window!!.decorView.findViewWithTag<CheckBox>("size_lock").isChecked)
        dialog.window!!.decorView.findViewWithTag<android.widget.EditText>("size_width").setText("200")
        dialog.getButton(android.app.AlertDialog.BUTTON_POSITIVE).performClick()
        assertEquals(200,activity.document.bitmap.width); assertEquals(50,activity.document.bitmap.height)
        assertEquals(0xff00ff00.toInt(),activity.document.bitmap.getPixel(8,9)); assertEquals(Color.WHITE,activity.document.bitmap.getPixel(180,9))
        activity.document.undo(); assertEquals(100,activity.document.bitmap.width)
    }
    @Test fun visibleSelectAllCanMoveImageBeyondCanvasThenTouchTrimAndUndoRestoreIt() {
        val doc = activity.document; doc.bitmap.eraseColor(Color.BLUE)
        Canvas(doc.bitmap).drawRect(0f,0f,40f,100f,Paint().apply { color = Color.RED })
        click("select_all"); assertEquals(RectF(0f,0f,200f,100f),doc.selection!!.rect)
        val canvas = activity.paintCanvas
        drag(canvas.toScreen(100f,50f),canvas.toScreen(60f,50f))
        assertTrue(doc.selection!!.floating)
        click("trim_canvas")
        assertEquals(Color.BLUE,doc.bitmap.getPixel(0,50)); assertEquals(Color.WHITE,doc.bitmap.getPixel(180,50))
        drag(canvas.toScreen(200f,100f),canvas.toScreen(160f,80f))
        assertEquals(Rect(0,0,160,80),canvas.trim!!.rect)
        render(activity.window.decorView,"canvas-trim.png")
        click("trim_apply")
        assertEquals(160,doc.bitmap.width); assertEquals(80,doc.bitmap.height); assertEquals(Color.BLUE,doc.bitmap.getPixel(159,79))
        doc.undo(); assertEquals(200,doc.bitmap.width); assertEquals(100,doc.bitmap.height)
        doc.undo(); assertEquals(Color.RED,doc.bitmap.getPixel(0,50)); assertEquals(Color.BLUE,doc.bitmap.getPixel(180,50))
    }
    @Test fun cancellingTouchTrimKeepsAllPixelsAndTrimCanRemoveLeftAndTopMargins() {
        val doc = activity.document; doc.bitmap.setPixel(30,20,Color.MAGENTA)
        click("trim_canvas"); val canvas = activity.paintCanvas
        drag(canvas.toScreen(0f,0f),canvas.toScreen(30f,20f)); assertEquals(Rect(30,20,200,100),canvas.trim!!.rect)
        click("trim_cancel"); assertEquals(200,doc.bitmap.width); assertEquals(Color.MAGENTA,doc.bitmap.getPixel(30,20))
        click("trim_canvas"); drag(canvas.toScreen(0f,0f),canvas.toScreen(30f,20f)); click("trim_apply")
        assertEquals(170,doc.bitmap.width); assertEquals(80,doc.bitmap.height); assertEquals(Color.MAGENTA,doc.bitmap.getPixel(0,0))
    }
    @Test fun touchExpansionOnEverySidePreservesOpaquePixelsAndUndo() {
        val doc=activity.document; val canvas=activity.paintCanvas
        doc.bitmap.eraseColor(Color.BLUE); doc.bitmap.setPixel(37,29,0xff00ff00.toInt()); doc.background=Color.YELLOW
        click("trim_canvas")
        drag(canvas.toScreen(0f,0f),canvas.toScreen(-20f,-10f))
        drag(canvas.toScreen(200f,100f),canvas.toScreen(225f,115f))
        assertEquals(Rect(-20,-10,225,115),canvas.trim!!.rect)
        click("trim_fit")
        val corner=canvas.toScreen(-20f,-10f); assertTrue(corner.x>0 && corner.y>0)
        render(activity.window.decorView,"canvas-expand.png")
        click("trim_apply")
        assertEquals(245,doc.bitmap.width); assertEquals(125,doc.bitmap.height)
        assertEquals(0xff00ff00.toInt(),doc.bitmap.getPixel(57,39))
        assertEquals(Color.BLUE,doc.bitmap.getPixel(20,10)); assertEquals(Color.BLUE,doc.bitmap.getPixel(219,109))
        for ((x,y) in listOf(0 to 0,244 to 124,0 to 50,100 to 0,244 to 50,100 to 124)) assertEquals(Color.YELLOW,doc.bitmap.getPixel(x,y))
        val bytes=java.io.ByteArrayOutputStream(); assertTrue(doc.bitmap.compress(Bitmap.CompressFormat.PNG,100,bytes))
        val png=BitmapFactory.decodeByteArray(bytes.toByteArray(),0,bytes.size())!!
        assertTrue(doc.bitmap.sameAs(png)); png.recycle()
        click("undo"); assertEquals(200,doc.bitmap.width); assertEquals(100,doc.bitmap.height)
        assertEquals(0xff00ff00.toInt(),doc.bitmap.getPixel(37,29)); assertFalse(doc.canUndo)
        click("redo"); assertEquals(245,doc.bitmap.width); assertEquals(0xff00ff00.toInt(),doc.bitmap.getPixel(57,39))
    }
    @Test fun noOpBoundsCreateNoHistoryAndUndoCancelsOnlyThePendingExpansion() {
        val root=activity.window.decorView; val doc=activity.document; val canvas=activity.paintCanvas
        assertFalse(root.findViewWithTag<View>("undo").isEnabled)
        click("trim_canvas"); assertFalse(root.findViewWithTag<View>("undo").isEnabled)
        click("trim_apply"); assertFalse(doc.canUndo)
        click("trim_canvas"); drag(canvas.toScreen(200f,100f),canvas.toScreen(240f,120f))
        assertTrue(root.findViewWithTag<View>("undo").isEnabled)
        click("undo"); assertNull(canvas.trim); assertEquals(200,doc.bitmap.width)
        assertFalse(root.findViewWithTag<View>("undo").isEnabled)
        assertNotNull(root.findViewWithTag<View>("clipboard_row_0"))
        click("trim_canvas"); drag(canvas.toScreen(0f,0f),canvas.toScreen(-15f,-20f)); click("trim_cancel")
        assertEquals(200,doc.bitmap.width); assertEquals(100,doc.bitmap.height); assertFalse(doc.canUndo)
    }
    @Test fun cropSourcesStayBoundedWhileCanvasEdgesExpandWithoutIntegerWrap() {
        val source=CropOverlay(ImageDimensions(200,100))
        source.begin(PointF(0f,0f),1f); source.move(PointF(-20f,-30f)); source.end()
        assertEquals(Rect(0,0,200,100),source.rect)
        for ((handle,point) in listOf(1 to PointF(100f,-20f),3 to PointF(230f,50f),5 to PointF(100f,125f),7 to PointF(-15f,50f))) {
            val overlay=CropOverlay(ImageDimensions(200,100),allowOutside=true)
            assertTrue(overlay.begin(overlay.handles()[handle],1f)); overlay.move(point); overlay.end()
            when(handle) { 1 -> assertEquals(-20,overlay.rect.top); 3 -> assertEquals(230,overlay.rect.right); 5 -> assertEquals(125,overlay.rect.bottom); 7 -> assertEquals(-15,overlay.rect.left) }
        }
        val huge=CropOverlay(ImageDimensions(200,100),allowOutside=true)
        huge.begin(PointF(0f,0f),1f); huge.move(PointF(-Float.MAX_VALUE,-Float.MAX_VALUE)); huge.end()
        assertEquals(Int.MAX_VALUE.toLong(),huge.rect.right.toLong()-huge.rect.left)
        assertEquals(Int.MAX_VALUE.toLong(),huge.rect.bottom.toLong()-huge.rect.top)
    }
    @Test fun rejectedExpansionPreservesPixelsHistoryAndTransparentBackground() {
        val doc=PaintDocument(4,4,File(activity.cacheDir,"guarded-bounds")) { w,h ->
            if (w.toLong()*h>100) throw ImageSizeException("Test memory budget exceeded")
        }
        try {
            doc.bitmap.setPixel(1,1,Color.RED); doc.background=Color.TRANSPARENT
            try { doc.changeCanvasBounds(Rect(-100,0,4,4)); fail("Oversized canvas accepted") } catch (_: ImageSizeException) { }
            assertEquals(4,doc.bitmap.width); assertEquals(Color.RED,doc.bitmap.getPixel(1,1)); assertFalse(doc.canUndo)
            try { doc.changeCanvasBounds(Rect(Int.MIN_VALUE,0,Int.MAX_VALUE,4)); fail("Overflow accepted") } catch (_: IllegalArgumentException) { }
            doc.changeCanvasBounds(Rect(-1,-1,5,5)); assertEquals(0,doc.bitmap.getPixel(0,0)); assertEquals(Color.RED,doc.bitmap.getPixel(2,2))
        } finally { doc.close() }
    }
    @Test fun undoAvailabilityTracksHistoryAndUnfinishedShapesInToolbarAndMenu() {
        val root=activity.window.decorView; val canvas=activity.paintCanvas
        fun undoEnabled()=root.findViewWithTag<View>("undo").isEnabled
        fun redoEnabled()=root.findViewWithTag<View>("redo").isEnabled
        assertFalse(undoEnabled()); assertFalse(redoEnabled())
        click("menu_Edit"); assertFalse(ShadowPopupMenu.getLatestPopupMenu().menu.findItem(0).isEnabled)
        drag(canvas.toScreen(10f,10f),canvas.toScreen(60f,20f)); assertTrue(undoEnabled())
        click("undo"); assertFalse(undoEnabled()); assertTrue(redoEnabled())
        click("redo"); assertTrue(undoEnabled()); assertFalse(redoEnabled())
        click("undo")
        for (tool in listOf("tool_POLYGON","tool_CURVE")) {
            click(tool); drag(canvas.toScreen(10f,10f),canvas.toScreen(80f,30f))
            assertTrue(undoEnabled()); click("undo"); assertFalse(undoEnabled()); assertFalse(canvas.hasPendingEdit)
        }
        activity.document.newImage(200,100); assertFalse(undoEnabled()); assertFalse(redoEnabled())
        click("select_all"); assertFalse(undoEnabled())
        val help=root.findViewWithTag<View>("tool_help")
        help.requestRectangleOnScreen(Rect(0,0,help.width,help.height+300),true)
        render(root,"clipboard-grid.png")
    }
    private fun render(view: View,name: String) {
        shadowOf(Looper.getMainLooper()).idle()
        // Capture settled widget states, not the first frame of a radio animation.
        fun settle(v: View) {
            v.jumpDrawablesToCurrentState()
            if (v is android.view.ViewGroup) for (i in 0 until v.childCount) settle(v.getChildAt(i))
        }
        settle(view)
        val bitmap=Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888); view.draw(Canvas(bitmap))
        val file=File("build/reports/classic-preview",name); file.parentFile.mkdirs(); file.outputStream().use { bitmap.compress(Bitmap.CompressFormat.PNG,100,it) }; bitmap.recycle()
    }

}
