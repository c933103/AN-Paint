"""Bounded SVG-error resource contracts; these are not linguistic acceptance."""
import json
import pathlib
import unittest

import translation_catalogues as catalogues
from test_translations import SCOPED_TAGS


ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
KEYS = {
    'commons_svg_original_size_unavailable':
        'The SVG does not declare a usable original size. No canvas-based size was substituted.',
    'commons_svg_original_size_too_large':
        'The original SVG size exceeds Android bitmap dimensions. No resizing was applied.',
}


class SvgErrorTranslationTests(unittest.TestCase):
    def test_canonical_source_preserves_both_failure_qualifiers(self):
        source = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        for key, expected in KEYS.items():
            with self.subTest(key=key):
                self.assertEqual(expected, source[key])
                self.assertEqual({}, catalogues.placeholders(source[key]))

    def test_every_present_scoped_message_preserves_the_unformatted_contract(self):
        paths = catalogues.catalogue_paths()
        for tag in sorted(SCOPED_TAGS):
            strings = catalogues.read_strings(paths[tag])
            for key in KEYS:
                with self.subTest(tag=tag, key=key):
                    if key not in strings:
                        continue  # The unchanged full scoped-completeness gate still rejects this.
                    text = strings[key]
                    self.assertTrue(text.strip())
                    self.assertEqual({}, catalogues.placeholders(text))
                    self.assertEqual([], catalogues.android_string_errors(text))
                    self.assertEqual([], catalogues.format_string_errors(text))
                    self.assertIn('SVG', text)
                    if key.endswith('too_large'):
                        self.assertIn('Android', text)

    def test_review_manifest_matches_only_the_two_published_resource_values(self):
        manifest = json.loads((ROOT / 'verification/svg-size-errors-2026-10-09/translations.json').read_text())
        complete = set(manifest['translations'])
        blocked = set(manifest['blocked_scoped_locales'])
        self.assertFalse(complete & blocked)
        self.assertEqual(set(SCOPED_TAGS), complete | blocked)
        paths = catalogues.catalogue_paths()
        for tag, values in manifest['translations'].items():
            with self.subTest(tag=tag):
                self.assertEqual(set(KEYS), set(values))
                actual = catalogues.read_strings(paths[tag])
                self.assertEqual(values, {key: actual[key] for key in KEYS})
        for tag in blocked:
            actual = catalogues.read_strings(paths[tag])
            with self.subTest(blocked_tag=tag):
                self.assertFalse(set(KEYS) & set(actual), 'Do not fill an unreviewed catalogue with English placeholders')

    def test_dimension_helper_keeps_typed_reasons_and_no_android_dependency(self):
        source = (JAVA / 'SvgOriginalSize.kt').read_text()
        self.assertIn('enum class Reason { UNUSABLE_ORIGINAL_SIZE, EXCEEDS_BITMAP_DIMENSIONS }', source)
        self.assertIn('class SizeException(val reason: Reason) : IllegalArgumentException()', source)
        self.assertIn('if (!value.isFinite() || value <= 0)', source)
        self.assertIn('val pixels = ceil(value)', source)
        self.assertIn('if (pixels > Int.MAX_VALUE.toDouble())', source)
        self.assertNotIn('import android', source)
        self.assertNotIn('R.string.', source)
        for message in KEYS.values():
            self.assertNotIn(message, source)

    def test_only_typed_svg_failures_are_translated_at_the_display_boundary(self):
        source = (JAVA / 'MediaGalleryActivity.kt').read_text()
        self.assertIn('SvgOriginalSize.Reason.UNUSABLE_ORIGINAL_SIZE -> R.string.commons_svg_original_size_unavailable', source)
        self.assertIn('SvgOriginalSize.Reason.EXCEEDS_BITMAP_DIMENSIONS -> R.string.commons_svg_original_size_too_large', source)
        self.assertIn('if(error is SvgOriginalSize.SizeException)', source)
        self.assertIn('}) else error.message', source)
        self.assertIn('failure(ui(R.string.ui_could_not_load_gallery_image,reason))', source)


if __name__ == '__main__':
    unittest.main()
