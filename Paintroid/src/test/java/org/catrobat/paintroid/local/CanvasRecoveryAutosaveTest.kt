/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.os.Looper
import android.net.Uri
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.json.JSONArray
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
class CanvasRecoveryAutosaveTest {
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
    private fun checkMalformed(canvas: JSONObject,legacy: Boolean) {
        val target=SavedTarget(Uri.parse("content://documents/previous-canvas"),"Previous.png",ExportOptions(ImageFormat.PNG))
        val metadata=JSONObject().put("version",1).put("dirty",true).put("canvas",canvas).put("save_target",target.json())
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
            assertNull(ReflectionHelpers.getField<SavedTarget?>(activity,"savedTarget"))
            assertEquals(if(legacy) DocumentName.Recovered else DocumentName.Untitled,ReflectionHelpers.getField<DocumentName>(activity,"documentName"))
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
            assertNull(ReflectionHelpers.getField<SavedTarget?>(second.get(),"savedTarget"))
            assertEquals(width,second.get().document.bitmap.width);assertEquals(height,second.get().document.bitmap.height)
            assertEquals(Color.GREEN,second.get().document.bitmap.getPixel(0,0))
            assertTrue(AutosaveStore(context.filesDir).recoveryCopies().any {it.readBytes().contentEquals(original)})
        } finally {finish(second)}
    }

    @Test fun truncatedCurvePreservesOriginalAndNewCanvasCanAutosave()=
        checkMalformed(JSONObject().put("curve_points",JSONArray(listOf(0,0))),false)
    @Test fun truncatedPolygonDoesNotBindFailedIdentityToLegacyFallback()=
        checkMalformed(JSONObject().put("polygon",JSONArray().put(JSONArray(listOf(0)))),true)
    @Test fun truncatedBoundsPreservesOriginalAndNewCanvasCanAutosave()=
        checkMalformed(JSONObject().put("bounds",JSONArray(listOf(0,0,2))),false)
    @Test fun reversedBoundsDoesNotPoisonLegacyFallback()=
        checkMalformed(JSONObject().put("bounds",JSONArray(listOf(2,0,1,2))),true)
    @Test fun overflowingPendingPointPreservesOriginalAndNewCanvasCanAutosave()=
        checkMalformed(JSONObject().put("polygon",JSONArray().put(JSONArray(listOf(1e300,0)))),false)

    @Test fun directMalformedRestorePreservesExistingPendingGeometryAndSettings() {
        val document=PaintDocument()
        try {
            val canvas=PaintCanvas(context,document)
            val valid=JSONObject().put("pencil_size",7).put("tool","CURVE").put("curve_stage",1)
                .put("polygon",JSONArray().put(JSONArray(listOf(-2,3))).put(JSONArray(listOf(4,5))))
                .put("curve_points",JSONArray(listOf(1,2,3,4,5,6,7,8)))
                .put("bounds",JSONArray(listOf(-1,-2,4,5)))
            canvas.restoreDraft(valid)
            val before=canvas.draftState()
            val malformed=JSONObject().put("pencil_size",99).put("curve_points",JSONArray(listOf(0,0)))
            try {canvas.restoreDraft(malformed);fail("Truncated pending curve must reject")} catch(_: org.json.JSONException) {}
            assertEquals(7f,document.pencilWidth,0f)
            val after=canvas.draftState()
            for(key in listOf("polygon","curve_points","bounds")) assertEquals(before.getJSONArray(key).toString(),after.getJSONArray(key).toString())
            assertEquals(1,after.getInt("curve_stage"))
            // Legacy absent optional geometry remains accepted.
            PaintCanvas(context,document).restoreDraft(JSONObject())
        } finally {document.close()}
    }
}
