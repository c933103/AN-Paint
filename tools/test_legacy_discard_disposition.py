"""Current Discard action semantics, not a historical approval/predecessor adapter."""
import unittest
import translation_catalogues as catalogues
from current_localization_contracts import decode_display


class LegacyDiscardDispositionTest(unittest.TestCase):
    def test_discard_names_the_same_change_action_not_save_or_keep_editing(self):
        for tag in ('ps', 'eu-ES'):
            strings = catalogues.read_strings(catalogues.catalogue_paths()[tag])
            value = decode_display(strings['ui_discard'])
            with self.subTest(tag=tag):
                self.assertEqual(decode_display(strings['ui_discard_changes23']), value)
                self.assertNotEqual(decode_display(strings['ui_save']), value)
                self.assertNotEqual(decode_display(strings['ui_keep_editing23']), value)
                self.assertFalse(catalogues.placeholders(value))
                self.assertEqual([], catalogues.android_string_errors(strings['ui_discard']))
                self.assertEqual([], catalogues.format_string_errors(value, True))
        # The old generic rejection term did not name discarding the changes.
        self.assertNotEqual('رد کړئ', decode_display(
            catalogues.read_strings(catalogues.catalogue_paths()['ps'])['ui_discard']))


if __name__ == '__main__':
    unittest.main()
