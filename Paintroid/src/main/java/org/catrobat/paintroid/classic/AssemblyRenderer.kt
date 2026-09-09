/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.*
import androidx.exifinterface.media.ExifInterface
import java.io.IOException
import kotlin.math.*

/** Only one source region is decoded at a time; previews never determine export quality. */
class AssemblyRenderer(private val context: Context, private val images: List<AssemblyImage>, private val layout: Map<String,Rect>, private val residentPixels: Long) {
    val original = ImageDimensions(layout.values.maxOf { it.right },layout.values.maxOf { it.bottom })
    fun estimatedBytes(size: ImageDimensions) = size.pixels * 28.0 + residentPixels * 4.0
    fun fits(size: ImageDimensions): Boolean = size.pixels <= ImageMemoryPolicy.MAX_BITMAP_PIXELS && estimatedBytes(size) <= ImageMemoryPolicy.forDevice(context).workingBytes
    fun suggested(previous: ImageDimensions? = null): ImageDimensions {
        val policy = ImageMemoryPolicy.forDevice(context)
        val pixels = ((policy.workingBytes-residentPixels*4).coerceAtLeast(0)/28).coerceAtMost(ImageMemoryPolicy.MAX_BITMAP_PIXELS)
        val ratio = min(1.0,sqrt(pixels.toDouble()/original.pixels)*.9)
        return original.scaled(min(ratio,previous?.let { it.width.toDouble()/original.width*.75 } ?: 1.0))
    }
    fun render(size: ImageDimensions, progress: (Int,Int) -> Unit = { _,_ -> }): Bitmap {
        if (!fits(size)) throw ImageSizeException("The assembly needs about ${memoryLabel(estimatedBytes(size))}. Choose a smaller output size.")
        val output = Bitmap.createBitmap(size.width,size.height,Bitmap.Config.ARGB_8888)
        try {
            val canvas = Canvas(output)
            val entries = images.filter { it.id in layout }
            entries.forEachIndexed { index,item ->
                val rect = layout.getValue(item.id)
                fun x(n: Int) = (n.toDouble()*size.width/original.width).roundToInt()
                fun y(n: Int) = (n.toDouble()*size.height/original.height).roundToInt()
                val dest = Rect(x(rect.left),y(rect.top),x(rect.right),y(rect.bottom))
                if (dest.width() > 0 && dest.height() > 0) {
                    val source = decodeCrop(item,ImageDimensions(dest.width(),dest.height()),residentPixels+size.pixels)
                    try { canvas.drawBitmap(source,null,dest,null) } finally { source.recycle() }
                }
                progress(index+1,entries.size)
            }
            return output
        } catch (error: Throwable) { output.recycle(); throw error }
    }
    private fun orientation(item: AssemblyImage): Pair<Int,Boolean> = try { ExifInterface(item.file.path).let { it.rotationDegrees to it.isFlipped } } catch (_: IOException) { 0 to false }
    private fun transform(width: Int, height: Int, rotation: Int, flip: Boolean): Matrix {
        val m = Matrix(); if (flip) m.postScale(-1f,1f); m.postRotate(rotation.toFloat())
        val rect = RectF(0f,0f,width.toFloat(),height.toFloat()); m.mapRect(rect); m.postTranslate(-rect.left,-rect.top); return m
    }
    @Suppress("DEPRECATION")
    fun decodeCrop(item: AssemblyImage, target: ImageDimensions, resident: Long = residentPixels): Bitmap {
        val (rotation,flip) = orientation(item)
        val rawWidth = if (rotation in listOf(90,270)) item.dimensions.height else item.dimensions.width
        val rawHeight = if (rotation in listOf(90,270)) item.dimensions.width else item.dimensions.height
        val inverse = Matrix(); check(transform(rawWidth,rawHeight,rotation,flip).invert(inverse))
        val raw = RectF(item.crop); inverse.mapRect(raw)
        val rect = Rect(raw.left.roundToInt().coerceIn(0,rawWidth-1),raw.top.roundToInt().coerceIn(0,rawHeight-1),raw.right.roundToInt().coerceIn(1,rawWidth),raw.bottom.roundToInt().coerceIn(1,rawHeight))
        // Upscaling final output is also allowed; decode the available original detail.
        val sampleTarget = ImageDimensions(min(target.width,item.crop.width()),min(target.height,item.crop.height()))
        val plan = ImportPlan.create(item.croppedSize,sampleTarget)
        ImageMemoryPolicy.forDevice(context).checkImport(plan,resident)
        val decoder = try { BitmapRegionDecoder.newInstance(item.file.path,false) } catch (_: IOException) { null }
        var input: Bitmap? = null; var output: Bitmap? = null
        try {
            if (decoder != null) {
                input = decoder.decodeRegion(rect,BitmapFactory.Options().apply { inSampleSize = plan.sample; inPreferredConfig = Bitmap.Config.ARGB_8888; inScaled = false })
                    ?: throw IOException("Could not decode the cropped region of ${item.name}.")
                val decoded = input
                val local = transform(decoded.width,decoded.height,rotation,flip)
                val rotated = RectF(0f,0f,decoded.width.toFloat(),decoded.height.toFloat()); local.mapRect(rotated)
                local.postScale(target.width/rotated.width(),target.height/rotated.height())
                output = Bitmap.createBitmap(target.width,target.height,Bitmap.Config.ARGB_8888)
                Canvas(output).drawBitmap(decoded,local,Paint(Paint.FILTER_BITMAP_FLAG))
            } else {
                // Some older platform codecs have no region decoder. Use a bounded full
                // decode, and fail visibly if preserving the requested crop detail cannot fit.
                val scale = min(1.0,max(target.width.toDouble()/item.crop.width(),target.height.toDouble()/item.crop.height()))
                val fullTarget = item.dimensions.scaled(scale)
                val fullPlan = ImportPlan.create(item.dimensions,fullTarget)
                ImageMemoryPolicy.forDevice(context).checkImport(fullPlan,resident+target.pixels)
                input = ImportedImage(item.file,item.name).decode(fullPlan)
                val decoded = input
                val region = RectF(item.crop.left.toFloat()*decoded.width/item.dimensions.width,item.crop.top.toFloat()*decoded.height/item.dimensions.height,
                    item.crop.right.toFloat()*decoded.width/item.dimensions.width,item.crop.bottom.toFloat()*decoded.height/item.dimensions.height)
                output = Bitmap.createBitmap(target.width,target.height,Bitmap.Config.ARGB_8888)
                val matrix = Matrix().apply { setRectToRect(region,RectF(0f,0f,target.width.toFloat(),target.height.toFloat()),Matrix.ScaleToFit.FILL) }
                Canvas(output).drawBitmap(decoded,matrix,Paint(Paint.FILTER_BITMAP_FLAG))
            }
            return output!!.also { output = null }
        } finally { decoder?.recycle(); input?.recycle(); output?.recycle() }
    }
}
