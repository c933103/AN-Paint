"""Bounded HNE/YI/CSB/KAB/MWW/MAI/WA/SE/SA forward decisions, not fluency claims."""
from copy import deepcopy
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
from current_localization_contracts import residual_rows, fixture

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



if __name__ == '__main__':
    unittest.main()
