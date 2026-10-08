"""Exercise startup recovery without an Android SDK or a long-running emulator."""
import json
import os
import shutil
import signal
import sys
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

from run_android_instrumentation import declared_tests, restart_partition

SCRIPT = Path(__file__).with_name('ci_emulator.sh').resolve()
# This is infrastructure cleanup protection, not the behavior under test. Setup
# launches several Python/fake-ADB processes, installs/discovers the fake runner,
# completes seed instrumentation and parses its report. Slow host scheduling must
# not be charged to the production command's ten-second deadline.
HARNESS_SETUP_ALLOWANCE_SECONDS = 45
HARNESS_COMMAND_ALLOWANCE_SECONDS = 10
HARNESS_CLEANUP_ALLOWANCE_SECONDS = 5
HARNESS_WATCHDOG_SECONDS = (HARNESS_SETUP_ALLOWANCE_SECONDS + HARNESS_COMMAND_ALLOWANCE_SECONDS
                            + HARNESS_CLEANUP_ALLOWANCE_SECONDS)


class EmulatorReadinessTest(unittest.TestCase):
    def run_probe(self, fake_adb, *, budget=5, process='$$', pattern='1'):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adb = root / 'adb'
            adb.write_text('#!/usr/bin/env bash\nset -e\n' + fake_adb)
            adb.chmod(0o700)
            command = '''
source "$CI_SCRIPT"
report="$CI_TEST_DIR"
adb="$report/adb"
emulator_pid=PROCESS
readiness_deadline=$((SECONDS + CI_TEST_BUDGET))
wait_until_ready "Test readiness" "$CI_TEST_PATTERN" shell getprop sys.boot_completed
'''.replace('PROCESS', process)
            started = time.monotonic()
            result = subprocess.run(
                ['bash', '-c', command], text=True, capture_output=True, timeout=10,
                env={**os.environ, 'CI_SCRIPT': str(SCRIPT), 'CI_TEST_DIR': directory,
                     'CI_TEST_BUDGET': str(budget), 'CI_TEST_PATTERN': pattern})
            elapsed = time.monotonic() - started
            saved = (root / 'startup.log').read_text()
            count = (root / 'count').read_text().strip() if (root / 'count').exists() else None
            return result, elapsed, saved, count

    def test_transient_adb_timeout_is_retried_with_phase_evidence(self):
        result, _, saved, count = self.run_probe('''
count=0
if test -f "$CI_TEST_DIR/count"; then read -r count < "$CI_TEST_DIR/count"; fi
count=$((count + 1))
printf '%s\\n' "$count" > "$CI_TEST_DIR/count"
if (( count == 1 )); then echo 'service is still starting' >&2; exit 124; fi
printf '1\\r\\n'
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(count, '2')
        self.assertIn('probe exit 124', saved)
        self.assertIn('service is still starting', saved)
        self.assertIn('Ready: Test readiness', saved)

    def test_boot_property_must_have_expected_value(self):
        result, _, saved, _ = self.run_probe('echo 0\n', budget=1)
        self.assertEqual(result.returncode, 124, result.stdout + result.stderr)
        self.assertIn('startup deadline reached', saved)
        self.assertNotIn('Ready:', saved)

    def test_hung_service_is_killed_within_remaining_budget(self):
        result, elapsed, saved, _ = self.run_probe('exec sleep 30\n', budget=1, pattern='*')
        self.assertEqual(result.returncode, 124, result.stdout + result.stderr)
        self.assertLess(elapsed, 4)
        self.assertIn('probe exit 124', saved)
        self.assertIn('startup deadline reached', saved)

    def test_exited_emulator_fails_without_waiting_for_deadline(self):
        result, elapsed, saved, _ = self.run_probe('echo 1\n', process='999999999')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertLess(elapsed, 1)
        self.assertIn('emulator exited during Test readiness', saved)

    def test_package_service_requires_real_package_path(self):
        result, _, saved, _ = self.run_probe('echo "package:/system/framework/framework-res.apk"\n',
                                            pattern='package:*')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Ready: Test readiness', saved)


class AcceptedCreditBoundaryTest(unittest.TestCase):
    def run_boundary(self, failure='', *, setup_delay=0):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'tools').mkdir()
            shutil.copyfile(SCRIPT.with_name('run_android_instrumentation.py'),root/'tools/run_android_instrumentation.py')
            source=root/'app/src/androidTest';source.mkdir(parents=True)
            for name,method in (('EditorDeviceTest','ordinary'),('FutureTest','future'),
                                ('AcceptedCreditRestartSeedTest','seed'),('AcceptedCreditRestartVerifyTest','verify')):
                (source/(name+'.kt')).write_text(f'package paint.anpaint.android\nclass {name} {{ @Test fun {method}() {{}} }}\n')
            apk=root/'build/prebuilt/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk'
            apk.parent.mkdir(parents=True);apk.touch()
            report=root/'report/app/androidTest-results';report.mkdir(parents=True)
            ordinary=restart_partition(declared_tests(source))[0]
            (report/'summary.json').write_text(json.dumps(dict(success=True,leave_target_running=False,
                expected_tests=len(ordinary),completed_tests=len(ordinary),
                cases=[dict(classname=owner,name=name,status='passed') for owner,name in ordinary])))
            stale=root/'report/app/accepted-credit-restart/verify'
            stale.mkdir(parents=True)
            (stale/'summary.json').write_text('{"success":true}')
            (stale/'TEST-stale.xml').write_text('<testsuite/>')
            fake=root/'adb'
            fake.write_text('#!'+sys.executable+'\n'+r'''
import json, os, sys, time
from pathlib import Path
root=Path(os.environ['CI_TEST_DIR']); args=sys.argv[1:]; failure=os.environ['BOUNDARY_FAILURE']
def event(value):
    with (root/'events').open('a') as out:out.write(value+'\n')
    with (root/'timing.jsonl').open('a') as out:out.write(json.dumps(dict(event=value,monotonic=time.monotonic()))+'\n')
def state():return (root/'pid').read_text() if (root/'pid').exists() else 'absent'
event('adb '+json.dumps(args))
if args[0]=='install':
    # One explicitly requested benign delay, outside the PID boundary command.
    delay=float(os.environ['HARNESS_SETUP_DELAY'])
    if delay and not (root/'setup-delay-done').exists():
        (root/'setup-delay-done').touch();event('BENIGN_SETUP_DELAY_ENTERED')
        time.sleep(delay);event('BENIGN_SETUP_DELAY_COMPLETED')
    print('Success');sys.exit(0)
if args[:4]==['shell','pm','list','instrumentation']:
    print('instrumentation:paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner (target=paint.anpaint.android)');sys.exit(0)
if args[:3]==['shell','am','start']:
    (root/'pid').write_text('123');print('Status: ok');sys.exit(0)
if args[:2]==['shell','pidof']:
    if state()=='absent':sys.exit(1)
    print(state());sys.exit(0)
if len(args)==2 and args[0]=='shell' and args[1].startswith('p=$(pidof'):
    if failure=='transport' and (root/'seed-finished').exists():
        print('error: transport disconnected',file=sys.stderr);sys.exit(1)
    if failure=='timeout' and (root/'seed-finished').exists():event('FAULT_IMMEDIATE124_ENTERED');sys.exit(124)
    if failure=='hung_pid' and (root/'seed-finished').exists():event('FAULT_HUNG_PID_ENTERED');time.sleep(30)
    print('absent' if state()=='absent' else 'alive:'+state());sys.exit(0)
if args[:4]==['shell','dumpsys','activity','activities']:
    activity='ClassicPaintActivity' if failure=='gallery_closed' else 'MediaGalleryActivity'
    print('topResumedActivity=ActivityRecord{42 u0 paint.anpaint.android/org.catrobat.paintroid.classic.'+activity+' t2}')
    if failure=='die_after_gallery':(root/'pid').write_text('absent')
    sys.exit(0)
if args[:3]==['shell','am','force-stop']:
    event('EXTERNAL_STOP')
    if failure=='stop_failed':sys.exit(1)
    if failure!='stop_ineffective':(root/'pid').write_text('absent')
    sys.exit(0)
if args[:3]==['shell','am','instrument']:
    seed='--no-restart' in args
    owner='AcceptedCreditRestartSeedTest' if seed else 'AcceptedCreditRestartVerifyTest'
    method='seed' if seed else 'verify'
    event('SEED' if seed else 'VERIFY')
    excludes=args[args.index('notClass')+1].split(',')
    assert 'paint.anpaint.android.FutureTest' in excludes
    assert 'paint.anpaint.android.EditorDeviceTest' in excludes
    if seed:assert args[args.index('waitForActivitiesToComplete')+1]=='false'
    else:
        assert state()=='absent'
        assert 'waitForActivitiesToComplete' not in args
        (root/'pid').write_text('456')
    for code in (1,0):
        print('INSTRUMENTATION_STATUS: class=paint.anpaint.android.'+owner)
        print('INSTRUMENTATION_STATUS: test='+method)
        print('INSTRUMENTATION_STATUS: numtests=1')
        print('INSTRUMENTATION_STATUS_CODE: '+str(code))
    if not (seed and failure=='truncated'):
        print('INSTRUMENTATION_CODE: -1')
    if seed:
        event('SEED_FINISHED');(root/'seed-finished').touch()
        if failure=='died':(root/'pid').write_text('absent')
        if failure=='changed':(root/'pid').write_text('456')
    sys.exit(0)
raise SystemExit('Unhandled fake adb command: '+repr(args))
''')
            fake.chmod(0o700)
            env={**os.environ,'CI_SCRIPT':str(SCRIPT),'CI_TEST_DIR':str(root),
                 'BOUNDARY_FAILURE':failure,'HARNESS_SETUP_DELAY':str(setup_delay)}
            if failure=='hung_pid':
                # Timestamp completion in the same waiting process, after the real
                # GNU timeout has reaped its child. This excludes all earlier setup.
                shim=root/'bin/timeout';shim.parent.mkdir()
                shim.write_text('#!'+sys.executable+'\n'+r'''
import json, os, subprocess, sys, time
from pathlib import Path
started=time.monotonic()
result=subprocess.run([os.environ['REAL_TIMEOUT'],*sys.argv[1:]])
with (Path(os.environ['CI_TEST_DIR'])/'timing.jsonl').open('a') as out:
    out.write(json.dumps(dict(event='TIMED_COMMAND_COMPLETED',monotonic=time.monotonic(),
                             started_monotonic=started,returncode=result.returncode,command=sys.argv[1:]))+'\n')
raise SystemExit(result.returncode)
''')
                shim.chmod(0o700)
                env.update(REAL_TIMEOUT=shutil.which('timeout'),PATH=str(shim.parent)+os.pathsep+env['PATH'])
            command='''
source "$CI_SCRIPT"
report="$CI_TEST_DIR/report"
adb="$CI_TEST_DIR/adb"
variant=debug
run_credit_restart_regression || exit "$?"
'''
            started=time.monotonic()
            process=subprocess.Popen(['bash','-c',command],cwd=root,text=True,stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,env=env,start_new_session=True)
            try:
                stdout,stderr=process.communicate(timeout=HARNESS_WATCHDOG_SECONDS)
            except subprocess.TimeoutExpired as watchdog_error:
                # GNU timeout creates child process groups. Kill this isolated test
                # session, not just its shell, so inherited output pipes cannot hang.
                killed=[]
                for entry in sorted(Path('/proc').iterdir(),key=lambda p:p.name,reverse=True):
                    if not entry.name.isdigit():continue
                    pid=int(entry.name)
                    try:
                        if os.getsid(pid)==process.pid:
                            os.kill(pid,signal.SIGKILL);killed.append(pid)
                    except ProcessLookupError:pass
                cleanup_timed_out=False
                try:
                    stdout,stderr=process.communicate(timeout=HARNESS_CLEANUP_ALLOWANCE_SECONDS)
                except subprocess.TimeoutExpired as cleanup_error:
                    # A second timeout must not escape TemporaryDirectory before
                    # diagnostics survive. TimeoutExpired output may be bytes even
                    # when Popen was created with text=True.
                    cleanup_timed_out=True
                    def text(value):return value.decode(errors='replace') if isinstance(value,bytes) else (value or '')
                    stdout=text(cleanup_error.output if cleanup_error.output is not None else watchdog_error.output)
                    stderr=text(cleanup_error.stderr if cleanup_error.stderr is not None else watchdog_error.stderr)
                (root/'stdout.log').write_text(stdout);(root/'stderr.log').write_text(stderr)
                (root/'watchdog.json').write_text(json.dumps(dict(failure=failure,
                    elapsed_seconds=time.monotonic()-started,watchdog_seconds=HARNESS_WATCHDOG_SECONDS,
                    killed_session_pids=killed,cleanup_timed_out=cleanup_timed_out),indent=2)+'\n')
                retained=Path(tempfile.mkdtemp(prefix='anpaint-credit-boundary-failure-'))
                shutil.copytree(root,retained,dirs_exist_ok=True)
                events=(root/'events').read_text() if (root/'events').exists() else 'No fake-ADB events recorded'
                self.fail(f'Host harness watchdog expired; production phase is not inferred. '
                          f'Retained evidence: {retained}\n{events}')
            result=subprocess.CompletedProcess(process.args,process.returncode,stdout,stderr)
            self.boundary_timings=[json.loads(line) for line in (root/'timing.jsonl').read_text().splitlines()]
            events=(root/'events').read_text()
            phase_root=root/'report/app/accepted-credit-restart'
            self.assertFalse((phase_root/'verify/TEST-stale.xml').exists())
            boundary=(phase_root/'boundary.log').read_text()
            status=(phase_root/'verify-status.txt').read_text()
            coverage=json.loads((phase_root/'coverage.json').read_text()) if (phase_root/'coverage.json').exists() else None
            return result,events,boundary,status,coverage

    def test_complete_seed_precedes_stop_and_fresh_normal_verify_with_full_union(self):
        result,events,boundary,status,coverage=self.run_boundary()
        self.assertEqual(result.returncode,0,result.stdout+result.stderr+boundary)
        self.assertLess(events.index('SEED_FINISHED'),events.index('EXTERNAL_STOP'))
        self.assertLess(events.index('EXTERNAL_STOP'),events.index('VERIFY'))
        self.assertIn('Complete successful seed report verified; PID=123',boundary)
        self.assertIn('Verified target PID absent',boundary)
        self.assertIn('COMPLETED',status)
        self.assertEqual(coverage['completed_tests'],4)

    def test_failed_seed_or_dead_changed_process_never_reaches_external_stop(self):
        for failure in ('truncated','died','changed','transport','timeout','gallery_closed','die_after_gallery'):
            with self.subTest(failure=failure):
                result,events,boundary,status,coverage=self.run_boundary(failure)
                self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertNotIn('EXTERNAL_STOP',events)
                self.assertNotIn('VERIFY',events)
                self.assertIn('NOT RUN',status)
                self.assertIsNone(coverage)
                if failure=='timeout':
                    self.assertEqual(result.returncode,124)
                    self.assertIn('FAULT_IMMEDIATE124_ENTERED',events)
                    self.assertLess(events.index('SEED_FINISHED'),events.index('FAULT_IMMEDIATE124_ENTERED'))

    def test_positive_pid_absence_is_required_before_verify(self):
        result,events,boundary,status,coverage=self.run_boundary('stop_ineffective')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('EXTERNAL_STOP',events)
        self.assertNotIn('VERIFY',events)
        self.assertIn('process remains after force-stop',boundary)
        self.assertIn('NOT RUN',status)
        self.assertIsNone(coverage)

    def test_hung_boundary_command_obeys_actual_ten_second_deadline(self):
        result,events,boundary,status,coverage=self.run_boundary('hung_pid')
        self.assertEqual(result.returncode,124)
        entry=next(row for row in self.boundary_timings if row['event']=='FAULT_HUNG_PID_ENTERED')
        completion=next(row for row in self.boundary_timings if row['event']=='TIMED_COMMAND_COMPLETED'
                        and row['monotonic']>entry['monotonic'])
        self.assertEqual(completion['returncode'],124)
        self.assertIn('10s',completion['command'])
        elapsed=completion['monotonic']-entry['monotonic']
        command_elapsed=completion['monotonic']-completion['started_monotonic']
        self.assertGreater(elapsed,0)
        self.assertLessEqual(elapsed,command_elapsed)
        self.assertGreaterEqual(command_elapsed,9)
        self.assertLess(command_elapsed,14)
        self.assertNotIn('EXTERNAL_STOP',events)
        self.assertNotIn('VERIFY',events)
        self.assertIn('NOT RUN',status)
        self.assertIsNone(coverage)

    def test_failed_force_stop_never_launches_verification(self):
        result,events,boundary,status,coverage=self.run_boundary('stop_failed')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('EXTERNAL_STOP',events)
        self.assertNotIn('VERIFY',events)
        self.assertIn('NOT RUN',status)
        self.assertIsNone(coverage)

    def test_benign_slow_setup_preserves_complete_boundary_and_inventory(self):
        # This one delay intentionally exceeds the obsolete fifteen-second whole
        # harness watchdog. It does not consume the later PID command's budget.
        result,events,boundary,status,coverage=self.run_boundary(setup_delay=16)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr+boundary)
        self.assertEqual(events.count('BENIGN_SETUP_DELAY_ENTERED'),1)
        self.assertEqual(events.count('BENIGN_SETUP_DELAY_COMPLETED'),1)
        entry=next(row for row in self.boundary_timings if row['event']=='BENIGN_SETUP_DELAY_ENTERED')
        completion=next(row for row in self.boundary_timings if row['event']=='BENIGN_SETUP_DELAY_COMPLETED')
        self.assertGreaterEqual(completion['monotonic']-entry['monotonic'],16)
        self.assertLess(events.index('BENIGN_SETUP_DELAY_COMPLETED'),events.index('SEED_FINISHED'))
        self.assertLess(events.index('SEED_FINISHED'),events.index('EXTERNAL_STOP'))
        self.assertLess(events.index('EXTERNAL_STOP'),events.index('VERIFY'))
        self.assertNotIn('FAULT_',events)
        self.assertIn('Verified target PID absent',boundary)
        self.assertIn('COMPLETED',status)
        self.assertTrue(coverage['success'])
        self.assertEqual(coverage['declared_tests'],4)
        self.assertEqual(coverage['completed_tests'],4)
        self.assertEqual({tuple(identity) for identity in coverage['completed']},{
            ('paint.anpaint.android.EditorDeviceTest','ordinary'),
            ('paint.anpaint.android.FutureTest','future'),
            ('paint.anpaint.android.AcceptedCreditRestartSeedTest','seed'),
            ('paint.anpaint.android.AcceptedCreditRestartVerifyTest','verify')})

    def test_secondary_cleanup_timeout_still_retains_partial_diagnostics(self):
        process=Mock(pid=-1)
        process.communicate.side_effect=[
            subprocess.TimeoutExpired('synthetic harness',60,output=b'seed output',stderr=b'first error'),
            subprocess.TimeoutExpired('synthetic cleanup',5,output=b'partial cleanup output',stderr=b'partial cleanup error')]
        # No real child is started; an impossible session ID prevents any signals.
        with patch(__name__+'.subprocess.Popen',return_value=process):
            with self.assertRaises(AssertionError) as raised:
                self.run_boundary('timeout')
        retained=Path(str(raised.exception).split('Retained evidence: ',1)[1].splitlines()[0])
        try:
            metadata=json.loads((retained/'watchdog.json').read_text())
            self.assertTrue(metadata['cleanup_timed_out'])
            self.assertEqual(metadata['killed_session_pids'],[])
            self.assertEqual((retained/'stdout.log').read_text(),'partial cleanup output')
            self.assertEqual((retained/'stderr.log').read_text(),'partial cleanup error')
        finally:shutil.rmtree(retained)

    def test_host_watchdog_retains_events_and_phase_diagnostics(self):
        with patch(__name__+'.HARNESS_WATCHDOG_SECONDS',0.01):
            with self.assertRaises(AssertionError) as raised:
                self.run_boundary('timeout')
        retained=Path(str(raised.exception).split('Retained evidence: ',1)[1].splitlines()[0])
        try:
            self.assertTrue((retained/'watchdog.json').is_file())
            self.assertTrue((retained/'stdout.log').is_file())
            self.assertTrue((retained/'stderr.log').is_file())
            self.assertTrue(json.loads((retained/'watchdog.json').read_text())['killed_session_pids'])
        finally:shutil.rmtree(retained)

    def test_api30_omission_and_phase_deadlines_are_explicit(self):
        source=SCRIPT.read_text()
        self.assertIn('if test "$TEST_API" = 35',source)
        self.assertIn('API35-only; both phase classes excluded on API30',source)
        self.assertEqual(source.count('--timeout-seconds 60'),2)
        self.assertEqual(source.count('--timeout-seconds 180'),2)
        self.assertIn('credit_restart_command \"Force-stop',source.replace('"','\"'))


if __name__ == '__main__':
    unittest.main()
