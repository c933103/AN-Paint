"""Synthetic receipt-schema guards only; no actual CI claim."""
from copy import deepcopy
import unittest
import actual_join as c
SYNTHETIC_MERGE=c.MERGE

def fixture():
 arts=[{'id':x,'run_id':123,'head':SYNTHETIC_MERGE,'expired':False,'sha256':str(x)*64} for x in range(1,5)]
 e={'schema_version':1,'record_kind':'actual-postmerge-terminal','merge':{'sha':SYNTHETIC_MERGE,'tree':c.TREE,'ordered_parents':[c.BASE,c.HEAD],'develop_at_verification':SYNTHETIC_MERGE},'PR':{'number':183,'head':c.HEAD,'tree':c.TREE,'run_id':122,'artifact_ids':[11,12,13,14]},'run':{'id':123,'head':SYNTHETIC_MERGE,'event':'push','status':'completed','conclusion':'success','attempt':1,'updated_at':'synthetic-only'},'checks':[{'id':i,'name':n,'head':SYNTHETIC_MERGE,'status':'completed','conclusion':'success'} for i,n in enumerate(sorted(c.CHECKS))],'artifacts':arts,'verified_receipts':{},'compiled_values':{'new_hr':78,'new_bs':78,'new_reviewed':156,'preserved_hr_bs':215,'prior_reviewed':697,'combined_bounded_reviewed':853},'new_linguistic_acceptances_due_to_CI':0,'native_human_layout_whole_language_release_certifications':0};p={}
 for kind,aid in {'apk-source':1,'compiled-values':1,'regression-lint':2,'exact-script':3,'api35':4}.items():
  e['verified_receipts'][kind]={'run_id':123,'tested_commit':SYNTHETIC_MERGE,'source_tree':c.TREE,'reviewed_pr_head':c.HEAD,'artifact_id':aid,'result':'pass','receipt_sha256':'b'*64}
  d={'run_id':123,'source_commit' if kind=='exact-script' else 'tested_commit':SYNTHETIC_MERGE,'reviewed_pr_head' if kind in ('exact-script','api35') else 'reviewed_head':c.HEAD}
  if kind!='regression-lint':d['tree' if kind in ('compiled-values','exact-script') else 'source_tree']=c.TREE
  if kind!='compiled-values':d['artifact_id']=aid;d['archive_sha256' if kind in ('apk-source','exact-script') else 'artifact_sha256']=str(aid)*64
  p[kind]=d
 p['apk-source']['build_info']={'apk_sha256':'a'*64};p['compiled-values'].update(apk_sha256='a'*64,current_Serbian_reviewed_entries=149,current_Serbian_reviewed_entries_by_locale={'sr-Cyrl':75,'sr-Latn':74},successor_changed_values=2,unchanged_Serbian_reviewed_values=147,prior_reviewed_entries=548,total_reviewed_entries=853,new_reviewed_entries=156,new_reviewed_entries_by_locale={'hr':78,'bs':78},prior_reviewed_total=697,inherited_entries=806,inherited_entries_by_locale={'hr':98,'bs':117,'sk':127,'sl':127,'sr-Cyrl':169,'sr-Latn':168})
 return e,p
class Joins(unittest.TestCase):
 def test_schema_join_without_fabrication(self):
  e,p=fixture();before=deepcopy(p);self.assertEqual(c.bind_receipt_payloads(e,p)['actual_merge'],SYNTHETIC_MERGE);self.assertEqual(before,p);self.assertNotIn('source_tree',p['regression-lint']);self.assertNotIn('artifact_id',p['compiled-values'])
 def test_each_payload_identity_and_scope_mutation(self):
  for kind,fields in fixture()[1].items():
   for field in fields:
    if field=='build_info':continue
    e,p=fixture();p[kind][field]='wrong'
    with self.subTest(kind=kind,field=field),self.assertRaises((ValueError,KeyError)):c.bind_receipt_payloads(e,p)
 def test_PR_run_prior_merge_and_partial_run_rejected(self):
  for group,key,value in [('PR','number',180),('PR','head',c.BASE),('merge','sha',c.BASE),('merge','ordered_parents',[c.HEAD,c.BASE]),('run','head',c.HEAD),('run','event','pull_request'),('run','id',122),('run','status','in_progress'),('run','conclusion','failure')]:
   e,p=fixture();e[group][key]=value
   with self.subTest(group=group,key=key),self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
 def test_missing_checks_families_and_wrong_artifacts_rejected(self):
  for kind in fixture()[1]:
   e,p=fixture();p.pop(kind)
   with self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
  for key,value in [('expired',True),('id',11),('sha256','f'*64)]:
   e,p=fixture();e['artifacts'][0][key]=value
   with self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
  e,p=fixture();e['checks'].pop()
  with self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
 def test_old148_partition_and_extra_acceptance_rejected(self):
  for key,value in [('new_reviewed',853),('preserved_hr_bs',337),('new_hr',0)]:
   e,p=fixture();e['compiled_values'][key]=value
   with self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
  for key in ('new_linguistic_acceptances_due_to_CI','native_human_layout_whole_language_release_certifications'):
   e,p=fixture();e[key]=1
   with self.assertRaises(ValueError):c.bind_receipt_payloads(e,p)
if __name__=='__main__':unittest.main()
