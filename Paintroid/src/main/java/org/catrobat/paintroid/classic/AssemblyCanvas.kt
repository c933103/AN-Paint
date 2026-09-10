/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. Attachment glyph replaced 2026-09-09 with KDE Breeze Icons (LGPL-3.0-or-later). */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import android.view.DragEvent
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.view.View
import kotlin.math.*
import org.catrobat.paintroid.R

class AssemblyCanvas(context: Context, val assembly: ImageAssembly, private val preview: (String) -> Bitmap?) : View(context) {
    private val attachGlyph = CopyleftIcon(context, R.drawable.breeze_add)
    var selectedId: String? = null; private set
    var onSelect: (String) -> Unit = {}
    var onError: (Throwable) -> Unit = {}
    var onStatus: (String) -> Unit = {}
    var zoom = 1f; private set
    private var panX = 0f; private var panY = 0f
    private var dragging: String? = null
    private var touchImage: String? = null
    private var touchDragging = false
    private var dragOffset = PointF()
    private var targets = emptyList<SnapTarget>()
    var ghost: SnapTarget? = null; private set
    private var start = PointF(); private var previous = PointF(); private var moved = false; private var pinching = false
    private val density = resources.displayMetrics.density
    private val detector = ScaleGestureDetector(context,object : ScaleGestureDetector.SimpleOnScaleGestureListener() {
        override fun onScale(d: ScaleGestureDetector): Boolean {
            val p = toImage(d.focusX,d.focusY); zoom = (zoom*d.scaleFactor).coerceIn(.000001f,32f)
            panX = d.focusX-p.x*zoom; panY = d.focusY-p.y*zoom; invalidate(); return true
        }
    })
    init { isFocusable = true; isClickable = true; contentDescription = ui(R.string.ui_image_assembly_workspace_drag_placed_images_or_drop); setLayerType(LAYER_TYPE_SOFTWARE,null) }
    fun toScreen(x: Float,y: Float) = PointF(panX+x*zoom,panY+y*zoom)
    fun toImage(x: Float,y: Float) = PointF((x-panX)/zoom,(y-panY)/zoom)
    fun select(id: String?,fitView: Boolean = true) {
        selectedId = id; targets = if (id != null && assembly.images.any { it.id == id }) assembly.targets(id) else emptyList(); ghost = null
        if (fitView) fit(); invalidate()
    }
    fun refresh() {
        if (assembly.images.none { it.id == selectedId }) selectedId = null
        if (assembly.images.none { it.id == dragging }) { dragging=null; touchImage=null; touchDragging=false }
        select(selectedId)
    }
    override fun onSizeChanged(w: Int,h: Int,oldw: Int,oldh: Int) { fit() }
    fun fit() {
        if (width <= 0 || height <= 0) return
        val rects = assembly.layout().values + targets.map { it.rect }
        val w = (rects.maxOfOrNull { it.right } ?: 800).coerceAtLeast(1)
        val h = (rects.maxOfOrNull { it.bottom } ?: 600).coerceAtLeast(1)
        val pad = 30*density
        zoom = min((width-2*pad).coerceAtLeast(1f)/w,(height-2*pad).coerceAtLeast(1f)/h).coerceAtMost(32f)
        panX = (width-w*zoom)/2; panY = (height-h*zoom)/2; invalidate()
    }
    private fun drawImage(canvas: Canvas,item: AssemblyImage,rect: Rect,alpha: Int = 255) {
        val bitmap = preview(item.id) ?: return
        val crop = item.crop
        val src = RectF(crop.left.toFloat()*bitmap.width/item.dimensions.width,crop.top.toFloat()*bitmap.height/item.dimensions.height,
            crop.right.toFloat()*bitmap.width/item.dimensions.width,crop.bottom.toFloat()*bitmap.height/item.dimensions.height)
        val matrix = Matrix().apply { setRectToRect(src,RectF(rect),Matrix.ScaleToFit.FILL) }
        canvas.save(); canvas.clipRect(rect)
        canvas.drawBitmap(bitmap,matrix,Paint(Paint.FILTER_BITMAP_FLAG).apply { this.alpha = alpha }); canvas.restore()
    }
    private fun targetPoint(target: SnapTarget) = PointF(target.rect.left.toFloat(),target.rect.top.toFloat())
    override fun onDraw(canvas: Canvas) {
        canvas.drawColor(0xffaeb7c0.toInt())
        val layout = dragging?.let { assembly.layoutWithout(it) } ?: assembly.layout()
        if (layout.isEmpty() && selectedId == null) {
            val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = 0xff233b4d.toInt(); textSize = 16*density; textAlign = Paint.Align.CENTER }
            canvas.drawText(ui(R.string.ui_add_images_then_drag_a_thumbnail_here),width/2f,height/2f,p); return
        }
        canvas.save(); canvas.translate(panX,panY); canvas.scale(zoom,zoom)
        val p = Paint(Paint.ANTI_ALIAS_FLAG)
        layout.forEach { (id,rect) ->
            p.color = Color.WHITE; p.style = Paint.Style.FILL; canvas.drawRect(rect,p)
            drawImage(canvas,assembly.image(id),rect)
            p.style = Paint.Style.STROKE; p.color = if (id == selectedId) 0xff1559a6.toInt() else 0xff7b8790.toInt(); p.strokeWidth = (if (id == selectedId) 3 else 1)*density/zoom; canvas.drawRect(rect,p)
        }
        ghost?.let { target -> selectedId?.let { id -> drawImage(canvas,assembly.image(id),target.rect,180) }
            p.style = Paint.Style.FILL; p.color = 0x3300b46b; canvas.drawRect(target.rect,p)
            p.style = Paint.Style.STROKE; p.color = 0xff007647.toInt(); p.strokeWidth = 3*density/zoom; canvas.drawRect(target.rect,p)
        }
        targets.forEach { target ->
            val point = targetPoint(target); p.style = Paint.Style.FILL; p.color = if (target == ghost) 0xff007647.toInt() else 0xff1559a6.toInt()
            canvas.drawCircle(point.x,point.y,13*density/zoom,p)
            val r = 8*density/zoom
            attachGlyph.draw(canvas, point.x-r, point.y-r, point.x+r, point.y+r, Color.WHITE)
        }
        canvas.restore()
    }
    fun beginImageDrag(id: String,fitView: Boolean = true): Boolean {
        if (!isEnabled || assembly.images.none { it.id == id }) return false
        dragging = id; select(id,fitView); onSelect(id)
        onStatus(if (targets.isEmpty()) ui(R.string.ui_no_attachment_fits_within_the_current_coordinate_range) else ui(R.string.ui_drop_at_a_highlighted_edge_right_top_aligned))
        return true
    }
    fun dragImageTo(x: Float,y: Float) {
        val p = toImage(x,y)
        ghost = targets.minByOrNull { val t = targetPoint(it); hypot(p.x-t.x,p.y-t.y) }
        invalidate()
    }
    fun dropImage(x: Float,y: Float): Boolean {
        val id = dragging ?: selectedId ?: return false; dragImageTo(x,y); val target = ghost ?: return false
        return try { dragging = null; ghost = null; assembly.place(id,target.attachment); select(null); onStatus(ui(R.string.ui_image_placed_drag_it_to_move_or_hold)); true }
        catch (error: Exception) { onError(error); false }
    }
    override fun onDragEvent(event: DragEvent): Boolean {
        if (!isEnabled) return false
        when (event.action) {
            DragEvent.ACTION_DRAG_STARTED -> {
                val id = event.localState as? String ?: event.clipData?.takeIf { it.itemCount > 0 }?.getItemAt(0)?.text?.toString() ?: return false
                return beginImageDrag(id)
            }
            DragEvent.ACTION_DRAG_LOCATION -> dragImageTo(event.x,event.y)
            DragEvent.ACTION_DROP -> return dropImage(event.x,event.y)
            DragEvent.ACTION_DRAG_EXITED -> { ghost = null; invalidate() }
            DragEvent.ACTION_DRAG_ENDED -> { dragging = null; ghost = null; invalidate() }
        }
        return true
    }
    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (!isEnabled) return false
        detector.onTouchEvent(event)
        if (event.pointerCount > 1) { pinching = true; touchDragging = false; touchImage = null; dragging = null; ghost = null; invalidate(); return true }
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                pinching = false; moved = false; touchDragging = false
                start = PointF(event.x,event.y); previous = start
                val p=toImage(event.x,event.y)
                val hit=assembly.layout().entries.lastOrNull { it.value.contains(p.x.toInt(),p.y.toInt()) }
                touchImage=hit?.key
                hit?.let { val origin=toScreen(it.value.left.toFloat(),it.value.top.toFloat()); dragOffset=PointF(event.x-origin.x,event.y-origin.y) }
                parent?.requestDisallowInterceptTouchEvent(true)
            }
            MotionEvent.ACTION_MOVE -> if (!pinching) {
                if (hypot(event.x-start.x,event.y-start.y) > 8*density) moved = true
                if (moved && touchImage != null) {
                    if (!touchDragging) touchDragging=beginImageDrag(touchImage!!,false)
                    if (touchDragging) dragImageTo(event.x-dragOffset.x,event.y-dragOffset.y)
                } else if (moved) { panX += event.x-previous.x; panY += event.y-previous.y; previous = PointF(event.x,event.y); invalidate() }
            }
            MotionEvent.ACTION_UP -> {
                if (!pinching && touchDragging) dropImage(event.x-dragOffset.x,event.y-dragOffset.y)
                else if (!pinching && !moved) {
                    val p = toImage(event.x,event.y)
                    val target = targets.minByOrNull { val t = targetPoint(it); hypot(p.x-t.x,p.y-t.y) }
                    if (target != null && (assembly.layout().isEmpty() || hypot(p.x-target.rect.left,p.y-target.rect.top)*zoom < 36*density)) dropImage(event.x,event.y)
                    else assembly.layout().entries.lastOrNull { it.value.contains(p.x.toInt(),p.y.toInt()) }?.let { select(it.key,false); onSelect(it.key) }
                }
                touchImage=null; touchDragging=false; dragging=null; ghost=null
                parent?.requestDisallowInterceptTouchEvent(false); performClick(); invalidate()
            }
            MotionEvent.ACTION_CANCEL -> { touchImage=null; touchDragging=false; dragging=null; ghost=null; parent?.requestDisallowInterceptTouchEvent(false); invalidate() }
        }
        return true
    }
    override fun performClick(): Boolean { super.performClick(); return true }
}
