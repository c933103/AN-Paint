/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import kotlin.math.*

/** Integer image coordinates; tick count is bounded by the visible screen, not image size. */
internal object PixelRuler {
    data class Tick(val pixel: Int,val position: Float,val major: Boolean)
    fun ticks(origin: Float,zoom: Float,start: Float,end: Float,pixels: Int,labelSpacing: Float): List<Tick> {
        if(!zoom.isFinite() || zoom<=0f || end<=start || pixels<=0) return emptyList()
        val wanted=max(1.0,labelSpacing/zoom.toDouble())
        val power=10.0.pow(floor(log10(wanted)))
        val major=(listOf(1.0,2.0,5.0,10.0).first {it*power>=wanted}*power).toLong().coerceIn(1,Int.MAX_VALUE.toLong())
        val minor=when {major%5==0L ->major/5;major%2==0L ->major/2;else->major}
        val first=max(0.0,ceil((start-origin)/zoom.toDouble()/minor)).toLong()*minor
        val last=min(pixels.toDouble(),floor((end-origin)/zoom.toDouble())).toLong()
        if(first>last) return emptyList()
        return (first..last step minor).map {Tick(it.toInt(),origin+it*zoom,it%major==0L)}
    }
}
