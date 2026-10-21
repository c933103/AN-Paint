/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.content.res.Configuration
import android.graphics.Rect
import android.os.Looper
import android.text.InputType
import android.widget.EditText
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.shadows.ShadowAlertDialog
import java.io.File
import java.text.DecimalFormatSymbols
import java.util.Locale

/** Paste through Editable, then exercise the unchanged parsers and real dialog consumers. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [21, 25, 35], qualifiers = "w412dp-h900dp-port-xhdpi")
class UnicodeMinusInputTest {
    private val locales = listOf("cs", "sv", "en", "ar", "fa", "he")
    private fun idle() = shadowOf(Looper.getMainLooper()).idle()
    private fun paste(field: EditText, value: String) {
        field.setText("")
        field.text.replace(0, 0, value)
    }
    private fun digits(value: String, symbols: DecimalFormatSymbols) = value.map {
        if (it in '0'..'9') (symbols.zeroDigit.code + (it - '0')).toChar() else it
    }.joinToString("")

    @Suppress("DEPRECATION")
    private fun withActivity(tag: String, check: (Activity, DecimalFormatSymbols) -> Unit) {
        val oldLocale = Locale.getDefault()
        val oldResources = PaintApplication.currentResources
        val controller = Robolectric.buildActivity(Activity::class.java)
        val activity = controller.get()
        activity.setTheme(R.style.ClassicPaintTheme)
        controller.setup()
        val oldConfig = Configuration(activity.resources.configuration)
        try {
            val locale = Locale.forLanguageTag(tag)
            activity.resources.updateConfiguration(Configuration(oldConfig).apply {
                setLocale(locale)
                setLayoutDirection(locale)
            }, activity.resources.displayMetrics)
            PaintApplication.currentResources = activity.resources
            Locale.setDefault(locale)
            assertEquals(locale, activity.resources.configuration.locale)
            assertEquals(locale, Locale.getDefault())
            check(activity, DecimalFormatSymbols(locale))
        } finally {
            ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
            idle()
            controller.pause().stop().destroy()
            activity.resources.updateConfiguration(oldConfig, activity.resources.displayMetrics)
            PaintApplication.currentResources = oldResources
            Locale.setDefault(oldLocale)
        }
    }

    @Test fun unicodeMinusReachesTheParserUnchangedInBothKeyboardModes() {
        for (tag in locales) withActivity(tag) { activity, symbols ->
            if (tag in listOf("cs", "en")) assertEquals('-', symbols.minusSign)
            if (tag == "sv") assertEquals('\u2212', symbols.minusSign)
            for (decimal in listOf(false, true)) {
                val field = EditText(activity)
                LocaleNumberInput.configure(field, decimal)
                val expectedMode = InputType.TYPE_CLASS_NUMBER or if (decimal) InputType.TYPE_NUMBER_FLAG_DECIMAL else 0
                assertEquals(expectedMode, field.inputType)
                for (value in listOf("\u221212", "\u2212" + digits("12", symbols))) {
                    paste(field, value)
                    assertEquals("$tag must retain the pasted minus", value, field.text.toString())
                    val parsed = uiNumber(field.text.toString())
                    when (tag) {
                        "cs", "en" -> assertNull("$tag rejects unsupported U+2212", parsed)
                        "sv" -> assertEquals(-12.0, parsed!!, 0.0)
                        else -> assertTrue("$tag must reject or parse as negative", parsed == null || parsed == -12.0)
                    }
                    assertNull("Integer callers remain strict", field.text.toString().toIntOrNull())
                }
            }
        }
    }

    @Test fun unicodeMinusCannotCommitAsAPositiveCoordinate() {
        for (tag in locales) withActivity(tag) { activity, symbols ->
            withAssembly(activity) { assembly, project ->
                val originalLayout = assembly.layout()
                val originalImages = assembly.images
                val originalBytes = project.readBytes()
                for (fieldTag in listOf("assembly_position_x", "assembly_position_y")) {
                    val dialog = AssemblyPositionDialog(activity, assembly, "a").show()
                    idle()
                    val field = dialog.window!!.decorView.findViewWithTag<EditText>(fieldTag)
                    val input = "\u2212" + digits("1", symbols)
                    paste(field, input)
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
                    idle()
                    // These assertions deliberately follow Apply: the baseline test must
                    // expose an accepted positive mutation, not only a changed string.
                    assertEquals("$tag $fieldTag must not move the image", originalLayout, assembly.layout())
                    assertEquals(originalImages, assembly.images)
                    assertArrayEquals(originalBytes, project.readBytes())
                    assertTrue(dialog.isShowing)
                    assertEquals(input, field.text.toString())
                    dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                    idle()
                    assertFalse(dialog.isShowing)
                    assertEquals(originalLayout, assembly.layout())
                    assertArrayEquals(originalBytes, project.readBytes())
                }
            }
        }
    }

    @Test fun nativeSignsStrictValidationCancelAndValidCoordinatesRemainUnchanged() {
        for (tag in locales) withActivity(tag) { activity, symbols ->
            withAssembly(activity) { assembly, project ->
                val layout = assembly.layout()
                val saved = project.readBytes()
                val dialog = AssemblyPositionDialog(activity, assembly, "a").show()
                idle()
                val root = dialog.window!!.decorView
                val x = root.findViewWithTag<EditText>("assembly_position_x")
                val y = root.findViewWithTag<EditText>("assembly_position_y")
                val nativeNegative = symbols.minusSign + digits("1", symbols)
                for (invalid in listOf("-1", nativeNegative, "1" + symbols.decimalSeparator + "5", "2147483648", "")) {
                    paste(x, invalid)
                    assertEquals(invalid, x.text.toString())
                    dialog.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
                    idle()
                    assertTrue(dialog.isShowing)
                    assertEquals(layout, assembly.layout())
                    assertArrayEquals(saved, project.readBytes())
                }
                paste(x, digits("24", symbols))
                paste(y, digits("36", symbols))
                dialog.getButton(AlertDialog.BUTTON_NEGATIVE).performClick()
                idle()
                assertFalse(dialog.isShowing)
                assertEquals(layout, assembly.layout())
                assertArrayEquals(saved, project.readBytes())
                val reopened = AssemblyPositionDialog(activity, assembly, "a").show()
                idle()
                val reopenedRoot = reopened.window!!.decorView
                paste(reopenedRoot.findViewWithTag("assembly_position_x"), digits("24", symbols))
                paste(reopenedRoot.findViewWithTag("assembly_position_y"), digits("36", symbols))
                reopened.getButton(AlertDialog.BUTTON_POSITIVE).performClick()
                idle()
                assertFalse(reopened.isShowing)
                assertEquals(Rect(24, 36, 224, 436), assembly.layout().getValue("a"))
                assertEquals(layout.getValue("b"), assembly.layout().getValue("b"))
            }
        }
    }

    private fun withAssembly(activity: Activity, check: (ImageAssembly, File) -> Unit) {
        val directory = File(activity.cacheDir, "unicode-minus-${System.nanoTime()}")
        val assembly = ImageAssembly(directory)
        try {
            assembly.add(listOf(
                AssemblyImage("a", File(directory, "a.image").apply { writeText("not decoded") }, "a.png", null,
                    ImageDimensions(200, 400), position = ImagePosition(10, 20)),
                AssemblyImage("b", File(directory, "b.image").apply { writeText("not decoded") }, "b.png", null,
                    ImageDimensions(80, 100), position = ImagePosition(300, 400))
            ))
            check(assembly, File(directory, "project.json"))
        } finally {
            directory.deleteRecursively()
        }
    }
}
