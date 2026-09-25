"""Regressions for contextual homonyms and navigation repaired in the handoff."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / 'Paintroid/src/main/res'


def strings(locale):
    return {e.get('name'): e.text or '' for e in ET.parse(
        RES / ('values-' + locale) / 'strings.xml').getroot() if e.tag == 'string'}


class KoreanNomContextTests(unittest.TestCase):
    def test_nom_lens_radius_copy_star_and_file_arrow_are_distinct(self):
        v = strings('b+vi+Hani')
        self.assertIn('鏡', v['ui_magnifier33'])
        self.assertIn('徑', v['ui_spray_radius_px'])
        self.assertIn('抄', v['ui_copy'])
        self.assertIn('𣇟', v['ui_star'])
        self.assertIn('𠄼', v['ui_drag_between_opposite_corners_to_draw_a_five'])
        self.assertNotIn('𢆥', v['ui_drag_between_opposite_corners_to_draw_a_five'])
        self.assertIn('𠸜', v['save20_file_name'])
        self.assertIn('箭', v['ui_arrow'])
        self.assertIn('割', v['ui_cut'])

    def test_nom_technical_error_messages_keep_the_app_sense(self):
        v = strings('b+vi+Hani')
        for key in ('ui_autosave_pixels_are_missing', 'ui_no_readable_image_data',
                    'ui_lossless_format'):
            self.assertIn('與 料', v[key])
            self.assertNotIn('療', v[key])
        self.assertIn('戟 𡱩', v['ui_original_size34'])
        self.assertIn('糊 疏', v['save20_unsupported_tagged_colour'])
        self.assertIn('密 口', v['formats22_pdf_encrypted'])
        self.assertIn('併', v['ui_estimated_memory_current_working_budget'])
        self.assertIn('𡨸喃', v['ui_aa_bb_0123'])
        self.assertNotIn('あいう', v['ui_aa_bb_0123'])

    def test_korean_large_image_connective_is_not_the_cursor_noun(self):
        v = strings('b+ko+KP')
        self.assertIn('커서', v['formats22_pdf_dimensions'])
        self.assertNotIn('지시자', v['formats22_pdf_dimensions'])

    def test_all_five_manuals_name_the_live_routes(self):
        for locale in ('b+ko+KR', 'b+ko+KP', 'b+ko+Kore+KR', 'vi', 'b+vi+Hani'):
            with self.subTest(locale=locale):
                v = strings(locale)
                paragraphs = v['ui_the_arrow_on_the_left_directly_below_the'].split('\\n\\n')
                self.assertIn(v['ui_menu_file'] + ' → ' + v['ui_image_assembly'], paragraphs[8])
                self.assertIn(' → '.join(v[k] for k in (
                    'ui_draw26', 'ui_category_insert', 'ui_other_images34')), paragraphs[7])
                self.assertIn(v['ui_about_credits23'], paragraphs[-1])
                self.assertNotIn(v['ui_menu_help'], paragraphs[-1].split('。')[0]
                                 if locale == 'b+vi+Hani' else paragraphs[-1].split('.')[0])
                for caption in ('ui_swap23', 'ui_fit_selection34', 'ui_about_credits23'):
                    self.assertIn(v[caption], v['ui_help23'])


if __name__ == '__main__':
    unittest.main()
