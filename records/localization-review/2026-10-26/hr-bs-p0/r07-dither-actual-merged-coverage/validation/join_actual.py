"""Join only caller-pinned actual c404 push receipts, never prior PR receipts."""
import argparse,hashlib,json
from pathlib import Path
from recompute_successor import MERGE,TREE,HEAD,BASE,read,require
RUN=40421554043
FAMILIES={'artifact-source-binding.json','compiled-resource-verification.json','exact-script-verification.json','hosted-regression-verification.json','api35-terminal-verification.json','api35-expected-selection.json','run-terminal.json','jobs-terminal.json','artifacts-terminal.json'}
def join(directory,pin):
    mpath=directory/'manifest.json';require(hashlib.sha256(mpath.read_bytes()).hexdigest()==pin,'caller manifest pin');manifest=read(mpath)
    rows={e['path']:e for e in manifest['payloads']};require(len(rows)==len(manifest['payloads']) and FAMILIES<=rows.keys(),'unique complete receipt families')
    for name,e in rows.items():
        require(Path(name).name==name and name!='manifest.json','safe payload basename');b=(directory/name).read_bytes();require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'payload hash '+name)
    d={n:read(directory/n) for n in FAMILIES};run=d['run-terminal.json'];jobs=d['jobs-terminal.json'];artifacts=d['artifacts-terminal.json']
    require(run['id']==RUN and run['event']=='push' and run['head_branch']=='develop' and run['head_sha']==MERGE and run['status']=='completed' and run['conclusion']=='success','actual natural push terminal')
    require(jobs['total_count']==len(jobs['jobs'])==6 and len({j['id'] for j in jobs['jobs']})==6,'six distinct jobs')
    require(all(j['run_id']==RUN and j['head_sha']==MERGE and j['status']=='completed' and j['conclusion']=='success' for j in jobs['jobs']),'all actual jobs success')
    require(artifacts['total_count']==len(artifacts['artifacts']),'complete artifacts');index={a['id']:a for a in artifacts['artifacts']};require(len(index)==len(artifacts['artifacts']),'unique artifact IDs')
    bindings=[('artifact-source-binding.json','tested_commit','reviewed_head','source_tree','archive_sha256'),('exact-script-verification.json','source_commit','reviewed_pr_head','tree','archive_sha256'),('hosted-regression-verification.json','tested_commit','reviewed_head',None,'artifact_sha256'),('api35-terminal-verification.json','tested_commit','reviewed_pr_head','source_tree','artifact_sha256')]
    for name,commit,head,tree,digest in bindings:
        r=d[name];require(r['run_id']==RUN and r[commit]==MERGE and r[head]==HEAD and (tree is None or r[tree]==TREE),'fresh family identity '+name)
        a=index[r['artifact_id']];require(a['workflow_run']['id']==RUN and a['workflow_run']['head_sha']==MERGE and a['digest']=='sha256:'+r[digest] and a['expired'] is False,'artifact provenance '+name)
    src=d['artifact-source-binding.json'];require(src['tracked_files']==1388 and src['packaged_tracked_source_files_exact']==1385 and src['embedded_source_matches_external'] and src['tracked_executable_modes_match'],'packaged source exact')
    compiled=d['compiled-resource-verification.json'];require(compiled['run_id']==RUN and compiled['tested_commit']==MERGE and compiled['reviewed_head']==HEAD and compiled['tree']==TREE,'compiled identity');require(len(compiled['entries'])==1659 and compiled['total_reviewed_entries']==854 and compiled['inherited_entries']==805 and compiled['current_HR_BS_reviewed_entries']==157 and sum(compiled['inherited_entries_by_locale'][t] for t in ['hr','bs'])==214,'compiled bounded scopes')
    require(compiled['apk_sha256']==src['build_info']['apk_sha256'] and compiled['signature_exit']==0 and compiled['v1_verified'] and compiled['v2_verified'],'compiled APK/signature')
    exact=d['exact-script-verification.json'];require(exact['probe_count']==13 and exact['all_log_hashes_and_expected_exits_verified'],'all exact probes')
    reg=d['hosted-regression-verification.json'];require(reg['junit_totals']=={'tests':1399,'failures':0,'errors':0,'skipped':0} and reg['junit_files']==151 and reg['unique_junit_identities']==1399,'actual JVM aggregate');require(len(reg['focused_suites'])==14 and sum(x['source_test_methods'] for x in reg['focused_suites'])==82 and all(len(x['cases'])==x['source_test_methods'] and all(c['passed'] for c in x['cases']) for x in reg['focused_suites']),'focused method scope')
    require(reg['hosted_python']['run']==1449 and reg['hosted_python']['passed']==1447 and reg['hosted_python']['skipped']==2 and reg['lint_issues']==0,'actual Python/lint')
    api=d['api35-terminal-verification.json'];require(api['workflow_head']==MERGE and api['app_source_bound_selected']==api['app_source_bound_completed']==47 and api['native_source_bound_selected']==api['native_source_bound_completed']==74 and api['native_all_unique_case_identities_exact_match'] and not api['native_missing_unexpected_errors'] and api['native_return_code']==0 and api['native_timed_out'] is False,'actual API35 case completion')
    require(api['expected_selection_exact_match'] and api['artifact_selection']==d['api35-expected-selection.json'],'independent actual selection')
    instrumentation=[a for a in index.values() if a['name']=='instrumentation-apks-'+MERGE];require(len(instrumentation)==1,'one actual instrumentation archive')
    require(instrumentation[0]['workflow_run']['id']==RUN and instrumentation[0]['workflow_run']['head_sha']==MERGE and instrumentation[0]['digest']=='sha256:'+api['instrumentation_apks_archive_sha256'] and instrumentation[0]['expired'] is False,'instrumentation artifact provenance')
    identity=api['composed_device_identity'];require(identity['commit']==MERGE and identity['run_id']==str(RUN) and identity['apk_sha256']==src['build_info']['apk_sha256'] and identity['source_sha256']==src['build_info']['source_sha256'],'execution bytes')
    require(api['attempt_contract']=={'core':1,'position':1,'composed':1} and run['run_attempt']==1,'original natural run without retry')
    return {'actual_merge':MERGE,'source_tree':TREE,'immediate_base':BASE,'reviewed_head':HEAD,'actual_push_run':{'id':RUN,'attempt':run['run_attempt']},'all_six_checks_successful':True,'all_five_families_verified':True,'manifest_sha256':pin,'JVM':1399,'Python_passed':1447,'Python_skipped':2,'lint_issues':0,'API35_app':47,'API35_native':74,'packaged_source_files':1385,'compiled_values':1659,'exact_probes':13,'HR_BS_current_reviewed':157,'HR_BS_preserved':214,'original_PR183_reviewed':156,'original_PR183_preserved':215,'new_native_human_or_global_linguistic_acceptance':0,'release_performed':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);p.add_argument('--manifest-sha256',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=join(a.directory,a.manifest_sha256);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
