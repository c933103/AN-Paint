"""Join actual postmerge terminal evidence to immutable source-bound coverage."""
import argparse,collections,csv,hashlib,json,types
from pathlib import Path
MERGE='e5f2d4e2d07e678076f022aa7b3ef923e13c3721';TREE='806d9577409c4044212d1c12e6e38da46417bae6';HEAD='82995ec1f030d23cb4e2b1426b511abe802890eb';BASE='ce796879f4568a27b9d905a8e8db639dd0a93a30';RUN=40350966050
PENDING='2d9942b85176f5a5536e33745677f723448fd48b5396ac96cab8ad964167588b';TERMINAL='e0a961d4e4f2d6c280836e308adfaf192bea43f7b8a19e2c3686c854ace63b8b'
TERMINAL_RECORD='4e9897b8c030c0ab785a34a69f2c872d2d9505d9'
TERMINAL_URL='https://github.com/c933103/AN-Paint/tree/'+TERMINAL_RECORD+'/records/localization-review/2026-10-26/catalan-romanian-p0-completion/r07-postmerge-terminal'
STATUS='integrated actual merge; actual postmerge push run 40350966050 completed successfully at 2026-10-26T16:00:53Z'
CHECKS={'Emulator API 35','Core emulator API 35','Position dialog API 35','Regression tests and lint','Build APK and corresponding source','Exact-script resource generation'}
FOCUSED={'CatalanRomanianCompletionWordingTest':5,'CatalanRomanianImportWordingTest':2,'CatalanRomanianSaveWordingTest':2,'DanishNorwegianP0Test':4,'DerivedExportStateTest':7,'ImportSelectionTitleTest':12,'NumericDisplayLocaleTest':6,'NynorskRemainingP0Test':4,'NynorskSaveWordingTest':2,'TaggedColourImportTest':5}
FILES=['run-merge-artifact-identity.json','artifact-source-binding.json','compiled-resource-verification.json','exact-script-verification.json','hosted-regression-verification.json','api35-terminal-verification.json','PR-versus-actual-merge.json']
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON field');d[k]=v
 return d
def read(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def emit(root,name,d):(root/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def manifest(root,expected):
 need(sha((root/'manifest.json').read_bytes())==expected,'immutable package manifest identity');d=read(root/'manifest.json');files=d['files'];need(len(files)==len({x['path'] for x in files}),'manifest identity grain');actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()};need(actual=={x['path'] for x in files}|{'manifest.json'},'immutable package membership')
 for x in files:
  p=root/x['path'];need(not Path(x['path']).is_absolute() and '..' not in Path(x['path']).parts and p.resolve().is_relative_to(root.resolve()),'manifest safe path');b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'] and git(b)==x['git_blob_sha1'],'immutable payload bytes')
 return d

def validate(d,prior,approved):
 i=d['run-merge-artifact-identity.json'];run=i['run'];need(i['merge']==MERGE and i['tree']==TREE and i['reviewed_pr_head']==HEAD and i['ordered_parents']==[BASE,HEAD] and i['develop_at_terminal_verification']==MERGE,'terminal merge/head/tree/parents/develop')
 need(run['id']==RUN and run['event']=='push' and run['head']==MERGE and run['status']=='completed' and run['conclusion']=='success' and run['attempt']==1 and run['updated_at']=='2026-10-26T16:00:53Z','actual terminal run/event/head/status')
 checks=i['checks'];need(len(checks)==6 and {c['name'] for c in checks}==CHECKS and len({c['id'] for c in checks})==6 and all(c['head']==MERGE and c['status']=='completed' and c['conclusion']=='success' for c in checks),'six actual merge checks')
 jobs=i['jobs'];need(len(jobs)==6 and {j['name'] for j in jobs}==CHECKS and all(j['status']=='completed' and j['conclusion']=='success' for j in jobs),'six actual terminal jobs')
 artifacts=i['artifacts'];need(len(artifacts)==8 and len({x['id'] for x in artifacts})==8,'actual artifact inventory');byid={x['id']:x for x in artifacts}
 def artifact(identifier,digest,prefix):
  need(identifier in byid,'artifact ID missing from actual run');a=byid[identifier];need(a['sha256']==digest and a['name']==prefix+'-'+MERGE and a['expired'] is False,'actual artifact digest/name binding')
 b=d['artifact-source-binding.json'];c=d['compiled-resource-verification.json'];e=d['exact-script-verification.json'];r=d['hosted-regression-verification.json'];a=d['api35-terminal-verification.json'];compare=d['PR-versus-actual-merge.json']
 for receipt in (b,c,r):need(receipt['run_id']==RUN and receipt['tested_commit']==MERGE and receipt['reviewed_head']==HEAD,'fresh build/compiled/regression identity')
 need(b['source_tree']==c['tree']==TREE and e['run_id']==a['run_id']==RUN and e['source_commit']==a['tested_commit']==a['workflow_head']==MERGE and e['tree']==a['source_tree']==TREE and e['reviewed_pr_head']==a['reviewed_pr_head']==HEAD,'fresh exact/API tree identities')
 artifact(b['artifact_id'],b['archive_sha256'],'apk-and-source');artifact(r['artifact_id'],r['artifact_sha256'],'regression-and-lint');artifact(e['artifact_id'],e['archive_sha256'],'exact-script-generation');artifact(a['artifact_id'],a['artifact_sha256'],'emulator-api-35')
 build=b['build_info'];need(build['commit']==MERGE and build['run_id']==str(RUN) and build['build_variant']=='debug','actual build-info identity')
 need(b['tracked_files']==1379 and b['packaged_tracked_source_files_exact']==1376 and b['packager_exclusions']==['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore'] and b['embedded_source_matches_external'] is True,'actual packaged source counts/exclusions')
 need(c['apk_sha256']==build['apk_sha256'] and c['new_reviewed_entries']==110 and c['prior_reviewed_entries']==282 and c['new_reviewed_entries_by_locale']=={'ca':55,'ro':55} and c['prior_reviewed_entries_by_locale']=={'ca':23,'ro':23,'da':78,'no':78,'nn':80} and c['CA_RO_new_prior_keys_disjoint'] is True,'compiled source/110+282 partition')
 entries=c['entries'];pairs={(x['locale'],x['identity']):x for x in entries};need(len(entries)==len(pairs)==392 and all(x['exact_approved_display_match'] is True for x in entries),'compiled exact-pair grain')
 need(entries==prior['compiled-resource-verification.json']['entries'],'compiled actual/prior source-bound fixture equality')
 for x in approved['values']:need(pairs[(x['locale'],x['identity'])]['display_sha256']==x['final_value_sha256_utf8'],'new reviewed compiled fixture hash')
 need(c['signature_exit']==0 and c['v1_verified'] is True and c['v2_verified'] is True,'CI debug APK signature checks')
 need(r['junit_files']==148 and r['junit_totals']=={'tests':1366,'failures':0,'errors':0,'skipped':0} and r['unique_junit_identities']==1366,'fresh actual JVM inventory/result')
 suites=r['focused_suites'];need(len(suites)==10 and {s['class']:len(s['cases']) for s in suites}==FOCUSED and all(s['source_test_methods']==FOCUSED[s['class']] and all(x['passed'] is True for x in s['cases']) and len({x['name'] for x in s['cases']})==len(s['cases']) for s in suites),'ten actual source-focused suites')
 py=r['hosted_python'];need(py['run']==1398 and py['passed']==1396 and py['skipped']==2 and py['run']==py['passed']+py['skipped'] and py['seconds']==267.641 and py['skipped_identities']=='Not named in non-verbose hosted terminal summary; not guessed from source or local results.','hosted Python actual skips remain distinct')
 need(r['lint_issues']==0 and r['lint_severities']==[] and set(r['phase_receipts'])=={'python','jvm','native','lint'} and all(x['exit_code']==0 for x in r['phase_receipts'].values()),'actual lint/phase receipts')
 need(e['probe_count']==len(e['probes'])==13 and len({x['name'] for x in e['probes']})==13 and e['all_log_hashes_and_expected_exits_verified'] is True and all((x['exit_code']==0)==x['expected_success'] for x in e['probes']) and sum(not x['expected_success'] for x in e['probes'])==1,'13 source generation probes including expected rejection')
 device=a['composed_device_identity'];need(device['commit']==MERGE and device['run_id']==str(RUN) and device['device_sdk']==35 and device['apk_sha256']==build['apk_sha256'] and device['source_sha256']==build['source_sha256'],'actual composed device source/build identity')
 priorapi=prior['api35-terminal-verification.json'];need(device['source_tests_sha256']==priorapi['composed_device_identity']['source_tests_sha256'] and a['native_source_tests_sha256']==priorapi['native_source_tests_sha256'],'source-bound API fixture identities unchanged')
 need(a['app_source_bound_selected']==a['app_source_bound_completed']==45 and sum(a['app_phases'].values())==45 and a['app_phases']==priorapi['app_phases'] and a['app_composed_validator_matches_original_except_separately_verified_identity'] is True,'exact app API35 selection/phases')
 need(a['native_source_bound_selected']==a['native_source_bound_completed']==74 and a['native_all_unique_case_identities_exact_match'] is True and a['native_missing_unexpected_errors']==[] and a['native_return_code']==0 and a['native_timed_out'] is False,'exact native API35 selection/outcome')
 selection=a['artifact_selection'];need(selection['run_id']==RUN and selection['checkout']==selection['workflow_head']==MERGE and selection['device_sdk']==35 and selection['current_attempt']==1 and set(selection['selected'])=={'core','position'},'actual composed selection identity')
 for name,rec in selection['selected'].items():artifact(rec['artifact_id'],rec['digest'].removeprefix('sha256:'),'emulator-'+name+'-api-35');need(rec['job_record_run_attempt']==1 and rec['job_id'] in {j['id'] for j in jobs},'selected artifact job/attempt')
 need(any(x['name']=='instrumentation-apks-'+MERGE and x['sha256']==a['instrumentation_apks_archive_sha256'] for x in artifacts),'instrumentation APK artifact join')
 need(compare['PR_run']==40346532936 and compare['actual_push_run']==RUN and compare['actual_merge']==MERGE and compare['tree']==TREE and compare['compiled_392_entries_exactly_equal'] is True and compare['fresh_actual_push_and_artifact_ids_distinct'] is True and compare['same_source_zip_sha256']==build['source_sha256'] and compare['actual_apk_sha256']==build['apk_sha256'] and compare['PR_apk_sha256']!=compare['actual_apk_sha256'],'PR versus actual artifact separation')
 need({x['artifact_id'] for x in (b,r,e,a)}.isdisjoint({prior[f]['artifact_id'] for f in ('artifact-source-binding.json','hosted-regression-verification.json','exact-script-verification.json','api35-terminal-verification.json')}),'fresh artifact IDs not reused PR artifacts')
 return {'run':run,'successful_checks':checks,'source_files':{'tracked':1379,'packaged_exact':1376,'explicit_exclusions':b['packager_exclusions'],'additional_members_counted_not_Git_authenticated':b['non_git_bound_extra_members']},'compiled_values':{'total':392,'new_reviewed':110,'prior_reviewed':282},'JVM':r['junit_totals'],'JVM_XML_files':148,'source_focused_suites':10,'hosted_Python':py,'lint_issues':0,'API35':{'app_selected_completed':45,'native_selected_completed':74,'scope':a['limits']},'exact_script_probes':13,'APK_sha256':build['apk_sha256'],'source_ZIP_sha256':build['source_sha256'],'fresh_artifact_ids':[x['artifact_id'] for x in (b,r,e,a)],'GitHub_reported_signature':i['github_reported_signature_verification'],'monitor_closed':True}

def prepare(a):
 pending=a.inputs/'integrated-pending';terminal=a.inputs/'actual-terminal';pm=manifest(pending,PENDING);tm=manifest(terminal,TERMINAL);need(len(pm['files'])==174 and len(tm['files'])==8,'175 pending /9 terminal inventories')
 docs={n:read(terminal/n) for n in FILES};oldpr=pending/'inputs/corrected-PR-terminal';prior={n:read(oldpr/n) for n in ('artifact-source-binding.json','compiled-resource-verification.json','exact-script-verification.json','hosted-regression-verification.json','api35-terminal-verification.json')};approved=read(pending/'inputs/original-preview/inputs/approved-manifest.json');status=validate(docs,prior,approved)
 engine=types.ModuleType('immutable_pending_engine');path=pending/'recompute_integrated.py';exec(compile(path.read_bytes(),str(path),'exec'),engine.__dict__)
 args=argparse.Namespace(inputs=pending/'inputs',source_root=a.source_root,original_source_root=a.original_source_root,baseline_source_root=a.baseline_source_root);recomputed,_=engine.prepare(args)
 for name,d in recomputed.items():need(d==read(pending/name),'current source/scopes differ from immutable integrated snapshot')
 outputs={};copy_names=('coverage-delta.json','review-scope-reconciliation.json','data-quality-profile.json','source-bindings.json','full-source-delta.json')
 for name in copy_names:
  d=read(pending/name);d['source_status']=STATUS;d['historical_pending_input']='inputs/integrated-pending/'+name;d['historical_pending_sha256']=sha((pending/name).read_bytes());outputs[name]=d
 rows=read(pending/'structural-per-locale.json');need(len(rows)==171,'terminal current option denominator');outputs['structural-per-locale.json']=rows
 delta=outputs['coverage-delta.json'];delta['workflow_results']={'PR':178,'corrected_PR_run':40346532936,'corrected_PR_result':'historical separate success','actual_postmerge_run':RUN,'actual_postmerge_head':MERGE,'actual_postmerge_event':'push','actual_postmerge_status':'completed','actual_postmerge_terminal_result':'success','actual_postmerge_updated_at':'2026-10-26T16:00:53Z','PR_artifacts_are_not_postmerge_artifacts':True};delta['terminal_record_commit']=TERMINAL_RECORD;delta['terminal_record_url']=TERMINAL_URL;delta['terminal_evidence_manifest_sha256']=TERMINAL;delta['terminal_status_supplement']='terminal-status-supplement.json'
 need(outputs['review-scope-reconciliation.json']['new_review_scopes']==read(pending/'review-scope-reconciliation.json')['new_review_scopes'],'no linguistic expansion on terminal success')
 outputs['terminal-status-supplement.json']={'schema_version':1,'source_commit':MERGE,'source_tree':TREE,'status':STATUS,'terminal_record_commit':TERMINAL_RECORD,'terminal_record_url':TERMINAL_URL,'terminal_evidence_manifest_sha256':TERMINAL,'historical_pending_manifest_sha256':PENDING,'historical_pending_175_files_preserved':True,'original_failed_PR_and_corrected_PR_evidence_preserved':True,'terminal_join':status,'coverage_counts_unchanged':True,'review_scopes_unchanged':True,'new_linguistic_acceptances_due_to_CI':0,'new_native_human_layout_whole_language_or_release_certifications':0,'global_linguistic_accepted_count':None,'new_Valencian_direct_acceptance':0,'limitations':['CI artifacts are fresh actual-merge artifacts; this wrapper joins already-verified receipts and recomputes current source coverage, not a new CI run.','Hosted Python skips are unnamed in the non-verbose summary; they are retained rather than guessed or treated as passes.','Existing API35 emulator coverage is not locale-specific physical-device, layout or native-human certification.','Debug APK signing is not private upgrade signing or a release. All existing scope/hold qualifications remain unchanged.']}
 return outputs,docs,prior,approved

def run(a):
 outputs,docs,prior,approved=prepare(a);a.out.mkdir(parents=True,exist_ok=True)
 for n,d in outputs.items():emit(a.out,n,d)
 rows=outputs['structural-per-locale.json']
 with (a.out/'structural-per-locale.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 bindings=[]
 for path in sorted(a.inputs.rglob('*')):
  if path.is_file():b=path.read_bytes();bindings.append({'path':path.relative_to(a.inputs).as_posix(),'bytes':len(b),'sha256':sha(b),'git_blob_sha1':git(b)})
 emit(a.out,'input-bindings.json',{'source_commit':MERGE,'source_tree':TREE,'status':STATUS,'files':bindings,'all_paths_public_roles_not_execution_locations':True});print(json.dumps({'source_commit':MERGE,'run':RUN,'result':'success','checks':6,'new_review_scopes_due_to_terminal_CI':0,'scope_values_preserved':110,'hosted_Python_passed':1396,'hosted_Python_unnamed_skips':2},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ('inputs','source-root','original-source-root','baseline-source-root','out'):p.add_argument('--'+name,type=Path,required=True)
 run(p.parse_args())
