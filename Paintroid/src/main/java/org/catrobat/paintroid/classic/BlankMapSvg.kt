/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import com.caverock.androidsvg.SVG
import java.io.File
import java.io.IOException

/** Rasterise the Commons original SVG at exactly the chosen pixels, on solid white. */
internal object BlankMapSvg {
    fun aspectRatio(file: File): Double {
        val svg=file.inputStream().use {SVG.getFromInputStream(it)}
        val viewBox=svg.documentViewBox
        val w=viewBox?.width()?.toDouble()?.takeIf {it.isFinite() && it>0}
            ?: svg.documentWidth.toDouble().takeIf {it.isFinite() && it>0} ?: 2000.0
        val h=viewBox?.height()?.toDouble()?.takeIf {it.isFinite() && it>0}
            ?: svg.documentHeight.toDouble().takeIf {it.isFinite() && it>0} ?: 1000.0
        return (w/h).coerceIn(0.01,100.0)
    }

    fun render(source: File, destination: File, width: Int, height: Int) {
        require(width>0 && height>0 && width.toLong()*height<=ImageMemoryPolicy.MAX_BITMAP_PIXELS)
        val svg=source.inputStream().use {SVG.getFromInputStream(it)}
        val bitmap=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888)
        try {
            bitmap.density=Bitmap.DENSITY_NONE
            bitmap.eraseColor(Color.WHITE)
            svg.renderToCanvas(HardEdgeCanvas(bitmap))
            destination.outputStream().use {out ->
                if(!bitmap.compress(Bitmap.CompressFormat.PNG,100,out)) throw IOException("Could not encode blank map as PNG")
            }
        } finally {bitmap.recycle()}
    }
}

/** Intercept SVG drawing operations *before* antialiasing can create boundary colours. */
internal class HardEdgeCanvas(bitmap: Bitmap) : Canvas(bitmap) {
    private fun hard(paint: Paint): Paint = Paint(paint).apply {
        isAntiAlias=false
        isDither=false
        isFilterBitmap=false
        if(style!=Paint.Style.FILL) {
            // SVG border strokes should be continuous and 100% opaque.
            pathEffect=null
            alpha=255
        }
    }

    override fun drawPath(path: Path, paint: Paint) = super.drawPath(path,hard(paint))
    override fun drawText(text: String, x: Float, y: Float, paint: Paint) =
        super.drawText(text,x,y,hard(paint))
    override fun drawTextOnPath(text: String, path: Path, hOffset: Float, vOffset: Float, paint: Paint) =
        super.drawTextOnPath(text,path,hOffset,vOffset,hard(paint))
}