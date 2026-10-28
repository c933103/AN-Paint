/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.view.View
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.text.DecimalFormatSymbols
import java.util.Locale

/** Display formatting follows resource selection, without changing numeric inputs or calculations. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class ImageDisplayLocaleTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale

    @Before fun saveLocaleState() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
    }

    @After fun restoreLocaleState() {
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    private fun resources(tag: String, processDefault: String): Context {
        val application = RuntimeEnvironment.getApplication() as Context
        val context = application.createConfigurationContext(Configuration(application.resources.configuration).apply {
            setLocale(Locale.forLanguageTag(tag))
        })
        PaintApplication.currentResources = context.resources
        Locale.setDefault(Locale.forLanguageTag(processDefault))
        assertEquals(tag, context.resources.configuration.locales[0].toLanguageTag())
        return context
    }

    @Test fun completeSummariesUseResourceLocaleDespiteOppositeProcessDefaults() {
        val cases = listOf(
            Triple("pt-BR", "en-US", "1500 × 1500 px · Quantidade de pixels: 2.250.000 (2,25 MP)"),
            Triple("de", "en-US", "1500 × 1500 px · 2.250.000 Pixel (2,25 MP)"),
            Triple("en-US", "pt-BR", "1500 × 1500 px · Pixel count: 2,250,000 (2.25 MP)"),
            Triple("ar-EG", "en-US", "١٥٠٠ × ١٥٠٠ px · عدد البكسلات: ٢٬٢٥٠٬٠٠٠ (٢٫٢٥ ميغابكسل)")
        )
        for ((tag, process, expected) in cases) {
            resources(tag, process)
            assertEquals(tag, expected, ImageDimensions(1500, 1500).describe())
        }
        resources("fr", "en-US")
        val symbols = DecimalFormatSymbols(Locale.FRENCH)
        assertEquals(',', symbols.decimalSeparator)
        assertTrue(symbols.groupingSeparator in listOf('\u00a0', '\u202f'))
        val group = symbols.groupingSeparator
        assertEquals("1500 × 1500 px · Nombre de pixels : 2${group}250${group}000 (2,25 MP)",
            ImageDimensions(1500, 1500).describe())
    }

    @Test fun englishFallbackStillUsesSelectedLocaleNumbers() {
        // Private-use qtz is deliberately unsupported; later offered-locale translations cannot replace this fallback.
        resources("qtz-u-nu-arab", "en-US")
        assertEquals("%1\$d × %2\$d px · Pixel count: %3\$,d (%4\$.2f MP)",
            PaintApplication.currentResources.getString(R.string.ui_d_d_px_d_pixels_2f_mp))
        val symbols = DecimalFormatSymbols(Locale.forLanguageTag("qtz-u-nu-arab"))
        assertEquals('\u066b', symbols.decimalSeparator)
        assertEquals('\u066c', symbols.groupingSeparator)
        assertEquals("١٥٠٠ × ١٥٠٠ px · Pixel count: ٢٬٢٥٠٬٠٠٠ (٢٫٢٥ MP)",
            ImageDimensions(1500, 1500).describe())
        assertEquals("١٫٥ KiB", memoryLabel(1536.0))
    }

    @Test fun reviewedBretonSummaryStillUsesSelectedLocaleNumbers() {
        // Preserve actual offered Breton coverage now that its complete summary is independently reviewed.
        resources("br", "en-US")
        assertEquals("%1\$d × %2\$d px · Niver a bikselioù: %3\$,d (%4\$.2f MP)",
            PaintApplication.currentResources.getString(R.string.ui_d_d_px_d_pixels_2f_mp))
        val symbols = DecimalFormatSymbols(Locale.forLanguageTag("br"))
        assertEquals(',', symbols.decimalSeparator)
        val group = symbols.groupingSeparator
        assertEquals("1500 × 1500 px · Niver a bikselioù: 2${group}250${group}000 (2,25 MP)",
            ImageDimensions(1500, 1500).describe())
        assertEquals("1,5 KiB", memoryLabel(1536.0))
    }

    @Test fun memoryDisplayKeepsUnitScalingAndResourceSpecificDecimalDigits() {
        for ((tag, process, decimal) in listOf(Triple("pt-BR", "en-US", ','), Triple("en-US", "pt-BR", '.'))) {
            resources(tag, process)
            for ((bytes, expected) in listOf(-1536.0 to "0${decimal}0 B", 0.0 to "0${decimal}0 B", 1023.0 to "1023${decimal}0 B",
                    1024.0 to "1${decimal}0 KiB", 1536.0 to "1${decimal}5 KiB",
                    1572864.0 to "1${decimal}5 MiB", 1610612736.0 to "1${decimal}5 GiB")) {
                assertEquals("$tag / $bytes", expected, memoryLabel(bytes))
            }
        }
        resources("ar-EG", "en-US")
        assertEquals("١٫٥ KiB", memoryLabel(1536.0))
    }

    @Test fun existingDimensionControlRefreshUsesNewResourceSnapshot() {
        val context = resources("pt-BR", "en-US")
        val controls = DimensionControls(context, ImageDimensions(1500, 1500), locked = false)
        val result = controls.findViewWithTag<TextView>("size_result")
        assertEquals("1500 × 1500 px · Quantidade de pixels: 2.250.000 (2,25 MP)", result.text.toString())
        resources("en-US", "pt-BR")
        controls.setDimensions(ImageDimensions(1500, 1500))
        assertEquals("1500 × 1500 px · Pixel count: 2,250,000 (2.25 MP)", result.text.toString())
        assertEquals(ImageDimensions(1500, 1500), controls.dimensions)
    }

    @Test fun localizedDisplayDoesNotChangeParsingUnitRoundTripsOrInvalidInputRejection() {
        val context = resources("pt-BR", "pt-BR")
        val controls = DimensionControls(context, ImageDimensions(400, 200), locked = false)
        controls.findViewWithTag<View>("size_percent").performClick()
        controls.widthInput.setText("12,5")
        assertEquals(ImageDimensions(50, 200), controls.dimensions)
        for (input in listOf("12.5", "12,5")) {
            controls.widthInput.setText(input)
            assertEquals(ImageDimensions(50, 200), controls.dimensions)
        }
        repeat(5) {
            controls.findViewWithTag<View>("size_pixels").performClick()
            assertEquals("50", controls.widthInput.text.toString())
            assertEquals(ImageDimensions(50, 200), controls.dimensions)
            controls.findViewWithTag<View>("size_percent").performClick()
            assertEquals("12.5", controls.widthInput.text.toString())
            assertEquals(ImageDimensions(50, 200), controls.dimensions)
        }
        controls.findViewWithTag<View>("size_pixels").performClick()
        val result = controls.findViewWithTag<TextView>("size_result")
        assertEquals("50 × 200 px · Quantidade de pixels: 10.000 (0,01 MP)", result.text.toString())
        for (invalid in listOf("0", "-1", "NaN", "Infinity", "1e200", "2147483648", "1,5", "")) {
            controls.widthInput.setText(invalid)
            assertNull(invalid, controls.dimensions)
            assertEquals(ui(R.string.ui_enter_positive_dimensions_that_resolve_to_at_least), result.text.toString())
        }
    }

    @Test fun longPixelArithmeticAndAdmissionAreUnaffectedByDisplayLocale() {
        val huge = ImageDimensions(Int.MAX_VALUE, Int.MAX_VALUE)
        val expectedPixels = 4_611_686_014_132_420_609L
        for ((tag, process) in listOf("pt-BR" to "en-US", "en-US" to "pt-BR")) {
            resources(tag, process)
            assertEquals(expectedPixels, huge.pixels)
            val count = if (tag == "pt-BR") "4.611.686.014.132.420.609" else "4,611,686,014,132,420,609"
            assertTrue(huge.describe().contains(count))
            val plan = ImportPlan.create(ImageDimensions(4000, 3000), ImageDimensions(1500, 1125))
            assertEquals(25_500_000.0, plan.estimatedBytes(0), 0.0)
            val policy = ImageMemoryPolicy.calculate(128L * 1024 * 1024, 100L * 1024 * 1024,
                64L * 1024 * 1024, 128L * 1024 * 1024, false)
            assertEquals(0L, policy.maxPixels())
            assertNull(policy.suggestResize(huge, 0))
            assertThrows(ImageSizeException::class.java) { policy.check(Int.MAX_VALUE, Int.MAX_VALUE) }
        }
    }
}
