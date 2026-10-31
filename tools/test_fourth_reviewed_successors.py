"""Bounded HNE/YI/CSB/KAB/MWW/MAI/WA/SE/SA forward decisions, not fluency claims."""
from copy import deepcopy
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
from current_localization_contracts import residual_rows, fixture
import chhattisgarhi_yiddish_hong_kong_priority_expectations as hne
import cebuano_low_german_kashubian_priority_expectations as csb
import walloon_northern_sami_sanskrit_priority_expectations as wa
from test_kabyle_hmong_daw_maithili_priority_wording import require_current as require_kab

TAGS = ('hne', 'yi', 'csb', 'kab', 'mww', 'mai', 'wa', 'se', 'sa')
MISSING = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg',
           'ui_save_as_jpeg_xl', 'ui_save_as_png', 'ui_bg', 'ui_fg', 'ui_fit_image',
           'ui_foreground_background_colour_palette', 'ui_main23', 'ui_pinch_and_pan_mode'}
GESTURE = 'ui_drawing_canvas_pinch_and_move_two_fingers_to'
EXISTING = {(tag, GESTURE) for tag in ('yi', 'csb', 'mww', 'wa', 'se', 'sa')} | {
    ('mww', 'ui_zoom_out'), ('se', 'ui_ellipse'), ('se', 'ui_your_current_image_has_unsaved_changes')}


class FourthReviewedSuccessors(unittest.TestCase):
    def test_exact_98_additions_and_9_existing_corrections(self):
        rows = {identity: row for identity, row in residual_rows().items() if identity[0] in TAGS}
        missing = {(tag, key) for tag in TAGS for key in MISSING} - {('kab', 'ui_fit_image')}
        self.assertEqual(98, len(missing))
        self.assertEqual(9, len(EXISTING))
        self.assertEqual(missing | EXISTING, set(rows))
        self.assertEqual(missing, {identity for identity, row in rows.items() if row['previous_target'] is None})
        self.assertIn('https://github.com/c933103/AN-Paint/pull/56#issuecomment-6532578683',
                      fixture('reviewed_residuals_20261030.json')['reviews'])
        self.assertNotIn(('kab', 'ui_fit_image'), rows)

    def test_strict_catalogues_reject_every_new_target_shape_mutation(self):
        rows = residual_rows()
        roots = {tag: ET.parse(catalogues.catalogue_paths()[tag]).getroot() for tag in TAGS}
        english = ET.parse(catalogues.RES / 'values/strings.xml').getroot()
        kab_data = fixture('kabyle_hmong_daw_maithili_priority_wording.json')
        def check(tag, root):
            if tag in ('kab', 'mww', 'mai'):
                require_kab(kab_data, {t: root if t == tag else roots[t] for t in ('kab', 'mww', 'mai')}, english)
            else:
                module = hne if tag in ('hne', 'yi') else csb if tag == 'csb' else wa
                module.require_catalogue(tag, root)
        for tag in TAGS:
            check(tag, roots[tag])
        for (tag, key), row in rows.items():
            if tag not in TAGS:
                continue
            for mutation in ('missing', 'duplicate', 'type', 'text', 'attribute', 'child', 'tail'):
                root = deepcopy(roots[tag]); node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'type': node.tag = 'plurals'
                elif mutation == 'text': node.text += ' forged'
                elif mutation == 'attribute': node.set('formatted', 'false')
                elif mutation == 'child': ET.SubElement(node, 'b')
                else: node.tail = 'forged'
                with self.subTest(tag=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                    check(tag, root)
            changed = deepcopy(rows); changed[(tag, key)]['previous_target'] = 'forged predecessor'
            with patch('current_localization_contracts.residual_rows', return_value=changed), self.subTest(tag=tag, key=key):
                # KAB's local import must see the same deliberately corrupt registry.
                with patch('test_kabyle_hmong_daw_maithili_priority_wording.residual_rows', return_value=changed):
                    with self.assertRaises(ValueError): check(tag, roots[tag])


if __name__ == '__main__':
    unittest.main()
