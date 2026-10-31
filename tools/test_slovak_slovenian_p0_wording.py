"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


class SlovakSlovenianP0Tests(unittest.TestCase):

    def test_recovery_compositions_retain_actual_labels_and_literal_filenames(self):
        for tag, menu in [('sk', 'Súbor'), ('sl', 'Datoteka')]:
            value = lambda key: current_display(tag, key)
            recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
            self.assertIn(menu + (' > ' if tag == 'sk' else ' → ') + current_display(tag,'ui_load_image'), recovery)
            self.assertIn('canvas.png', recovery);self.assertIn('ZIP', recovery)
            paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
            self.assertIn(menu + ' → ' + value('ui_export_recovery_copy'), paused)
            self.assertIn(menu + ' → ' + current_display(tag, 'save20_title'), paused)
            self.assertIn(current_display(tag, 'save20_file_format') + ': PNG / JPEG', paused)
            kept = value('ui_a_separate_recovery_copy_has_been_kept_use')
            self.assertIn(menu + (' > ' if tag == 'sk' else ' → ') + value('ui_export_recovery_copy'), kept)
            self.assertIn('canvas.png', kept);self.assertIn('ZIP', kept)

    def test_save_share_and_error_composition_keeps_command_and_punctuation_contracts(self):
        for tag in ('sk', 'sl'):
            value = lambda key: current_display(tag, key)
            save = current_display(tag, 'ui_save')
            save_as = current_display(tag, 'save20_title')
            for key in ('ui_export_did_not_save23', 'ui_export_explanation23', 'ui_save_explanation23', 'ui_share_explanation34'):
                self.assertIn(save, value(key))
            self.assertIn(save_as, value('ui_export_did_not_save23'))
            self.assertEqual(value('ui_save_and_share_41edb4') + '…', value('ui_save_and_share'))
            self.assertEqual(value('ui_export_recovery_copy_144b8a') + '…', value('ui_export_recovery_copy'))
            for key in ('ui_could_not_save_image', 'ui_could_not_open_image', 'ui_could_not_export_the_recovery_copy',
                        'ui_not_enough_memory_to_save_in_this_format'):
                self.assertFalse(value(key).endswith(('.', ':', '…')))
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(value('ui_saved')))
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(value('ui_the_image_was_saved_but_android_could_not')))

if __name__ == '__main__':
    unittest.main()
