"""Synthetic guard tests; no synthetic terminal object is actual execution evidence."""
from copy import deepcopy
import argparse,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import recompute_coverage as c
R=Path(__file__).resolve().parent

def synthetic_terminal():
 merge='a'*40;run=123;arts=[{'id':x,'run_id':run,'head':merge,'expired':False,'sha256':str(x)*64} for x in (1,2,3,4)]
 return {'schema_version':1,'record_kind':'actual-postmerge-terminal','merge':{'sha':merge,'tree':c.TREE,'ordered_parents':[c.BASE,c.HEAD],'develop_at_verification':merge},'PR':{'number':179,'head':c.HEAD,'tree':c.TREE,'run_id':122,'artifact_ids':[11,12,13,14]},'run':{'id':run,'head':merge,'event':'push','status':'completed','conclusion':'success','attempt':1,'updated_at':'synthetic-time-not-evidence'},'checks':[{'id':x,'name':n,'head':merge,'status':'completed','conclusion':'success'} for x,n in enumerate(sorted(c.CHECKS))],'artifacts':arts,'verified_receipts':{n:{'run_id':run,'tested_commit':merge,'source_tree':c.TREE,'reviewed_pr_head':c.HEAD,'artifact_id':1+i%4,'result':'pass','receipt_sha256':'b'*64} for i,n in enumerate(['apk-source','compiled-values','regression-lint','exact-script','api35'])},'compiled_values':{'new_reviewed_sk':78,'new_reviewed_sl':78,'exact_new_reviewed':156},'new_linguistic_acceptances_due_to_CI':0,'native_human_layout_whole_language_release_certifications':0}
class CoverageGuards(unittest.TestCase):
 def test_synthetic_terminal_shape_positive_is_not_execution_evidence(self):
  self.assertEqual(123,c.validate_actual(synthetic_terminal(),None)['actual_push_run']['id'])
 def test_terminal_identity_and_scope_mutations_rejected(self):
  cases=[]
  for field,value in [('schema_version',2),('record_kind','PR-success'),('new_linguistic_acceptances_due_to_CI',156),('native_human_layout_whole_language_release_certifications',1)]:
   d=synthetic_terminal();d[field]=value;cases.append(d)
  for group,field,value in [('PR','number',178),('PR','head',c.BASE),('PR','tree','0'*40),('merge','sha',c.HEAD),('merge','tree','0'*40),('merge','ordered_parents',[c.HEAD,c.BASE]),('merge','develop_at_verification',c.HEAD),('run','head',c.HEAD),('run','event','pull_request'),('run','status','in_progress'),('run','conclusion','failure'),('run','id',122),('run','attempt',0),('run','updated_at','')]:
   d=synthetic_terminal();d[group][field]=value;cases.append(d)
  for field,value in [('head',c.HEAD),('status','queued'),('conclusion','skipped'),('name','invented')]:
   d=synthetic_terminal();d['checks'][0][field]=value;cases.append(d)
  d=synthetic_terminal();d['checks'].pop();cases.append(d)
  d=synthetic_terminal();d['checks'][0]['id']=d['checks'][1]['id'];cases.append(d)
  for field,value in [('run_id',122),('head',c.HEAD),('expired',True),('sha256','wrong'),('id',11)]:
   d=synthetic_terminal();d['artifacts'][0][field]=value;cases.append(d)
  d=synthetic_terminal();d['artifacts'].append(d['artifacts'][0]);cases.append(d)
  for field,value in [('run_id',122),('tested_commit',c.HEAD),('source_tree','0'*40),('reviewed_pr_head',c.BASE),('artifact_id',99),('result','pending'),('receipt_sha256','wrong')]:
   d=synthetic_terminal();d['verified_receipts']['api35'][field]=value;cases.append(d)
  d=synthetic_terminal();d['verified_receipts'].pop('api35');cases.append(d)
  d=synthetic_terminal();d['compiled_values']['exact_new_reviewed']=155;cases.append(d)
  for i,d in enumerate(cases):
   with self.subTest(i=i),self.assertRaises(ValueError):c.validate_actual(d,None)
  self.assertEqual(39,len(cases))
 def test_actual_mode_requires_real_evidence_and_immutable_manifest(self):
  with tempfile.TemporaryDirectory() as tmp:
   a=argparse.Namespace(inputs=R/'inputs',source_root=R.parent/'source',baseline_source_root=R.parent/'base-source',out=Path(tmp)/'out',mode='actual-postmerge',actual_evidence=None,actual_manifest_sha256=None)
   with patch.object(c,'compute',return_value=({},{})),self.assertRaises(ValueError):c.run(a)
   self.assertFalse(a.out.exists())
 def test_XML_duplicates_entities_empty_and_wrong_type_rejected(self):
  for xml in [b'<resources><string name="x">a</string><string name="x">b</string></resources>',b'<!DOCTYPE resources><resources/>',b'<!ENTITY x "a"><resources/>',b'<resources><string name="x"/></resources>',b'<resources><integer name="x">1</integer></resources>',b'<resources><plurals name="x"><item quantity="bogus">a</item></plurals></resources>']:
   with self.subTest(xml=xml),self.assertRaises(ValueError):c.parse(xml)
 def test_Git_tree_mutations_rejected(self):
  tree=c.read(R/'inputs/source-head-tree.json')
  for kind in ['sha','duplicate','mode','path','truncated','blob']:
   d=deepcopy(tree)
   if kind=='sha':d['sha']='0'*40
   elif kind=='duplicate':d['tree'].append(d['tree'][0])
   elif kind=='mode':d['tree'][0]['mode']='100777'
   elif kind=='path':d['tree'][0]['path']='../outside'
   elif kind=='truncated':d['truncated']=True
   else:next(e for e in d['tree'] if e['type']=='blob')['sha']='0'*40
   with self.subTest(kind=kind),self.assertRaises(ValueError):c.verify_tree(d,c.TREE)
 def test_duplicate_JSON_and_path_traversal_rejected(self):
  with self.assertRaises(ValueError):json.loads('{"a":1,"a":2}',object_pairs_hook=c.unique)
  for path in ['../outside','/absolute','a\\b']:
   with self.assertRaises(ValueError):c.safe(R,path)
if __name__=='__main__':unittest.main()
