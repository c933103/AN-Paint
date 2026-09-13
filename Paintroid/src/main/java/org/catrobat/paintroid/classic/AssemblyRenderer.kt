/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.content.Context
import android.graphics.*
import androidx.exifinterface.media.ExifInterface
import java.io.IOException
import kotlin.math.*

/** Only one source region is decoded at a time; previews never determine export quality. */
class AssemblyRenderer(private val context: Context, private val images: List<AssemblyImage>, private val layout: Map<String,Rect>, private val residentPixels: Long) {
    val original = ImageDimensions(layout.values.maxOf { it.right },layout.values.maxOf { it.bottom })
    // File metadata stays constant for this output request. Inspect it once so
    // resizing the dialog does not repeatedly open native codecs on the UI thread.
    private val imports = images.filter { it.id in layout }.associate { it.id to ImportedImage(it.file,it.name,it.pageIndex) }
    private fun destination(rect: Rect,size: ImageDimensions): Rect {
        fun x(n: Int) = (n.toDouble()*size.width/original.width).roundToInt()
        fun y(n: Int) = (n.toDouble()*size.height/original.height).roundToInt()
        return Rect(x(rect.left),y(rect.top),x(rect.right),y(rect.bottom))
    }
    fun estimatedBytes(size: ImageDimensions): Double {
        var peak = size.pixels * 28.0 + residentPixels * 4.0
        imports.forEach { (id,source) ->
            val rect = destination(layout.getValue(id),size)
            val target = ImageDimensions(max(1,rect.width()),max(1,rect.height()))
            // Include the resident assembly output and the same native decode
            // plus compositing reserve used by decodeCrop below.
            val item=images.first { it.id==id }
            val sampleTarget=ImageDimensions(min(target.width,item.crop.width()),min(target.height,item.crop.height()))
            val plan=ImportPlan.create(item.croppedSize,sampleTarget)
            peak = max(peak,source.estimatedBytes(plan.copy(target=target),residentPixels+size.pixels))
        }
        return peak
    }
    fun fits(size: ImageDimensions): Boolean = size.pixels <= ImageMemoryPolicy.MAX_BITMAP_PIXELS && estimatedBytes(size) <= ImageMemoryPolicy.forDevice(context).workingBytes
    fun suggested(previous: ImageDimensions? = null): ImageDimensions? {
        val policy = ImageMemoryPolicy.forDevice(context)
        if (!fits(ImageDimensions(1,1))) return null
        var low = 0.0
        var high = min(1.0,previous?.let { it.width.toDouble()/original.width*.75 } ?: 1.0)
        repeat(48) {
            val ratio = (low+high)/2
            val candidate = original.scaled(ratio)
            if (candidate.pixels<=ImageMemoryPolicy.MAX_BITMAP_PIXELS && estimatedBytes(candidate)<=policy.workingBytes*.9) low=ratio else high=ratio
        }
        return original.scaled(low)
    }
    fun render(size: ImageDimensions, progress: (Int,Int) -> Unit = { _,_ -> }): Bitmap {
        if (!fits(size)) throw ImageSizeException(ui(R.string.ui_the_assembly_needs_about_choose_a_smaller_output, memoryLabel(estimatedBytes(size))))
        val output = Bitmap.createBitmap(size.width,size.height,Bitmap.Config.ARGB_8888)
        try {
            output.eraseColor(Color.WHITE);output.setHasAlpha(false)
            val canvas = Canvas(output)
            val entries = images.filter { it.id in layout }
            entries.forEachIndexed { index,item ->
                val rect = layout.getValue(item.id)
                val dest = destination(rect,size)
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
        val jxl=JxlCodec.isJxl(item.file)
        val tiff=TiffCodec.isTiff(item.file)
        val pdf=PdfCodec.isPdf(item.file)
        if(jxl || tiff || pdf || HeifCodec.isHeif(item.file)) {
            val policy=ImageMemoryPolicy.forDevice(context)
            val requirements=(imports[item.id] ?: ImportedImage(item.file,item.name,item.pageIndex)).memoryRequirements
            requirements.checkImport(policy,ImportPlan(target,1,target.pixels),resident)
            val budget=requirements.decoderBudget(policy.workingBytes,target,resident)
            return when {jxl -> JxlCodec.decode(item.file,target,budget,item.crop);tiff -> TiffCodec.decode(item.file,target,budget,item.crop,item.pageIndex);pdf -> PdfCodec.decode(item.file,target,budget,item.crop,item.pageIndex);else -> HeifCodec.decode(item.file,target,budget,item.crop)}
        }
        if(IcoCodec.isIco(item.file)) {
            val source=imports[item.id] ?: ImportedImage(item.file,item.name,item.pageIndex)
            val policy=ImageMemoryPolicy.forDevice(context)
            val plan=ImportPlan.create(source.dimensions,source.dimensions)
            source.checkImport(policy,plan,resident+target.pixels)
            val input=source.decode(plan,policy.workingBytes,resident+target.pixels)
            try {
                val output=Bitmap.createBitmap(target.width,target.height,Bitmap.Config.ARGB_8888)
                try {Canvas(output).drawBitmap(input,item.crop,Rect(0,0,target.width,target.height),Paint(Paint.FILTER_BITMAP_FLAG));return output}
                catch(error: Throwable) {output.recycle();throw error}
            } finally {input.recycle()}
        }
        val (rotation,flip) = orientation(item)
        val rawWidth = if (rotation in listOf(90,270)) item.dimensions.height else item.dimensions.width
        val rawHeight = if (rotation in listOf(90,270)) item.dimensions.width else item.dimensions.height
        val inverse = Matrix(); check(transform(rawWidth,rawHeight,rotation,flip).invert(inverse))
        val raw = RectF(item.crop); inverse.mapRect(raw)
        val rect = Rect(raw.left.roundToInt().coerceIn(0,rawWidth-1),raw.top.roundToInt().coerceIn(0,rawHeight-1),raw.right.roundToInt().coerceIn(1,rawWidth),raw.bottom.roundToInt().coerceIn(1,rawHeight))
        // Upscaling final output is also allowed; decode the available original detail.
        val sampleTarget = ImageDimensions(min(target.width,item.crop.width()),min(target.height,item.crop.height()))
        val plan = ImportPlan.create(item.croppedSize,sampleTarget)
        val source=imports[item.id] ?: ImportedImage(item.file,item.name,item.pageIndex)
        source.checkImport(ImageMemoryPolicy.forDevice(context),plan.copy(target=target),resident)
        val colour=checkNotNull(source.platformColour)
        return source.withPlatformFile { platformFile -> colour.withDecodeFile(platformFile) { decodeFile ->
            val decoder = try { BitmapRegionDecoder.newInstance(decodeFile.path,false) } catch (_: IOException) { null }
            var input: Bitmap? = null; var output: Bitmap? = null
            try {
                if (decoder != null) {
                    input = decoder.decodeRegion(rect,colour.options(plan.sample))
                        ?: throw IOException(ui(R.string.ui_could_not_decode_the_cropped_region_of, item.name))
                    val rawInput=input
                    val decoded = colour.convert(rawInput)
                    if(decoded !== rawInput) { rawInput.recycle();input=decoded }
                    val local = transform(decoded.width,decoded.height,rotation,flip)
                    val rotated = RectF(0f,0f,decoded.width.toFloat(),decoded.height.toFloat()); local.mapRect(rotated)
                    local.postScale(target.width/rotated.width(),target.height/rotated.height())
                    output = Bitmap.createBitmap(target.width,target.height,Bitmap.Config.ARGB_8888)
                    Canvas(output).drawBitmap(decoded,local,Paint(Paint.FILTER_BITMAP_FLAG or Paint.DITHER_FLAG))
                } else {
                    // Some older platform codecs have no region decoder. Use a bounded full
                    // decode, and fail visibly if preserving the requested crop detail cannot fit.
                    val scale = min(1.0,max(target.width.toDouble()/item.crop.width(),target.height.toDouble()/item.crop.height()))
                    val fullTarget = item.dimensions.scaled(scale)
                    val fullPlan = ImportPlan.create(item.dimensions,fullTarget)
                    val policy = ImageMemoryPolicy.forDevice(context)
                    source.checkImport(policy,fullPlan,resident+target.pixels)
                    input = source.decode(fullPlan,policy.workingBytes,resident+target.pixels)
                    val decoded = input
                    val region = RectF(item.crop.left.toFloat()*decoded.width/item.dimensions.width,item.crop.top.toFloat()*decoded.height/item.dimensions.height,
                        item.crop.right.toFloat()*decoded.width/item.dimensions.width,item.crop.bottom.toFloat()*decoded.height/item.dimensions.height)
                    output = Bitmap.createBitmap(target.width,target.height,Bitmap.Config.ARGB_8888)
                    val matrix = Matrix().apply { setRectToRect(region,RectF(0f,0f,target.width.toFloat(),target.height.toFloat()),Matrix.ScaleToFit.FILL) }
                    Canvas(output).drawBitmap(decoded,matrix,Paint(Paint.FILTER_BITMAP_FLAG or Paint.DITHER_FLAG))
                }
                output!!.also { output = null }
            } finally { decoder?.recycle(); input?.recycle(); output?.recycle() }
        } }
    }
}
