"""Execute the real EXIT collector against synthetic exports and a fake ADB.

The real capture validators run. These fixtures prove host lifecycle contracts,
not installed screenshot appearance or the cause of a real ADB disconnect.
"""
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

from dialog_evidence_transport import METHOD_SCREENS
from test_dialog_evidence_transport import summary, write_archive
from test_vertical_control_reachability import fixture as reachability_fixture
from test_vertical_evidence_transport import export_fixture
from vertical_locale_matrix import EXPECTED_SCREENSHOTS

ROOT = Path(__file__).resolve().parents[1]


class CaptureCleanupTest(unittest.TestCase):
    def run_cleanup(self, *, fault='', incoming=0, started=True, server_symlink=False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        report = root / 'report'
        report.mkdir()
        dialog = root / 'dialog'
        dialog.mkdir()
        for method in METHOD_SCREENS:
            write_archive(dialog, method)
        summary_path = report / 'app-dialog/androidTest-results/summary.json'
        summary_path.parent.mkdir(parents=True)
        summary_path.write_text(json.dumps(summary()))
        source = root / 'vertical-source'
        source.mkdir()
        reachability_fixture(source / 'reachability')
        for name in EXPECTED_SCREENSHOTS:
            size = (240, 120) if '-landscape-' in name else (120, 240)
            (source / name).write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' +
                                       struct.pack('>II', *size) + b'\0' * 9 + name.encode())
        if fault == 'vertical_matrix':
            names = sorted(EXPECTED_SCREENSHOTS)
            (source / names[1]).write_bytes((source / names[0]).read_bytes())
        if fault == 'reachability':
            path = next((source / 'reachability').glob('*.json'))
            value = json.loads(path.read_text())
            value['cancel_preserved_quality'] = False
            path.write_text(json.dumps(value))
        vertical = root / 'vertical'
        export_fixture(vertical, source=source)
        if fault == 'dialog_incomplete':
            next(dialog.glob('*.zip')).unlink()
        if fault == 'vertical_incomplete':
            next(vertical.glob('*.zip')).unlink()
        server = root / f'adb.{os.getuid()}.log'
        server_bytes = b'synthetic runner ADB diagnostics\n' * 4000
        if server_symlink:
            (root / 'other-log').write_bytes(server_bytes)
            server.symlink_to(root / 'other-log')
        else:
            server.write_bytes(server_bytes)
        adb = root / 'adb'
        adb.write_text('#!' + sys.executable + '\n' + r'''
import json, os, shutil, sys, time
from pathlib import Path
root = Path(os.environ['CLEANUP_ROOT'])
fault = os.environ['CLEANUP_FAULT']
args = sys.argv[1:]
with (root / 'events.jsonl').open('a') as out:
    out.write(json.dumps(args) + '\n')
if args[0] == 'pull':
    group = 'dialog' if args[1].endswith('dialog-evidence') else 'vertical'
    target = Path(args[2])
    target.mkdir(parents=True)
    if fault in (group + '_pull', 'both_pulls') or (root / 'offline').exists():
        (target / 'partial-export.zip').write_bytes(b'partial synthetic transfer')
        print('adb: error: failed to get feature set: device offline', file=sys.stderr)
        sys.exit(1)
    shutil.copytree(root / group, target, dirs_exist_ok=True)
    print(group + ' synthetic files pulled')
elif args == ['logcat', '-d']:
    print('partial synthetic logcat', flush=True)
    if fault in ('logcat', 'logcat_hang'):
        (root / 'offline').touch()
        if fault == 'logcat_hang':
            time.sleep(30)
        sys.exit(1)
elif args != ['emu', 'kill']:
    raise SystemExit('Unexpected command: ' + repr(args))
''')
        adb.chmod(0o700)
        script = r'''
source "$CI_SCRIPT"
report="$CLEANUP_ROOT/report"
adb="$CLEANUP_ROOT/adb"
emulator_pid=''
phase='Synthetic completed instrumentation'
TEST_API=35
dialog_started="$CLEANUP_STARTED"
vertical_started="$CLEANUP_STARTED"
timeout() {
    printf '%s\n' "$*" >> "$CLEANUP_ROOT/timeouts.log"
    command timeout "$@"
}
trap cleanup EXIT
exit "$CLEANUP_INCOMING"
'''
        result = subprocess.run(['bash', '-c', script], cwd=ROOT, capture_output=True,
                                text=True, timeout=25, env={**os.environ,
                                    'CI_SCRIPT': str(ROOT / 'tools/ci_emulator.sh'),
                                    'CLEANUP_ROOT': str(root), 'CLEANUP_FAULT': fault,
                                    'CLEANUP_INCOMING': str(incoming),
                                    'CLEANUP_STARTED': str(int(started)), 'TMPDIR': str(root)})
        events = [json.loads(line) for line in (root / 'events.jsonl').read_text().splitlines()]
        timeouts = (root / 'timeouts.log').read_text().splitlines()
        expected = ['pull', 'pull', 'logcat', 'emu'] if started else ['logcat', 'emu']
        self.assertEqual([event[0] for event in events], expected)
        self.assertEqual([line.split()[:2] for line in timeouts],
                         ([['--kill-after=3s', '15s']] * 2 if started else []) +
                         [['--kill-after=3s', '10s']] * 2)
        self.assertTrue((report / 'logcat.txt').is_file())
        self.assertEqual(events[-1], ['emu', 'kill'])
        return result, root, report, events, server_bytes

    def assert_successful_captures(self, report):
        for name in ('dialog-evidence.json', 'vertical-locale-export.json',
                     'vertical-locale-screenshots.json', 'vertical-control-reachability.json'):
            self.assertIs(json.loads((report / name).read_text())['success'], True)
        self.assertEqual(len(list((report / 'app/dialog-evidence').rglob('*.png'))), 39)
        self.assertEqual(len(list((report / 'app/vertical-locale-evidence').rglob('*.png'))), 96)

    def test_real_validators_accept_complete_exports_before_logcat_and_shutdown(self):
        result, _, report, _, server_bytes = self.run_cleanup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_successful_captures(report)
        self.assertEqual((report / 'collection-status.log').read_text(),
                         'dialog_pull_exit=0\nvertical_pull_exit=0\nlogcat_exit=0\nresult=0\n')
        self.assertEqual((report / 'adb-server-tail.log').read_bytes(), server_bytes[-65536:])

    def test_disrupting_logcat_cannot_preempt_required_exports(self):
        result, root, report, _, _ = self.run_cleanup(fault='logcat')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((root / 'offline').exists())
        self.assert_successful_captures(report)
        self.assertIn('logcat_exit=1\nresult=0', (report / 'collection-status.log').read_text())
        self.assertIn('partial synthetic logcat', (report / 'logcat.txt').read_text())

    def test_hung_logcat_keeps_original_deadline_and_does_not_erase_captures(self):
        result, _, report, _, _ = self.run_cleanup(fault='logcat_hang')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_successful_captures(report)
        self.assertIn('logcat_exit=124\nresult=0', (report / 'collection-status.log').read_text())
        self.assertIn('partial synthetic logcat', (report / 'logcat.txt').read_text())

    def test_each_failed_pull_is_attempted_once_and_keeps_partial_raw_export(self):
        for fault in ('dialog_pull', 'vertical_pull', 'both_pulls'):
            with self.subTest(fault=fault):
                result, _, report, _, _ = self.run_cleanup(fault=fault)
                self.assertEqual(result.returncode, 1)
                for group, folder, receipt in [('dialog', 'dialog-export', 'dialog-evidence.json'),
                                               ('vertical', 'vertical-locale-export', 'vertical-locale-export.json')]:
                    if fault in (group + '_pull', 'both_pulls'):
                        self.assertEqual((report / folder / 'partial-export.zip').read_bytes(),
                                         b'partial synthetic transfer')
                        self.assertFalse((report / receipt).exists())
                        self.assertIn(group + '_pull_exit=1', (report / 'collection-status.log').read_text())
                    else:
                        self.assertIs(json.loads((report / receipt).read_text())['success'], True)

    def test_incomplete_exports_fail_real_validators_without_removing_raw_files(self):
        for group, folder, receipt in [('dialog', 'dialog-export', 'dialog-evidence.json'),
                                      ('vertical', 'vertical-locale-export', 'vertical-locale-export.json')]:
            with self.subTest(group=group):
                result, root, report, _, _ = self.run_cleanup(fault=group + '_incomplete')
                self.assertEqual(result.returncode, 1)
                self.assertFalse((report / receipt).exists())
                self.assertEqual({p.name: p.read_bytes() for p in (root / group).iterdir()},
                                 {p.name: p.read_bytes() for p in (report / folder).iterdir()})
                self.assertIn('result=1', (report / 'collection-status.log').read_text())

    def test_matrix_and_native_reachability_failures_still_fail_after_transport(self):
        for fault, missing in [('vertical_matrix', 'vertical-locale-screenshots.json'),
                               ('reachability', 'vertical-control-reachability.json')]:
            with self.subTest(fault=fault):
                result, _, report, _, _ = self.run_cleanup(fault=fault)
                self.assertEqual(result.returncode, 1)
                self.assertIs(json.loads((report / 'vertical-locale-export.json').read_text())['success'], True)
                self.assertFalse((report / missing).exists())
                self.assertTrue(list((report / 'vertical-locale-export').glob('*.zip')))

    def test_cleanup_never_overwrites_existing_instrumentation_failure_status(self):
        for fault in ('', 'both_pulls', 'logcat'):
            with self.subTest(fault=fault):
                result, _, report, _, _ = self.run_cleanup(fault=fault, incoming=7)
                self.assertEqual(result.returncode, 7)
                self.assertIn('result=7', (report / 'collection-status.log').read_text())

    def test_unstarted_phases_are_not_pulled_or_accepted(self):
        result, _, report, _, _ = self.run_cleanup(started=False, fault='logcat')
        self.assertEqual(result.returncode, 0)
        self.assertFalse((report / 'dialog-evidence.json').exists())
        self.assertFalse((report / 'vertical-locale-export.json').exists())
        self.assertEqual((report / 'collection-status.log').read_text(), 'logcat_exit=1\nresult=0\n')

    def test_optional_server_log_symlink_is_not_read(self):
        result, _, report, _, _ = self.run_cleanup(server_symlink=True)
        self.assertEqual(result.returncode, 0)
        self.assertFalse((report / 'adb-server-tail.log').exists())


if __name__ == '__main__':
    unittest.main()
