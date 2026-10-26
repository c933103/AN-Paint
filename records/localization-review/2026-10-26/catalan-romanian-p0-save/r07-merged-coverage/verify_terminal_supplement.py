"""Validate supplied actual-merge terminal receipts; no polling, execution or new review judgment."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

SOURCE='6a42948a3ac7bad241d502f3b6c18ebf1c0327d8'
TREE='65afa7b96a83c08e0ae08365166dec0520694356'
HEAD='a365f4b552448803c0bb48b3c44cdf508550eaf9'
RUN=40311048893
PENDING_MANIFEST='a52598bf8ef983a2016a7e8f0fab6e6843cf368bb7f4ea6cd708e6be6ceabe7b'
TERMINAL_RECORD='e9fbc0899ec952b1b5ae95cafb98a4b40f7c5ef8'
RECORD_URL='https://github.com/c933103/AN-Paint/tree/'+TERMINAL_RECORD+'/records/localization-review/2026-10-26/catalan-romanian-p0-save/r06-postmerge-terminal'
NAMES=('terminal-gates.json','hosted-regression-verification.json','api35-terminal-verification.json','artifact-source-binding.json','compiled-resource-verification.json','exact-script-verification.json')
CHECKS={'Emulator API 35','Core emulator API 35','Position dialog API 35','Build APK and corresponding source','Exact-script resource generation','Regression tests and lint'}

def require(ok,message):
    if not ok:raise ValueError(message)

def unique(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result

def load(path):return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def binding(root,path):
    raw=(root/path).read_bytes()
    return {'path':path,'bytes':len(raw),'sha256':sha(raw),'git_blob_sha1':blob(raw)}
def integer(value,expected,message):require(type(value) is int and value==expected,message)

def derive(root):
    pending=root/'integrated-pending'
    raw=(pending/'manifest.json').read_bytes()
    require(sha(raw)==PENDING_MANIFEST,'historical pending manifest changed')
    manifest=load(pending/'manifest.json')
    require(len(manifest['files'])==16 and len({f['path'] for f in manifest['files']})==16,'pending file inventory')
    for record in manifest['files']:
        require(Path(record['path']).name==record['path'],'unsafe pending filename')
        require(binding(pending,record['path'])==record,'historical pending payload changed')
    history=load(pending/'source-identity.json')
    require(history['source_commit']==SOURCE and history['source_tree']==TREE and history['run']['id']==RUN and history['run']['status']=='in_progress' and history['run']['conclusion'] is None,'pending observation changed')
    coverage=load(pending/'coverage-delta.json')
    scopes=load(pending/'review-scope-reconciliation.json')
    require(coverage['source_commit']==SOURCE and coverage['source_tree']==TREE and scopes['global_accepted_count'] is None,'coverage source/scope')
    for filename in ('structural-per-locale.csv','structural-per-locale.json'):
        require((root/filename).read_bytes()==(pending/filename).read_bytes(),'convenience table differs from preserved computation')
    documents={name:load(root/'terminal-evidence'/name) for name in NAMES}
    gate,jvm,api,apk,compiled,exact=(documents[name] for name in NAMES)
    for doc in documents.values():integer(doc['schema_version'],1,'receipt schema')
    require(gate['source_commit']==SOURCE and gate['source_tree']==TREE and gate['reviewed_pr_head']==HEAD and gate['pr']==176,'terminal gate source identity')
    run=gate['run'];integer(run['id'],RUN,'actual merge run')
    require(run['head']==SOURCE and run['event']=='push' and run['status']=='completed' and run['conclusion']=='success','terminal actual merge run outcome')
    require(run['updated_at']=='2026-10-26T11:19:16Z' and run['run_attempt']==1,'terminal timestamp/attempt')
    require(gate['explicit_develop_at_terminal']==SOURCE and gate['source_snapshot_pinned'] is True,'terminal develop pin')
    require(len(gate['checks'])==len({c['id'] for c in gate['checks']})==6 and {c['name'] for c in gate['checks']}==CHECKS,'six exact checks')
    checks={c['id']:c for c in gate['checks']}
    require(len(gate['jobs'])==len({j['id'] for j in gate['jobs']})==6,'six unique jobs')
    for collection in ('checks','jobs'):
        for item in gate[collection]:
            require(item['head_sha']==SOURCE and item['status']=='completed' and item['conclusion']=='success','stale or failed terminal check/job')
            require(item['id'] in checks and checks[item['id']]['name']==item['name'],'job/check identity mismatch')
    artifacts={a['id']:a for a in gate['artifacts']}
    require(len(artifacts)==len(gate['artifacts']) and all(a['expired'] is False for a in artifacts.values()),'artifact inventory')
    for doc,source_field,head_field,hash_field in ((jvm,'tested_commit','reviewed_head','artifact_sha256'),(api,'tested_commit','reviewed_pr_head','artifact_sha256'),(apk,'tested_commit','reviewed_head','archive_sha256'),(exact,'source_commit','reviewed_pr_head','archive_sha256')):
        integer(doc['run_id'],RUN,'artifact receipt run')
        require(doc[source_field]==SOURCE and doc[head_field]==HEAD,'artifact receipt source')
        artifact=artifacts[doc['artifact_id']]
        require(artifact['digest']=='sha256:'+doc[hash_field] and SOURCE in artifact['name'],'artifact digest/name join')
    require(jvm['junit_totals']=={'tests':1358,'failures':0,'errors':0,'skipped':0} and jvm['unique_junit_identities']==1358 and jvm['junit_files']==146,'JVM receipt totals')
    py=jvm['hosted_python']
    require((py['run'],py['passed'],py['skipped'])==(1381,1379,2) and py['passed']+py['skipped']==py['run'],'hosted Python totals/skip distinction')
    require(py['skipped_identities']=='Not named in non-verbose hosted terminal summary; not guessed from source or local results.','unknown hosted skip identities must not be fabricated')
    require(jvm['lint_issues']==0 and jvm['lint_severities']==[] and all(r['exit_code']==0 for r in jvm['phase_receipts'].values()),'lint/phase outcomes')
    focused={s['class']:s for s in jvm['focused_suites']}
    require(len(focused)==len(jvm['focused_suites']) and {'CatalanRomanianSaveWordingTest','DerivedExportStateTest'}<=focused.keys(),'focused suite inventory')
    for suite in focused.values():
        require(len(suite['cases'])==suite['source_test_methods'] and len({c['name'] for c in suite['cases']})==len(suite['cases']) and all(c['passed'] is True for c in suite['cases']),'focused real test results')
    require(api['source_tree']==TREE and api['workflow_head']==SOURCE,'API35 source')
    require(api['app_source_bound_selected']==api['app_source_bound_completed']==sum(api['app_phases'].values())==45,'API35 app selected/completed counts')
    require(api['native_source_bound_selected']==api['native_source_bound_completed']==74 and api['native_all_unique_case_identities_exact_match'] is True and api['native_missing_unexpected_errors']==[] and api['native_return_code']==0 and api['native_timed_out'] is False,'API35 native completion')
    device=api['composed_device_identity'];build=apk['build_info']
    require(device['commit']==build['commit']==SOURCE and device['run_id']==build['run_id']==str(RUN) and device['device_sdk']==35,'composed device/build identity')
    require(device['apk_sha256']==build['apk_sha256'] and device['source_sha256']==build['source_sha256'],'APK/source artifact composition')
    selection=api['artifact_selection']
    require(selection['run_id']==RUN and selection['checkout']==selection['workflow_head']==SOURCE and selection['device_sdk']==35,'device selection source')
    require(set(selection['selected'])=={'core','position'},'device lane inventory')
    for lane in selection['selected'].values():
        require(lane['artifact_id'] in artifacts and artifacts[lane['artifact_id']]['digest']==lane['digest'] and lane['job_id'] in checks and lane['job_record_run_attempt']==1,'device lane artifact/job join')
    instrumentation=[a for a in artifacts.values() if a['name'].startswith('instrumentation-apks-')]
    require(len(instrumentation)==1 and instrumentation[0]['digest']=='sha256:'+api['instrumentation_apks_archive_sha256'],'instrumentation artifact hash')
    require(apk['source_tree']==TREE and apk['tracked_files']==1373 and apk['packaged_tracked_source_files_exact']==1370 and len(apk['packager_exclusions'])==3 and apk['embedded_source_matches_external'] is True,'source archive identity')
    require(compiled['run_id']==RUN and compiled['reviewed_head']==HEAD and compiled['tested_commit']==SOURCE and compiled['tree']==TREE and compiled['apk_sha256']==build['apk_sha256'],'compiled APK/source join')
    require(compiled['new_reviewed_entries']==20 and compiled['prior_reviewed_entries']==236 and compiled['reviewed_entries_by_locale']=={'ca':10,'ro':10,'da':78,'no':78,'nn':80},'bounded compiled scope')
    entries={(e['locale'],e['identity']):e for e in compiled['entries']}
    require(len(entries)==len(compiled['entries'])==256 and all(e['exact_approved_display_match'] is True for e in entries.values()),'compiled entry inventory')
    require(dict(Counter(e['locale'] for e in entries.values()))==compiled['reviewed_entries_by_locale'],'compiled locale grain')
    new={(e['locale'],e['identity']):e for e in scopes['new_review_scopes']}
    require(len(new)==20 and {p for p in entries if p[0] in ('ca','ro')}==set(new),'compiled/new-review exact pair join')
    for pair,entry in new.items():require(entries[pair]['display_sha256']==entry['display_sha256'],'compiled/new-review display hash')
    require(compiled['signature_exit']==0 and compiled['v1_verified'] is True and compiled['v2_verified'] is True,'APK CI signature verification')
    require(exact['tree']==TREE and exact['probe_count']==len(exact['probes'])==13 and len({p['name'] for p in exact['probes']})==13 and exact['all_log_hashes_and_expected_exits_verified'] is True,'exact-script probe inventory')
    for probe in exact['probes']:
        require((probe['exit_code']==0)==probe['expected_success'] and bool(re.fullmatch('[0-9a-f]{64}',probe['log_sha256'])),'exact-script expected result/hash')
    rejected=[p['name'] for p in exact['probes'] if not p['expected_success']]
    require(rejected==['06-reserved-app-variant-rejected'],'deliberate rejection preserved')
    return {'schema_version':1,'source_commit':SOURCE,'source_tree':TREE,'status':'integrated source; actual postmerge CI completed successfully','terminal_record_commit':TERMINAL_RECORD,'terminal_record_url':RECORD_URL,
        'terminal_record_manifest_sha256':'082b76f865222e352907cde53dca16958b63d195c91589a7484ebeceaa60373e',
        'run':run,'successful_exact_merge_checks':[{'id':c['id'],'name':c['name']} for c in gate['checks']],
        'historical_pending_manifest':binding(root,'integrated-pending/manifest.json'),'historical_pending_observation_retained_unchanged':True,
        'terminal_receipt_bindings':[binding(root,'terminal-evidence/'+name) for name in NAMES],
        'structural_tables':[binding(root,name) for name in ('structural-per-locale.csv','structural-per-locale.json')],
        'coverage_totals_unchanged':coverage['presence_totals'],'locales_after':coverage['locales_after'],'missingness_qualifications':coverage['remaining_missing_P0_classification'],
        'test_outcomes':{'JVM':jvm['junit_totals'],'hosted_Python':py,'lint_issues':jvm['lint_issues'],'API35_app_completed':45,'API35_native_completed':74,'exact_script_probes':13,'deliberate_exact_script_rejections':rejected,'new_compiled_values':20,'prior_compiled_values':236},
        'linguistic_scope_change':False,'global_accepted_count':None,'new_native_human_physical_device_layout_release_or_whole_language_certification':False,
        'limits':'This supplement joins supplied exact actual-merge terminal receipts; it does not rerun CI, re-extract APKs or add linguistic acceptance. The preserved pending snapshot contains the validated arithmetic, original qualifications and 62 historical controls. Its pending observation is not rewritten. Hosted Python skips remain two unnamed skips; local/optimized results are not substituted.'}

def run(root,write=False):
    expected=derive(root)
    path=root/'terminal-status-supplement.json'
    if write:path.write_text(json.dumps(expected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    require(load(path)==expected,'terminal supplement differs from exact supplied evidence')
    return {'schema_version':1,'source_commit':SOURCE,'source_tree':TREE,'run_id':RUN,'actual_merge_terminal_receipts_verified':6,'checks_jobs_joined':6,'new_review_compiled_pairs_joined':20,'historical_pending_payload_files_plus_manifest_byte_preserved':17,'convenience_tables_byte_identical':True,'stable_arithmetic_rerun':False,'source_or_external_changes':False,'no_new_linguistic_acceptance':True}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report-root',type=Path,required=True);p.add_argument('--write',action='store_true');a=p.parse_args()
    result=run(a.report_root,a.write)
    (a.report_root/'terminal-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
