"""Exercise startup recovery without an Android SDK or a long-running emulator."""
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

SCRIPT = Path(__file__).with_name('ci_emulator.sh').resolve()


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
