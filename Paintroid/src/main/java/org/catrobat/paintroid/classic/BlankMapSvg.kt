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

/** Rasterise the Commons original SVG at its own declared dimensions, on solid white. */
internal object BlankMapSvg {
    private fun read(source: File): SVG = source.inputStream().use { SVG.getFromInputStream(it) }.apply {
        // CSS physical units use 96 px/in, independent of the Android screen density.
        setRenderDPI(96f)
    }

    private fun originalDimensions(svg: SVG): ImageDimensions {
        // A viewBox is an internal coordinate system, not a replacement pixel size.
        // Do not substitute the editor canvas, a thumbnail size or a fixed 2000-pixel default.
        val pixels=SvgOriginalSize.pixels(svg.documentWidth.toDouble(),svg.documentHeight.toDouble())
        return ImageDimensions(pixels.width,pixels.height)
    }

    fun originalDimensions(source: File): ImageDimensions = originalDimensions(read(source))

    /** No target-size argument: this import must not rescale the source to the editor canvas. */
    fun renderOriginal(source: File,destination: File,policy: ImageMemoryPolicy,residentPixels: Long=0) {
        val svg=read(source)
        val size=originalDimensions(svg)
        // Fail before allocating if the original will not fit. Never silently shrink it.
        policy.check(size.width,size.height,residentPixels)
        val bitmap=Bitmap.createBitmap(size.width,size.height,Bitmap.Config.ARGB_8888)
        try {
            bitmap.density=Bitmap.DENSITY_NONE
            bitmap.eraseColor(Color.WHITE)
            svg.renderToCanvas(HardEdgeCanvas(bitmap))
            // Masks/clip effects may clear pixels despite the initial white canvas.
            Canvas(bitmap).drawColor(Color.WHITE,android.graphics.PorterDuff.Mode.DST_OVER)
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
