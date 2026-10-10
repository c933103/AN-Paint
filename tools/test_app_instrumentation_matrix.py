"""Exact bounded app coverage: synthetic receipts cannot hide omitted methods."""
import copy
import json
import os
import shutil
import sys
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from app_instrumentation_matrix import (GALLERY_DRAFT, GALLERY_METHODS, PHASE_TIMEOUTS,
    app_partition, report_paths, verify_app_reports, verify_reports, coverage_paths, SELECTED_PHASES)
from vertical_locale_matrix import VERTICAL_SHARDS
from run_android_instrumentation import (RESTART_SEED, RESTART_VERIFY, declared_tests,
                                         source_tests_sha256)

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT/'app/src/androidTest'


def receipts(source, sdk):
    expected = declared_tests(source, sdk_level=sdk)
    digest = source_tests_sha256(source)
    suppressed = declared_tests(source)-expected
    reports = {}
    for phase, wanted in app_partition(expected, sdk).items():
        reports[phase] = dict(success=True, device_sdk=sdk, source_tests_sha256=digest,
            sdk_suppressed_tests=[list(item) for item in sorted(suppressed)],
            included_tests=sorted(f'{owner}#{name}' for owner, name in wanted) if phase in SELECTED_PHASES else [],
            timeout_seconds=PHASE_TIMEOUTS[phase], timed_out=False, returncode=0, errors=[], missing=[], unexpected=[],
            leave_target_running=(phase=='seed'), expected_tests=len(wanted), completed_tests=len(wanted),
            cases=[dict(classname=owner, name=name, status='passed') for owner, name in sorted(wanted)])
    return expected, reports, digest, suppressed


class AppPartitionTest(unittest.TestCase):
    def test_exact_current_source_inventory_for_both_apis_and_korean_remains_required(self):
        for sdk, counts in ((30, {'ordinary':15, 'gallery-draft':3, **{p:2 for p in VERTICAL_SHARDS}}),
                            (35, {'ordinary':16, 'gallery-draft':3, **{p:2 for p in VERTICAL_SHARDS}, 'seed':1, 'verify':1})):
            expected, reports, digest, suppressed = receipts(SOURCE, sdk)
            result = verify_app_reports(expected, sdk, reports, digest, suppressed)
            self.assertEqual(result['phases'], counts)
            self.assertEqual(result['declared_tests'], 25)
            self.assertEqual(result['completed_tests'], 22 if sdk==30 else 25)
            self.assertEqual(len(result['sdk_suppressed_tests']), 1 if sdk==30 else 0)
            self.assertEqual(len(result['explicitly_excluded_tests']), 2 if sdk==30 else 0)
            self.assertIn(('paint.anpaint.android.EditorDeviceTest',
                'mixedScriptKoreanUsesItsCatalogueAcrossRealPickerSwitchesAndRotation'), app_partition(expected,sdk)['ordinary'])
            self.assertEqual(result['ordinary_and_gallery_total_timeout_seconds'],270)
            self.assertEqual(result['all_app_total_timeout_seconds'],630 if sdk==30 else 750)

    def test_future_ordinary_methods_are_included_and_unknown_gallery_methods_fail_closed(self):
        expected, reports, digest, suppressed = receipts(SOURCE,35)
        future=('paint.anpaint.android.FutureTest','newCase')
        self.assertIn(future,app_partition(expected|{future},35)['ordinary'])
        with self.assertRaises(ValueError): verify_app_reports(expected|{future},35,reports,digest,suppressed)
        for changed in (expected|{(GALLERY_DRAFT,'newGalleryCase')},
                        expected-{(GALLERY_DRAFT,next(iter(GALLERY_METHODS)))},
                        expected|{(RESTART_SEED,'extra')},
                        {item for item in expected if item[0]!=RESTART_VERIFY}):
            with self.assertRaises(ValueError): app_partition(changed,35)

    def test_each_phase_rejects_missing_duplicate_foreign_skipped_failed_and_unfinished_methods(self):
        for sdk in (30,35):
            expected, original, digest, suppressed=receipts(SOURCE,sdk)
            for phase in original:
                mutations=[lambda r:r['cases'].pop(),
                    lambda r:r['cases'].append(copy.deepcopy(r['cases'][0])),
                    lambda r:r['cases'][0].update(name='undeclared'),
                    *[lambda r,status=status:r['cases'][0].update(status=status) for status in ('skipped','failure','error')]]
                for mutate in mutations:
                    reports=copy.deepcopy(original);mutate(reports[phase])
                    with self.subTest(sdk=sdk,phase=phase,mutate=mutate),self.assertRaises(ValueError):
                        verify_app_reports(expected,sdk,reports,digest,suppressed)

    def test_wrong_sdk_source_selector_budget_or_failure_metadata_rejected_in_every_phase(self):
        for sdk in (30,35):
            expected, original, digest, suppressed=receipts(SOURCE,sdk)
            for phase in original:
                bad={'success':[False,None], 'device_sdk':[None,str(sdk),True,30 if sdk==35 else 35],
                     'source_tests_sha256':[None,'0'*64], 'included_tests':[None,['foreign#method']],
                     'timeout_seconds':[None,PHASE_TIMEOUTS[phase]+1], 'timed_out':[None,True],
                     'returncode':[None,1], 'errors':[None,['failed']], 'missing':[None,['missing']],
                     'unexpected':[None,['extra']], 'leave_target_running':[None,phase!='seed'],
                     'expected_tests':[0], 'completed_tests':[0], 'sdk_suppressed_tests':[None,[['foreign','method']]]}
                for key,values in bad.items():
                    for value in values:
                        reports=copy.deepcopy(original);reports[phase][key]=value
                        with self.subTest(sdk=sdk,phase=phase,key=key,value=value),self.assertRaises(ValueError):
                            verify_app_reports(expected,sdk,reports,digest,suppressed)
            for phase in original:
                reports=copy.deepcopy(original);reports.pop(phase)
                with self.assertRaises(ValueError):verify_app_reports(expected,sdk,reports,digest,suppressed)
            reports={**original,'unexpected':original['ordinary']}
            with self.assertRaises(ValueError):verify_app_reports(expected,sdk,reports,digest,suppressed)

    def test_exact_report_paths_and_stale_union_removed_on_missing_or_extra_report(self):
        for sdk in (30,35):
            _,reports,_,_=receipts(SOURCE,sdk)
            with tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                for phase,path in report_paths(root,sdk).items():
                    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(reports[phase]))
                restart=root/'app/accepted-credit-restart';restart.mkdir(parents=True,exist_ok=True)
                result=verify_reports(SOURCE,root,sdk)
                self.assertTrue(result['success'])
                self.assertEqual((root/'app/ordinary-gallery-coverage.json').exists(),True)
                self.assertEqual((restart/'coverage.json').exists(),sdk==35)
                extra=root/'app-gallery-draft/stale/summary.json';extra.parent.mkdir();extra.write_text('{}')
                with self.assertRaises(ValueError): verify_reports(SOURCE,root,sdk)
                self.assertFalse((root/'app/ordinary-gallery-coverage.json').exists())
                self.assertFalse((restart/'coverage.json').exists())
                extra.unlink();verify_reports(SOURCE,root,sdk)
                report_paths(root,sdk)['gallery-draft'].unlink()
                with self.assertRaises(ValueError): verify_reports(SOURCE,root,sdk)
                self.assertFalse((root/'app/ordinary-gallery-coverage.json').exists())

    def test_shell_selects_exact_gallery_methods_without_changing_outer_deadlines(self):
        shell=(ROOT/'tools/ci_emulator.sh').read_text()
        body=shell.split('run_gallery_draft_regression() {',1)[1].split('\n}\n',1)[0]
        selected=set(re.findall(r'--include-test "\$gallery_class#(\w+)"',body))
        self.assertEqual(selected,GALLERY_METHODS)
        self.assertEqual(body.count('tools/run_android_instrumentation.py'),1)
        self.assertIn('--timeout-seconds 90',body)
        self.assertNotIn('--leave-target-running',body)
        self.assertEqual(shell.count('--timeout-seconds 180'),4)
        self.assertEqual(shell.count('--timeout-seconds 60'),2)
        main=shell.split('main() {',1)[1]
        self.assertIn('--exclude-class paint.anpaint.android.GalleryDraftDeviceTest || editor_failed=1',main)
        self.assertIn('run_gallery_draft_regression || editor_failed=1',main)
        self.assertLess(main.index('run_gallery_draft_regression'),main.index('run_credit_restart_regression'))
        self.assertLess(main.index('run_credit_restart_regression'),main.index('tools/app_instrumentation_matrix.py'))
        workflow=(ROOT/'.github/workflows/android.yml').read_text()
        self.assertIn('timeout-minutes: 25',workflow)
        self.assertIn('timeout-minutes: 15',workflow)


class ComposedDriverTest(unittest.TestCase):
    def test_main_schedules_every_distinct_phase_and_preserves_failure_gates(self):
        shell=(ROOT/'tools/ci_emulator.sh').read_text()
        main=shell.split('main() {',1)[1]
        driver=main[main.index('  failed=0\n'):main.index('\n}\n')]
        harness=r"""
set -euo pipefail
report="$TEST_ROOT/report"; mkdir -p "$report"
adb=unused; variant=debug
progress() { :; }
python3() {
  printf 'python3'; printf ' %s' "$@"; printf '\n'
  if [[ "$1" == tools/app_instrumentation_matrix.py ]]; then [[ "$TEST_FAULT" != verifier ]];
  elif [[ " $* " == *' --suite Paintroid '* ]]; then [[ "$TEST_FAULT" != native ]];
  else [[ "$TEST_FAULT" != ordinary ]]; fi
}
run_gallery_draft_regression() { echo gallery; [[ "$TEST_FAULT" != gallery ]]; }
run_vertical_locale_matrix() { echo vertical; [[ "$TEST_FAULT" != vertical ]]; }
run_credit_restart_regression() { echo restart; [[ "$TEST_FAULT" != restart ]]; }
"""
        for sdk in (30,35):
            for fault in ('', 'native', 'ordinary', 'gallery', 'vertical', 'restart', 'verifier'):
                with self.subTest(sdk=sdk,fault=fault),tempfile.TemporaryDirectory() as directory:
                    run=subprocess.run(['bash','-c',harness+'\n'+driver],cwd=ROOT,
                        env={**os.environ,'TEST_ROOT':directory,'TEST_API':str(sdk),'TEST_FAULT':fault},
                        text=True,capture_output=True,timeout=10)
                    expected_failure=bool(fault) and not (sdk==30 and fault=='restart')
                    self.assertEqual(run.returncode,int(expected_failure),run.stdout+run.stderr)
                    lines=run.stdout.splitlines()
                    self.assertEqual(lines.count('gallery'),1)
                    self.assertEqual(lines.count('vertical'),1)
                    self.assertEqual(lines.count('restart'),int(sdk==35 and fault not in ('ordinary','gallery')))
                    ordinary=next(line for line in lines if ' --suite app ' in line)
                    for owner in (GALLERY_DRAFT,'paint.anpaint.android.VerticalLocaleDeviceTest',RESTART_SEED,RESTART_VERIFY):
                        self.assertIn('--exclude-class '+owner,ordinary)
                    verifiers=[line for line in lines if line.startswith('python3 tools/app_instrumentation_matrix.py')]
                    self.assertEqual(len(verifiers),1)
                    self.assertEqual(lines[-1],verifiers[0])
                    self.assertLess(lines.index('gallery'),lines.index('vertical'))
                    if 'restart' in lines:self.assertLess(lines.index('vertical'),lines.index('restart'))

    def test_both_clis_require_composed_reports_and_clear_all_receipts_in_optimized_modes(self):
        for sdk in (30,35):
            _,reports,_,_=receipts(SOURCE,sdk)
            for mode in ('normal','flag','environment'):
                for script,subcommand in (('app_instrumentation_matrix.py',[]),
                                         ('vertical_locale_matrix.py',['verify-reports'])):
                    with self.subTest(sdk=sdk,mode=mode,script=script),tempfile.TemporaryDirectory() as directory:
                        root=Path(directory)
                        for phase,path in report_paths(root,sdk).items():
                            path.parent.mkdir(parents=True,exist_ok=True)
                            path.write_text(json.dumps(reports[phase]))
                        env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
                        if mode=='environment':env['PYTHONOPTIMIZE']='1'
                        command=[sys.executable,*(['-O'] if mode=='flag' else []),str(ROOT/'tools'/script),
                                 *subcommand,'--source-tests',str(SOURCE),'--sdk',str(sdk),'--root',str(root)]
                        run=subprocess.run(command,env=env,text=True,capture_output=True,timeout=10)
                        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
                        outputs=coverage_paths(root)
                        selected=outputs if sdk==35 else outputs[:-1]
                        self.assertEqual(len({path.read_bytes() for path in selected}),1)
                        result=json.loads(selected[0].read_text())
                        self.assertEqual(result['receipt_scope'],'complete-composed-app-union')
                        self.assertEqual(result['completed_tests'],22 if sdk==30 else 25)
                        # A copied standalone/old report in any app subtree is not
                        # allowed to coexist with an otherwise complete report set.
                        for subtree in ('app','app-gallery-draft','app-vertical'):
                            extra=root/subtree/'old/summary.json';extra.parent.mkdir(parents=True)
                            extra.write_text('{}')
                            for output in outputs:
                                output.parent.mkdir(parents=True,exist_ok=True);output.write_text('{"success":true}')
                            run=subprocess.run(command,env=env,text=True,capture_output=True,timeout=10)
                            self.assertNotEqual(run.returncode,0)
                            self.assertEqual(run.stdout,'')
                            self.assertTrue(all(not output.exists() for output in outputs))
                            extra.unlink()
                        # Every required phase independently fails closed when
                        # absent or repeated, including both optimized modes.
                        for phase,path in report_paths(root,sdk).items():
                            original=path.read_text()
                            for fault in ('missing','duplicate'):
                                with self.subTest(phase=phase,fault=fault):
                                    if fault=='missing':path.unlink()
                                    else:
                                        broken=json.loads(original)
                                        broken['cases'].append(copy.deepcopy(broken['cases'][0]))
                                        path.write_text(json.dumps(broken))
                                    for output in outputs:
                                        output.parent.mkdir(parents=True,exist_ok=True)
                                        output.write_text('{"success":true}')
                                    run=subprocess.run(command,env=env,text=True,capture_output=True,timeout=10)
                                    self.assertNotEqual(run.returncode,0,run.stdout+run.stderr)
                                    self.assertEqual(run.stdout,'')
                                    self.assertTrue(all(not output.exists() for output in outputs))
                                    path.write_text(original)
                        # A complete standalone PR34 union still lacks both shards.
                        for phase in VERTICAL_SHARDS:report_paths(root,sdk)[phase].unlink()
                        run=subprocess.run(command,env=env,text=True,capture_output=True,timeout=10)
                        self.assertNotEqual(run.returncode,0)
                        self.assertEqual(run.stdout,'')


class GalleryInvocationTest(unittest.TestCase):
    def test_real_wrapper_runs_one_exact_bounded_selection_and_never_retries_failed_results(self):
        for fault in ('', 'missing', 'extra', 'skipped', 'truncated'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                (root/'tools').mkdir()
                shutil.copyfile(ROOT/'tools/run_android_instrumentation.py',root/'tools/run_android_instrumentation.py')
                source=root/'app/src/androidTest';source.mkdir(parents=True)
                (source/'GalleryDraftDeviceTest.kt').write_text('package paint.anpaint.android\nclass GalleryDraftDeviceTest {\n'+
                    ''.join(f'@Test fun {name}() {{}}\n' for name in sorted(GALLERY_METHODS))+'}\n')
                (source/'Other.kt').write_text('package example\nclass Other { @Test fun keepOrdinary() {} }\n')
                apk=root/'build/prebuilt/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk'
                apk.parent.mkdir(parents=True);apk.touch()
                (root/'report').mkdir()
                adb=root/'adb'
                adb.write_text('#!'+sys.executable+'\n'+"""
import json, os, sys
from pathlib import Path
args=sys.argv[1:];root=Path(os.environ['TEST_ROOT'])
with (root/'commands.jsonl').open('a') as out:out.write(json.dumps(args)+'\\n')
if args==['shell','getprop','ro.build.version.sdk']: print('35')
elif args[0]=='install': print('Success')
elif args==['shell','pm','list','instrumentation']:
    print('instrumentation:paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner (target=paint.anpaint.android)')
elif args[:3]==['shell','am','instrument']:
    methods=args[args.index('class')+1].split(',');fault=os.environ['TEST_FAULT']
    if fault=='missing':methods=methods[:-1]
    if fault=='extra':methods.append('example.Other#keepOrdinary')
    for selector in methods:
        owner,name=selector.split('#')
        for code in (1,-3 if fault=='skipped' else 0):
            print('INSTRUMENTATION_STATUS: class='+owner)
            print('INSTRUMENTATION_STATUS: test='+name)
            print('INSTRUMENTATION_STATUS: numtests='+str(len(methods)))
            print('INSTRUMENTATION_STATUS_CODE: '+str(code))
    if fault!='truncated':print('INSTRUMENTATION_CODE: -1')
else:raise SystemExit('Unexpected adb command: '+repr(args))
""")
                adb.chmod(0o700)
                run=subprocess.run(['bash','-c',
                    'source "$CI_SCRIPT"; report="$TEST_ROOT/report"; adb="$TEST_ROOT/adb"; variant=debug; run_gallery_draft_regression'],
                    cwd=root,env={**os.environ,'CI_SCRIPT':str(ROOT/'tools/ci_emulator.sh'),
                                  'TEST_ROOT':str(root),'TEST_FAULT':fault},text=True,capture_output=True,timeout=15)
                report=json.loads((root/'report/app-gallery-draft/androidTest-results/summary.json').read_text())
                commands=[json.loads(line) for line in (root/'commands.jsonl').read_text().splitlines()]
                instrumentation=[args for args in commands if args[:3]==['shell','am','instrument']]
                self.assertEqual(len(instrumentation),1)
                command=instrumentation[0]
                self.assertEqual(command[command.index('class')+1].split(','),
                                 sorted(f'{GALLERY_DRAFT}#{method}' for method in GALLERY_METHODS))
                self.assertNotIn('--no-restart',command)
                self.assertNotIn('waitForActivitiesToComplete',command)
                self.assertEqual(report['timeout_seconds'],90)
                self.assertEqual(report['success'],not fault,run.stdout+run.stderr)
                self.assertEqual(run.returncode,1 if fault else 0,run.stdout+run.stderr)


if __name__=='__main__': unittest.main()
