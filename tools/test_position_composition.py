"""Position selection, cross-job identity and partial/full evidence boundaries."""
import copy
import json
import math
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import unittest

from app_instrumentation_matrix import (POSITION_SHARDS, coverage_paths, report_paths,
                                         verify_reports)
from compose_device_reports import compose, record, sha256
from test_app_instrumentation_matrix import SOURCE, receipts
from test_ci_timeout_budget import (ROOT, SHELL, RUNNER, WORKFLOW, body, controlled_model,
                                   job, one, shell_timeout, step_minutes)

ENV = dict(GITHUB_SHA='a'*40, GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1', BUILD_VARIANT='debug')


def fixture(root, sdk):
    prebuilt = root/'prebuilt'
    for name in ('app/build/outputs/apk/debug/app-debug.apk',
                 'app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk',
                 'build/delivery/AN-Paint-source.zip'):
        path = prebuilt/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(name.encode())  # Identity fixtures, not installable APKs.
    build = dict(commit=ENV['GITHUB_SHA'], run_id=ENV['GITHUB_RUN_ID'], build_variant='debug',
        apk_sha256=sha256(prebuilt/'app/build/outputs/apk/debug/app-debug.apk'),
        source_sha256=sha256(prebuilt/'build/delivery/AN-Paint-source.zip'))
    (prebuilt/'build/delivery/build-info.json').write_text(json.dumps(build))
    _, reports, _, _ = receipts(SOURCE, sdk)
    for group in ('core', 'position'):
        out = root/group
        record(SOURCE, prebuilt, out, sdk, group, ENV)
        for phase, path in report_paths(out, sdk, group).items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(reports[phase]))
    return prebuilt


class PositionCompositionTest(unittest.TestCase):
    def test_partial_receipts_are_never_complete_and_only_exact_union_passes(self):
        for sdk in (30, 35):
            with self.subTest(sdk=sdk), tempfile.TemporaryDirectory() as directory:
                root=Path(directory);fixture(root,sdk)
                for group in ('core','position'):
                    result=verify_reports(SOURCE,root/group,sdk,group)
                    self.assertEqual(result['receipt_scope'],f'partial-{group}-app-union')
                    self.assertEqual(result['completed_tests'],7 if group=='position' else (23 if sdk==30 else 38))
                    self.assertTrue(result['deferred_tests'])
                    self.assertTrue(all(not path.exists() for path in coverage_paths(root/group)))
                    with self.assertRaises(ValueError): verify_reports(SOURCE,root/group,sdk)
                result=compose(SOURCE,root/'core',root/'position',sdk,ENV)
                self.assertEqual(result['receipt_scope'],'complete-composed-app-union')
                self.assertEqual(result['completed_tests'],30 if sdk==30 else 45)
                self.assertEqual(result['deferred_tests'],[])
                self.assertTrue((root/'core/app/coverage.json').is_file())

    def test_each_wrong_identity_and_missing_failed_or_extra_phase_fails_closed(self):
        mutations={key:'b'*40 if key=='commit' else 'mismatch' for key in
                   ('commit','run_id','run_attempt','build_variant','source_tests_sha256','group')}
        mutations.update(device_sdk=30,apk_sha256='b'*64,source_sha256='b'*64,test_apk_sha256='b'*64)
        for group in ('core','position'):
            for key,value in mutations.items():
                with self.subTest(group=group,key=key), tempfile.TemporaryDirectory() as directory:
                    root=Path(directory);fixture(root,35)
                    path=root/group/'device-identity.json';identity=json.loads(path.read_text())
                    identity[key]=value;path.write_text(json.dumps(identity))
                    stale=root/'core/app/coverage.json';stale.write_text('{"success":true}')
                    with self.assertRaises(ValueError):compose(SOURCE,root/'core',root/'position',35,ENV)
                    self.assertFalse(stale.exists())
            for fault in ('missing','failed','duplicate','extra'):
                with self.subTest(group=group,fault=fault), tempfile.TemporaryDirectory() as directory:
                    root=Path(directory);fixture(root,35)
                    path=next(iter(report_paths(root/group,35,group).values()))
                    report=json.loads(path.read_text())
                    if fault=='missing':path.unlink()
                    elif fault=='extra':(path.parent/'extra').mkdir();(path.parent/'extra/summary.json').write_text('{}')
                    else:
                        if fault=='failed':report['cases'][0]['status']='failure'
                        else:report['cases'].append(copy.deepcopy(report['cases'][0]))
                        path.write_text(json.dumps(report))
                    with self.assertRaises(ValueError):compose(SOURCE,root/'core',root/'position',35,ENV)
                    self.assertTrue(all(not path.exists() for path in coverage_paths(root/'core')))

    def test_same_run_mixed_attempts_are_provenance_and_future_or_invalid_attempts_fail(self):
        for attempt in ('2', '3', '0', '-1', '1.5', '', None, 2, True, 'missing'):
            with self.subTest(attempt=attempt), tempfile.TemporaryDirectory() as directory:
                root=Path(directory);fixture(root,35)
                path=root/'position/device-identity.json';identity=json.loads(path.read_text())
                if attempt == 'missing':identity.pop('run_attempt')
                else:identity['run_attempt']=attempt
                path.write_text(json.dumps(identity))
                env={**ENV,'GITHUB_RUN_ATTEMPT':'2'}
                if attempt == '2':
                    result=compose(SOURCE,root/'core',root/'position',35,env)
                    self.assertEqual(result['device_identity']['group_run_attempts'],{'core':1,'position':2})
                    self.assertEqual(result['device_identity']['composed_in_run_attempt'],2)
                    self.assertEqual(json.loads((root/'core/app/coverage.json').read_text()),json.loads(json.dumps(result)))
                else:
                    with self.assertRaises(ValueError):compose(SOURCE,root/'core',root/'position',35,env)
                    self.assertTrue(all(not path.exists() for path in coverage_paths(root/'core')))

    def test_prebuilt_binding_rejects_other_build_or_modified_bytes(self):
        for name in ('app/build/outputs/apk/debug/app-debug.apk','build/delivery/AN-Paint-source.zip',
                     'build/delivery/build-info.json'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root=Path(directory);prebuilt=fixture(root,35)
                path=prebuilt/name
                if name.endswith('.json'):
                    value=json.loads(path.read_text());value['commit']='b'*40;path.write_text(json.dumps(value))
                else:path.write_bytes(b'changed')
                with self.assertRaises(ValueError):record(SOURCE,prebuilt,root/'new',35,'core',ENV)

    def test_two_shell_shards_execute_once_even_when_first_fails(self):
        for fault in ('none','first','last','gate'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                events=Path(directory)/'events'
                command=r'''source tools/ci_position.sh
report="$TEST_ROOT/report"; adb=fake; variant=debug; TEST_API=35
progress() { :; }
python3() {
  printf '%s\n' "$*" >> "$TEST_ROOT/events"
  case "$FAULT:$*" in
    first:*--suite\ app-position-ainu-manchu*|last:*--suite\ app-position-tibetan-jeju-nom*|gate:*app_instrumentation_matrix.py*) return 1;;
  esac
}
run_position_regression
'''
                result=subprocess.run(['bash','-c',command],cwd=ROOT,
                    env={**os.environ,'TEST_ROOT':directory,'FAULT':fault},capture_output=True,text=True,timeout=5)
                calls=[shlex.split(line) for line in events.read_text().splitlines()]
                self.assertEqual(len(calls),3)
                for args,(phase,wanted) in zip(calls,POSITION_SHARDS.items()):
                    self.assertEqual(args[args.index('--suite')+1],'app-'+phase)
                    self.assertEqual(args[args.index('--timeout-seconds')+1],'180')
                    self.assertEqual({args[i+1] for i,value in enumerate(args) if value=='--include-test'},
                                     {f'{owner}#{name}' for owner,name in wanted})
                self.assertEqual(calls[-1][-2:],['--group','position'])
                self.assertEqual(result.returncode,0 if fault=='none' else 1,result.stderr)

    def test_workflow_gates_share_selection_prebuilt_identity_and_release_gate_name(self):
        core,position,union=(job(WORKFLOW,name) for name in ('device','position','device-union'))
        self.assertEqual(one(r'^        api: (.+)$',core),one(r'^        api: (.+)$',position))
        self.assertEqual(one(r'^        api: (.+)$',core),one(r'^        api: (.+)$',union))
        self.assertEqual(one(r'^    if: (.+)$',core),one(r'^    if: (.+)$',position))
        for group,block in (('core',core),('position',position)):
            self.assertIn('needs: build',block)
            for text in ('name: apk-and-source-${{ github.sha }}','name: instrumentation-apks-${{ github.sha }}',
                         f'APP_TEST_GROUP: {group}',f'--group {group}',f'name: emulator-{group}-api-'):
                self.assertIn(text,block)
            self.assertNotIn('continue-on-error',block)
        for text in ('name: Emulator API ${{ matrix.api }}','needs: [device, position]',
                     'always() &&','test "$CORE_RESULT" = success && test "$POSITION_RESULT" = success',
                     'artifact-ids: ${{ steps.artifacts.outputs.core }}',
                     'artifact-ids: ${{ steps.artifacts.outputs.position }}',
                     'compose_device_reports.py compose','name: emulator-api-'):
            self.assertIn(text,union)
        self.assertNotIn('if: always()',union.split('actions/upload-artifact')[1])
        self.assertIn('--exclude-class paint.anpaint.android.AssemblyPositionDeviceTest',SHELL)
        self.assertIn('source tools/ci_position.sh',body(SHELL,'main'))

    def test_position_job_budget_is_separate_and_source_bound(self):
        model=controlled_model(SHELL,RUNNER)
        script=(ROOT/'tools/ci_position.sh').read_text().replace('\\\n',' ')
        caps=re.findall(r'--suite (\S+) --timeout-seconds (\d+)',script)
        self.assertEqual(dict(caps),{'app-'+phase:'180' for phase in POSITION_SHARDS})
        cleanup=body(SHELL.replace('\\\n',' '),'cleanup')
        pulls=re.findall(r'timeout --kill-after=(\d+)s (\d+)s [^\n]*\bpull\b',cleanup)
        collection=model['cleanup']-sum(int(grace)+int(seconds) for grace,seconds in pulls)
        total=model['startup']+sum(int(cap) for _,cap in caps)+2*(
            model['preparation']/8+model['tails']/8+model['recovery']/4)+collection
        self.assertEqual(total,876)
        position=job(WORKFLOW,'position')
        self.assertEqual(step_minutes(position,'Run prebuilt tests with deadlines and live logs'),math.ceil((total+60)/60))
        self.assertEqual(int(one(r'^    timeout-minutes: (\d+)$',position)),16+6+4)

    def test_native_edit_dismisses_keyboard_before_revealing_and_keeps_real_input(self):
        source=(SOURCE/'java/paint/anpaint/android/AssemblyPositionDeviceTest.kt').read_text()
        replace=source.split('private fun replace(',1)[1].split('private fun hideIme(',1)[0]
        self.assertLess(replace.index('hideIme('),replace.index('tap(field)'))
        for text in ('field.hasFocus() && field.hasWindowFocus()','KEYCODE_A,KeyEvent.META_CTRL_ON',
                     'KEYCODE_DEL','instrumentation.sendStringSync(value)','field.text.toString()==value'):
            self.assertIn(text,replace)
        # Explicit native field taps must complete the asynchronous IME-show
        # transition before typing can race the existing native-Back hide.
        show=replace.index('await("IME shown for native field input:')
        self.assertLess(replace.index('tap(field)'),show)
        self.assertLess(show,replace.index('KEYCODE_A,KeyEvent.META_CTRL_ON'))
        self.assertIn('field.rootWindowInsets?.isVisible(WindowInsets.Type.ime())==true',replace)
        tap=source.split('private fun tap(',1)[1].split('private data class Gesture',1)[0]
        self.assertLess(tap.index('view.rootWindowInsets?.isVisible(WindowInsets.Type.ime())==false'),
                        tap.index('device.click('))
        hide=source.split('private fun hideIme(',1)[1].split('private fun orient(',1)[0]
        self.assertIn('device.pressKeyCode(KeyEvent.KEYCODE_BACK)',hide)
        self.assertIn('root.isAttachedToWindow && root.hasWindowFocus()',hide)
        self.assertIn('root.rootWindowInsets?.isVisible(WindowInsets.Type.ime())==false',hide)
        for forbidden in ('showSoftInput(', 'hideSoftInputFromWindow(', '.performClick('):
            self.assertNotIn(forbidden,source)
        self.assertIn('SystemClock.uptimeMillis()+8000',source)
        self.assertIn('45-second interaction budget',source)
        self.assertNotIn('requestFocus(',source)
        self.assertNotIn('.setText(',source)
        self.assertIn('CaptionTileTraversal.visit(region.left,region.top,region.right,region.bottom,tile)',source)
        self.assertIn('reveal(view) {rawBounds(view).let {raw ->Rect(piece).apply {offset(raw.left,raw.top)}}}',source)
        self.assertIn('SystemClock.uptimeMillis()>=deadline',source)
        self.assertIn('45-second interaction budget while waiting for: $label',source)
        self.assertIn('Timed out at 8-second wait bound: $label',source)


if __name__=='__main__':unittest.main()
