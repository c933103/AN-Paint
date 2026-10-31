"""French Help refers to current nearby controls, not copied approved prose."""
import unittest
import translation_catalogues as catalogues
from current_localization_contracts import decode_display


class FrenchAssemblyHelpTests(unittest.TestCase):
    def test_actual_control_labels_match_the_help(self):
        strings = catalogues.read_strings(catalogues.catalogue_paths()['fr'])
        value = decode_display(strings['ui_add_up_to_20_images_with_android_s'])
        for key in ('ui_assembly_exact_position', 'ui_same_width', 'ui_same_height'):
            self.assertIn(decode_display(strings[key]), value)


if __name__ == '__main__':
    unittest.main()
