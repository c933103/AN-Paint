"""October registration and preserved Filipino resources, not linguistic acceptance."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as c

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tools/fixtures/language_option_additions_20261014.json"
EXPECTED = {"ang":"Ænglisc","ary":"الدارجة المغربية","non":"Norrœna","zgh":"ⵜⴰⵎⴰⵣⵉⵖⵜ / Tamaziɣt (Morocco)"}




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

    def test_current_catalogues_are_valid_without_historical_empty_or_approval_freezes(self):
        for row in json.loads(FIXTURE.read_text())['languages']:
            with self.subTest(tag=row['tag']):
                self.assertEqual([], c.validate_catalogue(row['tag']))
                self.assertEqual('default-English', row['fallback'])
        # Registration history is not an instruction to keep a catalogue untranslated.


    def test_fil_retains_existing_coverage_but_no_new_linguistic_review(self):
        self.assertFalse((c.RES/'values-tl/strings.xml').exists())
        self.assertNotIn('tl',c.catalogue_paths())
        path=c.catalogue_paths()['fil']
        self.assertEqual('Pambura',c.read_strings(path)['ui_eraser'])
        self.assertEqual('I-save',c.read_strings(path)['ui_save'])


if __name__ == '__main__':
    unittest.main()
