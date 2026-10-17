/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.widget.Button
import android.widget.EditText
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
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
import java.io.File
import java.util.Locale

/** Real application/resource/consumer tests. Inject text after Android decoding;
 * invalid XML must still fail AAPT rather than reaching this boundary. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[21,30,35])
class LocaleTextBoundaryTest {
    private lateinit var previous: Resources
    private lateinit var previousLocale: Locale
    @Before fun save() { previous=PaintApplication.currentResources;previousLocale=Locale.getDefault() }
    @After fun restore() { PaintApplication.currentResources=previous;Locale.setDefault(previousLocale) }

    @Suppress("DEPRECATION")
    private fun inject(tag: String, strings: Map<Int,String?> = emptyMap(), plural: String? = "bad %99\$d"): Resources {
        val config=Configuration(previous.configuration).apply {setLocale(Locale.forLanguageTag(tag))}
        val base=RuntimeEnvironment.getApplication().createConfigurationContext(config).resources
        return object: Resources(base.assets,base.displayMetrics,config) {
            override fun getString(id: Int): String = if (id in strings)
                strings[id] ?: throw NotFoundException("Injected missing translation") else super.getString(id)
            override fun getQuantityString(id: Int, quantity: Int): String = if (id == R.plurals.ui_crop_preview_images)
                plural ?: throw NotFoundException("Injected missing plural") else super.getQuantityString(id,quantity)
        }.also {PaintApplication.currentResources=it}
    }

    @Test fun malformedEnglishAndOtherLocalesFallBackAtActualNumericConsumers() {
        for(tag in listOf("en-US","ar","mn-Mong","qaa-Zsye-XV")) {
            inject(tag,mapOf(R.string.ui_d_d_px_d_pixels_2f_mp to "%1\$999999999d",
                R.string.ui_1f_s to "%1\$s %2\$d",R.string.ui_current_safe_budget_2f_mp to null))
            assertEquals("640 × 480 px · Pixel count: 307,200 (0.31 MP)",ImageDimensions(640,480).describe())
            assertEquals("1.0 MiB",memoryLabel(1024.0*1024))
            assertEquals("Current safe budget: 2.50 MP.",uiRoot(R.string.ui_current_safe_budget_2f_mp,2.5))
            assertEquals("Enter positive image dimensions.",uiText(inject(tag,mapOf(R.string.ui_enter_positive_image_dimensions to "")),R.string.ui_enter_positive_image_dimensions))
        }
    }

    @Test fun fallbackPluralRulesAreEnglishAndKeepTheEntireCropWarning() {
        for(tag in listOf("en-US","ar","fr","ja","mn-Mong")) for(count in listOf(0,1,2,3,21,101)) {
            val resources=inject(tag)
            val formatted=uiText(resources,R.plurals.ui_crop_preview_images,count,Locale.ROOT,arrayOf(4,8,count))
            assertEquals("Preview: 4 × 8 px\nApply to $count ${if(count==1) "image" else "images"}. Cropping placed images may move their attached images.",formatted)
        }
        val resources=inject("ar",plural=null)
        assertEquals("Preview: 4 × 8 px\nApply to 2 images. Cropping placed images may move their attached images.",
            uiText(resources,R.plurals.ui_crop_preview_images,2,Locale.ROOT,arrayOf(4,8,2)))
    }

    @Test fun literalPercentUnicodeAndLongHelpReachTheResourceBoundaryIntact() {
        val text="100% %q \" \\ \u2028\u2029\u202eالعربية\u202c ᠮᠣᠩᠭᠣᠯ\u202f𡨸 👩🏽‍🎨\n".repeat(100)
        inject("mn-Mong",mapOf(R.string.ui_help23 to text))
        assertEquals(text,ui(R.string.ui_help23))
        val source=previous.getString(previous.getIdentifier("anpaint_source_ui_help23","string",previous.getResourcePackageName(R.string.ui_help23)))
        inject("en-US",mapOf(R.string.ui_help23 to "x".repeat(LocaleText.MAX_TEMPLATE_LENGTH+1)))
        assertEquals(source,ui(R.string.ui_help23))
    }

    @Test fun actualFormattedFalsePixelGridHelpAndPercentTranslationsStayLiteral() {
        val id=R.string.ui_pixel_grid_help33
        val source="Pixel grid appears at 800% zoom or above. Rulers show positions in image pixels."
        for (tag in listOf("en-US","ar","mn-Mong")) {
            inject(tag,mapOf(id to null))
            assertEquals(source,ui(id))
            for (text in listOf(source,"100% done", "100% satisfied", "%1\$s %2\$999999999d", "800% zoom")) {
                inject(tag,mapOf(id to text))
                assertEquals(text,ui(id))
                assertEquals(text,ui(id,"ignored"))
            }
        }
    }

    @Test fun galleryQuotesSurviveAndroidJsonEncodingAsData() {
        val use="\"\\\n\u2028\u2029\u202eᠮᠣᠩᠭᠣᠯ\u202c <img onerror=boom()> %1\$999999s"
        val copy="';globalThis.boom(); // 𡨸 👩🏽‍🎨"
        val script=GalleryPage.script(use,copy)
        assertEquals(use,org.json.JSONTokener(script.substringAfter("var useLabel=")).nextValue())
        assertEquals(copy,org.json.JSONTokener(script.substringAfter(", copyLabel=")).nextValue())
        assertTrue(script.contains("link.textContent=useLabel"))
        assertTrue(script.contains("copy.textContent=copyLabel"))
    }

    @Test fun sourceAliasesCannotResolveBackToCorruptTranslatedTargets() {
        inject("en-US",mapOf(R.string.ui_cursor_help29 to "",R.string.ui_cursor_help31 to "wrong target"))
        val id=previous.getIdentifier("anpaint_source_ui_cursor_help31","string",previous.getResourcePackageName(R.string.ui_cursor_help31))
        assertEquals(previous.getString(id),ui(R.string.ui_cursor_help29))
        assertNotEquals("wrong target",ui(R.string.ui_cursor_help29))
    }

    @Test fun duplicatePresetLabelsDoNotChangeIdentityCancelOrRepeatedActions() {
        val controller=Robolectric.buildActivity(Activity::class.java)
        val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup()
        val directory=File(activity.cacheDir,"translation-normalize-${System.nanoTime()}")
        val assembly=ImageAssembly(directory)
        var dialog: AlertDialog?=null
        try {
            val file=File(directory,"source.image").apply {writeText("no decoder is used")}
            assembly.add(listOf(AssemblyImage("small",file,"small.png",null,ImageDimensions(20,40)),
                AssemblyImage("large",file,"large.png",null,ImageDimensions(80,160))))
            inject("en-US",mapOf(R.string.ui_smallest to "same \u202e%",
                R.string.ui_largest to "same \u202e%",R.string.ui_normalize_width_info to "%99\$d"))
            repeat(2) {
                dialog=NormalizeImagesDialog(activity,assembly,NormalizeAxis.WIDTH).show()
                shadowOf(Looper.getMainLooper()).idle()
                val root=dialog!!.window!!.decorView
                val small=root.findViewWithTag<Button>("normalize_smallest")
                val large=root.findViewWithTag<Button>("normalize_largest")
                assertEquals(small.text.toString(),large.text.toString())
                val value=root.findViewWithTag<EditText>("normalize_value")
                repeat(3) {small.performClick();assertEquals("20",value.text.toString());large.performClick();assertEquals("80",value.text.toString())}
                small.performClick()
                dialog!!.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertFalse(dialog!!.isShowing)
                assertEquals(ImageDimensions(80,160),assembly.image("large").placedSize)
            }
            dialog=NormalizeImagesDialog(activity,assembly,NormalizeAxis.WIDTH).show()
            shadowOf(Looper.getMainLooper()).idle()
            dialog!!.window!!.decorView.findViewWithTag<View>("normalize_smallest").performClick()
            dialog!!.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            shadowOf(Looper.getMainLooper()).idle()
            assertEquals(ImageDimensions(20,40),assembly.image("large").placedSize)
            assertFalse(dialog!!.isShowing)
        } finally {dialog?.dismiss();controller.close();directory.deleteRecursively()}
    }
    @Test fun packagedAinuAndManchuEscapedPercentsPreserveReviewedWording() {
        val strings=listOf(R.string.ui_each_px_px_percent_is_relative_to_the,
            R.string.ui_percent_of_pixels,R.string.ui_trim_in_percent)
        val numbers=listOf(R.string.ui_normalize_width_info,R.string.ui_normalize_height_info,
            R.string.ui_normalize_width_input_percent,R.string.ui_normalize_height_input_percent)
        var checked=0
        for (tag in listOf("ain-Kana","ain-Latn","mnc-Mong")) {
            val config=Configuration(previous.configuration).apply {setLocale(Locale.forLanguageTag(tag))}
            val resources=RuntimeEnvironment.getApplication().createConfigurationContext(config).resources
            PaintApplication.currentResources=resources
            for (id in (if(tag.startsWith("ain")) strings else emptyList())+numbers) {
                val text=resources.getString(id)
                assertTrue("Packaged $tag / ${resources.getResourceEntryName(id)}",text.contains("%%"))
                val args: Array<out Any> = if(id in numbers) arrayOf(20,10,40,80)
                    else arrayOf("width","20","height","10","40","width","80")
                assertEquals(String.format(Locale.ROOT,text,*args),uiRoot(id,*args))
                checked++
            }
        }
        assertEquals(18,checked)
    }

    @Test @Config(sdk=[35])
    fun japaneseCropAccessibilityKeepsThePercentSymbol() {
        val controller=Robolectric.buildActivity(Activity::class.java)
        val activity=controller.get();activity.setTheme(R.style.ClassicPaintTheme);controller.setup()
        val config=Configuration(previous.configuration).apply {setLocale(Locale.JAPANESE)}
        PaintApplication.currentResources=activity.createConfigurationContext(config).resources
        val file=File(activity.cacheDir,"translation-crop-${System.nanoTime()}.image")
        val item=AssemblyImage("crop",file,"sample.png",null,ImageDimensions(80,160))
        var dialog: AlertDialog?=null
        var applied=false
        try {
            dialog=ImageCropDialog(activity,listOf(item),{null}) {applied=true}.show()
            shadowOf(Looper.getMainLooper()).idle()
            val root=dialog.window!!.decorView
            root.findViewWithTag<View>("crop_percent").performClick()
            val edges=mapOf("left" to "左","top" to "上","right" to "右","bottom" to "下")
            for((edge,name) in edges) {
                assertEquals("${name}の切り詰め量（%）",
                    root.findViewWithTag<EditText>("crop_$edge").contentDescription.toString())
            }
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            assertFalse(applied)
        } finally {dialog?.dismiss();controller.close();file.delete()}
    }

}
