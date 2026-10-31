"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


class CatalanRomanianSaveWordingTests(unittest.TestCase):

    def test_actual_action_labels_share_pair_and_product_literals_are_consistent(self):
        for tag, save, save_as in [('ca', 'Desa', 'Anomena i desa…'), ('ro', 'Salvează', 'Salvează ca…')]:
            value = lambda k: current_display(tag, k)
            self.assertIn('«' + save + '»', value('ui_export_did_not_save23'))
            self.assertIn('«' + save_as + '»', value('ui_export_did_not_save23'))
            self.assertIn('«' + save + '»', value('ui_save_explanation23'))
            self.assertEqual(value('ui_save_and_share_41edb4') + '…', value('ui_save_and_share'))
            self.assertIn('Base64', value('ui_export_explanation23'))
            self.assertIn('ASCII', value('ui_export_explanation23'))
            self.assertIn('Android', value('ui_the_image_was_saved_but_android_could_not'))
            self.assertFalse(value('ui_could_not_save_image').endswith('.'))
            for key in ('ui_saved', 'ui_the_image_was_saved_but_android_could_not'):
                self.assertEqual({'%1$s': 1}, full_format_tokens(value(key)))

if __name__ == '__main__':
    unittest.main()
