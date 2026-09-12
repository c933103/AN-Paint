/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.graphics.Bitmap
import android.graphics.Color
import android.os.Looper
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ImportMemoryIntegrationTest {
    private val mib=1024L*1024
    private fun policy(bytes: Long)=ImageMemoryPolicy.calculate(4L*1024*mib,0,(bytes+32*mib)*3,0,true)

    @Test fun tinyOutputCannotHideAnOversizedUntiledNativeSource() {
        val source=ImageDimensions(40000,40000)
        val small=ImportPlan.create(source,ImageDimensions(1,1))
        val available=policy(128*mib)
        assertTrue(available.accepts(small,0)) // Generic sampled-image assumptions alone are insufficient.
        val native=ImportMemoryRequirements(source.pixels*32+32*mib+4)
        assertFalse(native.accepts(available,small,0))
        assertNull(native.suggestResize(source,available,0))
        assertTrue(native.estimatedBytes(small,0)>50_000_000_000.0)
        try {native.checkImport(available,small,0);fail("Native source footprint ignored")}
        catch(expected: ImageSizeException) {assertTrue(expected.message!!.contains(memoryLabel(native.estimatedBytes(small,0))))}
    }

    @Test fun nativeTileFootprintAndResidentCanvasLeaveAConsistentDecoderBudget() {
        val source=ImageDimensions(12000,8000);val resident=2_000_000L
        val nativeAtOnePixel=512L*512*32+32*mib+4
        val native=ImportMemoryRequirements(nativeAtOnePixel);val available=policy(128*mib)
        val chosen=native.suggestResize(source,available,resident)!!
        assertTrue(chosen.width<source.width && chosen.height<source.height)
        val plan=ImportPlan.create(source,chosen)
        native.checkImport(available,plan,resident)
        val nativeDecode=nativeAtOnePixel+(chosen.pixels-1)*4
        assertTrue(native.estimatedBytes(plan,resident)<=available.workingBytes*.9)
        assertTrue(native.decoderBudget(available.workingBytes,chosen,resident)>=nativeDecode)
        assertEquals(available.workingBytes-resident*4-chosen.pixels*8,native.decoderBudget(available.workingBytes,chosen,resident))
        assertFalse(native.accepts(policy(32*mib),plan,resident))
        assertEquals(0L,native.decoderBudget(1,ImageDimensions(Int.MAX_VALUE,Int.MAX_VALUE),Long.MAX_VALUE))
    }

    @Test fun pngKeepsSampledEstimatesAndDecodesWithoutLoadingANativeCodec() {
        val context=RuntimeEnvironment.getApplication()
        val file=File.createTempFile("memory-png-",".bin",context.cacheDir)
        val bitmap=Bitmap.createBitmap(160,240,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)}
        try {
            file.outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}
            val source=ImportedImage(file,"provider-image.bin")
            val plan=ImportPlan.create(source.dimensions,ImageDimensions(40,60));val available=policy(8*mib)
            assertFalse(source.memoryRequirements.hasNativeWork)
            assertEquals(plan.estimatedBytes(1234),source.estimatedBytes(plan,1234),0.0)
            assertEquals(available.suggestResize(source.dimensions,1234),source.suggestResize(available,1234))
            source.checkImport(available,plan,1234)
            val output=source.decode(plan,available.workingBytes,1234)
            try {assertEquals(40,output.width);assertEquals(60,output.height);assertEquals(Color.MAGENTA,output.getPixel(20,30))}
            finally {output.recycle()}
        } finally {bitmap.recycle();file.delete()}
    }

    @Test fun resizeDialogShowsNativeFloorAndDisablesAnImpossibleResize() {
        val controller=Robolectric.buildActivity(Activity::class.java).setup();val activity=controller.get()
        val source=ImageDimensions(40000,40000)
        val native=ImportMemoryRequirements(source.pixels*32+32*mib+4)
        var cancelled=0;var resized=false
        val dialog=ImageResizeDialog(activity,source,10000,{policy(128*mib)},
            resize={resized=true},cancel={cancelled++},memoryRequirements=native).show()
        try {
            // Dialog.show posts OnShowListener to the main looper. Run it before
            // reading the initial estimate or pressing its guarded action button.
            shadowOf(Looper.getMainLooper()).idle()
            val view=dialog.window!!.decorView
            assertTrue(view.findViewWithTag<TextView>("resize_original").text.contains(memoryLabel(native.estimatedBytes(ImportPlan.create(source,source),10000))))
            assertTrue(view.findViewWithTag<TextView>("resize_estimate").text.contains("smallest output"))
            assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertFalse(resized);assertTrue(dialog.isShowing)
            dialog.cancel();shadowOf(Looper.getMainLooper()).idle();assertEquals(1,cancelled)
        } finally {dialog.dismiss();shadowOf(Looper.getMainLooper()).idle();controller.pause().stop().destroy()}
    }

    @Test fun resizeConfirmationRechecksNativeWorkAgainstCurrentMemory() {
        val controller=Robolectric.buildActivity(Activity::class.java).setup();val activity=controller.get()
        val source=ImageDimensions(4000,3000);val native=ImportMemoryRequirements(48*mib+4)
        var available=policy(128*mib);var result: ImageDimensions?=null
        val dialog=ImageResizeDialog(activity,source,0,{available},resize={result=it},cancel={},memoryRequirements=native).show()
        try {
            shadowOf(Looper.getMainLooper()).idle()
            assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            available=policy(32*mib)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertNull(result);assertTrue(dialog.isShowing);assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            available=policy(128*mib)
            dialog.window!!.decorView.findViewWithTag<EditText>("resize_width").setText("400")
            assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertEquals(ImageDimensions(400,300),result)
        } finally {dialog.dismiss();shadowOf(Looper.getMainLooper()).idle();controller.pause().stop().destroy()}
    }
}
