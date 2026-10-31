"""Bounded source/fixture contracts; hosted Android tests establish resolution."""
import json
import pathlib
import re
import unittest

import translation_catalogues as catalogues
from current_localization_contracts import fixture, CURRENT_CATALOGUE_TAGS
import copy
from unittest.mock import patch
import exact_script_priority_expectations as exact_script

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt'
FIXTURE = ROOT / 'Paintroid/src/test/resources/exact-script-resources/expected.json'


class ExactScriptResourceRoutingContracts(unittest.TestCase):
    def test_only_two_internal_variants_and_public_tag_catalogues_are_unchanged(self):
        source = JAVA.read_text()
        method = source.split('internal fun resourceLocale(', 1)[1].split('    fun wrap(', 1)[0]
        self.assertIn('chosen.toLanguageTag()=="ko-Kore-KR"', method)
        self.assertIn('setLocale(chosen).setVariant("anpaint")', method)
        self.assertIn('chosen.toLanguageTag()=="qaa-Zsye-XV"', method)
        self.assertIn('Locale.forLanguageTag("en-Zsye-XV-anpaint")', method)
        self.assertIn('else chosen', method)
        self.assertNotIn('R.string', method)
        self.assertNotIn('複寫', source)
        self.assertIn('ko-Kore-KR', catalogues.offered_tags())
        self.assertIn('qaa-Zsye-XV', catalogues.offered_tags())
        self.assertFalse(any('anpaint' in tag for tag in catalogues.offered_tags()))
        self.assertFalse((catalogues.RES / 'values-b+ko+Kore+KR+anpaint').exists())
        self.assertFalse((catalogues.RES / 'values-b+en+Zsye+XV+anpaint').exists())

    def test_build_mirrors_all_xml_from_canonical_catalogue_before_prebuild(self):
        build = (ROOT / 'Paintroid/build.gradle').read_text()
        task = build.split("tasks.register('generateExactScriptResources', Sync)", 1)[1]
        task = task.split('// AAPT decodes canonical English', 1)[0]
        self.assertIn("from('src/main/res/values-b+ko+Kore+KR')", task)
        self.assertIn("include '*.xml'", task)
        self.assertIn("into 'values-b+ko+Kore+KR+anpaint'", task)
        self.assertIn("from('src/main/res/values-b+qaa+Zsye+XV')", task)
        self.assertIn("into 'values-b+en+Zsye+XV+anpaint'", task)
        self.assertEqual(2, task.count("include '*.xml'"))
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
            if row['requested_tag']=='tt-Latn':row=exact_script.reviewed_tatar_latin_script_row(row)
            tag = row['requested_tag']
            strings = catalogues.read_strings(catalogues.catalogue_paths()[tag])
            expected = {'ko-Kore-KR': 'ko-Kore-KR-anpaint',
                        'qaa-Zsye-XV': 'en-Zsye-XV-anpaint'}.get(tag, tag)
            self.assertEqual(expected, row['resource_tag'])
            if tag in CURRENT_CATALOGUE_TAGS:
                continue  # Public route remains checked; copied approval text is retired.
            self.assertEqual({key: strings.get(key, defaults[key]).strip('"')
                              for key in ('ui_save', 'ui_menu_file', 'language20_device_default')},
                             row['expected'])

    def test_tatar_latin_successor_rejects_changed_history_and_coordinated_fixture(self):
        original={'requested_tag':'tt-Latn','resource_tag':'tt-Latn','expected':{
            'ui_save':'Saqlaw','ui_menu_file':'Fayl','language20_device_default':'Use device language'}}
        snapshot=copy.deepcopy(original)
        self.assertEqual('Caylanma telen qullanu',exact_script.reviewed_tatar_latin_script_row(original)['expected']['language20_device_default'])
        self.assertEqual(snapshot,original)
        invalid=[]
        for key in ('requested_tag','resource_tag','expected'):
            row=copy.deepcopy(original);del row[key];invalid.append(row)
        for key in ('requested_tag','resource_tag'):
            row=copy.deepcopy(original);row[key]='tt-Cyrl';invalid.append(row)
        row=copy.deepcopy(original);row['extra']=True;invalid.append(row)
        for key in original['expected']:
            row=copy.deepcopy(original);del row['expected'][key];invalid.append(row)
            row=copy.deepcopy(original);row['expected'][key]='forged';invalid.append(row)
        row=copy.deepcopy(original);row['expected']['extra']=True;invalid.append(row)
        row=copy.deepcopy(original);row['expected']['language20_device_default']='Caylanma telen qullanu';invalid.append(row)
        self.assertEqual(14,len(invalid))
        for row in invalid:
            with self.subTest(row=row),self.assertRaises(ValueError):exact_script.reviewed_tatar_latin_script_row(row)
        for field in ('reviewed_value','compiled_display','source','previous_target','attributes'):
            data=exact_script.bound_fixture('tt-Latn');data['rows']['language20_device_default'][field]='forged'
            with patch.object(exact_script,'bound_fixture',return_value=data),self.assertRaises(ValueError):
                exact_script.reviewed_tatar_latin_script_row(original)
        self.assertEqual(snapshot,original)


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
