/* Pocket Paint Local additions, 2026-09-07.
 * GNU AGPL version 3 or (at your option) any later version. No warranty.
 * Local.4 uses disk undo and a bounded-cache scanline fill at full resolution.
 */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.graphics.*
import android.os.Build
import java.util.ArrayDeque
import java.io.File

enum class PaintTool(private val labelId: Int, private val hintId: Int) {
    LASSO(R.string.ui_free_form_select, R.string.ui_draw_around_an_area_drag_inside_to_move),
    SELECT(R.string.ui_rectangle_select, R.string.ui_drag_a_selection_drag_inside_to_move_square),
    ERASER(R.string.ui_eraser, R.string.ui_drag_to_erase_with_the_background_colour),
    FILL(R.string.ui_bucket_fill, R.string.ui_tap_an_enclosed_area_adjust_tolerance_for_similar),
    PICKER(R.string.ui_eyedropper, R.string.ui_tap_the_image_to_sample_the_foreground_colour),
    ZOOM(R.string.ui_navigate, R.string.ui_drag_to_pan_without_drawing_pinch_with_two),
    PENCIL(R.string.ui_pencil, R.string.ui_draw_a_crisp_one_pixel_line),
    BRUSH(R.string.ui_brush, R.string.ui_draw_with_the_selected_brush_tip_and_size),
    WATERCOLOR(R.string.ui_watercolor, R.string.ui_draw_soft_watercolor_strokes_strength_controls_how_strongly),
    SPRAY(R.string.ui_airbrush, R.string.ui_hold_or_drag_to_spray_colour),
    TEXT(R.string.ui_text, R.string.ui_tap_the_canvas_to_place_text_and_choose),
    LINE(R.string.ui_line, R.string.ui_drag_from_the_start_to_the_end_of),
    CURVE(R.string.ui_curve, R.string.ui_drag_a_line_then_drag_twice_to_set),
    RECTANGLE(R.string.ui_rectangle, R.string.ui_drag_between_opposite_corners_choose_outline_or_fill),
    POLYGON(R.string.ui_polygon, R.string.ui_tap_vertices_then_double_tap_the_last_vertex),
    ELLIPSE(R.string.ui_ellipse, R.string.ui_drag_across_the_ellipse_s_bounding_box),
    ROUND_RECT(R.string.ui_rounded_rectangle, R.string.ui_set_radius_px_then_drag_between_opposite_corners),
    HEART(R.string.ui_heart, R.string.ui_drag_between_opposite_corners_to_draw_a_heart),
    STAR(R.string.ui_star, R.string.ui_drag_between_opposite_corners_to_draw_a_five),
    ARROW(R.string.ui_arrow, R.string.ui_drag_from_the_tail_towards_the_arrowhead_choose);
    val label: String get() = ui(labelId)
    val hint: String get() = ui(hintId)
}

/** A single raster document. Every committed gesture is one undoable operation. */
class PaintDocument(width: Int = 1024, height: Int = 768,
    historyDirectory: File = File(System.getProperty("java.io.tmpdir"), "pocketpaint-history"),
    private val allocationGuard: (Int, Int) -> Unit = { w, h -> ImageMemoryPolicy.forRuntime().check(w, h) }) {
    var bitmap: Bitmap = blank(width, height, Color.WHITE); private set
    var foreground = Color.BLACK
        set(value) { field = value or Color.BLACK }
    var background = Color.WHITE
        set(value) { field = value or Color.BLACK }
    var cornerRadius = 16f
    var strokeWidth = 5f
    var pencilWidth = 1f
        set(value) { field = if (value.isFinite()) value.coerceIn(1f,100f) else 1f }
    var watercolorStrength = 50
    var strokeSmoothing = false
    var antialiasing = false
    var sprayRadius = 10f
    var brushTip = 0
    var shapeStyle = 0 // outline, solid, background fill + foreground outline
    var tolerance = 0f
    var dirty = false; private set
    var changed: () -> Unit = {}
    private val history = RasterHistory(historyDirectory)
    private val undo = ArrayDeque<RasterHistory.Entry>()
    private val redo = ArrayDeque<RasterHistory.Entry>()
    private var gesture = false
    private var gestureDirty = false
    val canUndo get() = undo.isNotEmpty()
    val canRedo get() = redo.isNotEmpty()

    data class Selection(var rect: RectF, val image: Bitmap, val mask: Path?, var floating: Boolean, var rotation: Float = 0f,
        val outline: Path? = mask?.let { Path(it).apply {
            op(Path().apply { addRect(rect,Path.Direction.CW) },Path.Op.INTERSECT)
            offset(-rect.left,-rect.top)
        } }) {
        internal val geometry get() = SelectionGeometry(rect,rotation)
        internal fun transformedOutline(): Path? = outline?.let { local ->
            val matrix=Matrix().apply {
                setRectToRect(RectF(0f,0f,image.width.toFloat(),image.height.toFloat()),rect,Matrix.ScaleToFit.FILL)
                postRotate(rotation,rect.centerX(),rect.centerY())
            }
            Path(local).apply { transform(matrix) }
        }
        fun draw(canvas: Canvas, rendered: Bitmap, paint: Paint? = null) {
            canvas.save(); canvas.rotate(rotation,rect.centerX(),rect.centerY())
            canvas.drawBitmap(rendered,null,rect,paint); canvas.restore()
        }
    }
    var selection: Selection? = null; private set
    var clipboard: Bitmap? = null; private set
    val residentPixels: Long get() = bitmap.width.toLong() * bitmap.height +
        (selection?.image?.let { it.width.toLong() * it.height } ?: 0) +
        (clipboard?.let { it.width.toLong() * it.height } ?: 0)

    private fun blank(w: Int, h: Int, color: Int): Bitmap {
        require(w > 0 && h > 0) { ui(R.string.ui_enter_positive_image_dimensions) }
        allocationGuard(w, h)
        return Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888).apply { eraseColor(color or Color.BLACK);setHasAlpha(false) }
    }

    fun checkpoint(clearRedo: Boolean = true) {
        val snapshot = history.capture(bitmap)
        undo.addLast(snapshot)
        if (clearRedo) { redo.forEach { history.discard(it) }; redo.clear() }
        // Limit disk history, never image resolution. Retain at least one complete step.
        while (undo.size > 1 && undo.sumOf { it.file.length() } > 256L * 1024 * 1024) {
            history.discard(undo.removeFirst())
        }
    }

    fun beginGesture() { gestureDirty=dirty; checkpoint(false); gesture=true }
    fun finishGesture() {
        if (!gesture) return
        gesture=false; redo.forEach { history.discard(it) }; redo.clear(); edited()
    }
    fun cancelGesture() {
        if (!gesture) return
        val restored=history.restore(undo.last,bitmap)
        if (restored !== bitmap) bitmap.recycle()
        bitmap=restored; history.discard(undo.removeLast()); gesture=false; dirty=gestureDirty; changed()
    }

    fun edited() { dirty = true; changed() }
    fun markSaved() { dirty = false; changed() }

    private fun canonicalPixels(image: Bitmap): Boolean = image.config == Bitmap.Config.ARGB_8888 &&
        (Build.VERSION.SDK_INT < 26 || image.colorSpace?.isSrgb == true)

    private fun copyToCanvasFormat(image: Bitmap, checkMemory: Boolean = true): Bitmap {
        if (checkMemory) allocationGuard(image.width,image.height)
        if (canonicalPixels(image)) return image.copy(Bitmap.Config.ARGB_8888,true)
            ?: throw OutOfMemoryError(ui(R.string.ui_could_not_prepare_the_image))
        val copy=Bitmap.createBitmap(image.width,image.height,Bitmap.Config.ARGB_8888)
        try { Canvas(copy).drawBitmap(image,0f,0f,null); return copy }
        catch (error: Throwable) { copy.recycle(); throw error }
    }

    fun replace(image: Bitmap, asEdit: Boolean = false) {
        val incoming = if (!image.isMutable || !canonicalPixels(image)) copyToCanvasFormat(image) else image
        try {
            Canvas(incoming).drawColor(background,PorterDuff.Mode.DST_OVER)
            incoming.setHasAlpha(false)
            if (asEdit) checkpoint()
        } catch (error: Throwable) {
            if (incoming !== image) incoming.recycle()
            throw error
        }
        if (!asEdit) {
            undo.forEach { history.discard(it) }; undo.clear()
            redo.forEach { history.discard(it) }; redo.clear()
        }
        clearSelection()
        if (bitmap !== incoming) bitmap.recycle()
        if (image !== incoming && !image.isRecycled) image.recycle()
        bitmap = incoming
        dirty = asEdit
        changed()
    }

    fun newImage(w: Int, h: Int) = replace(blank(w, h, background))

    fun historySnapshot()=RasterHistory.Snapshot(undo.toList(),redo.toList())
    fun readHistory(zip: java.util.zip.ZipFile)=HistoryArchive.read(zip,history)
    fun restoreHistory(snapshot: RasterHistory.Snapshot) {
        undo.forEach {history.discard(it)};redo.forEach {history.discard(it)}
        undo.clear();redo.clear();undo.addAll(snapshot.undo);redo.addAll(snapshot.redo)
        changed()
    }

    fun undo() = moveHistory(undo, redo)
    fun redo() = moveHistory(redo, undo)

    private fun moveHistory(from: ArrayDeque<RasterHistory.Entry>, to: ArrayDeque<RasterHistory.Entry>) {
        if (from.isEmpty()) { clearSelection(); changed(); return }
        finishSelection() // Redo must include the visible, transformed floating content.
        val saved = history.capture(bitmap)
        try {
            if (bitmap.width != from.last.width || bitmap.height != from.last.height) allocationGuard(from.last.width, from.last.height)
            val restored = history.restore(from.last, bitmap)
            if (restored !== bitmap) bitmap.recycle()
            bitmap = restored; clearSelection()
            history.discard(from.removeLast()); to.addLast(saved); edited()
        } catch (error: Throwable) { history.discard(saved); throw error }
    }

    fun paint(tool: PaintTool): Paint = Paint().apply {
        color = if (tool == PaintTool.ERASER) background else foreground
        strokeWidth = if (tool == PaintTool.PENCIL) pencilWidth else this@PaintDocument.strokeWidth
        style = Paint.Style.STROKE
        strokeJoin = Paint.Join.ROUND
        strokeCap = if (brushTip == 1 || tool == PaintTool.PENCIL) Paint.Cap.SQUARE else Paint.Cap.ROUND
        isAntiAlias = tool != PaintTool.PENCIL && antialiasing
        if (tool == PaintTool.WATERCOLOR) {
            alpha = (watercolorStrength.coerceIn(1,100) * 255 / 100)
            maskFilter = BlurMaskFilter(maxOf(.5f,strokeWidth / 6), BlurMaskFilter.Blur.NORMAL)
        }
    }

    fun fill(x: Int, y: Int) {
        if (x !in 0 until bitmap.width || y !in 0 until bitmap.height) return
        if (bitmap.getPixel(x, y) == foreground && tolerance == 0f) return
        checkpoint()
        try { ScanlineFill.fill(bitmap, x, y, foreground, tolerance) }
        catch (error: Throwable) {
            // A failed operation must leave the original full-resolution pixels intact.
            history.restore(undo.last, bitmap); history.discard(undo.removeLast()); throw error
        }
        edited()
    }

    fun drawShape(canvas: Canvas, tool: PaintTool, path: Path) {
        val p = paint(tool)
        if (tool !in listOf(PaintTool.LINE, PaintTool.CURVE) && shapeStyle > 0) {
            p.style = Paint.Style.FILL
            p.color = if (shapeStyle == 2) background else foreground
            canvas.drawPath(path, p)
        }
        if (shapeStyle != 1 || tool in listOf(PaintTool.LINE, PaintTool.CURVE)) {
            p.style = Paint.Style.STROKE; p.color = foreground
            canvas.drawPath(path, p)
        }
    }

    fun commitShape(tool: PaintTool, path: Path) {
        checkpoint(); drawShape(Canvas(bitmap), tool, path); edited()
    }

    fun select(bounds: RectF, mask: Path? = null) {
        finishSelection()
        val r = RectF(bounds)
        if (!r.intersect(0f, 0f, bitmap.width.toFloat(), bitmap.height.toFloat()) || r.width() < 1 || r.height() < 1) return
        val rect = Rect(r.left.toInt(), r.top.toInt(), kotlin.math.ceil(r.right).toInt(), kotlin.math.ceil(r.bottom).toInt())
        allocationGuard(rect.width(), rect.height())
        val image = Bitmap.createBitmap(rect.width(), rect.height(), Bitmap.Config.ARGB_8888)
        val canvas = Canvas(image)
        canvas.translate(-rect.left.toFloat(), -rect.top.toFloat())
        if (mask != null) canvas.clipPath(mask)
        canvas.drawBitmap(bitmap, 0f, 0f, null)
        selection = Selection(RectF(rect), image, mask?.let { Path(it) }, false)
        changed()
    }

    fun selectionImage(): Bitmap? {
        // Alpha here is solely an internal geometric mask for non-rectangular selections.
        return selection?.image
    }

    private fun eraseSelection(s: Selection) {
        val canvas = Canvas(bitmap)
        val p = Paint().apply { color = background; style = Paint.Style.FILL; xfermode = PorterDuffXfermode(PorterDuff.Mode.SRC) }
        if (s.mask != null) canvas.drawPath(s.mask, p) else canvas.drawRect(s.rect, p)
    }

    fun startMovingSelection(asGesture: Boolean = false) {
        val s = selection ?: return
        if (!s.floating) {
            if (asGesture) beginGesture() else checkpoint()
            eraseSelection(s); s.floating = true; edited()
        }
    }

    fun finishSelection() {
        val s = selection ?: return
        if (s.floating) {
            val rendered = selectionImage()!!
            s.draw(Canvas(bitmap),rendered,Paint(Paint.FILTER_BITMAP_FLAG))
            if (rendered !== s.image) rendered.recycle()
            dirty = true
        }
        clearSelection(); changed()
    }

    private fun clearSelection() { selection?.image?.recycle(); selection = null }

    /** Restored floating content has already been lifted from the saved canvas. */
    fun restoreFloatingSelection(image: Bitmap, rect: RectF, rotation: Float = 0f, outline: Path? = null) {
        require(rect.width() > 0 && rect.height() > 0)
        require(rotation.isFinite())
        clearSelection(); selection = Selection(RectF(rect),image,null,true,rotation,outline); changed()
    }

    /** Render the transformed selection for clipboard/crop without resampling its source in place. */
    private fun transformedSelectionImage(): Bitmap? {
        val s = selection ?: return null
        val bounds = s.geometry.bounds()
        val w = kotlin.math.ceil(bounds.width().toDouble()).toLong()
        val h = kotlin.math.ceil(bounds.height().toDouble()).toLong()
        require(w in 1..Int.MAX_VALUE.toLong() && h in 1..Int.MAX_VALUE.toLong()) { ui(R.string.ui_selection_dimensions_are_too_large) }
        allocationGuard(w.toInt(),h.toInt())
        val output = Bitmap.createBitmap(w.toInt(),h.toInt(),Bitmap.Config.ARGB_8888)
        var rendered: Bitmap? = null
        try {
            rendered = selectionImage()!!
            val canvas = Canvas(output);canvas.translate(-bounds.left,-bounds.top)
            s.draw(canvas,rendered,Paint(Paint.FILTER_BITMAP_FLAG))
            return output
        } catch (error: Throwable) { output.recycle();throw error }
        finally { if (rendered !== s.image) rendered?.recycle() }
    }

    fun copySelection(): Boolean {
        val copied = transformedSelectionImage() ?: return false
        clipboard?.recycle(); clipboard = copied
        changed(); return true
    }

    fun deleteSelection(): Boolean {
        val s = selection ?: return false
        if (!s.floating) { checkpoint(); eraseSelection(s) }
        clearSelection(); edited(); return true
    }

    fun cutSelection(): Boolean {
        if (!copySelection()) return false
        return deleteSelection()
    }

    fun paste(image: Bitmap? = clipboard, takeOwnership: Boolean = false): Boolean {
        image ?: return false
        val copyRequired = !takeOwnership || !image.isMutable || !canonicalPixels(image)
        if (copyRequired) allocationGuard(image.width,image.height)
        val copy = if (copyRequired) copyToCanvasFormat(image,false) else image
        try { finishSelection(); checkpoint() }
        catch (error: Throwable) { if (copy !== image) copy.recycle(); throw error }
        if(takeOwnership && copy !== image) image.recycle()
        // Alpha is an internal floating-content mask. Commit composites it onto
        // the existing opaque canvas, including for an inserted transparent file.
        selection = Selection(RectF(0f, 0f, copy.width.toFloat(), copy.height.toFloat()), copy, null, true)
        edited(); return true
    }

    /** Placement changes only the floating geometry; retain the full-resolution source pixels. */
    fun fitSelectionToCanvas(): Boolean {
        val s=selection ?: return false
        startMovingSelection()
        val factor=minOf(bitmap.width.toFloat()/s.image.width,bitmap.height.toFloat()/s.image.height)
        val w=s.image.width*factor;val h=s.image.height*factor
        s.rect.set((bitmap.width-w)/2,(bitmap.height-h)/2,(bitmap.width+w)/2,(bitmap.height+h)/2)
        s.rotation=0f;edited();return true
    }

    fun restoreSelectionSize(): Boolean {
        val s=selection ?: return false
        startMovingSelection()
        val cx=s.rect.centerX();val cy=s.rect.centerY()
        s.rect.set(cx-s.image.width/2f,cy-s.image.height/2f,cx+s.image.width/2f,cy+s.image.height/2f)
        edited();return true
    }

    fun resize(w: Int, h: Int, stretch: Boolean) {
        require(w > 0 && h > 0) { ui(R.string.ui_enter_positive_image_dimensions) }
        finishSelection()
        val next = blank(w, h, background)
        val canvas = Canvas(next)
        val copyPaint = Paint(if (stretch) Paint.FILTER_BITMAP_FLAG else 0).apply { xfermode = PorterDuffXfermode(PorterDuff.Mode.SRC) }
        if (stretch) canvas.drawBitmap(bitmap, null, Rect(0, 0, w, h), copyPaint)
        else canvas.drawBitmap(bitmap, 0f, 0f, copyPaint)
        replace(next, true)
    }

    fun cropCanvas(rect: Rect) {
        require(rect.left >= 0 && rect.top >= 0 && rect.right <= bitmap.width && rect.bottom <= bitmap.height && rect.width() > 0 && rect.height() > 0) { ui(R.string.ui_crop_must_stay_inside_the_canvas) }
        changeCanvasBounds(rect)
    }

    fun changeCanvasBounds(rect: Rect) {
        val width = rect.right.toLong()-rect.left; val height = rect.bottom.toLong()-rect.top
        require(width in 1..Int.MAX_VALUE.toLong() && height in 1..Int.MAX_VALUE.toLong()) { ui(R.string.ui_enter_positive_canvas_dimensions_within_android_s_coordinate) }
        if (rect == Rect(0,0,bitmap.width,bitmap.height)) return
        allocationGuard(rect.width(),rect.height()); finishSelection()
        val next = Bitmap.createBitmap(rect.width(),rect.height(),Bitmap.Config.ARGB_8888)
        try {
            next.eraseColor(background)
            val copy = Paint().apply { xfermode = PorterDuffXfermode(PorterDuff.Mode.SRC) }
            Canvas(next).drawBitmap(bitmap,-rect.left.toFloat(),-rect.top.toFloat(),copy)
            replace(next,true)
        } catch (error: Throwable) { if (bitmap !== next) next.recycle(); throw error }
    }

    fun transform(matrix: Matrix) {
        allocationGuard(bitmap.width, bitmap.height)
        finishSelection()
        val transformed = Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, bitmap.height, matrix, false)
        replace(transformed.copy(Bitmap.Config.ARGB_8888, true), true)
        if (transformed !== bitmap && !transformed.isRecycled) transformed.recycle()
    }

    fun cropSelection(): Boolean {
        val image = transformedSelectionImage() ?: return false
        try { finishSelection(); replace(image, true); return true }
        catch (error: Throwable) { if (image !== bitmap) image.recycle(); throw error }
    }

    fun invert() {
        finishSelection(); checkpoint()
        val row = IntArray(bitmap.width)
        for (y in 0 until bitmap.height) {
            bitmap.getPixels(row, 0, row.size, 0, y, row.size, 1)
            for (x in row.indices) row[x] = (row[x] and -0x1000000) or (row[x].inv() and 0xffffff)
            bitmap.setPixels(row, 0, row.size, 0, y, row.size, 1)
        }
        edited()
    }

    fun clear() { finishSelection(); checkpoint(); bitmap.eraseColor(background); edited() }

    fun close() { clearSelection(); clipboard?.recycle(); bitmap.recycle(); history.close() }

    fun text(x: Float,y: Float,text: String,size: Float,typeface: Typeface,opaque: Boolean,
        underline: Boolean=false,strike: Boolean=false,alignment: Paint.Align=Paint.Align.LEFT,spacing: Float=1f,
        direction: TextDirection=TextDirection.HORIZONTAL,glyphOrientation: GlyphOrientation=GlyphOrientation.MIXED) {
        if(text.isBlank()) return
        require(text.length<=8192 && size.isFinite() && size in 1f..1024f && spacing.isFinite() && spacing in .5f..3f)
        val p=Paint(Paint.ANTI_ALIAS_FLAG).apply {color=foreground;textSize=size;this.typeface=typeface;isUnderlineText=underline;isStrikeThruText=strike}
        val bounds=VerticalText.bounds(text,p,direction,glyphOrientation,spacing)
        val length=if(direction==TextDirection.HORIZONTAL) bounds.width() else bounds.height()
        val shift=when(alignment) {Paint.Align.CENTER->length/2;Paint.Align.RIGHT->length;else->0f}
        val left=if(direction==TextDirection.HORIZONTAL) x-shift else if(direction==TextDirection.VERTICAL_RL) x-bounds.width()+p.fontSpacing else x
        val top=if(direction==TextDirection.HORIZONTAL) y else y-shift
        checkpoint()
        val canvas=Canvas(bitmap);canvas.save();canvas.translate(left,top)
        if(opaque) canvas.drawRect(bounds,Paint().apply {color=background})
        VerticalText.draw(canvas,text,p,direction,glyphOrientation,spacing,alignment)
        canvas.restore();edited()
    }

}
