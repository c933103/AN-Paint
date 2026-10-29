"""Eight bounded Nynorsk messages; not native, complete-locale or runtime acceptance."""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape, require_string_root
import translation_catalogues as catalogues
from nynorsk_belarusian_albanian_priority_expectations import current_fixture, current_value, current_row

KEYS = {'ui_save_your_changes', 'ui_your_current_image_has_unsaved_changes',
        'ui_export_did_not_save23', 'ui_could_not_save_image', 'ui_saved',
        'ui_export_explanation23', 'ui_save_explanation23', 'ui_share_explanation34'}


class NynorskSaveWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('nynorsk_save_wording.json'), KEYS, {'default', 'nn'})
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('nn', 'values-b+nn')]}
        cls.roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}

    def test_complete_values_attributes_and_placeholders_match_reviewed_contract(self):
        tiers = json.loads((catalogues.DATA / 'string-importance.json').read_text())['tiers']
        priority = next(t['keys'] for t in tiers if t['id'] == 'P0')
        self.assertTrue({'string/' + key for key in KEYS}.issubset(priority))
        for key in KEYS:
            for tag in ('default', 'nn'):
                with self.subTest(tag=tag, key=key):
                    require_string_root(self.roots[tag], key, self.data['values'][key][tag],
                                   self.data['constraints'][key][tag])
            source = self.roots['default'].find(f"./string[@name='{key}']")
            target = self.roots['nn'].find(f"./string[@name='{key}']")
            self.assertEqual(source.attrib, target.attrib)
            self.assertEqual(catalogues.placeholders(source.text), catalogues.placeholders(target.text))
        self.assertEqual({'%1$s': 1}, catalogues.placeholders(self.data['values']['ui_saved']['nn']))
        self.assertEqual('false', self.roots['nn'].find("./string[@name='ui_share_explanation34']").get('formatted'))
        self.assertFalse(self.data['values']['ui_could_not_save_image']['nn'].strip('"').endswith('.'))

    def test_guards_reject_missing_duplicate_truncated_markup_attributes_and_wrong_types(self):
        for key in KEYS:
            for mutation in ('missing', 'duplicate', 'truncate', 'markup', 'attribute', 'wrong-type'):
                root = deepcopy(self.roots['nn'])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncate': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                elif mutation == 'attribute': node.set('translatable', 'false')
                else: node.tag = 'plurals'
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key,
                                   self.data['values'][key]['nn'], self.data['constraints'][key]['nn'])

    def test_saved_filename_argument_and_nonformatted_share_contract_fail_closed(self):
        for key, mutation in [('ui_saved', 'wrong-argument'), ('ui_saved', 'missing-argument'),
                              ('ui_share_explanation34', 'formatted')]:
            root = deepcopy(self.roots['nn'])
            node = root.find(f"./string[@name='{key}']")
            if mutation == 'wrong-argument': node.text = node.text.replace('%1$s', '%2$s')
            elif mutation == 'missing-argument': node.text = node.text.replace('%1$s', '')
            else: node.attrib.pop('formatted')
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_string(ET.tostring(root, encoding='unicode'), key,
                               self.data['values'][key]['nn'], self.data['constraints'][key]['nn'])

    def test_neighbouring_actions_aliases_and_unrelated_fallbacks_are_not_rewritten(self):
        expected = {'ui_save': '"Lagra"', 'ui_save_a5d0d9': '@string/ui_save',
                    'save20_title': '"Lagra som…"', 'ui_export_as23': '"Eksporter som…"',
                    'ui_discard_changes23': '"Avslutt utan lagring"',
                    'ui_keep_editing23': '"Avbryt"', 'ui_cancel': '"Avbryt"'}
        for key, value in expected.items():
            require_string_root(self.roots['nn'], key, current_value('nn',key,value,{'name':key}), {'attributes': {'name': key}})
        # Newly reviewed neighbors have exact separate expectations, not removed guards.
        remaining = current_fixture('nynorsk_p0_remaining_wording.json')
        for key in ('ui_save_and_share', 'ui_save_and_share_41edb4', 'save20_file_format'):
            require_string_root(self.roots['nn'], key, remaining['values'][key]['nn'], remaining['constraints'][key]['nn'])
        for key in ('ui_choose_location', 'ui_try_a_different_file_or_location'):
            row=current_row('nn',key)
            self.assertIsNone(row['previous_target'])
            require_string_root(self.roots['nn'],key,row['target'],{'attributes':row['attributes']})
        from test_translations import SCOPED_TAGS
        self.assertNotIn('nn', SCOPED_TAGS)

    def test_affected_catalogue_remains_partial_but_structurally_valid(self):
        self.assertEqual([], catalogues.validate_catalogue('nn', require_complete=False))
        names = [(node.tag, node.get('name')) for node in self.roots['nn']]
        self.assertEqual(len(names), len(set(names)))
        remaining = current_fixture('nynorsk_p0_remaining_wording.json')
        require_string_root(self.roots['nn'], 'ui_draft_restored', remaining['values']['ui_draft_restored']['nn'],
                       remaining['constraints']['ui_draft_restored']['nn'])


if __name__ == '__main__':
    unittest.main()
