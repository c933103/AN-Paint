"""Keep unsupported-locale numeric fallback distinct from reviewed Breton wording."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
import translation_catalogues as catalogues
from current_localization_contracts import current_display as display

ROOT=Path(__file__).resolve().parents[1]
KEY='ui_d_d_px_d_pixels_2f_mp'
JVM=ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/ImageDisplayLocaleTest.kt'
ENGLISH='%1$d × %2$d px · Pixel count: %3$,d (%4$.2f MP)'

def section(source,name):
    token='    @Test fun '+name+'() {'
    if source.count(token)!=1:raise ValueError('Missing or duplicate complete display test')
    return source.split(token,1)[1].split('\n    @Test',1)[0]

def require_contract(source,offered,paths,english,breton):
    if any(t.split('-')[0]=='qtz'for t in set(offered)|set(paths)):
        raise ValueError('Private-use fallback must stay deliberately unsupported')
    if english!=ENGLISH or breton!=display('br',KEY):raise ValueError('Complete reviewed source/display binding differs')
    fallback=section(source,'englishFallbackStillUsesSelectedLocaleNumbers')
    required=['resources("qtz-u-nu-arab", "en-US")',
        'assertEquals('+json.dumps(ENGLISH,ensure_ascii=False).replace('$','\\$')+',',
        'DecimalFormatSymbols(Locale.forLanguageTag("qtz-u-nu-arab"))',
        "assertEquals('\\u066b', symbols.decimalSeparator)",
        "assertEquals('\\u066c', symbols.groupingSeparator)",
        'assertEquals("١٥٠٠ × ١٥٠٠ px · Pixel count: ٢٬٢٥٠٬٠٠٠ (٢٫٢٥ MP)",',
        'ImageDimensions(1500, 1500).describe())',
        'assertEquals("١٫٥ KiB", memoryLabel(1536.0))']
    for text in required:
        if text not in fallback:raise ValueError('Unsupported fallback/numeric requirement missing')
    direct=section(source,'reviewedBretonSummaryStillUsesSelectedLocaleNumbers')
    for text in ['resources("br", "en-US")',
            'assertEquals('+json.dumps(breton,ensure_ascii=False).replace('$','\\$')+',',
            'DecimalFormatSymbols(Locale.forLanguageTag("br"))',
            "assertEquals(',', symbols.decimalSeparator)",
            'val group = symbols.groupingSeparator',
            'assertEquals("1500 × 1500 px · Niver a bikselioù: 2${group}250${group}000 (2,25 MP)",',
            'ImageDimensions(1500, 1500).describe())',
            'assertEquals("1,5 KiB", memoryLabel(1536.0))']:
        if text not in direct:raise ValueError('Complete offered Breton coverage missing')
    return True

class ImageDisplayFallbackSuccessorTest(unittest.TestCase):
    def setUp(self):
        self.source=JVM.read_text();self.offered=catalogues.offered_tags();self.paths=catalogues.catalogue_paths()
        self.english=ENGLISH;self.breton=display('br',KEY)
    def check(self,source=None,offered=None,paths=None,english=None,breton=None):
        return require_contract(source if source is not None else self.source,
            offered if offered is not None else self.offered,paths if paths is not None else self.paths,
            english if english is not None else self.english,breton if breton is not None else self.breton)
    def test_complete_fallback_and_reviewed_offered_language_consumers(self):
        self.assertTrue(self.check())
        default=E.parse(catalogues.RES/'values/strings.xml').find("./string[@name='"+KEY+"']")
        self.assertEqual(self.english,default.text.strip('"'))
    def test_future_private_use_resource_or_picker_addition_rejected(self):
        for offered,paths in [(self.offered+['qtz'],self.paths),(self.offered,{**self.paths,'qtz-u-nu-arab':Path('unused')})]:
            with self.assertRaises(ValueError):self.check(offered=offered,paths=paths)
    def test_actual_offered_locale_cannot_replace_unsupported_fallback(self):
        for tag in ['is','br','en-US']:
            with self.assertRaises(ValueError):self.check(source=self.source.replace('qtz-u-nu-arab',tag))
    def test_complete_english_and_breton_words_cannot_drift(self):
        for english,breton in [(self.english+'!',self.breton),(self.english,self.breton+'!')]:
            with self.assertRaises(ValueError):self.check(english=english,breton=breton)
        for old in ['Pixel count: ٢','Niver a bikselioù: 2']:
            with self.assertRaises(ValueError):self.check(source=self.source.replace(old,'forged'))
    def test_numeric_symbols_memory_and_offered_case_are_not_optional(self):
        for old in ["assertEquals('\\u066b', symbols.decimalSeparator)","assertEquals('\\u066c', symbols.groupingSeparator)",
                'assertEquals("١٫٥ KiB", memoryLabel(1536.0))','assertEquals("1,5 KiB", memoryLabel(1536.0))',
                'resources("br", "en-US")','val group = symbols.groupingSeparator']:
            with self.assertRaises(ValueError):self.check(source=self.source.replace(old,''))
    def test_duplicate_or_missing_whole_case_is_rejected(self):
        token='    @Test fun reviewedBretonSummaryStillUsesSelectedLocaleNumbers() {'
        for source in [self.source.replace(token,''),self.source+'\n'+token]:
            with self.assertRaises(ValueError):self.check(source=source)

if __name__=='__main__':unittest.main()
