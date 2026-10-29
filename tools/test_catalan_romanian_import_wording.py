"""26 bounded CA/RO P0 import/format values; no whole-language certification."""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape, require_string_root
from test_danish_norwegian_p0_wording import full_format_tokens, require_reviewed_string
import translation_catalogues as catalogues
from sk_sl_ca_priority_successors import current_fixture, added_keys, catalogue_count, current_display

KEYS = {'formats22_animation_message', 'formats22_animation_poster', 'formats22_animation_still',
        'formats22_animation_title', 'formats22_animation_unknown', 'formats22_ascii_description',
        'formats22_open_still', 'formats22_pdf_raster_hint', 'save20_gif_description',
        'save20_invalid_name', 'save20_lossy_quality_description', 'save20_unsupported_image_colour',
        'ui_higher_quality_usually_makes_a_larger_file_lossless'}
TAGS = {'default', 'ca', 'ro'}
HOLDS = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg', 'ui_save_as_jpeg_xl', 'ui_save_as_png'}

class CatalanRomanianImportWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(current_fixture('catalan_romanian_import_wording.json'), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('ca', 'values-ca'), ('ro', 'values-ro')]}
        cls.roots = {tag: ET.fromstring(value) for tag, value in cls.xml.items()}

    def test_exact_13_P0_values_attributes_and_complete_format_inventory(self):
        self.assertEqual(13, len(KEYS))
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
                    self.assertNotIn('formatted', self.data['constraints'][key][tag]['attributes'])

    def test_each_value_rejects_missing_duplicate_empty_truncation_markup_attributes_type_and_tokens(self):
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

    def test_refreshed_expected_text_cannot_hide_unindexed_nonargument_or_malformed_tokens(self):
        key = 'formats22_ascii_description'
        for tag in ('ca', 'ro'):
            for suffix in (' %s', ' %d', ' %.2f', ' %1$s', ' %%', ' %n', ' %', ' %q', ' %1$', ' %.', ' %t'):
                changed = self.data['values'][key][tag] + suffix
                root = ET.Element('resources');ET.SubElement(root, 'string', self.data['constraints'][key][tag]['attributes']).text = changed
                with self.subTest(tag=tag, suffix=suffix), self.assertRaises(ValueError):
                    require_reviewed_string(ET.tostring(root, encoding='unicode'), key, changed,
                        self.data['constraints'][key][tag], self.data['values'][key]['default'])
        # Synthetic compatibility check only: no selected real value has formatted=false.
        constraints = {'attributes': {'name': 'synthetic', 'formatted': 'false'}}
        for suffix in (' %s', ' %%', ' %n', ' %'):
            changed = 'literal' + suffix;root = ET.Element('resources')
            ET.SubElement(root, 'string', constraints['attributes']).text = changed
            with self.assertRaises(ValueError):
                require_reviewed_string(ET.tostring(root, encoding='unicode'), 'synthetic', changed, constraints, 'literal')

    def test_inherited_values_attributes_with_only_exact_reviewed_priority_successors(self):
        self.assertEqual({'ca', 'ro'}, set(self.data['preserved_values']))
        from test_translations import SCOPED_TAGS
        for tag in ('ca', 'ro'):
            preserved = self.data['preserved_values'][tag]
            self.assertEqual(137, len(preserved));self.assertFalse(set(preserved) & KEYS)
            for key, expected in preserved.items():
                with self.subTest(tag=tag, key=key):
                    require_string_root(self.roots[tag], key, expected['value'], {'attributes': expected['attributes']})
            self.assertEqual(catalogue_count(tag,205), len(self.roots[tag]));self.assertNotIn(tag, SCOPED_TAGS)
        self.assertEqual(59, len(SCOPED_TAGS))
        self.assertEqual(112, len(set(catalogues.offered_tags()) - SCOPED_TAGS))

    def test_five_holds_remain_while_explicit_reviewed_neighbors_advance(self):
        self.assertEqual(HOLDS, set(self.data['held_absent']))
        completion = current_fixture('catalan_romanian_completion_wording.json')
        for tag in ('ca', 'ro'):
            key = 'ui_assembly_source_memory_floor'
            require_reviewed_string(self.xml[tag], key, completion['values'][key][tag],
                                    completion['constraints'][key][tag], completion['values'][key]['default'])
            for key in HOLDS | {'formats22_at_least_frames', 'ui_no_resize_fits_decoder_memory'}:
                if key not in HOLDS:
                    successor = fixture('slovak_slovenian_catalan_priority_wording.json' if tag == 'ca' else 'ukrainian_lithuanian_romanian_priority_wording.json')['locales'][tag]['values'][key]
                    self.assertIsNone(successor['previous_target'])
                    require_string_root(self.roots[tag], key, successor['target'], {'attributes': successor['attributes']})
                else:
                    self.assertIsNone(self.roots[tag].find(f"./string[@name='{key}']"), (tag, key))
            self.assertEqual('"' + current_display(tag,'save20_file_format') + '"', self.roots[tag].find("./string[@name='save20_file_format']").text)
            self.assertEqual({'%1$s': 1, '%2$s': 1}, full_format_tokens(self.data['values']['formats22_animation_message'][tag]))
            self.assertEqual({'%1$s': 1}, full_format_tokens(self.data['values']['formats22_animation_unknown'][tag]))
        self.assertEqual('at least %1$d', self.roots['default'].find("./string[@name='formats22_at_least_frames']").text)
        self.assertEqual('Tramatge', self.roots['ca'].find("./string[@name='save20_dither']").text.strip('"'))
        self.assertEqual('Dithering', self.roots['ro'].find("./string[@name='save20_dither']").text.strip('"'))

    def test_source_product_and_numeric_literals_remain_in_exact_reviewed_values(self):
        for tag in ('ca', 'ro'):
            for key, literals in {'formats22_animation_message': ['AN Paint'],
                                  'formats22_animation_unknown': ['AN Paint'],
                                  'formats22_animation_poster': ['PNG'],
                                  'formats22_pdf_raster_hint': ['PDF', '144', 'dpi'],
                                  'save20_gif_description': ['GIF', '256'],
                                  'save20_unsupported_image_colour': ['AN Paint', 'sRGB', 'PNG']}.items():
                for literal in literals:self.assertIn(literal, self.data['values'][key][tag])

    def test_fixture_scope_rejects_missing_extra_empty_or_wrong_locale(self):
        mutations=[]
        d=deepcopy(self.data);d['values'].pop(next(iter(KEYS)));mutations.append(d)
        d=deepcopy(self.data);d['constraints'].pop(next(iter(KEYS)));mutations.append(d)
        d=deepcopy(self.data);d['values'][next(iter(KEYS))]['ca']='';mutations.append(d)
        d=deepcopy(self.data);d['values'][next(iter(KEYS))]['fr']='unexpected';mutations.append(d)
        d=deepcopy(self.data);d['values']['save20_file_format']=dict(d['values'][next(iter(KEYS))]);mutations.append(d)
        for data in mutations:
            with self.assertRaises(ValueError):require_wording_shape(data, KEYS, TAGS)

if __name__ == '__main__':
    unittest.main()
