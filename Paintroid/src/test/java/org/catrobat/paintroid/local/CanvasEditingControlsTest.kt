/* AN Paint interaction regressions, 2026-09-09. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.*
import android.os.Looper
import android.view.*
import android.widget.*
import org.catrobat.paintroid.classic.*
import org.junit.*
import org.junit.Assert.*
import org.junit.runner.RunWith
import org.robolectric.*
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.*
import java.io.File
import java.util.concurrent.TimeUnit
import kotlin.math.*

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CanvasEditingControlsTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private val doc get()=activity.document
    private val canvas get()=activity.paintCanvas
    private var clock=1000L
    private var downTime=1000L
    private fun <T: View> view(tag: String): T=activity.window.decorView.findViewWithTag(tag)
    private fun settle() { shadowOf(Looper.getMainLooper()).idleFor(20,TimeUnit.MILLISECONDS) }
    private fun waitIo() {
        val end=System.nanoTime()+15_000_000_000L
        do { shadowOf(Looper.getMainLooper()).idle();if (activity.busy) Thread.sleep(10) } while (activity.busy && System.nanoTime()<end)
        assertFalse(activity.busy)
    }
    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        listOf("classic-recovery.png","classic-autosave.zip","classic-autosave.zip.bak").forEach { File(context.filesDir,it).delete() }
        AutosaveStore(context.filesDir).recoveryCopies().forEach { it.delete() }
        context.getSharedPreferences("classic-ui",Context.MODE_PRIVATE).edit().clear().commit()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get()
        doc.newImage(240,240);canvas.fit();settle()
    }
    @After fun stop() { controller.pause().stop();waitIo();controller.destroy() }
    private fun click(tag: String) { EditorTestNavigation.click(activity,tag) }
    private fun event(action: Int,point: PointF) {
        val p=canvas.toScreen(point.x,point.y)
        clock+=20;if (action==MotionEvent.ACTION_DOWN) downTime=clock
        val e=MotionEvent.obtain(downTime,clock,action,p.x,p.y,0)
        assertTrue(canvas.dispatchTouchEvent(e));e.recycle()
    }
    private fun tap(x: Float,y: Float,gap: Long=500) {
        clock+=gap;event(MotionEvent.ACTION_DOWN,PointF(x,y));event(MotionEvent.ACTION_UP,PointF(x,y));settle()
    }
    private fun drag(from: PointF,to: PointF) {
        event(MotionEvent.ACTION_DOWN,from)
        event(MotionEvent.ACTION_MOVE,PointF((from.x+to.x)/2,(from.y+to.y)/2))
        event(MotionEvent.ACTION_UP,to);settle()
    }
    private fun selectBlock(rect: RectF=RectF(60f,70f,120f,100f)) {
        val c=Canvas(doc.bitmap)
        c.drawRect(rect,Paint().apply { color=Color.RED })
        c.drawRect(rect.centerX(),rect.top,rect.right,rect.bottom,Paint().apply { color=Color.BLUE })
        click("tool_SELECT");doc.select(rect);settle()
    }
    private fun grip(): PointF {
        val s=doc.selection!!;val d=activity.resources.displayMetrics.density
        return s.geometry.rotationHandle(34*d/canvas.zoom)
    }
    private fun rotateQuarter() {
        val s=doc.selection!!;val g=grip();val cx=s.rect.centerX();val cy=s.rect.centerY()
        drag(g,PointF(cx-(g.y-cy),cy+(g.x-cx)))
    }
    private fun render(name: String) {
        settle();val root=activity.window.decorView
        val image=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888);root.draw(Canvas(image))
        val path=File("build/reports/classic-preview",name);path.parentFile.mkdirs()
        path.outputStream().use { assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it)) };image.recycle()
    }

    @Test fun polygonDoubleTapClosesWithoutDuplicateVertexAndIsOneUndoStep() {
        click("tool_POLYGON");doc.shapeStyle=1
        tap(40f,40f);tap(140f,40f);tap(140f,140f)
        assertEquals(3,canvas.draftState().getJSONArray("polygon").length())
        tap(140f,140f,100)
        assertFalse(canvas.hasPendingEdit);assertEquals(Color.BLACK,doc.bitmap.getPixel(110,70))
        click("undo");assertEquals(Color.WHITE,doc.bitmap.getPixel(110,70));assertFalse(doc.canUndo)
        click("redo");assertEquals(Color.BLACK,doc.bitmap.getPixel(110,70))
    }
    @Test fun polygonSlowRepeatedTapAndDistantFastTapKeepAddingVertices() {
        click("tool_POLYGON")
        tap(40f,40f);tap(140f,40f);tap(140f,140f)
        tap(140f,140f,ViewConfiguration.getDoubleTapTimeout()+100L)
        tap(40f,140f,100)
        assertTrue(canvas.hasPendingEdit);assertEquals(5,canvas.draftState().getJSONArray("polygon").length());assertFalse(doc.canUndo)
    }
    @Test fun polygonDragReturningToLastVertexDoesNotCountAsDoubleTap() {
        click("tool_POLYGON");tap(40f,40f);tap(140f,40f);tap(140f,140f)
        clock+=50;event(MotionEvent.ACTION_DOWN,PointF(140f,140f))
        event(MotionEvent.ACTION_MOVE,PointF(180f,180f));event(MotionEvent.ACTION_UP,PointF(140f,140f))
        assertTrue(canvas.hasPendingEdit);assertFalse(doc.canUndo)
    }
    @Test fun radiusSliderControlsAbsolutePixelsAndClampsForSmallShapes() {
        click("tool_ROUND_RECT");doc.shapeStyle=1;doc.foreground=Color.RED
        val slider=view<SeekBar>("corner_radius")
        slider.progress=0;drag(PointF(30f,30f),PointF(90f,90f))
        assertEquals(Color.RED,doc.bitmap.getPixel(32,32))
        doc.newImage(240,240);slider.progress=20
        drag(PointF(30f,30f),PointF(90f,90f))
        assertEquals(20f,doc.cornerRadius,0f);assertEquals(Color.WHITE,doc.bitmap.getPixel(32,32));assertEquals(Color.RED,doc.bitmap.getPixel(60,32))
        doc.newImage(240,240);slider.progress=60
        drag(PointF(40f,40f),PointF(60f,60f))
        assertEquals(Color.WHITE,doc.bitmap.getPixel(40,40));assertEquals(Color.RED,doc.bitmap.getPixel(50,41))
    }
    @Test fun zoomButtonsStopAtActualSizeInBothDirectionsAndContinueNextPress() {
        canvas.zoomAt(.8f);click("zoom_in");assertEquals(1f,canvas.zoom,0f)
        click("zoom_in");assertEquals(1.5f,canvas.zoom,0f)
        canvas.zoomAt(1.2f);click("zoom_out");assertEquals(1f,canvas.zoom,0f)
        click("zoom_out");assertEquals(1/1.5f,canvas.zoom,0f)
        canvas.zoomAt(.2f);click("zoom_in");assertEquals(.3f,canvas.zoom,.0001f)
    }
    @Test fun sliderCentreIsExactlyActualSizeAndFitFramesTheCanvas() {
        val slider=view<SeekBar>("zoom_slider");assertTrue(slider is ZoomSeekBar)
        assertEquals(1f,canvas.zoomForSlider(500),0f)
        canvas.zoomAt(1f);assertEquals(500,slider.progress)
        assertEquals(canvas.minimumZoom(),canvas.zoomForSlider(0),.000001f)
        assertEquals(32f,canvas.zoomForSlider(1000),.0001f)
        canvas.zoomAt(10f);click("zoom_fit_view")
        val top=canvas.toScreen(0f,0f);val bottom=canvas.toScreen(240f,240f)
        val bar=20*activity.resources.displayMetrics.density
        assertTrue(top.x>=0 && top.y>=0);assertTrue(bottom.x<=canvas.width-bar && bottom.y<=canvas.height-bar)
        assertEquals(canvas.sliderForZoom(),slider.progress)
    }
    @Test fun eachCornerResizesAboutItsOppositeCornerAndKeepsSourcePixels() {
        for (corner in 0..3) {
            doc.newImage(240,240);selectBlock(RectF(70f,70f,130f,130f))
            val s=doc.selection!!;val source=s.image;val pixels=source.copy(Bitmap.Config.ARGB_8888,false)
            val points=s.geometry.corners();val anchor=points[(corner+2)%4];val from=points[corner]
            val to=PointF(anchor.x+2*(from.x-anchor.x),anchor.y+2*(from.y-anchor.y))
            drag(from,to)
            assertEquals(120f,s.rect.width(),.01f);assertEquals(120f,s.rect.height(),.01f)
            val fixed=s.geometry.corners()[(corner+2)%4]
            assertEquals(anchor.x,fixed.x,.01f);assertEquals(anchor.y,fixed.y,.01f)
            assertSame(source,s.image);assertTrue(pixels.sameAs(s.image));pixels.recycle()
        }
    }
    @Test fun selectionCanShrinkThenEnlargeWithoutRepeatedResampling() {
        selectBlock(RectF(60f,60f,140f,100f));val s=doc.selection!!;val source=s.image.copy(Bitmap.Config.ARGB_8888,false)
        drag(PointF(140f,100f),PointF(100f,80f))
        assertEquals(40f,s.rect.width(),.01f);assertEquals(20f,s.rect.height(),.01f)
        drag(PointF(100f,80f),PointF(140f,100f))
        assertEquals(RectF(60f,60f,140f,100f),s.rect);assertTrue(source.sameAs(s.image));source.recycle()
        click("apply");assertEquals(Color.RED,doc.bitmap.getPixel(70,70));assertEquals(Color.BLUE,doc.bitmap.getPixel(130,70))
    }
    @Test fun unlockingProportionsAllowsIndependentWidthAndHeight() {
        selectBlock(RectF(60f,60f,120f,100f));click("selection_lock_aspect")
        drag(PointF(120f,100f),PointF(160f,100f))
        assertEquals(100f,doc.selection!!.rect.width(),.01f);assertEquals(40f,doc.selection!!.rect.height(),.01f)
    }
    @Test fun roundHandleRotatesPixelsAndUndoRedoIncludeTheFloatingResult() {
        selectBlock();rotateQuarter()
        assertEquals(90f,doc.selection!!.rotation,.001f)
        assertTrue(view<TextView>("selection_dimensions").text.contains("90.0°"))
        click("undo");assertNull(doc.selection);assertEquals(Color.RED,doc.bitmap.getPixel(65,80));assertFalse(doc.canUndo)
        click("redo");assertEquals(Color.WHITE,doc.bitmap.getPixel(65,80))
        assertEquals(Color.RED,doc.bitmap.getPixel(90,65));assertEquals(Color.BLUE,doc.bitmap.getPixel(90,105))
    }
    @Test fun rotatedSelectionCanResizeInItsOwnAxesAndMoveFromInside() {
        selectBlock();rotateQuarter();val s=doc.selection!!
        val corners=s.geometry.corners();val anchor=corners[0];val from=corners[2]
        drag(from,PointF(anchor.x+(from.x-anchor.x)*1.5f,anchor.y+(from.y-anchor.y)*1.5f))
        assertEquals(90f,s.rect.width(),.02f);assertEquals(45f,s.rect.height(),.02f)
        assertEquals(anchor.x,s.geometry.corners()[0].x,.02f);assertEquals(anchor.y,s.geometry.corners()[0].y,.02f)
        val before=RectF(s.rect);val centre=PointF(before.centerX(),before.centerY())
        drag(centre,PointF(centre.x+20,centre.y+10))
        assertEquals(before.left+20,s.rect.left,.02f);assertEquals(before.top+10,s.rect.top,.02f);assertEquals(90f,s.rotation,.001f)
    }
    @Test fun copyAndCropUseTheRotatedSelectionDimensionsAndPixels() {
        selectBlock();rotateQuarter();assertTrue(doc.copySelection())
        val copied=doc.clipboard!!;assertEquals(30,copied.width);assertEquals(60,copied.height)
        assertEquals(Color.RED,copied.getPixel(15,10));assertEquals(Color.BLUE,copied.getPixel(15,50))
        assertTrue(doc.cropSelection());assertEquals(30,doc.bitmap.width);assertEquals(60,doc.bitmap.height)
        assertEquals(Color.BLUE,doc.bitmap.getPixel(15,50));doc.undo();assertEquals(240,doc.bitmap.width)
    }
    @Test fun cancelledCornerDragRestoresPixelsBoundsAndUndoAvailability() {
        selectBlock();val before=doc.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        event(MotionEvent.ACTION_DOWN,PointF(120f,100f));event(MotionEvent.ACTION_MOVE,PointF(160f,120f))
        assertTrue(doc.selection!!.floating)
        event(MotionEvent.ACTION_CANCEL,PointF(160f,120f))
        assertEquals(RectF(60f,70f,120f,100f),doc.selection!!.rect);assertFalse(doc.selection!!.floating)
        assertFalse(doc.canUndo);assertTrue(before.sameAs(doc.bitmap));before.recycle()
    }
    @Test fun addingSecondFingerCancelsRotationWithoutLosingTheSelection() {
        selectBlock();val before=doc.bitmap.copy(Bitmap.Config.ARGB_8888,false)
        val from=grip();event(MotionEvent.ACTION_DOWN,from);event(MotionEvent.ACTION_MOVE,PointF(160f,85f))
        val props=Array(2) { i -> MotionEvent.PointerProperties().apply { id=i;toolType=MotionEvent.TOOL_TYPE_FINGER } }
        val coords=arrayOf(200f to 200f,350f to 200f).map { (px,py) -> MotionEvent.PointerCoords().apply { x=px;y=py;pressure=1f;size=1f } }.toTypedArray()
        val e=MotionEvent.obtain(downTime,clock+20,MotionEvent.ACTION_POINTER_DOWN or (1 shl MotionEvent.ACTION_POINTER_INDEX_SHIFT),2,props,coords,0,0,1f,1f,0,0,InputDevice.SOURCE_TOUCHSCREEN,0)
        assertTrue(canvas.dispatchTouchEvent(e));e.recycle();event(MotionEvent.ACTION_UP,PointF(100f,100f))
        assertEquals(0f,doc.selection!!.rotation,0f);assertFalse(doc.selection!!.floating);assertFalse(doc.canUndo)
        assertTrue(before.sameAs(doc.bitmap));before.recycle()
    }
    @Test fun transformedLassoKeepsItsMaskAndErasesOnlyTheOriginalShape() {
        Canvas(doc.bitmap).drawColor(Color.YELLOW);click("tool_LASSO")
        val mask=Path().apply { moveTo(60f,60f);lineTo(120f,60f);lineTo(60f,120f);close() }
        doc.select(RectF(60f,60f,120f,120f),mask)
        drag(PointF(120f,120f),PointF(180f,180f));assertTrue(doc.copySelection())
        assertEquals(120,doc.clipboard!!.width);assertEquals(0,Color.alpha(doc.clipboard!!.getPixel(110,110)))
        assertEquals(Color.YELLOW,doc.bitmap.getPixel(110,110));assertEquals(Color.WHITE,doc.bitmap.getPixel(65,65))
        click("apply");assertEquals(Color.YELLOW,doc.bitmap.getPixel(80,80))
    }
    @Test fun autosaveRestoresRotationRadiusAndProportionChoice() {
        click("tool_ROUND_RECT");view<SeekBar>("corner_radius").progress=27
        selectBlock();rotateQuarter();click("selection_lock_aspect")
        val rect=RectF(doc.selection!!.rect)
        shadowOf(Looper.getMainLooper()).idleFor(2,TimeUnit.SECONDS);waitIo();assertNull(activity.lastAutosaveError)
        controller.pause().stop();waitIo();controller.destroy()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get();settle()
        assertEquals(27f,doc.cornerRadius,0f);assertEquals(90f,doc.selection!!.rotation,.001f);assertEquals(rect,doc.selection!!.rect)
        assertFalse(canvas.lockSelectionAspect);assertFalse(view<CheckBox>("selection_lock_aspect").isChecked)
        click("apply");assertEquals(Color.RED,doc.bitmap.getPixel(90,65));assertEquals(Color.BLUE,doc.bitmap.getPixel(90,105))
    }
    @Test fun portraitHandlesAndZoomControlsRender() { selectBlock(RectF(60f,80f,180f,160f));rotateQuarter();render("editing-controls-portrait.png") }
    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi") fun landscapeHandlesAndZoomControlsRender() {
        selectBlock(RectF(60f,80f,180f,160f));rotateQuarter();render("editing-controls-landscape.png")
        val fit=view<View>("zoom_fit_view");val location=IntArray(2);fit.getLocationOnScreen(location)
        assertTrue(fit.isShown);assertTrue(location[0]+fit.width<=activity.window.decorView.width)
    }
    @Test fun oversizedTransformedCopyKeepsTheExistingClipboardAndSelection() {
        val model=PaintDocument(16,16,File(activity.cacheDir,"selection-budget"),allocationGuard={ w,h ->
            if (w>32 || h>32) throw ImageSizeException("Test memory budget exceeded")
        })
        try {
            model.bitmap.eraseColor(Color.RED);model.select(RectF(0f,0f,8f,8f));assertTrue(model.copySelection())
            val clipboard=model.clipboard!!;model.startMovingSelection();model.selection!!.rect.set(0f,0f,64f,64f)
            val canvasBefore=model.bitmap.copy(Bitmap.Config.ARGB_8888,false)
            try { model.copySelection();fail("Oversized clipboard allocation must be rejected") } catch (_: ImageSizeException) { }
            assertSame(clipboard,model.clipboard);assertFalse(clipboard.isRecycled);assertTrue(canvasBefore.sameAs(model.bitmap));canvasBefore.recycle()
            assertEquals(Color.RED,model.selection!!.image.getPixel(2,2))
        } finally { model.close() }
    }
    @Test fun selectAllKeepsRotationHandleReachableAtFitAndPastedContentCanResize() {
        click("select_all");canvas.fit()
        val s=doc.selection!!;val ideal=grip();val screen=canvas.toScreen(ideal.x,ideal.y)
        val d=activity.resources.displayMetrics.density
        val actual=canvas.toImage(screen.x,max(22*d,screen.y))
        val centre=PointF(s.rect.centerX(),s.rect.centerY())
        drag(actual,PointF(centre.x-(actual.y-centre.y),centre.y+(actual.x-centre.x)))
        assertEquals(90f,s.rotation,.001f)
        doc.newImage(240,240)
        val image=Bitmap.createBitmap(60,40,Bitmap.Config.ARGB_8888).apply { eraseColor(Color.GREEN) }
        assertTrue(doc.paste(image,takeOwnership=true));doc.selection!!.rect.offset(70f,70f)
        drag(PointF(130f,110f),PointF(160f,130f))
        assertEquals(90f,doc.selection!!.rect.width(),.01f);assertEquals(60f,doc.selection!!.rect.height(),.01f)
        click("apply");assertEquals(Color.GREEN,doc.bitmap.getPixel(155,120))
    }
    @Test fun roundedRadiusControlRenders() {
        click("tool_ROUND_RECT");view<SeekBar>("corner_radius").progress=24;doc.shapeStyle=2
        drag(PointF(30f,60f),PointF(210f,180f));render("rounded-radius-portrait.png")
    }

}
