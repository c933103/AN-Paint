/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.graphics.*
import androidx.exifinterface.media.ExifInterface
import java.io.File
import java.io.IOException
import java.util.Locale
import kotlin.math.*

data class ImageDimensions(val width: Int, val height: Int) {
    init { require(width > 0 && height > 0) { ui(R.string.ui_enter_positive_image_dimensions) } }
    val pixels: Long get() = width.toLong() * height
    fun describe() = String.format(Locale.ROOT, ui(R.string.ui_d_d_px_d_pixels_2f_mp), width, height, pixels, pixels / 1_000_000.0)
    fun scaled(scale: Double) = ImageDimensions(max(1, floor(width * scale).toInt()), max(1, floor(height * scale).toInt()))
}

/** Estimates are doubles only for byte display/comparison; exact pixel counts use Long. */
fun memoryLabel(bytes: Double): String {
    val units = arrayOf("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB")
    var amount = bytes.coerceAtLeast(0.0); var unit = 0
    while (amount >= 1024 && unit < units.lastIndex) { amount /= 1024; unit++ }
    return String.format(Locale.ROOT, ui(R.string.ui_1f_s), amount, units[unit])
}

data class ImportPlan(val target: ImageDimensions, val sample: Int, val decodedPixels: Long) {
    fun estimatedBytes(residentPixels: Long) = max(target.pixels * 12.0, decodedPixels * 4.0 + target.pixels * 8.0) + residentPixels * 4.0
    companion object {
        fun create(source: ImageDimensions, target: ImageDimensions): ImportPlan {
            require(target.width <= source.width && target.height <= source.height) { ui(R.string.ui_choose_dimensions_no_larger_than_the_original) }
            fun ceilDivide(n: Int, d: Int) = (n.toLong() + d - 1) / d
            var sample = 1
            // Keep at least the requested detail. Decode a bounded power-of-two sample,
            // then scale once to the exact requested dimensions while applying EXIF.
            while (sample < (1 shl 30) && sample * 2 <= max(source.width, source.height) &&
                ceilDivide(source.width, sample * 2) >= target.width && ceilDivide(source.height, sample * 2) >= target.height) sample *= 2
            return ImportPlan(target, sample, ceilDivide(source.width,sample) * ceilDivide(source.height,sample))
        }
    }
}

fun ImageMemoryPolicy.accepts(plan: ImportPlan, residentPixels: Long): Boolean =
    plan.target.pixels <= maxPixels(residentPixels) && plan.decodedPixels <= ImageMemoryPolicy.MAX_BITMAP_PIXELS && plan.estimatedBytes(residentPixels) <= workingBytes.toDouble()

fun ImageMemoryPolicy.checkImport(plan: ImportPlan, residentPixels: Long) {
    check(plan.target.width, plan.target.height, residentPixels)
    if (!accepts(plan, residentPixels)) throw ImageSizeException(ui(R.string.ui_the_decoder_and_editing_buffers_need_about_the, memoryLabel(plan.estimatedBytes(residentPixels)), memoryLabel(workingBytes.toDouble())))
}

fun ImageMemoryPolicy.suggestResize(source: ImageDimensions, residentPixels: Long, maxScale: Double = 1.0): ImageDimensions? {
    if (!accepts(ImportPlan.create(source, ImageDimensions(1,1)), residentPixels)) return null
    var low = 0.0; var high = maxScale.coerceIn(0.0,1.0)
    // Leave 10% of the computed working budget free for changes while the dialog is open.
    repeat(48) {
        val scale = (low + high) / 2
        val plan = ImportPlan.create(source, source.scaled(scale))
        if (accepts(plan, residentPixels) && plan.estimatedBytes(residentPixels) <= workingBytes * .9) low = scale else high = scale
    }
    return source.scaled(low)
}

/** Native source/tile decode work does not necessarily shrink with the output.
 * Keep the same estimate for the prompt, admission check and decoder allowance.
 */
class ImportMemoryRequirements(private val nativeBytesAtOnePixel: Long? = null) {
    val hasNativeWork get() = nativeBytesAtOnePixel != null
    private fun nativeBytes(target: ImageDimensions): Double =
        nativeBytesAtOnePixel?.let { it.toDouble() + (target.pixels - 1) * 4.0 } ?: 0.0

    fun estimatedBytes(plan: ImportPlan, residentPixels: Long): Double = max(
        plan.estimatedBytes(residentPixels),
        nativeBytes(plan.target) + plan.target.pixels * 8.0 + residentPixels.coerceAtLeast(0) * 4.0
    )

    fun accepts(policy: ImageMemoryPolicy, plan: ImportPlan, residentPixels: Long): Boolean =
        policy.accepts(plan,residentPixels) && estimatedBytes(plan,residentPixels) <= policy.workingBytes.toDouble()

    fun checkImport(policy: ImageMemoryPolicy, plan: ImportPlan, residentPixels: Long) {
        policy.check(plan.target.width,plan.target.height,residentPixels)
        if(!accepts(policy,plan,residentPixels)) throw ImageSizeException(ui(R.string.ui_the_decoder_and_editing_buffers_need_about_the,
            memoryLabel(estimatedBytes(plan,residentPixels)),memoryLabel(policy.workingBytes.toDouble())))
    }

    fun suggestResize(source: ImageDimensions, policy: ImageMemoryPolicy, residentPixels: Long, maxScale: Double = 1.0): ImageDimensions? {
        if(!accepts(policy,ImportPlan.create(source,ImageDimensions(1,1)),residentPixels)) return null
        var low=0.0;var high=maxScale.coerceIn(0.0,1.0)
        repeat(48) {
            val scale=(low+high)/2;val plan=ImportPlan.create(source,source.scaled(scale))
            if(accepts(policy,plan,residentPixels) && estimatedBytes(plan,residentPixels)<=policy.workingBytes*.9) low=scale else high=scale
        }
        return source.scaled(low)
    }

    /** Native codec allowance includes its output, but excludes resident canvas
     * and the two further output-sized edit/compositing buffers reserved above.
     */
    fun decoderBudget(workingBytes: Long, target: ImageDimensions, residentPixels: Long): Long {
        fun subtract(bytes: Long,pixels: Long,perPixel: Long): Long =
            (bytes-pixels.coerceIn(0,Long.MAX_VALUE/perPixel)*perPixel).coerceAtLeast(0)
        return subtract(subtract(workingBytes.coerceAtLeast(0),residentPixels,4),target.pixels,8)
    }
}

/** The provider is copied once; this private file stays alive across the resize choice. */
class ImportedImage(val file: File, val name: String) {
    private val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
    private val orientation: ExifInterface?
    private val jxl=JxlCodec.isJxl(file)
    private val heif=HeifCodec.isHeif(file)
    val dimensions: ImageDimensions
    val memoryRequirements: ImportMemoryRequirements
    init {
        if(jxl) {val size=JxlCodec.dimensions(file);bounds.outWidth=size.width;bounds.outHeight=size.height}
        else if(heif) {val size=HeifCodec.dimensions(file);bounds.outWidth=size.width;bounds.outHeight=size.height}
        else BitmapFactory.decodeFile(file.path, bounds)
        if (bounds.outWidth <= 0 || bounds.outHeight <= 0) throw IOException(ui(R.string.ui_this_file_is_not_a_supported_image_use))
        orientation = if(jxl || heif) null else try { ExifInterface(file.path) } catch (_: IOException) { null }
        dimensions = if (orientation?.rotationDegrees in listOf(90,270)) ImageDimensions(bounds.outHeight,bounds.outWidth) else ImageDimensions(bounds.outWidth,bounds.outHeight)
        // Inspect the native source/tile footprint once, not on every slider tick.
        // Ordinary formats never initialize a JNI library here.
        memoryRequirements=ImportMemoryRequirements(if(heif) HeifCodec.decodeWorkingBytes(file,ImageDimensions(1,1)) else null)
    }
    fun estimatedBytes(plan: ImportPlan,residentPixels: Long)=memoryRequirements.estimatedBytes(plan,residentPixels)
    fun accepts(policy: ImageMemoryPolicy,plan: ImportPlan,residentPixels: Long)=memoryRequirements.accepts(policy,plan,residentPixels)
    fun checkImport(policy: ImageMemoryPolicy,plan: ImportPlan,residentPixels: Long)=memoryRequirements.checkImport(policy,plan,residentPixels)
    fun suggestResize(policy: ImageMemoryPolicy,residentPixels: Long,maxScale: Double=1.0)=memoryRequirements.suggestResize(dimensions,policy,residentPixels,maxScale)

    fun decode(plan: ImportPlan,workingBytes: Long=ImageMemoryPolicy.forRuntime().workingBytes,residentPixels: Long=0): Bitmap {
        val decoderBudget=memoryRequirements.decoderBudget(workingBytes,plan.target,residentPixels)
        if(jxl) return JxlCodec.decode(file,plan.target,decoderBudget)
        if(heif) return HeifCodec.decode(file,plan.target,decoderBudget)
        var decoded: Bitmap? = null
        var output: Bitmap? = null
        try {
            val input = BitmapFactory.decodeFile(file.path, BitmapFactory.Options().apply {
                inSampleSize = plan.sample; inScaled = false; inMutable = true; inPreferredConfig = Bitmap.Config.ARGB_8888
            }) ?: throw IOException(ui(R.string.ui_android_could_not_decode_this_image))
            decoded = input
            input.density = Bitmap.DENSITY_NONE
            val rotation = orientation?.rotationDegrees ?: 0; val flip = orientation?.isFlipped == true
            if (rotation == 0 && !flip && input.width == plan.target.width && input.height == plan.target.height && input.isMutable) {
                decoded = null; return input
            }
            output = Bitmap.createBitmap(plan.target.width,plan.target.height,Bitmap.Config.ARGB_8888)
            output.density = Bitmap.DENSITY_NONE
            val matrix = Matrix()
            if (flip) matrix.postScale(-1f,1f)
            matrix.postRotate(rotation.toFloat())
            val rect = RectF(0f,0f,input.width.toFloat(),input.height.toFloat()); matrix.mapRect(rect)
            matrix.postTranslate(-rect.left,-rect.top)
            matrix.postScale(plan.target.width / rect.width(),plan.target.height / rect.height())
            Canvas(output).drawBitmap(input,matrix,Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG))
            return output.also { output = null }
        } finally { decoded?.recycle(); output?.recycle() }
    }
}
