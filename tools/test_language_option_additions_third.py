"""October registration and preserved Filipino resources, not linguistic acceptance."""
import json
from copy import deepcopy
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as c
from language_option_additions import require_untranslated_option
from current_localization_contracts import fixture
from moroccan_arabic_mongolian_toki_pona_priority_expectations import NAME, TAGS
from test_moroccan_arabic_mongolian_toki_pona_priority_wording import require_current

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tools/fixtures/language_option_additions_20261014.json"
EXPECTED = {"ang":"Ænglisc","ary":"الدارجة المغربية","non":"Norrœna","zgh":"ⵜⴰⵎⴰⵣⵉⵖⵜ / Tamaziɣt (Morocco)"}


def require_reviewed_ary_option(row, xml):
    original=next(r for r in json.loads(FIXTURE.read_text())['languages'] if r['tag']=='ary')
    if row!=original:raise ValueError('Exact historical ARY registration differs')
    # Registration history is still the original empty-catalogue contract.
    require_untranslated_option(row,'<resources/>')
    roots={tag:ET.parse(c.catalogue_paths()[tag]).getroot() for tag in TAGS}
    roots['ary']=ET.fromstring(xml)
    # Immutable complete reviewed fixture, partitions, attrs and all current values.
    require_current(fixture(NAME),roots,ET.parse(c.RES/'values/strings.xml').getroot())
    return roots['ary']


class OctoberLanguageOptionTests(unittest.TestCase):
    def test_picker_platform_names_metadata_and_scope_agree(self):
        data=json.loads(FIXTURE.read_text())
        tags=c.offered_tags()
        self.assertEqual(171,len(tags))
        self.assertEqual(len(tags),len(set(tags)))
        self.assertEqual("en-001",tags[0])
        self.assertEqual(sorted(tags[1:],key=str.casefold),tags[1:])
        self.assertNotIn("tl",tags)
        platform=[r.get('{http://schemas.android.com/apk/res/android}name')
                  for r in ET.parse(c.RES/'xml/app_locales.xml').getroot()]
        self.assertEqual(tags,platform)
        names=[r.text for r in ET.parse(c.RES/'values/app_language_names.xml')
               .findall(".//string-array[@name='app_language_names']/item")]
        picker=dict(zip(tags,names))
        self.assertEqual("Filipino",picker["fil"])
        meta=json.loads((ROOT/'translations/language-options.json').read_text())
        self.assertEqual("fil",meta['aliases']['tl'])
        self.assertEqual("Filipino",next(r['name'] for r in meta['options'] if r['tag']=="fil"))
        self.assertEqual(EXPECTED,{r['tag']:r['name'] for r in data['languages']})
        for tag,name in EXPECTED.items():
            self.assertEqual(name,picker[tag])
            self.assertEqual(name,next(r['name'] for r in meta['options'] if r['tag']==tag))
            self.assertEqual(c.RES/f'values-b+{tag}/strings.xml',c.catalogue_paths()[tag])
        scope=json.loads((ROOT/'tools/fixtures/current_localization/locale_contract_scope.json').read_text())
        self.assertEqual(59,len(scope['scoped_tags']))
        self.assertEqual(112,len(scope['fallback_tags']))
        self.assertEqual(set(EXPECTED),set(EXPECTED)&set(scope['fallback_tags']))
        self.assertIn("fil",scope['scoped_tags'])
        self.assertNotIn("tl",scope['scoped_tags'])

    def test_exact_reviewed_ary_successor_preserves_other_empty_fallbacks(self):
        for row in json.loads(FIXTURE.read_text())['languages']:
            path=ROOT/row['catalogue']
            if row['tag']=='ary':
                require_reviewed_ary_option(row,path.read_text())
                # 348 historical reviewed entries plus eleven exact accepted additions.
                self.assertEqual(359,len(ET.parse(path).getroot()))
                self.assertEqual([],c.validate_catalogue('ary'))
                continue
            if row['tag'] in ('ang','non'):
                require_untranslated_option(row,'<resources/>')
                from remaining_accepted_wording import require_historical_catalogue
                require_historical_catalogue(row['tag'],ET.parse(path).getroot())
                self.assertEqual([],c.validate_catalogue(row['tag']))
                continue
            require_untranslated_option(row,path.read_text())
            self.assertEqual([],list(ET.parse(path).getroot()))
            self.assertEqual({},c.read_strings(path))
            self.assertEqual({},c.read_plurals(path))
            self.assertEqual([],c.validate_catalogue(row['tag']))

    def test_reviewed_ary_successor_rejects_registration_and_complete_catalogue_mutants(self):
        row=next(r for r in json.loads(FIXTURE.read_text())['languages']if r['tag']=='ary')
        xml=c.catalogue_paths()['ary'].read_text()
        for field,value in [('tag','ang'),('source_strings_present',348),('translation_status','complete'),('catalogue','forged')]:
            bad=deepcopy(row);bad[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):require_reviewed_ary_option(bad,xml)
        for key in ('ui_menu_file','ui_brush','ui_save','language20_translation_note'):
            for mutation in ('complete-value','missing','attribute'):
                root=ET.fromstring(xml);node=root.find("./string[@name='"+key+"']")
                if mutation=='complete-value':node.text='forged nonempty value'
                elif mutation=='missing':root.remove(node)
                else:node.set('formatted','false')
                with self.subTest(key=key,mutation=mutation),self.assertRaises(ValueError):require_reviewed_ary_option(row,ET.tostring(root,encoding='unicode'))
        with self.assertRaises(ValueError):require_reviewed_ary_option(row,'<resources/>')
        root=ET.fromstring(xml);ET.SubElement(root,'string',name='ui_fg').text='forged held value'
        with self.assertRaises(ValueError):require_reviewed_ary_option(row,ET.tostring(root,encoding='unicode'))

    def test_fil_retains_existing_coverage_but_no_new_linguistic_review(self):
        self.assertFalse((c.RES/'values-tl/strings.xml').exists())
        self.assertNotIn('tl',c.catalogue_paths())
        path=c.catalogue_paths()['fil']
        self.assertEqual('Pambura',c.read_strings(path)['ui_eraser'])
        self.assertEqual('I-save',c.read_strings(path)['ui_save'])
        self.assertEqual([],c.validate_catalogue('fil',require_complete=True))


if __name__ == '__main__':
    unittest.main()
