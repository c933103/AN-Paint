"""Host contracts for matrix selection, fail-closed accounting and evidence cleanup."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

from run_android_instrumentation import RESTART_SEED, RESTART_VERIFY, declared_tests
from vertical_locale_matrix import (VERTICAL, VERTICAL_METHODS, EXPECTED_SCREENSHOTS,
                                   app_partition, verify_app_reports, verify_screenshots)

ROOT = Path(__file__).resolve().parents[1]
EDITOR = 'paint.anpaint.android.EditorDeviceTest'
FUTURE = 'paint.anpaint.android.FutureDeviceTest'


def expected(sdk=35):
    result = {(EDITOR, 'ordinary'), (FUTURE, 'future')} | {(VERTICAL, name) for name in VERTICAL_METHODS}
    result |= {(RESTART_SEED, 'seed'), (RESTART_VERIFY, 'verify')}
    return result


def reports(sdk=35):
    return {phase: dict(success=True, device_sdk=sdk, leave_target_running=phase == 'seed',
                        expected_tests=len(part), completed_tests=len(part),
                        cases=[dict(classname=owner, name=name, status='passed') for owner, name in sorted(part)])
            for phase, part in app_partition(expected(sdk), sdk).items()}


def source_fixture(root):
    source = root/'app/src/androidTest'
    source.mkdir(parents=True)
    for owner in {owner for owner, _ in expected()}:
        name = owner.rsplit('.', 1)[1]
        annotation = ''
        methods = ''.join(f'@Test fun {method}() {{}}\n' for item_owner, method in sorted(expected()) if owner == item_owner)
        (source/f'{name}.kt').write_text(f'package paint.anpaint.android\n{annotation}class {name} {{\n{methods}}}\n')
    return source


def screenshot_fixture(directory):
    directory.mkdir(parents=True, exist_ok=True)
    for name in EXPECTED_SCREENSHOTS:
        width, height = (120, 240) if '-portrait-' in name else (240, 120)
        # Deliberately header-only fixtures exercise inventory and byte-duplicate checks.
        # They do not pretend to be rendered screenshots or fully decodable PNGs.
        data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'+struct.pack('>II', width, height)+b'\0'*9+name.encode('utf-8')
        (directory/name).write_bytes(data)


class MatrixInventoryTest(unittest.TestCase):
    def test_complete_current_and_future_methods_form_disjoint_sdk_partitions(self):
        for sdk in (30, 35):
            result = verify_app_reports(expected(sdk), sdk, reports(sdk))
            self.assertEqual(result['completed_tests'], 6 if sdk == 30 else 8)
            self.assertIn((FUTURE, 'future'), app_partition(expected(sdk), sdk)['ordinary'])
            self.assertEqual(result['phases']['vertical'], 4)
            self.assertEqual(len(result['explicitly_excluded_tests']), 2 if sdk == 30 else 0)

    def test_each_missing_duplicate_unexpected_failed_or_wrong_sdk_result_is_rejected(self):
        for sdk in (30, 35):
            good = reports(sdk)
            for phase in good:
                mutations = (
                    lambda r: r.pop(phase),
                    lambda r: r[phase]['cases'].pop(),
                    lambda r: r[phase]['cases'].append(r[phase]['cases'][0]),
                    lambda r: r[phase]['cases'][0].update(name='unknown'),
                    lambda r: r[phase]['cases'][0].update(status='skipped'),
                    lambda r: r[phase].update(device_sdk=29),
                    lambda r: r[phase].update(completed_tests=999),
                    lambda r: r[phase].update(leave_target_running=phase != 'seed'),
                    lambda r: r[phase].update(success=False),
                )
                for mutation in mutations:
                    broken = copy.deepcopy(good); mutation(broken)
                    with self.subTest(sdk=sdk, phase=phase), self.assertRaises(ValueError):
                        verify_app_reports(expected(sdk), sdk, broken)

    def test_every_phase_requires_a_captured_exact_integer_sdk(self):
        for sdk in (30, 35):
            for phase in reports(sdk):
                for invalid in (None, 29, 30 if sdk == 35 else 35, 36, str(sdk), float(sdk), True):
                    broken = reports(sdk)
                    if invalid is None:
                        broken[phase].pop('device_sdk')
                    else:
                        broken[phase]['device_sdk'] = invalid
                    with self.subTest(sdk=sdk, phase=phase, invalid=invalid), self.assertRaises(ValueError):
                        verify_app_reports(expected(sdk), sdk, broken)
            for invalid in (29, str(sdk), float(sdk), True):
                with self.subTest(requested_sdk=invalid), self.assertRaises(ValueError):
                    verify_app_reports(expected(sdk), invalid, reports(sdk))

    def test_cli_uses_captured_sdk_for_future_min_and_max_source_eligibility(self):
        for sdk in (30, 35):
            for bound, eligible in ((f'minSdkVersion={sdk+1}', False), (f'maxSdkVersion={sdk-1}', False),
                                    (f'minSdkVersion={sdk}', True), (f'maxSdkVersion={sdk}', True)):
                with self.subTest(sdk=sdk, bound=bound), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    source = source_fixture(root)
                    future = source/'FutureDeviceTest.kt'
                    future.write_text(future.read_text().replace('@Test fun future', f'@Test @SdkSuppress({bound}) fun future'))
                    selected = declared_tests(source, sdk_level=sdk)
                    parts = app_partition(selected, sdk)
                    paths = {'ordinary': root/'report/app/androidTest-results/summary.json',
                             'vertical': root/'report/app-vertical/androidTest-results/summary.json'}
                    if sdk == 35:
                        paths.update({phase: root/f'report/app/accepted-credit-restart/{phase}/summary.json'
                                      for phase in ('seed', 'verify')})
                    for phase, part in parts.items():
                        paths[phase].parent.mkdir(parents=True, exist_ok=True)
                        paths[phase].write_text(json.dumps(dict(success=True, device_sdk=sdk,
                            leave_target_running=phase == 'seed', expected_tests=len(part), completed_tests=len(part),
                            cases=[dict(classname=owner, name=name, status='passed') for owner, name in sorted(part)])))
                    command = [sys.executable, str(ROOT/'tools/vertical_locale_matrix.py'), 'verify-reports',
                               '--source-tests', str(source), '--sdk', str(sdk), '--root', str(root/'report')]
                    result = subprocess.run(command, capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                    receipt = json.loads((root/'report/app/coverage.json').read_text())
                    self.assertEqual(receipt['device_sdk'], sdk)
                    self.assertEqual(receipt['declared_tests'], 8 if eligible else 7)
                    self.assertEqual(receipt['completed_tests'], (8 if sdk == 35 else 6) - (not eligible))
                    self.assertEqual([FUTURE, 'future'] in receipt['completed'], eligible)
                    self.assertEqual(receipt['phases']['ordinary'], 2 if eligible else 1)
                    self.assertEqual(receipt['phases']['vertical'], 4)
                    restart_receipt = root/'report/app/accepted-credit-restart/coverage.json'
                    if sdk == 35:
                        self.assertEqual(json.loads(restart_receipt.read_text()), receipt)
                    else:
                        self.assertFalse(restart_receipt.exists())

    def test_missing_matrix_method_or_restart_phase_fails_closed(self):
        for broken in (expected()-{(VERTICAL, sorted(VERTICAL_METHODS)[0])},
                       expected() | {(VERTICAL, 'unexpected')}, expected()-{(RESTART_SEED, 'seed')}):
            with self.assertRaises(ValueError): app_partition(broken, 35)
        with self.assertRaises(ValueError): verify_app_reports(expected(), 30, reports())

    def test_actual_source_contains_the_complete_four_locale_matrix(self):
        for sdk in (30, 35):
            selected = declared_tests(ROOT/'app/src/androidTest', sdk_level=sdk)
            parts = app_partition(selected, sdk)
            self.assertEqual(len(parts['vertical']), 4)
            omitted = {item for item in selected if sdk == 30 and item[0] in (RESTART_SEED, RESTART_VERIFY)}
            self.assertEqual(set.union(*parts.values()), selected-omitted)
        source = (ROOT/'app/src/androidTest/java/paint/anpaint/android/VerticalLocaleDeviceTest.kt').read_text()
        for prohibited in ('.performClick(', '.requestRectangleOnScreen(', '.scrollTo(', '.scrollBy('):
            self.assertNotIn(prohibited, source)
        self.assertIn('activity.startupReady', source)
        self.assertIn('draftGenerationField.getLong(activity)==savedDraftGenerationField.getLong(activity)', source)
        self.assertIn('receivedPosition.get()==index', source)
        self.assertIn('externalRequests.isEmpty()', source)
        self.assertIn('awaitRenderedFormatPopup()', source)
        self.assertIn('registerFrameCommitCallback(committed)', source)
        self.assertIn('unregisterFrameCommitCallback(committed)', source)
        self.assertIn('screenshot("format-popup",distinctFrom=initialSaveScreenshot)', source)
        self.assertIn('Color.MAGENTA,activity.document.bitmap.getPixel(4,7)', source)
        self.assertIn('Color.CYAN,activity.document.bitmap.getPixel(81,63)', source)

    def test_archived_attempt_two_is_bound_and_rejected_for_the_observed_duplicate(self):
        evidence = ROOT/'verification/installed-vertical-matrix-2026-10-10/attempt-2-visual'
        receipt = json.loads((evidence/'visual-receipt.json').read_text())
        screenshots = evidence/'screenshots'
        self.assertEqual({path.name for path in screenshots.glob('*.png')}, EXPECTED_SCREENSHOTS)
        for entry in receipt['images']['files']:
            self.assertEqual(hashlib.sha256((screenshots/entry['name']).read_bytes()).hexdigest(), entry['sha256'])
        with self.assertRaisesRegex(ValueError, 'Duplicate screenshot content: en-XV-landscape-format-popup.png and en-XV-landscape-save-initial.png'):
            verify_screenshots(screenshots)

    def test_screenshot_matrix_rejects_a_duplicated_closed_form_as_popup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); screenshot_fixture(root)
            before = root/'en-XV-landscape-save-initial.png'
            popup = root/'en-XV-landscape-format-popup.png'
            popup.write_bytes(before.read_bytes())
            with self.assertRaisesRegex(ValueError, 'Duplicate screenshot content'):
                verify_screenshots(root)

    def test_screenshot_matrix_rejects_missing_extra_or_corrupted_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); screenshot_fixture(root)
            result = verify_screenshots(root)
            self.assertEqual(len(result['files']), 32)
            selected = root/sorted(EXPECTED_SCREENSHOTS)[0]
            original = selected.read_bytes()
            selected.unlink()
            with self.assertRaises(ValueError): verify_screenshots(root)
            selected.write_bytes(original)
            extra = root/'unexpected.png'; extra.write_bytes(original)
            with self.assertRaises(ValueError): verify_screenshots(root)
            extra.unlink(); selected.write_bytes(b'corrupt')
            with self.assertRaises(ValueError): verify_screenshots(root)


class MatrixShellTest(unittest.TestCase):
    def test_runner_selects_only_matrix_once_with_normal_lifecycle_on_both_sdks(self):
        for sdk in (30, 35):
            for failure in ('', 'truncated', 'assertion'):
                with self.subTest(sdk=sdk, failure=failure), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory); source_fixture(root)
                    shutil.copytree(ROOT/'tools', root/'tools', ignore=shutil.ignore_patterns('__pycache__'))
                    apk = root/'build/prebuilt/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk'
                    apk.parent.mkdir(parents=True); apk.touch()
                    stale = root/'report/app-vertical/androidTest-results'; stale.mkdir(parents=True)
                    (stale/'summary.json').write_text('{"success":true}')
                    (stale/'stale.xml').touch()
                    fake = root/'adb'
                    fake.write_text('#!'+sys.executable+'\n'+r'''
import json, os, sys
from pathlib import Path
sys.path.insert(0, 'tools')
from vertical_locale_matrix import VERTICAL_METHODS, VERTICAL
args=sys.argv[1:]
with open('events', 'a') as out: out.write(json.dumps(args)+'\n')
if args[:3]==['shell','rm','-rf']: sys.exit(0)
if args[0]=='install': print('Success'); sys.exit(0)
if args==['shell','getprop','ro.build.version.sdk']: print(os.environ['TEST_SDK']); sys.exit(0)
if args[:4]==['shell','pm','list','instrumentation']:
    print('instrumentation:paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner (target=paint.anpaint.android)'); sys.exit(0)
if args[:3]==['shell','am','instrument']:
    assert '--no-restart' not in args and 'waitForActivitiesToComplete' not in args
    excluded=set(args[args.index('notClass')+1].split(','))
    assert excluded=={'paint.anpaint.android.'+name for name in
                     ('EditorDeviceTest','FutureDeviceTest','AcceptedCreditRestartSeedTest','AcceptedCreditRestartVerifyTest')}
    for method in sorted(VERTICAL_METHODS):
        for code in (1, -2 if os.environ['TEST_FAILURE']=='assertion' else 0):
            print('INSTRUMENTATION_STATUS: class='+VERTICAL)
            print('INSTRUMENTATION_STATUS: test='+method)
            print('INSTRUMENTATION_STATUS: numtests=4')
            print('INSTRUMENTATION_STATUS_CODE: '+str(code))
    if os.environ['TEST_FAILURE']!='truncated': print('INSTRUMENTATION_CODE: -1')
    sys.exit(0)
raise SystemExit('Unexpected command: '+repr(args))
''')
                    fake.chmod(0o700)
                    command = 'source "$CI_SCRIPT"; report="$PWD/report"; adb="$PWD/adb"; variant=debug; run_vertical_locale_matrix'
                    result = subprocess.run(['bash', '-c', command], cwd=root, capture_output=True, text=True, timeout=15,
                        env={**os.environ, 'CI_SCRIPT': str(ROOT/'tools/ci_emulator.sh'), 'TEST_SDK': str(sdk), 'TEST_FAILURE': failure})
                    self.assertEqual(result.returncode, 1 if failure else 0, result.stdout+result.stderr)
                    report = json.loads((stale/'summary.json').read_text())
                    self.assertEqual(report['success'], not failure)
                    self.assertEqual(report['expected_tests'], 4)
                    self.assertFalse((stale/'stale.xml').exists())
                    events = [json.loads(line) for line in (root/'events').read_text().splitlines()]
                    self.assertEqual(sum(event[:3]==['shell','am','instrument'] for event in events), 1)
                    self.assertEqual(events[0][:3], ['shell','rm','-rf'])

    def test_cleanup_collects_before_shutdown_and_never_turns_a_failure_green(self):
        for start, fault, expected_status in ((0, '', 0), (0, 'pull', 1), (0, 'missing', 1),
                                              (7, 'pull', 7), (7, 'missing', 7)):
            with self.subTest(start=start, fault=fault), tempfile.TemporaryDirectory() as directory:
                root = Path(directory); (root/'report').mkdir()
                shutil.copytree(ROOT/'tools', root/'tools', ignore=shutil.ignore_patterns('__pycache__'))
                screenshot_fixture(root/'device')
                if fault == 'missing': (root/'device'/sorted(EXPECTED_SCREENSHOTS)[0]).unlink()
                fake = root/'adb'
                fake.write_text('#!'+sys.executable+'\n'+r'''
import json, os, shutil, sys
with open('events','a') as out: out.write(json.dumps(sys.argv[1:])+'\n')
if sys.argv[1]=='pull':
    if os.environ['TEST_FAULT']=='pull': sys.exit(1)
    shutil.copytree('device',sys.argv[3])
''')
                fake.chmod(0o700)
                command = 'source "$CI_SCRIPT"; report="$PWD/report"; adb="$PWD/adb"; emulator_pid=""; vertical_started=1; phase=test; trap cleanup EXIT; exit "$INITIAL_STATUS"'
                result = subprocess.run(['bash','-c',command], cwd=root, capture_output=True, text=True, timeout=15,
                    env={**os.environ, 'CI_SCRIPT': str(ROOT/'tools/ci_emulator.sh'), 'INITIAL_STATUS': str(start), 'TEST_FAULT': fault})
                self.assertEqual(result.returncode, expected_status, result.stdout+result.stderr)
                events = [json.loads(line) for line in (root/'events').read_text().splitlines()]
                self.assertLess(next(i for i, event in enumerate(events) if event[0]=='pull'),
                                next(i for i, event in enumerate(events) if event[:2]==['emu','kill']))
                self.assertEqual((root/'report/vertical-locale-screenshots.json').exists(), not fault)


if __name__ == '__main__':
    unittest.main()
