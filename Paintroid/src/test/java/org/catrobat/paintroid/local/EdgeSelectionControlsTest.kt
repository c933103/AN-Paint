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
class EdgeSelectionControlsTest {
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
    private fun click(tag: String) {
        val control=view<View>(tag)
        if (control is CompoundButton) { val checked=control.isChecked;control.performClick();assertEquals(!checked,control.isChecked) }
        else assertTrue(control.performClick())
        settle()
    }
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

    private fun opposite(edge: Int)=when(edge) { 5->7;6->8;7->5;else->6 }
    private fun stretchEdge(edge: Int,factor: Float): Pair<PointF,PointF> {
        val handles=doc.selection!!.geometry.resizeHandles()
        val anchor=handles.getValue(opposite(edge));val from=handles.getValue(edge)
        drag(from,PointF(anchor.x+factor*(from.x-anchor.x),anchor.y+factor*(from.y-anchor.y)))
        return anchor to doc.selection!!.geometry.resizeHandles().getValue(opposite(edge))
    }
    private fun assertPoint(expected: PointF,actual: PointF) {
        assertEquals(expected.x,actual.x,.03f);assertEquals(expected.y,actual.y,.03f)
    }
    private fun lasso(hole: Boolean=false) {
        doc.bitmap.eraseColor(Color.YELLOW);click("tool_LASSO")
        val path=Path().apply {
            if (hole) {
                fillType=Path.FillType.EVEN_ODD
                addOval(RectF(60f,60f,140f,140f),Path.Direction.CW)
                addRect(RectF(85f,85f,115f,115f),Path.Direction.CW)
            } else {
                moveTo(60f,60f);lineTo(140f,60f);lineTo(140f,100f)
                lineTo(100f,100f);lineTo(100f,140f);lineTo(60f,140f);close()
            }
        }
        doc.select(RectF(60f,60f,140f,140f),path);settle()
    }
    private fun bounds(path: Path)=RectF().also { path.computeBounds(it,true) }

    @Test fun allFourEdgesChangeOnlyTheirAxisWhenUnlocked() {
        for (edge in 5..8) {
            doc.newImage(240,240);selectBlock(RectF(70f,80f,150f,140f));canvas.lockSelectionAspect=false
            val source=doc.selection!!.image;val before=source.copy(Bitmap.Config.ARGB_8888,false)
            val (anchor,fixed)=stretchEdge(edge,1.5f)
            assertPoint(anchor,fixed)
            assertEquals(if(edge==6 || edge==8) 120f else 80f,doc.selection!!.rect.width(),.03f)
            assertEquals(if(edge==5 || edge==7) 90f else 60f,doc.selection!!.rect.height(),.03f)
            assertSame(source,doc.selection!!.image);assertTrue(before.sameAs(source));before.recycle()
        }
    }
    @Test fun lockedEdgesScaleBothAxesAndKeepOppositeMidpointFixed() {
        for (edge in 5..8) {
            doc.newImage(240,240);selectBlock(RectF(70f,80f,150f,140f));canvas.lockSelectionAspect=true
            val (anchor,fixed)=stretchEdge(edge,1.5f);assertPoint(anchor,fixed)
            assertEquals(120f,doc.selection!!.rect.width(),.03f);assertEquals(90f,doc.selection!!.rect.height(),.03f)
        }
    }
    @Test fun rotatedEdgeGripsResizeAlongTheSelectionAxes() {
        for (edge in 5..8) {
            doc.newImage(240,240);selectBlock(RectF(70f,80f,150f,140f));rotateQuarter();canvas.lockSelectionAspect=false
            val (anchor,fixed)=stretchEdge(edge,1.5f);assertPoint(anchor,fixed)
            assertEquals(90f,doc.selection!!.rotation,.001f)
            assertEquals(if(edge==6 || edge==8) 120f else 80f,doc.selection!!.rect.width(),.03f)
            assertEquals(if(edge==5 || edge==7) 90f else 60f,doc.selection!!.rect.height(),.03f)
        }
    }
    @Test fun concaveLassoEdgeStretchAndRotationPreserveItsMaskedPixels() {
        lasso();canvas.lockSelectionAspect=false
        val s=doc.selection!!;val source=s.image.copy(Bitmap.Config.ARGB_8888,false)
        stretchEdge(6,2f)
        assertEquals(Color.WHITE,doc.bitmap.getPixel(65,125))
        assertEquals(Color.YELLOW,doc.bitmap.getPixel(130,130))
        assertTrue(doc.copySelection());assertEquals(160,doc.clipboard!!.width);assertEquals(80,doc.clipboard!!.height)
        assertEquals(Color.YELLOW,doc.clipboard!!.getPixel(20,65));assertEquals(0,Color.alpha(doc.clipboard!!.getPixel(130,65)))
        rotateQuarter();assertTrue(doc.copySelection())
        assertEquals(80,doc.clipboard!!.width);assertEquals(160,doc.clipboard!!.height)
        assertEquals(Color.YELLOW,doc.clipboard!!.getPixel(15,20));assertEquals(0,Color.alpha(doc.clipboard!!.getPixel(15,130)))
        assertTrue(source.sameAs(s.image));source.recycle();click("apply")
        assertEquals(Color.WHITE,doc.bitmap.getPixel(65,125));assertEquals(Color.YELLOW,doc.bitmap.getPixel(130,130))
        click("undo");assertEquals(Color.YELLOW,doc.bitmap.getPixel(65,125))
        click("redo");assertEquals(Color.WHITE,doc.bitmap.getPixel(65,125))
    }
    @Test fun ovalSelectionWithHoleKeepsBothContoursAndTransparentHole() {
        lasso(true);canvas.lockSelectionAspect=false;stretchEdge(7,2f);rotateQuarter()
        val s=doc.selection!!;val measure=PathMeasure(s.transformedOutline(),false)
        var contours=1;while(measure.nextContour()) contours++
        assertEquals(2,contours)
        assertTrue(doc.copySelection());val image=doc.clipboard!!
        assertEquals(160,image.width);assertEquals(80,image.height)
        assertEquals(0,Color.alpha(image.getPixel(80,40)))
        assertEquals(Color.YELLOW,image.getPixel(80,10))
        assertEquals(Color.YELLOW,doc.bitmap.getPixel(100,100))
    }
    @Test fun freeFormOutlineIsClippedToCanvasAndFollowsTheSameTransform() {
        click("tool_LASSO")
        val path=Path().apply { addRect(RectF(-20f,-10f,100f,80f),Path.Direction.CW) }
        doc.select(RectF(-20f,-10f,100f,80f),path)
        val s=doc.selection!!;assertEquals(RectF(0f,0f,100f,80f),bounds(s.outline!!))
        doc.startMovingSelection();s.rect.set(40f,60f,240f,100f);s.rotation=90f
        val transformed=bounds(s.transformedOutline()!!);val expected=s.geometry.bounds()
        assertEquals(expected.left,transformed.left,.03f);assertEquals(expected.top,transformed.top,.03f)
        assertEquals(expected.right,transformed.right,.03f);assertEquals(expected.bottom,transformed.bottom,.03f)
    }
    @Test fun cancellingAnEdgeDragRestoresTheIrregularSelectionAndCanvas() {
        lasso();val before=doc.bitmap.copy(Bitmap.Config.ARGB_8888,false);val outline=bounds(doc.selection!!.transformedOutline()!!)
        event(MotionEvent.ACTION_DOWN,PointF(140f,100f));event(MotionEvent.ACTION_MOVE,PointF(180f,100f))
        assertTrue(doc.selection!!.floating);event(MotionEvent.ACTION_CANCEL,PointF(180f,100f))
        assertFalse(doc.selection!!.floating);assertFalse(doc.canUndo);assertTrue(before.sameAs(doc.bitmap));before.recycle()
        assertEquals(outline,bounds(doc.selection!!.transformedOutline()!!))
    }
    @Test fun centreOfSmallSelectionStillMovesInsteadOfResizing() {
        selectBlock(RectF(100f,100f,104f,104f));val from=PointF(102f,102f)
        drag(from,PointF(122f,112f))
        val rect=doc.selection!!.rect
        assertEquals(120f,rect.left,.001f);assertEquals(110f,rect.top,.001f)
        assertEquals(4f,rect.width(),.001f);assertEquals(4f,rect.height(),.001f)
    }
    @Test fun autosaveRestoresIrregularOutlineAndExactFloatingPixels() {
        lasso(true);canvas.lockSelectionAspect=false;stretchEdge(6,1.5f);rotateQuarter()
        val s=doc.selection!!;val source=s.image.copy(Bitmap.Config.ARGB_8888,false)
        val box=RectF(s.rect);val outline=bounds(s.transformedOutline()!!)
        shadowOf(Looper.getMainLooper()).idleFor(2,TimeUnit.SECONDS);waitIo();assertNull(activity.lastAutosaveError)
        controller.pause().stop();waitIo();controller.destroy()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get();settle()
        val recovered=doc.selection!!;assertEquals(box,recovered.rect);assertEquals(90f,recovered.rotation,.001f)
        assertTrue(source.sameAs(recovered.image));source.recycle()
        val recoveredBounds=bounds(recovered.transformedOutline()!!)
        assertEquals(outline.left,recoveredBounds.left,.6f);assertEquals(outline.top,recoveredBounds.top,.6f)
        assertEquals(outline.right,recoveredBounds.right,.6f);assertEquals(outline.bottom,recoveredBounds.bottom,.6f)
        val measure=PathMeasure(recovered.outline,false);var contours=1;while(measure.nextContour()) contours++
        assertEquals(2,contours);assertTrue(doc.copySelection())
        assertEquals(0,Color.alpha(doc.clipboard!!.getPixel(doc.clipboard!!.width/2,doc.clipboard!!.height/2)))
    }
    @Test fun freeFormHandlesRenderInPortrait() {
        lasso();stretchEdge(6,1.4f);render("edge-handles-portrait.png")
    }
    @Test @Config(qualifiers="w900dp-h412dp-land-xhdpi") fun freeFormHandlesRenderInLandscape() {
        lasso();stretchEdge(6,1.4f);render("edge-handles-landscape.png")
    }
}
