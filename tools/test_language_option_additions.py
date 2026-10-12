"""Current option identities and truthful zero-coverage status; not linguistic acceptance."""
import hashlib
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
        self.assertEqual(EXPECTED, {r['tag']: r['name'] for r in data['languages']})
        tags = catalogues.offered_tags()
        self.assertEqual(167, len(tags)); self.assertEqual(167, len(set(tags)))
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
            self.assertEqual('not-started', entries[0]['translation_status'])
            self.assertEqual('default-English', entries[0]['fallback'])
            self.assertEqual(catalogues.RES / f'values-b+{tag}/strings.xml', catalogues.catalogue_paths()[tag])

    def test_new_catalogues_honestly_declare_untranslated_default_fallback(self):
        data = json.loads(ADDITIONS_PATH.read_text())
        defaults, plurals, source_strings, source_plurals = catalogues.default_resources()
        self.assertEqual(695, len(source_strings)); self.assertEqual(1, len(source_plurals))
        for row in data['languages']:
            self.assertEqual('not-started', row['translation_status'])
            self.assertEqual('not-started', row['linguistic_review'])
            self.assertEqual('default-English', row['fallback'])
            path = ROOT / row['catalogue']
            self.assertEqual([], list(ET.parse(path).getroot()), row['tag'])
            self.assertEqual({}, catalogues.read_strings(path))
            self.assertEqual({}, catalogues.read_plurals(path))
            self.assertEqual([], catalogues.validate_catalogue(row['tag']))
            self.assertTrue(catalogues.validate_catalogue(row['tag'], require_complete=True))
        self.assertIn('New or untranslated text appears in English.', defaults['language20_translation_note'])

    def test_historical_disposition_evidence_remains_byte_identical(self):
        expected = json.loads((ROOT / 'tools/fixtures/language_option_historical_evidence.json').read_text())
        for path, digest in expected.items():
            self.assertEqual(digest, hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), path)


if __name__ == '__main__':
    unittest.main()
