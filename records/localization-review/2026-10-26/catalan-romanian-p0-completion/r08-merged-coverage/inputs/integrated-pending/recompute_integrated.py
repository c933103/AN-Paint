"""Actual merge source coverage with pending postmerge CI; historical PR proof is separate."""
import argparse,collections,csv,difflib,hashlib,json,types
from pathlib import Path
MERGE='e5f2d4e2d07e678076f022aa7b3ef923e13c3721'
TREE='806d9577409c4044212d1c12e6e38da46417bae6'
BASE='ce796879f4568a27b9d905a8e8db639dd0a93a30'
HEAD='82995ec1f030d23cb4e2b1426b511abe802890eb'
OLD_HEAD='93f27ed172cc730c80ed7a2ffbcacc1b0c04383f'
OLD_TREE='571ec84860cb837ae8376f72d0becfb8fd2b7b6d'
STATUS='integrated actual merge source; actual postmerge push run 40350966050 pending in supplied identity receipt'
IDENTITY_HASH='0abf768af2344a93fa403e1730a11f049c92d1e9cb1d4fc314baaacf784c3d4e'
MANIFESTS={'original-preview':'28c877a059427dc64b6850c253198ddd07caadb8e655059e4e4f43a026e1520d','original-failure':'f3c1bf8082388baf86959be2179cdadd9393be6a13f95c35f78d6677ab06a64e','oracle-repair':'c4e46822e923c95f08fd786e46f8a1003ea381392bf10b81842d3b2310c56b5e','corrected-PR-terminal':'1abd19748c8cf746781e7fda6e2830c0109a6e64996a430392b5c764f963c438'}
TEST='Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt'
def need(ok,m):
 if not ok:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def unique(pairs):
 out={}
 for k,v in pairs:need(k not in out,'duplicate JSON field');out[k]=v
 return out
def read(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def emit(folder,name,d):(folder/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def safe(root,name):
 p=root/name;need(not Path(name).is_absolute() and '..' not in Path(name).parts and p.resolve().is_relative_to(root.resolve()),'unsafe input path');return p
def manifest(folder,expected):
 raw=(folder/'manifest.json').read_bytes();need(sha(raw)==expected,'immutable historical manifest identity');m=json.loads(raw,object_pairs_hook=unique);entries=m['files'];need(len(entries)==len({x['path'] for x in entries}),'historical file grain')
 actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()};need(actual=={x['path'] for x in entries}|{'manifest.json'},'historical package membership')
 for e in entries:
  b=safe(folder,e['path']).read_bytes();need(sha(b)==e['sha256'] and len(b)==e['bytes'] and ('git_blob_sha1' not in e or git(b)==e['git_blob_sha1']),'historical payload identity')
 return {'manifest_sha256':expected,'files_including_manifest':len(entries)+1,'all_payload_bytes_verified':True}
def validate_merge(d):
 need(d['schema_version']==1 and d['pr']==178 and d['merge']==MERGE and d['tree']==TREE,'actual merge identity')
 need(d['parents']==[BASE,HEAD] and d['reviewed_head']==HEAD and d['develop_at_verification']==MERGE and d['actual_merge_and_branch_verified'] is True,'actual ordered parents/head/develop')
 need(d['PR_gate_run']==40346532936 and d['merged_at']=='2026-10-26T15:36:21Z','actual merge/PR provenance')
 runs=d['postmerge_runs'];need(len(runs)==1 and runs[0]['id']==40350966050 and runs[0]['event']=='push' and runs[0]['head']==MERGE and runs[0]['status']=='in_progress' and runs[0]['created_at']=='2026-10-26T15:36:24Z','actual pending push identity')
 need(d['postmerge_status']=='Pending; PR artifacts are not relabelled.','pending boundary')
def load_engine(folder):
 path=folder/'original-preview/recompute_delta.py';module=types.ModuleType('immutable_preview_engine');exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__);return module

def prepare(a):
 histories={name:manifest(a.inputs/name,digest) for name,digest in MANIFESTS.items()}
 identity=read(a.inputs/'actual-merge-identity.json');need(sha((a.inputs/'actual-merge-identity.json').read_bytes())==IDENTITY_HASH,'actual merge receipt bytes');validate_merge(identity)
 v=load_engine(a.inputs);old_inputs=a.inputs/'original-preview/inputs';m=v.load_inputs(old_inputs);old_snapshot=v.source_snapshot(a.original_source_root,a.baseline_source_root,m);old_outputs=v.compute(m,old_snapshot)
 for name,d in old_outputs.items():need(d==read(a.inputs/'original-preview'/name),'immutable preview recomputation')
 tree=read(a.inputs/'fixed-head-tree.json');blobs=v.verify_tree(tree,TREE);need(len(blobs)==1379 and blobs.keys()==old_snapshot['blobs'].keys(),'corrected full source inventory')
 corrected_paths={p for p in blobs if blobs[p]['sha']!=old_snapshot['blobs'][p]['sha']};need(corrected_paths=={TEST},'only NumericDisplayLocaleTest repair')
 raw={}
 for p,e in blobs.items():
  b=v.safe(a.source_root,p).read_bytes();need(git(b)==e['sha'] and len(b)==e['size'],'actual raw source Git binding');raw[p]=b
 coverage_paths={x['path'] for x in old_snapshot['bindings']};need(len(coverage_paths)==176 and all(raw[p]==old_snapshot['raw'][p] for p in coverage_paths),'all 176 coverage inputs unchanged from preview')
 source_catalogues={p.relative_to(a.source_root).as_posix() for p in (a.source_root/'Paintroid/src/main/res').glob('values*/strings.xml')};need(len(source_catalogues)==174 and source_catalogues=={p for p in coverage_paths if p.endswith('/strings.xml')},'actual catalogue membership')
 base_blobs=v.verify_tree(m['base_tree'],v.BASE_TREE)
 full_delta=[{'path':p,'before':base_blobs.get(p,{}).get('sha'),'after':blobs.get(p,{}).get('sha'),'status':'added' if p not in base_blobs else 'removed' if p not in blobs else 'changed'} for p in sorted(base_blobs.keys()|blobs.keys()) if base_blobs.get(p,{}).get('sha')!=blobs.get(p,{}).get('sha')]
 need(len(full_delta)==13 and sum(x['status']=='added' for x in full_delta)==3 and all(not x['path'].startswith('Paintroid/src/main/') or x['path'] in v.LOCALES.values() for x in full_delta),'actual full 13-path base delta')
 actual=dict(old_snapshot,raw=raw,blobs=blobs,full_delta=full_delta)
 # Identity is rebound only after full historical/merge/tree/raw proofs above.
 # Neither historical files nor PR artifact receipts are relabelled or overwritten.
 v.SOURCE_COMMIT=MERGE;v.SOURCE_TREE=TREE;v.STATUS=STATUS
 outputs=v.compute(m,actual)
 for name,d in outputs.items():
  if isinstance(d,dict):d['current_production_replaced']=True;d['integration_identity_receipt']='inputs/actual-merge-identity.json'
 need(outputs['structural-per-locale.json']==old_outputs['structural-per-locale.json'],'actual merged rows equal original preview')
 profile=outputs['data-quality-profile.json'];profile['full_source_changed_or_added_paths']=13;profile['all_176_coverage_inputs_unchanged_from_preview']=True
 result=outputs['coverage-delta.json'];result['workflow_results']={'PR':178,'corrected_PR_run':40346532936,'corrected_PR_result':'completed success; separate premerge evidence','actual_postmerge_run':40350966050,'actual_postmerge_head':MERGE,'actual_postmerge_event':'push','actual_postmerge_status':'in_progress in supplied identity receipt','actual_postmerge_terminal_result':None,'PR_artifacts_are_not_postmerge_artifacts':True};result['original_preview_commit']=OLD_HEAD;result['original_preview_manifest_sha256']=MANIFESTS['original-preview'];result['actual_merge_receipt_sha256']=IDENTITY_HASH
 reconciliation=outputs['review-scope-reconciliation.json'];need(reconciliation['new_review_scopes']==old_outputs['review-scope-reconciliation.json']['new_review_scopes'],'review scope payload unchanged by test repair')
 failed=read(a.inputs/'original-failure/failure-analysis.json');need(failed['run_id']==40340230583 and failed['reviewed_head']==OLD_HEAD and failed['tree']==OLD_TREE and failed['junit_totals']=={'tests':1366,'failures':1,'errors':0,'skipped':0} and len(failed['failed_cases'])==1,'preserved original failure')
 pr=read(a.inputs/'corrected-PR-terminal/run-review-artifact-identity.json');need(pr['head']==HEAD and pr['base']==BASE and pr['tree']==TREE and pr['tested_tree_equal'] is True and pr['run']['id']==40346532936 and pr['run']['event']=='pull_request' and pr['run']['conclusion']=='success','corrected PR source/gate proof stays separate')
 reg=read(a.inputs/'corrected-PR-terminal/hosted-regression-verification.json');need(reg['run_id']==40346532936 and reg['reviewed_head']==HEAD and reg['junit_totals']=={'tests':1366,'failures':0,'errors':0,'skipped':0},'corrected PR regression result')
 numeric=[s for s in reg['focused_suites'] if s['class']=='NumericDisplayLocaleTest'];need(len(numeric)==1 and len(numeric[0]['cases'])==6 and all(c['passed'] is True for c in numeric[0]['cases']),'actual corrected numeric six')
 correction={'source_commit':MERGE,'source_tree':TREE,'source_status':STATUS,'original_preview_head':OLD_HEAD,'corrected_reviewed_head':HEAD,'original_preview_tree':OLD_TREE,'changed_paths_from_original_preview':[TEST],'before_blob':old_snapshot['blobs'][TEST]['sha'],'after_blob':blobs[TEST]['sha'],'before_sha256':sha(old_snapshot['raw'][TEST]),'after_sha256':sha(raw[TEST]),'unchanged_raw_blobs_from_preview':1378,'all_176_coverage_inputs_unchanged':True,'application_or_resource_changes_in_repair':0,'complete_source_delta_from_ce796_paths':13,'original_failed_run':40340230583,'original_failure_tests':1366,'original_failure_count':1,'corrected_PR_run':40346532936,'corrected_PR_JVM_tests':1366,'corrected_PR_JVM_failures':0,'corrected_PR_numeric_tests':6,'postmerge_terminal_status':'pending; no PR artifact relabel','diff':''.join(difflib.unified_diff(old_snapshot['raw'][TEST].decode().splitlines(True),raw[TEST].decode().splitlines(True),fromfile='original/'+TEST,tofile='corrected/'+TEST))}
 outputs['test-only-correction-provenance.json']=correction
 outputs['historical-package-bindings.json']={'source_commit':MERGE,'source_tree':TREE,'source_status':STATUS,'packages':histories,'corrected_PR_terminal_records_commit':'67a7dfe36e7f9652aa081ddcab7bb5e8aa062e44','original_failure_records_revision':'1984fd4','repair_records_commit':'79192cbafad86f7c582f357844efe8fb8cf7eb2e','original_preview_and_baseline_unchanged':True,'historical_PR_artifacts_not_relabelled':True,'actual_postmerge_terminal_proof_supplied':False,'GitHub_reported_signature_verification_supplied':{'verified':True,'reason':'valid','verified_at':'2026-10-26T15:36:21Z','classification':'Supplied GitHub-reported cryptographic verification; independent PGP validation not performed.'}}
 return outputs,v

def run(a):
 outputs,v=prepare(a);a.out.mkdir(parents=True,exist_ok=True)
 for name,d in outputs.items():emit(a.out,name,d)
 rows=outputs['structural-per-locale.json']
 with (a.out/'structural-per-locale.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 files=[v.file_binding(p,p.relative_to(a.inputs).as_posix()) for p in sorted(a.inputs.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
 emit(a.out,'input-bindings.json',{'source_commit':MERGE,'source_tree':TREE,'source_status':STATUS,'all_paths_are_public_roles_not_execution_locations':True,'files':files})
 print(json.dumps({'merge':MERGE,'pending_push_run':40350966050,'coverage_delta':outputs['coverage-delta.json']['presence_delta'],'full_source_delta_paths':13,'reviewed_pairs':110},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ('inputs','source-root','original-source-root','baseline-source-root','out'):p.add_argument('--'+name,type=Path,required=True)
 run(p.parse_args())
