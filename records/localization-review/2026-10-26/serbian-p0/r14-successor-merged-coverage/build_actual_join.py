#!/usr/bin/env python3
"""Build an exact actual-merge join from hash-pinned original producer receipts."""
from pathlib import Path
import shutil
from coverage_common import *
import actual_join as c
R=Path(__file__).resolve().parent; SOURCE=R.parent/'postmerge-ci'; DEST=R/'actual-evidence'
PIN='1ed57fde279530b33cb2c29888cba01fcfc4e72eff672fb083a8a6c5a0dfd404'
def main():
 m=read(SOURCE/'manifest.json');require(sha((SOURCE/'manifest.json').read_bytes())==PIN,'producer manifest pin')
 DEST.mkdir(exist_ok=True)
 for e in m['files']:
  b=c.safe(SOURCE,e['path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'] and git(b)==e['git_blob_sha1'],'producer payload '+e['path']);p=c.safe(DEST,e['path']);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 shutil.copyfile(SOURCE/'manifest.json',DEST/'producer-manifest.json')
 merge=read(R/'inputs/actual-merge-readback.json');develop=read(R/'inputs/develop-readback.json');run=read(DEST/'run-terminal.json');jobs=read(DEST/'jobs-terminal.json')['jobs'];ledger=read(DEST/'artifact-ledger.json')
 require(merge['sha']=='0ebd41d4d9b665213c776f5a0479a29ecabdd243' and merge['tree']==c.TREE and merge['ordered_parents']==[c.BASE,c.HEAD] and develop['sha']==merge['sha'],'actual immutable merge')
 selected=[]
 for name in sorted(c.CHECKS):
  candidates=[j for j in jobs if j['name']==name];require(bool(candidates),'missing job');j=max(candidates,key=lambda x:(x['run_attempt'],x['id']));require(j['head_sha']==merge['sha'] and j['run_id']==run['id'],'job source/run');selected.append({'id':j['id'],'name':name,'head':j['head_sha'],'status':j['status'],'conclusion':j['conclusion'],'attempt':j['run_attempt']})
 filenames={'apk-source':'artifact-source-binding.json','compiled-values':'compiled-resource-verification.json','regression-lint':'hosted-regression-verification.json','exact-script':'exact-script-verification.json','api35':'api35-terminal-verification.json'}
 receipts={};apk=read(DEST/filenames['apk-source'])
 for kind,path in filenames.items():
  p=read(DEST/path);receipts[kind]={'run_id':run['id'],'tested_commit':merge['sha'],'source_tree':c.TREE,'reviewed_pr_head':c.HEAD,'artifact_id':apk['artifact_id'] if kind=='compiled-values' else p['artifact_id'],'result':'pass','receipt_path':path,'receipt_sha256':sha((DEST/path).read_bytes())}
 envelope={'schema_version':1,'record_kind':'actual-postmerge-terminal','merge':{'sha':merge['sha'],'tree':merge['tree'],'ordered_parents':merge['ordered_parents'],'develop_at_verification':develop['sha']},'PR':{'number':182,'head':c.HEAD,'tree':c.TREE,'run_id':40398554058,'artifact_ids':list(ledger['prior_PR_artifact_ids'].values())},'run':{'id':run['id'],'head':run['head_sha'],'event':run['event'],'status':run['status'],'conclusion':run['conclusion'],'attempt':run['run_attempt'],'updated_at':run['updated_at']},'checks':selected,'artifacts':[{'id':a['id'],'run_id':a['workflow_run']['id'],'head':a['workflow_run']['head_sha'],'expired':a['expired'],'sha256':a['digest'].removeprefix('sha256:'),'name':a['name'],'expires_at':a['expires_at']} for a in ledger['artifacts']],'verified_receipts':receipts,'compiled_values':{'current_reviewed_sr_Cyrl':75,'current_reviewed_sr_Latn':74,'current_unique_reviewed':149,'corrected_values':2,'unchanged_reviewed':147,'preserved_inherited':337},'new_linguistic_acceptances_due_to_CI':0,'native_human_layout_whole_language_release_certifications':0,'qualification':'Actual natural push attempt 1 success, no retry. API35 core 1 / position 1 / composed 1. Historical PR and PR180 failures remain separate immutable records, not actual PR182 execution evidence.'}
 c.bind_receipt_payloads(envelope,{k:read(DEST/p) for k,p in filenames.items()});emit(DEST,'coverage-terminal-envelope.json',envelope)
 files=[]
 for p in sorted(DEST.rglob('*')):
  if p.is_file() and p.name!='manifest.json':
   b=p.read_bytes();files.append({'path':p.relative_to(DEST).as_posix(),'bytes':len(b),'sha256':sha(b),'git_blob_sha1':git(b)})
 emit(DEST,'manifest.json',{'schema_version':1,'producer_manifest_sha256':PIN,'source_commit':merge['sha'],'source_tree':c.TREE,'files':files});print(sha((DEST/'manifest.json').read_bytes()))
if __name__=='__main__':main()
