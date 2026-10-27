"""Keep the finite Tajik JVM option expectation aligned with reviewed full displays."""
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as E
from kazakh_tajik_pashto_priority_expectations import bound_fixture, require_edited_resource

ROOT=Path(__file__).resolve().parents[1]
KEYS=('ui_menu_file','ui_brush','ui_save','language20_translation_note')

class TajikOptionJvmSuccessorTest(unittest.TestCase):
    def section(self):
        text=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/AppLanguageTest.kt').read_text()
        start=text.index('fun furtherOptionsIncludingPrincipalVarietiesKeepTheirExactIdentityAndFallback()')
        return text[start:text.index('\n    @Test',start)]

    def test_tajik_branch_uses_exact_four_complete_reviewed_displays(self):
        data=bound_fixture('tg');catalogue=E.parse(ROOT/data['catalogue_path'])
        section=self.section();branch=section.split('} else if (tag == "tg") {')[1].split('} else {')[0]
        self.assertEqual(4,branch.count('assertEquals('))
        for key in KEYS:
            require_edited_resource('tg',key,catalogue.find("./string[@name='"+key+"']"))
            expected='assertEquals('+json.dumps(data['values'][key]['display'],ensure_ascii=False)+',wrapped.getString(R.string.'+key+'))'
            self.assertIn(expected,branch)

    def test_only_assamese_and_tajik_have_finite_successor_branches(self):
        section=self.section()
        self.assertEqual(['as','tg'],re.findall(r'(?:if|else if) \(tag == "([^"]+)"\)',section))
        expected=section.split('val expectedNames=mapOf(')[1].split('assertEquals(171,')[0]
        tags=re.findall(r'"([a-z]+)" to ',expected)
        self.assertEqual(21,len(tags));self.assertEqual(19,len(set(tags)-{'as','tg'}))
        branch=section.split('} else {')[1].split('if(android.os.Build')[0]
        for key,value in zip(KEYS[:3],('File','Brush','Save')):
            self.assertIn(f'assertEquals("{value}",wrapped.getString(R.string.{key}))',branch)
        self.assertIn('.contains("New or untranslated text appears in English.")',branch)

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
