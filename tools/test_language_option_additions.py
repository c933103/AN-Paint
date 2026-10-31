"""Current option identities and historical coverage records; not linguistic acceptance."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as catalogues
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
            self.assertEqual('default-English', entries[0]['fallback'])
            self.assertEqual(catalogues.RES / f'values-b+{tag}/strings.xml', catalogues.catalogue_paths()[tag])

    def test_current_catalogues_are_valid_without_historical_partial_status_freezes(self):
        for row in json.loads(ADDITIONS_PATH.read_text())['languages']:
            with self.subTest(tag=row['tag']):
                self.assertEqual([], catalogues.validate_catalogue(row['tag']))
                self.assertEqual('default-English', row['fallback'])
        defaults = catalogues.default_resources()[0]
        self.assertIn('New or untranslated text appears in English.', defaults['language20_translation_note'])
        # Missing-key counts and historical review status are reporting data, not
        # requirements to keep these options incomplete or reject new translations.


if __name__ == '__main__':
    unittest.main()
