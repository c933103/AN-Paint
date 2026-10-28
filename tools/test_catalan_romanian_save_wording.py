"""Twenty bounded CA/RO P0 Save/export/share values; no whole-locale acceptance."""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
from test_danish_norwegian_p0_wording import full_format_tokens, require_reviewed_string
import translation_catalogues as catalogues
from sk_sl_ca_priority_successors import current_fixture, added_keys, catalogue_count, current_display

KEYS = {'ui_your_current_image_has_unsaved_changes', 'ui_could_not_save_image', 'ui_saved',
        'ui_export_did_not_save23', 'ui_save_explanation23', 'ui_export_explanation23',
        'ui_share_explanation34', 'ui_save_and_share', 'ui_save_and_share_41edb4',
        'ui_the_image_was_saved_but_android_could_not'}
TAGS = {'default', 'ca', 'ro'}
HOLDS = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg',
         'ui_save_as_jpeg_xl', 'ui_save_as_png'}


class CatalanRomanianSaveWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(current_fixture('catalan_romanian_save_wording.json'), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('ca', 'values-ca'), ('ro', 'values-ro')]}
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

    def test_every_new_value_rejects_missing_duplicate_empty_truncated_markup_attributes_type_and_placeholder(self):
        for tag in ('ca', 'ro'):
            for key in KEYS:
                original = self.roots[tag].find(f"./string[@name='{key}']")
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
                    with self.subTest(tag=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                        require_reviewed_string(ET.tostring(root, encoding='unicode'), key,
                            self.data['values'][key][tag], self.data['constraints'][key][tag],
                            self.data['values'][key]['default'])

    def test_formatted_false_cannot_hide_extra_unindexed_or_nonargument_tokens_with_refreshed_expected(self):
        key = 'ui_share_explanation34'
        for tag in ('ca', 'ro'):
            constraints = self.data['constraints'][key][tag]
            self.assertEqual('false', constraints['attributes']['formatted'])
            source = self.data['values'][key]['default']
            self.assertFalse(full_format_tokens(source))
            for suffix in (' %s', ' %d', ' %.2f', ' %1$s', ' %%', ' %n',
                           ' %', ' %q', ' %1$', ' %.', ' %3$.', ' %3$.f', ' %t'):
                changed = self.data['values'][key][tag] + suffix
                node = ET.Element('string', constraints['attributes']);node.text = changed
                root = ET.Element('resources');root.append(node)
                with self.subTest(tag=tag, suffix=suffix), self.assertRaises(ValueError):
                    require_reviewed_string(ET.tostring(root, encoding='unicode'), key,
                                            changed, constraints, source)

    def test_inherited_values_attributes_with_only_exact_reviewed_priority_successors(self):
        self.assertEqual({'ca', 'ro'}, set(self.data['preserved_values']))
        from test_translations import SCOPED_TAGS
        for tag in ('ca', 'ro'):
            preserved = self.data['preserved_values'][tag]
            self.assertEqual(127, len(preserved));self.assertFalse(set(preserved) & KEYS)
            for key, expected in preserved.items():
                with self.subTest(tag=tag, key=key):
                    require_string(self.xml[tag], key, expected['value'], {'attributes': expected['attributes']})
            self.assertEqual(catalogue_count(tag,205), len(self.roots[tag]));self.assertNotIn(tag, SCOPED_TAGS)
            self.assertEqual('"' + current_display(tag,'save20_file_format') + '"', self.roots[tag].find("./string[@name='save20_file_format']").text)
        self.assertEqual('"'+current_display('ca','ui_save_your_changes')+'"', self.roots['ca'].find("./string[@name='ui_save_your_changes']").text)
        self.assertEqual('Salvaţi modificările?', self.roots['ro'].find("./string[@name='ui_save_your_changes']").text)
        self.assertEqual(59, len(SCOPED_TAGS))
        self.assertEqual(112, len(set(catalogues.offered_tags()) - SCOPED_TAGS))

    def test_five_holds_remain_while_explicit_reviewed_neighbors_advance(self):
        self.assertEqual(HOLDS, set(self.data['held_absent']))
        completion = current_fixture('catalan_romanian_completion_wording.json')
        for tag in ('ca', 'ro'):
            key = 'ui_assembly_source_memory_floor'
            require_reviewed_string(self.xml[tag], key, completion['values'][key][tag],
                                    completion['constraints'][key][tag], completion['values'][key]['default'])
            for key in HOLDS | {'ui_choose_location', 'ui_share_saved_image',
                                'ui_no_resize_fits_decoder_memory', 'ui_load_image'}:
                if key not in HOLDS:
                    successor = fixture('slovak_slovenian_catalan_priority_wording.json' if tag == 'ca' else 'ukrainian_lithuanian_romanian_priority_wording.json')['locales'][tag]['values'][key]
                    self.assertIsNone(successor['previous_target'])
                    require_string(self.xml[tag], key, successor['target'], {'attributes': successor['attributes']})
                else:
                    self.assertIsNone(self.roots[tag].find(f"./string[@name='{key}']"), (tag, key))
        self.assertEqual('Choose location…', self.roots['default'].find("./string[@name='ui_choose_location']").text)
        self.assertEqual('Share saved image', self.roots['default'].find("./string[@name='ui_share_saved_image']").text)

    def test_actual_action_labels_share_pair_and_product_literals_are_consistent(self):
        for tag, save, save_as in [('ca', 'Desa', 'Anomena i desa…'), ('ro', 'Salvează', 'Salvează ca…')]:
            value = lambda k: self.data['values'][k][tag][1:-1]
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

    def test_fixture_family_rejects_missing_extra_empty_or_wrong_locale_scope(self):
        mutations = []
        d = deepcopy(self.data);d['values'].pop(next(iter(KEYS)));mutations.append(d)
        d = deepcopy(self.data);d['constraints'].pop(next(iter(KEYS)));mutations.append(d)
        d = deepcopy(self.data);d['values'][next(iter(KEYS))]['ca'] = '';mutations.append(d)
        d = deepcopy(self.data);d['values'][next(iter(KEYS))]['fr'] = 'unexpected';mutations.append(d)
        d = deepcopy(self.data);d['values']['ui_save_your_changes'] = dict(d['values'][next(iter(KEYS))]);mutations.append(d)
        for d in mutations:
            with self.assertRaises(ValueError):require_wording_shape(d, KEYS, TAGS)


if __name__ == '__main__':
    unittest.main()
