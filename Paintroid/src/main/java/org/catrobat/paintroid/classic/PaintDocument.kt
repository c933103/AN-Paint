/* Pocket Paint Local additions, 2026-09-07.
 * GNU AGPL version 3 or (at your option) any later version. No warranty.
 * Local.4 uses disk undo and a bounded-cache scanline fill at full resolution.
 */
package org.catrobat.paintroid.classic

import android.graphics.*
import java.util.ArrayDeque
import java.io.File

enum class PaintTool(val label: String, val hint: String) {
    LASSO("Free-form select", "Draw around an area. Drag inside to move, square corner or edge handles to resize, or the round handle to rotate. Commit selection applies the edit."),
    SELECT("Rectangle select", "Drag a selection. Drag inside to move, square corner or edge handles to resize, or the round handle to rotate. Lock proportions keeps its shape."),
    ERASER("Eraser", "Drag to erase with the background colour."),
    FILL("Bucket fill", "Tap an enclosed area. Adjust tolerance for similar colours."),
    PICKER("Eyedropper", "Tap the image to sample the foreground colour."),
    ZOOM("Navigate", "Drag to pan without drawing. Pinch with two fingers to zoom and pan. Two-finger navigation also works with drawing tools."),
    PENCIL("Pencil", "Draw a crisp, one-pixel line."),
    BRUSH("Brush", "Draw with the selected brush tip and size."),
    SPRAY("Airbrush", "Hold or drag to spray colour."),
    TEXT("Text", "Tap the canvas to place text and choose its font and size."),
    LINE("Line", "Drag from the start to the end of the line."),
    CURVE("Curve", "Drag a line, then drag twice to set its two bends. Finish curve commits it early."),
    RECTANGLE("Rectangle", "Drag between opposite corners. Choose outline or fill below."),
    POLYGON("Polygon", "Tap vertices, then double-tap the last vertex to close the polygon. Finish polygon also works."),
    ELLIPSE("Ellipse", "Drag across the ellipse's bounding box."),
    ROUND_RECT("Rounded rectangle", "Set Radius (px), then drag between opposite corners. The radius is limited to half the shorter side of each rectangle.")
}

/** A single raster document. Every committed gesture is one undoable operation. */
class PaintDocument(width: Int = 1024, height: Int = 768,
    historyDirectory: File = File(System.getProperty("java.io.tmpdir"), "pocketpaint-history"),
    val opaqueCanvas: Boolean = false,
    private val allocationGuard: (Int, Int) -> Unit = { w, h -> ImageMemoryPolicy.forRuntime().check(w, h) }) {
    var bitmap: Bitmap = blank(width, height, Color.WHITE); private set
    var foreground = Color.BLACK
        set(value) { field = if (opaqueCanvas) value or Color.BLACK else value }
    var background = Color.WHITE
        set(value) { field = if (opaqueCanvas) value or Color.BLACK else value }
    var cornerRadius = 16f
    var strokeWidth = 5f
    var brushTip = 0
    var shapeStyle = 0 // outline, solid, background fill + foreground outline
    var tolerance = 0f
    var transparentSelection = false
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
        require(w > 0 && h > 0) { "Enter positive image dimensions." }
        allocationGuard(w, h)
        return Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888).apply { eraseColor(color) }
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

    fun replace(image: Bitmap, asEdit: Boolean = false) {
        val incoming = if (opaqueCanvas && !image.isMutable) {
            allocationGuard(image.width,image.height)
            image.copy(Bitmap.Config.ARGB_8888,true) ?: throw OutOfMemoryError("Could not prepare the image.")
        } else image
        if (opaqueCanvas) {
            Canvas(incoming).drawColor(background,PorterDuff.Mode.DST_OVER)
            incoming.setHasAlpha(false)
        }
        if (asEdit) checkpoint() else {
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
        strokeWidth = if (tool == PaintTool.PENCIL) 1f else this@PaintDocument.strokeWidth
        style = Paint.Style.STROKE
        strokeJoin = Paint.Join.ROUND
        strokeCap = if (brushTip == 1 || tool == PaintTool.PENCIL) Paint.Cap.SQUARE else Paint.Cap.ROUND
        isAntiAlias = tool != PaintTool.PENCIL
        if (tool == PaintTool.ERASER && !opaqueCanvas) xfermode = PorterDuffXfermode(PorterDuff.Mode.SRC)
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
        val image = selection?.image ?: return null
        if (!transparentSelection) return image
        allocationGuard(image.width, image.height)
        val output = image.copy(Bitmap.Config.ARGB_8888, true)
        val row = IntArray(output.width)
        for (y in 0 until output.height) {
            output.getPixels(row, 0, row.size, 0, y, row.size, 1)
            for (x in row.indices) if (row[x] == background) row[x] = Color.TRANSPARENT
            output.setPixels(row, 0, row.size, 0, y, row.size, 1)
        }
        return output
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
        require(w in 1..Int.MAX_VALUE.toLong() && h in 1..Int.MAX_VALUE.toLong()) { "Selection dimensions are too large." }
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
        if (!takeOwnership) allocationGuard(image.width, image.height)
        finishSelection(); checkpoint()
        val copy = if (takeOwnership) image else image.copy(Bitmap.Config.ARGB_8888, true)
        selection = Selection(RectF(0f, 0f, copy.width.toFloat(), copy.height.toFloat()), copy, null, true)
        edited(); return true
    }

    fun resize(w: Int, h: Int, stretch: Boolean) {
        require(w > 0 && h > 0) { "Enter positive image dimensions." }
        finishSelection()
        val next = blank(w, h, background)
        val canvas = Canvas(next)
        val copyPaint = Paint(if (stretch) Paint.FILTER_BITMAP_FLAG else 0).apply { xfermode = PorterDuffXfermode(PorterDuff.Mode.SRC) }
        if (stretch) canvas.drawBitmap(bitmap, null, Rect(0, 0, w, h), copyPaint)
        else canvas.drawBitmap(bitmap, 0f, 0f, copyPaint)
        replace(next, true)
    }

    fun cropCanvas(rect: Rect) {
        require(rect.left >= 0 && rect.top >= 0 && rect.right <= bitmap.width && rect.bottom <= bitmap.height && rect.width() > 0 && rect.height() > 0) { "Crop must stay inside the canvas." }
        changeCanvasBounds(rect)
    }

    fun changeCanvasBounds(rect: Rect) {
        val width = rect.right.toLong()-rect.left; val height = rect.bottom.toLong()-rect.top
        require(width in 1..Int.MAX_VALUE.toLong() && height in 1..Int.MAX_VALUE.toLong()) { "Enter positive canvas dimensions within Android's coordinate range." }
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

    fun text(x: Float, y: Float, text: String, size: Float, typeface: Typeface, opaque: Boolean,
        underline: Boolean = false, strike: Boolean = false, alignment: Paint.Align = Paint.Align.LEFT, spacing: Float = 1f) {
        if (text.isBlank()) return
        checkpoint()
        val canvas = Canvas(bitmap)
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = foreground; textSize = size; this.typeface = typeface
            isUnderlineText = underline; isStrikeThruText = strike; textAlign = alignment
        }
        val lines = text.split('\n')
        val lineHeight = p.fontSpacing * spacing
        val width = lines.maxOf { p.measureText(it) }
        val left = x - when (alignment) { Paint.Align.CENTER -> width/2; Paint.Align.RIGHT -> width; else -> 0f }
        if (opaque) canvas.drawRect(left, y, left + width, y + (lines.size - 1) * lineHeight + p.fontSpacing,
            Paint().apply { color = background })
        lines.forEachIndexed { i, line -> canvas.drawText(line, x, y - p.fontMetrics.top + i * lineHeight, p) }
        edited()
    }
}
