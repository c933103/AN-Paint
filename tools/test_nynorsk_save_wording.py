"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


class NynorskSaveWordingTests(unittest.TestCase):

    def test_filename_and_share_format_contracts_remain_current(self):
        root = ET.parse(catalogues.catalogue_paths()['nn']).getroot()
        self.assertEqual({'%1$s': 1}, catalogues.placeholders(current_display('nn', 'ui_saved')))
        self.assertEqual('false', root.find("./string[@name='ui_share_explanation34']").get('formatted'))
        self.assertFalse(current_display('nn', 'ui_could_not_save_image').endswith('.'))

    def test_save_alias_and_unsaved_actions_keep_distinct_meanings(self):
        strings = catalogues.read_strings(catalogues.catalogue_paths()['nn'])
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual(current_display('nn', 'ui_save'), current_display('nn', 'ui_save_a5d0d9'))
        self.assertEqual(3, len({current_display('nn', key) for key in
                                ('ui_save', 'ui_discard_changes23', 'ui_keep_editing23')}))
        self.assertNotEqual(current_display('nn', 'ui_keep_editing23'), current_display('nn', 'ui_cancel'))
        self.assertEqual(current_display('nn', 'ui_save_and_share_41edb4') + '…',
                         current_display('nn', 'ui_save_and_share'))


if __name__ == '__main__':
    unittest.main()
