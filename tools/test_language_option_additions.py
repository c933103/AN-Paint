"""Current option identities and truthful zero-coverage status; not linguistic acceptance."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as catalogues
from language_option_additions import require_untranslated_option
from javanese_sundanese_kyrgyz_priority_expectations import SUNDANESE_OPTION_STATUS, require_sundanese_option_successor
from yoruba_zulu_xhosa_priority_expectations import YO_ZU_OPTION_TAGS, PRIORITY_OPTION_STATUS as YO_ZU_OPTION_STATUS, require_priority_option_successor as require_yo_zu_option_successor
from hausa_igbo_lingala_priority_expectations import TAGS as PRIORITY_OPTION_TAGS, PRIORITY_OPTION_STATUS, require_priority_option_successor
from language_option_additions import FIRST_ADDED_TAGS, ADDITIONS_PATH

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {'ha': 'Hausa', 'ig': 'Igbo', 'ln': 'Lingála', 'su': 'Sunda', 'yo': 'Yorùbá', 'zu': 'isiZulu'}


class LanguageOptionAdditionTests(unittest.TestCase):
    def test_six_requested_identities_match_picker_platform_metadata_and_catalogues(self):
        data = json.loads(ADDITIONS_PATH.read_text())
        self.assertEqual(set(EXPECTED), FIRST_ADDED_TAGS)
        self.assertEqual(len(EXPECTED), len(data['languages']))
        self.assertEqual(EXPECTED, {r['tag']: r['name'] for r in data['languages']})
        tags = catalogues.offered_tags()
        self.assertEqual(171, len(tags)); self.assertEqual(171, len(set(tags)))
        self.assertEqual(tags, [n.get('{http://schemas.android.com/apk/res/android}name')
                               for n in ET.parse(catalogues.RES / 'xml/app_locales.xml').getroot()])
        names = [n.text for n in ET.parse(catalogues.RES / 'values/app_language_names.xml').findall(
            ".//string-array[@name='app_language_names']/item")]
        by_tag = dict(zip(tags, names))
        options = json.loads((ROOT / 'translations/language-options.json').read_text())['options']
        # Retained metadata has older aliases and excludes the two test modes.
        # Check only the six appended identities; live inventory authority is XML.
        for tag, name in EXPECTED.items():
            self.assertEqual(name, by_tag[tag])
            entries = [r for r in options if r['tag'] == tag]
            self.assertEqual(1, len(entries))
            self.assertEqual(name, entries[0]['name'])
            self.assertEqual(YO_ZU_OPTION_STATUS if tag in YO_ZU_OPTION_TAGS else PRIORITY_OPTION_STATUS if tag in PRIORITY_OPTION_TAGS else SUNDANESE_OPTION_STATUS if tag=='su' else 'not-started', entries[0]['translation_status'])
            self.assertEqual('default-English', entries[0]['fallback'])
            self.assertEqual(catalogues.RES / f'values-b+{tag}/strings.xml', catalogues.catalogue_paths()[tag])

    def test_new_catalogues_honestly_declare_untranslated_default_fallback(self):
        data = json.loads(ADDITIONS_PATH.read_text())
        defaults, plurals, source_strings, source_plurals = catalogues.default_resources()
        self.assertTrue(source_strings); self.assertTrue(source_plurals)
        self.assertLessEqual(source_strings, set(defaults)); self.assertLessEqual(source_plurals, set(plurals))
        for row in data['languages']:
            self.assertEqual('not-started', row['translation_status'])
            self.assertEqual('not-started', row['linguistic_review'])
            self.assertEqual('default-English', row['fallback'])
            path = ROOT / row['catalogue']
            if row['tag'] in YO_ZU_OPTION_TAGS:
                tag=row['tag'];root=require_yo_zu_option_successor(row,path.read_text())
                self.assertEqual([],catalogues.validate_catalogue(tag))
                missing_strings=source_strings-{n.get('name')for n in root if n.tag=='string'}
                missing_plurals=source_plurals-{n.get('name')for n in root if n.tag=='plurals'}
                self.assertTrue(missing_strings);self.assertFalse(missing_plurals)
                self.assertEqual([f"{tag}: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}"],catalogues.validate_catalogue(tag,require_complete=True))
                continue
            if row['tag'] in PRIORITY_OPTION_TAGS:
                tag=row['tag'];root=require_priority_option_successor(row,path.read_text())
                self.assertEqual([],catalogues.validate_catalogue(tag))
                missing_strings=source_strings-{n.get('name')for n in root if n.tag=='string'}
                missing_plurals=source_plurals-{n.get('name')for n in root if n.tag=='plurals'}
                self.assertTrue(missing_strings);self.assertFalse(missing_plurals)
                self.assertEqual([f"{tag}: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}"],catalogues.validate_catalogue(tag,require_complete=True))
                continue
            if row['tag']=='su':
                root=require_sundanese_option_successor(row,path.read_text())
                self.assertEqual([],catalogues.validate_catalogue('su'))
                present_strings={n.get('name') for n in root if n.tag=='string'}
                present_plurals={n.get('name') for n in root if n.tag=='plurals'}
                missing_strings=source_strings-present_strings;missing_plurals=source_plurals-present_plurals
                self.assertTrue(missing_strings);self.assertFalse(missing_plurals)
                self.assertEqual([
                    f"su: missing {len(missing_strings)} strings: {', '.join(sorted(missing_strings)[:20])}",
                ],catalogues.validate_catalogue('su',require_complete=True))
                continue
            require_untranslated_option(row, path.read_text())
            self.assertEqual([], list(ET.parse(path).getroot()), row['tag'])
            self.assertEqual({}, catalogues.read_strings(path))
            self.assertEqual({}, catalogues.read_plurals(path))
            self.assertEqual([], catalogues.validate_catalogue(row['tag']))
            self.assertEqual([
                f"{row['tag']}: missing {len(source_strings)} strings: {', '.join(sorted(source_strings)[:20])}",
                f"{row['tag']}: missing plural resources: {', '.join(sorted(source_plurals))}",
            ], catalogues.validate_catalogue(row['tag'], require_complete=True))
        self.assertIn('New or untranslated text appears in English.', defaults['language20_translation_note'])

    def test_false_translation_status_or_nonempty_fallback_catalogues_are_rejected(self):
        from copy import deepcopy
        row = next(r for r in json.loads(ADDITIONS_PATH.read_text())['languages'] if r['tag']=='yo')
        current_xml = (ROOT / row['catalogue']).read_text()
        with self.assertRaises(ValueError):require_untranslated_option(row,current_xml)
        # The frozen zero-coverage row is still strict; current accepted values are separately bound.
        xml = '<resources/>'
        require_untranslated_option(row, xml)
        for field, value in (('translation_status', 'complete'), ('linguistic_review', 'accepted'),
                             ('fallback', 'translated'), ('source_strings_present', 1),
                             ('source_plurals_present', 1)):
            changed = deepcopy(row); changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_untranslated_option(changed, xml)
            del changed[field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                require_untranslated_option(changed, xml)
        for broken in ('<resources><string name="ui_menu_file">File</string></resources>',
                       '<resources><plurals name="items"><item quantity="other">Items</item></plurals></resources>',
                       '<resources>Unreviewed English</resources>', '<catalogue/>'):
            with self.subTest(xml=broken), self.assertRaises(ValueError):
                require_untranslated_option(row, broken)
    def test_sundanese_residual_additions_keep_strict_shape_source_and_predecessors(self):
        from copy import deepcopy
        from unittest.mock import patch
        from current_localization_contracts import residual_rows
        old=next(row for row in json.loads(ADDITIONS_PATH.read_text())['languages'] if row['tag']=='su')
        original=ET.parse(ROOT/old['catalogue']).getroot();rows=residual_rows()
        keys={key for tag,key in rows if tag=='su'}
        self.assertEqual(7,len(keys));self.assertEqual(356,len(original))
        require_sundanese_option_successor(old,ET.tostring(original,encoding='unicode'))
        for key in keys:
            for mode in ('missing','duplicate','type','value','attribute','child','tail'):
                root=deepcopy(original);node=root.find(f"./string[@name='{key}']")
                if mode=='missing':root.remove(node)
                elif mode=='duplicate':root.append(deepcopy(node))
                elif mode=='type':node.tag='plurals'
                elif mode=='value':node.text+=' forged'
                elif mode=='attribute':node.set('formatted','false')
                elif mode=='child':ET.SubElement(node,'b')
                else:node.tail='unreviewed'
                with self.subTest(key=key,mode=mode),self.assertRaises(ValueError):
                    require_sundanese_option_successor(old,ET.tostring(root,encoding='unicode'))
            for field in ('source','previous_target'):
                changed=deepcopy(rows);changed[('su',key)][field]='forged'
                with patch('current_localization_contracts.residual_rows',return_value=changed):
                    with self.subTest(key=key,field=field),self.assertRaises(ValueError):
                        require_sundanese_option_successor(old,ET.tostring(original,encoding='unicode'))

    def test_only_exact_reviewed_sundanese_values_supersede_the_original_empty_option(self):
        from copy import deepcopy
        rows=json.loads(ADDITIONS_PATH.read_text())['languages']
        old=next(r for r in rows if r['tag']=='su')
        xml=(ROOT/old['catalogue']).read_text()
        require_sundanese_option_successor(old,xml)
        with self.assertRaises(ValueError):require_untranslated_option(old,xml)
        for row in rows:
            if row['tag']!='su':
                with self.subTest(tag=row['tag']),self.assertRaises(ValueError):require_sundanese_option_successor(row,xml)
        for field,value in [('translation_status','complete'),('linguistic_review','accepted'),('fallback','translated'),('source_strings_present',349)]:
            bad=deepcopy(old);bad[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):require_sundanese_option_successor(bad,xml)
        for mode in ('missing','extra','value','attribute','plural-child'):
            root=ET.fromstring(xml)
            if mode=='missing':root.remove(root[0])
            elif mode=='extra':ET.SubElement(root,'string',name='unreviewed').text='unreviewed'
            elif mode=='value':root[0].text='not the accepted value'
            elif mode=='attribute':root[0].set('formatted','false')
            else:root.find('./plurals')[0].text='incomplete child'
            with self.subTest(mode=mode),self.assertRaises(ValueError):require_sundanese_option_successor(old,ET.tostring(root,encoding='unicode'))




    def test_only_exact_full_priority_values_supersede_three_original_empty_options(self):
        from copy import deepcopy
        rows=json.loads(ADDITIONS_PATH.read_text())['languages']
        for tag in sorted(PRIORITY_OPTION_TAGS):
            old=next(r for r in rows if r['tag']==tag);xml=(ROOT/old['catalogue']).read_text()
            require_priority_option_successor(old,xml)
            with self.assertRaises(ValueError):require_untranslated_option(old,xml)
            for row in rows:
                if row['tag']!=tag:
                    with self.subTest(tag=tag,foreign=row['tag']),self.assertRaises(ValueError):require_priority_option_successor(row,xml)
            for field,value in [('translation_status','complete'),('linguistic_review','accepted'),('fallback','translated'),('source_strings_present',346)]:
                bad=deepcopy(old);bad[field]=value
                with self.subTest(tag=tag,field=field),self.assertRaises(ValueError):require_priority_option_successor(bad,xml)
            original=ET.fromstring(xml)
            for index,node in enumerate(original):
                bad=deepcopy(original)
                if node.tag=='string':bad[index].text=(node.text or '')+' altered'
                else:bad[index][0].text=(node[0].text or '')+' altered'
                with self.subTest(tag=tag,key=node.get('name')),self.assertRaises(ValueError):require_priority_option_successor(old,ET.tostring(bad,encoding='unicode'))
            for mode in ('missing','extra','attribute'):
                bad=deepcopy(original)
                if mode=='missing':bad.remove(bad[0])
                elif mode=='extra':ET.SubElement(bad,'string',name='unreviewed').text='unreviewed'
                else:bad[0].set('formatted','false')
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_priority_option_successor(old,ET.tostring(bad,encoding='unicode'))

    def test_only_exact_full_priority_values_supersede_two_remaining_original_empty_options(self):
        from copy import deepcopy
        rows=json.loads(ADDITIONS_PATH.read_text())['languages']
        for tag in sorted(YO_ZU_OPTION_TAGS):
            old=next(r for r in rows if r['tag']==tag);xml=(ROOT/old['catalogue']).read_text()
            require_yo_zu_option_successor(old,xml)
            with self.assertRaises(ValueError):require_untranslated_option(old,xml)
            for row in rows:
                if row['tag']!=tag:
                    with self.subTest(tag=tag,foreign=row['tag']),self.assertRaises(ValueError):require_yo_zu_option_successor(row,xml)
            for field,value in [('translation_status','complete'),('linguistic_review','accepted'),('fallback','translated'),('source_strings_present',346)]:
                bad=deepcopy(old);bad[field]=value
                with self.subTest(tag=tag,field=field),self.assertRaises(ValueError):require_yo_zu_option_successor(bad,xml)
            original=ET.fromstring(xml)
            for index,node in enumerate(original):
                bad=deepcopy(original)
                if node.tag=='string':bad[index].text=(node.text or '')+' altered'
                else:bad[index][0].text=(node[0].text or '')+' altered'
                with self.subTest(tag=tag,key=node.get('name')),self.assertRaises(ValueError):require_yo_zu_option_successor(old,ET.tostring(bad,encoding='unicode'))
            for mode in ('missing','extra','attribute'):
                bad=deepcopy(original)
                if mode=='missing':bad.remove(bad[0])
                elif mode=='extra':ET.SubElement(bad,'string',name='unreviewed').text='unreviewed'
                else:bad[0].set('formatted','false')
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_yo_zu_option_successor(old,ET.tostring(bad,encoding='unicode'))

if __name__ == '__main__':
    unittest.main()
