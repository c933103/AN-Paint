/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Looper
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.concurrent.ExecutorService
import java.util.concurrent.TimeUnit

/** A valid ZIP can fail after its Save destination has already been parsed. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class FailedRecoverySaveTargetTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    private val target=SavedTarget(Uri.parse("content://documents/previous-drawing"),"Previous.png",ExportOptions(ImageFormat.PNG))

    @Before fun clean() {
        AutosaveStore(context.filesDir).exists()
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-") && it.isFile}?.forEach {assertTrue(it.delete())}
        listOf("classic","classic-ui","export").forEach {context.getSharedPreferences(it,0).edit().clear().commit()}
    }

    private fun prepare(valid: Boolean,legacy: Boolean,overflow: Boolean=false) {
        val canvas=Bitmap.createBitmap(7,5,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.RED)}
        val floating=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.BLUE)}
        val rectangle=if(overflow) listOf(0.0,0.0,1e300,2.0) else if(valid) listOf(0,0,2,2) else listOf(0,0,2)
        val metadata=JSONObject().put("version",1).put("dirty",true)
            .put("save_target",target.json()).put("floating_rect",JSONArray(rectangle))
        try {AutosaveStore(context.filesDir).write(canvas,floating,metadata)}
        finally {canvas.recycle();floating.recycle()}
        if(legacy) {
            val old=Bitmap.createBitmap(11,9,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)}
            try {File(context.filesDir,"classic-recovery.png").outputStream().use {assertTrue(old.compress(Bitmap.CompressFormat.PNG,100,it))}}
            finally {old.recycle()}
            context.getSharedPreferences("classic",0).edit().putString("filename","Legacy.png").putBoolean("dirty",true).commit()
        }
    }

    @Test fun failedMetadataDoesNotInstallOldTargetOnNewCanvas()=checkRecovery(valid=false,legacy=false)
    @Test fun legacyFallbackDoesNotInheritFailedDraftTarget()=checkRecovery(valid=false,legacy=true)
    @Test fun successfulRecoveryRetainsItsSaveDestination()=checkRecovery(valid=true,legacy=false)

    @Test fun overflowingCoordinatesDoNotInstallOldTargetOnNewCanvas()=checkRecovery(valid=false,legacy=false,overflow=true)
    @Test fun legacyFallbackRejectsOverflowingSelectionCoordinates()=checkRecovery(valid=false,legacy=true,overflow=true)

    private fun checkRecovery(valid: Boolean,legacy: Boolean,overflow: Boolean=false) {
        prepare(valid,legacy,overflow)
        val original=AutosaveStore(context.filesDir).file.readBytes()
        val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity=controller.setup().get()
        try {
            awaitEditorStartup(activity)
            val installed=ReflectionHelpers.getField<SavedTarget?>(activity,"savedTarget")
            if(valid) {
                assertEquals(target,installed)
                assertEquals(7,activity.document.bitmap.width)
                assertEquals(Color.RED,activity.document.bitmap.getPixel(0,0))
            } else {
                assertNull("Failed ZIP metadata must not bind Save for replacement artwork",installed)
                assertNull("Replacement artwork must not retain invalid floating geometry",activity.document.selection)
                assertEquals(if(legacy) DocumentName.Named("Legacy.png") else DocumentName.Untitled,
                    ReflectionHelpers.getField<DocumentName>(activity,"documentName"))
                assertTrue("Failed original remains available for recovery",AutosaveStore(context.filesDir).recoveryCopies().any {it.readBytes().contentEquals(original)})
                if(legacy) {
                    assertEquals(11,activity.document.bitmap.width)
                    assertEquals(9,activity.document.bitmap.height)
                    assertEquals(Color.MAGENTA,activity.document.bitmap.getPixel(0,0))
                }
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                shadowOf(Looper.getMainLooper()).idle()
                EditorTestNavigation.named(activity,"File",activity.getString(R.string.ui_save))
                shadowOf(Looper.getMainLooper()).idle()
                val options=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                assertTrue("Save must ask for a destination, not write the failed draft's URI",options.isShowing)
                assertEquals(activity.getString(R.string.save20_title),shadowOf(options).title.toString())
                assertNull(activity.lastIoError)
                options.dismiss()
            }
        } finally {
            controller.pause().stop().destroy()
            val worker=ReflectionHelpers.getField<ExecutorService>(activity,"worker")
            assertTrue(worker.awaitTermination(10,TimeUnit.SECONDS))
            shadowOf(Looper.getMainLooper()).idle()
        }
    }
}
