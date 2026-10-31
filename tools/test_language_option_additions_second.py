"""Requested option and principal-variety identities; registration does not establish translation."""
ASSAMESE_OPTION_STATUS = 'partial-priority-reviewed'

import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from finite_resource_values import typed, require, _blank

import translation_catalogues as catalogues
from walloon_northern_sami_sanskrit_priority_expectations import SANSKRIT_OPTION_STATUS, require_sanskrit_option_successor
from language_option_additions import require_untranslated_option
from pidgin_tok_pisin_option_successors import require_pidgin_option_successor
from somali_wolof_haitian_creole_priority_expectations import SO_WO_HT_OPTION_TAGS, PRIORITY_OPTION_STATUS as SO_WO_HT_OPTION_STATUS, require_priority_option_successor as require_so_wo_ht_option_successor
from tajik_priority_option_successor import require_tajik_option_successor, TAJIK_OPTION_STATUS
from language_option_additions import ADDED_TAGS, FIRST_ADDED_TAGS, SECOND_ADDED_TAGS, SECOND_ADDITIONS_PATH

ROOT = Path(__file__).resolve().parents[1]
BATCHES = json.loads((ROOT / 'tools/fixtures/current_localization/reviewed_priority_batches.json').read_text())
BATCH_STATUS = 'partial independently reviewed wording; incomplete catalogue'
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
            self.assertEqual(BATCH_STATUS if tag in BATCHES['locales'] else SO_WO_HT_OPTION_STATUS if tag in SO_WO_HT_OPTION_TAGS else SANSKRIT_OPTION_STATUS if tag=='sa' else ASSAMESE_OPTION_STATUS if tag=='as' else 'not-started', rows[0]['translation_status'])
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
            if row['tag'] in SO_WO_HT_OPTION_TAGS:
                tag=row['tag'];root=require_so_wo_ht_option_successor(row,path.read_text())
                self.assertEqual([],catalogues.validate_catalogue(tag))
                missing_strings=strings-{n.get('name')for n in root if n.tag=='string'}
                missing_plurals=plurals-{n.get('name')for n in root if n.tag=='plurals'}
                self.assertTrue(missing_strings);self.assertFalse(missing_plurals)
                self.assertEqual([f"{tag}: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}"],catalogues.validate_catalogue(tag,require_complete=True))
                continue
            if row['tag']=='sa':
                root=require_sanskrit_option_successor(row,path.read_text())
                self.assertEqual([],catalogues.validate_catalogue('sa'))
                missing_strings=strings-{n.get('name')for n in root if n.tag=='string'}
                missing_plurals=plurals-{n.get('name')for n in root if n.tag=='plurals'}
                self.assertTrue(missing_strings);self.assertFalse(missing_plurals)
                self.assertEqual([f"sa: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}"],catalogues.validate_catalogue('sa',require_complete=True))
                continue
            if row['tag']=='as':
                root=ET.parse(path).getroot()
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
            if row['tag']=='tg':
                root=require_tajik_option_successor(row,path.read_text())
                self.assertIn('incomplete catalogue',TAJIK_OPTION_STATUS)
                self.assertEqual([],catalogues.validate_catalogue('tg'))
                present_strings={node.get('name') for node in root if node.tag=='string'}
                present_plurals={node.get('name') for node in root if node.tag=='plurals'}
                missing_strings=strings-present_strings;missing_plurals=plurals-present_plurals
                self.assertTrue(missing_strings)
                self.assertEqual(set(),missing_plurals)
                self.assertEqual([
                    f"tg: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}",
                ],catalogues.validate_catalogue('tg',require_complete=True))
                continue
            if row['tag'] in {'mi','sm'}:
                from maori_samoan_kinyarwanda_priority_expectations import require_empty_option_successor
                root=require_empty_option_successor(row,path.read_text())
                self.assertEqual([],catalogues.validate_catalogue(row['tag']))
                present_strings={n.get('name') for n in root if n.tag=='string'}
                present_plurals={n.get('name') for n in root if n.tag=='plurals'}
                missing_strings=strings-present_strings
                self.assertTrue(missing_strings)
                self.assertEqual(set(),plurals-present_plurals)
                self.assertEqual([f"{row['tag']}: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}"],catalogues.validate_catalogue(row['tag'],require_complete=True))
                continue
            if row['tag'] in ('pcm','tpi'):
                root=require_pidgin_option_successor(row,path.read_text())
                self.assertEqual([],catalogues.validate_catalogue(row['tag']))
                present_strings={node.get('name') for node in root if node.tag=='string'}
                present_plurals={node.get('name') for node in root if node.tag=='plurals'}
                missing_strings=strings-present_strings;missing_plurals=plurals-present_plurals
                self.assertTrue(missing_strings)
                self.assertEqual(set(),missing_plurals)
                self.assertEqual([f"{row['tag']}: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}"],catalogues.validate_catalogue(row['tag'],require_complete=True))
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







    def test_only_exact_full_priority_values_supersede_three_existing_second_batch_options(self):
        from copy import deepcopy
        rows=json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']
        for tag in sorted(SO_WO_HT_OPTION_TAGS):
            old=next(r for r in rows if r['tag']==tag);xml=(ROOT/old['catalogue']).read_text()
            require_so_wo_ht_option_successor(old,xml)
            with self.assertRaises(ValueError):require_untranslated_option(old,xml)
            for row in rows:
                if row['tag']!=tag:
                    with self.subTest(tag=tag,foreign=row['tag']),self.assertRaises(ValueError):require_so_wo_ht_option_successor(row,xml)
            for field,value in [('translation_status','complete'),('linguistic_review','accepted'),('fallback','translated'),('source_strings_present',346),('source_plurals_present',1)]:
                bad=deepcopy(old);bad[field]=value
                with self.subTest(tag=tag,field=field),self.assertRaises(ValueError):require_so_wo_ht_option_successor(bad,xml)
            original=ET.fromstring(xml)
            for index,node in enumerate(original):
                bad=deepcopy(original)
                if node.tag=='string':bad[index].text=(node.text or '')+' altered'
                else:bad[index][0].text=(node[0].text or '')+' altered'
                with self.subTest(tag=tag,key=node.get('name')),self.assertRaises(ValueError):require_so_wo_ht_option_successor(old,ET.tostring(bad,encoding='unicode'))
            for mode in ('missing','extra','attribute','tail','plural-text','plural-tail'):
                bad=deepcopy(original)
                if mode=='missing':bad.remove(bad[0])
                elif mode=='extra':ET.SubElement(bad,'string',name='unreviewed').text='unreviewed'
                elif mode=='tail':bad[0].tail='unreviewed text'
                elif mode=='plural-text':bad.find('./plurals').text='unreviewed text'
                elif mode=='plural-tail':bad.find('./plurals')[0].tail='unreviewed text'
                else:bad[0].set('formatted','false')
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_so_wo_ht_option_successor(old,ET.tostring(bad,encoding='unicode'))

    def test_only_exact_reviewed_tajik_values_supersede_the_original_empty_option(self):
        from copy import deepcopy
        rows=json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']
        old=next(row for row in rows if row['tag']=='tg')
        xml=(ROOT/old['catalogue']).read_text()
        require_tajik_option_successor(old,xml)
        with self.assertRaises(ValueError):require_untranslated_option(old,xml)
        for row in rows:
            if row['tag']!='tg':
                with self.subTest(tag=row['tag']),self.assertRaises(ValueError):require_tajik_option_successor(row,xml)
        for field,value in [('translation_status','complete'),('linguistic_review','accepted'),('fallback','translated'),('source_strings_present',345),('source_plurals_present',1)]:
            changed=deepcopy(old);changed[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):require_tajik_option_successor(changed,xml)
        for mode in ('missing','extra','duplicate','value','attribute','markup','plural-child','plural-quantity','plural-attribute','resource-tail','plural-parent','plural-tail'):
            root=ET.fromstring(xml)
            if mode=='missing':root.remove(root[0])
            elif mode=='extra':ET.SubElement(root,'string',name='unreviewed').text='unreviewed'
            elif mode=='duplicate':root.append(deepcopy(root[0]))
            elif mode=='value':root[0].text='unreviewed'
            elif mode=='attribute':root[0].set('formatted','false')
            elif mode=='markup':ET.SubElement(root[0],'b').text='unreviewed'
            elif mode=='plural-child':root.find('./plurals')[0].text='unreviewed'
            elif mode=='plural-quantity':root.find('./plurals')[0].set('quantity','one')
            elif mode=='plural-attribute':root.find('./plurals')[0].set('unreviewed','true')
            elif mode=='resource-tail':root[0].tail='unreviewed'
            elif mode=='plural-parent':root.find('./plurals').text='unreviewed'
            else:root.find('./plurals')[0].tail='unreviewed'
            with self.subTest(mode=mode),self.assertRaises(ValueError):require_tajik_option_successor(old,ET.tostring(root,encoding='unicode'))

    def test_each_tajik_typed_resource_rejects_complete_text_corruption(self):
        old=next(row for row in json.loads(SECOND_ADDITIONS_PATH.read_text())['languages'] if row['tag']=='tg')
        xml=(ROOT/old['catalogue']).read_text();original=ET.fromstring(xml)
        self.assertEqual(356,len(original))
        for index,node in enumerate(original):
            root=ET.fromstring(xml);changed=root[index]
            if changed.tag=='string':changed.text+=' unreviewed'
            else:changed[0].text+=' unreviewed'
            with self.subTest(identity=node.get('name')),self.assertRaises(ValueError):require_tajik_option_successor(old,ET.tostring(root,encoding='unicode'))



    def test_only_complete_reviewed_mi_sm_values_supersede_empty_options(self):
        from copy import deepcopy
        from maori_samoan_kinyarwanda_priority_expectations import require_empty_option_successor
        rows=json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']
        for tag in ('mi','sm'):
            old=next(r for r in rows if r['tag']==tag);xml=(ROOT/old['catalogue']).read_text()
            require_empty_option_successor(old,xml)
            with self.assertRaises(ValueError):require_untranslated_option(old,xml)
            for other in rows:
                if other['tag']!=tag:
                    with self.subTest(tag=tag,other=other['tag']),self.assertRaises(ValueError):require_empty_option_successor(other,xml)
            for field in old:
                bad=deepcopy(old);bad[field]='forged'
                with self.subTest(tag=tag,field=field),self.assertRaises(ValueError):require_empty_option_successor(bad,xml)
            for mode in ('missing','extra','duplicate','value','attribute','plural-child','plural-text','plural-tail','item-tail','root-text','root-attribute','string-child'):
                root=ET.fromstring(xml);plural=root.find('./plurals')
                if mode=='missing':root.remove(root[0])
                elif mode=='extra':ET.SubElement(root,'string',name='unreviewed').text='unreviewed'
                elif mode=='duplicate':root.append(deepcopy(root[0]))
                elif mode=='value':root[0].text='not accepted'
                elif mode=='attribute':root[0].set('formatted','false')
                elif mode=='plural-child':plural[0].text='incomplete'
                elif mode=='plural-text':plural.text='forged'
                elif mode=='plural-tail':plural.tail='forged'
                elif mode=='item-tail':plural[0].tail='forged'
                elif mode=='root-text':root.text='forged'
                elif mode=='root-attribute':root.set('forged','yes')
                else:ET.SubElement(root[0],'b').text='forged'
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_empty_option_successor(old,ET.tostring(root,encoding='unicode'))


    def test_only_exact_reviewed_sanskrit_values_supersede_the_original_empty_option(self):
        from copy import deepcopy
        rows=json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']
        old=next(r for r in rows if r['tag']=='sa')
        xml=(ROOT/old['catalogue']).read_text()
        require_sanskrit_option_successor(old,xml)
        with self.assertRaises(ValueError):require_untranslated_option(old,xml)
        for row in rows:
            if row['tag']!='sa':
                with self.subTest(tag=row['tag']),self.assertRaises(ValueError):require_sanskrit_option_successor(row,xml)
        for field,value in [('translation_status','complete'),('linguistic_review','accepted'),('fallback','translated'),('source_strings_present',349)]:
            bad=deepcopy(old);bad[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):require_sanskrit_option_successor(bad,xml)
        for mode in ('missing','extra','value','attribute','plural-child'):
            root=ET.fromstring(xml)
            if mode=='missing':root.remove(root[0])
            elif mode=='extra':ET.SubElement(root,'string',name='unreviewed').text='unreviewed'
            elif mode=='value':root[0].text='not the accepted value'
            elif mode=='attribute':root[0].set('formatted','false')
            else:root.find('./plurals')[0].text='incomplete child'
            with self.subTest(mode=mode),self.assertRaises(ValueError):require_sanskrit_option_successor(old,ET.tostring(root,encoding='unicode'))




if __name__ == '__main__':
    unittest.main()
