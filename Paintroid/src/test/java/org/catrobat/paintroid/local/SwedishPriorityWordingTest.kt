/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Color
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.Spinner
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
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import java.io.ByteArrayOutputStream
import java.io.File
import java.util.Base64
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

/** Real consumers of bounded Swedish wording; no installed-layout or fluency claim. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class SwedishPriorityWordingTest {
    private lateinit var beforeResources: Resources
    private lateinit var beforeLocale: Locale
    private lateinit var swedish: Context
    @Before fun useSwedish() {
        beforeResources = PaintApplication.currentResources
        beforeLocale = Locale.getDefault()
        val app = RuntimeEnvironment.getApplication() as Context
        swedish = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("sv"))
        })
        PaintApplication.currentResources = swedish.resources
        Locale.setDefault(Locale.US)
    }
    @After fun restoreResources() {
        PaintApplication.currentResources = beforeResources
        Locale.setDefault(beforeLocale)
    }
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    private fun texts(view: View): List<String> =
        (if (view is TextView) listOf(view.text.toString()) else emptyList()) +
            (if (view is ViewGroup) (0 until view.childCount).flatMap { texts(view.getChildAt(it)) } else emptyList())

    @Test fun actualCategoryButtonsUseLineWatercolorAndNeutralSelectedToolGrammar() {
        assertEquals("Linje", PaintTool.LINE.label)
        assertEquals("Akvarell", PaintTool.WATERCOLOR.label)
        for (down in listOf(false, true)) for (category in ToolCategory.values()) {
            val button = ToolCategoryButton(swedish, category, category.tools.first(), down)
            for (tool in category.tools) for (expanded in listOf(false, true)) {
                button.selectedTool = tool; button.expanded = expanded; button.refresh()
                val action = if (expanded) "Dölj" else "Visa"
                val expected = "${ui(category.labelId)}. Valt verktyg: ${tool.label}. $action verktyg och alternativ"
                assertEquals(ui(category.labelId), button.text.toString())
                assertEquals(expected, button.contentDescription.toString())
                assertEquals(expected, button.tooltipText.toString())
            }
        }
    }

    @Test fun pickerExplainsFallbackAndCancelKeepsTheSelectedLanguage() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var dialog: AlertDialog? = null
        try {
            val selected = AppLanguage.selectedTag(activity)
            var changed = false
            val shown = AppLanguage.showPicker(activity) { changed = true }; dialog = shown
            val expected = "Appens språk\n\nÖversättningarna underhålls i AN Paints språkresurser. Ny eller oöversatt text visas på engelska."
            assertTrue(texts(shown.window!!.decorView).contains(expected))
            assertEquals("Appens språk", ui(R.string.language20_app_language))
            assertEquals("Använd enhetens språk", ui(R.string.language20_device_default))
            shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
            assertFalse(shown.isShowing); assertFalse(changed)
            assertEquals(selected, AppLanguage.selectedTag(activity))
        } finally {
            dialog?.dismiss(); controller.pause().stop().destroy()
        }
    }

    @Test fun saveExportAndShareShowDistinctCompleteGuidanceOnRepeatedOpenAndCancel() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        var shown: AlertDialog? = null
        var confirmed = 0; var cancelled = 0
        try {
            val cases = listOf(
                Triple(false, false, "Välj ett bildformat och dess komprimeringsinställningar. Spara återanvänder detta filnamn, denna plats, detta format och dessa inställningar."),
                Triple(false, true, "Exportera en ikon, Base64-text eller ASCII-konst. Exporten ändrar varken den aktuella bilden eller platsen som används av Spara."),
                Triple(true, true, "Spara en kopia på önskad plats och välj sedan en app att dela den med. Den aktuella platsen som används av Spara förblir oförändrad.")
            )
            repeat(2) {
                for ((share, export, expected) in cases) {
                    val dialog = SaveOptionsDialog(activity, ExportOptions(), share = share,
                        confirm = { confirmed++ }, cancel = { cancelled++ }, initialFilename = "test.png", export = export).show()
                    shown = dialog
                    assertTrue(texts(dialog.window!!.decorView).contains(expected))
                    val formats = dialog.window!!.decorView.findViewWithTag<Spinner>("export_format")
                    assertEquals("Filformat", formats.contentDescription.toString())
                    if (export) {
                        EditorTestNavigation.format(formats, ImageFormat.ASCII_ART)
                        assertTrue(texts(dialog.window!!.decorView).contains("Skriver vanlig text med ljusa och mörka tecken. Visa texten med ett typsnitt med fast teckenbredd. Detta är en visuell återgivning som inte kan öppnas igen som originalbilden."))
                    } else {
                        EditorTestNavigation.format(formats, ImageFormat.GIF)
                        assertTrue(texts(dialog.window!!.decorView).contains("Stillbild med upp till 256 färger. Färgutjämning ger mjukare färgövergångar. När en animerad GIF-fil öppnas visas endast den första bildrutan."))
                    }
                    dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
                    assertFalse(dialog.isShowing); assertEquals(0, confirmed)
                }
            }
            assertEquals(6, cancelled)
        } finally {
            shown?.dismiss(); controller.pause().stop().destroy()
        }
    }

    @Test fun actualAnimationWarningsKeepExactAndLowerBoundCountsAndCancelWithoutImporting() {
        val controller = Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        val activity = controller.setup().get()
        val worker = Executors.newSingleThreadExecutor()
        var selection: ImportSelection? = null
        val files = mutableListOf<File>()
        try {
            for ((count, exact) in listOf(2 to true, 21 to true, 21 to false, 101 to true)) {
                val bytes = ByteArrayOutputStream().apply {
                    write(Base64.getDecoder().decode("R0lGODlhAQABAIAAAAAAAP///w=="))
                    repeat(count) { write(Base64.getDecoder().decode("LAAAAAABAAEAAAICRAEA")) }
                    if (!exact) repeat(100_001) { write(byteArrayOf(0x21, 0xfe.toByte(), 1, 0x78, 0)) }
                    write(0x3b)
                }.toByteArray()
                val file = File.createTempFile("swedish-animation-", ".gif", activity.cacheDir).apply { writeBytes(bytes) }; files.add(file)
                assertEquals(AnimationInfo("GIF", count, exact, false), AnimationInfo.inspect(file))
                var selected = 0; var cancelled = 0; var failure: Throwable? = null
                selection = ImportSelection(activity, worker, { 0L }, { selected++ }, { cancelled++ }, { failure = it })
                selection.start(file, "source.gif")
                worker.submit {}.get(10, TimeUnit.SECONDS); idle()
                assertNull(failure)
                val shown = checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                val countText = if (exact) count.toString() else "minst $count"
                val expected = "Den här GIF-filen innehåller $countText bildrutor. AN Paint redigerar stillbilder och bevarar inte animeringar.\n\nEndast den första bildrutan importeras. När du sparar skapas en stillbild."
                assertEquals("Animerad bild", shadowOf(shown).title.toString())
                assertEquals(expected, shadowOf(shown).message.toString())
                assertEquals("Öppna stillbild", shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(0, selected); assertTrue(file.exists())
                shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
                assertEquals(1, cancelled); assertEquals(0, selected); assertNull(failure)
                assertFalse(shown.isShowing); assertFalse(file.exists())
            }
        } finally {
            selection?.dispose(); ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            worker.shutdownNow()
            try { assertTrue(worker.awaitTermination(10, TimeUnit.SECONDS)) }
            finally { files.forEach { it.delete() }; controller.pause().stop().destroy() }
        }
    }

    @Test fun keepEditingFromTheActualNewImageGuardPreservesDirtyPixelsAndCanBeRepeated() {
        val application = RuntimeEnvironment.getApplication() as Context
        val oldTag = AppLanguage.selectedTag(application)
        AppLanguage.select(application, "sv")
        val controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity = controller.get()
        try {
            controller.setup(); awaitEditorStartup(activity)
            activity.document.newImage(5, 7)
            activity.document.bitmap.setPixel(2, 3, Color.MAGENTA)
            activity.document.edited(); idle()
            val bitmap = activity.document.bitmap
            repeat(2) {
                EditorTestNavigation.named(activity, "File", "Ny…")
                val dialog = checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                assertEquals("Den aktuella bilden har osparade ändringar.", shadowOf(dialog).message.toString())
                assertEquals("Spara", dialog.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals("Förkasta ändringar", dialog.getButton(AlertDialog.BUTTON_NEUTRAL).text.toString())
                assertEquals("Fortsätt redigera", dialog.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick(); idle()
                assertFalse(dialog.isShowing); assertFalse(activity.isFinishing)
                assertTrue(activity.document.dirty); assertSame(bitmap, activity.document.bitmap)
                assertEquals(Color.MAGENTA, bitmap.getPixel(2, 3))
            }
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            try { controller.pause().stop().destroy() }
            finally { AppLanguage.select(application, oldTag) }
        }
    }

    @Test fun actualShapeOptionsDistinguishOutlineFromSolidFillWithoutDrawing() {
        val application = RuntimeEnvironment.getApplication() as Context
        val oldTag = AppLanguage.selectedTag(application)
        AppLanguage.select(application, "sv")
        val controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity = controller.get()
        try {
            controller.setup(); awaitEditorStartup(activity)
            activity.document.newImage(5, 7)
            activity.document.shapeStyle = 0
            val bitmap = activity.document.bitmap
            EditorTestNavigation.click(activity, "category_INSERT")
            EditorTestNavigation.click(activity, "tool_RECTANGLE")
            val choice = activity.window.decorView.findViewWithTag<TextView>("tool_option")
            assertEquals("Kontur", choice.text.toString())
            assertTrue(choice.performClick()); idle()
            val dialog = checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
            assertEquals("Kontur", dialog.listView.adapter.getItem(0).toString())
            assertEquals("Enfärgad fyllning", dialog.listView.adapter.getItem(1).toString())
            assertTrue(dialog.listView.performItemClick(null, 1, 1L)); idle()
            assertEquals(1, activity.document.shapeStyle)
            assertEquals("Enfärgad fyllning", choice.text.toString()); assertFalse(dialog.isShowing)
            assertSame(bitmap, activity.document.bitmap)
            assertEquals(Color.WHITE, bitmap.getPixel(2, 3))
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            try { controller.pause().stop().destroy() }
            finally { AppLanguage.select(application, oldTag) }
        }
    }
}
