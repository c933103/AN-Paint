"""Requested option and principal-variety identities; registration does not establish translation."""

import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from finite_resource_values import typed, require, _blank

import translation_catalogues as catalogues
from language_option_additions import require_untranslated_option
from language_option_additions import ADDED_TAGS, FIRST_ADDED_TAGS, SECOND_ADDED_TAGS, SECOND_ADDITIONS_PATH

ROOT = Path(__file__).resolve().parents[1]
BATCHES = json.loads((ROOT / 'tools/fixtures/current_localization/reviewed_priority_batches.json').read_text())
EXPECTED = {'pcm': 'Naijá', 'so': 'Soomaaliga', 'as': 'অসমীয়া', 'wo': 'Wolof',
            'ht': 'Kreyòl ayisyen', 'tpi': 'Tok Pisin', 'nv': 'Diné bizaad', 'chr': 'ᏣᎳᎩ',
            'yua': 'Maaya t’aan', 'ch': 'Chamoru',
            'nch': 'Mexicano (Central Huasteca)', 'nhe': 'Náhuatl (Eastern Huasteca)',
            'nhw': 'Náhuatl (Western Huasteca)', 'quz': 'Qichwa (Cusco)',
            'quy': 'Qichwa (Ayacucho / Chanka)', 'quh': 'Qhichwa (South Bolivian)',
            'qug': 'Kichwa (Chimborazo)',
            'sm': 'Gagana Samoa', 'mi': 'Māori', 'sa': 'संस्कृतम्', 'tg': 'Тоҷикӣ'}


def reviewed_batch_values(xml):
    root = ET.fromstring(xml)
    require(root.tag == 'resources' and not root.attrib, 'Unexpected resource root')
    require(_blank(root.text) and _blank(root.tail), 'Unexpected resource root text')
    result = {}
    for node in root:
        row = typed(node)  # Reject nested content and nonblank resource tails.
        require(row['type'] == 'string', 'Unexpected batch resource type')
        name = node.get('name')
        require(name is not None and name not in result, 'Missing or duplicate resource name')
        result[name] = {'attributes': row['attributes'], 'value': row['value']}
    return result


class FurtherLanguageOptionTests(unittest.TestCase):
    def test_requested_concrete_identities_match_all_active_and_recorded_inventories(self):
        data = json.loads(SECOND_ADDITIONS_PATH.read_text())
        self.assertEqual(set(EXPECTED), SECOND_ADDED_TAGS)
        self.assertEqual(21, len(data['languages']))
        self.assertEqual(len(EXPECTED), len(data['languages']))
        self.assertEqual(EXPECTED, {r['tag']: r['name'] for r in data['languages']})
        self.assertFalse(FIRST_ADDED_TAGS & SECOND_ADDED_TAGS)
        self.assertEqual(27, len(ADDED_TAGS))
        tags = catalogues.offered_tags()
        self.assertEqual(171, len(tags)); self.assertEqual(171, len(set(tags)))
        self.assertEqual(tags, [n.get('{http://schemas.android.com/apk/res/android}name')
                               for n in ET.parse(catalogues.RES / 'xml/app_locales.xml').getroot()])
        names = [n.text for n in ET.parse(catalogues.RES / 'values/app_language_names.xml').findall(
            ".//string-array[@name='app_language_names']/item")]
        by_tag = dict(zip(tags, names))
        options = json.loads((ROOT / 'translations/language-options.json').read_text())['options']
        for tag, name in EXPECTED.items():
            self.assertEqual(name, by_tag[tag])
            rows = [r for r in options if r['tag'] == tag]
            self.assertEqual(1, len(rows)); self.assertEqual(name, rows[0]['name'])
            self.assertEqual('default-English', rows[0]['fallback'])
            self.assertEqual(catalogues.RES / f'values-b+{tag}/strings.xml', catalogues.catalogue_paths()[tag])

    def test_reviewed_batches_exact_values_and_preserved_existing_entries(self):
        expected_counts = {'ch': 68, 'shn': 156, 'za': 39, 'nv': 12,
                           'yua': 49, 'qug': 51, 'quh': 53, 'quz': 53}
        self.assertEqual(expected_counts, {t: len(v['accepted']) for t,v in BATCHES['locales'].items()})
        self.assertEqual(474, sum(len(v['added']) for v in BATCHES['locales'].values()))
        self.assertEqual(1, sum(len(v['updated']) for v in BATCHES['locales'].values()))
        self.assertEqual(6, sum(len(v['unchanged']) for v in BATCHES['locales'].values()))
        for tag, loc in BATCHES['locales'].items():
            actual = reviewed_batch_values(catalogues.catalogue_paths()[tag].read_text())
            from current_localization_contracts import residual_rows
            expected={**loc['existing_unreviewed'], **loc['accepted']}
            for (locale,key),row in residual_rows().items():
                if locale!=tag:continue
                self.assertEqual(expected.get(key,{}).get('value'),row['previous_target'])
                expected[key]={'value':row['target'],'attributes':row['attributes']}
            self.assertEqual(expected, actual, tag)
            self.assertEqual(set(loc['accepted']), set(loc['added']) | set(loc['updated']) | set(loc['unchanged']))
            for key, row in loc['accepted'].items():
                self.assertEqual([], catalogues.android_string_errors(row['value']), tag+'/'+key)
                self.assertEqual([], catalogues.format_string_errors(row['value'], row['attributes'].get('formatted') != 'false'), tag+'/'+key)
            self.assertEqual([], catalogues.validate_catalogue(tag))
            self.assertTrue(catalogues.validate_catalogue(tag, require_complete=True))
        self.assertEqual(9, len(BATCHES['locales']['za']['existing_unreviewed']))
        self.assertNotIn('tdd', BATCHES['locales'])
        self.assertNotIn('quy', BATCHES['locales'])

    def test_reviewed_batches_reject_hidden_markup_tails_and_wrong_xml_shape(self):
        for tag in BATCHES['locales']:
            xml = catalogues.catalogue_paths()[tag].read_text()
            for mode in ('child', 'child-tail', 'resource-tail', 'root-text',
                         'root-tag', 'root-attribute', 'wrong-type', 'duplicate'):
                root = ET.fromstring(xml)
                if mode in ('child', 'child-tail'):
                    child = ET.SubElement(root[0], 'b')
                    if mode == 'child': child.text = 'unreviewed addition'
                    else: child.tail = 'unreviewed addition'
                elif mode == 'resource-tail': root[0].tail = 'unreviewed addition'
                elif mode == 'root-text': root.text = 'unreviewed addition'
                elif mode == 'root-tag': root.tag = 'unreviewed'
                elif mode == 'root-attribute': root.set('unreviewed', 'true')
                elif mode == 'wrong-type': root[0].tag = 'item'
                else: root.append(ET.fromstring(ET.tostring(root[0], encoding='unicode')))
                with self.subTest(tag=tag, mode=mode), self.assertRaises(ValueError):
                    reviewed_batch_values(ET.tostring(root, encoding='unicode'))

    def test_principal_varieties_replace_broad_groups_with_exact_scope(self):
        data = json.loads(SECOND_ADDITIONS_PATH.read_text())
        rows = {r['tag']: r for r in data['languages']}
        self.assertEqual(set(), {t for t, r in rows.items() if r['registry_scope'] == 'collection'})
        self.assertEqual({'sa'}, {t for t, r in rows.items() if r['registry_scope'] == 'macrolanguage'})
        self.assertEqual(20, sum(r['registry_scope'] == 'individual' for r in rows.values()))
        varieties = {'nch', 'nhe', 'nhw', 'quz', 'quy', 'quh', 'qug'}
        self.assertEqual(varieties, set(data['selection_decision']['principal_variety_tags']))
        self.assertEqual({'nah', 'qu'}, set(data['selection_decision']['removed_umbrella_tags']))
        self.assertTrue(data['selection_decision']['selection_not_exhaustive'])
        self.assertFalse({'nah', 'qu'} & set(catalogues.offered_tags()))
        self.assertFalse({'nah', 'qu'} & set(catalogues.catalogue_paths()))
        self.assertEqual({'nch', 'nhe', 'nhw'}, {t for t, r in rows.items() if r.get('requested_group') == 'Nahuatl'})
        self.assertEqual({'quz', 'quy', 'quh', 'qug'}, {t for t, r in rows.items() if r.get('requested_group') == 'Quechua'})
        self.assertIn('does not cover all Southern Quechua', rows['quz']['scope_note'])
        self.assertIn('does not cover all Ecuadorian Kichwa', rows['qug']['scope_note'])
        self.assertIn('not an exact qug census', rows['qug']['scope_note'])
        options = {r['tag']: r for r in json.loads((ROOT / 'translations/language-options.json').read_text())['options']}
        for tag in EXPECTED:
            self.assertEqual(rows[tag]['registry_scope'], options[tag]['registry_scope'])
            if tag in varieties | {'sa'}:
                self.assertEqual(rows[tag]['scope_note'], options[tag]['scope_note'])
                self.assertIn(rows[tag]['scope_note'], (ROOT / rows[tag]['catalogue']).read_text())

    def test_current_catalogue_completeness_is_separate_from_historical_empty_records(self):
        defaults, default_plurals, strings, plurals = catalogues.default_resources()
        self.assertTrue(strings); self.assertTrue(plurals)
        self.assertLessEqual(strings, set(defaults)); self.assertLessEqual(plurals, set(default_plurals))
        for row in json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']:
            path = ROOT / row['catalogue']
            if row['tag'] in BATCHES['locales']:
                tag = row['tag']
                self.assertEqual([], catalogues.validate_catalogue(tag))
                self.assertTrue(catalogues.validate_catalogue(tag, require_complete=True))
                self.assertEqual('default-English', row['fallback'])
                continue
            if row['tag'] in {'as', 'so', 'wo', 'ht', 'tg', 'mi', 'sm', 'sa', 'pcm', 'tpi'}:
                # Current resources may evolve without rewriting an old empty registration.
                self.assertEqual([], catalogues.validate_catalogue(row['tag']))
                continue
            require_untranslated_option(row, path.read_text())
            self.assertEqual('not-started', row['translation_status'])
            self.assertEqual('not-started', row['linguistic_review'])
            self.assertEqual('default-English', row['fallback'])
            self.assertEqual(0, row['source_strings_present']); self.assertEqual(0, row['source_plurals_present'])
            self.assertEqual([], list(ET.parse(path).getroot()))
            self.assertEqual([], catalogues.validate_catalogue(row['tag']))
            self.assertEqual([
                f"{row['tag']}: missing {len(strings)} strings: {', '.join(sorted(strings)[:20])}",
                f"{row['tag']}: missing plural resources: {', '.join(sorted(plurals))}",
            ], catalogues.validate_catalogue(row['tag'], require_complete=True))


















if __name__ == '__main__':
    unittest.main()
