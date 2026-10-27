"""Actual-merge source/status guard mutations; no external or source writes."""
import argparse,copy,json
from pathlib import Path
from unittest.mock import patch
import recompute_integrated as v
p=argparse.ArgumentParser()
for name in ('inputs','source-root','original-source-root','baseline-source-root','out'):p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();outputs,engine=v.prepare(a);cases=[]
def reject(label,fn,expected=None):
 try:fn()
 except (ValueError,KeyError,TypeError,IndexError) as e:
  if expected:v.need(expected in str(e),'wrong guard '+label+': '+str(e))
  cases.append({'case':label,'result':'rejected','guard':str(e)});return
 raise ValueError('accepted negative '+label)
proof=v.read(a.inputs/'actual-merge-identity.json')
for label,fn in [('wrong actual merge',lambda d:d.__setitem__('merge',v.OLD_HEAD)),('wrong actual tree',lambda d:d.__setitem__('tree',v.OLD_TREE)),('reversed parents',lambda d:d['parents'].reverse()),('wrong reviewed head',lambda d:d.__setitem__('reviewed_head',v.OLD_HEAD)),('stale develop ref',lambda d:d.__setitem__('develop_at_verification',v.BASE)),('unverified merge',lambda d:d.__setitem__('actual_merge_and_branch_verified',False)),('wrong PR number',lambda d:d.__setitem__('pr',177)),('wrong PR gate run',lambda d:d.__setitem__('PR_gate_run',40340230583)),('relabeled PR event as postmerge',lambda d:d['postmerge_runs'][0].__setitem__('event','pull_request')),('wrong pending push head',lambda d:d['postmerge_runs'][0].__setitem__('head',v.HEAD)),('wrong pending push run',lambda d:d['postmerge_runs'][0].__setitem__('id',40346532936)),('invented terminal success',lambda d:d['postmerge_runs'][0].__setitem__('status','completed')),('missing pending push',lambda d:d.__setitem__('postmerge_runs',[])),('duplicate pending push',lambda d:d['postmerge_runs'].append(copy.deepcopy(d['postmerge_runs'][0]))),('invented successful status text',lambda d:d.__setitem__('postmerge_status','success'))]:
 d=copy.deepcopy(proof);fn(d);reject(label,lambda d=d:v.validate_merge(d))
# These inspect metadata structures with the recursive Git hashing guard, not a mocked successful root.
tree=v.read(a.inputs/'fixed-head-tree.json')
for label,fn in [('truncated actual tree',lambda d:d.__setitem__('truncated',True)),('forged actual root',lambda d:d.__setitem__('sha','0'*40)),('forged resource leaf',lambda d:next(x for x in d['tree'] if x['path']=='Paintroid/src/main/res/values-ro/strings.xml').__setitem__('sha','0'*40)),('forged numeric repair leaf',lambda d:next(x for x in d['tree'] if x['path']==v.TEST).__setitem__('sha','0'*40)),('duplicate actual tree path',lambda d:d['tree'].append(copy.deepcopy(d['tree'][0])))]:
 d=copy.deepcopy(tree);fn(d);reject(label,lambda d=d:engine.verify_tree(d,v.TREE))
# Explicit synthetic read substitutions verify immutable provenance and raw-source checks.
original=Path.read_bytes
for label,path,guard in [('preview ledger corruption',a.inputs/'original-preview/review-scope-reconciliation.json','historical payload identity'),('original failure removed',a.inputs/'original-failure/failure-analysis.json','historical payload identity'),('repair provenance corrupted',a.inputs/'oracle-repair/oracle-change.json','historical payload identity'),('corrected PR falsely relabelled',a.inputs/'corrected-PR-terminal/run-review-artifact-identity.json','historical payload identity'),('actual merge proof corrupted',a.inputs/'actual-merge-identity.json',None),('actual raw numeric source corrupted',a.source_root/v.TEST,'actual raw source Git binding'),('actual raw locale source corrupted',a.source_root/'Paintroid/src/main/res/values-ro/strings.xml','actual raw source Git binding')]:
 def changed(p,path=path):return b'{"corrupted":"synthetic"}\n' if p==path else original(p)
 def check():
  with patch.object(Path,'read_bytes',changed):v.prepare(a)
 reject(label,check,guard)
v.need(len(cases)==len({x['case'] for x in cases})==27,'integrated guard inventory')
a.out.mkdir(parents=True,exist_ok=True);v.emit(a.out,'integrated-mutation-controls.json',{'schema_version':1,'source_commit':v.MERGE,'source_tree':v.TREE,'source_status':v.STATUS,'positive_actual_source_recomputation':'passed','controls_rejected':27,'cases':cases,'historical_preview_71_controls_preserved':True,'source_files_changed':False,'limits':['All failures are labelled synthetic test mutations, not observed defects.','Historical preview source/data controls and all 84 preview files remain unchanged.','Pending postmerge identity is verified; no actual postmerge success is created or inferred.']});print(27)
