/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import java.io.File
import java.io.ByteArrayOutputStream
import java.util.Base64
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.annotation.GraphicsMode
import android.graphics.Color
import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.RadioButton
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
import java.util.Locale

/** Bounded real-consumer checks, not native-speaker or installed-layout acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "w412dp-h900dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class LatvianPriorityWordingTest {
    private lateinit var beforeResources: Resources
    private lateinit var beforeLocale: Locale
    private lateinit var latvian: Context

    @Before fun useLatvian() {
        beforeResources = PaintApplication.currentResources
        beforeLocale = Locale.getDefault()
        val app = RuntimeEnvironment.getApplication() as Context
        latvian = app.createConfigurationContext(Configuration(app.resources.configuration).apply {
            setLocale(Locale.forLanguageTag("lv"))
        })
        PaintApplication.currentResources = latvian.resources
        // Numeric punctuation must follow the resource locale, not the process locale.
        Locale.setDefault(Locale.US)
    }

    @After fun restoreResources() {
        PaintApplication.currentResources = beforeResources
        Locale.setDefault(beforeLocale)
    }

    @Test fun liveDimensionsComposeAllFourLabelsAcrossRepeatedUnitSwitches() {
        val controls = DimensionControls(latvian, ImageDimensions(24, 16), locked = false)
        val pixels = controls.findViewWithTag<RadioButton>("size_pixels")
        val percent = controls.findViewWithTag<RadioButton>("size_percent")
        assertEquals("Pikseļi", pixels.text.toString())
        assertEquals("Procenti", percent.text.toString())
        repeat(2) {
            assertEquals("Platums pikseļos", controls.widthInput.contentDescription.toString())
            assertEquals("Augstums pikseļos", controls.heightInput.contentDescription.toString())
            assertEquals("24", controls.widthInput.text.toString())
            assertEquals("16", controls.heightInput.text.toString())
            percent.performClick()
            assertEquals("Platums procentos", controls.widthInput.contentDescription.toString())
            assertEquals("Augstums procentos", controls.heightInput.contentDescription.toString())
            assertEquals("100", controls.widthInput.text.toString())
            assertEquals("100", controls.heightInput.text.toString())
            pixels.performClick()
        }
        assertEquals(ImageDimensions(24, 16), controls.dimensions)
    }

    @Test fun livePixelSummaryIsCountNeutralForOneAndSeveralPixels() {
        val controls = DimensionControls(latvian, ImageDimensions(1, 1), locked = false)
        val result = controls.findViewWithTag<TextView>("size_result")
        for ((size, expected) in listOf(
            ImageDimensions(1, 1) to "1 × 1 px · Pikseļu skaits: 1 (0,00 MP)",
            ImageDimensions(1, 2) to "1 × 2 px · Pikseļu skaits: 2 (0,00 MP)",
            ImageDimensions(2, 2) to "2 × 2 px · Pikseļu skaits: 4 (0,00 MP)",
            ImageDimensions(3, 7) to "3 × 7 px · Pikseļu skaits: 21 (0,00 MP)"
        )) {
            controls.setDimensions(size)
            assertEquals(expected, result.text.toString())
        }
        controls.setDimensions(ImageDimensions(100, 100))
        assertEquals("100 × 100 px · Pikseļu skaits: 10\u00a0000 (0,01 MP)", result.text.toString())
    }

    @Test fun actualCategoryControlsKeepAgreementForEveryToolAndExpansion() {
        assertEquals("Zīmulis", PaintTool.PENCIL.label)
        assertEquals("Ota", PaintTool.BRUSH.label)
        for (down in listOf(false, true)) for (category in ToolCategory.values()) {
            val button = ToolCategoryButton(latvian, category, category.tools.first(), down)
            for (tool in category.tools) for (expanded in listOf(false, true)) {
                button.selectedTool = tool
                button.expanded = expanded
                button.refresh()
                val action = if (expanded) "Sakļaut" else "Izvērst"
                val expected = "${ui(category.labelId)}. Atlasītais rīks: ${tool.label}. $action rīkus un opcijas"
                assertEquals(ui(category.labelId), button.text.toString())
                assertEquals(expected, button.contentDescription.toString())
                assertEquals(expected, button.tooltipText.toString())
            }
        }
    }

    @Test fun actualAnimationWarningsKeepCountsAndCancelWithoutImporting() {
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
                val file = File.createTempFile("latvian-animation-", ".gif", activity.cacheDir).apply { writeBytes(bytes) }
                files.add(file)
                assertEquals(AnimationInfo("GIF", count, exact, false), AnimationInfo.inspect(file))
                var selected = 0; var cancelled = 0; var failure: Throwable? = null
                selection = ImportSelection(activity, worker, { 0L }, { selected++ }, { cancelled++ }, { failure = it })
                selection.start(file, "source.gif")
                worker.submit {}.get(10, TimeUnit.SECONDS)
                shadowOf(Looper.getMainLooper()).idle()
                assertNull(failure)
                val shown = checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                val countText = if (exact) count.toString() else latvian.getString(R.string.formats22_at_least_frames, count)
                val expected = latvian.getString(R.string.formats22_animation_message, "GIF", countText) + "\n\n" +
                    latvian.getString(R.string.formats22_animation_still)
                assertEquals(latvian.getString(R.string.formats22_animation_title), shadowOf(shown).title.toString())
                assertEquals(expected, shadowOf(shown).message.toString())
                assertEquals(latvian.getString(R.string.formats22_open_still), shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                assertEquals(0, selected)
                assertTrue(file.exists())
                shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                shadowOf(Looper.getMainLooper()).idle()
                assertEquals(1, cancelled)
                assertEquals(0, selected)
                assertNull(failure)
                assertFalse(shown.isShowing)
                assertFalse(file.exists())
            }
        } finally {
            selection?.dispose()
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            worker.shutdownNow()
            assertTrue(worker.awaitTermination(10, TimeUnit.SECONDS))
            files.forEach { it.delete() }
            controller.pause().stop().destroy()
        }
    }

    @Test fun actualPaletteInstructionsMatchTapAndLongPressWithoutChangingCanvas() {
        val application = RuntimeEnvironment.getApplication() as Context
        val oldTag = AppLanguage.selectedTag(application)
        AppLanguage.select(application, "lv")
        val controller = Robolectric.buildActivity(ClassicPaintActivity::class.java)
        val activity = controller.get()
        try {
            controller.setup()
            awaitEditorStartup(activity)
            EditorTestNavigation.click(activity, "menu_Color")
            val root = activity.window.decorView
            val swatch = root.findViewWithTag<View>("colour_FF0000")
            assertEquals(activity.getString(R.string.ui_colour_tap_foreground_hold_background, "FF0000"), swatch.contentDescription.toString())
            fun descriptions(view: View): List<String> = listOfNotNull(view.contentDescription?.toString()) +
                (if (view is ViewGroup) (0 until view.childCount).flatMap { descriptions(view.getChildAt(it)) } else emptyList())
            assertTrue(descriptions(root).contains(activity.getString(R.string.ui_colour_palette_tap_for_foreground_hold_for_background)))
            val bitmap = activity.document.bitmap
            val pixels = IntArray(bitmap.width * bitmap.height)
            bitmap.getPixels(pixels, 0, bitmap.width, 0, 0, bitmap.width, bitmap.height)
            activity.document.foreground = Color.BLACK; activity.document.background = Color.WHITE
            assertTrue(swatch.performClick())
            assertEquals(Color.RED, activity.document.foreground)
            assertEquals(Color.WHITE, activity.document.background)
            activity.document.foreground = Color.BLUE
            assertTrue(swatch.performLongClick())
            assertEquals(Color.BLUE, activity.document.foreground)
            assertEquals(Color.RED, activity.document.background)
            assertSame(bitmap, activity.document.bitmap)
            val after = IntArray(pixels.size)
            bitmap.getPixels(after, 0, bitmap.width, 0, 0, bitmap.width, bitmap.height)
            assertArrayEquals(pixels, after)
        } finally {
            try {
                controller.pause().stop()
                val deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(10)
                while (activity.busy && System.nanoTime() < deadline) { shadowOf(Looper.getMainLooper()).idle(); Thread.sleep(10) }
                assertFalse("Editor save did not settle", activity.busy)
            } finally {
                try {
                    controller.destroy()
                } finally {
                    AppLanguage.select(application, oldTag)
                }
            }
        }
    }
}

