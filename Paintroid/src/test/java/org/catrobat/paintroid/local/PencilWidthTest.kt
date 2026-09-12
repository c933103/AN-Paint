/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import org.catrobat.paintroid.classic.PaintCanvas
import org.catrobat.paintroid.classic.PaintDocument
import org.catrobat.paintroid.classic.PaintTool
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class PencilWidthTest {
    private fun withDocument(width: Int,height: Int,block: (PaintDocument)->Unit) {
        val document=PaintDocument(width,height,RuntimeEnvironment.getApplication().cacheDir)
        try { block(document) } finally { document.close() }
    }
    @Test fun pencilDrawsExactAdjustableHardEdgedWidthsIndependentlyOfBrushSize() {
        withDocument(160,160) { document ->
            document.foreground=Color.BLACK
            document.strokeWidth=17f
            for (width in listOf(1,4,25,100)) {
                document.bitmap.eraseColor(Color.WHITE)
                document.pencilWidth=width.toFloat()
                val paint=document.paint(PaintTool.PENCIL)
                assertFalse(paint.isAntiAlias)
                assertEquals(Paint.Cap.SQUARE,paint.strokeCap)
                Canvas(document.bitmap).drawLine(20.5f,80.5f,139.5f,80.5f,paint)
                val column=(0 until 160).map { document.bitmap.getPixel(80,it) }
                assertEquals(width,column.count { it==Color.BLACK })
                assertTrue(column.all { it==Color.BLACK || it==Color.WHITE })
                assertEquals(17f,document.paint(PaintTool.BRUSH).strokeWidth,0f)
            }
        }
    }

    @Test fun pencilWidthSurvivesDraftRestoreAndOldDraftsKeepOnePixelDefault() {
        val context=RuntimeEnvironment.getApplication()
        withDocument(20,20) { document ->
            val board=PaintCanvas(context,document)
            board.pencilSize=73f
            val state=board.draftState()
            board.pencilSize=1f
            board.restoreDraft(state)
            assertEquals(73f,document.paint(PaintTool.PENCIL).strokeWidth,0f)
            board.restoreDraft(JSONObject())
            assertEquals(1f,board.pencilSize,0f)
            board.pencilSize=Float.NaN
            assertEquals(1f,board.pencilSize,0f)
            board.pencilSize=1000f
            assertEquals(100f,board.pencilSize,0f)
        }
    }
}
