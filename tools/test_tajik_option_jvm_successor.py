"""Finite Tajik option expectations and reviewed partial/fallback resources."""
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as E
from kazakh_tajik_pashto_priority_expectations import bound_fixture, require_edited_resource
from language_option_additions import SECOND_ADDITIONS_PATH
import translation_catalogues as catalogues

ROOT=Path(__file__).resolve().parents[1]
KEYS=('ui_menu_file','ui_brush','ui_save','language20_translation_note')

class TajikOptionJvmSuccessorTest(unittest.TestCase):
    def section(self):
        text=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/AppLanguageTest.kt').read_text()
        start=text.index('fun furtherOptionsIncludingPrincipalVarietiesKeepTheirExactIdentityAndFallback()')
        return text[start:text.index('\n    @Test',start)]

    def test_tajik_branch_uses_exact_four_complete_reviewed_displays(self):
        data=bound_fixture('tg');catalogue=E.parse(ROOT/data['catalogue_path'])
        section=self.section();branch=re.split(r'} else(?: if \(tag == "[^"]+"\))? \{',section.split('} else if (tag == "tg") {')[1])[0]
        self.assertEqual(4,branch.count('assertEquals('))
        for key in KEYS:
            require_edited_resource('tg',key,catalogue.find("./string[@name='"+key+"']"))
            expected='assertEquals('+json.dumps(data['values'][key]['display'],ensure_ascii=False)+',wrapped.getString(R.string.'+key+'))'
            self.assertIn(expected,branch)

    def test_exact_combined_successors_preserve_partial_and_remaining_fallbacks(self):
        rows=json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']
        tags={r['tag'] for r in rows}
        successors={'as','so','wo','ht','tg','mi','sm','sa','pcm','tpi'}
        partial={'qug','quh','quz'}
        fallbacks={'ch','chr','nv','yua','nch','nhe','nhw','quy'}
        self.assertEqual(21,len(rows));self.assertEqual(21,len(tags))
        self.assertEqual(tags,successors|partial|fallbacks)
        reviewed=json.loads((ROOT/'tools/fixtures/current_localization/reviewed_priority_batches.json').read_text())
        defaults=catalogues.default_resources()[0]
        paths=catalogues.catalogue_paths()
        for tag in partial|fallbacks:
            values=catalogues.read_strings(paths[tag])
            for key in KEYS:
                if tag in partial and key=='ui_save':
                    row=reviewed['locales'][tag]['accepted'][key]
                    node=E.parse(paths[tag]).find("./string[@name='ui_save']")
                    self.assertIsNotNone(node,tag)
                    self.assertEqual(row['attributes'],dict(node.attrib),tag)
                    self.assertEqual(row['value'],node.text,tag)
                else:
                    self.assertNotIn(key,values,tag+'/'+key)
                    self.assertEqual(defaults[key],values.get(key,defaults[key]),tag+'/'+key)
        self.assertEqual(8,len(fallbacks))

    def test_identity_and_platform_round_trip_assertions_remain(self):
        section=self.section()
        for assertion in ('assertEquals(tag,AppLanguage.selectedTag(wrapped))',
                'assertEquals(tag,wrapped.resources.configuration.locales[0].toLanguageTag())',
                'assertEquals(tag,Locale.getDefault().toLanguageTag())',
                'assertEquals("$name [$tag]",AppLanguage.name(tag))',
                'assertEquals(tag,manager.applicationLocales[0].toLanguageTag())',
                'assertEquals("en-001",AppLanguage.selectedTag(context))',
                'assertEquals(tag,AppLanguage.selectedTag(context))'):
            self.assertIn(assertion,section)

if __name__=='__main__':unittest.main()
