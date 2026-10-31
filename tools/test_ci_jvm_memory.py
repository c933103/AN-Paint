"""Memory observation must not hide failures, alter scope, or touch workloads."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import sys
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('jvm_memory', ROOT / 'tools/ci_observe_jvm_memory.py')
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)


class JvmMemoryTest(unittest.TestCase):
    def test_process_selection_excludes_observer_unrelated_and_reused_pids(self):
        def row(parent, start):
            return {'parent': parent, 'start_ticks': start, 'rss_kib': 4, 'hwm_kib': 8}
        frame = {1: row(0, 10), 2: row(1, 20), 3: row(2, 30),
                 4: row(1, 40), 5: row(0, 50), 6: row(0, 61)}
        known = {1: 10, 6: 60}
        self.assertEqual(set(memory.select_owned(frame, 1, known, 4)), {2, 3})
        frame[2]['parent'] = 99  # Already observed detached child remains bound.
        self.assertEqual(set(memory.select_owned(frame, 1, known, 4)), {2, 3})
        frame[2]['start_ticks'] = 21  # Reused detached PID is not the old child.
        frame.pop(3)
        self.assertEqual(memory.select_owned(frame, 1, known, 4), {})

    def test_proc_snapshot_and_memory_units(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / '23').mkdir()
            # stat fields after comm: state, ppid, ... starttime (index 19).
            fields = ['S', '7'] + ['0'] * 17 + ['12345'] + ['0'] * 4
            (root / '23/stat').write_text('23 (name with ) brackets) ' + ' '.join(fields))
            (root / '23/status').write_text('Name:\ttest\nVmRSS:\t123 kB\nVmHWM:\t456 kB\n')
            (root / 'meminfo').write_text('MemTotal: 999 kB\nMemAvailable: 789 kB\n')
            self.assertEqual(memory.snapshot(root), {23: {'parent': 7, 'start_ticks': 12345, 'rss_kib': 123, 'hwm_kib': 456}})
            self.assertEqual(memory.available_kib(root), 789)

    def test_jvm_probe_preserves_success_failure_output_and_measurement(self):
        for status in (0, 7):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary); (root / 'tools').mkdir()
                for name in ('ci_run_timed.sh', 'ci_observe_jvm_memory.py'):
                    shutil.copy(ROOT / 'tools' / name, root / 'tools')
                result = subprocess.run(['bash', 'tools/ci_run_timed.sh', 'jvm',
                    'bash', '-c', f'echo retained-output; sleep .25; exit {status}'],
                    cwd=root, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, status, result.stderr)
                self.assertEqual(result.stdout, 'retained-output\n')
                reports = root / 'build/reports/ci-phases'
                receipt = json.loads((reports / 'jvm.memory.json').read_text())
                self.assertTrue(receipt['completed'])
                self.assertGreaterEqual(receipt['samples'], 2)
                self.assertGreater(receipt['peak_sampled_rss_kib'], 0)
                self.assertGreater(receipt['minimum_host_available_kib'], 0)
                self.assertEqual((reports / 'jvm.log').read_text(), result.stdout)
                self.assertIn(f'exit_status={status}', (reports / 'jvm.time').read_text())
                self.assertTrue(any(value > 0 for value in receipt['per_process_hwm_kib'].values()))

    def test_observer_failure_never_converts_command_to_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / 'tools').mkdir()
            shutil.copy(ROOT / 'tools/ci_run_timed.sh', root / 'tools')
            (root / 'tools/ci_observe_jvm_memory.py').write_text('raise SystemExit(19)\n')
            result = subprocess.run(['bash', 'tools/ci_run_timed.sh', 'jvm', 'touch', 'command-ran'],
                                    cwd=root, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 125)
            self.assertFalse((root / 'command-ran').exists())

    def test_reused_checkout_startup_failure_replaces_old_success_and_failed_receipts(self):
        for prior_status in (0, 7):
            with self.subTest(prior_status=prior_status), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary); (root / 'tools').mkdir()
                for name in ('ci_run_timed.sh', 'ci_observe_jvm_memory.py'):
                    shutil.copy(ROOT / 'tools' / name, root / 'tools')
                before = subprocess.run(['bash', 'tools/ci_run_timed.sh', 'jvm', 'bash', '-c',
                    f'echo previous-invocation; exit {prior_status}'], cwd=root,
                    capture_output=True, text=True, timeout=5)
                self.assertEqual(before.returncode, prior_status, before.stderr)
                reports = root / 'build/reports/ci-phases'
                prior = (reports / 'jvm.time').read_text()
                self.assertIn(f'workload_exit_status={prior_status}\n', prior)
                self.assertTrue((reports / 'jvm.memory.json').exists())
                (reports / 'jvm.ended-at').write_text('old terminal marker\n')
                real = str(ROOT / 'tools/ci_observe_jvm_memory.py')
                (root / 'tools/ci_observe_jvm_memory.py').write_text(
                    'import sys,runpy\n'
                    f'if "--stop-pid" in sys.argv: runpy.run_path({real!r},run_name="__main__")\n'
                    'raise SystemExit(19)\n')
                after = subprocess.run(['bash', 'tools/ci_run_timed.sh', 'jvm', 'touch', 'must-not-run'],
                                       cwd=root, capture_output=True, text=True, timeout=5)
                self.assertEqual(after.returncode, 125, after.stderr)
                self.assertFalse((root / 'must-not-run').exists())
                current = dict(line.split('=', 1) for line in (reports / 'jvm.time').read_text().splitlines())
                self.assertEqual(current, {'workload_exit_status': 'unrun', 'observer_exit_status': '19',
                    'observer_cleanup_complete': 'true', 'exit_status': '125'})
                self.assertEqual((reports / 'jvm.log').read_text(), '')
                self.assertFalse((reports / 'jvm.memory.json').exists())
                self.assertRegex((reports / 'jvm.ended-at').read_text(), r'^\d{4}-\d\d-\d\dT')

    def cancellation_case(self, force_kill):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / 'tools').mkdir(); (root / 'owner').mkdir()
            for name in ('ci_run_timed.sh', 'ci_observe_jvm_memory.py'):
                shutil.copy(ROOT / 'tools' / name, root / 'tools')
            # Reuse the existing subreaper in a separate report directory: it
            # owns only this invocation and reaps every cancelled descendant.
            workload = ('import os,signal,time; from pathlib import Path; '
                'Path("workload.pid").write_text(str(os.getpid())); '
                'print("partial-jvm",flush=True)\n'
                'while not Path("stop-now").exists(): time.sleep(.01)\n'
                'os.killpg(os.getpgrp(),signal.SIGSTOP)\n')
            owner = subprocess.Popen([sys.executable, str(ROOT / 'tools/ci_run_process_group.py'),
                '--timeout-seconds', '5', '--kill-after-seconds', '3', '--',
                'bash', '-c', 'cd ..; exec "$@"', 'owned-jvm', 'bash',
                'tools/ci_run_timed.sh', 'jvm', sys.executable, '-c', workload],
                cwd=root / 'owner', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            reports = root / 'build/reports/ci-phases'
            def ready(predicate):
                deadline = time.monotonic() + 5
                while not predicate() and owner.poll() is None and time.monotonic() < deadline:
                    time.sleep(.01)
                self.assertTrue(predicate(), 'Workload readiness must precede cancellation')
            try:
                ready(lambda: (root / 'workload.pid').exists() and
                    (reports / 'jvm.log').exists() and
                    (reports / 'jvm.log').read_text() == 'partial-jvm\n')
                pid = int((root / 'workload.pid').read_text())
                if force_kill:
                    # A stopped owned group cannot run EXIT traps. The owner
                    # must KILL/reap it and retain explicitly incomplete evidence.
                    (root / 'stop-now').touch()
                    ready(lambda: Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[0] == 'T')
                owner.send_signal(signal.SIGTERM)
                out, err = owner.communicate(timeout=10)
            finally:
                if owner.poll() is None:
                    owner.send_signal(signal.SIGTERM)
                    owner.communicate(timeout=10)
            self.assertEqual(owner.returncode, 143, err)
            owner_reports = root / 'owner/build/reports/ci-phases'
            lifecycle = dict(line.split('=', 1) for line in (owner_reports / 'python.lifecycle').read_text().splitlines())
            self.assertEqual(lifecycle['reason'], 'signal')
            self.assertEqual(lifecycle['forced_kill'], str(force_kill).lower())
            self.assertEqual(lifecycle['owned_children_remaining'], '0')
            self.assertEqual(lifecycle['cleanup_complete'], 'true')
            self.assertEqual(lifecycle['output_complete'], 'true')
            self.assertIn('exit_status=143\n', (owner_reports / 'python.time').read_text())
            self.assertIn('partial-jvm\n', out)
            self.assertEqual((reports / 'jvm.log').read_text(), 'partial-jvm\n')
            receipt = dict(line.split('=', 1) for line in (reports / 'jvm.time').read_text().splitlines() if '=' in line)
            if force_kill:
                self.assertNotIn('exit_status', receipt)
                self.assertFalse((reports / 'jvm.ended-at').exists())
                self.assertFalse(json.loads((reports / 'jvm.memory.json').read_text())['completed'])
            else:
                self.assertNotEqual(receipt['exit_status'], '0')
                self.assertNotEqual(receipt['workload_exit_status'], '0')
                self.assertEqual(receipt['observer_cleanup_complete'], 'true')
                self.assertTrue((reports / 'jvm.ended-at').is_file())
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)

    def test_cancelled_jvm_remains_failure_with_partial_output(self):
        self.cancellation_case(force_kill=False)

    def test_force_killed_jvm_retains_incomplete_non_success_evidence(self):
        self.cancellation_case(force_kill=True)

    def test_bad_proc_record_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / '23').mkdir()
            (root / '23/stat').write_text('malformed')
            with self.assertRaises((IndexError, ValueError)):
                memory.snapshot(root)

    def test_two_forks_keep_workers_heap_scope_and_deadlines(self):
        gradle = (ROOT / 'Paintroid/build.gradle').read_text()
        self.assertIn('maxParallelForks = 2', gradle)
        self.assertIn("maxHeapSize = '2g'", gradle)
        self.assertNotIn('forkEvery', gradle)
        workflow = (ROOT / '.github/workflows/android.yml').read_text()
        jvm = workflow.split('      - name: Run JVM regression tests\n', 1)[1].split('      - name:', 1)[0]
        self.assertIn('timeout-minutes: 20', jvm)
        self.assertIn('--max-workers=2', jvm)
        self.assertNotIn('--tests', jvm)
        self.assertNotIn('continue-on-error', jvm)

    def test_mid_run_observer_failure_is_in_terminal_receipt_and_retains_workload_failure(self):
        for workload_status in (0, 7):
            with self.subTest(workload_status=workload_status), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary); (root / 'tools').mkdir()
                shutil.copy(ROOT / 'tools/ci_run_timed.sh', root / 'tools')
                real = str(ROOT / 'tools/ci_observe_jvm_memory.py')
                (root / 'tools/ci_observe_jvm_memory.py').write_text(
                    'import sys,runpy,time\nfrom pathlib import Path\n'
                    f'if "--stop-pid" in sys.argv: runpy.run_path({real!r},run_name="__main__")\n'
                    'Path(sys.argv[-1]).write_text("{}")\ntime.sleep(.1)\nraise SystemExit(19)\n')
                result = subprocess.run(['bash', 'tools/ci_run_timed.sh', 'jvm', 'bash', '-c',
                    f'echo actual-workload; sleep .25; exit {workload_status}'], cwd=root,
                    capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, workload_status or 125, result.stderr)
                reports = root / 'build/reports/ci-phases'
                receipt = dict(line.split('=', 1) for line in (reports / 'jvm.time').read_text().splitlines())
                self.assertEqual(receipt['workload_exit_status'], str(workload_status))
                self.assertEqual(receipt['observer_exit_status'], '19')
                self.assertEqual(receipt['exit_status'], str(workload_status or 125))
                self.assertEqual(receipt['observer_cleanup_complete'], 'true')
                self.assertTrue((reports / 'jvm.ended-at').is_file())
                self.assertEqual((reports / 'jvm.log').read_text(), 'actual-workload\n')

    def test_unresponsive_observer_has_bounded_owned_cleanup_and_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / 'tools').mkdir()
            shutil.copy(ROOT / 'tools/ci_run_timed.sh', root / 'tools')
            real = str(ROOT / 'tools/ci_observe_jvm_memory.py')
            (root / 'tools/ci_observe_jvm_memory.py').write_text(
                'import sys,runpy,time,signal,os\nfrom pathlib import Path\n'
                f'if "--stop-pid" in sys.argv: runpy.run_path({real!r},run_name="__main__")\n'
                'signal.signal(signal.SIGTERM,signal.SIG_IGN)\n'
                'Path("observer.pid").write_text(str(os.getpid()))\n'
                'Path(sys.argv[-1]).write_text("{}")\ntime.sleep(30)\n')
            started = time.monotonic()
            result = subprocess.run(['bash', 'tools/ci_run_timed.sh', 'jvm', 'true'],
                                    cwd=root, capture_output=True, text=True, timeout=5)
            self.assertLess(time.monotonic() - started, 4)
            self.assertEqual(result.returncode, 125, result.stderr)
            reports = root / 'build/reports/ci-phases'
            cleanup = json.loads((reports / 'jvm.observer-cleanup.json').read_text())
            self.assertTrue(cleanup['cleanup_complete']); self.assertTrue(cleanup['forced_kill'])
            receipt = dict(line.split('=', 1) for line in (reports / 'jvm.time').read_text().splitlines())
            self.assertEqual(receipt['workload_exit_status'], '0')
            self.assertEqual(receipt['observer_exit_status'], '137')
            self.assertEqual(receipt['exit_status'], '125')
            with self.assertRaises(ProcessLookupError):
                os.kill(int((root / 'observer.pid').read_text()), 0)

    def test_cleanup_identity_mismatch_does_not_signal_another_process(self):
        with tempfile.TemporaryDirectory() as temporary:
            child = subprocess.Popen(['sleep', '10'])
            try:
                start = memory.snapshot()[child.pid]['start_ticks']
                out = Path(temporary) / 'cleanup.json'
                self.assertEqual(memory.stop_observer(child.pid, start + 1, os.getpid(), out), 125)
                self.assertIsNone(child.poll())
                self.assertFalse(json.loads(out.read_text())['cleanup_complete'])
            finally:
                child.terminate(); child.wait(timeout=2)


if __name__ == '__main__':
    unittest.main()
