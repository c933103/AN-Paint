"""Isolated negative controls for the terminal supplement; historical validators remain unchanged."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import verify_terminal_supplement as verify

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report-root',type=Path,required=True);a=p.parse_args()
    verify.run(a.report_root)
    cases=[]
    def rejected(label,action):
        try:action()
        except (ValueError,KeyError,FileNotFoundError,TypeError):cases.append({'case':label,'rejected':True})
        else:raise RuntimeError('Malformed input accepted: '+label)
    rejected('duplicate JSON key',lambda:json.loads('{"run":1,"run":2}',object_pairs_hook=verify.unique))
    mutations=[
      ('wrong merge source','terminal-gates.json',lambda d:d.__setitem__('source_commit','0'*40)),
      ('wrong merge tree','terminal-gates.json',lambda d:d.__setitem__('source_tree','0'*40)),
      ('PR event substituted','terminal-gates.json',lambda d:d['run'].__setitem__('event','pull_request')),
      ('wrong run id','terminal-gates.json',lambda d:d['run'].__setitem__('id',1)),
      ('run still pending','terminal-gates.json',lambda d:d['run'].__setitem__('status','in_progress')),
      ('run failed','terminal-gates.json',lambda d:d['run'].__setitem__('conclusion','failure')),
      ('wrong terminal timestamp','terminal-gates.json',lambda d:d['run'].__setitem__('updated_at','2026-10-26T10:54:36Z')),
      ('wrong explicit develop','terminal-gates.json',lambda d:d.__setitem__('explicit_develop_at_terminal','0'*40)),
      ('missing check','terminal-gates.json',lambda d:d['checks'].pop()),
      ('duplicate check id','terminal-gates.json',lambda d:d['checks'][1].__setitem__('id',d['checks'][0]['id'])),
      ('stale check head','terminal-gates.json',lambda d:d['checks'][0].__setitem__('head_sha',verify.HEAD)),
      ('failed current check','terminal-gates.json',lambda d:d['checks'][0].__setitem__('conclusion','failure')),
      ('mismatched job identity','terminal-gates.json',lambda d:d['jobs'][0].__setitem__('name','different')),
      ('duplicate artifact identity','terminal-gates.json',lambda d:d['artifacts'].append(d['artifacts'][0])),
      ('wrong regression archive digest','hosted-regression-verification.json',lambda d:d.__setitem__('artifact_sha256','0'*64)),
      ('JVM skipped mislabeled passing','hosted-regression-verification.json',lambda d:d['junit_totals'].__setitem__('skipped',1)),
      ('hosted Python skips hidden','hosted-regression-verification.json',lambda d:d['hosted_python'].__setitem__('skipped',0)),
      ('hosted skipped identities invented','hosted-regression-verification.json',lambda d:d['hosted_python'].__setitem__('skipped_identities',['invented'])),
      ('lint errors hidden','hosted-regression-verification.json',lambda d:d.__setitem__('lint_issues',1)),
      ('focused test not passed','hosted-regression-verification.json',lambda d:d['focused_suites'][0]['cases'][0].__setitem__('passed',False)),
      ('API35 incomplete app cases','api35-terminal-verification.json',lambda d:d.__setitem__('app_source_bound_completed',44)),
      ('API35 missing native case','api35-terminal-verification.json',lambda d:d.__setitem__('native_source_bound_completed',73)),
      ('API35 timeout','api35-terminal-verification.json',lambda d:d.__setitem__('native_timed_out',True)),
      ('wrong composed APK hash','api35-terminal-verification.json',lambda d:d['composed_device_identity'].__setitem__('apk_sha256','0'*64)),
      ('wrong composed source hash','api35-terminal-verification.json',lambda d:d['composed_device_identity'].__setitem__('source_sha256','0'*64)),
      ('wrong device lane artifact','api35-terminal-verification.json',lambda d:d['artifact_selection']['selected']['core'].__setitem__('artifact_id',1)),
      ('wrong build commit','artifact-source-binding.json',lambda d:d['build_info'].__setitem__('commit',verify.HEAD)),
      ('source archive mismatch','artifact-source-binding.json',lambda d:d.__setitem__('embedded_source_matches_external',False)),
      ('duplicate compiled pair','compiled-resource-verification.json',lambda d:d['entries'].append(d['entries'][0])),
      ('wrong compiled new-value hash','compiled-resource-verification.json',lambda d:next(e for e in d['entries'] if e['locale']=='ca').__setitem__('display_sha256','0'*64)),
      ('unverified APK signature','compiled-resource-verification.json',lambda d:d.__setitem__('v2_verified',False)),
      ('deliberate rejection erased','exact-script-verification.json',lambda d:next(p for p in d['probes'] if not p['expected_success']).__setitem__('expected_success',True)),
      ('missing exact-script probe','exact-script-verification.json',lambda d:d['probes'].pop()),
      ('wrong receipt schema','exact-script-verification.json',lambda d:d.__setitem__('schema_version',True)),
    ]
    for label,name,mutation in mutations:
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'report';shutil.copytree(a.report_root,root,ignore=shutil.ignore_patterns('__pycache__'))
            path=root/'terminal-evidence'/name;doc=verify.load(path);mutation(doc);path.write_text(json.dumps(doc))
            # Derive before comparing bindings: these are semantic guard checks, not checksum-only rejection.
            rejected(label,lambda:verify.derive(root))
    for label,mutation in [('supplement invented global acceptance',lambda d:d.__setitem__('global_accepted_count',20)),('supplement claims native acceptance',lambda d:d.__setitem__('new_native_human_physical_device_layout_release_or_whole_language_certification',True)),('supplement wrong immutable record',lambda d:d.__setitem__('terminal_record_commit','0'*40))]:
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'report';shutil.copytree(a.report_root,root,ignore=shutil.ignore_patterns('__pycache__'))
            path=root/'terminal-status-supplement.json';doc=verify.load(path);mutation(doc);path.write_text(json.dumps(doc));rejected(label,lambda:verify.run(root))
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)/'report';shutil.copytree(a.report_root,root,ignore=shutil.ignore_patterns('__pycache__'))
        path=root/'integrated-pending/source-identity.json';doc=verify.load(path);doc['run']['status']='completed';path.write_text(json.dumps(doc));rejected('historical pending observation rewritten',lambda:verify.derive(root))
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)/'report';shutil.copytree(a.report_root,root,ignore=shutil.ignore_patterns('__pycache__'))
        (root/'structural-per-locale.csv').write_text('changed');rejected('convenience table differs',lambda:verify.derive(root))
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)/'report';shutil.copytree(a.report_root,root,ignore=shutil.ignore_patterns('__pycache__'))
        (root/'terminal-evidence/terminal-gates.json').unlink();rejected('missing terminal receipt',lambda:verify.derive(root))
    result={'schema_version':1,'source_commit':verify.SOURCE,'run_id':verify.RUN,'positive_terminal_receipt_join_passed':True,'negative_controls':len(cases),'all_rejected':True,'historical_62_controls_unchanged':True,'source_or_original_evidence_modified':False,'cases':cases}
    (a.report_root/'terminal-mutation-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'positive':True,'negative_controls':len(cases),'all_rejected':True}))
if __name__=='__main__':main()
