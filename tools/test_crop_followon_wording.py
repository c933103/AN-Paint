"""Current crop semantics and edge/unit composition, not historical wording snapshots."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


class CropFollowonWordingTests(unittest.TestCase):
    def test_attached_images_may_move_and_reference_count_stays_typed(self):
        for tag, quantities, clauses in (
            ('eo', {'one', 'other'}, ('povas movi', 'bildojn alkroĉitajn al ili')),
            ('et', {'one', 'other'}, ('võib liigutada', 'nende külge kinnitatud pilte')),
            ('id', {'other'}, ('dapat menggeser', 'gambar yang tersambung dengannya')),
        ):
            items = ET.parse(catalogues.catalogue_paths()[tag]).findall("./plurals[@name='ui_crop_preview_images']/item")
            self.assertEqual(quantities, {n.get('quantity') for n in items})
            for item in items:
                self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$d': 1}, catalogues.placeholders(item.text))
                for clause in clauses:
                    self.assertIn(clause, item.text)

    def test_all_four_actual_edge_captions_with_both_unit_templates(self):
        strings = catalogues.read_strings(catalogues.catalogue_paths()['eo'])
        captions = [strings[k] for k in ('ui_left', 'ui_top', 'ui_right', 'ui_bottom')]
        self.assertEqual(4, len(set(captions)))
        for caption in captions:
            for key in ('ui_trim_in_pixels', 'ui_trim_in_percent'):
                template = strings[key]
                self.assertEqual({'%1$s': 1}, catalogues.placeholders(template))
                composed = template.replace('%1$s', caption)
                self.assertTrue(composed.startswith(caption))
                if key == 'ui_trim_in_pixels':
                    self.assertEqual(1, composed.count(':'))
                self.assertNotIn('%1$s', composed)


if __name__ == '__main__':
    unittest.main()
