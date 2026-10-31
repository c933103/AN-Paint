/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.widget.CheckBox
import android.widget.TextView
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

/** Bounded compiled-resource and consumer behavior; not layout or fluency certification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class BrazilianPortuguesePriorityWordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var portuguese: Context

    @Before fun useBrazilianPortuguese() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        val locale = Locale.forLanguageTag("pt-BR")
        val application = RuntimeEnvironment.getApplication() as Context
        val configuration = Configuration(application.resources.configuration).apply { setLocale(locale) }
        portuguese = application.createConfigurationContext(configuration)
        PaintApplication.currentResources = portuguese.resources
        Locale.setDefault(locale)
    }

    @After fun restoreResources() {
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    @Test fun actualCategoryControlsKeepAgreementWhenToolAndExpansionChange() {
        assertEquals("Lápis", PaintTool.PENCIL.label)
        assertEquals("Elipse", PaintTool.ELLIPSE.label)
        for (down in listOf(false, true)) for (category in ToolCategory.values()) {
            val button = ToolCategoryButton(portuguese, category, category.tools.first(), down)
            for (tool in category.tools) for (expanded in listOf(false, true)) {
                button.selectedTool = tool
                button.expanded = expanded
                button.refresh()
                val action = if (expanded) "Recolher" else "Expandir"
                val expected = "${ui(category.labelId)}. Ferramenta selecionada: ${tool.label}. $action ferramentas e opções"
                assertEquals(ui(category.labelId), button.text.toString())
                assertEquals(expected, button.contentDescription.toString())
                assertEquals(expected, button.tooltipText.toString())
            }
        }
    }

    @Test fun dimensionControlsKeepCountAndComposedUnitsAcrossSizeAndUnitChanges() {
        val controls = DimensionControls(portuguese, ImageDimensions(1, 1), locked = false)
        val result = controls.findViewWithTag<TextView>("size_result")
        assertEquals("1 × 1 px · Quantidade de pixels: 1 (0,00 MP)", result.text.toString())
        assertEquals("Largura em pixels", controls.widthInput.contentDescription.toString())
        assertEquals("Altura em pixels", controls.heightInput.contentDescription.toString())
        assertEquals("Pixels", controls.findViewWithTag<TextView>("size_pixels").text.toString())
        controls.setDimensions(ImageDimensions(40, 25))
        assertEquals("40 × 25 px · Quantidade de pixels: 1.000 (0,00 MP)", result.text.toString())
        controls.findViewWithTag<View>("size_percent").performClick()
        assertEquals("Largura em porcentagem", controls.widthInput.contentDescription.toString())
        assertEquals("Altura em porcentagem", controls.heightInput.contentDescription.toString())
        controls.findViewWithTag<View>("size_pixels").performClick()
        assertEquals("Largura em pixels", controls.widthInput.contentDescription.toString())
        assertEquals("Altura em pixels", controls.heightInput.contentDescription.toString())
        controls.setDimensions(ImageDimensions(2000, 1000))
        assertEquals("2000 × 1000 px · Quantidade de pixels: 2.000.000 (2,00 MP)", result.text.toString())
    }

    @Test fun noneButtonClearsActualImageChecklistAndDoesNotApplyAnEmptySelection() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var dialog: AlertDialog? = null
        try {
            val images = listOf("one", "two").map { id ->
                AssemblyImage(id, File(activity.cacheDir, "$id.image"), id, null, ImageDimensions(24, 16))
            }
            var applied = false
            val shown = ImageCropDialog(activity, images, { null }) { applied = true }.show()
            dialog = shown
            // Android queues OnShow; drain it so the production validating
            // Apply listener is installed before exercising the native button.
            shadowOf(Looper.getMainLooper()).idle()
            val root = shown.window!!.decorView
            val none = root.findViewWithTag<TextView>("crop_none")
            assertEquals("Nenhuma", none.text.toString())
            assertEquals("Aplicar a estas imagens", ui(R.string.ui_apply_to_these_images))
            images.forEach { assertTrue(root.findViewWithTag<CheckBox>("crop_include_${it.id}").isChecked) }
            none.performClick()
            images.forEach { assertFalse(root.findViewWithTag<CheckBox>("crop_include_${it.id}").isChecked) }
            shown.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
            assertFalse(applied)
            assertTrue(shown.isShowing)
            assertEquals("Escolha pelo menos uma imagem.", root.findViewWithTag<TextView>("crop_status").text.toString())
            root.findViewWithTag<View>("crop_all").performClick()
            images.forEach { assertTrue(root.findViewWithTag<CheckBox>("crop_include_${it.id}").isChecked) }
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
            shadowOf(Looper.getMainLooper()).idle()
            assertFalse(shown.isShowing)
            assertFalse(applied)
        } finally {
            dialog?.dismiss()
            controller.pause().stop().destroy()
        }
    }

}
