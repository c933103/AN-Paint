"""Universal-build diagnostics preserve commands, limits and failure status."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/android.yml').read_text()
BUILD = WORKFLOW.split('\n  build:\n', 1)[1].split('\n  device:\n', 1)[0]


class BuildDiagnosticsTest(unittest.TestCase):
    def test_universal_command_preserves_both_variants_and_failures(self):
        command = BUILD.split('      - name: Build universal APK\n', 1)[1].split('        run: ', 1)[1].splitlines()[0]
        for variant in ('debug', 'release'):
            for status in (0, 7):
                with self.subTest(variant=variant, status=status), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    (root / 'tools').mkdir()
                    shutil.copy(ROOT / 'tools/ci_run_timed.sh', root / 'tools')
                    stub = root / 'gradlew'
                    stub.write_text('#!/bin/bash\nprintf "%s\\n" "$@"\nexit "$TEST_EXIT"\n')
                    stub.chmod(0o755)
                    result = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', command], cwd=root,
                        env={**os.environ, 'BUILD_VARIANT': variant, 'TEST_EXIT': str(status)},
                        capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, status, result.stderr)
                    self.assertEqual(result.stdout.splitlines(), ['--no-daemon', '--max-workers=2', '--console=plain',
                        '--profile', f':app:assemble{variant.capitalize()}', '-PciReleaseSigning'])
                    reports = root / 'build/reports/ci-phases'
                    self.assertEqual((reports / 'apk.log').read_text(), result.stdout)
                    self.assertIn(f'exit_status={status}', (reports / 'apk.time').read_text())

    def test_existing_deadlines_signing_and_universal_abis_remain(self):
        self.assertIn('    timeout-minutes: 35\n', BUILD)
        step = BUILD.split('      - name: Build universal APK\n', 1)[1].split('      - name:', 1)[0]
        self.assertIn('        timeout-minutes: 22\n', step)
        self.assertNotIn('nativeAbis', step)
        self.assertNotIn('continue-on-error', BUILD)
        self.assertNotIn('|| true', step)
        source = (ROOT / 'Paintroid/build.gradle').read_text()
        self.assertIn("'arm64-v8a,armeabi-v7a,x86_64,x86'", source)

    def test_diagnostic_upload_is_bounded_allowlisted_and_attempt_specific(self):
        step = BUILD.split('      - name: Upload build diagnostics even on failure\n', 1)[1].split('      - name:', 1)[0]
        self.assertIn('        if: always()\n', step)
        self.assertIn('        timeout-minutes: 2\n', step)
        self.assertIn('uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a', step)
        self.assertIn('name: build-diagnostics-${{ github.sha }}-${{ github.run_attempt }}', step)
        self.assertIn('retention-days: 14', step)
        paths = step.split('          path: |\n', 1)[1].splitlines()
        self.assertEqual([line.strip() for line in paths if line.strip()],
                         ['build/reports/ci-phases/', 'build/reports/profile/'])
        self.assertLess(BUILD.index('Upload build diagnostics even on failure'),
                        BUILD.index('Record build identity and extract matching source'))

    def test_terminated_build_retains_partial_output_without_success_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(['timeout', '--kill-after=1s', '0.5s', 'bash',
                str(ROOT / 'tools/ci_run_timed.sh'), 'apk', 'bash', '-c',
                'echo partial-build-phase; sleep 10'], cwd=temporary, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 124)
            reports = Path(temporary) / 'build/reports/ci-phases'
            self.assertEqual((reports / 'apk.log').read_text(), 'partial-build-phase\n')
            self.assertTrue((reports / 'apk.started-at').exists())
            self.assertFalse((reports / 'apk.ended-at').exists())
            self.assertNotIn('exit_status=0', (reports / 'apk.time').read_text())

    def test_apk_log_write_failure_does_not_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'build/reports/ci-phases/apk.log').mkdir(parents=True)
            result = subprocess.run(['bash', str(ROOT / 'tools/ci_run_timed.sh'), 'apk', 'true'],
                                    cwd=root, capture_output=True, text=True, timeout=5)
            self.assertNotEqual(result.returncode, 0)
