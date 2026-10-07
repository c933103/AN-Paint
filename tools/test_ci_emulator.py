"""Exercise startup recovery without an Android SDK or a long-running emulator."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).with_name('ci_emulator.sh').resolve()
VERTICAL = 'paint.anpaint.android.VerticalLocaleDeviceTest'


class EmulatorSuitesTest(unittest.TestCase):
    def run_suites(self, *, api=35, variant='debug', failing=''):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runner = root / 'runner.py'
            runner.write_text('''import json, os, sys
from pathlib import Path
args = sys.argv[1:]
with (Path(os.environ['CI_TEST_DIR']) / 'calls.jsonl').open('a') as saved:
    saved.write(json.dumps(args) + '\\n')
suite = args[args.index('--suite') + 1]
sys.exit(1 if suite == os.environ['CI_FAIL_SUITE'] else 0)
''')
            result = subprocess.run(['bash', '-c', '''
source "$CI_SCRIPT"
report="$CI_TEST_DIR"
adb=test-adb
variant="$BUILD_VARIANT"
python3() { "$CI_TEST_PYTHON" "$CI_TEST_RUNNER" "$@"; }
run_instrumentation_suites
'''], text=True, capture_output=True, timeout=10,
                env={**os.environ, 'CI_SCRIPT': str(SCRIPT), 'CI_TEST_DIR': directory,
                     'CI_TEST_PYTHON': sys.executable, 'CI_TEST_RUNNER': str(runner),
                     'TEST_API': str(api), 'BUILD_VARIANT': variant, 'CI_FAIL_SUITE': failing})
            calls = [json.loads(line) for line in (root / 'calls.jsonl').read_text().splitlines()]
            return result, calls

    def test_all_variants_keep_native_checks_and_partition_app_with_separate_budgets(self):
        for api in (30, 35):
            for variant in ('debug', 'release'):
                with self.subTest(api=api, variant=variant):
                    result, calls = self.run_suites(api=api, variant=variant)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(len(calls), 3)
                    native, editor, vertical = calls
                    value = lambda call, key: call[call.index(key) + 1]
                    self.assertEqual([value(call, '--suite') for call in calls],
                                     ['Paintroid', 'app', 'app-vertical'])
                    self.assertEqual([value(call, '--timeout-seconds') for call in calls], ['180'] * 3)
                    self.assertEqual(value(native, '--source-tests'), 'Paintroid/src/androidTest')
                    self.assertEqual(value(native, '--component'),
                                     'org.catrobat.paintroid.test/androidx.test.runner.AndroidJUnitRunner')
                    self.assertEqual(value(native, '--apk'),
                                     f'build/prebuilt/Paintroid/build/outputs/apk/androidTest/{variant}/Paintroid-{variant}-androidTest.apk')
                    self.assertNotIn('--include-class', native)
                    if api == 30:
                        self.assertEqual(value(native, '--exclude-class'),
                                         'org.catrobat.paintroid.classic.UltraHdrImportTest')
                        self.assertEqual(native.count('--exclude-class'), 1)
                    else:
                        self.assertNotIn('--exclude-class', native)
                    for call in (editor, vertical):
                        self.assertEqual(value(call, '--source-tests'), 'app/src/androidTest')
                        self.assertEqual(value(call, '--component'),
                                         'paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner')
                        self.assertEqual(value(call, '--apk'),
                                         f'build/prebuilt/app/build/outputs/apk/androidTest/{variant}/app-{variant}-androidTest.apk')
                    self.assertEqual(value(editor, '--exclude-class'), VERTICAL)
                    self.assertEqual(editor.count('--exclude-class'), 1)
                    self.assertNotIn('--include-class', editor)
                    self.assertEqual(value(vertical, '--include-class'), VERTICAL)
                    self.assertEqual(vertical.count('--include-class'), 1)
                    self.assertNotIn('--exclude-class', vertical)
                    outputs = [value(call, '--output') for call in calls]
                    self.assertEqual(len(set(outputs)), 3)
                    self.assertTrue(outputs[0].endswith('/Paintroid/androidTest-results'))
                    self.assertTrue(outputs[1].endswith('/app/androidTest-results'))
                    self.assertTrue(outputs[2].endswith('/app-vertical/androidTest-results'))

    def test_failed_suite_is_not_retried_and_does_not_skip_later_suites(self):
        for failing in ('Paintroid', 'app', 'app-vertical'):
            with self.subTest(failing=failing):
                result, calls = self.run_suites(failing=failing)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(len(calls), 3)


class EmulatorEvidenceTest(unittest.TestCase):
    def test_exit_cleanup_pulls_screenshots_before_shutdown_and_preserves_failures(self):
        for status, pull_status in ((0, 0), (7, 0), (124, 0), (0, 1), (7, 1)):
            with self.subTest(status=status, pull_status=pull_status), \
                    tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                adb = root / 'adb'
                adb.write_text('''#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$CI_TEST_DIR/adb-calls.txt"
if test "$1" = pull; then
  if test "$CI_PULL_STATUS" != 0; then echo 'pull failed' >&2; exit "$CI_PULL_STATUS"; fi
  mkdir -p "$3"
  printf 'screenshot' > "$3/evidence.png"
  echo '1 file pulled'
fi
''')
                adb.chmod(0o700)
                result = subprocess.run(['bash', '-c', '''
source "$CI_SCRIPT"
report="$CI_TEST_DIR"
adb="$report/adb"
emulator_pid=''
phase='Test evidence cleanup'
trap cleanup EXIT
exit "$CI_EXIT_STATUS"
'''], text=True, capture_output=True, timeout=10,
                    env={**os.environ, 'CI_SCRIPT': str(SCRIPT), 'CI_TEST_DIR': directory,
                         'CI_EXIT_STATUS': str(status), 'CI_PULL_STATUS': str(pull_status)})
                self.assertEqual(result.returncode, status or pull_status, result.stdout + result.stderr)
                calls = (root / 'adb-calls.txt').read_text().splitlines()
                self.assertEqual(calls, ['logcat -d',
                    'pull /sdcard/Android/data/paint.anpaint.android/files/vertical-locale-evidence ' +
                    str(root / 'app/vertical-locale-evidence'), 'emu kill'])
                self.assertTrue((root / 'logcat.txt').is_file())
                pull_log = (root / 'vertical-locale-pull.log').read_text()
                if pull_status:
                    self.assertIn('pull failed', pull_log)
                    self.assertIn('FAILED: could not collect vertical locale evidence', result.stderr)
                else:
                    self.assertIn('1 file pulled', pull_log)
                    self.assertEqual((root / 'app/vertical-locale-evidence/evidence.png').read_text(), 'screenshot')


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


if __name__ == '__main__':
    unittest.main()
