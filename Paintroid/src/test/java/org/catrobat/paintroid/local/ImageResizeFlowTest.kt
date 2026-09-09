/* AN Paint regression checks, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.ActivityManager
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.content.pm.ProviderInfo
import android.graphics.*
import android.net.Uri
import android.os.Looper
import android.view.View
import android.widget.EditText
import android.widget.TextView
import androidx.exifinterface.media.ExifInterface
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
import org.robolectric.shadows.ShadowPopupMenu
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ImageResizeFlowTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    private lateinit var provider: ClassicWorkspaceTest.DocumentProvider
    private val mib = 1024L * 1024
    private val uri = Uri.parse("content://resize.fixture/document/1")
    @Before fun start() {
        val context = RuntimeEnvironment.getApplication() as Context
        File(context.filesDir,"classic-recovery.png").delete()
        File(context.filesDir,"classic-autosave.zip").delete(); File(context.filesDir,"classic-autosave.zip.bak").delete()
        context.getSharedPreferences("classic-ui",Context.MODE_PRIVATE).edit().clear().commit()
        controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        activity = controller.setup().get()
        activity.document.newImage(120,120); activity.paintCanvas.fit()
        provider = ClassicWorkspaceTest.DocumentProvider().apply {
            file = File(context.cacheDir,"resize-fixture.png")
            attachInfo(context,ProviderInfo().apply { authority = "resize.fixture" })
        }
        ShadowContentResolver.registerProviderInternal("resize.fixture",provider)
    }
    @After fun stop() {
        if (activity.isDestroyed) return
        (ShadowAlertDialog.getLatestAlertDialog() as? AlertDialog)?.dismiss()
        idleUntil { !activity.busy }; controller.pause().stop(); idleUntil { !activity.busy }; controller.destroy()
    }
    private fun idleUntil(condition: () -> Boolean) {
        val deadline = System.nanoTime() + 10_000_000_000L
        while (!condition() && System.nanoTime() < deadline) { shadowOf(Looper.getMainLooper()).idle(); Thread.sleep(10) }
        shadowOf(Looper.getMainLooper()).idle(); assertTrue("Timed out waiting for Android UI/import",condition())
    }
    private fun memoryBudget(bytes: Long) {
        shadowOf(activity.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager).setMemoryInfo(ActivityManager.MemoryInfo().apply {
            totalMem = 2 * 1024 * mib; availMem = (bytes + 32 * mib) * 3; threshold = 0
        })
    }
    private fun fixture(format: Bitmap.CompressFormat = Bitmap.CompressFormat.PNG, exif: Boolean = false) {
        val image = Bitmap.createBitmap(1600,2400,Bitmap.Config.ARGB_8888)
        val canvas = Canvas(image); val paint = Paint()
        paint.color = Color.RED; canvas.drawRect(0f,0f,800f,1200f,paint)
        paint.color = Color.BLUE; canvas.drawRect(800f,0f,1600f,1200f,paint)
        paint.color = 0x8000ff00.toInt(); canvas.drawRect(0f,1200f,800f,2400f,paint)
        provider.file.outputStream().use { assertTrue(image.compress(format,100,it)) }; image.recycle()
        if (exif) ExifInterface(provider.file.path).apply { setAttribute(ExifInterface.TAG_ORIENTATION,ExifInterface.ORIENTATION_ROTATE_90.toString()); saveAttributes() }
    }
    private fun load(import: Boolean = false) {
        activity.window.decorView.findViewWithTag<View>("menu_File").performClick()
        ShadowPopupMenu.getLatestPopupMenu().menu.performIdentifierAction(if (import) 2 else 1,0)
        val intent = shadowOf(activity).nextStartedActivityForResult.intent
        shadowOf(activity).receiveResult(intent,Activity.RESULT_OK,Intent().setData(uri))
    }
    private fun resizeDialog(): AlertDialog {
        idleUntil { ShadowAlertDialog.getLatestAlertDialog()?.window?.decorView?.findViewWithTag<View>("resize_width") != null }
        return ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
    }
    private fun setWidth(dialog: AlertDialog, width: String) {
        dialog.window!!.decorView.findViewWithTag<EditText>("resize_width").setText(width)
        shadowOf(Looper.getMainLooper()).idle()
    }
    @Test fun approvedResizeLoadsExactDimensionsAndOpaquePixelsFromOneProviderRead() {
        fixture(); val originalFile = provider.file.readBytes(); memoryBudget(24 * mib); load()
        val dialog = resizeDialog(); val root = dialog.window!!.decorView
        val text = root.findViewWithTag<TextView>("resize_original").text.toString()
        assertTrue(text,text.contains("1600 × 2400")); assertTrue(text.contains("3,840,000 pixels"))
        assertTrue(text.contains("14.6 MiB")); assertTrue(text.contains("44.0 MiB"))
        setWidth(dialog,"800")
        assertEquals("1200",root.findViewWithTag<EditText>("resize_height").text.toString())
        assertTrue(root.findViewWithTag<TextView>("resize_estimate").text.contains("960,000 pixels"))
        render(dialog,"resize-image.png")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idleUntil { !activity.busy }
        val image = activity.document.bitmap
        assertEquals(800,image.width); assertEquals(1200,image.height)
        assertEquals(Color.RED,image.getPixel(100,100)); assertEquals(Color.BLUE,image.getPixel(700,100))
        assertEquals(Color.rgb(127,255,127),image.getPixel(100,1000)); assertEquals(Color.WHITE,image.getPixel(700,1000))
        assertEquals(1,provider.reads); assertArrayEquals(originalFile,provider.file.readBytes()); assertNull(activity.lastIoError)
        assertNoCachedImport()
    }
    @Test @Config(sdk = [28]) fun resizeImportCreatesSelectionAtChosenSizeOnAndroidNine() {
        fixture(); memoryBudget(24*mib); val original = activity.document.bitmap; load(true)
        val dialog = resizeDialog(); setWidth(dialog,"400")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idleUntil { !activity.busy }
        assertSame(original,activity.document.bitmap)
        val selection = activity.document.selection!!.image
        assertEquals(400,selection.width); assertEquals(600,selection.height)
        assertEquals(0x8000ff00.toInt(),selection.getPixel(50,500)); assertEquals(1,provider.reads); assertNoCachedImport()
    }
    @Test fun invalidOrOverBudgetSizesStayInDialogAndCancelPreservesCanvasAndSource() {
        fixture(); memoryBudget(24*mib); activity.document.bitmap.setPixel(2,3,Color.MAGENTA)
        val original = activity.document.bitmap; load(); val dialog = resizeDialog()
        for (width in listOf("0","999999999999999","1601","1600")) {
            setWidth(dialog,width); assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
        }
        setWidth(dialog,"800"); assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
        dialog.cancel(); idleUntil { !activity.busy }
        assertSame(original,activity.document.bitmap); assertEquals(Color.MAGENTA,original.getPixel(2,3))
        assertNull(activity.lastIoError); assertEquals(1,provider.reads); assertNoCachedImport()
    }
    @Test fun changedMemoryIsCheckedAgainOnConfirmationAndCanRecoverWithoutReselectingFile() {
        fixture(); memoryBudget(24*mib); load(); val dialog = resizeDialog(); setWidth(dialog,"800")
        memoryBudget(0)
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertTrue(dialog.isShowing); assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
        memoryBudget(24*mib); setWidth(dialog,"400")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idleUntil { !activity.busy }
        assertEquals(400,activity.document.bitmap.width); assertEquals(1,provider.reads); assertNoCachedImport()
    }
    @Test fun jpegOrientationIsShownAndAppliedTogetherWithExactResize() {
        fixture(Bitmap.CompressFormat.JPEG,true); memoryBudget(24*mib); load(); val dialog = resizeDialog()
        assertTrue(dialog.window!!.decorView.findViewWithTag<TextView>("resize_original").text.contains("2400 × 1600"))
        setWidth(dialog,"900")
        assertEquals("600",dialog.window!!.decorView.findViewWithTag<EditText>("resize_height").text.toString())
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); idleUntil { !activity.busy }
        val image = activity.document.bitmap
        assertEquals(900,image.width); assertEquals(600,image.height)
        assertTrue(Color.red(image.getPixel(800,100)) > 245); assertTrue(Color.blue(image.getPixel(800,500)) > 245)
        assertEquals(1,provider.reads); assertNoCachedImport()
    }
    @Test fun sampledDecodeHandlesNonPowerOfTwoTargetAndVeryThinImages() {
        fixture()
        val source = ImportedImage(provider.file,"fixture")
        val image = source.decode(ImportPlan.create(source.dimensions,ImageDimensions(713,1069)))
        assertEquals(713,image.width); assertEquals(1069,image.height); assertEquals(Color.RED,image.getPixel(50,50)); image.recycle()
        val thin = Bitmap.createBitmap(1,10000,Bitmap.Config.ARGB_8888); thin.eraseColor(Color.CYAN)
        provider.file.outputStream().use { thin.compress(Bitmap.CompressFormat.PNG,100,it) }; thin.recycle()
        val tall = ImportedImage(provider.file,"thin"); val plan = ImportPlan.create(tall.dimensions,ImageDimensions(1,100))
        assertTrue(plan.sample >= 64)
        val result = tall.decode(plan); assertEquals(1,result.width); assertEquals(100,result.height); assertEquals(Color.CYAN,result.getPixel(0,50)); result.recycle()
    }
    @Test fun destroyingActivityWhileResizeChoiceIsOpenCleansUpCachedProviderCopy() {
        fixture(); memoryBudget(24*mib); load(); val dialog = resizeDialog()
        assertTrue(dialog.isShowing); assertTrue(activity.cacheDir.listFiles()!!.any { it.name.startsWith("classic-import-") })
        controller.pause().stop().destroy(); shadowOf(Looper.getMainLooper()).idle()
        assertFalse(dialog.isShowing); assertNoCachedImport()
    }
    private fun assertNoCachedImport() { assertTrue(activity.cacheDir.listFiles()!!.none { it.name.startsWith("classic-import-") }) }
    private fun render(dialog: AlertDialog, name: String) {
        val view = dialog.window!!.decorView
        view.measure(View.MeasureSpec.makeMeasureSpec(760,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(1640,View.MeasureSpec.AT_MOST))
        view.layout(0,0,view.measuredWidth,view.measuredHeight)
        val bitmap = Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888); view.draw(Canvas(bitmap))
        val file = File("build/reports/classic-preview",name); file.parentFile.mkdirs()
        file.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it)) }; bitmap.recycle()
    }
}
