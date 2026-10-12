import unittest
from audit_success_protocol import verify_success_sequence
IDENTITY=('example.Test','method')
def event(code):
 return 'INSTRUMENTATION_STATUS: class=example.Test\nINSTRUMENTATION_STATUS: test=method\nINSTRUMENTATION_STATUS: current=1\nINSTRUMENTATION_STATUS: numtests=1\nINSTRUMENTATION_STATUS_CODE: '+str(code)+'\n'
def good():return event(1)+event(0)+'INSTRUMENTATION_CODE: -1\n'
class ProtocolControls(unittest.TestCase):
 def test_complete_serial_success(self):self.assertEqual(verify_success_sequence(good(),{IDENTITY})['event_count'],2)
 def test_missing_duplicate_or_wrong_terminal(self):
  for bad in (good().removesuffix('INSTRUMENTATION_CODE: -1\n'),good()+'INSTRUMENTATION_CODE: -1\n',good().replace('INSTRUMENTATION_CODE: -1','INSTRUMENTATION_CODE: 0')):
   with self.assertRaises(ValueError):verify_success_sequence(bad,{IDENTITY})
 def test_failed_duplicate_reordered_or_postterminal_status(self):
  for bad in (event(1)+event(-2)+'INSTRUMENTATION_CODE: -1\n',event(0)+event(1)+'INSTRUMENTATION_CODE: -1\n',event(1)+good(),good()+event(1)):
   with self.assertRaises(ValueError):verify_success_sequence(bad,{IDENTITY})
 def test_missing_extra_or_wrong_count_identity(self):
  for bad in (good().replace('test=method','test=other'),good().replace('numtests=1','numtests=2'),good().replace('current=1','current=2'),good().replace('class=example.Test','class=example.Test\nINSTRUMENTATION_STATUS: class=example.Test')):
   with self.assertRaises(ValueError):verify_success_sequence(bad,{IDENTITY})
