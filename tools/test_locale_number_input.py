"""Numeric-entry source coverage guard; runtime behavior is in LocaleNumberInputTest."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'


class LocaleNumberInputSourceTest(unittest.TestCase):
    def test_all_numeric_routes_use_shared_configuration(self):
        expected = {
            'NumericSlider.kt': ['LocaleNumberInput.configure(this)'],
            'AdvancedColourDialog.kt': ['LocaleNumberInput.configure(this, decimal = true)'],
            'DimensionControls.kt': ['LocaleNumberInput.configure(it, decimal = percent)'],
            'ImageCropDialog.kt': ['LocaleNumberInput.configure(this, decimal = true)'],
            'NormalizeImagesDialog.kt': ['LocaleNumberInput.configure(this)', 'LocaleNumberInput.configure(input, decimal = percent)'],
            'TextStyleDialog.kt': ['LocaleNumberInput.configure(this, decimal = true)'],
            'ImportSelection.kt': ['LocaleNumberInput.configure(this)'],
        }
        for name, calls in expected.items():
            source = (JAVA / name).read_text()
            for call in calls:
                self.assertEqual(1, source.count(call), (name, call))
        numeric = [p.name for p in JAVA.glob('*.kt') if 'InputType.TYPE_CLASS_NUMBER' in p.read_text()]
        self.assertEqual(['LocaleNumberInput.kt'], numeric)

    def test_dialog_initialization_precedes_decor_for_api21(self):
        source = (JAVA / 'VerticalUi.kt').read_text().split('override fun create(): AlertDialog {', 1)[1]
        self.assertLess(source.index('val dialog=super.create()'), source.index('dialog.create()'))
        self.assertLess(source.index('dialog.create()'), source.index('dialog.window!!.decorView'))

    def test_filter_preserves_syntax_and_ime_restart_order_without_overriding_validation(self):
        source = (JAVA / 'LocaleNumberInput.kt').read_text()
        for text in ('DecimalFormatSymbols(view.resources.configuration.locale)',
                     'symbols.zeroDigit', 'symbols.decimalSeparator', 'symbols.minusSign',
                     '"0123456789.+-"', 'view.keyListener = object : NumberKeyListener()',
                     'val keyboardType = InputType.TYPE_CLASS_NUMBER or if (decimal) InputType.TYPE_NUMBER_FLAG_DECIMAL else 0',
                     'override fun getInputType() = keyboardType', 'override fun getAcceptedChars() = accepted'):
            self.assertIn(text, source)
        for forbidden in ('setText(', 'contentDescription', 'setOn', 'uiNumber(', 'toIntOrNull(', 'inputType ='):
            self.assertNotIn(forbidden, source)


if __name__ == '__main__':
    unittest.main()
