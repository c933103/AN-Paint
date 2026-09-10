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
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.SeekBar
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
class ANPaintControlsTest {
    private lateinit var controller: ActivityController<ClassicPaintActivity>
    private lateinit var activity: ClassicPaintActivity
    @Before fun start() {
        val context = RuntimeEnvironment.getApplication() as Context
        File(context.filesDir,"classic-recovery.png").delete()
        File(context.filesDir,"classic-autosave.zip").delete(); File(context.filesDir,"classic-autosave.zip.bak").delete()
        context.getSharedPreferences("classic-ui",Context.MODE_PRIVATE).edit().clear().commit()
        context.getSharedPreferences("classic-custom-colours",Context.MODE_PRIVATE).edit().clear().commit()
        controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        activity = controller.setup().get()
        activity.document.newImage(120,120); activity.paintCanvas.fit()
    }
    @After fun stop() { controller.pause().stop(); waitForIo(); controller.destroy() }
    private fun waitForIo() {
        val end = System.nanoTime() + 10_000_000_000L
        while (activity.busy && System.nanoTime() < end) { shadowOf(Looper.getMainLooper()).idle(); Thread.sleep(10) }
        shadowOf(Looper.getMainLooper()).idle(); assertFalse(activity.busy)
    }
    private fun root() = activity.window.decorView
    private fun click(tag: String) { assertTrue(root().findViewWithTag<View>(tag).performClick()); shadowOf(Looper.getMainLooper()).idle() }
    private fun picker(): AlertDialog { click("foreground_colour"); return ShadowAlertDialog.getLatestAlertDialog() as AlertDialog }
    private fun edit(dialog: AlertDialog, tag: String, text: String) {
        dialog.window!!.decorView.findViewWithTag<View>("colour_advanced_tab").performClick()
        shadowOf(Looper.getMainLooper()).idle()
        dialog.window!!.decorView.findViewWithTag<EditText>("colour_$tag").setText(text)
    }
    private fun field(dialog: AlertDialog, tag: String) = dialog.window!!.decorView.findViewWithTag<EditText>("colour_$tag").text.toString()
    private fun touch(view: View, x: Float, y: Float) {
        listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP).forEach { action ->
            val event=MotionEvent.obtain(0,20,action,x,y,0); assertTrue(view.dispatchTouchEvent(event)); event.recycle()
        }
        shadowOf(Looper.getMainLooper()).idle()
    }
    @Test fun actionsAreSingleIconsWithAccessibleNamesAndZoomOccupiesBottomRight() {
        listOf("undo" to "Undo","redo" to "Redo","clipboard_cut" to "Cut","clipboard_copy" to "Copy","clipboard_paste" to "Paste").forEach { (tag,label) ->
            val view=root().findViewWithTag<View>(tag); assertTrue(view is ActionButton); assertEquals(label,view.contentDescription)
        }
        assertNull(root().findViewWithTag<View>("apply"))
        val slider=root().findViewWithTag<SeekBar>("zoom_slider")
        assertEquals("zoom_controls",(slider.parent as View).tag)
        val footer=(slider.parent as View).parent as ViewGroup
        assertSame(slider.parent,footer.getChildAt(footer.childCount-1))
        click("tool_POLYGON")
        val apply=root().findViewWithTag<View>("apply")
        assertNotNull(apply); assertNotSame(footer,apply.parent)
        assertSame(root().findViewWithTag<View>("tool_help").parent,apply.parent)
    }
    @Test fun zoomSliderChangesViewportAndStaysInSyncWithOtherZoomControls() {
        val slider=root().findViewWithTag<SeekBar>("zoom_slider")
        val canvas=activity.paintCanvas
        canvas.zoomAt(1f); val old=canvas.zoom
        slider.measure(View.MeasureSpec.makeMeasureSpec(240,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(88,View.MeasureSpec.EXACTLY)); slider.layout(0,0,240,88)
        touch(slider,slider.width*.8f,slider.height/2f)
        assertTrue(canvas.zoom>old)
        canvas.zoomAt(8f); assertEquals(canvas.sliderForZoom(),slider.progress)
        click("zoom_out"); assertTrue(canvas.zoom<8f)
        click("zoom_in"); assertEquals(8f,canvas.zoom,.001f)
        assertTrue(slider.contentDescription.contains("800%"))
    }
    @Test fun colourFieldsSynchronizeRgbHsvHslAndOpaqueHexAndCommit() {
        val dialog=picker()
        edit(dialog,"hex","#4080C0")
        assertEquals("64",field(dialog,"r")); assertEquals("128",field(dialog,"g")); assertEquals("192",field(dialog,"b"))
        edit(dialog,"h","120"); edit(dialog,"s","100"); edit(dialog,"v","100")
        assertEquals("0",field(dialog,"r")); assertEquals("255",field(dialog,"g")); assertEquals("0",field(dialog,"b")); assertEquals("#00FF00",field(dialog,"hex"))
        edit(dialog,"hl","240"); edit(dialog,"sl","100"); edit(dialog,"l","50")
        assertEquals("#0000FF",field(dialog,"hex"))
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertEquals(Color.BLUE,activity.document.foreground)
    }
    @Test fun invalidNumericAndHexInputDoNotCommitAndCancelKeepsOriginal() {
        val dialog=picker(); edit(dialog,"r","999")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); assertTrue(dialog.isShowing)
        assertEquals(Color.BLACK,activity.document.foreground)
        edit(dialog,"r","64"); edit(dialog,"hex","#broken")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); assertTrue(dialog.isShowing)
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); assertEquals(Color.BLACK,activity.document.foreground)
    }
    @Test fun customSwatchesPersistAcrossDialogReopenAndBackgroundUsesSamePicker() {
        var dialog=picker(); edit(dialog,"hex","#AA3300")
        dialog.window!!.decorView.findViewWithTag<View>("colour_mode_0").performClick()
        assertTrue(dialog.window!!.decorView.findViewWithTag<View>("add_custom_colour").performClick())
        dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
        click("background_colour"); dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        assertTrue(dialog.window!!.decorView.findViewWithTag<View>("custom_colour_4").performClick())
        assertEquals("#AA3300",field(dialog,"hex"))
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); assertEquals(0xffaa3300.toInt(),activity.document.background)
    }
    @Test fun spectrumAndWheelBothAcceptTouchIncludingStartingAtBlack() {
        val dialog=picker(); val content=dialog.window!!.decorView
        val surface=content.findViewWithTag<ColourSurface>("colour_surface")
        content.findViewWithTag<View>("colour_advanced_tab").performClick();
        content.findViewWithTag<View>("colour_mode_1").performClick(); shadowOf(Looper.getMainLooper()).idle()
        val d=activity.resources.displayMetrics.density
        touch(surface,(surface.width-42*d)/3,4f) // spectrum saturation at L=0
        touch(surface,surface.width-10f,surface.height/2f) // visible lightness bar
        assertTrue("HSL saturation="+field(dialog,"sl"),field(dialog,"sl").toFloat()>99f)
        assertTrue("HSV value="+field(dialog,"v"),field(dialog,"v").toFloat()>90f)
        content.findViewWithTag<View>("colour_mode_2").performClick(); shadowOf(Looper.getMainLooper()).idle()
        val right=surface.width-42*d; val radius=minOf(right-4,surface.height-8f)/2
        touch(surface,(4+right)/2+radius,surface.height/2f)
        touch(surface,surface.width-10f,4f)
        assertTrue("HSV saturation="+field(dialog,"s"),field(dialog,"s").toFloat()>95f)
        assertTrue("HSV value="+field(dialog,"v"),field(dialog,"v").toFloat()>99f)
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertTrue(Color.red(activity.document.foreground)>240)
    }
    @Test fun aboutAndAssetCreditsNameAnPaintAndCreditVisualAssetsAndDeviceFonts() {
        val about=LegalInfo.aboutText(activity)
        assertTrue(about.contains("AN Paint")); assertTrue(about.contains("Catrobat"))
        val credits=activity.assets.open("legal/ASSET_CREDITS.txt").bufferedReader().readText()
        listOf("ActionButton.kt","ToolButton.kt","system","monospace","LGPL","AGPL","launcher.svg","CC BY-SA 4.0").forEach { assertTrue(it,credits.contains(it)) }
        click("menu_Help"); val menu=ShadowPopupMenu.getLatestPopupMenu().menu
        assertTrue(menu.performIdentifierAction(5,0)); assertTrue(org.robolectric.shadows.ShadowDialog.getLatestDialog().isShowing)
    }
    @Test fun colourPickerPreviewsRender() {
        val dialog=picker()
        listOf(0 to "colour-palette.png",3 to "colour-honeycomb.png",1 to "colour-spectrum.png",2 to "colour-wheel.png").forEach { (mode,name) ->
            if (mode in 1..2) dialog.window!!.decorView.findViewWithTag<View>("colour_advanced_tab").performClick()
            dialog.window!!.decorView.findViewWithTag<View>("colour_mode_$mode").performClick()
            val view=dialog.window!!.decorView
            view.measure(View.MeasureSpec.makeMeasureSpec(760,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(1640,View.MeasureSpec.AT_MOST))
            view.layout(0,0,view.measuredWidth,view.measuredHeight)
            val bitmap=Bitmap.createBitmap(view.width,view.height,Bitmap.Config.ARGB_8888); view.draw(Canvas(bitmap))
            val file=File("build/reports/classic-preview",name); file.parentFile.mkdirs()
            file.outputStream().use { assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it)) }; bitmap.recycle()
        }
        dialog.dismiss()
    }
    @Test fun honeycombIsAnIntermediateViewAndNoModeOffersOpacity() {
        val dialog=picker(); val root=dialog.window!!.decorView
        val opacity=root.findViewWithTag<View>("colour_alpha_slider")
        assertNull(opacity)
        root.findViewWithTag<View>("colour_mode_3").performClick(); shadowOf(Looper.getMainLooper()).idle()
        val honeycomb=root.findViewWithTag<HoneycombPalette>("colour_honeycomb")
        assertTrue(honeycomb.isShown); assertEquals(140,honeycomb.childCount); assertNull(opacity)
        val cell=honeycomb.getChildAt(12)
        val expected=Color.parseColor(cell.contentDescription.toString().substringAfterLast(' '))
        touch(cell,cell.width / 2f,cell.height / 2f)
        assertEquals(String.format(java.util.Locale.ROOT,"#%06X",expected and 0xffffff),field(dialog,"hex"))
        root.findViewWithTag<View>("colour_advanced_tab").performClick(); shadowOf(Looper.getMainLooper()).idle()
        assertNull(opacity); assertFalse(honeycomb.isShown)
        assertNull(root.findViewWithTag<View>("colour_a"))
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick(); assertEquals(expected,activity.document.foreground)
    }
    @Test fun oversizedNewCanvasFailsBeforeAllocationAndPreservesPixels() {
        val doc=activity.document; doc.bitmap.setPixel(2,3,Color.RED); val original=doc.bitmap
        click("menu_File"); ShadowPopupMenu.getLatestPopupMenu().menu.performIdentifierAction(0,0)
        shadowOf(Looper.getMainLooper()).idle()
        val dialog=ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val fields=mutableListOf<EditText>()
        fun collect(v: View) { if(v is EditText) fields.add(v); if(v is ViewGroup) for(i in 0 until v.childCount) collect(v.getChildAt(i)) }
        collect(dialog.window!!.decorView); fields[0].setText("40000"); fields[1].setText("40000")
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertSame(original,doc.bitmap); assertEquals(Color.RED,doc.bitmap.getPixel(2,3))
        assertTrue(dialog.isShowing); assertNotSame(dialog,ShadowAlertDialog.getLatestAlertDialog())
    }
    @Test fun billionPixelImportOffersResizeBeforeDecodingAndCancelKeepsExistingCanvas() {
        val context=RuntimeEnvironment.getApplication() as Context
        val provider=ClassicWorkspaceTest.DocumentProvider().apply {
            file=File(context.cacheDir,"huge-header.png")
            attachInfo(context,ProviderInfo().apply { authority="anpaint.fixture" })
        }
        val small=Bitmap.createBitmap(24,48,Bitmap.Config.ARGB_8888)
        provider.file.outputStream().use { small.compress(Bitmap.CompressFormat.PNG,100,it) }; small.recycle()
        val bytes=provider.file.readBytes()
        val buffer=java.nio.ByteBuffer.wrap(bytes).order(java.nio.ByteOrder.BIG_ENDIAN)
        buffer.putInt(16,40000); buffer.putInt(20,40000)
        val crc=java.util.zip.CRC32(); crc.update(bytes,12,17); buffer.putInt(29,crc.value.toInt())
        provider.file.writeBytes(bytes)
        ShadowContentResolver.registerProviderInternal("anpaint.fixture",provider)
        val doc=activity.document; doc.bitmap.setPixel(2,3,Color.RED); val original=doc.bitmap
        click("menu_File"); ShadowPopupMenu.getLatestPopupMenu().menu.performIdentifierAction(1,0)
        val launch=shadowOf(activity).nextStartedActivityForResult
        shadowOf(activity).receiveResult(launch.intent,Activity.RESULT_OK,Intent().setData(Uri.parse("content://anpaint.fixture/document/1")))
        val end = System.nanoTime() + 10_000_000_000L
        while (ShadowAlertDialog.getLatestAlertDialog()?.window?.decorView?.findViewWithTag<View>("resize_original") == null && System.nanoTime() < end) {
            shadowOf(Looper.getMainLooper()).idle(); Thread.sleep(10)
        }
        val resize = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
        val originalText = resize.window!!.decorView.findViewWithTag<android.widget.TextView>("resize_original").text.toString()
        assertTrue(originalText,originalText.contains("40000 × 40000")); assertTrue(originalText.contains("1,600,000,000 pixels"))
        assertTrue(originalText.contains("6.0 GiB")); assertTrue(originalText.contains("17.9 GiB"))
        assertSame(original,doc.bitmap); assertEquals(Color.RED,doc.bitmap.getPixel(2,3)); assertTrue(activity.busy)
        resize.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); waitForIo()
        assertNull(activity.lastIoError); assertEquals(1,provider.reads)
        assertTrue(activity.cacheDir.listFiles()!!.none { it.name.startsWith("classic-import-") })
    }

}
