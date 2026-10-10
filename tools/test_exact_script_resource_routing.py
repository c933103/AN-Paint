"""Bounded source/fixture contracts; hosted Android tests establish resolution."""
import json
import pathlib
import re
import unittest

import translation_catalogues as catalogues

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt'
FIXTURE = ROOT / 'Paintroid/src/test/resources/exact-script-resources/expected.json'


class ExactScriptResourceRoutingContracts(unittest.TestCase):
    def test_only_one_internal_variant_and_public_tag_catalogue_are_unchanged(self):
        source = JAVA.read_text()
        method = source.split('internal fun resourceLocale(', 1)[1].split('    fun wrap(', 1)[0]
        self.assertIn('chosen.toLanguageTag()=="ko-Kore-KR"', method)
        self.assertIn('setLocale(chosen).setVariant("anpaint")', method)
        self.assertIn('else chosen', method)
        self.assertNotIn('R.string', method)
        self.assertNotIn('複寫', source)
        self.assertIn('ko-Kore-KR', catalogues.offered_tags())
        self.assertFalse(any('anpaint' in tag for tag in catalogues.offered_tags()))
        self.assertFalse((catalogues.RES / 'values-b+ko+Kore+KR+anpaint').exists())

    def test_build_mirrors_all_xml_from_canonical_catalogue_before_prebuild(self):
        build = (ROOT / 'Paintroid/build.gradle').read_text()
        task = build.split("tasks.register('generateExactScriptResources', Sync)", 1)[1]
        task = task.split('// Host-side Android graphics tests', 1)[0]
        self.assertIn("from('src/main/res/values-b+ko+Kore+KR')", task)
        self.assertIn("include '*.xml'", task)
        self.assertIn("into 'values-b+ko+Kore+KR+anpaint'", task)
        self.assertIn('into exactScriptResourceDirectory', task)
        self.assertIn('android.sourceSets.main.res.srcDir(exactScriptResourceDirectory)', task)
        self.assertIn("tasks.named('preBuild').configure { dependsOn(generateExactScriptResources) }", task)
        self.assertNotIn('filter', task)
        self.assertNotIn('replace', task)

    def test_all_explicit_script_choices_have_independent_general_ui_expectations(self):
        rows = json.loads(FIXTURE.read_text())
        explicit = {tag for tag in catalogues.offered_tags()
                    if any(re.fullmatch('[A-Z][a-z]{3}', subtag) for subtag in tag.split('-')[1:])}
        controls = {'ko-KR', 'ko-KP', 'vi', 'fr', 'ar', 'en-GB', 'ja'}
        self.assertEqual(21, len(explicit))
        self.assertEqual(explicit | controls, {row['requested_tag'] for row in rows})
        self.assertEqual(28, len(rows))
        defaults = catalogues.default_resources()[0]
        for row in rows:
            tag = row['requested_tag']
            strings = catalogues.read_strings(catalogues.catalogue_paths()[tag])
            self.assertEqual(tag + '-anpaint' if tag == 'ko-Kore-KR' else tag,
                             row['resource_tag'])
            self.assertEqual({key: strings.get(key, defaults[key]).strip('"')
                              for key in ('ui_save', 'ui_menu_file', 'language20_device_default')},
                             row['expected'])

    def test_wrap_refresh_and_device_label_apply_the_same_bounded_resource_mapping(self):
        source = JAVA.read_text()
        for method, end in [('fun wrap(', '/** Updating'), ('fun refresh(', '    fun select('),
                            ('fun deviceDefaultLabel(', '    fun showSettings(')]:
            body = source.split(method, 1)[1].split(end, 1)[0]
            self.assertIn('val resource = resourceLocale(chosen)', body)
            self.assertIn('setLocales(LocaleList(resource))', body)
            self.assertIn('setLocale(resource)', body)
            self.assertIn('setLayoutDirection(chosen)', body)
        self.assertEqual(2, source.count('Locale.setDefault(chosen)'))

    def test_current_scriptless_competitors_remain_bounded_and_visible(self):
        paths = catalogues.catalogue_paths()
        pairs = set()
        for tag in paths:
            pieces = tag.split('-')
            scripts = [piece for piece in pieces[1:] if re.fullmatch('[A-Z][a-z]{3}', piece)]
            if scripts:
                without = '-'.join(piece for piece in pieces if piece != scripts[0])
                if without in paths:
                    pairs.add((tag, without))
        self.assertEqual({('ko-Kore-KR', 'ko-KR'), ('vi-Hani', 'vi')}, pairs)


if __name__ == '__main__':
    unittest.main()
