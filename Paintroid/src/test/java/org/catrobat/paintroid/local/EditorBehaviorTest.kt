/*
 * Added for Pocket Paint Local, 2026-09-07.
 * Licensed under GNU AGPL version 3 or (at your option) any later version.
 * See LICENSE at the project root. Distributed without any warranty.
 */
package org.catrobat.paintroid.local

import android.graphics.*
import android.content.Intent
import android.view.View
import org.catrobat.paintroid.MainActivity
import org.catrobat.paintroid.FileIO
import org.catrobat.paintroid.R
import org.catrobat.paintroid.command.implementation.PointCommand
import org.catrobat.paintroid.command.implementation.DefaultCommandFactory
import org.catrobat.paintroid.command.implementation.DefaultCommandManager
import org.catrobat.paintroid.command.implementation.FillCommand
import org.catrobat.paintroid.common.CommonFactory
import org.catrobat.paintroid.model.Layer
import org.catrobat.paintroid.model.LayerModel
import org.catrobat.paintroid.tools.ToolType
import org.catrobat.paintroid.tools.helper.JavaFillAlgorithm
import org.catrobat.paintroid.tools.helper.JavaFillAlgorithmFactory
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.ByteArrayOutputStream
import java.io.File
import android.net.Uri

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [28], qualifiers = "w360dp-h640dp-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class EditorBehaviorTest {
    private fun image(w: Int, h: Int, color: Int = Color.WHITE): Bitmap =
        Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888).apply { eraseColor(color) }

    private fun fill(bitmap: Bitmap, x: Int, y: Int, color: Int, tolerance: Float = 0f) {
        JavaFillAlgorithm().apply {
            setParameters(bitmap, Point(x,y), color, bitmap.getPixel(x,y), tolerance)
            performFilling()
        }
    }

    @Test fun bucketStopsAtBoundaryAndLeavesDisconnectedAreaAlone() {
        val bitmap = image(32, 32)
        for (y in 0 until 32) bitmap.setPixel(16,y,Color.BLACK)
        fill(bitmap, 4, 4, Color.RED)
        for (y in 0 until 32) for (x in 0 until 32) {
            val expected = when { x < 16 -> Color.RED; x == 16 -> Color.BLACK; else -> Color.WHITE }
            assertEquals("pixel $x,$y",expected,bitmap.getPixel(x,y))
        }
    }

    @Test fun bucketToleranceIncludesNearbyColorsAndStillRequiresConnection() {
        val bitmap = image(4, 1, Color.BLACK)
        bitmap.setPixel(1,0,Color.rgb(12,0,0))
        bitmap.setPixel(2,0,Color.rgb(40,0,0))
        fill(bitmap,0,0,Color.BLUE,20f)
        assertEquals(Color.BLUE,bitmap.getPixel(0,0))
        assertEquals(Color.BLUE,bitmap.getPixel(1,0))
        assertEquals(Color.rgb(40,0,0),bitmap.getPixel(2,0))
        assertEquals(Color.BLACK,bitmap.getPixel(3,0))
    }

    @Test fun bucketPreservesSelectedTransparency() {
        val bitmap = image(9,9,Color.TRANSPARENT)
        bitmap.setPixel(8,8,Color.BLACK)
        val chosen = Color.argb(96,255,0,0)
        fill(bitmap,0,0,chosen)
        assertEquals(chosen,bitmap.getPixel(0,0))
        assertEquals(chosen,bitmap.getPixel(7,8))
        assertEquals(Color.BLACK,bitmap.getPixel(8,8))
    }

    @Test fun singlePixelImageCanBeFilled() {
        val bitmap = image(1,1)
        fill(bitmap,0,0,Color.GREEN)
        assertEquals(Color.GREEN,bitmap.getPixel(0,0))
    }

    @Test fun nativeRectangleCanBeFilledWithoutTouchingItsOutline() {
        val bitmap = image(32,32)
        val stroke = Paint().apply { color=Color.BLACK; style=Paint.Style.STROKE; strokeWidth=2f; isAntiAlias=false }
        Canvas(bitmap).drawRect(4f,4f,28f,28f,stroke)
        fill(bitmap,12,12,Color.GREEN)
        assertEquals(Color.GREEN,bitmap.getPixel(12,12))
        assertEquals(Color.WHITE,bitmap.getPixel(0,0))
        assertEquals(Color.BLACK,bitmap.getPixel(4,12))
        assertEquals(Color.BLACK,bitmap.getPixel(28,12))
    }

    @Test fun drawingCommandAndTransparentEraserChangeRealPixels() {
        val bitmap = image(32,32,Color.TRANSPARENT)
        val canvas = Canvas(bitmap)
        val stroke = Paint().apply { color=Color.BLUE; strokeWidth=9f; strokeCap=Paint.Cap.ROUND }
        PointCommand(stroke,PointF(16f,16f)).run(canvas,LayerModel())
        assertEquals(Color.BLUE,bitmap.getPixel(16,16))
        val eraser = Paint(stroke).apply { xfermode=PorterDuffXfermode(PorterDuff.Mode.CLEAR) }
        PointCommand(eraser,PointF(16f,16f)).run(canvas,LayerModel())
        assertEquals(0,Color.alpha(bitmap.getPixel(16,16)))
    }

    @Test fun pngRoundTripPreservesColorAndTransparency() {
        val bitmap = image(4,4,Color.TRANSPARENT)
        bitmap.setPixel(0,0,Color.BLUE)
        bitmap.setPixel(2,1,Color.argb(96,255,0,0))
        val bytes = ByteArrayOutputStream()
        assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,bytes))
        val encoded = bytes.toByteArray()
        val decoded = BitmapFactory.decodeByteArray(encoded,0,encoded.size)
        assertNotNull(decoded)
        assertTrue(bitmap.sameAs(decoded))
    }

    @Test fun portraitImportPreservesDimensionsWhenMemoryIsAvailable() {
        val context = RuntimeEnvironment.getApplication()
        val file = File(context.cacheDir, "portrait-import.png")
        val original = image(24,48,Color.BLUE)
        file.outputStream().use { assertTrue(original.compress(Bitmap.CompressFormat.PNG,100,it)) }
        val imported = FileIO.getScaledBitmapFromUri(context.contentResolver,Uri.fromFile(file),context)
        assertNotNull(imported.bitmap)
        assertEquals(24,imported.bitmap!!.width)
        assertEquals(48,imported.bitmap!!.height)
        assertEquals(Color.BLUE,imported.bitmap!!.getPixel(0,0))
    }

    @Test fun undoAndRedoRestoreActualBucketPixels() {
        val layers = LayerModel()
        val manager = DefaultCommandManager(CommonFactory(),layers)
        manager.setInitialStateCommand(DefaultCommandFactory().createInitCommand(image(16,16)))
        manager.reset()
        val paint = Paint().apply { color=Color.RED }
        manager.addCommand(FillCommand(JavaFillAlgorithmFactory(),Point(2,2),paint,0f))
        assertEquals(Color.RED,layers.currentLayer!!.bitmap.getPixel(2,2))
        assertTrue(manager.isUndoAvailable)
        manager.undo()
        assertEquals(Color.WHITE,layers.currentLayer!!.bitmap.getPixel(2,2))
        assertTrue(manager.isRedoAvailable)
        manager.redo()
        assertEquals(Color.RED,layers.currentLayer!!.bitmap.getPixel(2,2))
    }

    @Test fun editorActivityInitializesItsCanvasAndSamplesImageColor() {
        val controller = Robolectric.buildActivity(MainActivity::class.java, Intent(Intent.ACTION_MAIN))
        try {
            val activity = controller.create().start().resume().visible().get()
            assertNotNull(activity.findViewById<View>(R.id.pocketpaint_drawing_surface_view))
            assertNotNull(activity.toolReference.tool)
            assertNotNull(activity.defaultToolController)
            val chosen=Color.rgb(25,120,240)
            activity.layerModel.apply {
                reset()
                width=32; height=32
                val layer=Layer(image(32,32,chosen))
                addLayerAt(0,layer); currentLayer=layer
            }
            activity.defaultToolController.switchTool(ToolType.PIPETTE)
            assertTrue(activity.toolReference.tool!!.handleDown(PointF(8f,8f)))
            assertEquals(chosen,activity.toolPaint.color)
            activity.defaultToolController.switchTool(ToolType.FILL)
            assertEquals(ToolType.FILL,activity.toolReference.tool!!.toolType)
        } finally {
            controller.pause().stop().destroy()
        }
    }
}
