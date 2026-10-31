"""Deterministic deadline/session/partial-transfer tests, not device evidence."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import pull_device_evidence as pull

BOOT = '12345678-1234-1234-1234-123456789abc'
REMOTE = '/sdcard/Download/anpaint-ci-vertical-evidence'


class PullEvidenceTest(unittest.TestCase):
    def run_collection(self, fault='', *, stale=False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        output = root / 'export'
        if stale:
            output.mkdir()
            (output / 'original').write_bytes(b'unchanged')
        now = [0.0]
        calls = []
        pulls = [0]
        identities = [0]

        def command(args, **kwargs):
            self.assertEqual(args[:3], ['adb', '-s', 'emulator-5554'])
            self.assertLessEqual(kwargs['timeout'], pull.BUDGET_SECONDS - now[0])
            calls.append(args[3:])
            result = subprocess.CompletedProcess(args, 0, '')
            if args[3] == 'shell':
                identities[0] += 1
                result.stdout = f'{BOOT}\n35\nx86_64\n'
                if fault == 'wrong_session' and identities[0] == 2:
                    result.stdout = result.stdout.replace(BOOT, '87654321-1234-1234-1234-123456789abc')
                if fault == 'wrong_sdk':
                    result.stdout = result.stdout.replace('35', '30')
                if fault == 'wrong_abi':
                    result.stdout = result.stdout.replace('x86_64', 'x86')
                if fault == 'after_pull_identity' and identities[0] == 2:
                    result.returncode = 1
                if fault.startswith('initial_offline') and identities[0] == 1:
                    result.returncode = 1
                if fault == 'initial_offline_permanent':
                    result.returncode = 1
            elif args[3] == 'pull':
                pulls[0] += 1
                target = Path(args[-1])
                self.assertFalse(target.exists(), 'Never merge attempts or reuse old exports')
                target.mkdir()
                if ((pulls[0] == 1 and fault not in ('', 'after_pull_identity', 'initial_offline'))
                        or fault == 'permanent'):
                    (target / 'partial.zip').write_bytes(b'original incomplete transfer')
                    kwargs['stdout'].write('original transport failure\n')
                    result.returncode = 1
                    if fault in ('deadline', 'late_success'):
                        now[0] += kwargs['timeout']
                        if fault == 'deadline':
                            raise subprocess.TimeoutExpired(args, kwargs['timeout'])
                        result.returncode = 0
                else:
                    (target / 'complete.zip').write_bytes(b'new complete transfer')
            elif args[3:] == ['wait-for-device']:
                if fault in ('wait_deadline', 'initial_offline_deadline'):
                    now[0] += kwargs['timeout']
                    raise subprocess.TimeoutExpired(args, kwargs['timeout'])
                now[0] += 0.5
            else:
                self.fail(f'Unauthorized command {args!r}')
            return result

        with patch.object(pull.time, 'monotonic', side_effect=lambda: now[0]), \
                patch.object(pull.subprocess, 'run', side_effect=command):
            result = pull.collect('adb', 'emulator-5554', BOOT, 35, 'x86_64',
                                  os.getpid(), REMOTE, output)
        receipt = output.with_name('export-transfer.json')
        return result, output, calls, json.loads(receipt.read_text()) if receipt.exists() else None

    def test_immediate_success_has_no_wait_or_second_pull(self):
        result, output, calls, receipt = self.run_collection()
        self.assertEqual(result, 0)
        self.assertTrue(receipt['transport_complete'])
        self.assertEqual(receipt['accepted_attempt'], 1)
        self.assertEqual([c[0] for c in calls], ['shell', 'pull', 'shell'])
        self.assertEqual((output / 'complete.zip').read_bytes(), b'new complete transfer')

    def test_transient_recovery_preserves_failed_bytes_and_never_merges(self):
        result, output, calls, receipt = self.run_collection('transient')
        self.assertEqual(result, 0)
        self.assertEqual([c[0] for c in calls], ['shell', 'pull', 'wait-for-device', 'shell', 'pull', 'shell'])
        self.assertEqual(set(p.name for p in output.iterdir()), {'complete.zip'})
        attempts = output.with_name('export-attempts')
        self.assertEqual((attempts / 'attempt-1/partial.zip').read_bytes(), b'original incomplete transfer')
        self.assertIn('original transport failure', (attempts / 'pull-1.log').read_text())
        self.assertEqual(receipt['accepted_attempt'], 2)
        self.assertEqual([e['exit_status'] for e in receipt['commands']], [0, 1, 0, 0, 0, 0])

    def test_deadline_or_late_success_never_recovers_or_promotes(self):
        for fault in ('deadline', 'late_success', 'wait_deadline'):
            with self.subTest(fault=fault):
                result, output, calls, receipt = self.run_collection(fault)
                self.assertEqual(result, 124)
                self.assertFalse(output.exists())
                self.assertFalse(receipt['transport_complete'])
                self.assertEqual(sum(c[0] == 'pull' for c in calls), 1)
                if fault != 'wait_deadline':
                    self.assertNotIn(['wait-for-device'], calls)

    def test_changed_session_or_identity_never_supplies_evidence(self):
        for fault in ('wrong_session', 'wrong_sdk', 'wrong_abi', 'after_pull_identity'):
            with self.subTest(fault=fault):
                result, output, calls, receipt = self.run_collection(fault)
                self.assertEqual(result, 1)
                self.assertFalse(output.exists())
                self.assertFalse(receipt['transport_complete'])
                self.assertLessEqual(sum(c[0] == 'pull' for c in calls), 1)

    def test_permanent_failure_has_only_two_preserved_attempts(self):
        result, output, calls, receipt = self.run_collection('permanent')
        self.assertEqual(result, 1)
        self.assertFalse(output.exists())
        self.assertFalse(receipt['transport_complete'])
        self.assertEqual(sum(c[0] == 'pull' for c in calls), 2)
        for number in (1, 2):
            self.assertTrue((output.with_name('export-attempts') / f'attempt-{number}/partial.zip').is_file())

    def test_stale_export_is_not_overwritten(self):
        result, output, calls, receipt = self.run_collection(stale=True)
        self.assertEqual(result, 1)
        self.assertEqual(calls, [])
        self.assertIsNone(receipt)
        self.assertEqual((output / 'original').read_bytes(), b'unchanged')

    def test_initially_offline_transport_can_use_the_same_single_recovery(self):
        result, output, calls, receipt = self.run_collection('initial_offline')
        self.assertEqual(result, 0)
        self.assertEqual([c[0] for c in calls], ['shell', 'wait-for-device', 'shell', 'pull', 'shell'])
        self.assertTrue(receipt['transport_complete'])
        self.assertEqual(receipt['accepted_attempt'], 1)
        self.assertTrue(output.is_dir())

    def test_initial_recovery_does_not_allow_another_recovery_or_repull(self):
        for fault, status, pulls in (('initial_offline_permanent', 1, 0),
                                     ('initial_offline_deadline', 124, 0),
                                     ('initial_offline_then_pull_fails', 1, 1)):
            with self.subTest(fault=fault):
                result, output, calls, receipt = self.run_collection(fault)
                self.assertEqual(result, status)
                self.assertEqual(sum(c[0] == 'wait-for-device' for c in calls), 1)
                self.assertEqual(sum(c[0] == 'pull' for c in calls), pulls)
                self.assertFalse(output.exists())
                self.assertFalse(receipt['transport_complete'])

    def test_dead_emulator_is_rejected_before_any_adb_command(self):
        with patch.object(pull.os, 'kill', side_effect=ProcessLookupError('original emulator exited')):
            result, output, calls, receipt = self.run_collection()
        self.assertEqual(result, 1)
        self.assertEqual(calls, [])
        self.assertFalse(output.exists())
        self.assertFalse(receipt['transport_complete'])

    def test_emulator_death_during_final_identity_prevents_promotion(self):
        with patch.object(pull.os, 'kill', side_effect=[None] * 5 + [ProcessLookupError('emulator exited')]):
            result, output, calls, receipt = self.run_collection()
        self.assertEqual(result, 1)
        self.assertEqual([c[0] for c in calls], ['shell', 'pull', 'shell'])
        self.assertFalse(output.exists())
        self.assertFalse(receipt['transport_complete'])

    def test_signal_reaps_the_owned_hung_adb_client_without_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adb = root / 'adb'
            pid_file = root / 'client.pid'
            # Publish readiness only after the complete PID is closed, before signalling.
            adb.write_text('#!' + sys.executable + '\nimport os,time\n'
                           f'with open({str(pid_file)+".tmp"!r}, "w") as ready: ready.write(str(os.getpid()))\n'
                           f'os.replace({str(pid_file)+".tmp"!r}, {str(pid_file)!r})\n'
                           'time.sleep(30)\n')
            adb.chmod(0o700)
            command = [sys.executable, str(Path(pull.__file__)), '--adb', str(adb),
                       '--serial', 'emulator-5554', '--boot-id', BOOT, '--sdk', '35',
                       '--abi', 'x86_64', '--emulator-pid', str(os.getpid()),
                       '--remote', REMOTE, '--output', str(root / 'export')]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                until = time.monotonic() + 5
                while not pid_file.exists() and time.monotonic() < until:
                    time.sleep(0.01)
                self.assertTrue(pid_file.exists(), 'Actual ADB client must start')
                client = int(pid_file.read_text())
                process.terminate()
                _, stderr = process.communicate(timeout=3)
                self.assertEqual(process.returncode, 124, stderr)
                with self.assertRaises(ProcessLookupError):
                    os.kill(client, 0)
                self.assertFalse((root / 'export').exists())
                receipt = json.loads((root / 'export-transfer.json').read_text())
                self.assertFalse(receipt['transport_complete'])
                self.assertEqual(len(receipt['commands']), 1)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.communicate(timeout=3)


if __name__ == '__main__':
    unittest.main()
