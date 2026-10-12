"""Synthetic Save telemetry controls; not native Android execution evidence."""
import unittest
from audit_native_vertical import parse_save
class SaveTelemetryCheckerTests(unittest.TestCase):
 case='lzh-Hant-landscape'
 fields='default=en-US activity=lzh-Hant,en-US target=lzh-Hant,en-US rootLocale=lzh-Hant,en-US dialogLocale=absent application=en-US selected=lzh-Hant busy=false draft=10 saved=10 attached=true raw=Rect(10, 20 - 30, 40) visible=Rect(10, 20 - 30, 40) root=false form=absent columns=absent'
 def raw(self,phases=('before','touch=ACTION_DOWN','touch=ACTION_UP'),fields=None):return '\n'.join('10-12 17:00:01.123  100  100 I VerticalLocaleDeviceTest: '+self.case+' Save '+p+' '+(fields or self.fields) for p in phases).encode()
 def test_resource_mismatch_with_process_is_retained(self):
  r=parse_save(self.raw(),{self.case},1);self.assertEqual(['en-US'],r['cases'][0]['process_locales'])
 def test_incomplete_duplicate_missing_or_failure_sequences_fail(self):
  for phases in [('before','touch=ACTION_DOWN'),('touch=ACTION_DOWN','touch=ACTION_UP'),('before','touch=ACTION_DOWN','touch=ACTION_DOWN','touch=ACTION_UP'),('before','touch=ACTION_UP'),('before','failure')]:
   with self.assertRaises(ValueError):parse_save(self.raw(phases),{self.case},1)
 def test_canceled_reveal_then_completed_tap_is_retained(self):
  r=parse_save(self.raw(('before','touch=ACTION_DOWN','touch=ACTION_CANCEL','touch=ACTION_DOWN','touch=ACTION_UP')),{self.case},1);self.assertEqual(5,len(r['records']))
 def test_source_call_count_and_case_inventory_fail_closed(self):
  for cases,count in [({self.case},2),({self.case,'en-XV-landscape'},1),({'en-XV-landscape'},1)]:
   with self.assertRaises(ValueError):parse_save(self.raw(),cases,count)
 def test_resource_locale_busy_attachment_and_invisible_target_fail(self):
  for src,dst in [('target=lzh-Hant,en-US','target=en-US'),('rootLocale=lzh-Hant,en-US','rootLocale=en-US'),('busy=false','busy=true'),('attached=true','attached=false'),('visible=Rect(10, 20 - 30, 40)','visible=Rect(0, 0 - 0, 0)')]:
   with self.assertRaises(ValueError):parse_save(self.raw(fields=self.fields.replace(src,dst)),{self.case},1)
 def test_duplicate_missing_malformed_fields_fail(self):
  for fields in [self.fields+' default=en-US',self.fields.replace(' saved=10',''),self.fields.replace('draft=10','draft=false'),self.fields.replace('root=false','root=0')]:
   with self.assertRaises(ValueError):parse_save(self.raw(fields=fields),{self.case},1)
if __name__=='__main__':unittest.main()
