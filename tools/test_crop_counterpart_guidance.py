"""Current nearby control-caption relationships, not per-locale prose mirrors.

Shared assembly mode boundaries and actual crop/undo regressions cover behavior.
"""
import unittest
import translation_catalogues as catalogues
from current_localization_contracts import decode_display


class CropCounterpartGuidanceTests(unittest.TestCase):
    def test_same_entry_clarifications_retain_exact_current_control_names(self):
        for tag, keys in (
            ('es-ES', ('ui_crop_image', 'ui_remove')),
            ('it', ('ui_same_width', 'ui_same_height', 'ui_pixels', 'ui_percent')),
            ('pt-PT', ('ui_same_width', 'ui_same_height')),
        ):
            strings = catalogues.read_strings(catalogues.catalogue_paths()[tag])
            help_text = decode_display(strings['ui_add_up_to_20_images_with_android_s'])
            for key in keys:
                self.assertIn(decode_display(strings[key]), help_text)


if __name__ == '__main__':
    unittest.main()
