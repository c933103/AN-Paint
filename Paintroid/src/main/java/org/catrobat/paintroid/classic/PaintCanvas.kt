/* Pocket Paint Local additions, 2026-09-07. GNU AGPL-3.0-or-later; no warranty. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.content.Context
import android.graphics.*
import android.view.MotionEvent
import android.view.View
import android.view.ViewConfiguration
import kotlin.math.*
import kotlin.random.Random
import org.json.JSONArray
import org.json.JSONObject

class PaintCanvas(context: Context, val document: PaintDocument) : View(context) {
    var tool = PaintTool.ZOOM; private set
    var pencilSize: Float
        get() = document.pencilWidth
        set(value) { document.pencilWidth = value }
    var zoom = 1f; private set
    var panX = 0f; private set
    var panY = 0f; private set
    var grid = false
        set(value) {
            if(field==value) return
            val centre=if(viewportWidth>0 && viewportHeight>0) toImage(viewportInset+viewportWidth/2,viewportInset+viewportHeight/2) else null
            pauseGesture();field=value
            updateViewport(width,height)
            if(fitted && fitMode) fit() else {
                centre?.let {panX=rulerInset+viewportWidth/2-it.x*zoom;panY=rulerInset+viewportHeight/2-it.y*zoom}
                clampPan();invalidate();onStatus()
            }
        }
    var trim: CropOverlay? = null; private set
    var onStatus: () -> Unit = {}
    var onPick: (Int) -> Unit = {}
    var onText: (Float, Float) -> Unit = { _, _ -> }
    var onFill: (Int, Int) -> Unit = { x, y -> document.fill(x, y) }
    var onError: (Throwable) -> Unit = {}
    private var start = PointF()
    private var end = PointF()
    private var previous = PointF()
    private var screenStart = PointF()
    private var screenPrevious = PointF()
    private var down = false
    private var movingSelection = false
    private var panning = false
    private var multiTouch = false
    private var initialSelectionRect: RectF? = null
    private var initialSelectionFloating = false
    private var initialSelectionRotation = 0f
    private var selectionHandle = -1 // -2: move, 0..3: corners, 4: rotate, 5..8: edge midpoints
    private var selectionTouchStart = PointF()
    private var selectionChanged = false
    var lockSelectionAspect = true
    private val touchSlop = ViewConfiguration.get(context).scaledTouchSlop.toFloat()
    private val doubleTapSlop = min(ViewConfiguration.get(context).scaledDoubleTapSlop.toFloat(),24*resources.displayMetrics.density)
    private var lastPolygonTap: PointF? = null
    private var lastPolygonTapTime = -1L
    private var polygonDoubleTap = false
    private var polygonTouchMoved = false
    private var initialCurve: Pair<PointF,PointF>? = null
    val hasActiveGesture get() = down || multiTouch
    private var pinchFocus = PointF()
    private var pinchSpan = 0f
    private var scrollAxis = 0
    private var trace = Path()
    private val polygon = mutableListOf<PointF>()
    var closePolygon = true
    private var curveStage = 0
    val hasPendingEdit get() = polygon.isNotEmpty() || curveStage > 0 || trim?.changed == true
    private var control1 = PointF()
    private var control2 = PointF()
    private val bar = 20f * resources.displayMetrics.density
    private var fitted = false
    private var fitMode = true
    private var restoredCentre: PointF? = null
    private var viewportWidth = 0f
    private var viewportHeight = 0f
    private var viewportInset = 0f
    internal val rulerInset get() = if(grid) 24f*resources.displayMetrics.density else 0f
    private val contentWidth get() = (width-bar-rulerInset).coerceAtLeast(1f)
    private val contentHeight get() = (height-bar-rulerInset).coerceAtLeast(1f)
    private var rulerTouch = false
    private var scrollGrab = 0f
    var cursorMode = false; private set
    var cursorDrawing = false; private set
    private var cursor = PointF()
    private val cursorOverlay = PaintroidCursorOverlay()
    private val bitmapDisplayPaint = Paint(0)
    private var cursorInitial = PointF()
    var cursorMagnifier = true
    var magnifiedPreview = false
    var previewMagnification = 2f
    private var previewPoint: PointF? = null
    private var previewTouch = PointF()
    private var smoothedPrevious = PointF()

    fun setCursorMode(enabled: Boolean) {
        pauseGesture(); cursorMode=enabled; cursorDrawing=enabled
        if(enabled && document.brushTip==2) document.brushTip=0
        cursor=toImage(rulerInset+contentWidth/2,rulerInset+contentHeight/2).also { clampCursor(it) }
        if (enabled && tool !in listOf(PaintTool.BRUSH,PaintTool.PENCIL,PaintTool.WATERCOLOR,PaintTool.ERASER)) selectTool(PaintTool.BRUSH)
        invalidate();onStatus()
    }
    fun setCursorDrawing(enabled: Boolean) {
        val drawing=cursorMode && enabled
        if(cursorDrawing==drawing) return
        pauseGesture();cursorDrawing=drawing;invalidate();onStatus()
    }
    private fun clampCursor(p: PointF) {
        p.x=p.x.coerceIn(0f,document.bitmap.width-1f);p.y=p.y.coerceIn(0f,document.bitmap.height-1f)
    }
    private fun supportsCursor() = cursorMode && tool in listOf(PaintTool.BRUSH,PaintTool.PENCIL,PaintTool.WATERCOLOR,PaintTool.ERASER)

    private var renderedSelection: Bitmap? = null
    private var renderedSource: Bitmap? = null
    private var renderedBackground = 0
    private val sprayTick = object : Runnable {
        override fun run() {
            if (down && tool == PaintTool.SPRAY && !multiTouch) {
                spray(previous); invalidate(); postDelayed(this, 40)
            }
        }
    }

    init {
        contentDescription = ui(R.string.ui_drawing_canvas_pinch_and_move_two_fingers_to)
        isFocusable = true
        setLayerType(LAYER_TYPE_SOFTWARE, null)
    }

    fun selectTool(next: PaintTool) {
        applyPending()
        if (next !in listOf(PaintTool.SELECT, PaintTool.LASSO)) document.finishSelection()
        tool = next; invalidate(); onStatus()
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        if (w <= bar + 24 || h <= bar + 24) return
        val centre = restoredCentre ?: if (viewportWidth > 0 && viewportHeight > 0)
            toImage(viewportInset+viewportWidth / 2, viewportInset+viewportHeight / 2) else null
        updateViewport(w,h);restoredCentre = null
        if (!fitted || fitMode) fit() else {
            centre?.let { panX = rulerInset+viewportWidth / 2 - it.x * zoom; panY = rulerInset+viewportHeight / 2 - it.y * zoom }
            clampPan(); invalidate(); onStatus()
        }
    }

    private fun updateViewport(w: Int,h: Int) {
        viewportInset=rulerInset
        viewportWidth=(w-bar-rulerInset).coerceAtLeast(0f);viewportHeight=(h-bar-rulerInset).coerceAtLeast(0f)
    }

    private fun viewportBounds() = RectF(0f,0f,document.bitmap.width.toFloat(),document.bitmap.height.toFloat()).apply {
        trim?.let { union(RectF(it.rect)) }
    }

    fun fit() {
        resetPolygonTap()
        if (width <= bar + 24 || height <= bar + 24) return
        val bounds = viewportBounds()
        // Leave touch space around the handles for dragging outwards.
        val padding = if (trim == null) 12f else max(36*resources.displayMetrics.density,min(contentWidth,contentHeight)*.12f)
        zoom = min((contentWidth-2*padding).coerceAtLeast(1f)/bounds.width(),(contentHeight-2*padding).coerceAtLeast(1f)/bounds.height()).coerceAtMost(32f)
        panX = rulerInset+(contentWidth-bounds.width()*zoom)/2-bounds.left*zoom
        panY = rulerInset+(contentHeight-bounds.height()*zoom)/2-bounds.top*zoom
        fitted = true; fitMode = true; invalidate(); onStatus()
    }

    fun zoomAt(value: Float, x: Float = rulerInset+contentWidth / 2, y: Float = rulerInset+contentHeight / 2) {
        if (!value.isFinite() || value <= 0f) return
        resetPolygonTap()
        val point = toImage(x, y)
        fitMode = false
        zoom = value.coerceIn(minimumZoom(), 32f)
        panX = x - point.x * zoom; panY = y - point.y * zoom
        clampPan(); invalidate(); onStatus()
    }

    fun zoomStep(factor: Float) {
        val target = zoom*factor
        zoomAt(if (zoom < 1f && target >= 1f || zoom > 1f && target <= 1f) 1f else target)
    }
    fun minimumZoom(): Float = viewportBounds().let { bounds -> (min(contentWidth/bounds.width(),
        contentHeight/bounds.height())/8).coerceIn(.000000001f,.125f) }
    fun zoomForSlider(progress: Int): Float {
        val value = progress.coerceIn(0,1000)
        return if (value <= 500) exp(ln(minimumZoom().toDouble())*(1-value/500.0)).toFloat()
            else exp(ln(32.0)*(value-500)/500.0).toFloat()
    }
    fun sliderForZoom(): Int = (if (zoom <= 1f) 500*(1-ln(zoom.toDouble())/ln(minimumZoom().toDouble()))
        else 500+500*ln(zoom.toDouble())/ln(32.0)).roundToInt().coerceIn(0,1000)
    fun zoomLabel(): String = if (zoom >= .1f) "${(zoom * 100).roundToInt()}%" else String.format(java.util.Locale.ROOT, "%.2f%%", zoom * 100)
    fun zoomStatusLabel(): String = zoomLabel()+if(cursorMode) " · "+ui(R.string.ui_cursor_position26,
        floor(cursor.x).toInt().coerceIn(0,document.bitmap.width-1),floor(cursor.y).toInt().coerceIn(0,document.bitmap.height-1)) else ""

    fun toImage(x: Float, y: Float) = PointF((x - panX) / zoom, (y - panY) / zoom)
    fun toScreen(x: Float, y: Float) = PointF(panX + x * zoom, panY + y * zoom)

    private fun axis(horizontal: Boolean): ViewportAxis {
        val bounds = viewportBounds()
        val extent = if(horizontal) contentWidth else contentHeight
        val padding = min(24 * resources.displayMetrics.density, extent / 5)
        return ViewportAxis(extent, (if (horizontal) bounds.left else bounds.top) * zoom,
            (if (horizontal) bounds.right else bounds.bottom) * zoom, padding)
    }
    private fun clampPan() {
        if (width <= bar || height <= bar) return
        panX = rulerInset+axis(true).clamp(panX-rulerInset); panY = rulerInset+axis(false).clamp(panY-rulerInset)
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        canvas.drawColor(EditorColours.surfaceDim)
        canvas.save()
        canvas.clipRect(rulerInset, rulerInset, width - bar, height - bar)
        canvas.translate(panX, panY); canvas.scale(zoom, zoom)
        val bitmap = document.bitmap
        trim?.drawExpansion(canvas,document.background)
        val p = Paint().apply { color = Color.WHITE }
        canvas.drawRect(0f, 0f, bitmap.width.toFloat(), bitmap.height.toFloat(), p)
        canvas.drawBitmap(bitmap, 0f, 0f, bitmapDisplayPaint)
        document.selection?.let { s ->
            if (s.floating) {
                if (renderedSource !== s.image || renderedBackground != document.background) {
                    if (renderedSelection !== renderedSource) renderedSelection?.recycle()
                    renderedSelection = document.selectionImage()
                    renderedSource = s.image; renderedBackground = document.background
                }
                renderedSelection?.let { s.draw(canvas,it,bitmapDisplayPaint) }
            }
            p.color = EditorColours.primary; p.style = Paint.Style.STROKE; p.strokeWidth = 1.5f / zoom
            p.pathEffect = DashPathEffect(floatArrayOf(5f / zoom, 4f / zoom), 0f)
            s.transformedOutline()?.let { canvas.drawPath(it,p);p.pathEffect=null;p.strokeWidth=1f/zoom }
            val corners=s.geometry.corners()
            val outline=Path().apply { moveTo(corners[0].x,corners[0].y);corners.drop(1).forEach { lineTo(it.x,it.y) };close() }
            canvas.drawPath(outline,p);p.pathEffect=null
            drawSelectionHandles(canvas,s)
        }
        if (down && !multiTouch && !panning && !movingSelection && scrollAxis == 0) {
            when (tool) {
                PaintTool.SELECT, PaintTool.LASSO -> {
                    p.color = EditorColours.primary; p.style = Paint.Style.STROKE; p.strokeWidth = 1.5f / zoom
                    p.pathEffect = DashPathEffect(floatArrayOf(5f / zoom, 4f / zoom), 0f)
                    if (tool == PaintTool.SELECT) canvas.drawRect(bounds(), p) else canvas.drawPath(trace, p)
                }
                PaintTool.LINE, PaintTool.RECTANGLE, PaintTool.ELLIPSE, PaintTool.ROUND_RECT, PaintTool.HEART, PaintTool.STAR, PaintTool.ARROW -> document.drawShape(canvas, tool, shapePath())
                else -> Unit
            }
        }
        if (polygon.isNotEmpty()) document.drawShape(canvas, if(closePolygon) PaintTool.POLYGON else PaintTool.LINE, polygonPath(false))
        if (curveStage > 0 || down && tool == PaintTool.CURVE) document.drawShape(canvas, PaintTool.CURVE, curvePath())
        if (grid && zoom >= 8) {
            val line = Paint().apply { color = 0x55808080; strokeWidth = 1f / zoom }
            val l = max(0, ((rulerInset-panX) / zoom).toInt()); val t = max(0, ((rulerInset-panY) / zoom).toInt())
            val r = min(bitmap.width, ((width - bar - panX) / zoom).toInt() + 1)
            val b = min(bitmap.height, ((height - bar - panY) / zoom).toInt() + 1)
            for (x in l..r) canvas.drawLine(x.toFloat(), t.toFloat(), x.toFloat(), b.toFloat(), line)
            for (y in t..b) canvas.drawLine(l.toFloat(), y.toFloat(), r.toFloat(), y.toFloat(), line)
        }
        trim?.draw(canvas,zoom,resources.displayMetrics.density)
        canvas.restore()
        drawScrollbars(canvas)
        canvas.save();canvas.clipRect(rulerInset,rulerInset,width-bar,height-bar)
        if (supportsCursor()) {
            canvas.save();canvas.translate(panX,panY);canvas.scale(zoom,zoom)
            cursorOverlay.draw(canvas,cursor,document.paint(tool),zoom,resources.displayMetrics.density,cursorDrawing)
            canvas.restore()
        }
        if ((if(supportsCursor()) cursorMagnifier else magnifiedPreview) && down && !multiTouch && !panning && scrollAxis==0)
            previewPoint?.let { drawMagnifiedPreview(canvas,it) }
        canvas.restore()
        if(grid) drawRulers(canvas)
    }

    private fun drawRulers(canvas: Canvas) {
        val d=resources.displayMetrics.density
        val p=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=EditorColours.surfaceContainerHighest}
        canvas.drawRect(0f,0f,width-bar,rulerInset,p)
        canvas.drawRect(0f,0f,rulerInset,height-bar,p)
        p.color=EditorColours.onSurface;p.textSize=10*d;p.strokeWidth=d
        fun axisLabels(horizontal: Boolean) {
            val size=if(horizontal) document.bitmap.width else document.bitmap.height
            val origin=if(horizontal) panX else panY
            val limit=if(horizontal) width-bar else height-bar
            val ticks=PixelRuler.ticks(origin,zoom,rulerInset,limit,size,max(48*d,p.measureText(size.toString())+12*d))
            canvas.save()
            if(horizontal) canvas.clipRect(rulerInset,0f,limit,rulerInset) else canvas.clipRect(0f,rulerInset,rulerInset,limit)
            ticks.forEach {tick ->
                val length=if(tick.major) 8*d else 4*d
                if(horizontal) {
                    canvas.drawLine(tick.position,rulerInset-length,tick.position,rulerInset,p)
                    if(tick.major) canvas.drawText(tick.pixel.toString(),tick.position+3*d,rulerInset-10*d,p)
                } else {
                    canvas.drawLine(rulerInset-length,tick.position,rulerInset,tick.position,p)
                    if(tick.major) {
                        canvas.save();canvas.translate(rulerInset-10*d,tick.position-3*d);canvas.rotate(-90f)
                        canvas.drawText(tick.pixel.toString(),0f,0f,p);canvas.restore()
                    }
                }
            }
            canvas.restore()
        }
        axisLabels(true);axisLabels(false)
        p.color=EditorColours.outline
        canvas.drawLine(rulerInset,0f,rulerInset,height-bar,p);canvas.drawLine(0f,rulerInset,width-bar,rulerInset,p)
        p.color=EditorColours.onSurface;p.textAlign=Paint.Align.CENTER
        canvas.drawText("px",rulerInset/2,rulerInset/2-(p.ascent()+p.descent())/2,p)
    }

    private fun drawMagnifiedPreview(canvas: Canvas, point: PointF) {
        val d=resources.displayMetrics.density
        val size=min(120*d,min(contentWidth,contentHeight)*.45f)
        if (size<40*d) return
        // Paintroid's zoom window samples the cursor position, independently of
        // the finger, and moves to the opposite corner when the finger covers it.
        val left=if (previewTouch.x<width/2 && previewTouch.y<height/2) width-bar-size-8*d else rulerInset+8*d
        val r=RectF(left,rulerInset+8*d,left+size,rulerInset+8*d+size)
        val p=Paint(Paint.ANTI_ALIAS_FLAG).apply { color=EditorColours.primary;strokeWidth=2*d;style=Paint.Style.STROKE }
        canvas.save();canvas.clipPath(Path().apply {addOval(r,Path.Direction.CW)});canvas.drawColor(EditorColours.surfaceDim)
        canvas.translate(r.centerX(),r.centerY());val factor=max(zoom,1f)*previewMagnification.coerceIn(1f,4f)
        canvas.scale(factor,factor);canvas.translate(-point.x,-point.y)
        canvas.drawRect(0f,0f,document.bitmap.width.toFloat(),document.bitmap.height.toFloat(),Paint().apply {color=Color.WHITE})
        canvas.drawBitmap(document.bitmap,0f,0f,bitmapDisplayPaint)
        document.selection?.takeIf { it.floating }?.let { it.draw(canvas,it.image,bitmapDisplayPaint) }
        if(supportsCursor()) cursorOverlay.draw(canvas,point,document.paint(tool),factor,d,cursorDrawing)
        canvas.restore();canvas.drawOval(r,p)
    }

    private fun drawScrollbars(c: Canvas) {
        val w = (width - bar).coerceAtLeast(1f); val h = (height - bar).coerceAtLeast(1f)
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = EditorColours.surfaceContainerHighest }
        c.drawRect(0f, h, width.toFloat(), height.toFloat(), p)
        c.drawRect(w, 0f, width.toFloat(), height.toFloat(), p)
        val horizontal = axis(true); val vertical = axis(false)
        val bw = horizontal.thumbSize(bar); val bh = vertical.thumbSize(bar)
        val left = rulerInset+horizontal.thumbStart(panX-rulerInset, bw); val top = rulerInset+vertical.thumbStart(panY-rulerInset, bh)
        p.color = if (horizontal.range > 0) EditorColours.outline else EditorColours.outlineVariant
        c.drawRoundRect(RectF(left + 2, h + 4, left + bw - 2, height - 4f), 3f, 3f, p)
        p.color = if (vertical.range > 0) EditorColours.outline else EditorColours.outlineVariant
        c.drawRoundRect(RectF(w + 4, top + 2, width - 4f, top + bh - 2), 3f, 3f, p)
    }

    private fun beginScrollbar(x: Float, y: Float) {
        if (scrollAxis == 0) return
        val horizontal = scrollAxis == 1
        val a = axis(horizontal); val thumb = a.thumbSize(bar)
        val start = rulerInset+a.thumbStart((if (horizontal) panX else panY)-rulerInset, thumb)
        val point = if (horizontal) x else y
        scrollGrab = if (point in start..start + thumb) point - start else thumb / 2
        dragScrollbar(x, y)
    }
    private fun dragScrollbar(x: Float, y: Float) {
        fitMode = false
        val a = axis(scrollAxis == 1)
        val pan = rulerInset+a.panForThumb((if (scrollAxis == 1) x else y) - rulerInset - scrollGrab, a.thumbSize(bar))
        if (scrollAxis == 1) panX = pan else if (scrollAxis == 2) panY = pan
        clampPan(); invalidate(); onStatus()
    }

    private fun bounds() = RectF(min(start.x, end.x), min(start.y, end.y), max(start.x, end.x), max(start.y, end.y))
    private fun shapePath() = Path().apply {
        val r = bounds()
        when (tool) {
            PaintTool.RECTANGLE -> addRect(r, Path.Direction.CW)
            PaintTool.ROUND_RECT -> { val radius=document.cornerRadius.coerceIn(0f,min(r.width(),r.height())/2);addRoundRect(r,radius,radius,Path.Direction.CW) }
            PaintTool.ELLIPSE -> addOval(r, Path.Direction.CW)
            PaintTool.HEART -> addPath(ShapePaths.heart(r))
            PaintTool.STAR -> addPath(ShapePaths.star(r))
            PaintTool.ARROW -> addPath(ShapePaths.arrow(start,end,document.strokeWidth))
            else -> { moveTo(start.x, start.y); lineTo(end.x, end.y) }
        }
    }
    private fun polygonPath(close: Boolean) = Path().apply {
        polygon.forEachIndexed { i, point -> if (i == 0) moveTo(point.x, point.y) else lineTo(point.x, point.y) }
        if (close) close()
    }
    private fun curvePath() = Path().apply {
        moveTo(start.x, start.y)
        if (curveStage == 0) lineTo(end.x, end.y)
        else cubicTo(control1.x, control1.y, control2.x, control2.y, end.x, end.y)
    }

    fun beginTrim() {
        applyPending(); trim = CropOverlay(ImageDimensions(document.bitmap.width,document.bitmap.height),allowOutside = true); fit(); invalidate(); onStatus()
    }
    fun applyTrim() {
        val crop = trim ?: return
        document.changeCanvasBounds(crop.rect); trim = null; fit(); invalidate(); onStatus()
    }
    fun cancelTrim() { trim = null; fit(); invalidate(); onStatus() }

    fun pauseGesture() {
        document.finishGesture(); down=false;multiTouch=false;movingSelection=false;selectionHandle=-1;removeCallbacks(sprayTick)
    }

    fun applyPending() {
        if (trim != null) applyTrim()
        if (polygon.size >= 2) document.commitShape(if(closePolygon) PaintTool.POLYGON else PaintTool.LINE, polygonPath(closePolygon))
        polygon.clear();resetPolygonTap()
        if (curveStage > 0) document.commitShape(PaintTool.CURVE, curvePath())
        curveStage = 0
        document.finishSelection(); invalidate(); onStatus()
    }
    fun cancelPending(): Boolean {
        val had = hasPendingEdit
        val resizing = trim != null
        trim = null
        polygon.clear();resetPolygonTap(); curveStage = 0; down = false
        if (resizing) fit()
        invalidate(); onStatus(); return had
    }

    fun draftState(): JSONObject = JSONObject().apply {
        put("pencil_size",pencilSize.toDouble())
        put("close_polygon",closePolygon)
        put("cursor_mode",cursorMode);put("cursor_drawing",cursorDrawing);put("cursor_x",cursor.x.toDouble());put("cursor_y",cursor.y.toDouble());put("cursor_magnifier",cursorMagnifier);put("magnified_preview",magnifiedPreview);put("preview_magnification",previewMagnification.toDouble())
        put("viewport_width",viewportWidth.toDouble());put("viewport_height",viewportHeight.toDouble());put("fit_mode",fitMode)
        put("centre_x",toImage(viewportInset+viewportWidth/2,viewportInset+viewportHeight/2).x.toDouble());put("centre_y",toImage(viewportInset+viewportWidth/2,viewportInset+viewportHeight/2).y.toDouble())
        put("tool",tool.name); put("zoom",zoom.toDouble()); put("pan_x",panX.toDouble()); put("pan_y",panY.toDouble()); put("grid",grid);put("selection_lock_aspect",lockSelectionAspect)
        put("polygon",JSONArray().apply { polygon.forEach { put(JSONArray(listOf(it.x,it.y))) } })
        put("curve_stage",curveStage)
        put("curve_points",JSONArray(listOf(start.x,start.y,end.x,end.y,control1.x,control1.y,control2.x,control2.y)))
        trim?.rect?.let { put("bounds",JSONArray(listOf(it.left,it.top,it.right,it.bottom))) }
    }
    fun restoreDraft(state: JSONObject) {
        pencilSize=state.optDouble("pencil_size",1.0).toFloat()
        closePolygon=state.optBoolean("close_polygon",true)
        tool=PaintTool.values().firstOrNull { it.name==state.optString("tool") } ?: PaintTool.ZOOM
        cursorMode=state.optBoolean("cursor_mode");cursorDrawing=cursorMode && state.optBoolean("cursor_drawing",true);cursor=PointF(state.optDouble("cursor_x",0.0).toFloat(),state.optDouble("cursor_y",0.0).toFloat());clampCursor(cursor)
        magnifiedPreview=state.optBoolean("magnified_preview");previewMagnification=state.optDouble("preview_magnification",2.0).toFloat().coerceIn(1f,4f)
        cursorMagnifier=state.optBoolean("cursor_magnifier",true)
        grid=state.optBoolean("grid");lockSelectionAspect=state.optBoolean("selection_lock_aspect",true); polygon.clear();resetPolygonTap()
        state.optJSONArray("polygon")?.let { points -> for (i in 0 until points.length()) {
            val p=points.getJSONArray(i); polygon.add(PointF(p.getDouble(0).toFloat(),p.getDouble(1).toFloat()))
        } }
        curveStage=state.optInt("curve_stage").coerceIn(0,2)
        state.optJSONArray("curve_points")?.let { a ->
            fun point(i: Int)=PointF(a.getDouble(i).toFloat(),a.getDouble(i+1).toFloat())
            start=point(0);end=point(2);control1=point(4);control2=point(6)
        }
        state.optJSONArray("bounds")?.let { a ->
            trim=CropOverlay(ImageDimensions(document.bitmap.width,document.bitmap.height),allowOutside=true).apply {
                set(Rect(a.getInt(0),a.getInt(1),a.getInt(2),a.getInt(3)))
            }
        }
        zoom=state.optDouble("zoom",1.0).toFloat().takeIf {it.isFinite()}?.coerceIn(.000001f,32f) ?: 1f
        panX=state.optDouble("pan_x",0.0).toFloat();panY=state.optDouble("pan_y",0.0).toFloat();fitted=true
        // Old drafts stored absolute screen offsets without the old viewport size.
        // Fit those once; new drafts preserve their image-space centre across sizes.
        fitMode=state.optBoolean("fit_mode",true)
        if(state.has("centre_x") && state.has("centre_y")) {
            val x=state.optDouble("centre_x").toFloat();val y=state.optDouble("centre_y").toFloat()
            if(x.isFinite() && y.isFinite()) restoredCentre=PointF(x,y) else fitMode=true
        } else fitMode=true
        invalidate();onStatus()
    }

    private fun stroke(from: PointF, to: PointF, finishing: Boolean = false) {
        val canvas = Canvas(document.bitmap)
        val paint = document.paint(tool)
        if (document.brushTip == 2 && tool == PaintTool.BRUSH) {
            val count = max(1, hypot(to.x - from.x, to.y - from.y).toInt())
            paint.strokeWidth = max(1f, document.strokeWidth / 4)
            for (i in 0..count) {
                val x = from.x + (to.x - from.x) * i / count
                val y = from.y + (to.y - from.y) * i / count
                canvas.drawLine(x - document.strokeWidth / 2, y + document.strokeWidth / 2, x + document.strokeWidth / 2, y - document.strokeWidth / 2, paint)
            }
        } else if (document.strokeSmoothing && tool != PaintTool.PENCIL && !finishing && from != to) {
            val mid=PointF((from.x+to.x)/2,(from.y+to.y)/2)
            canvas.drawPath(Path().apply { moveTo(smoothedPrevious.x,smoothedPrevious.y);quadTo(from.x,from.y,mid.x,mid.y) },paint)
            smoothedPrevious=mid
        } else if (from == to) canvas.drawPoint(to.x, to.y, paint)
        else canvas.drawLine(from.x, from.y, to.x, to.y, paint)
    }

    private fun spray(point: PointF) {
        val canvas = Canvas(document.bitmap)
        val p = Paint().apply { color = document.foreground; strokeWidth = 1f }
        val radius = document.sprayRadius.coerceIn(1f,100f)
        repeat(max(8, radius.toInt())) {
            val angle = Random.nextFloat() * 2 * PI
            val r = sqrt(Random.nextFloat()) * radius
            canvas.drawPoint(point.x + (cos(angle) * r).toFloat(), point.y + (sin(angle) * r).toFloat(), p)
        }
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        return try { handleTouch(event) }
        catch (error: ImageSizeException) { abortTouch(error); true }
        catch (error: OutOfMemoryError) { abortTouch(error); true }
        catch (error: java.io.IOException) { abortTouch(error); true }
    }

    private fun abortTouch(error: Throwable) {
        try { cancelTouchEdit() } catch (_: Throwable) { }
        down = false; movingSelection = false; removeCallbacks(sprayTick)
        onError(error); invalidate()
    }

    private fun cancelTouchEdit() {
        document.cancelGesture()
        if (movingSelection) initialSelectionRect?.let { rect -> document.selection?.let { it.rect.set(rect);it.rotation=initialSelectionRotation;it.floating=initialSelectionFloating } }
        initialCurve?.let { control1=it.first;control2=it.second }
        trim?.end(true)
        movingSelection=false;selectionHandle=-1;resetPolygonTap()
    }

    private fun resetPolygonTap() { lastPolygonTap=null;lastPolygonTapTime=-1L;polygonDoubleTap=false }

    private fun rotationHandle(s: PaintDocument.Selection): PointF {
        val d=resources.displayMetrics.density
        val ideal=s.geometry.rotationHandle(34*d/zoom)
        val screen=toScreen(ideal.x,ideal.y)
        // Keep the rotation grip reachable even when selecting the whole canvas at Fit.
        screen.x=screen.x.coerceIn(min(22*d,(width-bar)/2),max(22*d,width-bar-22*d))
        screen.y=screen.y.coerceIn(min(22*d,(height-bar)/2),max(22*d,height-bar-22*d))
        return toImage(screen.x,screen.y)
    }
    private fun drawSelectionHandles(canvas: Canvas,s: PaintDocument.Selection) {
        val d=resources.displayMetrics.density/zoom
        val edge=Paint(Paint.ANTI_ALIAS_FLAG).apply { color=EditorColours.primary;style=Paint.Style.STROKE;strokeWidth=1.5f*d }
        val fill=Paint(Paint.ANTI_ALIAS_FLAG).apply { color=Color.WHITE }
        val grip=rotationHandle(s);val top=s.geometry.point(s.rect.centerX(),s.rect.top)
        canvas.drawLine(top.x,top.y,grip.x,grip.y,edge)
        canvas.drawCircle(grip.x,grip.y,7*d,fill);canvas.drawCircle(grip.x,grip.y,7*d,edge)
        val text=Paint(Paint.ANTI_ALIAS_FLAG).apply { color=edge.color;textSize=11*resources.displayMetrics.scaledDensity/zoom }
        canvas.drawText(ui(R.string.ui_rotate),grip.x+10*d,grip.y+4*d,text)
        s.geometry.resizeHandles().values.forEach { point ->
            val r=RectF(point.x-5*d,point.y-5*d,point.x+5*d,point.y+5*d)
            canvas.drawRect(r,fill);canvas.drawRect(r,edge)
        }
    }
    private fun hitSelection(s: PaintDocument.Selection,point: PointF): Int {
        val radius=22*resources.displayMetrics.density/zoom
        val handles=s.geometry.resizeHandles()
        val corner=handles.keys.minByOrNull { hypot(handles.getValue(it).x-point.x,handles.getValue(it).y-point.y) }!!
        val nearest=handles.getValue(corner)
        val cornerDistance=hypot(nearest.x-point.x,nearest.y-point.y)
        val grip=rotationHandle(s);val rotationDistance=hypot(grip.x-point.x,grip.y-point.y)
        val centreDistance=hypot(s.rect.centerX()-point.x,s.rect.centerY()-point.y)
        // A small selection still has a usable move target at its centre.
        if (s.geometry.contains(point) && centreDistance < min(cornerDistance,rotationDistance)) return -2
        if (rotationDistance <= radius && rotationDistance < cornerDistance) return 4
        if (cornerDistance <= radius) return corner
        return if (s.geometry.contains(point)) -2 else -1
    }
    private fun updateSelectionTouch(point: PointF) {
        val s=document.selection ?: return
        val original=initialSelectionRect ?: return
        if (!selectionChanged && hypot(point.x-selectionTouchStart.x,point.y-selectionTouchStart.y)*zoom < touchSlop) return
        val geometry=SelectionGeometry(original,initialSelectionRotation)
        var rotation=initialSelectionRotation
        val rect=when (selectionHandle) {
            -2 -> RectF(original).apply { offset(point.x-selectionTouchStart.x,point.y-selectionTouchStart.y) }
            4 -> {
                val before=atan2(selectionTouchStart.y-original.centerY(),selectionTouchStart.x-original.centerX())
                val after=atan2(point.y-original.centerY(),point.x-original.centerX())
                rotation=((initialSelectionRotation+Math.toDegrees((after-before).toDouble()).toFloat()+540)%360)-180
                val cardinal=(rotation/90).roundToInt()*90f
                if (abs(rotation-cardinal)<.001f) rotation=cardinal
                RectF(original)
            }
            in 0..3, in 5..8 -> {
                val target=geometry.resizeHandles().getValue(selectionHandle).apply { offset(point.x-selectionTouchStart.x,point.y-selectionTouchStart.y) }
                geometry.resized(selectionHandle,target,lockSelectionAspect)
            }
            else -> return
        }
        if (rect!=s.rect || rotation!=s.rotation) {
            document.startMovingSelection(asGesture=true)
            s.rect.set(rect);s.rotation=rotation;selectionChanged=true
        }
    }

    private fun handleTouch(event: MotionEvent): Boolean {
        if (!isEnabled) return false
        parent?.requestDisallowInterceptTouchEvent(true)
        if(event.actionMasked==MotionEvent.ACTION_DOWN) rulerTouch=grid && (event.x<rulerInset || event.y<rulerInset)
        if(rulerTouch) {
            if(event.actionMasked in listOf(MotionEvent.ACTION_UP,MotionEvent.ACTION_CANCEL)) rulerTouch=false
            return true
        }
        if (event.pointerCount > 1) {
            val focus=PointF((event.getX(0)+event.getX(1))/2,(event.getY(0)+event.getY(1))/2)
            val span=hypot(event.getX(0)-event.getX(1),event.getY(0)-event.getY(1))
            if (!multiTouch) { cancelTouchEdit(); if (supportsCursor()) cursor.set(cursorInitial) }
            if (multiTouch && event.actionMasked==MotionEvent.ACTION_MOVE) {
                if (pinchSpan > 1 && span > 1) zoomAt(zoom*span/pinchSpan,pinchFocus.x,pinchFocus.y)
                fitMode=false;panX+=focus.x-pinchFocus.x;panY+=focus.y-pinchFocus.y;clampPan();invalidate();onStatus()
            }
            pinchFocus=focus;pinchSpan=span
            multiTouch = true; down = false; scrollAxis = 0; removeCallbacks(sprayTick)
            return true
        }
        // Scrollbars remain reachable for every tool, including cursor drawing.
        if (event.actionMasked == MotionEvent.ACTION_DOWN) {
            scrollAxis = if (event.y >= height-bar) 1 else if (event.x >= width-bar) 2 else 0
            if (scrollAxis != 0) { down=false; multiTouch=false; beginScrollbar(event.x,event.y); return true }
        } else if (scrollAxis != 0) {
            if (event.actionMasked != MotionEvent.ACTION_CANCEL) dragScrollbar(event.x,event.y)
            if (event.actionMasked in listOf(MotionEvent.ACTION_UP,MotionEvent.ACTION_CANCEL)) scrollAxis=0
            invalidate();onStatus();return true
        }
        var point = toImage(event.x, event.y)
        previewTouch.set(event.x,event.y)
        if (supportsCursor() && trim==null) {
            when(event.actionMasked) {
                MotionEvent.ACTION_DOWN -> {
                    multiTouch=false;down=true;cursorInitial.set(cursor)
                    screenStart.set(event.x,event.y);screenPrevious.set(event.x,event.y)
                    previous.set(cursor);smoothedPrevious.set(cursor)
                    if(cursorDrawing) {document.beginGesture();stroke(cursor,cursor)}
                }
                MotionEvent.ACTION_MOVE -> if(down && !multiTouch) {
                    val old=PointF(cursor.x,cursor.y)
                    cursor.offset((event.x-screenPrevious.x)/zoom,(event.y-screenPrevious.y)/zoom);clampCursor(cursor)
                    screenPrevious.set(event.x,event.y)
                    if(cursorDrawing && old!=cursor) stroke(old,cursor)
                }
                MotionEvent.ACTION_UP -> {
                    if(multiTouch || !down) {multiTouch=false;down=false;return true}
                    val old=PointF(cursor.x,cursor.y)
                    cursor.offset((event.x-screenPrevious.x)/zoom,(event.y-screenPrevious.y)/zoom);clampCursor(cursor)
                    if(cursorDrawing) {
                        if(old!=cursor || document.strokeSmoothing && tool!=PaintTool.PENCIL && smoothedPrevious!=cursor) {
                            stroke(if(document.strokeSmoothing && tool!=PaintTool.PENCIL) smoothedPrevious else old,cursor,finishing=true)
                        }
                        document.finishGesture()
                    }
                    down=false;performClick();onStatus()
                }
                MotionEvent.ACTION_CANCEL -> { if(cursorDrawing && down) document.cancelGesture();cursor.set(cursorInitial);down=false;multiTouch=false }
            }
            previewPoint=PointF(cursor.x,cursor.y);invalidate();onStatus();return true
        }
        previewPoint=point
        trim?.let { crop ->
            if (event.actionMasked == MotionEvent.ACTION_DOWN) {
                scrollAxis = if (event.y >= height-bar) 1 else if (event.x >= width-bar) 2 else 0
                beginScrollbar(event.x,event.y)
            }
            if (scrollAxis != 0) {
                if (event.actionMasked != MotionEvent.ACTION_CANCEL) dragScrollbar(event.x,event.y)
                if (event.actionMasked in listOf(MotionEvent.ACTION_UP,MotionEvent.ACTION_CANCEL)) scrollAxis = 0
                invalidate(); onStatus(); return true
            }
            when (event.actionMasked) {
                MotionEvent.ACTION_DOWN -> { multiTouch = false; crop.begin(point,24*resources.displayMetrics.density/zoom) }
                MotionEvent.ACTION_MOVE -> if (!multiTouch) crop.move(point)
                MotionEvent.ACTION_UP -> { if (!multiTouch) crop.move(point); crop.end(); multiTouch = false; performClick() }
                MotionEvent.ACTION_CANCEL -> crop.end(true)
            }
            invalidate(); onStatus(); return true
        }
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                multiTouch = false; down = true; panning = tool == PaintTool.ZOOM
                screenStart = PointF(event.x, event.y); screenPrevious = PointF(event.x, event.y)
                scrollAxis = if (event.y >= height - bar) 1 else if (event.x >= width - bar) 2 else 0
                if (scrollAxis != 0) { beginScrollbar(event.x, event.y); return true }
                if (panning) return true
                selectionHandle=if (tool in listOf(PaintTool.SELECT,PaintTool.LASSO)) document.selection?.let { hitSelection(it,point) } ?: -1 else -1
                movingSelection=selectionHandle != -1
                initialSelectionRect=document.selection?.rect?.let { RectF(it) }
                initialSelectionFloating=document.selection?.floating==true
                initialSelectionRotation=document.selection?.rotation ?: 0f
                selectionTouchStart=PointF(point.x,point.y);selectionChanged=false
                polygonTouchMoved=false
                polygonDoubleTap=tool==PaintTool.POLYGON && polygon.size>=(if(closePolygon) 3 else 2) && lastPolygonTapTime>=0 &&
                    event.eventTime-lastPolygonTapTime in 1..ViewConfiguration.getDoubleTapTimeout().toLong() &&
                    lastPolygonTap?.let { hypot(event.x-it.x,event.y-it.y)<=doubleTapSlop }==true
                initialCurve=if (tool==PaintTool.CURVE) PointF(control1.x,control1.y) to PointF(control2.x,control2.y) else null
                if (movingSelection) { previous = point; return true }
                if (tool !in listOf(PaintTool.SELECT,PaintTool.LASSO)) document.finishSelection()
                previous = point
                if (tool == PaintTool.CURVE && curveStage > 0) {
                    if (curveStage == 1) control1 = point else control2 = point
                } else {
                    start = point; end = point; trace = Path().apply { moveTo(point.x, point.y) }
                }
                when (tool) {
                    PaintTool.PENCIL, PaintTool.BRUSH, PaintTool.WATERCOLOR, PaintTool.ERASER -> { document.beginGesture(); smoothedPrevious.set(point); stroke(point, point) }
                    PaintTool.SPRAY -> { document.beginGesture(); spray(point); postDelayed(sprayTick, 40) }
                    else -> Unit
                }
            }
            MotionEvent.ACTION_MOVE -> {
                if (multiTouch || !down) return true
                if (hypot(event.x-screenStart.x,event.y-screenStart.y)>touchSlop) polygonTouchMoved=true
                if (scrollAxis != 0) { dragScrollbar(event.x, event.y); return true }
                if (panning) {
                    fitMode=false;panX += event.x - screenPrevious.x; panY += event.y - screenPrevious.y; clampPan()
                    screenPrevious = PointF(event.x, event.y)
                } else if (movingSelection) {
                    updateSelectionTouch(point);onStatus()
                } else when (tool) {
                    PaintTool.PENCIL, PaintTool.BRUSH, PaintTool.WATERCOLOR, PaintTool.ERASER -> {
                        for (i in 0 until event.historySize) {
                            val historical = toImage(event.getHistoricalX(i), event.getHistoricalY(i))
                            stroke(previous, historical); previous = historical
                        }
                        stroke(previous, point); previous = point
                    }
                    PaintTool.SPRAY -> { previous = point; spray(point) }
                    PaintTool.LASSO -> { trace.lineTo(point.x, point.y); end = point }
                    PaintTool.CURVE -> {
                        if (curveStage == 1) control1 = point else if (curveStage == 2) control2 = point else end = point
                    }
                    else -> end = point
                }
            }
            MotionEvent.ACTION_UP -> {
                removeCallbacks(sprayTick)
                if (multiTouch || !down) { multiTouch = false; down = false; return true }
                down = false
                if (scrollAxis != 0) { scrollAxis = 0; performClick(); return true }
                if (panning) {
                    // Navigate mode never draws or changes zoom on a single tap.
                } else if (movingSelection) {
                    updateSelectionTouch(point)
                    document.finishGesture()
                    if (selectionChanged) document.edited()
                } else {
                    when (tool) {
                        PaintTool.PENCIL, PaintTool.BRUSH, PaintTool.WATERCOLOR, PaintTool.ERASER -> { stroke(if(document.strokeSmoothing && tool!=PaintTool.PENCIL) smoothedPrevious else previous, point, finishing=true); document.finishGesture() }
                        PaintTool.SPRAY -> document.finishGesture()
                        PaintTool.FILL -> onFill(point.x.toInt(), point.y.toInt())
                        PaintTool.PICKER -> if (point.x >= 0 && point.y >= 0 && point.x < document.bitmap.width && point.y < document.bitmap.height) {
                            document.foreground = document.bitmap.getPixel(point.x.toInt(), point.y.toInt()); onPick(document.foreground)
                        }
                        PaintTool.TEXT -> onText(point.x, point.y)
                        PaintTool.SELECT -> { document.finishSelection();end = point; document.select(bounds()) }
                        PaintTool.LASSO -> { document.finishSelection();trace.lineTo(point.x, point.y); trace.close(); val r = RectF(); trace.computeBounds(r, true); document.select(r, trace) }
                        PaintTool.POLYGON -> {
                            val tapped=!polygonTouchMoved && hypot(event.x-screenStart.x,event.y-screenStart.y)<=touchSlop
                            if (polygonDoubleTap && tapped) applyPending()
                            else {
                                polygon.add(PointF(point.x,point.y))
                                lastPolygonTap=if (tapped) PointF(event.x,event.y) else null
                                lastPolygonTapTime=if (tapped) event.eventTime else -1L
                                polygonDoubleTap=false
                            }
                        }
                        PaintTool.CURVE -> {
                            if (curveStage == 0) {
                                end = point; control1 = PointF(start.x + (end.x - start.x) / 3, start.y + (end.y - start.y) / 3)
                                control2 = PointF(start.x + 2 * (end.x - start.x) / 3, start.y + 2 * (end.y - start.y) / 3)
                            } else if (curveStage == 1) control1 = point else control2 = point
                            curveStage++
                            if (curveStage == 3) applyPending()
                        }
                        PaintTool.LINE, PaintTool.RECTANGLE, PaintTool.ELLIPSE, PaintTool.ROUND_RECT, PaintTool.HEART, PaintTool.STAR, PaintTool.ARROW -> { end = point; document.commitShape(tool, shapePath()) }
                        else -> Unit
                    }
                }
                movingSelection = false;selectionHandle=-1; panning = false; performClick(); onStatus()
            }
            MotionEvent.ACTION_CANCEL -> {
                cancelTouchEdit(); multiTouch=false; down = false; removeCallbacks(sprayTick)
            }
        }
        invalidate(); return true
    }
    override fun performClick(): Boolean { super.performClick(); return true }
    override fun onDetachedFromWindow() { removeCallbacks(sprayTick); super.onDetachedFromWindow() }
}
