/* AN Paint regression checks, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

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
import android.provider.DocumentsContract
import android.provider.OpenableColumns
import android.view.DragEvent
import android.view.View
import android.widget.EditText
import android.widget.Spinner
import org.catrobat.paintroid.classic.*
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
import org.robolectric.util.ReflectionHelpers
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33],shadows = [PixelRegionDecoderShadow::class],qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class AssemblyActivityTest {
    private lateinit var controller: ActivityController<AssemblyActivity>
    private lateinit var activity: AssemblyActivity
    private lateinit var provider: Provider
    @Before fun start() {
        val context=RuntimeEnvironment.getApplication() as Context
        File(context.filesDir,"image-assembly").deleteRecursively(); File(context.filesDir,"classic-recovery.png").delete();File(context.filesDir,"classic-autosave.zip").delete();File(context.filesDir,"classic-autosave.zip.bak").delete();context.getSharedPreferences("classic-ui",Context.MODE_PRIVATE).edit().clear().commit()
        provider=Provider().apply { attachInfo(context,ProviderInfo().apply { authority="assembly.fixture" }) }
        ShadowContentResolver.registerProviderInternal("assembly.fixture",provider)
        controller=Robolectric.buildActivity(AssemblyActivity::class.java); activity=controller.setup().get(); idle()
    }
    @After fun stop() { ShadowAlertDialog.getLatestAlertDialog()?.dismiss(); waitForWork(); if (!activity.isDestroyed) controller.pause().stop().destroy() }
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    private fun waitForWork() {
        val end=System.nanoTime()+15_000_000_000L
        while (activity.busy && System.nanoTime()<end) { idle(); Thread.sleep(10) }; idle(); assertFalse(activity.lastError,activity.busy)
    }
    private fun click(tag: String) { assertTrue(activity.window.decorView.findViewWithTag<View>(tag).performClick()); idle() }
    private fun load(count: Int = 3) {
        repeat(count) { i ->
            val name=listOf("b.png","a.png","c.png").getOrElse(i) { "image-$i.png" }
            val w=listOf(24,12,18).getOrElse(i) { 10 }; val h=listOf(16,20,8).getOrElse(i) { 10 }
            val image=Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888); image.eraseColor(listOf(Color.RED,Color.GREEN,Color.BLUE).getOrElse(i) { Color.MAGENTA })
            val file=File(activity.cacheDir,"input-$i.png"); file.outputStream().use { image.compress(Bitmap.CompressFormat.PNG,100,it) }; image.recycle()
            provider.files["$i"]=Record(file,name,listOf(0L,2L,1L).getOrNull(i)?.let { java.time.Instant.parse("2026-09-05T12:00:00Z").toEpochMilli()+it*86400000 })
        }
        click("assembly_add"); val launch=shadowOf(activity).nextStartedActivityForResult
        assertEquals(Intent.ACTION_OPEN_DOCUMENT,launch.intent.action); assertTrue(launch.intent.getBooleanExtra(Intent.EXTRA_ALLOW_MULTIPLE,false))
        val clip=ClipData.newUri(activity.contentResolver,"images",Uri.parse("content://assembly.fixture/0"))
        for (i in 1 until count) clip.addItem(ClipData.Item(Uri.parse("content://assembly.fixture/$i")))
        shadowOf(activity).receiveResult(launch.intent,Activity.RESULT_OK,Intent().apply { clipData=clip }); waitForWork()
    }
    private fun image(name: String) = activity.assembly.images.first { it.name == name }
    private fun drag(id: String,x: Float,y: Float) {
        val view=activity.window.decorView.findViewWithTag<View>("assembly_item_$id")
        assertTrue(view.performLongClick())
        fun event(action: Int,x: Float = 0f,y: Float = 0f): DragEvent {
            val e=ReflectionHelpers.callStaticMethod<DragEvent>(DragEvent::class.java,"obtain")
            ReflectionHelpers.setField(e,"mAction",action); ReflectionHelpers.setField(e,"mX",x); ReflectionHelpers.setField(e,"mY",y); ReflectionHelpers.setField(e,"mLocalState",id)
            return e
        }
        assertTrue(activity.board.dispatchDragEvent(event(DragEvent.ACTION_DRAG_STARTED)))
        val point=activity.board.toScreen(x,y)
        assertTrue(activity.board.dispatchDragEvent(event(DragEvent.ACTION_DRAG_LOCATION,point.x,point.y)))
        assertNotNull(activity.board.ghost)
        assertTrue(activity.board.dispatchDragEvent(event(DragEvent.ACTION_DROP,point.x,point.y)))
        activity.board.dispatchDragEvent(event(DragEvent.ACTION_DRAG_ENDED)); idle()
    }
    private fun placeThree() { drag(image("b.png").id,0f,0f); drag(image("a.png").id,24f,0f); drag(image("c.png").id,0f,16f) }
    @Test fun multiPickerLoadsNamesTimesAndThumbnailsThenNativeDragEventsSnapBothDirections() {
        load(); assertEquals(3,activity.assembly.images.size); assertEquals(3,provider.reads)
        val tray=activity.window.decorView.findViewWithTag<android.view.ViewGroup>("assembly_thumbnails")
        assertEquals(3,tray.childCount); assertEquals("assembly_item_${image("a.png").id}",tray.getChildAt(0).tag)
        activity.window.decorView.findViewWithTag<Spinner>("assembly_sort").setSelection(AssemblySort.OLDEST.ordinal); idle()
        assertEquals("assembly_item_${image("b.png").id}",tray.getChildAt(0).tag)
        placeThree()
        assertEquals(Rect(24,0,36,20),activity.assembly.layout()[image("a.png").id]); assertEquals(Rect(0,16,18,24),activity.assembly.layout()[image("c.png").id])
        render(activity.window.decorView,"assembly-portrait.png")
    }
    @Test @Config(qualifiers = "w900dp-h412dp-land-xhdpi") fun landscapeTrayAndWorkspaceRemainReachable() {
        load(); placeThree(); render(activity.window.decorView,"assembly-landscape.png")
        assertTrue(activity.window.decorView.findViewWithTag<View>("assembly_crop").isShown)
        assertTrue(activity.window.decorView.findViewWithTag<View>("assembly_tray").isShown); assertTrue(activity.board.height > 100)
    }
    @Test fun individualAndBatchCropUsePercentAndAreUndoableBeforePlacement() {
        load(); click("assembly_item_${image("b.png").id}"); click("assembly_crop")
        var dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        dialog.window!!.decorView.findViewWithTag<View>("crop_percent").performClick()
        dialog.window!!.decorView.findViewWithTag<EditText>("crop_left").setText("25")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
        assertEquals(Rect(6,0,24,16),image("b.png").crop); assertTrue(activity.assembly.layout().isEmpty())
        click("assembly_batch_crop"); dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        dialog.window!!.decorView.findViewWithTag<View>("crop_percent").performClick()
        dialog.window!!.decorView.findViewWithTag<EditText>("crop_top").setText("25")
        render(dialog.window!!.decorView,"assembly-batch-crop.png")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
        assertEquals(Rect(0,4,24,16),image("b.png").crop); assertEquals(Rect(0,5,12,20),image("a.png").crop); assertEquals(Rect(0,2,18,8),image("c.png").crop)
        click("assembly_undo"); assertEquals(Rect(6,0,24,16),image("b.png").crop); assertEquals(Rect(0,0,12,20),image("a.png").crop)
        click("assembly_redo"); assertEquals(Rect(0,4,24,16),image("b.png").crop)
    }
    @Test fun savePngStreamsExactCompositeAndCancelRemovesOnlyTemporaryOutput() {
        load(); placeThree(); val originals=provider.files.mapValues { it.value.file.readBytes() }
        click("assembly_save"); waitForWork(); val launch=shadowOf(activity).nextStartedActivityForResult
        assertEquals(Intent.ACTION_CREATE_DOCUMENT,launch.intent.action); assertEquals("image/png",launch.intent.type)
        val output=File(activity.cacheDir,"assembly-export.png"); provider.files["out"]=Record(output,"out.png",null)
        shadowOf(activity).receiveResult(launch.intent,Activity.RESULT_OK,Intent().setData(Uri.parse("content://assembly.fixture/out"))); waitForWork()
        val bitmap=BitmapFactory.decodeFile(output.path)
        assertEquals(36,bitmap.width); assertEquals(24,bitmap.height)
        assertEquals(Color.RED,bitmap.getPixel(23,15)); assertEquals(Color.GREEN,bitmap.getPixel(24,15)); assertEquals(Color.BLUE,bitmap.getPixel(17,16)); assertEquals(Color.WHITE,bitmap.getPixel(35,23)); bitmap.recycle()
        originals.forEach { (id,bytes) -> assertArrayEquals(bytes,provider.files.getValue(id).file.readBytes()) }
        click("assembly_save"); waitForWork(); val cancelled=shadowOf(activity).nextStartedActivityForResult
        shadowOf(activity).receiveResult(cancelled.intent,Activity.RESULT_CANCELED,null); waitForWork()
        assertTrue(activity.filesDir.listFiles()!!.none { it.name.startsWith("assembly-output-") }); assertEquals(3,activity.assembly.layout().size)
    }
    @Test fun editInPaintTransfersCompositeAndMainUndoRestoresPreviousCanvas() {
        load(); placeThree(); click("assembly_edit"); waitForWork()
        assertEquals(Activity.RESULT_OK,shadowOf(activity).resultCode)
        val result=shadowOf(activity).resultIntent
        assertNotNull(result.getStringExtra("assembly_output"))
        val mainController=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val main=mainController.setup().get(); main.document.newImage(5,7); main.document.bitmap.setPixel(2,3,Color.MAGENTA)
        main.onActivityResult(ClassicPaintActivity.ASSEMBLY_IMAGE,Activity.RESULT_OK,result)
        val end=System.nanoTime()+10_000_000_000L
        while (main.busy && System.nanoTime()<end) { idle(); Thread.sleep(10) }; idle()
        assertNull(main.lastIoError); assertEquals(36,main.document.bitmap.width); assertEquals(24,main.document.bitmap.height); assertEquals(Color.GREEN,main.document.bitmap.getPixel(30,5))
        main.document.undo(); assertEquals(5,main.document.bitmap.width); assertEquals(7,main.document.bitmap.height); assertEquals(Color.MAGENTA,main.document.bitmap.getPixel(2,3))
        assertFalse(File(main.filesDir,result.getStringExtra("assembly_output")!!).exists())
        mainController.pause().stop(); val stopEnd=System.nanoTime()+10_000_000_000L
        while (main.busy && System.nanoTime()<stopEnd) { idle(); Thread.sleep(10) }; mainController.destroy()
    }
    @Test @Config(sdk = [28]) fun twentyImagesLoadAndAnOversizedPickerBatchIsRejectedBeforeReading() {
        load(20); assertEquals(20,activity.assembly.images.size); assertEquals(20,provider.reads); assertTrue(activity.assembly.layout().isEmpty())
        val before=provider.reads
        activity.onActivityResult(AssemblyActivity.ADD_IMAGES,Activity.RESULT_OK,Intent().setData(Uri.parse("content://assembly.fixture/0")))
        assertEquals(before,provider.reads); assertEquals(20,activity.assembly.images.size); assertTrue(activity.lastError!!.contains("Select fewer"))
    }
    @Test fun reopeningAssemblyRestoresOriginalFilesCropsAndAttachments() {
        load(); placeThree(); val original=activity.assembly.layout()
        controller.pause().stop().destroy()
        controller=Robolectric.buildActivity(AssemblyActivity::class.java); activity=controller.setup().get(); waitForWork()
        assertEquals(3,activity.assembly.images.size); assertEquals(original,activity.assembly.layout())
        assertEquals(3,provider.reads)
    }
    @Test fun cropTouchHandlesKeepTrackingAcrossMovesAndPixelPercentChoiceIsVisible() {
        load(); click("assembly_item_${image("b.png").id}"); click("assembly_crop")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog; val root=dialog.window!!.decorView
        val preview=root.findViewWithTag<CropPreview>("crop_preview"); idle()
        val pad=14*activity.resources.displayMetrics.density
        val scale=minOf((preview.width-2*pad)/24,(preview.height-2*pad)/16)
        val x=(preview.width-24*scale)/2; val y=(preview.height-16*scale)/2
        for ((action,p) in listOf(android.view.MotionEvent.ACTION_DOWN to PointF(x,y),android.view.MotionEvent.ACTION_MOVE to PointF(x+3*scale,y+2*scale),android.view.MotionEvent.ACTION_UP to PointF(x+6*scale,y+4*scale))) {
            val event=android.view.MotionEvent.obtain(0,20,action,p.x,p.y,0); assertTrue(preview.dispatchTouchEvent(event)); event.recycle()
        }
        assertEquals("6",root.findViewWithTag<EditText>("crop_left").text.toString()); assertEquals("4",root.findViewWithTag<EditText>("crop_top").text.toString())
        root.findViewWithTag<View>("crop_percent").performClick()
        assertTrue(root.findViewWithTag<android.widget.RadioButton>("crop_percent").isChecked); assertFalse(root.findViewWithTag<android.widget.RadioButton>("crop_pixels").isChecked)
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); assertEquals(Rect(6,4,24,16),image("b.png").crop)
    }

    @Test fun sameWidthAndHeightOfferPercentPreserveRatiosAndUndoWithoutChangingSources() {
        load(); click("assembly_same_width")
        var dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        dialog.window!!.decorView.findViewWithTag<View>("normalize_percent").performClick()
        dialog.window!!.decorView.findViewWithTag<EditText>("normalize_value").setText("50")
        render(dialog.window!!.decorView,"assembly-normalize.png")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
        assertTrue(activity.assembly.images.all { it.placedSize.width==12 }); assertEquals(ImageDimensions(12,8),image("b.png").placedSize)
        click("assembly_same_height"); dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        dialog.window!!.decorView.findViewWithTag<EditText>("normalize_value").setText("10")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
        assertTrue(activity.assembly.images.all { it.placedSize.height==10 }); assertEquals(ImageDimensions(15,10),image("b.png").placedSize)
        click("assembly_undo"); assertTrue(activity.assembly.images.all { it.placedSize.width==12 })
        click("assembly_same_width"); dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        dialog.window!!.decorView.findViewWithTag<View>("normalize_reset").performClick(); idle()
        assertTrue(activity.assembly.images.all { it.normalization==null })
        placeThree(); val dimensions=activity.assembly.size()
        assertEquals("Show all",activity.window.decorView.findViewWithTag<android.widget.Button>("assembly_fit").text.toString())
        click("assembly_fit"); assertEquals(dimensions,activity.assembly.size())
    }
    @Test fun unplaceButtonRemovesOnlySelectedRootAndPromotesRemainingImages() {
        load(); placeThree(); click("assembly_item_${image("b.png").id}"); click("assembly_unplace")
        assertEquals(2,activity.assembly.layout().size); assertNull(image("b.png").attachment)
        assertEquals(Rect(0,0,12,20),activity.assembly.layout()[image("a.png").id]); assertEquals(Rect(0,20,18,28),activity.assembly.layout()[image("c.png").id])
        click("assembly_undo"); assertEquals(3,activity.assembly.layout().size)
    }
    @Test fun placedImageCanBeDraggedByTouchWithVisibleSnappingAndCancelledSafely() {
        load(); placeThree(); val board=activity.board
        click("assembly_item_${image("a.png").id}")
        val from=board.toScreen(30f,10f); val to=board.toScreen(6f,34f)
        fun touch(action: Int,p: PointF) {
            val event=android.view.MotionEvent.obtain(0,20,action,p.x,p.y,0); assertTrue(board.dispatchTouchEvent(event)); event.recycle()
        }
        touch(android.view.MotionEvent.ACTION_DOWN,from); touch(android.view.MotionEvent.ACTION_MOVE,to)
        assertEquals(Rect(0,24,12,44),board.ghost!!.rect)
        render(activity.window.decorView,"assembly-drag.png")
        touch(android.view.MotionEvent.ACTION_UP,to); idle()
        assertEquals(Rect(0,24,12,44),activity.assembly.layout()[image("a.png").id]); assertEquals(3,activity.assembly.layout().size)
        val before=activity.assembly.layout(); val start=board.toScreen(6f,34f); val next=board.toScreen(30f,10f)
        touch(android.view.MotionEvent.ACTION_DOWN,start); touch(android.view.MotionEvent.ACTION_MOVE,next); touch(android.view.MotionEvent.ACTION_CANCEL,next)
        assertEquals(before,activity.assembly.layout()); assertNull(board.ghost)
    }
    private fun render(view: View,name: String) {
        idle()
        if (name.contains("crop")) {
            view.measure(View.MeasureSpec.makeMeasureSpec(760,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(1600,View.MeasureSpec.AT_MOST))
            view.layout(0,0,view.measuredWidth,view.measuredHeight)
        }
        assertTrue(view.width>0 && view.height>0)
        // Capture settled widget states, not the first frame of a radio animation.
        fun settle(v: View) {
            v.jumpDrawablesToCurrentState()
            if (v is android.view.ViewGroup) for (i in 0 until v.childCount) settle(v.getChildAt(i))
        }
        settle(view)
        val bitmap=Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888); view.draw(Canvas(bitmap))
        val file=File("build/reports/classic-preview",name); file.parentFile.mkdirs(); file.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it)) }; bitmap.recycle()
    }
    data class Record(val file: File,val name: String,val time: Long?)
    class Provider : ContentProvider() {
        val files=mutableMapOf<String,Record>(); var reads=0
        override fun onCreate()=true
        override fun getType(uri: Uri)="application/octet-stream"
        override fun openFile(uri: Uri,mode: String): ParcelFileDescriptor {
            val file=files.getValue(uri.lastPathSegment!!).file
            return if (mode.contains('w')) ParcelFileDescriptor.open(file,ParcelFileDescriptor.MODE_CREATE or ParcelFileDescriptor.MODE_READ_WRITE or ParcelFileDescriptor.MODE_TRUNCATE)
            else { reads++; ParcelFileDescriptor.open(file,ParcelFileDescriptor.MODE_READ_ONLY) }
        }
        override fun query(uri: Uri,projection: Array<out String>?,selection: String?,args: Array<out String>?,order: String?): Cursor {
            val record=files.getValue(uri.lastPathSegment!!)
            return MatrixCursor(arrayOf(OpenableColumns.DISPLAY_NAME,DocumentsContract.Document.COLUMN_LAST_MODIFIED)).apply { addRow(arrayOf(record.name,record.time)) }
        }
        override fun insert(uri: Uri,values: ContentValues?): Uri?=null
        override fun update(uri: Uri,values: ContentValues?,selection: String?,args: Array<out String>?)=0
        override fun delete(uri: Uri,selection: String?,args: Array<out String>?)=0
    }
}
