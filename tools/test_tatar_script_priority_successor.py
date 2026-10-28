"""Finite current Tatar device label; historical script fixture is immutable."""
import json
from copy import deepcopy
from pathlib import Path
import unittest
from sorani_uyghur_tatar_priority_expectations import reviewed_tatar_script_row,bound_fixture
ROOT=Path(__file__).resolve().parents[1]
class TatarScriptPrioritySuccessorTest(unittest.TestCase):
 def setUp(self):
  self.row=next(r for r in json.loads((ROOT/'Paintroid/src/test/resources/exact-script-resources/expected.json').read_text())if r['requested_tag']=='tt-Cyrl')
 def test_exact_bound_addition_keeps_history_and_other_two_fields(self):
  old=deepcopy(self.row);new=reviewed_tatar_script_row(self.row)
  self.assertEqual(old,self.row)
  expected=deepcopy(old);expected['expected']['language20_device_default']='Җайланма телен куллану'
  self.assertEqual(expected,new)
 def test_rejects_every_changed_historical_field_and_wrong_type(self):
  invalid=[None,[],True,0,'',{}]
  for key in self.row:
   v=deepcopy(self.row);v.pop(key);invalid.append(v)
   for bad in [None,[],True,0,'forged',{}]:
    v=deepcopy(self.row);v[key]=bad;invalid.append(v)
  for key in self.row['expected']:
   v=deepcopy(self.row);v['expected'].pop(key);invalid.append(v)
   for bad in [None,[],True,0,'forged',{}]:
    v=deepcopy(self.row);v['expected'][key]=bad;invalid.append(v)
  for v in invalid:
   with self.assertRaises(ValueError):reviewed_tatar_script_row(v)
 def test_rejects_changed_bound_review_fields(self):
  for key in ['source','previous_target','reviewed_value','reviewed_attributes','display']:
   d=deepcopy(bound_fixture('tt-Cyrl'));d['values']['language20_device_default'][key]='forged'
   with self.assertRaises(ValueError):reviewed_tatar_script_row(self.row,d)
