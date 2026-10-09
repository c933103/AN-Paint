"""Bounded required phases must preserve checks, diagnostics and failure status."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/android.yml').read_text()
CHECKS = WORKFLOW.split('\n  checks:\n', 1)[1].split('\n  build:\n', 1)[0]
STEPS = {
    block.splitlines()[0].removeprefix('name: '): block
    for block in re.split(r'(?m)^      - ', CHECKS)[1:]
    if block.startswith('name: ')
}
PHASES = {
    'Run Python contracts': ('python', 2),
    'Run JVM regression tests': ('jvm', 12),
    'Run Android lint and native dependencies': ('lint', 6),
}


class CheckPhaseContracts(unittest.TestCase):
    def test_each_phase_required_and_bounded_with_unchanged_outer_limit(self):
        self.assertIn('    timeout-minutes: 20\n', CHECKS)
        self.assertNotIn('continue-on-error', CHECKS)
        for name, (phase, minutes) in PHASES.items():
            with self.subTest(phase=phase):
                block = STEPS[name]
                self.assertIn('        if: ${{ !cancelled() }}\n', block)
                self.assertIn(f'        timeout-minutes: {minutes}\n', block)
                self.assertEqual(block.count('        run: '), 1)
                self.assertNotIn('|| true', block)
        self.assertNotIn('Run local checks', CHECKS)

    def test_reports_and_live_phase_profile_evidence_are_uploaded_on_failure(self):
        upload = CHECKS.split('      - uses: actions/upload-artifact@', 1)[1]
        self.assertIn('        if: always()', upload)
        for path in ('Paintroid/build/test-results/', 'Paintroid/build/reports/',
                     'app/build/reports/', 'build/reports/ci-phases/', 'build/reports/profile/'):
            self.assertIn(f'            {path}\n', upload)

    def test_exact_required_commands_for_debug_and_release_preserve_failures(self):
        for variant in ('debug', 'release'):
            for name, (phase, _) in PHASES.items():
                for returncode in (0, 7):
                    with self.subTest(variant=variant, phase=phase, returncode=returncode):
                        with tempfile.TemporaryDirectory() as temporary:
                            root = Path(temporary)
                            (root / 'tools').mkdir()
                            shutil.copy(ROOT / 'tools/ci_run_timed.sh', root / 'tools')
                            stub = '#!/bin/bash\nprintf "%s\\n" "$@"\nexit "$TEST_EXIT"\n'
                            for command in ('python3', 'gradlew'):
                                path = root / command
                                path.write_text(stub)
                                path.chmod(0o755)
                            command = STEPS[name].split('        run: ', 1)[1].splitlines()[0]
                            env = {**os.environ, 'BUILD_VARIANT': variant, 'TEST_EXIT': str(returncode),
                                   'PATH': f'{root}:{os.environ["PATH"]}'}
                            result = subprocess.run(['bash', '--noprofile', '--norc', '-e', '-o', 'pipefail',
                                                     '-c', command], cwd=root, env=env, capture_output=True, text=True)
                            self.assertEqual(result.returncode, returncode, result.stderr)
                            args = result.stdout.splitlines()
                            if phase == 'python':
                                self.assertEqual(args, ['-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_*.py'])
                            else:
                                task = (f':Paintroid:test{variant.capitalize()}UnitTest' if phase == 'jvm'
                                        else f':app:lint{variant.capitalize()}')
                                self.assertEqual(args, ['--no-daemon', '--max-workers=2', '--console=plain',
                                                       '--continue', '--profile', '-PnativeAbis=x86_64', task])
                            reports = root / 'build/reports/ci-phases'
                            self.assertEqual((reports / f'{phase}.log').read_text(), result.stdout)
                            timing = (reports / f'{phase}.time').read_text()
                            self.assertRegex(timing, r'real_seconds=\d+\.\d+')
                            self.assertIn(f'exit_status={returncode}\n', timing)
                            self.assertTrue((reports / f'{phase}.started-at').is_file())
                            self.assertTrue((reports / f'{phase}.ended-at').is_file())

    def test_stderr_and_successful_tee_cannot_hide_command_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(['bash', str(ROOT / 'tools/ci_run_timed.sh'), 'lint',
                                     'bash', '-c', 'echo output; echo diagnostic >&2; exit 9'],
                                    cwd=temporary, capture_output=True, text=True)
            self.assertEqual(result.returncode, 9)
            self.assertEqual(result.stdout, 'output\ndiagnostic\n')
            self.assertEqual((Path(temporary) / 'build/reports/ci-phases/lint.log').read_text(), result.stdout)

    def test_log_write_failure_cannot_turn_a_passing_check_green(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'build/reports/ci-phases/jvm.log').mkdir(parents=True)
            result = subprocess.run(['bash', str(ROOT / 'tools/ci_run_timed.sh'), 'jvm', 'true'],
                                    cwd=root, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_unknown_phase_and_missing_command_fail_before_execution(self):
        for args in ([], ['unexpected', 'true'], ['python']):
            with self.subTest(args=args), tempfile.TemporaryDirectory() as temporary:
                result = subprocess.run(['bash', str(ROOT / 'tools/ci_run_timed.sh'), *args],
                                        cwd=temporary, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((Path(temporary) / 'build/reports').exists())
