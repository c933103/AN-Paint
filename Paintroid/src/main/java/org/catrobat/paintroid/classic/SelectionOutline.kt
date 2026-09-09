/* AN Paint selection-outline recovery, 2026-09-09. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Path
import android.graphics.PathMeasure
import org.json.JSONArray
import org.json.JSONObject
import kotlin.math.ceil

/** This small vector is a display outline; the lossless floating PNG remains the selection mask. */
internal object SelectionOutline {
    fun write(path: Path): JSONArray {
        val countMeasure=PathMeasure(path,false)
        var contourCount=1
        while (contourCount<128 && countMeasure.nextContour()) contourCount++
        val pointsPerContour=4096/contourCount
        val result=JSONArray();val measure=PathMeasure(path,false)
        do {
            if (result.length()>=128) break
            // Reserve room for every contour so a large perimeter cannot hide its holes.
            val segments=ceil(measure.length/.5f).toInt().coerceIn(1,pointsPerContour-1)
            val points=JSONArray();val position=FloatArray(2)
            for (i in 0..segments) if (measure.getPosTan(measure.length*i/segments,position,null)) {
                points.put(position[0].toDouble());points.put(position[1].toDouble())
            }
            if (points.length()>=4) result.put(JSONObject().put("closed",measure.isClosed).put("points",points))
        } while (measure.nextContour())
        return result
    }
    fun read(contours: JSONArray?): Path? {
        if (contours==null || contours.length()==0) return null
        require(contours.length()<=128) { "Invalid selection outline." }
        var count=0
        return Path().apply {
            for (i in 0 until contours.length()) {
                val contour=contours.getJSONObject(i);val points=contour.getJSONArray("points")
                require(points.length()>=4 && points.length()%2==0)
                count+=points.length()/2;require(count<=4096)
                fun coordinate(index: Int)=points.getDouble(index).toFloat().also { require(it.isFinite()) }
                moveTo(coordinate(0),coordinate(1))
                for (j in 2 until points.length() step 2) lineTo(coordinate(j),coordinate(j+1))
                if (contour.optBoolean("closed")) close()
            }
        }
    }
}
