#!/usr/bin/env python3
"""Fresh 171-option source recomputation joined to exact actual PR183 push receipts."""
from pathlib import Path
import argparse,csv,json
import recompute_coverage as source
import actual_join as actual
from coverage_common import read,emit,require

def run(a):
 out=source.compute(a.inputs,a.source_root,a.baseline_source_root)
 merge=read(a.inputs/'actual-merge-readback.json');develop=read(a.inputs/'actual-develop-readback.json')
 require(merge['sha']==actual.MERGE and merge['tree']['sha']==source.TREE and [p['sha'] for p in merge['parents']]==[source.BASE,source.HEAD],'independent actual Git merge binding')
 develop_sha=develop.get('commit',{}).get('sha') or develop.get('object',{}).get('sha') or develop.get('sha')
 require(develop_sha==actual.MERGE,'actual develop readback')
 require(a.actual_evidence is not None and a.actual_manifest_sha256 is not None,'actual evidence and caller-pinned manifest required')
 envelope=read(a.actual_evidence/'coverage-terminal-envelope.json');terminal=actual.join_actual(envelope,a.actual_evidence,a.actual_manifest_sha256)
 out['terminal-status-supplement.json']=terminal
 for name in ('coverage-delta.json','review-scope-reconciliation.json','full-source-delta.json'):out[name]['source_commit']=actual.MERGE;out[name]['source_status']='actual merge; supplied fresh actual-postmerge terminal evidence verified'
 out['coverage-delta.json'].update(current_production_replaced=True,actual_postmerge_status='success; fresh actual push artifacts, not PR artifacts')
 a.out.mkdir(parents=True,exist_ok=True)
 for n,v in out.items():emit(a.out,n,v)
 with (a.out/'structural-per-locale.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(out['structural-per-locale.json'][0]));w.writeheader();w.writerows(out['structural-per-locale.json'])
 print(json.dumps({'source_commit':actual.MERGE,'source_tree':source.TREE,'options':171,'new_reviewed_HR_BS':156,'preserved_HR_BS':215,'actual_push_run':terminal['actual_push_run']['id'],'actual_push_attempt':terminal['actual_push_run']['attempt'],'actual_postmerge_verified':True},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ('inputs','source-root','baseline-source-root','out','actual-evidence'):p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--actual-manifest-sha256',required=True);run(p.parse_args())
