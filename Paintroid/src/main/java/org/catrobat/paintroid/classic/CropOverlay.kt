/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. Original touch-handle geometry. */
package org.catrobat.paintroid.classic

import android.graphics.*
import kotlin.math.*

/** Eight touch handles. Source cropping stays bounded; canvas bounds may expand. */
class CropOverlay(val image: ImageDimensions, initial: Rect = Rect(0,0,image.width,image.height), val allowOutside: Boolean = false) {
    var rect = Rect(initial); private set
    private var handle = -1
    private var origin = PointF()
    private var before = Rect(initial)
    val changed get() = rect != Rect(0,0,image.width,image.height)
    fun set(value: Rect) {
        require(value.right.toLong()-value.left in 1..Int.MAX_VALUE.toLong() && value.bottom.toLong()-value.top in 1..Int.MAX_VALUE.toLong())
        require(allowOutside || value.left >= 0 && value.top >= 0 && value.right <= image.width && value.bottom <= image.height)
        rect = Rect(value)
    }
    fun handles(): List<PointF> {
        val r = rect
        return listOf(PointF(r.left.toFloat(),r.top.toFloat()),PointF(r.exactCenterX(),r.top.toFloat()),PointF(r.right.toFloat(),r.top.toFloat()),
            PointF(r.right.toFloat(),r.exactCenterY()),PointF(r.right.toFloat(),r.bottom.toFloat()),PointF(r.exactCenterX(),r.bottom.toFloat()),
            PointF(r.left.toFloat(),r.bottom.toFloat()),PointF(r.left.toFloat(),r.exactCenterY()))
    }
    fun begin(point: PointF, radius: Float): Boolean {
        val nearest = handles().mapIndexed { i,p -> i to hypot(point.x-p.x,point.y-p.y) }.minByOrNull { it.second }!!
        handle = if (nearest.second <= radius) nearest.first else if (rect.contains(point.x.toInt(),point.y.toInt())) 8 else -1
        origin = point; before = Rect(rect); return handle >= 0
    }
    fun move(point: PointF) {
        if (handle < 0) return
        val r = Rect(before)
        val dx = (point.x.toDouble()-origin.x).roundToLong().coerceIn(Int.MIN_VALUE.toLong(),Int.MAX_VALUE.toLong())
        val dy = (point.y.toDouble()-origin.y).roundToLong().coerceIn(Int.MIN_VALUE.toLong(),Int.MAX_VALUE.toLong())
        val minX = if (allowOutside) Int.MIN_VALUE.toLong() else 0L
        val minY = minX
        val maxX = if (allowOutside) Int.MAX_VALUE.toLong() else image.width.toLong()
        val maxY = if (allowOutside) Int.MAX_VALUE.toLong() else image.height.toLong()
        if (handle == 8) {
            val x = dx.coerceIn(minX-r.left,maxX-r.right); val y = dy.coerceIn(minY-r.top,maxY-r.bottom)
            r.set((r.left+x).toInt(),(r.top+y).toInt(),(r.right+x).toInt(),(r.bottom+y).toInt())
        }
        else {
            if (handle in listOf(0,6,7)) r.left = (before.left.toLong()+dx).coerceIn(max(minX,r.right.toLong()-Int.MAX_VALUE),r.right-1L).toInt()
            if (handle in listOf(2,3,4)) r.right = (before.right.toLong()+dx).coerceIn(r.left+1L,min(maxX,r.left.toLong()+Int.MAX_VALUE)).toInt()
            if (handle in listOf(0,1,2)) r.top = (before.top.toLong()+dy).coerceIn(max(minY,r.bottom.toLong()-Int.MAX_VALUE),r.bottom-1L).toInt()
            if (handle in listOf(4,5,6)) r.bottom = (before.bottom.toLong()+dy).coerceIn(r.top+1L,min(maxY,r.top.toLong()+Int.MAX_VALUE)).toInt()
        }
        rect = r
    }
    fun end(cancel: Boolean = false) { if (cancel && handle >= 0) rect = before; handle = -1 }
    private fun difference(canvas: Canvas, outer: Rect, inner: Rect, paint: Paint) {
        val kept = Rect(outer)
        if (!kept.intersect(inner)) { canvas.drawRect(outer,paint); return }
        fun area(l: Int,t: Int,r: Int,b: Int) { if (l < r && t < b) canvas.drawRect(l.toFloat(),t.toFloat(),r.toFloat(),b.toFloat(),paint) }
        area(outer.left,outer.top,outer.right,kept.top); area(outer.left,kept.bottom,outer.right,outer.bottom)
        area(outer.left,kept.top,kept.left,kept.bottom); area(kept.right,kept.top,outer.right,kept.bottom)
    }
    fun drawExpansion(canvas: Canvas, background: Int) {
        if (!allowOutside) return
        val source = Rect(0,0,image.width,image.height)
        val p = Paint().apply { color = Color.WHITE }
        difference(canvas,rect,source,p)
        p.color = background; difference(canvas,rect,source,p)
    }
    fun draw(canvas: Canvas, zoom: Float, density: Float) {
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = 0x99000000.toInt() }; val r = RectF(rect)
        difference(canvas,Rect(0,0,image.width,image.height),rect,p)
        p.style = Paint.Style.STROKE; p.color = Color.WHITE; p.strokeWidth = 2*density/zoom; canvas.drawRect(r,p)
        val half = 6*density/zoom
        for (point in handles()) {
            p.style = Paint.Style.FILL; p.color = Color.WHITE; canvas.drawRect(point.x-half,point.y-half,point.x+half,point.y+half,p)
            p.style = Paint.Style.STROKE; p.color = 0xff1559a6.toInt(); p.strokeWidth = density/zoom; canvas.drawRect(point.x-half,point.y-half,point.x+half,point.y+half,p)
        }
    }
}
