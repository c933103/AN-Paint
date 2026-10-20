"""Exact-position catalogue regression checks, not linguistic certification."""
import json
import pathlib
import unittest

import translation_catalogues as catalogues
from test_translations import SCOPED_TAGS

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tools/fixtures/current_localization/assembly_position_current_wording.json'
KEYS = {
    'ui_assembly_exact_position', 'ui_assembly_target_x', 'ui_assembly_target_y',
    'ui_assembly_position_help', 'ui_assembly_position_nonnegative', 'ui_assembly_unknown_image',
}


class AssemblyPositionTranslationsTest(unittest.TestCase):
    def test_source_keys_and_unchanged_message_shape(self):
        manifest = json.loads(MANIFEST.read_text())
        source = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        self.assertEqual(KEYS, set(manifest['source_messages']))
        self.assertEqual(manifest['source_messages'], {key: source[key] for key in KEYS})
        for value in manifest['source_messages'].values():
            self.assertEqual({}, catalogues.placeholders(value))
            self.assertNotIn('\\n', value)

    def test_reviewed_values_are_complete_and_exact(self):
        manifest = json.loads(MANIFEST.read_text())
        paths = catalogues.catalogue_paths()
        translated = set(manifest['translations'])
        self.assertEqual(['sv'], manifest['additional_reviewed_tags'])
        self.assertLessEqual(translated, SCOPED_TAGS | {'sv'})
        for tag, expected in manifest['translations'].items():
            with self.subTest(tag=tag):
                self.assertEqual(KEYS, set(expected))
                actual = catalogues.read_strings(paths[tag])
                self.assertEqual(expected, {key: actual[key] for key in KEYS})
                for value in expected.values():
                    self.assertTrue(value.strip())
                    self.assertEqual({}, catalogues.placeholders(value))
                    self.assertEqual([], catalogues.android_string_errors(value))
                    self.assertEqual([], catalogues.format_string_errors(value))
                    self.assertNotIn('\\n', value)
        # Keep genuinely unreviewed locales on actual resource fallback; no
        # English-filled overrides to disguise the separate completeness gate.
        for tag, path in paths.items():
            if tag not in translated:
                with self.subTest(fallback=tag):
                    self.assertFalse(KEYS & set(catalogues.read_strings(path)))

    def test_position_controls_have_explicit_operational_priority(self):
        manifest = json.loads((ROOT / 'translations/string-importance.json').read_text())
        priorities = {key: tier['id'] for tier in manifest['tiers'] for key in tier['keys']}
        for key in KEYS:
            self.assertEqual('P2', priorities['string/' + key])


if __name__ == '__main__':
    unittest.main()
