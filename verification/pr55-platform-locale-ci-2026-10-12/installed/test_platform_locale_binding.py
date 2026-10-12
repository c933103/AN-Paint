import unittest
from audit_platform_locale_binding import bind_method,IDENTITY
class BoundPlatformReceiptTests(unittest.TestCase):
 tags=['en-001','ain-Kana']
 def line(self,logger,message,pid=42,tid=43):return f'10-12 19:40:00.000 {pid} {tid} I {logger}: {message}'
 def good(self):
  target=IDENTITY[1]+'('+IDENTITY[0]+')'
  return '\n'.join([self.line('TestRunner','started: '+target),self.line('LanguagePickerTest','platformLocaleConfigStatus=0 expected='+','.join(self.tags)+' actual='+','.join(self.tags)),*[self.line('LanguagePickerTest','device=en-US app='+t+' first=0 label=Use device language',tid=42) for t in ('ja','ar','en-001')],self.line('TestRunner','finished: '+target)])
 def bad(self,text):
  with self.assertRaises(ValueError):bind_method(text,self.tags)
 def test_exact_bound_method(self):self.assertEqual(bind_method(self.good(),self.tags)['line'],2)
 def test_receipt_before_or_after_method(self):
  lines=self.good().splitlines()
  self.bad('\n'.join([lines[1],lines[0],*lines[2:]]));self.bad('\n'.join([lines[0],*lines[2:],lines[1]]))
 def test_missing_or_duplicate_boundaries(self):
  lines=self.good().splitlines()
  for text in ('\n'.join(lines[1:]),'\n'.join(lines[:-1]),self.good()+'\n'+lines[0],self.good()+'\n'+lines[-1]):self.bad(text)
 def test_wrong_method(self):self.bad(self.good().replace(IDENTITY[1],'anotherMethod'))
 def test_wrong_receipt_process_or_thread(self):
  for prefix in ('99 43','42 99'):self.bad(self.good().replace('42 43 I LanguagePickerTest',prefix+' I LanguagePickerTest'))
 def test_wrong_boundary_process_or_thread(self):
  for prefix in ('99 43','42 99'):self.bad(self.good().replace('42 43 I TestRunner: finished',prefix+' I TestRunner: finished'))
 def test_wrong_receipt_logger(self):self.bad(self.good().replace('I LanguagePickerTest: platform','I OtherLogger: platform'))
 def test_bad_line_format(self):self.bad(self.good().replace('10-12 19:40:00.000 42 43 I LanguagePickerTest','NotLogcat LanguagePickerTest'))
 def test_interleaved_method_or_failure(self):
  for message in ('started: Other(class)','finished: Other(class)','failed: '+IDENTITY[1]+'('+IDENTITY[0]+')'):
   lines=self.good().splitlines();lines.insert(2,self.line('TestRunner',message));self.bad('\n'.join(lines))
 def test_labels_wrong_missing_duplicate_or_process(self):
  lines=self.good().splitlines()
  for text in (self.good().replace('app=ja','app=fr'),'\n'.join(lines[:2]+lines[3:]),'\n'.join(lines[:2]+[lines[2]]+lines[2:]),self.good().replace('42 42 I LanguagePickerTest','99 42 I LanguagePickerTest')):self.bad(text)
if __name__=='__main__':unittest.main()
