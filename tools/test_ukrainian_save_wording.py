"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


class UkrainianSaveWordingTests(unittest.TestCase):

    def test_actual_action_labels_share_pair_and_product_literals_are_consistent(self):
        value = lambda k: current_display('uk', k)
        for label in ('Зберегти', 'Зберегти як…'):
            self.assertIn('«' + label + '»', value('ui_export_did_not_save23'))
        self.assertIn('«Зберегти»', value('ui_save_explanation23'))
        self.assertIn('«Зберегти»', value('ui_export_explanation23'))
        self.assertIn('«Зберегти»', value('ui_share_explanation34'))
        self.assertEqual(value('ui_save_and_share_41edb4') + '…', value('ui_save_and_share'))
        self.assertIn('Base64', value('ui_export_explanation23'))
        self.assertIn('ASCII', value('ui_export_explanation23'))
        self.assertIn('Android', value('ui_the_image_was_saved_but_android_could_not'))
        self.assertNotEqual(value('ui_your_current_image_has_unsaved_changes'), value('ui_export_did_not_save23'))
        self.assertFalse(value('ui_could_not_save_image').endswith('.'))

if __name__ == '__main__':
    unittest.main()
