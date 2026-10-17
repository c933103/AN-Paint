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
import android.widget.TextView
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
        val main=mainController.setup().get();awaitEditorStartup(main); main.document.newImage(5,7); main.document.bitmap.setPixel(2,3,Color.MAGENTA)
        val credit=ImageCredit("https://example.org/previous.png","Previous canvas artwork — original author")
        main.document.paste(Bitmap.createBitmap(1,1,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.RED)},true,listOf(credit))
        main.document.finishSelection()
        main.onActivityResult(ClassicPaintActivity.ASSEMBLY_IMAGE,Activity.RESULT_OK,result)
        val end=System.nanoTime()+10_000_000_000L
        while (main.busy && System.nanoTime()<end) { idle(); Thread.sleep(10) }; idle()
        assertNull(main.lastIoError); assertEquals(36,main.document.bitmap.width); assertEquals(24,main.document.bitmap.height); assertEquals(Color.GREEN,main.document.bitmap.getPixel(30,5))
        assertTrue(main.document.imageCredits.isEmpty())
        main.document.undo(); assertEquals(5,main.document.bitmap.width); assertEquals(7,main.document.bitmap.height); assertEquals(Color.MAGENTA,main.document.bitmap.getPixel(2,3))
        assertEquals(listOf(credit),main.document.imageCredits)
        main.document.redo();assertTrue(main.document.imageCredits.isEmpty());assertEquals(Color.GREEN,main.document.bitmap.getPixel(30,5))
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
    private fun withLanguage(tag: String, block: () -> Unit) {
        val oldTag = AppLanguage.selectedTag(activity)
        val oldLocale = java.util.Locale.getDefault()
        try { AppLanguage.select(activity, if (tag == "en") "" else tag); AppLanguage.refresh(activity); block() }
        finally {
            AppLanguage.select(activity, oldTag)
            AppLanguage.refresh(activity)
            java.util.Locale.setDefault(oldLocale)
        }
    }

    @Test fun frenchHeaderTracksAddPlaceUnplaceAndRemoveIncludingOne() = withLanguage("fr") {
        val header = ReflectionHelpers.getField<android.widget.TextView>(activity, "count")
        fun checkCount(inputs: Int, placed: Int) = assertEquals(
            "AN Paint · Assemblage d’images\nImages : $inputs/20 · Images placées : $placed", header.text.toString())
        ReflectionHelpers.callInstanceMethod<Unit>(activity, "refresh"); checkCount(0, 0)
        load(2); checkCount(2, 0)
        drag(image("b.png").id, 0f, 0f); checkCount(2, 1)
        drag(image("a.png").id, 24f, 0f); checkCount(2, 2)
        click("assembly_item_${image("a.png").id}"); click("assembly_unplace"); checkCount(2, 1)
        click("assembly_remove"); checkCount(1, 1)
        click("assembly_item_${image("b.png").id}"); click("assembly_remove"); checkCount(0, 0)
    }

    @Test fun capacityRefusalUsesTrueRemainingCountBeforeReadingAndAcceptsAnExactFit() {
        load(17)
        for (tag in listOf("en", "en-001", "en-AU", "en-CA", "en-GB", "en-IN", "en-SG", "en-US", "en-XV", "fr")) withLanguage(tag) {
            for (remaining in listOf(3, 1, 0)) {
                // Reach each boundary through real loaded inputs, retaining the refusal branch.
                val target = 20 - remaining
                while (activity.assembly.images.size > target) activity.assembly.remove(activity.assembly.images.last().id)
                if (activity.assembly.images.size < target) load(target - activity.assembly.images.size)
                val clip = ClipData.newUri(activity.contentResolver, "images", Uri.parse("content://assembly.fixture/0"))
                repeat(remaining) { clip.addItem(ClipData.Item(Uri.parse("content://assembly.fixture/${it + 1}"))) }
                val reads = provider.reads
                activity.onActivityResult(AssemblyActivity.ADD_IMAGES, Activity.RESULT_OK, Intent().apply { clipData = clip })
                val expected = if (tag == "fr") "Nombre d’images pouvant encore être ajoutées : $remaining. Sélectionnez moins de fichiers."
                    else "Number of images you can still add: $remaining. Select fewer files."
                assertEquals(expected, activity.lastError)
                assertEquals(expected, shadowOf(ShadowAlertDialog.getLatestAlertDialog()).message.toString())
                assertEquals(reads, provider.reads)
                assertEquals(20 - remaining, activity.assembly.images.size)
                ShadowAlertDialog.getLatestAlertDialog().dismiss()
            }
        }
        activity.assembly.remove(activity.assembly.images.last().id)
        load(1); assertEquals(20, activity.assembly.images.size)
    }

    @Test fun renderingOneAndTwoImagesDisplaysEachActualProgressCallbackAndCreatesOutput() {
        load(2)
        for (tag in listOf("en", "en-001", "en-AU", "en-CA", "en-GB", "en-IN", "en-SG", "en-US", "en-XV", "fr")) withLanguage(tag) {
            for (item in activity.assembly.images) activity.assembly.unplace(item.id)
            for (total in 1..2) {
                val item = activity.assembly.images[total - 1]
                activity.assembly.place(item.id, Attachment(if (total == 1) null else activity.assembly.images[0].id,
                    if (total == 1) null else SnapEdge.RIGHT))
                val info = activity.window.decorView.findViewWithTag<android.widget.TextView>("assembly_status")
                val messages = mutableListOf<String>()
                val watcher = object : android.text.TextWatcher {
                    override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
                    override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) { messages += s.toString() }
                    override fun afterTextChanged(s: android.text.Editable?) = Unit
                }
                info.addTextChangedListener(watcher)
                click("assembly_save"); waitForWork()
                info.removeTextChangedListener(watcher)
                val expected = (1..total).map { if (tag == "fr") "Images traitées : $it / $total…" else "Images processed: $it / $total…" }
                assertEquals(expected, messages.filter { it.startsWith(if (tag == "fr") "Images traitées :" else "Images processed:") })
                val launch = shadowOf(activity).nextStartedActivityForResult
                assertEquals(Intent.ACTION_CREATE_DOCUMENT, launch.intent.action)
                val output = activity.filesDir.listFiles()!!.single { it.name.startsWith("assembly-output-") }
                val bitmap = BitmapFactory.decodeFile(output.path)
                assertNotNull(bitmap); assertEquals(Color.RED, bitmap.getPixel(0, 0)); bitmap.recycle()
                shadowOf(activity).receiveResult(launch.intent, Activity.RESULT_CANCELED, null); waitForWork()
                assertFalse(output.exists())
            }
        }
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
    @Test fun exactPositionMovesOnlySelectedImageAllowsOverlapAndSurvivesReopening() {
        load(); placeThree()
        val before=activity.assembly.layout(); val selected=image("a.png").id
        click("assembly_item_$selected"); click("assembly_position")
        var dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val root=dialog.window!!.decorView
        assertEquals("24",root.findViewWithTag<EditText>("assembly_position_x").text.toString())
        assertEquals("0",root.findViewWithTag<EditText>("assembly_position_y").text.toString())
        root.findViewWithTag<EditText>("assembly_position_x").setText("5")
        root.findViewWithTag<EditText>("assembly_position_y").setText("4")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
        assertFalse(dialog.isShowing)
        val expected=before.toMutableMap().apply { put(selected,Rect(5,4,17,24)) }
        assertEquals(expected,activity.assembly.layout()); assertEquals(ImagePosition(5,4),image("a.png").position)
        assertTrue(Rect.intersects(activity.assembly.layout().getValue(selected),activity.assembly.layout().getValue(image("b.png").id)))
        click("assembly_undo"); assertEquals(before,activity.assembly.layout())
        click("assembly_redo"); assertEquals(expected,activity.assembly.layout())
        controller.pause().stop().destroy()
        controller=Robolectric.buildActivity(AssemblyActivity::class.java); activity=controller.setup().get(); waitForWork()
        assertEquals(expected,activity.assembly.layout()); assertEquals(ImagePosition(5,4),image("a.png").position)
        assertEquals(3,provider.reads)
        click("assembly_item_$selected"); click("assembly_position")
        dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        assertEquals("5",dialog.window!!.decorView.findViewWithTag<EditText>("assembly_position_x").text.toString())
        assertEquals("4",dialog.window!!.decorView.findViewWithTag<EditText>("assembly_position_y").text.toString())
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
    }

    @Test fun invalidPositionAndCancelDoNotChangeImagesOrTheSavedProject() {
        load(); placeThree(); click("assembly_item_${image("a.png").id}")
        val before=activity.assembly.layout(); val saved=File(activity.assembly.directory,"project.json").readBytes()
        click("assembly_position")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog; val root=dialog.window!!.decorView
        val x=root.findViewWithTag<EditText>("assembly_position_x"); val y=root.findViewWithTag<EditText>("assembly_position_y")
        for ((left,top) in listOf("-1" to "0","1.5" to "0","0" to "","2147483648" to "0","2147483647" to "0")) {
            x.setText(left); y.setText(top); dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idle()
            assertTrue("$left,$top",dialog.isShowing)
            val error=root.findViewWithTag<TextView>("assembly_position_error")
            assertTrue(error.isShown); assertTrue(error.text.isNotBlank())
            assertEquals(before,activity.assembly.layout()); assertArrayEquals(saved,File(activity.assembly.directory,"project.json").readBytes())
        }
        x.setText("5"); y.setText("4"); dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
        assertFalse(dialog.isShowing); assertEquals(before,activity.assembly.layout())
        assertArrayEquals(saved,File(activity.assembly.directory,"project.json").readBytes())
    }

    @Test @Config(qualifiers = "w900dp-h412dp-land-xhdpi") fun positionDialogKeepsInputsAndActionsReachableInShortLandscape() {
        load(); click("assembly_item_${image("b.png").id}"); click("assembly_position")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        fun reachable(view: View) {
            assertTrue(view.width>0 && view.height>0)
            view.requestRectangleOnScreen(Rect(0,0,view.width,view.height),true); idle()
            val visible=Rect(); assertTrue(view.getGlobalVisibleRect(visible))
            assertEquals(view.height,visible.height())
        }
        for (tag in listOf("assembly_position_x","assembly_position_y")) reachable(dialog.window!!.decorView.findViewWithTag<View>(tag))
        reachable(dialog.getButton(AlertDialog.BUTTON_POSITIVE)); reachable(dialog.getButton(AlertDialog.BUTTON_NEGATIVE))
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
        assertTrue(activity.assembly.layout().isEmpty())
    }



    @Test fun frenchCompleteHelpAndActualDragStatusUseImageAttachmentLanguage() = withLanguage("fr") {
        click("assembly_help")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val expected="Ajoutez jusqu’à 20 images avec le sélecteur de fichiers d’Android. Le bac inférieur affiche les miniatures, les noms de fichiers, les dimensions des images après recadrage et après tout ajustement avec Même largeur ou Même hauteur et les dates de modification lorsqu’elles sont fournies par le fournisseur de fichiers. Triez par nom de fichier ou date de modification ; le tri ne réorganise pas les images placées.\n\nAppuyez sur une miniature pour la sélectionner. Recadrer l’image recadre cette image ; Recadrage par lot applique des marges en pixels ou en pourcentage aux images sélectionnées. Faites glisser les poignées de recadrage ou saisissez les valeurs. Réinitialiser le recadrage restaure les bords d’origine. Le recadrage est non destructif et peut être annulé.\n\nMaintenez une miniature appuyée, ou faites glisser une image déjà placée dans l’espace de travail, puis déposez-la sur un bord surligné. L’aperçu translucide montre le résultat exact de l’alignement. Une fixation à droite aligne les bords supérieurs ; une fixation en bas aligne les bords gauches. Vous pouvez aussi appuyer sur une miniature puis sur une cible +. La première image commence à l’origine. Les images rattachées peuvent se déplacer lorsque leur image parente est recadrée. Les chevauchements sont refusés.\n\nMême largeur et Même hauteur donnent à toutes les entrées une dimension commune tout en conservant le rapport hauteur/largeur propre à chaque image. Choisissez Pixels, Pourcentage, Plus petite ou Plus grande. Restaurer les tailles d’origine supprime la normalisation et conserve les recadrages.\n\nRetirer du placement renvoie uniquement l’image sélectionnée dans le bac. Les images suivantes comblent l’espace ; elles restent placées. Supprimer efface uniquement cette entrée. Annuler/Rétablir restaure ces modifications. Faites glisser une image placée pour la réorganiser ; faire glisser un espace vide déplace la vue. Pincez pour zoomer. Tout afficher ajuste le zoom pour montrer tout l’assemblage ; les dimensions de sortie ne changent jamais.\n\nEnregistrer PNG enregistre directement l’image assemblée. Modifier dans Paint la transfère dans l’éditeur principal comme remplacement annulable. Si la sortie dépasse la limite mémoire, choisissez une copie de sortie plus petite si cette option est proposée. Si même une sortie minuscule dépasse cette limite, l’application affiche un avertissement de mémoire au lieu d’un sélecteur de taille. Les fichiers source d’origine restent inchangés. L’assemblage actuel est enregistré localement et se rouvre à votre retour.\n\nCe mode utilise les mêmes crédits Catrobat/AGPL et de ressources que le panneau «Fichier > À propos, licences et remerciements» de l’éditeur principal."
        assertEquals(expected,dialog.findViewById<android.widget.TextView>(android.R.id.message).text.toString())
        dialog.dismiss()
        load(2);assertTrue(activity.board.beginImageDrag(image("b.png").id))
        assertEquals("Déposez sur un bord surligné : à droite avec les bords supérieurs alignés, ou en dessous avec les bords gauches alignés.",
            activity.window.decorView.findViewWithTag<android.widget.TextView>("assembly_status").text.toString())
    }

    @Test fun frenchActualBatchCropShowsCompleteWarningForZeroOneAndTwoSelectedImages() = withLanguage("fr") {
        load(2);click("assembly_batch_crop")
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val root=dialog.window!!.decorView
        fun check(count: Int) {
            val noun=if(count<=1) "image" else "images"
            assertEquals("Aperçu : 24 × 16 px\nAppliquer à $count $noun. Le recadrage des images placées peut déplacer les images qui leur sont rattachées.",
                root.findViewWithTag<android.widget.TextView>("crop_status").text.toString())
        }
        check(2);root.findViewWithTag<View>("crop_none").performClick();idle();check(0)
        (root.findViewWithTag<View>("crop_include_${image("b.png").id}") as android.widget.CheckBox).isChecked=true
        idle();check(1);root.findViewWithTag<View>("crop_all").performClick();idle();check(2)
        dialog.dismiss()
    }

    @Test fun everyEnglishOverrideAndFrenchQualifiesWholeCropQuantityMessages() {
        for(tag in listOf("en","en-001","en-AU","en-CA","en-GB","en-IN","en-SG","en-US","en-XV","fr","qaa-Zsye-XV")) withLanguage(tag) {
            val helpText=ui(org.catrobat.paintroid.R.string.ui_add_up_to_20_images_with_android_s)
            if(tag=="qaa-Zsye-XV") assertEquals("Complete emoji-English Help", "💾 Add up to 20 images with Android's file picker. The bottom tray shows thumbnails, filenames, image dimensions after cropping and any «↔️ Same width» or «↕️ Same height» adjustment, and file modification times when supplied by the provider. Sort by filename or modification time; sorting does not rearrange placed images.\n\nTap a thumbnail to select it. «🖼️ Crop image» trims that image; «🧪 Batch crop» applies pixel or percentage margins to selected images. Drag crop handles or type amounts. «🧪 Reset crop» restores the original edges. Cropping is non-destructive and can be undone.\n\nHold a thumbnail, or drag an image already in the workspace, then drop it onto a highlighted edge. The translucent preview shows the exact snapped result. A right attachment aligns the tops; a bottom attachment aligns the left edges. You can also tap a thumbnail and then a + target. When snapping, the first image starts at the origin. Attached images may move when their parent is cropped. Overlaps are rejected when snapping.\n\nSelect an image and use «📍 Exact position» to set its top-left X/Y coordinates in whole pixels, starting at zero. Other images keep their positions, and overlaps are allowed.\n\n«↔️ Same width» and «↕️ Same height» give every input a common dimension while preserving each image's own aspect ratio. Choose «🧪 Pixels», «🧪 Percent», «🧪 Smallest» or «🧪 Largest». «📏 Restore original sizes» removes normalization and keeps crops.\n\n«🧪 Unplace» returns only the selected image to the tray. Other images stay placed; attached images may move to fill the gap. «🧪 Remove» deletes only that input. Undo/Redo restore these changes. Drag a placed image to rearrange it; empty-space dragging pans. Pinch to zoom. «🧪 Show all» adjusts the zoom to show the whole assembly; it never changes output dimensions.\n\n«💾 Save PNG» saves the assembled image directly. «🎨 Edit in Paint» transfers it into the main editor as an undoable replacement. If the output exceeds the memory budget, choose a smaller output copy if offered. If even a tiny output exceeds the budget, the app shows a memory warning instead of a size chooser. Original source files stay unchanged. The current assembly is stored locally and reopens when you return.\n\nThis mode uses the same Catrobat/AGPL and asset credits shown in the main editor's «📁 File > ℹ️ About, licences & credits» panel.", helpText)
            assertTrue(tag,helpText.contains(if(tag=="fr") "Les images rattachées peuvent se déplacer lorsque leur image parente est recadrée." else "Attached images may move when their parent is cropped."))
            assertFalse(tag,helpText.contains("Existing attachments move"))
            for(count in listOf(0,1,2,20)) {
                val expected=if(tag=="fr") {
                    val noun=if(count<=1) "image" else "images"
                    "Aperçu : 24 × 16 px\nAppliquer à $count $noun. Le recadrage des images placées peut déplacer les images qui leur sont rattachées."
                } else {
                    val noun=if(count==1) "image" else "images"
                    (if(tag=="qaa-Zsye-XV") "✅ " else "") +
                    "Preview: 24 × 16 px\nApply to $count $noun. Cropping placed images may move their attached images."
                }
                assertEquals(tag,expected,activity.resources.getQuantityString(org.catrobat.paintroid.R.plurals.ui_crop_preview_images,count,24,16,count))
            }
        }
    }

    /** Whole-value consumers and mode controls, not glyph/layout acceptance. */
    @Test fun englishHelpModesReachActualHelpAndExactPositionToolbarWithCurrentLabels() {
        val expected=org.json.JSONObject(javaClass.getResourceAsStream("/assembly-help-modes/expected.json")!!
            .bufferedReader(Charsets.UTF_8).use { it.readText() }).getJSONObject("locales")
        // A language-only configuration explicitly exercises the default resource,
        // independently of the test device's regional English setting.
        val config=android.content.res.Configuration(activity.resources.configuration)
        config.setLocales(android.os.LocaleList.forLanguageTags("en"))
        assertEquals(expected.getJSONObject("en").getString("help"),activity.createConfigurationContext(config)
            .getString(org.catrobat.paintroid.R.string.ui_add_up_to_20_images_with_android_s))
        val tags=listOf("en-001","en-AU","en-CA","en-GB","en-IN","en-SG","en-US","en-XV","qaa-Zsye-XV")
        for(tag in tags) withLanguage(tag) {
            // Rebuild real toolbar consumers after the app-language change.
            activity.onConfigurationChanged(activity.resources.configuration); idle()
            val resourceTag=if(tag=="qaa-Zsye-XV") "en-Zsye-XV-anpaint" else tag
            assertEquals(tag,AppLanguage.selectedTag(activity))
            assertEquals(resourceTag,activity.resources.configuration.locales[0].toLanguageTag())
            val value=expected.getJSONObject(tag)
            assertEquals(tag,value.getString("positionLabel"),
                activity.window.decorView.findViewWithTag<TextView>("assembly_position").text.toString())
            click("assembly_help")
            val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            assertTrue(tag,dialog.isShowing)
            fun textViews(view: View): List<TextView> =
                (if(view is TextView) listOf(view) else emptyList()) +
                    (if(view is android.view.ViewGroup) (0 until view.childCount).flatMap { textViews(view.getChildAt(it)) } else emptyList())
            val messages=if(tag in listOf("en-XV","qaa-Zsye-XV")) {
                val shell=dialog.window!!.decorView.findViewWithTag<View>("vertical_dialog")
                assertNotNull(tag,shell)
                textViews(shell).filter { it is FlowTextView && it.text.toString()==value.getString("help") }
            } else listOf(dialog.findViewById<TextView>(android.R.id.message))
            assertEquals(tag,1,messages.size)
            assertTrue(tag,messages.single().isShown)
            val shown=messages.single().text.toString()
            assertEquals(tag,value.getString("help"),shown)
            assertEquals(8,shown.split("\n\n").size)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
            assertFalse(tag,dialog.isShowing)
            assertTrue(activity.assembly.images.isEmpty())
        }
    }

    @Test fun exactFirstPlacementAndUnplaceMatchHelpWhileSnapRemovalCanFillTheGap() {
        load()
        val first=image("b.png").id;val child=image("a.png").id;val last=image("c.png").id
        val originals=activity.assembly.images.associate { it.id to it.file.readBytes() }
        fun position(id: String,x: Int,y: Int) {
            click("assembly_item_$id");click("assembly_position")
            val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
            val root=dialog.window!!.decorView
            root.findViewWithTag<EditText>("assembly_position_x").setText(x.toString())
            root.findViewWithTag<EditText>("assembly_position_y").setText(y.toString())
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick();idle()
            assertFalse(dialog.isShowing)
        }
        // The first exact placement can start away from the origin.
        position(first,5,7)
        assertEquals(Rect(5,7,29,23),activity.assembly.layout()[first])
        activity.assembly.place(child,Attachment(first,SnapEdge.RIGHT))
        activity.assembly.place(last,Attachment(child,SnapEdge.BOTTOM));idle()
        val attached=activity.assembly.layout()
        // Removing an explicit anchor keeps its children exactly where they were.
        click("assembly_item_$first");click("assembly_unplace")
        assertEquals(attached.filterKeys { it!=first },activity.assembly.layout())
        assertFalse(activity.assembly.image(first).isPlaced)
        click("assembly_undo");assertEquals(attached,activity.assembly.layout())
        // Move just the selected image over its child through the actual toolbar.
        position(first,30,9)
        val moved=attached.toMutableMap().apply { put(first,Rect(30,9,54,25)) }
        assertEquals(moved,activity.assembly.layout())
        assertTrue(Rect.intersects(moved.getValue(first),moved.getValue(child)))
        click("assembly_undo");assertEquals(attached,activity.assembly.layout())
        click("assembly_redo");assertEquals(moved,activity.assembly.layout())
        // Unplace and Remove differ only in retention of the selected input.
        click("assembly_item_$first");click("assembly_remove")
        assertEquals(moved.filterKeys { it!=first },activity.assembly.layout())
        assertEquals(2,activity.assembly.images.size)
        click("assembly_undo");assertEquals(moved,activity.assembly.layout())
        assertEquals(3,activity.assembly.images.size)
        activity.assembly.images.forEach { assertArrayEquals(originals.getValue(it.id),it.file.readBytes()) }
        // Snapping still starts at zero, rejects a colliding target, and can
        // promote a successor into the removed image's gap.
        activity.assembly.images.forEach { activity.assembly.unplace(it.id) }
        activity.assembly.place(first,Attachment(null,null))
        activity.assembly.place(child,Attachment(first,SnapEdge.RIGHT))
        activity.assembly.place(last,Attachment(child,SnapEdge.RIGHT));idle()
        assertEquals(Rect(0,0,24,16),activity.assembly.layout()[first])
        val snapped=activity.assembly.layout()
        assertThrows(IllegalArgumentException::class.java) {
            activity.assembly.place(last,Attachment(first,SnapEdge.RIGHT))
        }
        assertEquals(snapped,activity.assembly.layout())
        click("assembly_item_$child");click("assembly_unplace")
        assertEquals(Rect(24,0,42,8),activity.assembly.layout()[last])
        assertEquals(2,activity.assembly.layout().size)
        click("assembly_undo");assertEquals(snapped,activity.assembly.layout())
        click("assembly_redo");assertEquals(Rect(24,0,42,8),activity.assembly.layout()[last])
    }

}
