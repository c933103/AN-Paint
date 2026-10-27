"""Requested option and principal-variety identities; registration does not establish translation."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as catalogues
from language_option_additions import require_untranslated_option
from assamese_khmer_lao_priority_expectations import ASSAMESE_OPTION_STATUS, require_assamese_option_successor
from language_option_additions import ADDED_TAGS, FIRST_ADDED_TAGS, SECOND_ADDED_TAGS, SECOND_ADDITIONS_PATH

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {'pcm': 'Naijá', 'so': 'Soomaaliga', 'as': 'অসমীয়া', 'wo': 'Wolof',
            'ht': 'Kreyòl ayisyen', 'tpi': 'Tok Pisin', 'nv': 'Diné bizaad', 'chr': 'ᏣᎳᎩ',
            'yua': 'Maaya t’aan', 'ch': 'Chamoru',
            'nch': 'Mexicano (Central Huasteca)', 'nhe': 'Náhuatl (Eastern Huasteca)',
            'nhw': 'Náhuatl (Western Huasteca)', 'quz': 'Qichwa (Cusco)',
            'quy': 'Qichwa (Ayacucho / Chanka)', 'quh': 'Qhichwa (South Bolivian)',
            'qug': 'Kichwa (Chimborazo)',
            'sm': 'Gagana Samoa', 'mi': 'Māori', 'sa': 'संस्कृतम्', 'tg': 'Тоҷикӣ'}


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
            self.assertEqual(ASSAMESE_OPTION_STATUS if tag=='as' else 'not-started', rows[0]['translation_status'])
            self.assertEqual('default-English', rows[0]['fallback'])
            self.assertEqual(catalogues.RES / f'values-b+{tag}/strings.xml', catalogues.catalogue_paths()[tag])

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

    def test_untranslated_catalogues_remain_empty_and_completeness_stays_honest(self):
        defaults, default_plurals, strings, plurals = catalogues.default_resources()
        self.assertTrue(strings); self.assertTrue(plurals)
        self.assertLessEqual(strings, set(defaults)); self.assertLessEqual(plurals, set(default_plurals))
        for row in json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']:
            path = ROOT / row['catalogue']
            if row['tag']=='as':
                root=require_assamese_option_successor(row,path.read_text())
                self.assertEqual([],catalogues.validate_catalogue('as'))
                present_strings={n.get('name') for n in root if n.tag=='string'}
                present_plurals={n.get('name') for n in root if n.tag=='plurals'}
                missing_strings=strings-present_strings;missing_plurals=plurals-present_plurals
                self.assertTrue(missing_strings)
                # The sole canonical plural resource is in the reviewed atomic dependency set.
                self.assertEqual(set(),missing_plurals)
                self.assertEqual([
                    f"as: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}",
                ],catalogues.validate_catalogue('as',require_complete=True))
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


    def test_only_exact_reviewed_assamese_values_supersede_the_original_empty_option(self):
        from copy import deepcopy
        rows=json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']
        old=next(r for r in rows if r['tag']=='as')
        xml=(ROOT/old['catalogue']).read_text()
        require_assamese_option_successor(old,xml)
        with self.assertRaises(ValueError):require_untranslated_option(old,xml)
        for row in rows:
            if row['tag']!='as':
                with self.subTest(tag=row['tag']),self.assertRaises(ValueError):require_assamese_option_successor(row,xml)
        for field,value in [('translation_status','complete'),('linguistic_review','accepted'),('fallback','translated'),('source_strings_present',349)]:
            bad=deepcopy(old);bad[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):require_assamese_option_successor(bad,xml)
        for mode in ('missing','extra','value','attribute','plural-child'):
            root=ET.fromstring(xml)
            if mode=='missing':root.remove(root[0])
            elif mode=='extra':ET.SubElement(root,'string',name='unreviewed').text='unreviewed'
            elif mode=='value':root[0].text='not the accepted value'
            elif mode=='attribute':root[0].set('formatted','false')
            else:root.find('./plurals')[0].text='incomplete child'
            with self.subTest(mode=mode),self.assertRaises(ValueError):require_assamese_option_successor(old,ET.tostring(root,encoding='unicode'))




if __name__ == '__main__':
    unittest.main()
