/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Configuration
import android.graphics.Color
import android.graphics.Rect
import android.os.Looper
import android.text.InputFilter
import android.text.InputType
import android.view.View
import android.widget.EditText
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.text.DecimalFormatSymbols
import java.util.Locale
import java.util.concurrent.Executors

/** Editable insertion exercises the real key filter; setText alone can bypass it. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[21,25,35], qualifiers="w412dp-h900dp-port-xhdpi")
class LocaleNumberInputTest {
    private fun enter(field: EditText, text: String) {
        field.setText("")
        field.text.replace(0, 0, text)
        assertEquals("Numeric syntax must reach validation unchanged", text, field.text.toString())
    }
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    @Suppress("DEPRECATION")
    private fun withActivity(tag: String, check: (Activity) -> Unit) {
        val oldLocale=Locale.getDefault()
        val oldResources=PaintApplication.currentResources
        val controller=Robolectric.buildActivity(Activity::class.java).setup()
        val activity=controller.get()
        val oldConfig=Configuration(activity.resources.configuration)
        try {
            val locale=Locale.forLanguageTag(tag)
            activity.resources.updateConfiguration(Configuration(oldConfig).apply {setLocale(locale);setLayoutDirection(locale)}, activity.resources.displayMetrics)
            PaintApplication.currentResources=activity.resources
            Locale.setDefault(locale)
            check(activity)
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            idle()
            controller.pause().stop().destroy()
            activity.resources.updateConfiguration(oldConfig,activity.resources.displayMetrics)
            PaintApplication.currentResources=oldResources
            Locale.setDefault(oldLocale)
        }
    }

    @Test @Config(sdk=[21,25]) fun legacyDefaultNumberFilterReproducesTheUnfixedLoss() = withActivity("fr") { activity ->
        val field=EditText(activity).apply {inputType=InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL}
        field.text.append("12,5")
        assertEquals("125",field.text.toString())
        field.setText("");field.text.append("١٢٫٥")
        assertEquals("",field.text.toString())
        LocaleNumberInput.configure(field,decimal=true)
        enter(field,"12,5");assertEquals(12.5,uiNumber(field.text.toString())!!,0.0)
    }

    @Test @Config(sdk=[21,25,30,35]) fun everyOfferedLocaleRetainsItsDigitsAndDecimalSyntaxWithBothImeModes() {
        val context=RuntimeEnvironment.getApplication()
        val old=Locale.getDefault()
        try {
            val tags=AppLanguage.tags(context)
            assertEquals(140,tags.size)
            for(tag in tags) {
                val locale=Locale.forLanguageTag(tag)
                val localized=context.createConfigurationContext(Configuration(context.resources.configuration).apply {setLocale(locale);setLayoutDirection(locale)})
                Locale.setDefault(locale)
                val symbols=DecimalFormatSymbols(locale)
                fun digits(value: String)=value.map {if(it in '0'..'9') (symbols.zeroDigit.code+(it-'0')).toChar() else it}.joinToString("")
                for(decimal in listOf(false,true)) {
                    val field=EditText(localized)
                    field.contentDescription="numeric purpose"
                    val limit=InputFilter.LengthFilter(20)
                    field.filters=arrayOf(limit)
                    LocaleNumberInput.configure(field,decimal)
                    assertEquals(tag,InputType.TYPE_CLASS_NUMBER or if(decimal) InputType.TYPE_NUMBER_FLAG_DECIMAL else 0,field.inputType)
                    assertEquals("numeric purpose",field.contentDescription)
                    assertTrue(field.filters.contains(limit))
                    for((text,expected) in listOf(digits("125") to 125.0,(digits("12")+symbols.decimalSeparator+digits("5")) to 12.5,"12.5" to 12.5)) {
                        enter(field,text)
                        assertEquals(tag,expected,uiNumber(field.text.toString())!!,0.0)
                    }
                    for(sign in setOf('-',symbols.minusSign)) {
                        enter(field,sign+digits("12"))
                        val parsed=uiNumber(field.text.toString())
                        assertTrue("$tag must not turn a negative into positive input",parsed==null || parsed<0)
                    }
                }
            }
        } finally {Locale.setDefault(old)}
    }

    @Test fun dimensionsKeepFractionalPercentAndRejectFractionalPixelsAfterRepeatedUnitChanges() = withActivity("fr") { activity ->
        val controls=DimensionControls(activity,ImageDimensions(200,400))
        repeat(3) {
            controls.findViewWithTag<View>("size_percent").performClick()
            enter(controls.widthInput,"12,5")
            assertEquals(ImageDimensions(25,50),controls.dimensions)
            controls.findViewWithTag<View>("size_pixels").performClick()
            assertEquals("25",controls.widthInput.text.toString())
            enter(controls.widthInput,"12,5");assertNull(controls.dimensions)
            enter(controls.widthInput,"-12");assertNull(controls.dimensions)
            enter(controls.widthInput,"200");assertEquals(ImageDimensions(200,400),controls.dimensions)
        }
        assertTrue(controls.widthInput.contentDescription.isNotEmpty())
    }

    @Test fun dimensionsAcceptArabicAndPersianDigitsAndRetainRangeValidation() {
        for((tag,value) in listOf("ar" to "١٢٥","fa" to "۱۲۵")) withActivity(tag) { activity ->
            val controls=DimensionControls(activity,ImageDimensions(200,400))
            enter(controls.widthInput,value)
            assertEquals(ImageDimensions(125,250),controls.dimensions)
            enter(controls.widthInput,"0");assertNull(controls.dimensions)
            enter(controls.widthInput,"2147483648");assertNull(controls.dimensions)
        }
    }

    @Test fun cropRetainsDecimalCommaAndRejectsFractionalPixelsOrNegativeMargins() = withActivity("fr") { activity ->
        val item=AssemblyImage("a",File(activity.cacheDir,"not-decoded.image"),"a.png",null,ImageDimensions(200,400))
        var result: Map<String,Rect>?=null
        val dialog=ImageCropDialog(activity,listOf(item),{null}) {result=it}.show();idle()
        val root=dialog.window!!.decorView
        val left=root.findViewWithTag<EditText>("crop_left")
        enter(left,"12,5");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertNull(result);assertTrue(dialog.isShowing)
        root.findViewWithTag<View>("crop_percent").performClick()
        enter(left,"-12,5");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertNull(result);assertTrue(dialog.isShowing)
        enter(left,"12,5");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertEquals(Rect(25,0,200,400),result!!.getValue("a"));assertFalse(dialog.isShowing)
    }

    @Test fun normalizationRetainsCommaAcrossModeChangesAndCancelDoesNotCommit() = withActivity("fr") { activity ->
        val directory=File(activity.cacheDir,"numeric-normalize-${System.nanoTime()}")
        val assembly=ImageAssembly(directory)
        try {
            val file=File(directory,"a.image").apply {writeText("no decoder is used")}
            assembly.add(listOf(AssemblyImage("a",file,"a.png",null,ImageDimensions(200,400))))
            val dialog=NormalizeImagesDialog(activity,assembly,NormalizeAxis.WIDTH).show();idle()
            val root=dialog.window!!.decorView
            val input=root.findViewWithTag<EditText>("normalize_value")
            enter(input,"12,5");assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            repeat(3) {
                root.findViewWithTag<View>("normalize_percent").performClick()
                enter(input,"12,5");assertTrue(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
                root.findViewWithTag<View>("normalize_pixels").performClick()
                assertEquals("25",input.text.toString())
            }
            enter(input,"-25");assertFalse(dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled)
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            assertEquals(ImageDimensions(200,400),assembly.image("a").placedSize)
            val reopened=NormalizeImagesDialog(activity,assembly,NormalizeAxis.WIDTH).show();idle()
            enter(reopened.window!!.decorView.findViewWithTag("normalize_value"),"25")
            reopened.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertEquals(ImageDimensions(25,50),assembly.image("a").placedSize)
        } finally {directory.deleteRecursively()}
    }

    @Test fun textSizeAndSpacingRetainDecimalsAndTheExistingRanges() = withActivity("fr") { activity ->
        var result: TextSettings?=null
        val dialog=TextStyleDialog(activity,TextSettings("text"),Color.BLACK,Color.WHITE) {settings,_->result=settings;true}.show();idle()
        val root=dialog.window!!.decorView
        val size=root.findViewWithTag<EditText>("text_size")
        val spacing=root.findViewWithTag<EditText>("text_spacing")
        enter(size,"12,5");enter(spacing,"125,5")
        enter(size,"-12,5");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertNull(result);assertTrue(dialog.isShowing)
        enter(size,"12,5");enter(spacing,"300,5");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertNull(result);assertTrue(dialog.isShowing)
        enter(spacing,"125,5");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertEquals(12.5f,result!!.size,0f);assertEquals(1.255f,result!!.spacing,.00001f)
    }

    @Test fun sliderRetainsArabicDigitsAndRejectsPastedFractionsAndNegativeNumbers() = withActivity("ar") { activity ->
        var result=1
        val slider=NumericSlider(activity,"size",1,1,100) {result=it}
        slider.number.performClick();idle()
        val dialog=ShadowAlertDialog.getLatestAlertDialog()!!
        val field=dialog.window!!.decorView.findViewWithTag<EditText>("numeric_input")
        for(invalid in listOf("١٢٫٥","-١٢","١٠١")) {
            enter(field,invalid);dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertTrue(dialog.isShowing);assertEquals(1,result)
        }
        enter(field,"٩٩");dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
        assertFalse(dialog.isShowing);assertEquals(99,result)
    }

    @Test fun colourRefactorKeepsCommaEntryAndNegativeRangeRejection() = withActivity("fr") { activity ->
        val picker=AdvancedColourDialog(activity,Color.RED,false) {}
        val dialog=picker.show();idle()
        val root=dialog.window!!.decorView
        val hue=root.findViewWithTag<EditText>("colour_h")
        enter(hue,"120,5");assertEquals(120.5f,picker.value.hsv[0],.001f)
        enter(hue,"-120,5");assertNotNull(hue.error)
        assertEquals(120.5f,picker.value.hsv[0],.001f)
    }

    @Test fun pageFieldRetainsPersianDigitsAndDisablesFractionalNegativeAndOutOfRangeEntries() = withActivity("fa") { activity ->
        val worker=Executors.newSingleThreadExecutor()
        val selection=ImportSelection(activity,worker,{0L},{},{},{throw AssertionError(it)})
        try {
            // Exercise the actual page form without staging/decoding a document.
            ImportSelection::class.java.getDeclaredMethod("showPages",String::class.java,Int::class.javaPrimitiveType).apply {isAccessible=true}.invoke(selection,"TIFF",20)
            idle()
            val dialog=ShadowAlertDialog.getLatestAlertDialog()!!
            val field=dialog.window!!.decorView.findViewWithTag<EditText>("import_page_number")
            val open=dialog.getButton(AlertDialog.BUTTON_POSITIVE)
            for(invalid in listOf("۱۲٫۵","-۱۲","۲۱","۰")) {enter(field,invalid);assertFalse(open.isEnabled)}
            enter(field,"۱۲");assertTrue(open.isEnabled)
            assertTrue(field.contentDescription.isNotEmpty())
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();assertFalse(dialog.isShowing)
        } finally {selection.dispose();worker.shutdownNow()}
    }
}
