/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.RectF
import org.catrobat.paintroid.classic.PaintDocument
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class FloatingSelectionGeometryRecoveryTest {
    @Test fun invalidGeometryCannotReplaceOrRecycleTheExistingSelection() {
        val folder=File(RuntimeEnvironment.getApplication().filesDir,"finite-selection-${java.util.UUID.randomUUID()}").apply {mkdirs()}
        val document=PaintDocument(8,6,folder)
        val accepted=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.BLUE)}
        val rejected=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888)
        try {
            // Ordinary off-canvas rotated selections remain valid, with no clipping.
            val rect=RectF(-3f,-2f,4f,5f)
            document.restoreFloatingSelection(accepted,rect,45f)
            val original=checkNotNull(document.selection)
            val cases=listOf(
                RectF(0f,0f,Float.POSITIVE_INFINITY,2f) to 0f,
                RectF(Float.NaN,0f,2f,2f) to 0f,
                RectF(-Float.MAX_VALUE,0f,Float.MAX_VALUE,2f) to 0f, // extent overflow
                RectF(2e38f,0f,3e38f,2f) to 0f, // centre overflow
                RectF(-1.5e38f,-1.5e38f,1.5e38f,1.5e38f) to 45f, // rotated extent overflow
                RectF(0f,0f,2f,2f) to Float.POSITIVE_INFINITY,
                RectF(0f,0f,0f,2f) to 0f
            )
            for((invalid,rotation) in cases) {
                try {document.restoreFloatingSelection(rejected,invalid,rotation);fail("Invalid geometry accepted")}
                catch(expected: IllegalArgumentException) { }
                assertSame(original,document.selection)
                assertEquals(rect,original.rect)
                assertEquals(45f,original.rotation,0f)
                assertFalse(accepted.isRecycled)
                assertFalse("Rejected bitmap remains caller-owned",rejected.isRecycled)
                assertEquals(Color.BLUE,accepted.getPixel(0,0))
            }
        } finally {document.close();rejected.recycle();folder.deleteRecursively()}
    }
}
