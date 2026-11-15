/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.PointF
import android.graphics.Rect
import org.json.JSONArray
import org.json.JSONObject

/** Parse fallible pending-edit geometry before changing a document or canvas. */
internal data class CanvasDraftGeometry(
    val polygon: List<PointF>,
    val curve: List<PointF>?,
    val trim: CropOverlay?
) {
    companion object {
        fun read(state: JSONObject,width: Int,height: Int): CanvasDraftGeometry {
            fun point(a: JSONArray,i: Int): PointF {
                val x=a.getDouble(i).toFloat();val y=a.getDouble(i+1).toFloat()
                require(x.isFinite() && y.isFinite()) { "Non-finite canvas draft point" }
                return PointF(x,y)
            }
            val polygon=state.optJSONArray("polygon")?.let { points ->
                List(points.length()) {point(points.getJSONArray(it),0)}
            } ?: emptyList()
            val curve=state.optJSONArray("curve_points")?.let {a ->List(4) {point(a,it*2)}}
            val trim=state.optJSONArray("bounds")?.let {a ->
                CropOverlay(ImageDimensions(width,height),allowOutside=true).apply {
                    set(Rect(a.getInt(0),a.getInt(1),a.getInt(2),a.getInt(3)))
                }
            }
            return CanvasDraftGeometry(polygon,curve,trim)
        }
    }
}
