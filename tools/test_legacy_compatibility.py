"""Legacy dispatch/SDK contracts. Host fakes are not Android device evidence."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from app_instrumentation_matrix import (DIALOG, DIALOG_METHODS, COLOUR, COLOUR_METHODS, app_partition, coverage_paths, report_paths,
                                        verify_app_reports)
from run_android_instrumentation import RESTART_SEED, RESTART_VERIFY, declared_tests
from test_app_instrumentation_matrix import SOURCE, receipts
from test_ci_timeout_budget import job, one, step_minutes

ROOT = Path(__file__).resolve().parents[1]
SHELL = (ROOT/'tools/ci_emulator.sh').read_text()


class LegacyInventoryTest(unittest.TestCase):
    def test_current_legacy_omission_is_explicit_and_never_a_test_pass(self):
        for sdk in (21, 24):
            expected, reports, digest, suppressed = receipts(SOURCE, sdk)
            result = verify_app_reports(expected, sdk, reports, digest, suppressed)
            self.assertEqual(reports, {})
            self.assertEqual(expected, {(RESTART_SEED, 'acceptedGalleryEditRemainsUndeliveredUntilExternalForceStop'),
                                        (RESTART_VERIFY, 'acceptedTextIsRecoverableWithoutAutomaticDocumentAssociation')})
            self.assertIsNone(result['success'])
            self.assertEqual(result['execution_status'], 'not-run-no-sdk-eligible-selected-tests')
            self.assertTrue(result['inventory_validated'])
            self.assertEqual(result['receipt_scope'], 'sdk-ineligible-app-omission')
            self.assertEqual(result['completed_tests'], 0)
            self.assertEqual(result['selected_tests'], 0)
            self.assertEqual(result['declared_tests'], 48)
            self.assertEqual(len(result['sdk_suppressed_tests']), 46)
            self.assertEqual({(DIALOG, method) for method in DIALOG_METHODS} | {(COLOUR, method) for method in COLOUR_METHODS},
                             {tuple(item) for item in result['sdk_suppressed_tests'] if item[0] in (DIALOG,COLOUR)})
            self.assertEqual(set(result['explicitly_excluded_tests']), expected)
            self.assertEqual(result['all_app_total_timeout_seconds'], 0)
            self.assertEqual(result['vertical_total_timeout_seconds'], 0)
            self.assertEqual(result['timeout_seconds_by_phase'], {})
            self.assertEqual(report_paths(Path('unused'), sdk), {})
            native = declared_tests(ROOT/'Paintroid/src/androidTest', sdk_level=sdk)
            self.assertEqual(len(native), 73)
            self.assertNotIn('org.catrobat.paintroid.classic.UltraHdrImportTest', {owner for owner, _ in native})

    def test_new_eligible_method_or_foreign_report_cannot_be_hidden_as_omission(self):
        for sdk in (21, 24):
            expected, reports, digest, suppressed = receipts(SOURCE, sdk)
            for owner in (DIALOG, 'paint.anpaint.android.FutureTest', 'paint.anpaint.android.EditorDeviceTest',
                          'paint.anpaint.android.GalleryDraftDeviceTest', 'paint.anpaint.android.VerticalLocaleDeviceTest',
                          RESTART_SEED):
                with self.subTest(sdk=sdk, owner=owner), self.assertRaises(ValueError):
                    app_partition(expected | {(owner, 'newEligibleMethod')}, sdk)
            with self.assertRaises(ValueError):
                verify_app_reports(expected, sdk, {'ordinary': {'success': True}}, digest, suppressed)
            for invalid in (True, str(sdk), float(sdk), 22, 29, 36):
                with self.assertRaises(ValueError):
                    app_partition(expected, invalid)

    def test_cli_proves_source_omission_and_clears_stale_success_in_all_modes(self):
        for sdk in (21, 24):
            for mode in ('normal', 'flag', 'environment'):
                for script, subcommand in (('app_instrumentation_matrix.py', []),
                                          ('vertical_locale_matrix.py', ['verify-reports'])):
                    with self.subTest(sdk=sdk, mode=mode, script=script), tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        env = os.environ.copy(); env.pop('PYTHONOPTIMIZE', None)
                        if mode == 'environment': env['PYTHONOPTIMIZE'] = '1'
                        command = [sys.executable, *(['-O'] if mode == 'flag' else []), str(ROOT/'tools'/script),
                                   *subcommand, '--source-tests', str(SOURCE), '--sdk', str(sdk), '--root', str(root)]
                        for output in coverage_paths(root):
                            output.parent.mkdir(parents=True, exist_ok=True)
                            output.write_text('{"success":true}')
                        run = subprocess.run(command, env=env, text=True, capture_output=True, timeout=10)
                        self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
                        result = json.loads((root/'app/coverage.json').read_text())
                        self.assertIsNone(result['success'])
                        self.assertEqual(result['completed_tests'], 0)
                        self.assertEqual(list(root.rglob('summary.json')), [])
                        self.assertTrue(all(not path.exists() for path in coverage_paths(root)[1:]))
                        for subtree in ('app', 'app-gallery-draft', 'app-dialog', 'app-vertical'):
                            stale = root/subtree/'old/summary.json'
                            stale.parent.mkdir(parents=True, exist_ok=True); stale.write_text('{"success":true}')
                            run = subprocess.run(command, env=env, text=True, capture_output=True, timeout=10)
                            self.assertNotEqual(run.returncode, 0)
                            self.assertTrue(all(not path.exists() for path in coverage_paths(root)))
                            stale.unlink()
                        # Lowering a source SDK bound must force a new execution
                        # plan, not silently retain the old empty selection.
                        changed = root/'source'; changed.mkdir()
                        (changed/'Future.kt').write_text('package paint.anpaint.android\nclass FutureTest { @Test fun eligible() {} }\n')
                        for name in ('AcceptedCreditRestartSeedTest', 'AcceptedCreditRestartVerifyTest'):
                            (changed/(name+'.kt')).write_text('package paint.anpaint.android\nclass '+name+' { @Test fun phase() {} }\n')
                        changed_command = command.copy()
                        changed_command[changed_command.index('--source-tests')+1] = str(changed)
                        run = subprocess.run(changed_command, env=env, text=True, capture_output=True, timeout=10)
                        self.assertNotEqual(run.returncode, 0)
                        self.assertTrue(all(not path.exists() for path in coverage_paths(root)))


class LegacyStartupTest(unittest.TestCase):
    def probe(self, sdk, abi='x86_64', actual_sdk=None, actual_abi=None):
        # Execute the actual main startup statements, replacing only external
        # Android processes/readiness probes. Production deadline tests remain
        # in test_ci_emulator.py; this checks command and platform selection.
        startup = SHELL.split('main() {', 1)[1].split('  failed=0\n', 1)[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            emulator = root/'sdk/emulator/emulator'; emulator.parent.mkdir(parents=True)
            emulator.write_text('#!/usr/bin/env bash\nexit 0\n'); emulator.chmod(0o700)
            harness = r'''
set -euo pipefail
progress() { printf '%s\n' "$*"; }
cleanup() { :; }
timeout() { printf 'COMMAND'; printf ' <%s>' "$@"; printf '\n'; }
wait_until_ready() {
  printf 'READINESS'; printf ' <%s>' "$@"; printf ' budget=%s\n' "$((readiness_deadline - SECONDS))"
  case "$1" in
    'Verify Android API') ready_output="$ACTUAL_SDK";;
    'Verify native ABI') ready_output="$ACTUAL_ABI";;
    *) ready_output=1;;
  esac
}
'''
            run = subprocess.run(['bash', '-c', harness+startup], cwd=root, text=True, capture_output=True, timeout=10,
                env={**os.environ, 'TEST_API':str(sdk), 'EMULATOR_ABI':abi, 'ANDROID_HOME':str(root/'sdk'),
                     'ACTUAL_SDK':str(sdk if actual_sdk is None else actual_sdk),
                     'ACTUAL_ABI':abi if actual_abi is None else actual_abi})
            return run

    def test_actual_sdk_abi_startup_commands_and_budgets_for_all_supported_combinations(self):
        for sdk in (21, 24, 30, 35):
            for abi in ('x86', 'x86_64'):
                with self.subTest(sdk=sdk, abi=abi):
                    run = self.probe(sdk, abi)
                    self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
                    self.assertIn('system-images;android-'+str(sdk)+';google_apis;'+abi, run.stdout)
                    self.assertIn('<shell> <getprop> <ro.product.cpu.abi>', run.stdout)
                    self.assertIn('budget='+str(180 if sdk<30 else 120), run.stdout)
                    self.assertIn('<shell> <pm> <path> <android>' if sdk<30 else
                                  '<shell> <cmd> <package> <path> <android>', run.stdout)
                    self.assertEqual('<shell> <wm> <dismiss-keyguard>' in run.stdout, sdk>=23)
                    self.assertIn('<60s>', run.stdout)
                    self.assertIn('<install> <-r> <-t>', run.stdout)

    def test_mismatched_sdk_or_abi_and_invalid_selection_fail_before_install(self):
        for sdk in (21, 24, 30, 35):
            for mismatch in ({'actual_sdk':99}, {'actual_abi':'arm64-v8a'}):
                run = self.probe(sdk, **mismatch)
                self.assertNotEqual(run.returncode, 0)
                self.assertNotIn('<install>', run.stdout)
        for sdk, abi in ((22, 'x86'), (29, 'x86_64'), (35, 'arm64-v8a')):
            run = self.probe(sdk, abi)
            self.assertEqual(run.returncode, 2)
            self.assertNotIn('COMMAND', run.stdout)

    def test_legacy_build_admits_reconciled_cold_universal_and_test_apk_budgets(self):
        legacy = (ROOT/'.github/workflows/android-legacy.yml').read_text()
        standard = (ROOT/'.github/workflows/android.yml').read_text()
        legacy_build, standard_build = job(legacy, 'build'), job(standard, 'build')
        def limits(build, test_step):
            return (int(one(r'^    timeout-minutes: (\d+)$', build)),
                    step_minutes(build, 'Build universal APK'), step_minutes(build, test_step))
        self.assertEqual(limits(legacy_build, 'Compile both instrumentation APKs'), (45, 30, 3))
        self.assertEqual(limits(legacy_build, 'Compile both instrumentation APKs'),
                         limits(standard_build, 'Compile test APKs once for all emulator jobs'))
        assembly = legacy_build.split('      - name: Build universal APK\n', 1)[1].split('      - name:', 1)[0]
        test_apks = legacy_build.split('      - name: Compile both instrumentation APKs\n', 1)[1].split('      - name:', 1)[0]
        self.assertIn(':app:assembleDebug ', assembly)
        self.assertNotIn('AndroidTest', assembly)
        self.assertIn(':Paintroid:assembleDebugAndroidTest :app:assembleDebugAndroidTest', test_apks)
        self.assertNotIn(':app:assembleDebug ', test_apks)
        # Reinstating either stale cap cannot satisfy the reconciled contract.
        for old, new in (('timeout-minutes: 45', 'timeout-minutes: 40'),
                         ('timeout-minutes: 30', 'timeout-minutes: 26')):
            self.assertNotEqual(limits(legacy_build.replace(old, new), 'Compile both instrumentation APKs'), (45, 30, 3))

    def test_manual_workflow_never_joins_regular_push_or_pr_matrix(self):
        legacy = (ROOT/'.github/workflows/android-legacy.yml').read_text()
        triggers = legacy.split('\non:\n', 1)[1].split('\npermissions:', 1)[0]
        self.assertEqual([line.strip() for line in triggers.splitlines()
                          if line.startswith('  ') and not line.startswith('   ')], ['workflow_dispatch:'])
        self.assertIn("options: [both, '21', '24']", triggers)
        self.assertIn('options: [both, x86, x86_64]', triggers)
        self.assertIn('fail-fast: false', legacy)
        self.assertNotIn('continue-on-error', legacy)
        normal = (ROOT/'.github/workflows/android.yml').read_text()
        self.assertIn("'[30,35]' || '[35]'", normal)
        self.assertNotIn('android-legacy.yml', normal)


if __name__ == '__main__':
    unittest.main()
