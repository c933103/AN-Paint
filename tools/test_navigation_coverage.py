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
        self.assertNotIn('ui_menu_help', keys)
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

    def test_numbered_rotation_commands_cannot_disappear_from_navigation_coverage(self):
        missing = ['ui_rotate_180', 'ui_rotate_90_clockwise']
        self.assertTrue(set(missing) <= navigation.navigation_keys())
        values = catalogues.read_strings(catalogues.catalogue_paths()['wa'])
        for key in missing:
            del values[key]
        with patch.object(catalogues, 'read_strings', return_value=values):
            self.assertEqual(missing, navigation.coverage('wa')['missing'])

    def test_alias_to_english_fallback_is_not_counted_as_a_localized_label(self):
        values = catalogues.read_strings(catalogues.catalogue_paths()['wa'])
        values['ui_magnifier33'] = '@string/untranslated_label'
        with patch.object(catalogues, 'read_strings', return_value=values):
            self.assertIn('ui_magnifier33', navigation.coverage('wa')['fallback_aliases'])

    def test_english_copy_is_reported_for_review_in_any_non_english_locale(self):
        defaults = catalogues.default_resources()[0]
        values = catalogues.read_strings(catalogues.catalogue_paths()['wa'])
        values['ui_magnifier33'] = defaults['ui_magnifier33']
        with patch.object(catalogues, 'read_strings', return_value=values):
            self.assertIn('ui_magnifier33', navigation.coverage('wa')['english_matches_for_review'])

    def test_emoji_prefix_does_not_hide_copied_english_wording(self):
        defaults = catalogues.default_resources()[0]
        values = catalogues.read_strings(catalogues.catalogue_paths()['wa'])
        values['ui_magnifier33'] = '🔍 ' + defaults['ui_magnifier33']
        with patch.object(catalogues, 'read_strings', return_value=values):
            self.assertIn('ui_magnifier33', navigation.coverage('wa')['english_matches_for_review'])

    def test_letter_internal_middle_dot_is_not_discarded(self):
        self.assertFalse(navigation._same_prose('a·bc', 'abc'))
        self.assertTrue(navigation._same_prose('ABC·DE', 'abc·de'))

    def test_decorative_middle_dots_do_not_hide_english_copy(self):
        for value in ('· abc', 'abc ·', '🔍 · abc ·'):
            with self.subTest(value=value):
                self.assertTrue(navigation._same_prose(value, 'abc'))


if __name__ == '__main__':
    unittest.main()
