"""Targeted synthetic terminal-join mutations; no source changes or CI calls."""
import argparse,copy,json
from pathlib import Path
import verify_terminal as v
p=argparse.ArgumentParser()
for n in ('inputs','source-root','original-source-root','baseline-source-root','out'):p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();outputs,docs,prior,approved=v.prepare(a);cases=[]
I='run-merge-artifact-identity.json';B='artifact-source-binding.json';C='compiled-resource-verification.json';E='exact-script-verification.json';R='hosted-regression-verification.json';A='api35-terminal-verification.json';X='PR-versus-actual-merge.json'
def reject(label,fn):
 d=copy.deepcopy(docs);fn(d)
 try:v.validate(d,prior,approved)
 except (ValueError,KeyError,TypeError,IndexError) as e:cases.append({'case':label,'outcome':'rejected','guard':str(e)});return
 raise ValueError('accepted negative '+label)
for label,fn in [
 ('wrong actual run',lambda d:d[I]['run'].__setitem__('id',40346532936)),
 ('PR event relabelled',lambda d:d[I]['run'].__setitem__('event','pull_request')),
 ('wrong workflow head',lambda d:d[I]['run'].__setitem__('head',v.HEAD)),
 ('wrong actual tree',lambda d:d[I].__setitem__('tree','0'*40)),
 ('wrong ordered parents',lambda d:d[I]['ordered_parents'].reverse()),
 ('stale develop ref',lambda d:d[I].__setitem__('develop_at_terminal_verification',v.BASE)),
 ('pending status not terminal',lambda d:d[I]['run'].__setitem__('status','in_progress')),
 ('failure conclusion',lambda d:d[I]['run'].__setitem__('conclusion','failure')),
 ('wrong completion timestamp',lambda d:d[I]['run'].__setitem__('updated_at','2026-10-26T15:36:24Z')),
 ('missing actual check',lambda d:d[I]['checks'].pop()),
 ('stale check head',lambda d:d[I]['checks'][0].__setitem__('head',v.HEAD)),
 ('failed check',lambda d:d[I]['checks'][0].__setitem__('conclusion','failure')),
 ('missing actual job',lambda d:d[I]['jobs'].pop()),
 ('duplicated artifact',lambda d:d[I]['artifacts'].__setitem__(1,copy.deepcopy(d[I]['artifacts'][0]))),
 ('wrong source artifact ID',lambda d:d[B].__setitem__('artifact_id',12662693319)),
 ('wrong source artifact digest',lambda d:d[B].__setitem__('archive_sha256','0'*64)),
 ('wrong compiled tree',lambda d:d[C].__setitem__('tree','0'*40)),
 ('wrong compiled tested commit',lambda d:d[C].__setitem__('tested_commit',v.HEAD)),
 ('wrong regression run',lambda d:d[R].__setitem__('run_id',40346532936)),
 ('wrong API tree',lambda d:d[A].__setitem__('source_tree','0'*40)),
 ('wrong exact-script source',lambda d:d[E].__setitem__('source_commit',v.HEAD)),
 ('wrong packaged source count',lambda d:d[B].__setitem__('packaged_tracked_source_files_exact',1379)),
 ('wrong source exclusions',lambda d:d[B]['packager_exclusions'].pop()),
 ('wrong build APK hash',lambda d:d[B]['build_info'].__setitem__('apk_sha256','0'*64)),
 ('compiled wrong fixture hash',lambda d:d[C]['entries'][0].__setitem__('display_sha256','0'*64)),
 ('compiled duplicate pair',lambda d:d[C]['entries'].__setitem__(1,copy.deepcopy(d[C]['entries'][0]))),
 ('compiled new versus prior inflated',lambda d:d[C].__setitem__('new_reviewed_entries',392)),
 ('JVM failure hidden',lambda d:d[R]['junit_totals'].__setitem__('failures',1)),
 ('JVM skipped case',lambda d:d[R]['junit_totals'].__setitem__('skipped',1)),
 ('missing focused suite case',lambda d:d[R]['focused_suites'][0]['cases'].pop()),
 ('failed focused case',lambda d:d[R]['focused_suites'][0]['cases'][0].__setitem__('passed',False)),
 ('hosted skips promoted to pass',lambda d:(d[R]['hosted_python'].__setitem__('passed',1398),d[R]['hosted_python'].__setitem__('skipped',0))),
 ('hosted skip identities guessed',lambda d:d[R]['hosted_python'].__setitem__('skipped_identities',['invented-one','invented-two'])),
 ('hosted duration replaced by local duration',lambda d:d[R]['hosted_python'].__setitem__('seconds',1.0)),
 ('lint failure hidden',lambda d:d[R].__setitem__('lint_issues',1)),
 ('phase failed',lambda d:d[R]['phase_receipts']['jvm'].__setitem__('exit_code',1)),
 ('missing generation probe',lambda d:d[E]['probes'].pop()),
 ('expected rejection promoted to success',lambda d:next(x for x in d[E]['probes'] if not x['expected_success']).__setitem__('exit_code',0)),
 ('API35 wrong fixture',lambda d:d[A]['composed_device_identity'].__setitem__('source_tests_sha256','0'*64)),
 ('native wrong fixture',lambda d:d[A].__setitem__('native_source_tests_sha256','0'*64)),
 ('API35 wrong source ZIP',lambda d:d[A]['composed_device_identity'].__setitem__('source_sha256','0'*64)),
 ('API35 app completion short',lambda d:d[A].__setitem__('app_source_bound_completed',44)),
 ('API35 native completion short',lambda d:d[A].__setitem__('native_source_bound_completed',73)),
 ('API35 native timed out',lambda d:d[A].__setitem__('native_timed_out',True)),
 ('API35 wrong selected artifact',lambda d:d[A]['artifact_selection']['selected']['core'].__setitem__('artifact_id',12663953202)),
 ('API35 wrong attempt',lambda d:d[A]['artifact_selection'].__setitem__('current_attempt',2)),
 ('instrumentation APK digest drift',lambda d:d[A].__setitem__('instrumentation_apks_archive_sha256','0'*64)),
 ('PR artifacts relabelled equal',lambda d:d[X].__setitem__('fresh_actual_push_and_artifact_ids_distinct',False)),
]:reject(label,fn)
v.need(len(cases)==len({x['case'] for x in cases})==48,'terminal control inventory')
a.out.mkdir(parents=True,exist_ok=True);v.emit(a.out,'terminal-mutation-controls.json',{'schema_version':1,'source_commit':v.MERGE,'source_tree':v.TREE,'run_id':v.RUN,'positive_terminal_join':'passed','controls_rejected':48,'cases':cases,'synthetic_scope':'Only in-memory mutations of verified receipt structures; no actual defect asserted, source file changed or CI rerun.','historical_pending_and_preview_controls_retained':True});print(48)
