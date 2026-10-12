import unittest
from audit_platform_locale_receipt import check
class PlatformLocaleReceiptTests(unittest.TestCase):
 tags=['en-001','ain-Kana','ca-ES-valencia','ko-Kore-KR','mn-Mong']
 def text(self,tags=None,status=0,expected=None):return '10-12 19:40:00 I LanguagePickerTest: platformLocaleConfigStatus='+str(status)+' expected='+','.join(self.tags if expected is None else expected)+' actual='+','.join(self.tags if tags is None else tags)
 def fail(self,text,tags=None,sdk=35):
  with self.assertRaises(ValueError):check(text,self.tags if tags is None else tags,sdk)
 def test_exact_receipt(self):self.assertEqual(check(self.text(),self.tags,35)['actual_count'],len(self.tags))
 def test_platform_order_is_not_contract(self):check(self.text(self.tags[::-1]),self.tags,35)
 def test_api33_constructor_is_explicit(self):self.assertIn('API33',check(self.text(),self.tags,33)['override_scope'])
 def test_ineligible_api_rejected(self):self.fail(self.text(),sdk=30)
 def test_missing(self):self.fail('')
 def test_duplicate(self):self.fail(self.text()+'\n'+self.text())
 def test_malformed(self):self.fail('platformLocaleConfigStatus=bogus')
 def test_unspecified_and_parse_failure(self):
  for status in (1,2,-1):self.fail(self.text(status=status))
 def test_missing_tag(self):self.fail(self.text(self.tags[:-1]))
 def test_extra_tag(self):self.fail(self.text(self.tags+['fr']))
 def test_duplicate_actual(self):self.fail(self.text(self.tags[:-1]+self.tags[:1]))
 def test_wrong_script(self):self.fail(self.text(['en-001','ain-Latn',*self.tags[2:]]))
 def test_expected_source_drift(self):self.fail(self.text(expected=self.tags[::-1]))
 def test_empty_expected(self):self.fail(self.text(),tags=[])
 def test_duplicate_expected(self):self.fail(self.text(),tags=self.tags+self.tags[:1])
 def test_null_or_empty_actual(self):
  self.fail(self.text(['null']));self.fail(self.text([]))
if __name__=='__main__':unittest.main()
