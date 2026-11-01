"""Plural/count and attached-image modality boundaries, not approved sentences."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class CropMovementTranslationTests(unittest.TestCase):
    def test_warning_forms_preserve_dimensions_count_and_optional_image_movement(self):
        # Russian object/case boundaries are covered once in test_russian_crop_warning.
        for tag, quantities, clauses in (
            ('lt', {'one', 'few', 'other'}, ('prijungti vaizdai', 'gali pasislinkti')),
            ('ar', {'zero', 'one', 'two', 'few', 'many', 'other'}, ('قد يؤدي', 'تحريك الصور المتصلة بها')),
            ('ja', {'other'}, ('接続された画像が', '移動する場合があります')),
        ):
            items = ET.parse(catalogues.catalogue_paths()[tag]).findall("./plurals[@name='ui_crop_preview_images']/item")
            self.assertEqual(quantities, {n.get('quantity') for n in items})
            self.assertEqual(len(quantities), len(items))
            for item in items:
                text = item.text
                self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$d': 1}, catalogues.placeholders(text))
                self.assertEqual(1, text.count(r'\n'))
                self.assertIn(' × ', text)
                self.assertNotIn('\n', text)
                for clause in clauses:
                    self.assertIn(clause, text)

if __name__ == '__main__':
    unittest.main()
