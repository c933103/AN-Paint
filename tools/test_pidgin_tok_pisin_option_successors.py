"""Finite PCM/TPI option adoption and preserved legacy JVM routing assertions."""
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as E
from unittest.mock import patch
from language_option_additions import SECOND_ADDITIONS_PATH, require_untranslated_option
from pidgin_tok_pisin_option_successors import require_pidgin_option_successor
from sindhi_nigerian_pidgin_tok_pisin_priority_expectations import bound_fixture
ROOT=Path(__file__).resolve().parents[1]
TAGS=('pcm','tpi')

class PidginTokPisinOptionSuccessorsTest(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads(SECOND_ADDITIONS_PATH.read_text())['languages']
        self.old={r['tag']:r for r in self.rows}
    def xml(self,tag):return (ROOT/self.old[tag]['catalogue']).read_text()
    def test_exact_empty_history_gets_only_complete_reviewed_additions(self):
        for tag in TAGS:
            root=require_pidgin_option_successor(self.old[tag],self.xml(tag))
            self.assertEqual(345,len(root))
            with self.assertRaises(ValueError):require_untranslated_option(self.old[tag],self.xml(tag))
    def test_wrong_options_and_history_fields_are_rejected(self):
        for tag in TAGS:
            for row in self.rows:
                if row['tag']not in TAGS:
                    with self.subTest(tag=tag,row=row['tag']),self.assertRaises(ValueError):require_pidgin_option_successor(row,self.xml(tag))
            for field,value in [('tag',None),('translation_status','complete'),('fallback','translated'),('source_strings_present',345),('source_plurals_present',1),('catalogue','invented')]:
                row=deepcopy(self.old[tag]);row[field]=value
                with self.subTest(tag=tag,field=field),self.assertRaises(ValueError):require_pidgin_option_successor(row,self.xml(tag))
            with self.assertRaises(ValueError):require_pidgin_option_successor(self.old[tag],self.xml('tpi'if tag=='pcm'else'pcm'))
    def test_missing_extra_mutated_and_malformed_resources_are_rejected(self):
        for tag in TAGS:
            for mutation in ('missing','extra','duplicate','value','attribute','child','tail','root-text','root-tail','root-attr','plural-count','plural-value','plural-attr','plural-child','plural-tail'):
                root=E.fromstring(self.xml(tag));n=root[0];plural=root.find('./plurals')
                if mutation=='missing':root.remove(n)
                elif mutation=='extra':E.SubElement(root,'string',name='unreviewed').text='unreviewed'
                elif mutation=='duplicate':root.append(deepcopy(n))
                elif mutation=='value':n.text='unreviewed'
                elif mutation=='attribute':n.set('formatted','false')
                elif mutation=='child':E.SubElement(n,'b').text='unreviewed'
                elif mutation=='tail':n.tail='unreviewed'
                elif mutation=='root-text':root.text='unreviewed'
                elif mutation=='root-tail':root.tail='unreviewed'
                elif mutation=='root-attr':root.set('unreviewed','true')
                elif mutation=='plural-count':plural.append(deepcopy(plural[0]))
                elif mutation=='plural-value':plural[0].text='unreviewed'
                elif mutation=='plural-attr':plural[0].set('formatted','false')
                elif mutation=='plural-child':E.SubElement(plural[0],'b').text='unreviewed'
                else:plural[0].tail='unreviewed'
                with self.subTest(tag=tag,mutation=mutation),self.assertRaises(ValueError):require_pidgin_option_successor(self.old[tag],E.tostring(root,encoding='unicode'))
    def test_source_changes_are_not_accepted_as_reviewed_predecessors(self):
        import pidgin_tok_pisin_option_successors as helper
        for tag in TAGS:
            original=E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml');root=deepcopy(original.getroot());root.find("./string[@name='ui_save']").text='unreviewed'
            with patch.object(helper.E,'parse',return_value=E.ElementTree(root)),self.assertRaises(ValueError):require_pidgin_option_successor(self.old[tag],self.xml(tag))
    def test_legacy_jvm_loop_preserves_all_other_fallbacks_and_exact_displays(self):
        text=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/AppLanguageTest.kt').read_text();start=text.index('fun furtherOptionsIncludingPrincipalVarietiesKeepTheirExactIdentityAndFallback()');section=text[start:text.index('\n    @Test',start)]
        self.assertEqual(['as','so','wo','ht','tg','mi','sm','sa','pcm','tpi'],re.findall(r'(?:if|else if) \(tag == "([^"]+)"\)',section))
        for tag in TAGS:
            data=bound_fixture(tag);branch=section.split('} else if (tag == '+json.dumps(tag)+') {')[1].split('} else')[0]
            self.assertEqual(4,branch.count('assertEquals('))
            for key in ('ui_menu_file','ui_brush','ui_save','language20_translation_note'):
                self.assertIn('assertEquals('+json.dumps(data['values'][key]['display'],ensure_ascii=False)+',wrapped.getString(R.string.'+key+'))',branch)
        fallback=section.split('} else {')[1]
        for key,value in [('ui_menu_file','File'),('ui_brush','Brush'),('ui_save','Save')]:self.assertIn(f'assertEquals("{value}",wrapped.getString(R.string.{key}))',fallback)
        for assertion in ('assertEquals(tag,AppLanguage.selectedTag(wrapped))','assertEquals(tag,wrapped.resources.configuration.locales[0].toLanguageTag())','assertEquals(tag,Locale.getDefault().toLanguageTag())','assertEquals(tag,manager.applicationLocales[0].toLanguageTag())','assertEquals("en-001",AppLanguage.selectedTag(context))'):
            self.assertIn(assertion,section)

if __name__=='__main__':unittest.main()
