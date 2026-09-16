/* Pocket Paint Local regression checks, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.content.*
import android.content.pm.ProviderInfo
import android.database.Cursor
import android.database.MatrixCursor
import android.graphics.*
import android.net.Uri
import android.os.Looper
import android.os.ParcelFileDescriptor
import android.provider.OpenableColumns
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import org.catrobat.paintroid.classic.*
import org.catrobat.paintroid.classic.ImageFormat
import org.junit.Assert.*
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.android.controller.ActivityController
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowContentResolver
import java.io.File
import java.util.zip.ZipInputStream

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ClassicWorkspaceTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private lateinit var provider: DocumentProvider
    private val uri = Uri.parse("content://classic.fixture/document/1")
    private val doc get() = activity.document
    private val canvas get() = activity.paintCanvas

    @Before fun start() {
        val context = RuntimeEnvironment.getApplication() as Context
        File(context.filesDir, "classic-recovery.png").delete()
        File(context.filesDir,"classic-autosave.zip").delete(); File(context.filesDir,"classic-autosave.zip.bak").delete()
        context.getSharedPreferences("classic-ui",Context.MODE_PRIVATE).edit().clear().commit()
        controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        activity = controller.setup().get()
        doc.newImage(96, 96); canvas.fit()
        provider = DocumentProvider().apply {
            file = File(context.cacheDir, "classic-fixture.image")
            attachInfo(context, ProviderInfo().apply { authority = "classic.fixture" })
        }
        ShadowContentResolver.registerProviderInternal("classic.fixture", provider)
    }
    @After fun stop() { controller.pause().stop(); awaitIo(); controller.destroy() }
    private fun click(tag: String) { EditorTestNavigation.click(activity,tag) }
    private fun tool(tool: PaintTool) { click("tool_${tool.name}"); assertEquals(tool, canvas.tool) }
    private fun event(action: Int, x: Float, y: Float) {
        val p = canvas.toScreen(x, y)
        val event = MotionEvent.obtain(0, 10, action, p.x, p.y, 0)
        assertTrue(canvas.dispatchTouchEvent(event)); event.recycle()
    }
    private fun tap(x: Float, y: Float) { event(MotionEvent.ACTION_DOWN, x, y); event(MotionEvent.ACTION_UP, x, y); shadowOf(Looper.getMainLooper()).idle(); awaitIo() }
    private fun drag(x1: Float, y1: Float, x2: Float, y2: Float) {
        event(MotionEvent.ACTION_DOWN, x1, y1)
        event(MotionEvent.ACTION_MOVE, (x1 + x2) / 2, (y1 + y2) / 2)
        event(MotionEvent.ACTION_UP, x2, y2)
    }
    private fun menu(name: String, index: Int) { EditorTestNavigation.command(activity,name,index) }
    private fun awaitIo() {
        val deadline = System.nanoTime() + 10_000_000_000L
        while (activity.busy && System.nanoTime() < deadline) { shadowOf(Looper.getMainLooper()).idle(); Thread.sleep(10) }
        shadowOf(Looper.getMainLooper()).idle()
        assertFalse("File operation remained busy", activity.busy)
    }
    private fun fixture(format: Bitmap.CompressFormat = Bitmap.CompressFormat.PNG) {
        val image = Bitmap.createBitmap(24, 48, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.BLUE) }
        writeSrgbFixture(image,provider.file,format); image.recycle()
    }
    private fun receive(result: Int = Activity.RESULT_OK) {
        EditorTestNavigation.chooseLocationIfShown()
        val launch = shadowOf(activity).nextStartedActivityForResult
        assertNotNull(launch)
        shadowOf(activity).receiveResult(launch.intent, result, if (result == Activity.RESULT_OK) Intent().setData(uri) else null)
        awaitIo()
    }
    private fun inkCount() = IntArray(doc.bitmap.width * doc.bitmap.height).also {
        doc.bitmap.getPixels(it, 0, doc.bitmap.width, 0, 0, doc.bitmap.width, doc.bitmap.height)
    }.count { it != Color.WHITE }

    @Test fun fileMenuLaunchesOpenDocumentWithoutAnyPhotoPermission() {
        shadowOf(activity.application).denyPermissions(Manifest.permission.READ_MEDIA_IMAGES, Manifest.permission.READ_EXTERNAL_STORAGE)
        menu("File", 1)
        val launch = shadowOf(activity).nextStartedActivityForResult
        assertNotNull("File > Load image must invoke Android", launch)
        assertEquals(ClassicPaintActivity.OPEN_IMAGE, launch.requestCode)
        assertEquals(Intent.ACTION_OPEN_DOCUMENT, launch.intent.action)
        assertTrue(launch.intent.hasCategory(Intent.CATEGORY_OPENABLE))
        assertEquals("*/*", launch.intent.type)
        assertEquals(0, launch.intent.flags and Intent.FLAG_ACTIVITY_NEW_DOCUMENT)
    }
    @Test @Config(sdk = [28]) fun fileMenuAlsoLaunchesOnAndroid9WithoutStoragePermission() = fileMenuLaunchesOpenDocumentWithoutAnyPhotoPermission()

    @Test fun clickThenProviderResultReplacesCanvasDespiteGenericMimeAndMissingNameColumn() {
        fixture(); provider.missingName = true
        menu("File", 1); receive()
        assertNull(activity.lastIoError); assertEquals(24, doc.bitmap.width); assertEquals(48, doc.bitmap.height)
        assertEquals(Color.BLUE, doc.bitmap.getPixel(10, 10)); assertEquals(1, provider.reads)
        assertTrue(activity.cacheDir.listFiles()!!.none { it.name.startsWith("classic-import-") })
    }
    @Test fun fileMenuOpensTheSamePickerAndCancellationKeepsCanvas() {
        menu("File", 1); receive(Activity.RESULT_CANCELED)
        assertEquals(96, doc.bitmap.width); assertNull(activity.lastIoError); assertFalse(doc.dirty)
    }
    @Test fun fileImportCreatesMovableSelectionAndAppliesImage() {
        fixture(Bitmap.CompressFormat.JPEG)
        EditorTestNavigation.otherImage(activity,0); receive()
        assertNotNull(doc.selection); assertEquals(PaintTool.SELECT, canvas.tool)
        drag(10f, 10f, 40f, 30f); click("apply")
        assertEquals(Color.WHITE, doc.bitmap.getPixel(5, 5))
        assertTrue(Color.blue(doc.bitmap.getPixel(40, 30)) > 240)
        assertTrue(Color.red(doc.bitmap.getPixel(40, 30)) < 15)
        click("undo"); assertEquals(0, inkCount())
    }
    @Test fun oversizedInsertedImageRemainsSelectedWithAllHandlesReachableAndOriginalPixelsRetained() {
        val image=Bitmap.createBitmap(480,240,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.BLUE)}
        provider.file.outputStream().use {assertTrue(image.compress(Bitmap.CompressFormat.PNG,100,it))};image.recycle()
        EditorTestNavigation.otherImage(activity,0);receive()
        assertEquals(96,doc.bitmap.width);assertEquals(PaintTool.SELECT,canvas.tool)
        val selection=doc.selection!!;assertTrue(selection.floating)
        assertEquals(480,selection.image.width);assertEquals(240,selection.image.height)
        val tl=canvas.toScreen(selection.rect.left,selection.rect.top)
        val br=canvas.toScreen(selection.rect.right,selection.rect.bottom)
        assertTrue(tl.x>0 && tl.y>0);assertTrue(br.x<canvas.width && br.y<canvas.height)
        click("selection_fit_canvas")
        assertTrue(selection.rect.right<=doc.bitmap.width && selection.rect.bottom<=doc.bitmap.height)
        assertEquals(480,selection.image.width)
        click("selection_original_size")
        assertEquals(480f,selection.rect.width(),0f);assertEquals(240f,selection.rect.height(),0f)
        assertEquals(Color.WHITE,doc.bitmap.getPixel(0,0))
        click("undo");assertNull(doc.selection);assertEquals(0,inkCount())
    }

    @Test fun unavailableColourConverterReportsErrorAndClearsBusyState() {
        val image=Bitmap.createBitmap(32,24,Bitmap.Config.ARGB_8888)
        image.eraseColor(Color.BLUE)
        provider.file.outputStream().use { assertTrue(image.compress(Bitmap.CompressFormat.JPEG,100,it)) };image.recycle()
        assertTrue("Exercise an actual profiled JPEG",provider.file.readBytes().toString(Charsets.ISO_8859_1).contains("ICC_PROFILE"))
        val previous=doc.bitmap
        menu("File",1);receive()
        assertSame(previous,doc.bitmap);assertEquals(0,inkCount())
        assertNotNull(activity.lastIoError);assertFalse(activity.busy)
        assertTrue(activity.lastIoError!!.contains(activity.getString(org.catrobat.paintroid.R.string.colour_converter_unavailable)))
    }
    @Test fun invalidImageLeavesCurrentCanvasAndShowsError() {
        provider.file.writeText("not an image")
        menu("File", 1); receive()
        assertNotNull(activity.lastIoError); assertEquals(96, doc.bitmap.width); assertFalse(doc.dirty)
    }
    @Test fun pngSaveButtonWritesActualImageToSelectedProvider() {
        doc.foreground = Color.RED; tool(PaintTool.BRUSH); drag(10f, 10f, 60f, 10f)
        click("save_image")
        receive()
        assertNull(activity.lastIoError); assertFalse(doc.dirty)
        val decoded = BitmapFactory.decodeFile(provider.file.path)
        assertEquals(96, decoded.width); assertEquals(Color.RED, decoded.getPixel(30, 10)); decoded.recycle()
    }
    @Test fun saveReusesSuccessfulSaveAsDestinationAndFormatWithoutAnotherPicker() {
        tool(PaintTool.PENCIL);doc.foreground=Color.RED;drag(10f,10f,50f,10f)
        menu("File",3)
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        EditorTestNavigation.format(dialog.window!!.decorView.findViewWithTag("export_format"),ImageFormat.BMP)
        receive();assertFalse(doc.dirty)
        assertTrue(provider.file.readBytes().take(2)==listOf('B'.code.toByte(),'M'.code.toByte()))
        doc.foreground=Color.BLUE;drag(10f,30f,50f,30f)
        click("save_image");awaitIo()
        assertNull(shadowOf(activity).nextStartedActivityForResult);assertFalse(doc.dirty)
        val decoded=BitmapFactory.decodeFile(provider.file.path)
        assertEquals(Color.BLUE,decoded.getPixel(30,30));decoded.recycle()
        provider.denyWrite=true;doc.edited();click("save_image");awaitIo()
        assertTrue(doc.dirty);assertNotNull(activity.lastIoError)
    }
    @Test fun recoveredDraftRetainsSaveAsUriAndCancelledSaveAsDoesNotReplaceIt() {
        click("save_image");receive()
        controller.pause().stop();awaitIo();controller.destroy()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get()
        shadowOf(Looper.getMainLooper()).idle()
        menu("File",3);EditorTestNavigation.chooseLocationIfShown();receive(Activity.RESULT_CANCELED)
        doc.bitmap.setPixel(7,9,Color.MAGENTA);doc.edited()
        click("save_image");awaitIo()
        assertNull(shadowOf(activity).nextStartedActivityForResult);assertFalse(doc.dirty)
        val saved=BitmapFactory.decodeFile(provider.file.path)
        assertEquals(Color.MAGENTA,saved.getPixel(7,9));saved.recycle()
    }
    @Test fun restartingPreservesForegroundAndBackgroundIncludingAnExplicitWhiteForeground() {
        for((hex,colour) in listOf("000000" to Color.BLACK,"FF0000" to Color.RED,"FFFFFF" to Color.WHITE)) {
            click("colour_$hex")
            activity.window.decorView.findViewWithTag<View>("colour_0000FF").performLongClick()
            controller.pause().stop();awaitIo();controller.destroy()
            controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get()
            shadowOf(Looper.getMainLooper()).idle()
            assertEquals("Saved foreground must not swap with the background",colour,doc.foreground)
            assertEquals(Color.BLUE,doc.background)
        }
    }

    @Test fun legacyDraftWithoutColourMetadataDefaultsToBlackForegroundAndWhiteBackground() {
        val context=activity.applicationContext
        controller.pause().stop();awaitIo();controller.destroy()
        val image=Bitmap.createBitmap(24,24,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.WHITE)}
        AutosaveStore(context.filesDir).write(image,null,org.json.JSONObject().put("version",1))
        image.recycle()
        controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);activity=controller.setup().get()
        shadowOf(Looper.getMainLooper()).idle()
        assertEquals(Color.BLACK,doc.foreground);assertEquals(Color.WHITE,doc.background)
    }

    @Test fun failedSaveKeepsUnsavedChanges() {
        tool(PaintTool.PENCIL); drag(10f, 10f, 50f, 10f)
        provider.denyWrite = true
        click("save_image"); receive()
        assertTrue(doc.dirty); assertNotNull(activity.lastIoError)
    }
    @Test fun cancellingSaveBeforeOpenDoesNotDiscardTheCurrentDrawing() {
        tool(PaintTool.PENCIL); drag(10f, 10f, 60f, 10f)
        val count = inkCount()
        menu("File", 1)
        (ShadowAlertDialog.getLatestAlertDialog() as AlertDialog).getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        shadowOf(Looper.getMainLooper()).idle()
        receive(Activity.RESULT_CANCELED)
        assertNull(shadowOf(activity).nextStartedActivityForResult)
        assertEquals(count, inkCount()); assertTrue(doc.dirty)
    }
    @Test fun successfulSaveBeforeOpenInvokesLoadPickerOnlyAfterSaving() {
        tool(PaintTool.PENCIL); drag(10f, 10f, 60f, 10f)
        menu("File", 1)
        (ShadowAlertDialog.getLatestAlertDialog() as AlertDialog).getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        shadowOf(Looper.getMainLooper()).idle()
        receive()
        val open = shadowOf(activity).nextStartedActivityForResult
        assertNotNull(open); assertEquals(ClassicPaintActivity.OPEN_IMAGE, open.requestCode)
        assertTrue(provider.file.length() > 0); assertFalse(doc.dirty)
        assertTrue(inkCount() > 0)
    }
    @Test fun sourceExportMenuWritesTheBundledSourceZip() {
        menu("File", 8); (ShadowAlertDialog.getLatestAlertDialog() as AlertDialog).listView.performItemClick(null,3,3); receive()
        assertNull(activity.lastIoError)
        assertArrayEquals(activity.assets.open(ClassicPaintActivity.SOURCE_ASSET).use { it.readBytes() }, provider.file.readBytes())
    }
    @Test fun eraserUsesOpaqueBackgroundInMainEditor() {
        doc.bitmap.eraseColor(Color.BLUE); doc.background = Color.TRANSPARENT
        tool(PaintTool.ERASER); doc.strokeWidth = 8f; drag(10f, 10f, 60f, 10f)
        assertEquals(Color.BLACK,doc.bitmap.getPixel(30,10))
        click("undo"); assertEquals(Color.BLUE, doc.bitmap.getPixel(30, 10))
    }
    @Test fun everyCurrentToolAndMenuHasAnActiveControl() {
        assertEquals(20, PaintTool.values().size)
        PaintTool.values().forEach { tool(it) }
        for (name in listOf("View","Draw","File","Edit","Color")) {
            click("menu_$name");assertTrue(activity.window.decorView.findViewWithTag<View>("tab_panel_host").isShown)
        }
    }
    @Test fun clipboardIsAdjacentToUndoRedoAndAllToolsHaveVisibleLabels() {
        val row=activity.window.decorView.findViewWithTag<ViewGroup>("quick_actions")
        assertEquals(listOf("undo","redo","clipboard_cut","clipboard_copy","clipboard_paste","save_image"),(0 until row.childCount).map {row.getChildAt(it).tag})
        for(type in PaintTool.values()) {
            tool(type)
            val button=activity.window.decorView.findViewWithTag<android.widget.Button>("tool_${type.name}")
            assertEquals(type.label,button.text.toString());assertTrue(button.text.isNotBlank())
        }
    }
    @Test fun leftPanelCutCopyPasteAndTopUndoRedoEditTheActualSelection() {
        Canvas(doc.bitmap).drawRect(10f, 10f, 30f, 30f, Paint().apply { color = Color.BLUE })
        tool(PaintTool.SELECT); drag(10f, 10f, 30f, 30f)
        click("clipboard_copy"); assertNotNull(doc.clipboard)
        click("clipboard_cut"); assertEquals(Color.WHITE, doc.bitmap.getPixel(15, 15))
        click("clipboard_paste"); drag(10f, 10f, 50f, 50f); click("apply")
        assertEquals(Color.BLUE, doc.bitmap.getPixel(50, 50))
        click("undo"); assertEquals(Color.WHITE, doc.bitmap.getPixel(50, 50))
        click("undo"); assertEquals(Color.BLUE, doc.bitmap.getPixel(15, 15))
        click("redo"); assertEquals(Color.WHITE, doc.bitmap.getPixel(15, 15))
    }
    @Test fun fullResolutionScreenshotSurvivesOpenDrawUndoRedoAndPngExport() {
        val source = Bitmap.createBitmap(1644, 3840, Bitmap.Config.ARGB_8888).apply {
            eraseColor(Color.WHITE); setPixel(0, 0, Color.RED); setPixel(1643, 3839, Color.BLUE)
            for (x in 1500..1599) setPixel(x, 3799, if (x % 2 == 0) Color.BLACK else Color.YELLOW)
        }
        provider.file.outputStream().use { source.compress(Bitmap.CompressFormat.PNG, 100, it) }; source.recycle()
        menu("File", 1); receive()
        assertNull(activity.lastIoError)
        assertEquals(1644, doc.bitmap.width); assertEquals(3840, doc.bitmap.height)
        assertEquals(Color.BLUE, doc.bitmap.getPixel(1643, 3839))
        assertEquals(Color.BLACK, doc.bitmap.getPixel(1500, 3799)); assertEquals(Color.YELLOW, doc.bitmap.getPixel(1501, 3799))
        val fullBitmap = doc.bitmap
        tool(PaintTool.BRUSH); doc.foreground = Color.GREEN; doc.strokeWidth = 6f
        drag(1600f, 3800f, 1620f, 3800f)
        assertEquals(Color.GREEN, doc.bitmap.getPixel(1610, 3800))
        click("undo"); assertSame(fullBitmap, doc.bitmap); assertEquals(Color.WHITE, doc.bitmap.getPixel(1610, 3800))
        click("redo"); assertSame(fullBitmap, doc.bitmap); assertEquals(Color.GREEN, doc.bitmap.getPixel(1610, 3800))
        click("save_image"); receive()
        val output = BitmapFactory.decodeFile(provider.file.path)
        assertEquals(1644, output.width); assertEquals(3840, output.height)
        assertEquals(Color.GREEN, output.getPixel(1610, 3800)); assertEquals(Color.BLUE, output.getPixel(1643, 3839))
        assertEquals(Color.BLACK, output.getPixel(1500, 3799)); assertEquals(Color.YELLOW, output.getPixel(1501, 3799)); output.recycle()
    }
    @Test fun imageLongerThan8192PixelsLoadsWithoutResizing() {
        val source = Bitmap.createBitmap(17, 10000, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.CYAN); setPixel(16, 9999, Color.RED) }
        provider.file.outputStream().use { source.compress(Bitmap.CompressFormat.PNG, 100, it) }; source.recycle()
        menu("File", 1); receive()
        assertNull(activity.lastIoError); assertEquals(17, doc.bitmap.width); assertEquals(10000, doc.bitmap.height)
        assertEquals(Color.RED, doc.bitmap.getPixel(16, 9999))
    }
    @Test fun twelveMegapixelFillRunsInBackgroundAndPreservesEnclosedPixels() {
        doc.newImage(4000, 3000); canvas.fit()
        val p = Paint().apply { color = Color.BLACK; style = Paint.Style.STROKE; strokeWidth = 2f }
        Canvas(doc.bitmap).drawRect(1000f, 1000f, 1500f, 1500f, p)
        tool(PaintTool.FILL); doc.foreground = Color.GREEN
        event(MotionEvent.ACTION_DOWN, 100f, 100f); event(MotionEvent.ACTION_UP, 100f, 100f)
        assertTrue("Large bucket fills must not block the UI thread", activity.busy)
        awaitIo()
        assertEquals(Color.GREEN, doc.bitmap.getPixel(3999, 2999)); assertEquals(Color.WHITE, doc.bitmap.getPixel(1200, 1200))
        click("undo"); assertEquals(Color.WHITE, doc.bitmap.getPixel(3999, 2999))
        click("redo"); assertEquals(Color.GREEN, doc.bitmap.getPixel(3999, 2999))
        assertEquals(4000, doc.bitmap.width); assertEquals(3000, doc.bitmap.height)
    }
    @Test fun newCanvasAndResizeAcceptDimensionsAbovePreviousLimits() {
        doc.newImage(4000, 3000)
        doc.bitmap.setPixel(3999, 2999, Color.BLUE)
        doc.resize(4000, 3100, false)
        assertEquals(Color.BLUE, doc.bitmap.getPixel(3999, 2999))
        doc.undo(); assertEquals(4000, doc.bitmap.width); assertEquals(3000, doc.bitmap.height)
        doc.newImage(10000, 17); assertEquals(10000, doc.bitmap.width)
    }
    @Test fun pencilBrushAndEraserChangePixelsWithUndoAndRedo() {
        tool(PaintTool.PENCIL); drag(10f, 10f, 60f, 10f)
        assertTrue(inkCount() >= 40); click("undo"); assertEquals(0, inkCount()); click("redo"); assertTrue(inkCount() >= 40)
        tool(PaintTool.BRUSH); doc.foreground = Color.RED; doc.strokeWidth = 10f; drag(10f, 20f, 60f, 20f)
        assertEquals(Color.RED, doc.bitmap.getPixel(30, 20))
        tool(PaintTool.ERASER); drag(10f, 20f, 60f, 20f); assertEquals(Color.WHITE, doc.bitmap.getPixel(30, 20))
    }
    @Test fun bucketFillsOnlyEnclosedRegionAndEyedropperSamplesIt() {
        tool(PaintTool.RECTANGLE); doc.strokeWidth = 2f; drag(15f, 15f, 65f, 65f)
        tool(PaintTool.FILL); doc.foreground = Color.GREEN; tap(30f, 30f)
        assertEquals(Color.GREEN, doc.bitmap.getPixel(30, 30)); assertEquals(Color.WHITE, doc.bitmap.getPixel(5, 5))
        doc.foreground = Color.RED; tool(PaintTool.PICKER); tap(30f, 30f); assertEquals(Color.GREEN, doc.foreground)
    }
    @Test fun airbrushMakesPixelsAndOneUndoRemovesGesture() {
        tool(PaintTool.SPRAY); drag(20f, 20f, 45f, 45f); assertTrue(inkCount() > 0)
        click("undo"); assertEquals(0, inkCount())
    }
    @Test fun lineAndTwoBendCurveCommitAsSeparateUndoSteps() {
        tool(PaintTool.LINE); drag(10f, 10f, 70f, 10f); val lineInk = inkCount()
        tool(PaintTool.CURVE); drag(10f, 30f, 80f, 30f)
        drag(25f, 30f, 25f, 75f); drag(65f, 30f, 65f, 75f)
        assertTrue(inkCount() > lineInk + 30)
        assertTrue((45..70).any { y -> (20..75).any { x -> doc.bitmap.getPixel(x, y) != Color.WHITE } })
        click("undo"); assertEquals(lineInk, inkCount())
    }
    @Test fun polygonClosesAndAllThreeShapeTypesRenderTheirGeometry() {
        tool(PaintTool.POLYGON); doc.shapeStyle = 1
        tap(15f, 15f); tap(75f, 15f); tap(45f, 70f); click("apply")
        assertEquals(Color.BLACK, doc.bitmap.getPixel(45, 35)); assertEquals(Color.WHITE, doc.bitmap.getPixel(17, 65))
        for (shape in listOf(PaintTool.RECTANGLE, PaintTool.ELLIPSE, PaintTool.ROUND_RECT)) {
            doc.newImage(96, 96); tool(shape); doc.shapeStyle = 1; drag(15f, 15f, 75f, 75f)
            assertEquals(shape.label, Color.BLACK, doc.bitmap.getPixel(45, 45))
            if (shape != PaintTool.RECTANGLE) assertEquals(shape.label, Color.WHITE, doc.bitmap.getPixel(15, 15))
        }
    }
    @Test fun rectangularSelectionMovesAndUndoRestoresOriginal() {
        Canvas(doc.bitmap).drawRect(10f, 10f, 30f, 30f, Paint().apply { color = Color.BLUE })
        tool(PaintTool.SELECT); drag(10f, 10f, 30f, 30f); drag(20f, 20f, 50f, 50f); click("apply")
        assertEquals(Color.WHITE, doc.bitmap.getPixel(15, 15)); assertEquals(Color.BLUE, doc.bitmap.getPixel(45, 45))
        click("undo"); assertEquals(Color.BLUE, doc.bitmap.getPixel(15, 15)); assertEquals(Color.WHITE, doc.bitmap.getPixel(45, 45))
    }
    @Test fun freeFormSelectionAndInsertedImagesCompositeThroughTheirMasks() {
        doc.bitmap.eraseColor(Color.RED)
        tool(PaintTool.LASSO)
        event(MotionEvent.ACTION_DOWN, 10f, 10f); event(MotionEvent.ACTION_MOVE, 60f, 10f); event(MotionEvent.ACTION_MOVE, 10f, 60f); event(MotionEvent.ACTION_UP, 10f, 10f)
        assertNotNull(doc.selection); assertTrue(doc.cutSelection())
        assertEquals(Color.WHITE, doc.bitmap.getPixel(20, 20)); assertEquals(Color.RED, doc.bitmap.getPixel(55, 55))
        assertTrue(doc.paste()); click("apply"); assertEquals(Color.RED, doc.bitmap.getPixel(10, 10))
        doc.bitmap.eraseColor(Color.GREEN)
        val pasted = Bitmap.createBitmap(20, 20, Bitmap.Config.ARGB_8888).apply { eraseColor(Color.WHITE); setPixel(10, 10, Color.BLUE) }
        pasted.setPixel(2, 2, Color.TRANSPARENT)
        doc.paste(pasted); click("apply")
        assertEquals(Color.GREEN, doc.bitmap.getPixel(2, 2)); assertEquals(Color.BLUE, doc.bitmap.getPixel(10, 10))
        assertFalse(doc.bitmap.hasAlpha()); pasted.recycle()
    }
    @Test fun textToolDialogPlacesTextAndCanBeUndone() {
        tool(PaintTool.TEXT); tap(5f, 5f)
        val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val edits = mutableListOf<EditText>()
        fun collect(view: View) { if (view is EditText) edits.add(view); if (view is ViewGroup) for (i in 0 until view.childCount) collect(view.getChildAt(i)) }
        collect(dialog.window!!.decorView)
        edits.first().setText("Paint")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertTrue(inkCount() > 20); click("undo"); assertEquals(0, inkCount())
    }
    @Test fun navigatePansWithoutTapZoomAndScrollbarsChangeViewport() {
        tool(PaintTool.ZOOM); val before = canvas.zoom; tap(48f, 48f); assertEquals(before,canvas.zoom,.0001f)
        canvas.zoomAt(12f)
        val old = canvas.panX
        val event = MotionEvent.obtain(0, 0, MotionEvent.ACTION_DOWN, canvas.width * .8f, canvas.height - 2f, 0)
        canvas.dispatchTouchEvent(event); event.recycle()
        assertTrue(old != canvas.panX)
        canvas.fit(); assertTrue(canvas.zoom < 12f)
    }
    @Test fun paletteForegroundBackgroundAndImageTransformMenusWork() {
        click("colour_FF0000"); assertEquals(Color.RED, doc.foreground)
        activity.window.decorView.findViewWithTag<View>("colour_00FF00").performLongClick(); assertEquals(Color.GREEN, doc.background)
        click("swap_colours"); assertEquals(Color.GREEN, doc.foreground); assertEquals(Color.RED, doc.background)
        doc.bitmap.setPixel(2, 3, Color.BLUE)
        menu("Edit", 6); assertEquals(Color.BLUE, doc.bitmap.getPixel(93, 3))
        click("undo"); assertEquals(Color.BLUE, doc.bitmap.getPixel(2, 3))
        doc.resize(48, 96, false); assertEquals(48, doc.bitmap.width); assertEquals(Color.BLUE, doc.bitmap.getPixel(2, 3))
    }
    @Test fun legalNoticesAndActualCorrespondingSourceAreAvailableOffline() {
        val text = LegalInfo.aboutText(activity)
        assertTrue(text.contains("The Catrobat Team")); assertTrue(text.contains("modified distribution")); assertTrue(text.contains("WITHOUT ANY WARRANTY"))
        assertTrue(activity.assets.open("legal/AGPL-3.0.txt").bufferedReader().readText().contains("GNU AFFERO GENERAL PUBLIC LICENSE"))
        assertTrue(activity.assets.open("legal/THIRD_PARTY_NOTICES.txt").bufferedReader().readText().contains("androidx.appcompat"))
        val paths = mutableSetOf<String>()
        ZipInputStream(activity.assets.open(ClassicPaintActivity.SOURCE_ASSET)).use { zip ->
            while (true) { val entry = zip.nextEntry ?: break; paths.add(entry.name) }
        }
        assertTrue(paths.any { it.endsWith("classic/PaintCanvas.kt") }); assertTrue(paths.any { it.endsWith("gradlew") })
        assertTrue(paths.none { it.endsWith(".keystore") || it.endsWith(".apk") })
    }
    @Test fun portraitInterfaceRenders() { render("classic-portrait.png") }
    @Test @Config(qualifiers = "w900dp-h412dp-land-xhdpi") fun landscapeInterfaceRenders() { render("classic-landscape.png") }
    private fun render(name: String) {
        val bar = (20 * activity.resources.displayMetrics.density).toInt()
        doc.newImage(canvas.width - bar - 24, canvas.height - bar - 24); canvas.fit()
        val view = activity.window.decorView
        val bitmap = Bitmap.createBitmap(view.width, view.height, Bitmap.Config.ARGB_8888)
        view.draw(Canvas(bitmap))
        val output = File("build/reports/classic-preview", name); output.parentFile.mkdirs()
        output.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it)) }; bitmap.recycle()
        assertTrue(output.length() > 1000)
    }

    class DocumentProvider : ContentProvider() {
        lateinit var file: File
        var reads = 0; var missingName = false; var denyWrite = false
        override fun onCreate() = true
        override fun getType(uri: Uri) = "application/octet-stream"
        override fun openFile(uri: Uri, mode: String): ParcelFileDescriptor {
            if (mode.contains('w')) {
                if (denyWrite) throw SecurityException("Provider is read-only")
                return ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_CREATE or ParcelFileDescriptor.MODE_READ_WRITE or ParcelFileDescriptor.MODE_TRUNCATE)
            }
            reads++; return ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
        }
        override fun query(uri: Uri, projection: Array<out String>?, selection: String?, args: Array<out String>?, order: String?): Cursor =
            if (missingName) MatrixCursor(arrayOf("unknown")).apply { addRow(arrayOf("value")) }
            else MatrixCursor(arrayOf(OpenableColumns.DISPLAY_NAME)).apply { addRow(arrayOf("fixture.png")) }
        override fun insert(uri: Uri, values: ContentValues?): Uri? = null
        override fun update(uri: Uri, values: ContentValues?, selection: String?, args: Array<out String>?) = 0
        override fun delete(uri: Uri, selection: String?, args: Array<out String>?) = 0
    }
}
