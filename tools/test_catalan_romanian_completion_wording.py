"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


class CatalanRomanianCompletionWordingTests(unittest.TestCase):

    def test_recovery_compositions_keep_existing_actions_product_syntax_and_prefix_punctuation(self):
        for tag, menu, save, save_as in [('ca', 'Fitxer', 'Desa', 'Anomena i desa…'),
                                        ('ro', 'Fișier', 'Salvează', 'Salvează ca…')]:
            value = lambda key: current_display(tag, key)
            paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
            self.assertIn(menu, paused);self.assertIn(save_as, paused)
            self.assertIn(value('ui_export_recovery_copy'), paused)
            self.assertIn(current_display(tag,'save20_file_format') + ': PNG / JPEG', paused)
            for key in ('ui_autosave_failed_use_save', 'ui_autosave_paused_use_save'):
                self.assertIn(save, value(key))
            recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
            self.assertIn(menu + ' > ' + current_display(tag,'ui_load_image'), recovery)
            self.assertIn('canvas.png', recovery);self.assertIn('ZIP', recovery)
            self.assertEqual(value('ui_export_recovery_copy_144b8a') + '…', value('ui_export_recovery_copy'))
            for key in ('ui_could_not_open_image', 'ui_could_not_export_the_recovery_copy',
                        'ui_not_enough_memory_to_save_in_this_format'):
                self.assertFalse(value(key).endswith(('.', ':', '…')))
            for literal in ('AN Paint', '×', 'MP'):
                self.assertIn(literal, value('ui_d_d_pixels_2f_mp_exceeds_the_current'))

if __name__ == '__main__':
    unittest.main()
