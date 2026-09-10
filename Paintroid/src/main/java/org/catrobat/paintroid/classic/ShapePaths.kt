/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Path
import android.graphics.PointF
import android.graphics.RectF
import kotlin.math.*

internal object ShapePaths {
    fun heart(r: RectF) = Path().apply {
        fun x(n: Float) = r.left+n*r.width()
        fun y(n: Float) = r.top+n*r.height()
        moveTo(x(.5f),y(1f))
        cubicTo(x(.38f),y(.82f),x(0f),y(.53f),x(0f),y(.28f))
        cubicTo(x(0f),y(-.06f),x(.39f),y(-.11f),x(.5f),y(.22f))
        cubicTo(x(.61f),y(-.11f),x(1f),y(-.06f),x(1f),y(.28f))
        cubicTo(x(1f),y(.53f),x(.62f),y(.82f),x(.5f),y(1f));close()
    }
    fun star(r: RectF) = Path().apply {
        repeat(10) { i ->
            val angle = -PI/2+i*PI/5
            val radius = if (i%2==0) 1.0 else .38196601125
            val x=(r.centerX()+cos(angle)*r.width()/2*radius).toFloat()
            val y=(r.centerY()+sin(angle)*r.height()/2*radius).toFloat()
            if (i==0) moveTo(x,y) else lineTo(x,y)
        };close()
    }
    fun arrow(start: PointF,end: PointF,width: Float) = Path().apply {
        val dx=end.x-start.x;val dy=end.y-start.y;val length=hypot(dx,dy)
        if (length<.01f) return@apply
        val ux=dx/length;val uy=dy/length
        val head=min(length*.45f,max(width*2,length*.25f));val wing=head*.65f
        val tail=min(wing*.4f,max(width*.65f,length*.07f))
        val vertices=listOf(0f to -tail,(length-head) to -tail,(length-head) to -wing,
            length to 0f,(length-head) to wing,(length-head) to tail,0f to tail)
        vertices.forEachIndexed { i,(x,y) ->
            val px=start.x+x*ux-y*uy;val py=start.y+x*uy+y*ux
            if (i==0) moveTo(px,py) else lineTo(px,py)
        };close()
    }
}
