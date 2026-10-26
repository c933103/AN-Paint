#!/usr/bin/env python3
"""Explicit current receipt mapping. Cannot emit while actual push evidence is pending."""
import argparse,collections,hashlib,json,re
from pathlib import Path
BASE='e5f2d4e2d07e678076f022aa7b3ef923e13c3721';HEAD='0824180c14ae979dc253f03d0fe628fbe9cf9b34';TREE='98b89d126533df3c0dbaeb729c74e4bcb44a3a8a';MERGE='e1e5433e63d45f5b76d39ce1a31ffc11fd7cd79d';RUN=40366731196;PR_RUN=40362410752
PR_MANIFEST='53f9b73c575fbc3dc1d5a0f82acbbd8ca79485c63fea09e7c4bfa016cb24cda1'
CHECKS={'Emulator API 35','Core emulator API 35','Position dialog API 35','Regression tests and lint','Build APK and corresponding source','Exact-script resource generation'}
FILES={'apk-source':'artifact-source-binding.json','compiled-values':'compiled-resource-verification.json','regression-lint':'hosted-regression-verification.json','exact-script':'exact-script-verification.json','api35':'api35-terminal-verification.json'}
PREFIX={'apk-source':'apk-and-source','regression-lint':'regression-and-lint','exact-script':'exact-script-generation','api35':'emulator-api-35'}
def need(ok,m):
 if not ok:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def read(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def safe(root,name):
 p=Path(name);need(not p.is_absolute() and '..' not in p.parts and '\\' not in name,'unsafe path');out=root/p;need(out.resolve().is_relative_to(root.resolve()),'escaped path');return out

def bind_manifest(root,expected,complete=True):
 raw=(root/'manifest.json').read_bytes();need(sha(raw)==expected,'immutable evidence manifest');m=read(root/'manifest.json');es=m['files'];need(len(es)==len({e['path'] for e in es}),'manifest grain')
 if complete:need({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}=={e['path'] for e in es}|{'manifest.json'},'complete evidence package inventory')
 for e in es:
  p=safe(root,e['path'])
  if not complete and not p.exists():continue
  b=p.read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'manifest payload hash')
 return m

def validate_payloads(d,arts,status,merge,prior):
 need(merge['actual_merge']==MERGE and merge['tree']==TREE and merge['parents']==[BASE,HEAD] and merge['reviewed_head']==HEAD and merge['develop_verified']==MERGE,'live actual merge identity')
 run=status['run'];need(run['id']==RUN and run['head_sha']==MERGE and run['event']=='push' and run['status']=='completed' and run['conclusion']=='success' and run['run_attempt']==1,'actual push terminal status')
 jobs=status['jobs'];need(len(jobs)==len({j['id'] for j in jobs})==6 and {j['name'] for j in jobs}==CHECKS and all(j['status']=='completed' and j['conclusion']=='success' for j in jobs),'six actual successful jobs')
 need(len(arts)==len({a['id'] for a in arts})==8,'eight actual artifact inventory');byid={a['id']:a for a in arts};need(set(byid).isdisjoint(a['id'] for a in prior['artifacts']),'PR artifacts cannot be postmerge')
 for a in arts:need(a['workflow_run']['id']==RUN and a['workflow_run']['head_sha']==MERGE and a['expired'] is False and re.fullmatch('sha256:[0-9a-f]{64}',a['digest']),'actual artifact workflow/digest')
 def artifact(identifier,digest,prefix):
  need(identifier in byid,'unknown artifact ID');a=byid[identifier];need(a['name']==prefix+'-'+MERGE and a['digest']=='sha256:'+digest,'artifact name/digest join')
 a=d['apk-source'];c=d['compiled-values'];r=d['regression-lint'];e=d['exact-script'];api=d['api35']
 for rec in (a,c,r):need(rec['run_id']==RUN and rec['tested_commit']==MERGE and rec['reviewed_head']==HEAD,'APK/compiled/regression identities')
 need(a['source_tree']==c['tree']==TREE,'APK/compiled tree');need(e['run_id']==RUN and e['source_commit']==MERGE and e['tree']==TREE and e['reviewed_pr_head']==HEAD,'exact-script identities');need(api['run_id']==RUN and api['workflow_head']==api['tested_commit']==MERGE and api['reviewed_pr_head']==HEAD and api['source_tree']==TREE,'API actual workflow/test identity')
 artifact(a['artifact_id'],a['archive_sha256'],PREFIX['apk-source']);artifact(r['artifact_id'],r['artifact_sha256'],PREFIX['regression-lint']);artifact(e['artifact_id'],e['archive_sha256'],PREFIX['exact-script']);artifact(api['artifact_id'],api['artifact_sha256'],PREFIX['api35'])
 build=a['build_info'];need(build['commit']==MERGE and build['run_id']==str(RUN) and build['build_variant']=='debug','actual build-info');need(a['tracked_files']==1382 and a['packaged_tracked_source_files_exact']==1379 and a['packager_exclusions']==['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore'] and a['embedded_source_matches_external'] is True and a['tracked_executable_modes_match'] is True,'source packaging verified')
 need(c['apk_sha256']==build['apk_sha256'] and c['new_reviewed_entries']==156 and c['prior_reviewed_entries']==392 and c['inherited_entries']==254 and c['new_reviewed_entries_by_locale']=={'sk':78,'sl':78} and c['inherited_entries_by_locale']=={'sk':127,'sl':127} and c['SK_SL_new_inherited_keys_disjoint'] is True,'compiled resource partition')
 entries=c['entries'];need(len(entries)==len({(x['locale'],x['identity']) for x in entries})==802 and all(x['exact_expected_display_match'] is True for x in entries),'802 exact compiled identities');need(entries==prior['compiled-values']['entries'],'same reviewed tree compiled-value equality');need(collections.Counter(x['scope'] for x in entries)=={'prior bounded review':392,'inherited preservation only':254,'new bounded SK/SL review':156},'compiled scope qualification');need(c['signature_exit']==0 and c['v1_verified'] is True and c['v2_verified'] is True,'actual CI debug signature')
 need(r['junit_files']==149 and r['junit_totals']=={'tests':1374,'failures':0,'errors':0,'skipped':0} and r['unique_junit_identities']==1374,'actual JVM inventory');need(r['lint_issues']==0 and r['lint_severities']==[] and set(r['phase_receipts'])=={'python','jvm','native','lint'} and all(x['exit_code']==0 for x in r['phase_receipts'].values()),'actual host/lint receipts')
 py=r['hosted_python'];need(py['run']==1408 and py['passed']==1406 and py['skipped']==2 and 'Not named' in py['skipped_identities'],'Python skips not passes');suites={x['class']:x for x in r['focused_suites']};need('SlovakSlovenianP0WordingTest' in suites and len(suites['SlovakSlovenianP0WordingTest']['cases'])==8,'new focused runtime suite');need(all(all(x['passed'] is True for x in s['cases']) for s in suites.values()),'focused cases pass')
 need(e['probe_count']==len(e['probes'])==13 and e['all_log_hashes_and_expected_exits_verified'] is True and sum(not x['expected_success'] for x in e['probes'])==1 and all((x['exit_code']==0)==x['expected_success'] for x in e['probes']),'exact-script positive and negative probes')
 device=api['composed_device_identity'];need(device['commit']==MERGE and device['run_id']==str(RUN) and device['device_sdk']==35 and device['apk_sha256']==build['apk_sha256'] and device['source_sha256']==build['source_sha256'],'API build/source composition')
 need(api['app_source_bound_selected']==api['app_source_bound_completed']==45 and sum(api['app_phases'].values())==45 and api['app_phases']==prior['api35']['app_phases'] and api['app_composed_validator_matches_original_except_separately_verified_identity'] is True,'app selected/completed45');need(api['native_source_bound_selected']==api['native_source_bound_completed']==74 and api['native_all_unique_case_identities_exact_match'] is True and api['native_missing_unexpected_errors']==[] and api['native_return_code']==0 and api['native_timed_out'] is False,'native selected/completed74')
 selection=api['artifact_selection'];need(selection['run_id']==RUN and selection['checkout']==selection['workflow_head']==MERGE and selection['device_sdk']==35 and selection['current_attempt']==1 and set(selection['selected'])=={'core','position'},'actual split API selection')
 for name,x in selection['selected'].items():artifact(x['artifact_id'],x['digest'].removeprefix('sha256:'),'emulator-'+name+'-api-35');need(x['job_id'] in {j['id'] for j in jobs} and x['job_record_run_attempt']==1,'split API job identity')
 need(any(x['name']=='instrumentation-apks-'+MERGE and x['digest']=='sha256:'+api['instrumentation_apks_archive_sha256'] for x in arts),'test APK artifact')
 return {'actual_merge':MERGE,'tree':TREE,'run_id':RUN,'compiled_new_reviewed':156,'compiled_prior_reviewed':392,'compiled_inherited_preservation_only':254,'JVM_tests':1374,'Python_passed':1406,'Python_unnamed_skips':2,'API35_app':45,'API35_native':74,'no_new_acceptance_from_CI':True}

def run(args):
 bind_manifest(args.pr_evidence,PR_MANIFEST,complete=False);bind_manifest(args.actual_evidence,args.actual_manifest_sha256)
 d={kind:read(args.actual_evidence/name) for kind,name in FILES.items()};prior={kind:read(args.pr_evidence/name) for kind,name in FILES.items()};prior['artifacts']=read(args.pr_evidence/'artifact-inventory.json');arts=read(args.actual_evidence/'artifact-inventory.json');status=read(args.status);merge=read(args.merge_identity);summary=validate_payloads(d,arts,status,merge,prior)
 envelope={'schema_version':1,'record_kind':'actual-postmerge-terminal','merge':{'sha':MERGE,'tree':TREE,'ordered_parents':[BASE,HEAD],'develop_at_verification':MERGE},'PR':{'number':179,'head':HEAD,'tree':TREE,'run_id':PR_RUN,'artifact_ids':[a['id'] for a in prior['artifacts']]},'run':{'id':RUN,'head':MERGE,'event':'push','status':'completed','conclusion':'success','attempt':1,'updated_at':status['run']['updated_at']},'checks':[dict(j,head=MERGE) for j in status['jobs']],'artifacts':[{'id':a['id'],'run_id':RUN,'head':MERGE,'expired':False,'sha256':a['digest'].removeprefix('sha256:')} for a in arts],'verified_receipts':{},'compiled_values':{'new_reviewed_sk':78,'new_reviewed_sl':78,'exact_new_reviewed':156},'new_linguistic_acceptances_due_to_CI':0,'native_human_layout_whole_language_release_certifications':0,'mapping_notes':{'compiled-values':'No artifact_id field is invented in receipt; actual APK/source artifact binds compiled receipt through equal run/tested commit/APK SHA.','regression-lint':'No tree field is invented in receipt; actual tested commit and workflow artifact head bind to independently verified merge tree.'},'actual_evidence_manifest_sha256':args.actual_manifest_sha256,'underlying_receipt_validation':summary}
 for kind,name in FILES.items():
  rec=d[kind];envelope['verified_receipts'][kind]={'run_id':RUN,'tested_commit':MERGE,'source_tree':TREE,'reviewed_pr_head':HEAD,'artifact_id':d['apk-source']['artifact_id'] if kind=='compiled-values' else rec['artifact_id'],'result':'pass','receipt_path':name,'receipt_sha256':sha((args.actual_evidence/name).read_bytes()),'identity_mapping':kind}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'coverage-terminal-envelope.json').write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ('pr-evidence','actual-evidence','status','merge-identity','out'):p.add_argument('--'+name,type=Path,required=True)
 p.add_argument('--actual-manifest-sha256',required=True);run(p.parse_args())
