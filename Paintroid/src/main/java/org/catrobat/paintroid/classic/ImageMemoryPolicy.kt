/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.ActivityManager
import android.content.Context
import android.os.Build
import java.util.Locale

/** Admission control for this whole-bitmap editor, not a promise that allocation cannot fail.
 * Three ARGB work buffers cover decode/orientation, transforms and selection compositing.
 * Keep memory for the current document/clipboard, Java objects, the UI and other apps.
 */
class ImageMemoryPolicy private constructor(val workingBytes: Long) {
    companion object {
        private const val MIB = 1024L * 1024
        private const val RESERVE = 32 * MIB
        // Android Bitmap allocation/row strides and several platform APIs use signed ints.
        const val MAX_BITMAP_PIXELS = (Int.MAX_VALUE.toLong() - 8) / 4
        fun calculate(maxHeap: Long, usedHeap: Long, availableSystem: Long, lowMemoryThreshold: Long, nativeBitmaps: Boolean): ImageMemoryPolicy {
            val heapHeadroom = (maxHeap - usedHeap - RESERVE).coerceAtLeast(0)
            val systemShare = ((availableSystem - lowMemoryThreshold).coerceAtLeast(0) / 3 - RESERVE).coerceAtLeast(0)
            val processShare = if (nativeBitmaps) (maxHeap.coerceAtMost(Long.MAX_VALUE / 2) * 2 - RESERVE).coerceAtLeast(0) else heapHeadroom
            return ImageMemoryPolicy(minOf(systemShare, processShare))
        }
        fun forDevice(context: Context): ImageMemoryPolicy {
            val runtime = Runtime.getRuntime()
            val memory = ActivityManager.MemoryInfo()
            (context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager).getMemoryInfo(memory)
            if (memory.totalMem <= 0) return forRuntime() // Platform memory data unavailable.
            return calculate(runtime.maxMemory(), runtime.totalMemory() - runtime.freeMemory(), memory.availMem, memory.threshold, Build.VERSION.SDK_INT >= 26)
        }
        fun forRuntime(): ImageMemoryPolicy {
            val runtime = Runtime.getRuntime()
            return ImageMemoryPolicy((runtime.maxMemory() - (runtime.totalMemory() - runtime.freeMemory()) - RESERVE).coerceAtLeast(0))
        }
    }
    fun maxPixels(residentPixels: Long = 0): Long {
        val residentBytes = residentPixels.coerceIn(0, Long.MAX_VALUE / 4) * 4
        return minOf(MAX_BITMAP_PIXELS, (workingBytes - residentBytes).coerceAtLeast(0) / 12)
    }
    fun check(width: Int, height: Int, residentPixels: Long = 0) {
        require(width > 0 && height > 0) { ui(R.string.ui_enter_positive_image_dimensions) }
        val pixels = width.toLong() * height.toLong()
        val permitted = maxPixels(residentPixels)
        if (pixels > permitted) throw ImageSizeException(String.format(Locale.ROOT,
            ui(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current),
            width, height, pixels / 1_000_000.0, permitted / 1_000_000.0))
    }
}
class ImageSizeException(message: String) : IllegalArgumentException(message)
