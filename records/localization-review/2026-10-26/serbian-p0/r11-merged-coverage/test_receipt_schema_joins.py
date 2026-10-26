"""Synthetic producer-schema joins: these are never actual execution receipts."""
import unittest
from copy import deepcopy
from test_coverage_guards import synthetic_terminal
import recompute_coverage as c

def fixture():
 e=synthetic_terminal();p={}
 for kind,r in e['verified_receipts'].items():
  r['artifact_id']={'apk-source':1,'compiled-values':1,'regression-lint':2,'exact-script':3,'api35':4}[kind]
  d={'run_id':r['run_id'], 'source_commit' if kind=='exact-script' else 'tested_commit':r['tested_commit'], 'reviewed_pr_head' if kind in ('exact-script','api35') else 'reviewed_head':c.HEAD}
  if kind!='regression-lint':d['tree' if kind in ('compiled-values','exact-script') else 'source_tree']=c.TREE
  if kind!='compiled-values':d['artifact_id']=r['artifact_id'];d['archive_sha256' if kind in ('apk-source','exact-script') else 'artifact_sha256']=str(r['artifact_id'])*64
  p[kind]=d
 p['apk-source']['build_info']={'apk_sha256':'a'*64};p['compiled-values']['apk_sha256']='a'*64
 p['compiled-values']['new_reviewed_entries']=148;p['compiled-values']['new_reviewed_entries_by_locale']={'sr-Cyrl':74,'sr-Latn':74}
 return e,p

class ReceiptSchemaJoins(unittest.TestCase):
 def test_actual_schema_absences_supported_without_fabrication(self):
  e,p=fixture();before=deepcopy(p);self.assertEqual(c.bind_receipt_payloads(e,p)['actual_push_run']['id'],123);self.assertEqual(before,p)
  self.assertNotIn('artifact_id',p['compiled-values']);self.assertNotIn('source_tree',p['regression-lint'])
 def test_every_present_identity_mutation_rejected(self):
  count=0
  for kind,fields in fixture()[1].items():
   for key in fields:
    if key=='build_info':continue
    e,p=fixture();p[kind][key]=0 if key in ('run_id','artifact_id') else 'wrong'
    with self.subTest(kind=kind,key=key),self.assertRaises((ValueError,KeyError)):c.bind_receipt_payloads(e,p)
    count+=1
  self.assertEqual(count,30)
 def test_prior_locale_or_expanded_review_scope_is_not_current_Serbian_acceptance(self):
  for count,locales in [(156,{'sk':78,'sl':78}),(148,{'sr-Cyrl':75,'sr-Latn':73}),(148,{'sr-Cyrl':74,'sr-Latn':74,'sk':78})]:
   e,p=fixture();p['compiled-values']['new_reviewed_entries']=count;p['compiled-values']['new_reviewed_entries_by_locale']=locales
   with self.subTest(count=count,locales=locales),self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
 def test_missing_family_and_artifact_joins_rejected(self):
  for kind in fixture()[1]:
   e,p=fixture();p.pop(kind)
   with self.subTest(missing=kind),self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
  e,p=fixture();e['verified_receipts']['compiled-values']['artifact_id']=2
  with self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
  e,p=fixture();p['apk-source']['build_info']['apk_sha256']='wrong'
  with self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
  e,p=fixture();e['artifacts'][0]['sha256']='f'*64
  with self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
if __name__=='__main__':unittest.main()
