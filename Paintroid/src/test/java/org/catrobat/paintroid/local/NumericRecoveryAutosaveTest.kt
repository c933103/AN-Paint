/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.os.Looper
import org.catrobat.paintroid.classic.*
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
import org.robolectric.android.controller.ActivityController
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.util.concurrent.ExecutorService
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33],qualifiers="w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class NumericRecoveryAutosaveTest {
    private val context get()=RuntimeEnvironment.getApplication() as Context
    @Before fun clean() {
        AutosaveStore(context.filesDir).exists()
        context.filesDir.listFiles()?.filter {it.name.startsWith("classic-") && it.isFile}?.forEach {assertTrue(it.delete())}
        listOf("classic","classic-ui","export").forEach {context.getSharedPreferences(it,0).edit().clear().commit()}
    }
    private fun finish(controller: ActivityController<ClassicPaintActivity>) {
        val activity=controller.get()
        controller.pause().stop().destroy() // Exercises real autosave serialization and final write.
        assertTrue(ReflectionHelpers.getField<ExecutorService>(activity,"worker").awaitTermination(10,TimeUnit.SECONDS))
        shadowOf(Looper.getMainLooper()).idle()
    }
    private fun checkOverflow(key: String,legacy: Boolean) {
        val metadata=JSONObject().put("version",1).put("dirty",true)
        if(key.startsWith("text_")) metadata.put("text_settings",JSONObject().put(key.removePrefix("text_"),1e300))
        else metadata.put(key,1e300)
        val image=Bitmap.createBitmap(7,5,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.RED)}
        try {AutosaveStore(context.filesDir).write(image,null,metadata)} finally {image.recycle()}
        val original=AutosaveStore(context.filesDir).file.readBytes()
        if(legacy) {
            val old=Bitmap.createBitmap(11,9,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.MAGENTA)}
            try {File(context.filesDir,"classic-recovery.png").outputStream().use {assertTrue(old.compress(Bitmap.CompressFormat.PNG,100,it))}}
            finally {old.recycle()}
        }
        val first=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        val activity=first.get()
        var width=0;var height=0
        try {
            awaitEditorStartup(activity)
            assertEquals(5f,activity.document.strokeWidth,0f)
            assertEquals(16f,activity.document.cornerRadius,0f)
            assertEquals(0f,activity.document.tolerance,0f)
            assertEquals(10f,activity.document.sprayRadius,0f)
            assertEquals(TextSettings(),ReflectionHelpers.getField<TextSettings>(activity,"textSettings"))
            assertTrue(AutosaveStore(context.filesDir).recoveryCopies().any {it.readBytes().contentEquals(original)})
            if(legacy) {assertEquals(11,activity.document.bitmap.width);assertEquals(Color.MAGENTA,activity.document.bitmap.getPixel(0,0))}
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            width=activity.document.bitmap.width;height=activity.document.bitmap.height
            activity.document.bitmap.setPixel(0,0,Color.GREEN);activity.document.edited()
        } finally {finish(first)}
        val written=AutosaveStore(context.filesDir).read {_,_->}
        try {
            for(field in listOf("stroke_width","corner_radius","tolerance","spray_radius")) assertTrue(written.metadata.getDouble(field).toFloat().isFinite())
            assertEquals(Color.GREEN,written.image.getPixel(0,0))
        } finally {written.image.recycle();written.floating?.recycle()}
        val second=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
        try {
            awaitEditorStartup(second.get())
            assertEquals(width,second.get().document.bitmap.width);assertEquals(height,second.get().document.bitmap.height)
            assertEquals(Color.GREEN,second.get().document.bitmap.getPixel(0,0))
            assertTrue(AutosaveStore(context.filesDir).recoveryCopies().any {it.readBytes().contentEquals(original)})
        } finally {finish(second)}
    }
    @Test fun strokeOverflowRejectsBeforeAdoptionAndNewCanvasCanAutosave()=checkOverflow("stroke_width",false)
    @Test fun cornerOverflowDoesNotPoisonLegacyFallbackAutosave()=checkOverflow("corner_radius",true)
    @Test fun toleranceOverflowRejectsBeforeAdoptionAndNewCanvasCanAutosave()=checkOverflow("tolerance",false)
    @Test fun sprayOverflowDoesNotPoisonLegacyFallbackAutosave()=checkOverflow("spray_radius",true)
    @Test fun textSizeOverflowRejectsBeforeAdoptionAndNewCanvasCanAutosave()=checkOverflow("text_size",false)
    @Test fun textSpacingOverflowDoesNotPoisonLegacyFallbackAutosave()=checkOverflow("text_spacing",true)
    @Test fun finiteFractionalSettingsRemainUnchangedAcrossRecoveryAndAutosave() {
        val metadata=JSONObject().put("version",1).put("stroke_width",2.75).put("corner_radius",3.125)
            .put("tolerance",0.375).put("spray_radius",7.5)
            .put("text_settings",TextSettings(size=19.25f,spacing=1.125f).json())
        val image=Bitmap.createBitmap(7,5,Bitmap.Config.ARGB_8888).apply {eraseColor(Color.BLUE)}
        try {AutosaveStore(context.filesDir).write(image,null,metadata)} finally {image.recycle()}
        repeat(2) {
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java).setup()
            try {
                val activity=controller.get();awaitEditorStartup(activity)
                assertEquals(2.75f,activity.document.strokeWidth,0f)
                assertEquals(3.125f,activity.document.cornerRadius,0f)
                assertEquals(0.375f,activity.document.tolerance,0f)
                assertEquals(7.5f,activity.document.sprayRadius,0f)
                assertEquals(TextSettings(size=19.25f,spacing=1.125f),ReflectionHelpers.getField<TextSettings>(activity,"textSettings"))
                assertEquals(Color.BLUE,activity.document.bitmap.getPixel(0,0))
                assertTrue(AutosaveStore(context.filesDir).recoveryCopies().isEmpty())
                activity.document.edited()
            } finally {finish(controller)}
        }
    }

}
