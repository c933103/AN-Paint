"""Import-change localization/data-boundary contracts, not linguistic acceptance."""
import json
import pathlib
import unittest

import translation_catalogues as catalogues

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
KEYS = {
    'commons_import_svg_changes':
        'AN Paint: SVG → PNG; original size; antiAlias=false; strokeDashArray=none; background=#FFFFFF.',
    'commons_import_raster_changes':
        'AN Paint: background=#FFFFFF (alpha compositing).',
}


class CommonsImportChangeTranslationsTest(unittest.TestCase):
    def test_default_is_exact_existing_english_with_no_arguments(self):
        source = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        self.assertEqual(KEYS, {key: source[key] for key in KEYS})
        for value in KEYS.values():
            self.assertEqual({}, catalogues.placeholders(value))


    def test_all_published_notes_preserve_literals_and_formatting(self):
        paths = {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}
        for tag, path in paths.items():
            messages = catalogues.read_strings(path)
            for key in set(KEYS) & set(messages):
                value = messages[key]
                with self.subTest(tag=tag, key=key):
                    self.assertEqual(1, value.count('AN Paint'))
                    self.assertEqual(1, value.count('background=#FFFFFF'))
                    self.assertEqual({}, catalogues.placeholders(value))
                    self.assertEqual([], catalogues.android_string_errors(value))
                    self.assertEqual([], catalogues.format_string_errors(value))
                    self.assertNotIn('\n', value)
                    for literal in ('SVG → PNG', 'antiAlias=false', 'strokeDashArray=none'):
                        self.assertEqual(1 if key == 'commons_import_svg_changes' else 0,
                                         value.count(literal), literal)

    def test_only_imported_boundary_uses_the_two_whole_resources(self):
        source = (JAVA / 'CommonsAttribution.kt').read_text()
        self.assertIn('fun text(imported: Boolean): String', source)
        self.assertIn('if (imported) lines.add(if (Uri.parse(source).path.orEmpty().endsWith(".svg", true))', source)
        self.assertIn('ui(R.string.commons_import_svg_changes)', source)
        self.assertIn('else ui(R.string.commons_import_raster_changes))', source)
        for value in KEYS.values():
            self.assertNotIn(value, source)
        self.assertNotIn('ui_original_size34', source)
        # Whole provider values still cross this boundary verbatim, not as resources.
        self.assertIn('lines.add("$key: $it")', source)
        self.assertIn('metadata[key]?.takeIf { it.isNotBlank() }', source)
        self.assertIn('CommonsAttribution.cached(this,source)?.text(imported=true)',
                      (JAVA / 'ClassicPaintActivity.kt').read_text())
        self.assertIn('val credit=document.imageCredits.firstOrNull {it.source==source} ?: ImageCredit(',
                      (JAVA / 'ClassicPaintActivity.kt').read_text())
        gallery = (JAVA / 'MediaGalleryActivity.kt').read_text()
        self.assertIn('record.text(imported=false)', gallery)
        self.assertNotIn('text(imported=true)', gallery)


if __name__ == '__main__':
    unittest.main()
