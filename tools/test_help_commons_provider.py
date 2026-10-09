"""Bounded AN-W05-C03 provider inventory and resource contracts, not fluency proof."""
import hashlib
import json
import pathlib
import re
import unittest

import translation_catalogues as catalogues
from test_translations import SCOPED_TAGS

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
MANIFEST = ROOT / 'verification/help-commons-provider-2026-10-09/translations.json'
KEY = 'ui_help23'


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


class HelpCommonsProviderTest(unittest.TestCase):
    def test_separate_one_key_manifest_has_exact_59_tag_scope(self):
        data = json.loads(MANIFEST.read_text())
        self.assertEqual(KEY, data['resource'])
        self.assertEqual(set(SCOPED_TAGS), set(data['scope']))
        self.assertEqual(set(SCOPED_TAGS) | {'default'}, set(data['translations']))
        remaining = set(catalogues.offered_tags()) - set(SCOPED_TAGS)
        self.assertEqual(81, len(remaining))
        self.assertEqual(remaining, set(data['remaining_other_offered_locales']))
        for tag, path in catalogues.catalogue_paths().items():
            if tag not in SCOPED_TAGS:
                self.assertNotIn(KEY, catalogues.read_strings(path), tag)

    def test_exact_caption_added_once_and_all_surrounding_help_preserved(self):
        data = json.loads(MANIFEST.read_text())
        for tag, row in data['translations'].items():
            with self.subTest(tag=tag):
                strings = catalogues.read_strings(ROOT / row['catalogue'])
                actual = strings[KEY]
                self.assertEqual(strings['commons_blank_maps'], row['caption'])
                self.assertEqual(1, actual.count(row['caption']))
                self.assertEqual(1, actual.count(row['after_segment']))
                self.assertEqual(row['after_help_sha256'], digest(actual))
                before = actual.replace(row['after_segment'], row['before_segment'], 1)
                self.assertEqual(row['before_help_sha256'], digest(before),
                                 'Only the documented provider-list passage may change')
                self.assertNotIn('Wikimedia Commons', before)
                self.assertIn(row['before_context'], before)
                self.assertIn(row['after_context'], actual)
                self.assertEqual(catalogues.placeholders(before), catalogues.placeholders(actual))
                self.assertEqual([], catalogues.android_string_errors(actual))
                self.assertEqual([], catalogues.format_string_errors(actual, False))
                for provider in ('Catrobat', 'Openclipart'):
                    self.assertEqual(before.count(provider), actual.count(provider))
                self.assertEqual(before.count('Irasutoya'), actual.count('Irasutoya'))
                self.assertEqual(before.count('いらすとや'), actual.count('いらすとや'))

    def test_default_lists_actual_device_and_four_provider_choices(self):
        strings = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        self.assertIn('Draw > Insert > Other images contains device files, Catrobat, '
                      'Irasutoya, Openclipart and “Wikimedia Commons · Blank maps…”.', strings[KEY])
        provider = (JAVA / 'IllustrationSource.kt').read_text()
        entries = re.findall(r'^    ([A-Z]+)\("https://', provider, re.M)
        self.assertEqual(['CATROBAT', 'IRASUTOYA', 'OPENCLIPART', 'COMMONS'], entries)
        self.assertIn('COMMONS->ui(R.string.commons_blank_maps)', provider)
        editor = (JAVA / 'ClassicPaintActivity.kt').read_text()
        self.assertIn('val sources=listOf(ui(R.string.ui_from_device34))+IllustrationSource.values().map {it.label}', editor)
        self.assertIn('private fun showHelp() = message(ui(R.string.ui_help23))', editor)
        self.assertIn('ui(R.string.ui_how_to_use) to {showHelp()}', editor)

    def test_source_assisted_punctuation_corrections(self):
        rows = json.loads(MANIFEST.read_text())['translations']
        self.assertTrue(rows['et']['after_segment'].endswith('„Wikimedia Commons · Kontuurkaardid…“'))
        self.assertTrue(rows['fi']['after_segment'].endswith('”Wikimedia Commons · Ääriviivakartat…” -valinnan'))
        self.assertTrue(rows['vi-Hani']['after_segment'].endswith('吧 「Wikimedia Commons · 版圖 𤿰…」'))

    def test_android_resource_test_uses_same_explicit_scope(self):
        source = (ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsHelpProviderTranslationTest.kt').read_text()
        tags = re.search(r'private val scopedTags=listOf\((.*?)\n    \)', source, re.S).group(1)
        self.assertEqual(set(SCOPED_TAGS), set(re.findall(r'"([\w-]+)"', tags)))
        self.assertIn('EditorTestNavigation.command(activity,"File",7)', source)
        self.assertIn('ShadowAlertDialog.getLatestAlertDialog()', source)


if __name__ == '__main__':
    unittest.main()
