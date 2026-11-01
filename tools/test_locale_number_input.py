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

if __name__ == '__main__':
    unittest.main()
