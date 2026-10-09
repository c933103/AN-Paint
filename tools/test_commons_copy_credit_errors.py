"""Bounded Copy credit wording/resource contracts; not runtime or linguistic proof."""
import hashlib
import json
import pathlib
import re
import unittest

import translation_catalogues as catalogues
from test_translations import SCOPED_TAGS

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
EVIDENCE = ROOT / 'verification/commons-copy-credit-errors-2026-10-09'
KEYS = {
    'commons_credit_copy_failed': 'Could not copy image credit.',
    'commons_credit_copy_failed_reason': 'Could not copy image credit: %1$s',
    'commons_credit_copy_out_of_memory': 'Not enough memory to copy image credit.',
}


class CommonsCopyCreditErrorContracts(unittest.TestCase):
    def test_default_and_exact_59_catalogues_match_review_manifest(self):
        data = json.loads((EVIDENCE / 'translations.json').read_text())
        self.assertEqual(KEYS, data['source_messages'])
        self.assertEqual(set(SCOPED_TAGS), set(data['scope']))
        self.assertEqual(set(SCOPED_TAGS), set(data['translations']))
        default = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        self.assertEqual(KEYS, {key: default[key] for key in KEYS})
        paths = catalogues.catalogue_paths()
        for tag, expected in data['translations'].items():
            with self.subTest(tag=tag):
                self.assertEqual(set(KEYS), set(expected))
                actual = catalogues.read_strings(paths[tag])
                self.assertEqual(expected, {key: actual[key] for key in KEYS})
                for key, value in expected.items():
                    self.assertEqual(catalogues.placeholders(KEYS[key]), catalogues.placeholders(value))
                    self.assertEqual([], catalogues.android_string_errors(value))
                    self.assertEqual([], catalogues.format_string_errors(value))
                    if not tag.startswith('en-') and tag != 'qaa-Zsye-XV':
                        self.assertNotEqual(KEYS[key], value)

    def test_other_81_tags_have_explicit_unmodified_fallback_disposition(self):
        data = json.loads((EVIDENCE / 'translations.json').read_text())
        remaining = set(catalogues.offered_tags()) - SCOPED_TAGS
        self.assertEqual(81, len(remaining))
        self.assertEqual(remaining, set(data['remaining_other_offered_locales']))
        for tag, path in catalogues.catalogue_paths().items():
            if tag not in SCOPED_TAGS:
                self.assertFalse(set(KEYS) & set(catalogues.read_strings(path)), tag)

    def test_resource_edit_is_exactly_three_additions_without_changing_existing_strings(self):
        scope = json.loads((EVIDENCE / 'source-scope.json').read_text())
        self.assertEqual(60, len(scope['catalogues']))
        for row in scope['catalogues']:
            text = (ROOT / row['path']).read_text()
            for key in KEYS:
                text, count = re.subn(r'    <string name="' + key + r'">[^\n]*</string>\n', '', text)
                self.assertEqual(1, count)
            self.assertEqual(row['before_sha256'], hashlib.sha256(text.encode()).hexdigest())

    def test_catch_change_is_confined_to_metadata_copy_and_keeps_detail_verbatim(self):
        text = (JAVA / 'MediaGalleryActivity.kt').read_text()
        copy = text.split('    private fun copyCommonsCredit(', 1)[1].split('    private fun showStatus(', 1)[0]
        self.assertIn('val reason=error.message?.takeIf {it.isNotBlank()}', copy)
        self.assertIn('ui(R.string.commons_credit_copy_failed_reason,reason)', copy)
        self.assertIn('record.text(imported=false)', copy)
        for old in ('ui_could_not_load_gallery_image', 'ui_not_enough_memory_to_inspect_the_gallery_image', 'colour_converter_unavailable'):
            self.assertNotIn('R.string.' + old, copy)
        self.assertNotIn('.trim()', copy)
        self.assertNotIn('error.javaClass', copy)
        self.assertNotIn('error.toString()', copy)
        before, after = text.split('    private fun copyCommonsCredit(', 1)
        after = after.split('    private fun showStatus(', 1)[1]
        for key in KEYS:
            self.assertNotIn('R.string.' + key, before + after)
        scope = json.loads((EVIDENCE / 'source-scope.json').read_text())
        for row in scope['unchanged_semantics_files']:
            self.assertEqual(row['sha256'], hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest())

    def test_android_tests_use_all_140_tags_and_actual_webview_route(self):
        tests = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local'
        resource = (tests / 'CommonsCopyCreditTranslationTest.kt').read_text()
        tags = re.search(r'private val scopedTags=setOf\((.*?)\n    \)', resource, re.S).group(1)
        self.assertEqual(SCOPED_TAGS, set(re.findall(r'"([\w-]+)"', tags)))
        data = json.loads((EVIDENCE / 'translations.json').read_text())
        for tag, values in data['translations'].items():
            def kotlin(value):
                return json.dumps(value, ensure_ascii=False).replace('$', '\\$')
            expected = (kotlin(tag) + ' to listOf(' + ', '.join(kotlin(values[key]) for key in KEYS) + ')')
            self.assertIn(expected, resource, tag)
        fallback = re.search(r'private val fallbackTags=setOf\((.*?)\n    \)', resource, re.S).group(1)
        self.assertEqual(set(data['remaining_other_offered_locales']), set(re.findall(r'"([\w-]+)"', fallback)))
        self.assertIn('expectedMessages.getValue(tag),keys.map {resources.getString(it)}', resource)
        self.assertIn('defaultMessages,keys.map {resourcesFor(tag).getString(it)}', resource)
        routes = (tests / 'CommonsCopyCreditErrorTest.kt').read_text()
        self.assertIn('GalleryPage.CREDIT_SCHEME', routes)
        self.assertIn('webViewClient.shouldOverrideUrlLoading(web,action.toString())', routes)
        self.assertNotIn('callInstanceMethod', routes)
        self.assertIn('activeController.pause().stop().destroy()', routes)
        self.assertIn('GalleryCredits.publishClipboard={_,_->throw', routes)
        self.assertIn('View.LAYOUT_DIRECTION_RTL', routes)
        self.assertIn('ColumnScrollView', routes)


if __name__ == '__main__':
    unittest.main()
