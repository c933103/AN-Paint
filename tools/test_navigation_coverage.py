"""Coverage is tied to current visible controls, independent of tier claims."""
import unittest
from unittest.mock import patch
import navigation_coverage as navigation
import translation_catalogues as catalogues


class NavigationCoverageTest(unittest.TestCase):
    def test_current_consumers_include_second_level_and_accessible_controls(self):
        keys = navigation.navigation_keys()
        self.assertTrue({'ui_about_credits23', 'ui_pixel_grid33', 'ui_cursor_drawing32',
                         'ui_magnifier33', 'ui_image_assembly', 'ui_toggle_toolbox'} <= keys)
        self.assertNotIn('ui_pixel_grid_help33', keys)
        self.assertNotIn('ui_drag_a_line_then_drag_twice_to_set', keys)

    def test_reported_locales_have_every_navigation_key(self):
        for tag in ('yue-Hant', 'wa', 'xh', 'qaa-Zsye-XV'):
            with self.subTest(tag=tag):
                self.assertEqual([], navigation.coverage(tag)['missing'])

    def test_missing_visible_button_is_reported_even_when_other_keys_exist(self):
        values = catalogues.read_strings(catalogues.catalogue_paths()['wa'])
        del values['ui_magnifier33']
        with patch.object(catalogues, 'read_strings', return_value=values):
            self.assertEqual(['ui_magnifier33'], navigation.coverage('wa')['missing'])


if __name__ == '__main__':
    unittest.main()
