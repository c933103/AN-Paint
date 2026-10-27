"""Validate supplied actual-merge terminal receipts; no polling, execution or new review judgment."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

SOURCE='ce796879f4568a27b9d905a8e8db639dd0a93a30'
TREE='f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c'
HEAD='10acbff912812b938bf2626be1e8a9e84e7aa7bc'
RUN=40327501312
PENDING_MANIFEST='070bca0f14f94c46d415e58749e9503e563eac12a0a910ebc46fb22700105a04'
TERMINAL_RECORD='c094a1b7bffdce01dd0ae6a7ab51f0d165fd2ffe'
RECORD_URL='https://github.com/c933103/AN-Paint/tree/'+TERMINAL_RECORD+'/records/localization-review/2026-10-26/catalan-romanian-p0-import/r07-postmerge-terminal'
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
    require(len(manifest['files'])==24 and len({f['path'] for f in manifest['files']})==24,'pending file inventory')
    for record in manifest['files']:
        require(Path(record['path']).name==record['path'],'unsafe pending filename')
        require(binding(pending,record['path'])==record,'historical pending payload changed')
    history=load(pending/'source-identity.json')
    require(history['merge_commit']==SOURCE and history['source_tree']==TREE and history['actual_postmerge_run']==RUN and history['actual_postmerge_status']=='pending at this identity record; terminal results separate','pending observation changed')
    coverage=load(pending/'coverage-delta.json')
    scopes=load(pending/'review-scope-reconciliation.json')
    require(coverage['source_commit']==SOURCE and coverage['source_tree']==TREE and scopes['global_accepted_count'] is None,'coverage source/scope')
    for filename in ('structural-per-locale.csv','structural-per-locale.json'):
        require((root/filename).read_bytes()==(pending/filename).read_bytes(),'convenience table differs from preserved computation')
    documents={name:load(root/'terminal-evidence'/name) for name in NAMES}
    gate,jvm,api,apk,compiled,exact=(documents[name] for name in NAMES)
    for doc in documents.values():integer(doc['schema_version'],1,'receipt schema')
    require(gate['source_snapshot']==SOURCE and gate['source_moved_since_pin'] is False,'terminal gate source identity')
    run=gate['run'];integer(run['id'],RUN,'actual merge run')
    require(run['head_sha']==SOURCE and run['event']=='push' and run['status']=='completed' and run['conclusion']=='success','terminal actual merge run outcome')
    require(run['updated_at']=='2026-10-26T13:25:59Z' and run['run_attempt']==1,'terminal timestamp/attempt')
    require(gate['develop_observed']==SOURCE and gate['source_snapshot']==SOURCE,'terminal develop pin')
    require(len(gate['checks'])==len({c['id'] for c in gate['checks']})==6 and {c['name'] for c in gate['checks']}==CHECKS,'six exact checks')
    checks={c['id']:c for c in gate['checks']}
    require(len(gate['jobs'])==len({j['id'] for j in gate['jobs']})==6,'six unique jobs')
    for collection in ('checks','jobs'):
        for item in gate[collection]:
            if collection=='checks':require(item['head_sha']==SOURCE,'stale terminal check source')
            require(item['status']=='completed' and item['conclusion']=='success','failed terminal check/job')
            require(item['id'] in checks and checks[item['id']]['name']==item['name'],'job/check identity mismatch')
    artifacts={a['id']:a for a in gate['artifacts']}
    require(len(artifacts)==len(gate['artifacts']) and all(a['expired'] is False for a in artifacts.values()),'artifact inventory')
    for doc,source_field,head_field,hash_field in ((jvm,'tested_commit','reviewed_head','artifact_sha256'),(api,'tested_commit','reviewed_pr_head','artifact_sha256'),(apk,'tested_commit','reviewed_head','archive_sha256'),(exact,'source_commit','reviewed_pr_head','archive_sha256')):
        integer(doc['run_id'],RUN,'artifact receipt run')
        require(doc[source_field]==SOURCE and doc[head_field]==HEAD,'artifact receipt source')
        artifact=artifacts[doc['artifact_id']]
        require(artifact['digest']=='sha256:'+doc[hash_field] and SOURCE in artifact['name'],'artifact digest/name join')
    require(jvm['junit_totals']=={'tests':1361,'failures':0,'errors':0,'skipped':0} and jvm['unique_junit_identities']==1361 and jvm['junit_files']==147,'JVM receipt totals')
    py=jvm['hosted_python']
    require((py['run'],py['passed'],py['skipped'])==(1389,1387,2) and py['passed']+py['skipped']==py['run'],'hosted Python totals/skip distinction')
    require(py['skipped_identities']=='Not named in non-verbose hosted terminal summary; not guessed from source or local results.','unknown hosted skip identities must not be fabricated')
    require(jvm['lint_issues']==0 and jvm['lint_severities']==[] and all(r['exit_code']==0 for r in jvm['phase_receipts'].values()),'lint/phase outcomes')
    focused={s['class']:s for s in jvm['focused_suites']}
    require(len(focused)==len(jvm['focused_suites']) and {'CatalanRomanianImportWordingTest','CatalanRomanianSaveWordingTest','TaggedColourImportTest'}<=focused.keys() and len(focused)==8,'focused suite inventory')
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
    require(apk['source_tree']==TREE and apk['tracked_files']==1376 and apk['packaged_tracked_source_files_exact']==1373 and len(apk['packager_exclusions'])==3 and apk['embedded_source_matches_external'] is True,'source archive identity')
    require(compiled['run_id']==RUN and compiled['reviewed_head']==HEAD and compiled['tested_commit']==SOURCE and compiled['tree']==TREE and compiled['apk_sha256']==build['apk_sha256'],'compiled APK/source join')
    require(compiled['new_reviewed_entries']==26 and compiled['prior_reviewed_entries']==256 and compiled['reviewed_entries_by_locale']=={'ca':23,'ro':23,'da':78,'no':78,'nn':80} and compiled['new_reviewed_entries_by_locale']=={'ca':13,'ro':13} and compiled['prior_reviewed_entries_by_locale']=={'ca':10,'ro':10,'da':78,'no':78,'nn':80} and compiled['CA_RO_new_prior_keys_disjoint'] is True,'bounded compiled scope')
    entries={(e['locale'],e['identity']):e for e in compiled['entries']}
    require(len(entries)==len(compiled['entries'])==282 and all(e['exact_approved_display_match'] is True for e in entries.values()),'compiled entry inventory')
    require(dict(Counter(e['locale'] for e in entries.values()))==compiled['reviewed_entries_by_locale'],'compiled locale grain')
    new={(e['locale'],e['identity']):e for e in scopes['new_review_scopes']}
    prior_save={'string/'+key for key in ('ui_your_current_image_has_unsaved_changes','ui_could_not_save_image','ui_saved','ui_export_did_not_save23','ui_save_explanation23','ui_export_explanation23','ui_share_explanation34','ui_save_and_share','ui_save_and_share_41edb4','ui_the_image_was_saved_but_android_could_not')}
    prior_pairs={(tag,key) for tag in ('ca','ro') for key in prior_save}
    require(len(new)==26 and set(new).isdisjoint(prior_pairs) and {p for p in entries if p[0] in ('ca','ro')}==set(new)|prior_pairs,'compiled/new-review disjoint pair join')
    for pair,entry in new.items():require(entries[pair]['display_sha256']==entry['display_sha256'],'compiled/new-review display hash')
    require(compiled['signature_exit']==0 and compiled['v1_verified'] is True and compiled['v2_verified'] is True,'APK CI signature verification')
    require(exact['tree']==TREE and exact['probe_count']==len(exact['probes'])==13 and len({p['name'] for p in exact['probes']})==13 and exact['all_log_hashes_and_expected_exits_verified'] is True,'exact-script probe inventory')
    for probe in exact['probes']:
        require((probe['exit_code']==0)==probe['expected_success'] and bool(re.fullmatch('[0-9a-f]{64}',probe['log_sha256'])),'exact-script expected result/hash')
    rejected=[p['name'] for p in exact['probes'] if not p['expected_success']]
    require(rejected==['06-reserved-app-variant-rejected'],'deliberate rejection preserved')
    inherited=[c for c in focused['TaggedColourImportTest']['cases'] if c['name']=='everyOfferedLanguageResolvesItsScopedMessageOrExplicitEnglishFallback']
    require(len(inherited)==1 and inherited[0]['passed'] is True,'actual postmerge inherited-value oracle pass')
    structural=coverage['single_selected_key_structural_presence'];prior_runtime=coverage['separate_runtime_resolution_qualification']
    require(structural['target_value_present_options']==70 and structural['target_value_absent_options']==101 and prior_runtime['direct_catalogue_options']==70 and prior_runtime['parent_inherited_options']==1 and prior_runtime['English_default_options']==100 and prior_runtime['new_Valencian_review_acceptance'] is False,'structural/runtime/linguistic partition preservation')
    runtime={'identity':'string/save20_unsupported_image_colour','direct_catalogue_options':70,'parent_inherited_options':1,'English_default_options':100,'parent_inherited_map':{'ca-ES-valencia':'ca'},'actual_postmerge_oracle_pass_verified':True,'run_id':RUN,'test':inherited[0]['name'],'new_Valencian_review_acceptance':False,'original_failed_and_successful_PR_proofs_retained_unchanged':True}
    # Authenticate the complete supplied terminal package after semantic joins, without rewriting its metadata.
    terminal_manifest_path=root/'terminal-evidence/manifest.json'
    require(sha(terminal_manifest_path.read_bytes())=='1be9b4be8f93edc7153747b8310cb3877b269b5eda9b54aaefcd3eaea54249f8','terminal package manifest identity')
    terminal_manifest=load(terminal_manifest_path)
    require(terminal_manifest['source_commit']==SOURCE and len(terminal_manifest['files'])==10,'terminal package source/inventory')
    for record in terminal_manifest['files']:require(binding(root/'terminal-evidence',record['path'])==record,'terminal package exact file bytes')
    require((root/'terminal-evidence/merge-identity.json').read_bytes()==(pending/'source-identity.json').read_bytes(),'historical pending merge receipt changed in terminal package')
    require(load(root/'terminal-evidence/build-info.json')==build,'build-info/verified APK binding')
    return {'schema_version':1,'source_commit':SOURCE,'source_tree':TREE,'status':'integrated source; actual postmerge CI completed successfully','terminal_record_commit':TERMINAL_RECORD,'terminal_record_url':RECORD_URL,
        'terminal_record_manifest_sha256':'1be9b4be8f93edc7153747b8310cb3877b269b5eda9b54aaefcd3eaea54249f8',
        'run':run,'successful_exact_merge_checks':[{'id':c['id'],'name':c['name']} for c in gate['checks']],
        'historical_pending_manifest':binding(root,'integrated-pending/manifest.json'),'historical_pending_observation_retained_unchanged':True,
        'terminal_receipt_bindings':[binding(root,'terminal-evidence/'+name) for name in NAMES],'complete_terminal_package_manifest':binding(root,'terminal-evidence/manifest.json'),'actual_postmerge_runtime_resolution_verification':runtime,
        'structural_tables':[binding(root,name) for name in ('structural-per-locale.csv','structural-per-locale.json')],
        'coverage_totals_unchanged':coverage['presence_totals'],'locales_after':coverage['locales_after'],'missingness_qualifications':coverage['remaining_missing_P0_classification'],
        'test_outcomes':{'JVM':jvm['junit_totals'],'hosted_Python':py,'lint_issues':jvm['lint_issues'],'API35_app_completed':45,'API35_native_completed':74,'exact_script_probes':13,'deliberate_exact_script_rejections':rejected,'new_compiled_values':26,'prior_compiled_values':256},
        'linguistic_scope_change':False,'global_accepted_count':None,'new_native_human_physical_device_layout_release_or_whole_language_certification':False,
        'limits':'This supplement joins supplied exact actual-merge terminal receipts; it does not rerun CI, re-extract APKs or add linguistic acceptance. The preserved pending snapshot contains the validated arithmetic, original qualifications and 78 historical controls. Its pending observation is not rewritten. Hosted Python skips remain two unnamed skips; local/optimized results are not substituted.'}

def run(root,write=False):
    expected=derive(root)
    path=root/'terminal-status-supplement.json'
    if write:path.write_text(json.dumps(expected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    require(load(path)==expected,'terminal supplement differs from exact supplied evidence')
    return {'schema_version':1,'source_commit':SOURCE,'source_tree':TREE,'run_id':RUN,'actual_merge_terminal_receipts_verified':6,'checks_jobs_joined':6,'job_source_binding_method':'Jobs lack their own head field in the supplied receipt; exact job IDs/names join the six source-bound check records.','new_review_compiled_pairs_joined':26,'historical_pending_payload_files_plus_manifest_byte_preserved':25,'complete_terminal_package_files_byte_verified':11,'actual_postmerge_inherited_oracle_pass_verified':True,'convenience_tables_byte_identical':True,'stable_arithmetic_rerun':False,'source_or_external_changes':False,'no_new_linguistic_acceptance':True}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report-root',type=Path,required=True);p.add_argument('--write',action='store_true');a=p.parse_args()
    result=run(a.report_root,a.write)
    (a.report_root/'terminal-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
