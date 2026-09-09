/* AN Paint selection controls, 2026-09-09. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.PointF
import android.graphics.RectF
import kotlin.math.*

/** Image-space geometry; the original selection pixels stay unscaled until rendering. */
internal class SelectionGeometry(val rect: RectF, val rotation: Float) {
    private fun rotateVector(x: Float, y: Float, angle: Float): PointF {
        val radians = Math.toRadians(angle.toDouble())
        return PointF((x*cos(radians)-y*sin(radians)).toFloat(), (x*sin(radians)+y*cos(radians)).toFloat())
    }
    fun point(x: Float, y: Float): PointF = rotateVector(x-rect.centerX(), y-rect.centerY(), rotation).apply {
        offset(rect.centerX(), rect.centerY())
    }
    fun corners() = listOf(point(rect.left,rect.top),point(rect.right,rect.top),point(rect.right,rect.bottom),point(rect.left,rect.bottom))
    fun resizeHandles(): Map<Int,PointF> = corners().mapIndexed { i,p -> i to p }.toMap()+mapOf(
        5 to point(rect.centerX(),rect.top),6 to point(rect.right,rect.centerY()),
        7 to point(rect.centerX(),rect.bottom),8 to point(rect.left,rect.centerY()))
    fun contains(p: PointF): Boolean = rotateVector(p.x-rect.centerX(),p.y-rect.centerY(),-rotation).let {
        rect.contains(it.x+rect.centerX(),it.y+rect.centerY())
    }
    fun bounds(): RectF = corners().let { points -> RectF(points.minOf { it.x },points.minOf { it.y },points.maxOf { it.x },points.maxOf { it.y }) }
    fun rotationHandle(distance: Float) = point(rect.centerX(),rect.top-distance)

    /** Resize about the opposite corner, in the selection's own rotated axes. */
    fun resized(corner: Int, target: PointF, lockAspect: Boolean): RectF {
        if (corner in 5..8) return resizedEdge(corner,target,lockAspect)
        val anchor = corners()[(corner+2)%4]
        val delta = rotateVector(target.x-anchor.x,target.y-anchor.y,-rotation)
        val sx = if (corner==0 || corner==3) -1 else 1
        val sy = if (corner<2) -1 else 1
        val coordinateLimit=Int.MAX_VALUE/4f
        var w = (delta.x*sx).coerceIn(1f,coordinateLimit)
        var h = (delta.y*sy).coerceIn(1f,coordinateLimit)
        if (lockAspect) {
            val scale = ((delta.x*sx*rect.width()+delta.y*sy*rect.height()) /
                (rect.width()*rect.width()+rect.height()*rect.height())).coerceIn(
                    max(1f/rect.width(),1f/rect.height()), min(coordinateLimit/rect.width(),coordinateLimit/rect.height()))
            w = rect.width()*scale; h = rect.height()*scale
        } else { w = w.roundToInt().toFloat(); h = h.roundToInt().toFloat() }
        val center = rotateVector(sx*w/2,sy*h/2,rotation).apply { offset(anchor.x,anchor.y) }
        return RectF(center.x-w/2,center.y-h/2,center.x+w/2,center.y+h/2)
    }
    /** Edges resize along the selection's rotated axes, with the opposite midpoint fixed. */
    private fun resizedEdge(edge: Int,target: PointF,lockAspect: Boolean): RectF {
        val vertical=edge==5 || edge==7
        val sign=if (edge==5 || edge==8) -1 else 1
        val opposite=when(edge) { 5 -> 7;6 -> 8;7 -> 5;else -> 6 }
        val anchor=resizeHandles().getValue(opposite)
        val delta=rotateVector(target.x-anchor.x,target.y-anchor.y,-rotation)
        val limit=Int.MAX_VALUE/4f
        val original=if (vertical) rect.height() else rect.width()
        val desired=((if (vertical) delta.y else delta.x)*sign).coerceIn(1f,limit)
        val scale=(desired/original).coerceIn(max(1f/rect.width(),1f/rect.height()),min(limit/rect.width(),limit/rect.height()))
        val w=if (lockAspect) rect.width()*scale else if (vertical) rect.width() else desired.roundToInt().toFloat()
        val h=if (lockAspect) rect.height()*scale else if (vertical) desired.roundToInt().toFloat() else rect.height()
        val centre=rotateVector(if (vertical) 0f else sign*w/2,if (vertical) sign*h/2 else 0f,rotation).apply { offset(anchor.x,anchor.y) }
        return RectF(centre.x-w/2,centre.y-h/2,centre.x+w/2,centre.y+h/2)
    }

}
