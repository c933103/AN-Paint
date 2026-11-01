"""Crop modality and inflected accessibility units, not copied complete values."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

class FinnishEstonianLatvianCropCompanionTests(unittest.TestCase):
    def test_crop_categories_count_and_attached_object_modality(self):
        for tag, clauses in (
            ('fi', ('voi siirtää', 'niihin liitettyjä kuvia')),
            ('lv', ('var pārvietot', 'tiem piesaistītos attēlus')),
        ):
            items = ET.parse(catalogues.catalogue_paths()[tag]).findall("./plurals[@name='ui_crop_preview_images']/item")
            self.assertEqual(['one', 'other'], [n.get('quantity') for n in items])
            for item in items:
                self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$d': 1}, catalogues.placeholders(item.text))
                for clause in clauses:
                    self.assertIn(clause, item.text)
                noun = 'kuvaan' if tag == 'fi' else ('attēlam' if item.get('quantity') == 'one' else 'attēliem')
                self.assertIn('%3$d ' + noun, item.text)

    def test_side_template_requires_argument_separator_and_complete_unit(self):
        for tag, pixel_unit, percent_unit in (
            ('fi', 'pikseleinä', 'prosentteina'),
            ('et', 'pikslites', 'protsentides'),
            ('lv', 'pikseļos', 'procentos'),
        ):
            strings = catalogues.read_strings(catalogues.catalogue_paths()[tag])
            for key, unit in (('ui_trim_in_pixels', pixel_unit), ('ui_trim_in_percent', percent_unit)):
                template = strings[key]
                self.assertEqual({'%1$s': 1}, catalogues.placeholders(template))
                self.assertTrue(template.startswith('%1$s: '))
                self.assertTrue(template.endswith(' ' + unit))
                for edge in ('left', 'top', 'right', 'bottom'):
                    label = strings['ui_' + edge]
                    composed = template.replace('%1$s', label)
                    self.assertTrue(composed.startswith(label + ': '))
                    self.assertNotIn('%1$s', composed)

if __name__ == '__main__':
    unittest.main()
