/* Pocket Paint Local regression checks, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.*
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.io.IOException
import java.util.ArrayDeque
import kotlin.random.Random

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class FullResolutionStorageTest {
    @Test fun undoHistoryPreservesTranslucentPixelsExactly() {
        val cache = RuntimeEnvironment.getApplication().cacheDir
        val bitmap = Bitmap.createBitmap(8197, 2, Bitmap.Config.ARGB_8888)
        val colours = intArrayOf(Color.TRANSPARENT, Color.argb(16, 240, 32, 80), Color.argb(128, 100, 50, 200), Color.WHITE, Color.BLACK)
        for (x in 0 until bitmap.width) bitmap.setPixel(x, 0, colours[x % colours.size])
        val before = IntArray(bitmap.width * bitmap.height)
        bitmap.getPixels(before, 0, bitmap.width, 0, 0, bitmap.width, bitmap.height)
        RasterHistory(cache).use { history ->
            val saved = history.capture(bitmap)
            bitmap.eraseColor(Color.RED)
            assertSame(bitmap, history.restore(saved, bitmap))
            val after = IntArray(before.size)
            bitmap.getPixels(after, 0, bitmap.width, 0, 0, bitmap.width, bitmap.height)
            assertArrayEquals(before, after)
            history.discard(saved); assertFalse(saved.file.exists())
        }
        bitmap.recycle()
    }
    @Test fun damagedUndoEntryIsRejectedBeforeChangingPixels() {
        val bitmap = Bitmap.createBitmap(80, 80, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.BLUE) }
        RasterHistory(RuntimeEnvironment.getApplication().cacheDir).use { history ->
            val saved = history.capture(bitmap)
            bitmap.eraseColor(Color.RED); saved.file.writeText("damaged cache")
            try { history.restore(saved, bitmap); fail("Corrupt history must be rejected") } catch (_: IOException) { }
            assertEquals(Color.RED, bitmap.getPixel(0, 0)); assertEquals(Color.RED, bitmap.getPixel(79, 79))
        }; bitmap.recycle()
    }
    @Test fun unavailableUndoStorageAbortsEditWithoutChangingTheImage() {
        val parent = File.createTempFile("unwritable-parent-", ".test", RuntimeEnvironment.getApplication().cacheDir)
        val document = PaintDocument(32, 32, parent)
        try {
            try { document.commitShape(PaintTool.LINE, Path().apply { moveTo(0f, 0f); lineTo(31f, 31f) }); fail("Edit must stop if its undo snapshot cannot be stored") }
            catch (_: IOException) { }
            assertEquals(Color.WHITE, document.bitmap.getPixel(16, 16)); assertFalse(document.canUndo)
        } finally { document.close(); parent.delete() }
    }
    @Test fun scanlineFillMatchesFourConnectedReferenceWithToleranceAndAlpha() {
        val random = Random(574)
        for (threshold in listOf(0, 25, 90)) repeat(4) {
            val width = 137; val height = 19
            val original = IntArray(width * height) {
                val value = random.nextInt(4)
                when (value) { 0 -> Color.WHITE; 1 -> Color.rgb(230, 230, 230); 2 -> Color.argb(220, 240, 240, 240); else -> Color.BLACK }
            }
            val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
            bitmap.setPixels(original, 0, width, 0, 0, width, height)
            // Compare the actual bitmap pixel values after Android's alpha conversion.
            bitmap.getPixels(original, 0, width, 0, 0, width, height)
            val start = random.nextInt(original.size); val target = original[start]
            val expected = original.clone(); val visited = BooleanArray(original.size)
            val queue = ArrayDeque<Int>(); queue.add(start)
            while (queue.isNotEmpty()) {
                val at = queue.removeFirst()
                if (visited[at]) continue
                visited[at] = true
                val value = original[at]
                val diff = listOf(Color.alpha(value) - Color.alpha(target), Color.red(value) - Color.red(target), Color.green(value) - Color.green(target), Color.blue(value) - Color.blue(target)).sumOf { it * it }
                if (diff > threshold * threshold) continue
                expected[at] = Color.BLUE
                if (at % width > 0) queue.add(at - 1)
                if (at % width < width - 1) queue.add(at + 1)
                if (at >= width) queue.add(at - width)
                if (at + width < expected.size) queue.add(at + width)
            }
            ScanlineFill.fill(bitmap, start % width, start / width, Color.BLUE, threshold.toFloat())
            val actual = IntArray(original.size); bitmap.getPixels(actual, 0, width, 0, 0, width, height)
            assertArrayEquals(expected, actual); bitmap.recycle()
        }
    }
    @Test fun fillCrossesRowSegmentBoundariesBeyond8192Pixels() {
        val bitmap = Bitmap.createBitmap(10003, 3, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.WHITE) }
        ScanlineFill.fill(bitmap, 0, 0, Color.RED, 0f)
        for (x in listOf(0, 8191, 8192, 10002)) assertEquals(Color.RED, bitmap.getPixel(x, 2))
        bitmap.recycle()
    }
}
