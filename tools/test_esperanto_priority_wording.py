"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

COUNT = 'ui_d_d_px_d_pixels_2f_mp'

KEYS = {'ui_trim_amounts_must_be_zero_or_greater', 'ui_reset_crop', 'ui_trim_amounts_must_fit_inside_each_image_use', 'ui_the_crop_must_contain_at_least_one_pixel', 'ui_could_not_apply_the_crop', 'ui_trim_expand_canvas_by_touch', 'ui_d_d_px_d_pixels_2f_mp', 'ui_apply_crop', 'ui_crop', 'ui_the_crop_must_stay_inside_the_image', 'ui_choose_a_smaller_output_copy_the_source_images', 'ui_enter_a_trim_amount_for_every_edge', 'ui_the_trim_would_remove_the_entire_image', 'ui_crop_must_stay_inside_the_canvas', 'ui_enter_all_four_trim_amounts', 'ui_crop_preview_drag_an_edge_or_corner_drag'}

CLASSIC = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class EsperantoPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in {'default': 'values', 'eo': 'values-b+eo'}.items()}
        cls.strings = {tag: {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(xml)
                            if n.tag == 'string'} for tag, xml in cls.xml.items()}

    def test_pixel_count_is_count_neutral_with_unchanged_numeric_contract(self):
        self.assertEqual('%1$d × %2$d px · Nombro de bilderoj: %3$,d (%4$.2f MP)', self.strings['eo'][COUNT])
        source = (CLASSIC / 'ImageImport.kt').read_text(encoding='utf-8')
        self.assertIn('width > 0 && height > 0', source)
        self.assertIn('val pixels: Long get() = width.toLong() * height', source)
        self.assertIn('ui(R.string.' + COUNT + ', width, height, pixels, pixels / 1_000_000.0)', source)

    def test_crop_spelling_matches_existing_crop_commands(self):
        self.assertEqual('Stuci bildon', self.strings['eo']['ui_crop_image'])
        self.assertEqual('Stuci al elekto', self.strings['eo']['ui_crop_to_selection'])
        for key in KEYS - {COUNT}:
            self.assertIn('stuc', self.strings['eo'][key].lower())
            self.assertNotIn('stuĉ', self.strings['eo'][key].lower())

if __name__ == '__main__':
    unittest.main()
