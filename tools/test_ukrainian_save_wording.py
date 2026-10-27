"""Ten bounded Ukrainian P0 values; not native-language or whole-locale acceptance."""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
from test_danish_norwegian_p0_wording import full_format_tokens, require_reviewed_string
import translation_catalogues as catalogues

KEYS = {'ui_your_current_image_has_unsaved_changes', 'ui_could_not_save_image', 'ui_saved',
        'ui_export_did_not_save23', 'ui_save_explanation23', 'ui_export_explanation23',
        'ui_share_explanation34', 'ui_save_and_share', 'ui_save_and_share_41edb4',
        'ui_the_image_was_saved_but_android_could_not'}
TAGS = {'default', 'uk'}
HOLDS = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg',
         'ui_save_as_jpeg_xl', 'ui_save_as_png'}


class UkrainianSaveWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('ukrainian_save_wording.json'), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('uk', 'values-uk')]}
        cls.roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}

    def test_exact_ten_P0_keys_and_complete_values_attributes_and_full_tokens(self):
        self.assertEqual(10, len(KEYS))
        self.assertTrue({'ui_save_your_changes', 'save20_file_format'}.isdisjoint(KEYS))
        tiers = json.loads((catalogues.DATA / 'string-importance.json').read_text())['tiers']
        self.assertTrue({'string/' + k for k in KEYS}.issubset(next(t['keys'] for t in tiers if t['id'] == 'P0')))
        for key in KEYS:
            self.assertEqual(TAGS, set(self.data['constraints'][key]))
            for tag in TAGS:
                with self.subTest(key=key, tag=tag):
                    require_reviewed_string(self.xml[tag], key, self.data['values'][key][tag],
                        self.data['constraints'][key][tag], self.data['values'][key]['default'])
                    self.assertEqual(self.roots['default'].find(f"./string[@name='{key}']").attrib,
                                     self.roots[tag].find(f"./string[@name='{key}']").attrib)

    def test_every_value_rejects_missing_duplicate_empty_truncated_markup_attributes_type_and_placeholder(self):
        for key in KEYS:
            original = self.roots['uk'].find(f"./string[@name='{key}']")
            for mutation in ('missing', 'duplicate', 'empty', 'truncate', 'markup', 'attribute', 'wrong-type', 'placeholder'):
                root = ET.Element('resources');node = deepcopy(original)
                if mutation != 'missing':root.append(node)
                if mutation == 'duplicate':root.append(deepcopy(node))
                elif mutation == 'empty':node.text = ''
                elif mutation == 'truncate':node.text = node.text[:-1]
                elif mutation == 'markup':ET.SubElement(node, 'b').text, node.text = node.text, None
                elif mutation == 'attribute':node.set('translatable', 'false')
                elif mutation == 'wrong-type':node.tag = 'plurals'
                elif mutation == 'placeholder':node.text += ' %9$s'
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_reviewed_string(ET.tostring(root, encoding='unicode'), key,
                        self.data['values'][key]['uk'], self.data['constraints'][key]['uk'],
                        self.data['values'][key]['default'])

    def test_single_string_arguments_reject_changed_index_type_count_and_nonargument_tokens(self):
        for key in ('ui_saved', 'ui_the_image_was_saved_but_android_could_not'):
            original = self.data['values'][key]['uk']
            self.assertEqual({'%1$s': 1}, full_format_tokens(original))
            for token in ('%2$s', '%1$d', '%s', '%1$s %1$s', '%1$s %%', '%1$s %n', '%1$S', '%1$'):
                changed = original.replace('%1$s', token)
                node = ET.Element('string', self.data['constraints'][key]['uk']['attributes']);node.text = changed
                root = ET.Element('resources');root.append(node)
                # Matching changed expectations cannot bypass the independent source-token guard.
                with self.subTest(key=key, token=token), self.assertRaises(ValueError):
                    require_reviewed_string(ET.tostring(root, encoding='unicode'), key,
                        changed, self.data['constraints'][key]['uk'], self.data['values'][key]['default'])

    def test_formatted_false_cannot_hide_extra_unindexed_or_nonargument_tokens(self):
        key = 'ui_share_explanation34'
        constraints = self.data['constraints'][key]['uk']
        self.assertEqual('false', constraints['attributes']['formatted'])
        source = self.data['values'][key]['default']
        self.assertFalse(full_format_tokens(source))
        for suffix in (' %s', ' %d', ' %.2f', ' %1$s', ' %%', ' %n',
                       ' %', ' %q', ' %1$', ' %.', ' %3$.', ' %3$.f', ' %t'):
            changed = self.data['values'][key]['uk'] + suffix
            node = ET.Element('string', constraints['attributes']);node.text = changed
            root = ET.Element('resources');root.append(node)
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                require_reviewed_string(ET.tostring(root, encoding='unicode'), key,
                                        changed, constraints, source)

    def test_all_127_inherited_values_attributes_and_scoped_catalogue_membership_stay_unchanged(self):
        self.assertEqual({'uk'}, set(self.data['preserved_values']))
        preserved = self.data['preserved_values']['uk']
        self.assertEqual(127, len(preserved));self.assertFalse(set(preserved) & KEYS)
        for key, expected in preserved.items():
            with self.subTest(key=key):
                require_string(self.xml['uk'], key, expected['value'], {'attributes': expected['attributes']})
        self.assertEqual(137, len(self.roots['uk']))
        self.assertEqual(set(preserved) | KEYS, {node.get('name') for node in self.roots['uk']})
        from test_translations import SCOPED_TAGS
        self.assertNotIn('uk', SCOPED_TAGS)
        self.assertIn('uk', catalogues.offered_tags())
        self.assertEqual(59, len(SCOPED_TAGS))
        self.assertEqual(112, len(set(catalogues.offered_tags()) - SCOPED_TAGS))

    def test_five_holds_and_unreviewed_neighbor_fallbacks_remain_absent(self):
        self.assertEqual(HOLDS, set(self.data['held_absent']))
        for key in HOLDS | {'ui_choose_location', 'ui_share_saved_image',
                            'ui_no_resize_fits_decoder_memory', 'ui_load_image'}:
            self.assertIsNone(self.roots['uk'].find(f"./string[@name='{key}']"), key)
        self.assertEqual('Choose location…', self.roots['default'].find("./string[@name='ui_choose_location']").text)
        self.assertEqual('Share saved image', self.roots['default'].find("./string[@name='ui_share_saved_image']").text)

    def test_actual_action_labels_share_pair_and_product_literals_are_consistent(self):
        value = lambda k: self.data['values'][k]['uk'][1:-1]
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
        for key in KEYS:
            self.assertTrue(self.data['values'][key]['uk'].startswith('"'))
            self.assertTrue(self.data['values'][key]['uk'].endswith('"'))

    def test_fixture_family_rejects_missing_extra_empty_or_wrong_locale_scope(self):
        mutations = []
        d = deepcopy(self.data);d['values'].pop(next(iter(KEYS)));mutations.append(d)
        d = deepcopy(self.data);d['constraints'].pop(next(iter(KEYS)));mutations.append(d)
        d = deepcopy(self.data);d['values'][next(iter(KEYS))]['uk'] = '';mutations.append(d)
        d = deepcopy(self.data);d['values'][next(iter(KEYS))]['fr'] = 'unexpected';mutations.append(d)
        d = deepcopy(self.data);d['values']['ui_save_your_changes'] = dict(d['values'][next(iter(KEYS))]);mutations.append(d)
        for d in mutations:
            with self.assertRaises(ValueError):require_wording_shape(d, KEYS, TAGS)


if __name__ == '__main__':
    unittest.main()
