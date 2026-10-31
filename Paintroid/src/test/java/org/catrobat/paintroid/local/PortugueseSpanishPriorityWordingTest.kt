/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.CheckBox
import android.widget.EditText
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.io.IOException
import java.util.Base64
import java.util.Locale

/** Exact compiled resources and real consumers; not installed UI or native-reader certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class PortugueseSpanishPriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String
    // Current compiled labels are the oracle for control binding, not approval history.
    private fun expected(tag: String, key: String) = PriorityWordingExpectations.resourceText(tag,key)
    private fun formatted(tag: String, key: String, vararg args: Any) =
        String.format(Locale.forLanguageTag(tag),expected(tag,key),*args)
    private fun cropText(tag: String,count: Int,width: Int=24,height: Int=16) =
        PriorityWordingExpectations.resources(tag).getQuantityString(R.plurals.ui_crop_preview_images,count,width,height,count)
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()

    @Before fun rememberLanguage() {
        previousResources=PaintApplication.currentResources;previousLocale=Locale.getDefault()
        previousTag=AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
    }
    @After fun restoreLanguage() {
        AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
        PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
    }
    private fun forEachLocale(tags: List<String> = listOf("pt-PT","es-ES"),check: (String,Activity)->Unit) {
        for(tag in tags) {
            val controller=Robolectric.buildActivity(Activity::class.java)
            val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup()
            try {
                AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
                assertEquals(tag,AppLanguage.selectedTag(activity))
                Locale.setDefault(Locale.US)
                check(tag,activity)
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                AppLanguage.select(activity,previousTag);AppLanguage.refresh(activity)
                controller.pause().stop().destroy()
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }
    private fun allText(view: View): List<String> {
        val result=mutableListOf<String>()
        if(view is TextView)result.add(view.text.toString())
        if(view is ViewGroup)for(i in 0 until view.childCount)result.addAll(allText(view.getChildAt(i)))
        return result
    }

    @Test fun actualDimensionControlsHandleOneTwoGroupedCountsAndRepeatedUnitChanges() = forEachLocale { tag,activity ->
        val controls=DimensionControls(activity,ImageDimensions(1,1),locked=false)
        val result=controls.findViewWithTag<TextView>("size_result")
        val label=if(tag=="pt-PT") "Contagem de píxeis" else "Número de píxeles"
        assertEquals("1 × 1 px · $label: 1 (0,00 MP)",result.text.toString())
        controls.setDimensions(ImageDimensions(2,1))
        assertEquals("2 × 1 px · $label: 2 (0,00 MP)",result.text.toString())
        for(size in listOf(ImageDimensions(40,25),ImageDimensions(2000,1000))) {
            controls.setDimensions(size)
            assertEquals(formatted(tag,"ui_d_d_px_d_pixels_2f_mp",size.width,size.height,size.pixels,size.pixels/1_000_000.0),result.text.toString())
        }
        for(percent in listOf(false,true,false)) {
            controls.findViewWithTag<View>(if(percent) "size_percent" else "size_pixels").performClick()
            val unit=expected(tag,if(percent) "ui_percent_fd8671" else "ui_pixels_6ec9c2")
            assertEquals(formatted(tag,"ui_width_in",unit),controls.widthInput.contentDescription.toString())
            assertEquals(formatted(tag,"ui_height_in",unit),controls.heightInput.contentDescription.toString())
            assertEquals(expected(tag,"ui_percent"),controls.findViewWithTag<TextView>("size_percent").text.toString())
            assertEquals(ImageDimensions(2000,1000),controls.dimensions)
        }
        controls.widthInput.setText("")
        assertNull(controls.dimensions)
        assertEquals(expected(tag,"ui_enter_positive_dimensions_that_resolve_to_at_least"),result.text.toString())
    }

    @Test fun realSpanishExportAndLosslessDialogsKeepCompleteExplanationsAndCancelWithoutSaving() = forEachLocale(listOf("es-ES")) { tag,activity ->
        var confirmed=false;var canceled=0
        var dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.ASCII_ART),
            confirm={confirmed=true},cancel={canceled++},export=true).show()
        try {
            shadowOf(Looper.getMainLooper()).idle()
            assertTrue(allText(dialog.window!!.decorView).contains(expected(tag,"ui_export_explanation23")))
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(dialog.isShowing);assertFalse(confirmed);assertEquals(1,canceled)
        } finally { dialog.dismiss() }
        dialog=SaveOptionsDialog(activity,ExportOptions(ImageFormat.WEBP),
            confirm={confirmed=true},cancel={canceled++}).show()
        try {
            shadowOf(Looper.getMainLooper()).idle()
            val root=dialog.window!!.decorView
            val lossless=root.findViewWithTag<CheckBox>("export_lossless")
            for(checked in listOf(false,true,false)) {
                lossless.isChecked=checked
                assertEquals(expected(tag,"ui_higher_quality_usually_makes_a_larger_file_lossless"),root.findViewWithTag<TextView>("export_description").text.toString())
            }
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(dialog.isShowing);assertFalse(confirmed);assertEquals(2,canceled)
        } finally { dialog.dismiss() }
    }

    @Test fun zeroBudgetRejectsOnePixelWithCompleteSingularWarning() = forEachLocale() { tag,_ ->
        val mib=1024L*1024
        val policy=ImageMemoryPolicy.calculate(256*mib,0,0,0,false)
        assertEquals(0L,policy.maxPixels())
        for(size in listOf(ImageDimensions(1,1),ImageDimensions(2,1),ImageDimensions(2000,1000))) {
            val error=assertThrows(ImageSizeException::class.java) { policy.check(size.width,size.height) }
            assertEquals(formatted(tag,"ui_d_d_pixels_2f_mp_exceeds_the_current",size.width,size.height,size.pixels/1_000_000.0,0.0),error.message)
            assertTrue(error.message!!.startsWith(if(tag=="pt-PT") "Uma imagem de " else "Una imagen de "))
            assertTrue(error.message!!.endsWith(if(tag=="pt-PT") "Não foi aplicado qualquer redimensionamento automático." else "No se aplicó ningún cambio de tamaño automático."))
        }
    }

    @Test fun actualCropFieldsKeepAllFourEdgesAcrossRepeatedUnitTogglesAndCancel() = forEachLocale() { tag,activity ->
        val image=AssemblyImage("fixture",File(activity.cacheDir,"fixture.image"),"fixture",null,ImageDimensions(24,16))
        var applied=false
        val shown=ImageCropDialog(activity,listOf(image),{null}) { applied=true }.show()
        try {
            shadowOf(Looper.getMainLooper()).idle()
            val root=shown.window!!.decorView
            val edges=mapOf("left" to "ui_left","top" to "ui_top","right" to "ui_right","bottom" to "ui_bottom")
            for(percent in listOf(false,true,false)) {
                root.findViewWithTag<View>(if(percent) "crop_percent" else "crop_pixels").performClick()
                val key=if(percent) "ui_trim_in_percent" else "ui_trim_in_pixels"
                for((edge,label) in edges) assertEquals(formatted(tag,key,expected(tag,label)),root.findViewWithTag<EditText>("crop_$edge").contentDescription.toString())
            }
            root.findViewWithTag<EditText>("crop_left").setText("2")
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();shadowOf(Looper.getMainLooper()).idle()
            assertFalse(applied);assertFalse(shown.isShowing)
            assertEquals(android.graphics.Rect(0,0,24,16),image.crop)
            if(tag=="pt-PT") {
                val cut=ActionButton(activity,EditIcon.CUT)
                assertEquals("Cortar",cut.contentDescription.toString())
                assertEquals("Cortar",cut.tooltipText.toString())
                assertEquals("Recortar imagem",ui(R.string.ui_crop_image))
            }
        } finally { shown.dismiss() }
    }

}
