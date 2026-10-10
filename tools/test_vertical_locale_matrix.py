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
from unittest.mock import patch

from run_android_instrumentation import RESTART_SEED, RESTART_VERIFY, declared_tests, source_tests_sha256
from test_vertical_control_reachability import fixture as reachability_fixture
from vertical_locale_matrix import (VERTICAL, VERTICAL_METHODS, VERTICAL_SHARDS, EXPECTED_SCREENSHOTS,
                                   app_partition, verify_app_reports, verify_screenshots, report_paths, read_app_reports)

ROOT = Path(__file__).resolve().parents[1]
EDITOR = 'paint.anpaint.android.EditorDeviceTest'
FUTURE = 'paint.anpaint.android.FutureDeviceTest'
SOURCE_DIGEST = 'a'*64


def expected(sdk=35):
    result = {(EDITOR, 'ordinary'), (FUTURE, 'future')} | {(VERTICAL, name) for name in VERTICAL_METHODS}
    result |= {(RESTART_SEED, 'seed'), (RESTART_VERIFY, 'verify')}
    return result


def report_for(phase, part, sdk=35, digest=SOURCE_DIGEST):
    return dict(success=True, device_sdk=sdk, leave_target_running=phase == 'seed',
                source_tests_sha256=digest, timed_out=False, returncode=0,
                errors=[], missing=[], unexpected=[],
                timeout_seconds=60 if phase in ('seed', 'verify') else 180,
                included_tests=sorted(f'{owner}#{name}' for owner, name in part) if phase in VERTICAL_SHARDS else [],
                expected_tests=len(part), completed_tests=len(part),
                cases=[dict(classname=owner, name=name, status='passed') for owner, name in sorted(part)])


def reports(sdk=35):
    return {phase: report_for(phase, part, sdk) for phase, part in app_partition(expected(sdk), sdk).items()}


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
            result = verify_app_reports(expected(sdk), sdk, reports(sdk), SOURCE_DIGEST)
            self.assertEqual(result['completed_tests'], 6 if sdk == 30 else 8)
            self.assertIn((FUTURE, 'future'), app_partition(expected(sdk), sdk)['ordinary'])
            self.assertEqual({phase: result['phases'][phase] for phase in VERTICAL_SHARDS},
                             {phase: 2 for phase in VERTICAL_SHARDS})
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
                        verify_app_reports(expected(sdk), sdk, broken, SOURCE_DIGEST)

    def test_success_flag_cannot_override_timeout_source_or_selection_mismatch(self):
        for sdk in (30, 35):
            for phase in reports(sdk):
                mutations = (
                    lambda r: r[phase].update(timed_out=True),
                    lambda r: r[phase].pop('timed_out'),
                    lambda r: r[phase].update(returncode=124),
                    lambda r: r[phase].update(errors=['deadline']),
                    lambda r: r[phase].update(missing=[['other', 'missing']]),
                    lambda r: r[phase].update(unexpected=[['other', 'extra']]),
                    lambda r: r[phase].update(timeout_seconds=360),
                    lambda r: r[phase].pop('source_tests_sha256'),
                    lambda r: r[phase].update(source_tests_sha256='b'*64),
                    lambda r: r[phase].update(included_tests=['unknown#method']),
                    lambda r: r[phase].pop('included_tests'),
                )
                for mutation in mutations:
                    broken = reports(sdk); mutation(broken)
                    with self.subTest(sdk=sdk, phase=phase, mutation=mutation), self.assertRaises(ValueError):
                        verify_app_reports(expected(sdk), sdk, broken, SOURCE_DIGEST)
        for digest in (None, '', 'invalid', 'A'*64):
            with self.assertRaises(ValueError): verify_app_reports(expected(), 35, reports(), digest)

    def test_cross_shard_duplicates_swaps_overlap_or_old_monolith_are_rejected(self):
        first, second = VERTICAL_SHARDS
        for sdk in (30, 35):
            broken = reports(sdk); broken[second] = copy.deepcopy(broken[first])
            with self.assertRaises(ValueError): verify_app_reports(expected(), sdk, broken, SOURCE_DIGEST)
            broken = reports(sdk); broken[first], broken[second] = broken[second], broken[first]
            with self.assertRaises(ValueError): verify_app_reports(expected(), sdk, broken, SOURCE_DIGEST)
            broken = reports(sdk); broken['vertical'] = broken.pop(first); broken.pop(second)
            with self.assertRaises(ValueError): verify_app_reports(expected(), sdk, broken, SOURCE_DIGEST)
            broken = reports(sdk); broken['vertical-extra'] = broken[first]
            with self.assertRaises(ValueError): verify_app_reports(expected(), sdk, broken, SOURCE_DIGEST)
        for mutation in ('overlap', 'missing', 'extra_shard'):
            shards = copy.deepcopy(VERTICAL_SHARDS)
            if mutation=='overlap': shards[second] = shards[first]
            elif mutation=='missing': shards[second].pop()
            else: shards['vertical-extra'] = shards[first]
            with patch('vertical_locale_matrix.VERTICAL_SHARDS', shards), self.assertRaises(ValueError):
                app_partition(expected(), 35)

    def test_cli_report_inventory_rejects_missing_extra_duplicate_and_old_monolith_paths(self):
        for sdk in (30, 35):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory); paths = report_paths(root, sdk)
                for phase, path in paths.items():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(reports(sdk)[phase]))
                self.assertEqual(read_app_reports(root, sdk), reports(sdk))
                selected = paths[next(iter(VERTICAL_SHARDS))]
                original = selected.read_bytes(); selected.unlink()
                with self.assertRaisesRegex(ValueError, 'Exact vertical shard report inventory'):
                    read_app_reports(root, sdk)
                selected.write_bytes(original)
                for relative in ('extra/androidTest-results/summary.json', 'androidTest-results/summary.json',
                                 'english-manchu/duplicate/summary.json'):
                    extra = root/'app-vertical'/relative
                    extra.parent.mkdir(parents=True, exist_ok=True); extra.write_bytes(original)
                    with self.assertRaisesRegex(ValueError, 'Exact vertical shard report inventory'):
                        read_app_reports(root, sdk)
                    extra.unlink()

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
                        verify_app_reports(expected(sdk), sdk, broken, SOURCE_DIGEST)
            for invalid in (29, str(sdk), float(sdk), True):
                with self.subTest(requested_sdk=invalid), self.assertRaises(ValueError):
                    verify_app_reports(expected(sdk), invalid, reports(sdk), SOURCE_DIGEST)

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
                    paths = report_paths(root/'report', sdk)
                    for phase, part in parts.items():
                        paths[phase].parent.mkdir(parents=True, exist_ok=True)
                        paths[phase].write_text(json.dumps(report_for(phase, part, sdk, source_tests_sha256(source))))
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
                    self.assertEqual({phase: receipt['phases'][phase] for phase in VERTICAL_SHARDS},
                                     {phase: 2 for phase in VERTICAL_SHARDS})
                    self.assertEqual(receipt['source_tests_sha256'], source_tests_sha256(source))
                    restart_receipt = root/'report/app/accepted-credit-restart/coverage.json'
                    if sdk == 35:
                        self.assertEqual(json.loads(restart_receipt.read_text()), receipt)
                    else:
                        self.assertFalse(restart_receipt.exists())

    def test_cli_rejects_same_inventory_with_changed_source_bytes_and_removes_stale_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = source_fixture(root)
            digest = source_tests_sha256(source)
            for phase, path in report_paths(root/'report', 35).items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(report_for(phase, app_partition(expected(), 35)[phase], 35, digest)))
            command = [sys.executable, str(ROOT/'tools/vertical_locale_matrix.py'), 'verify-reports',
                       '--source-tests', str(source), '--sdk', '35', '--root', str(root/'report')]
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            receipts = [root/'report/app/coverage.json', root/'report/app/accepted-credit-restart/coverage.json']
            self.assertTrue(all(path.is_file() for path in receipts))
            path = source/'VerticalLocaleDeviceTest.kt'
            path.write_text(path.read_text()+'// Source changed after these reports were captured.\n')
            self.assertEqual(declared_tests(source), expected())
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('exact successful SDK-specific inventory', result.stderr)
            self.assertTrue(all(not path.exists() for path in receipts))

    def test_missing_matrix_method_or_restart_phase_fails_closed(self):
        for broken in (expected()-{(VERTICAL, sorted(VERTICAL_METHODS)[0])},
                       expected() | {(VERTICAL, 'unexpected')}, expected()-{(RESTART_SEED, 'seed')}):
            with self.assertRaises(ValueError): app_partition(broken, 35)
        with self.assertRaises(ValueError): verify_app_reports(expected(), 30, reports(), SOURCE_DIGEST)

    def test_actual_source_contains_the_complete_four_locale_matrix(self):
        for sdk in (30, 35):
            selected = declared_tests(ROOT/'app/src/androidTest', sdk_level=sdk)
            parts = app_partition(selected, sdk)
            self.assertEqual([len(parts[phase]) for phase in VERTICAL_SHARDS], [2, 2])
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
    def test_each_shard_runs_once_with_normal_lifecycle_even_after_a_first_failure(self):
        for sdk in (30, 35):
            for failure in ('', 'truncated', 'assertion', 'timeout'):
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
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, 'tools')
from vertical_locale_matrix import VERTICAL_SHARDS, VERTICAL
args=sys.argv[1:]
with open('events', 'a') as out: out.write(json.dumps(args)+'\n')
if args[:3]==['shell','rm','-rf']: sys.exit(0)
if args[:3]==['shell','am','force-stop']: sys.exit(0)
if args[0]=='install': print('Success'); sys.exit(0)
if args==['shell','getprop','ro.build.version.sdk']: print(os.environ['TEST_SDK']); sys.exit(0)
if args[:4]==['shell','pm','list','instrumentation']:
    print('instrumentation:paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner (target=paint.anpaint.android)'); sys.exit(0)
if args[:3]==['shell','am','instrument']:
    assert '--no-restart' not in args and 'waitForActivitiesToComplete' not in args
    assert 'notClass' not in args
    selected=args[args.index('class')+1].split(',')
    assert len(selected)==2
    identities={tuple(item.split('#')) for item in selected}
    assert identities in VERTICAL_SHARDS.values()
    # Only the first shard fails: the second must execute exactly once afterward.
    failure=os.environ['TEST_FAILURE'] if identities==VERTICAL_SHARDS['vertical-english-manchu'] else ''
    for owner, method in sorted(identities):
        for code in (1, -2 if failure=='assertion' else 0):
            print('INSTRUMENTATION_STATUS: class='+owner)
            print('INSTRUMENTATION_STATUS: test='+method)
            print('INSTRUMENTATION_STATUS: numtests=2')
            print('INSTRUMENTATION_STATUS_CODE: '+str(code))
    if failure!='truncated': print('INSTRUMENTATION_CODE: -1')
    if failure=='timeout':
        sys.stdout.flush(); time.sleep(30)
    sys.exit(0)
raise SystemExit('Unexpected command: '+repr(args))
''')
                    fake.chmod(0o700)
                    # Keep the production driver and runner untouched. Only this host
                    # harness shortens capture_live's wait to 1s after asserting that
                    # the real call requested its unchanged 180s ceiling.
                    shim = root/'runner-harness.py'
                    shim.write_text("import sys\nfrom unittest.mock import patch\nsys.path.insert(0, 'tools')\n"
                        "import run_android_instrumentation as runner\n"
                        "sys.argv = sys.argv[1:]\noriginal = runner.capture_live\n"
                        "def capture(command, log, seconds):\n"
                        "    assert seconds == 180\n    return original(command, log, 1)\n"
                        "with patch.object(runner, 'capture_live', side_effect=capture):\n"
                        "    raise SystemExit(runner.main())\n")
                    command = ('source "$CI_SCRIPT"; '
                        'python3() { command "$PYTHON_EXE" "$PWD/runner-harness.py" "$@"; }; '
                        'report="$PWD/report"; adb="$PWD/adb"; variant=debug; run_vertical_locale_matrix')
                    result = subprocess.run(['bash', '-c', command], cwd=root, capture_output=True, text=True, timeout=15,
                        env={**os.environ, 'CI_SCRIPT': str(ROOT/'tools/ci_emulator.sh'), 'TEST_SDK': str(sdk), 'TEST_FAILURE': failure, 'PYTHON_EXE': sys.executable})
                    self.assertEqual(result.returncode, 1 if failure else 0, result.stdout+result.stderr)
                    self.assertFalse(stale.exists())
                    paths = report_paths(root/'report', sdk)
                    for phase in VERTICAL_SHARDS:
                        report = json.loads(paths[phase].read_text())
                        self.assertEqual(report['success'], not failure or phase != 'vertical-english-manchu')
                        self.assertEqual(report['expected_tests'], 2)
                        self.assertEqual(report['timeout_seconds'], 180)
                        self.assertEqual(report['timed_out'], failure=='timeout' and phase=='vertical-english-manchu')
                        self.assertEqual(report['source_tests_sha256'], source_tests_sha256(root/'app/src/androidTest'))
                        self.assertEqual(report['included_tests'], sorted(f'{owner}#{name}' for owner, name in VERTICAL_SHARDS[phase]))
                    events = [json.loads(line) for line in (root/'events').read_text().splitlines()]
                    calls = [event for event in events if event[:3]==['shell','am','instrument']]
                    self.assertEqual(len(calls), 2)
                    self.assertNotEqual(calls[0], calls[1])
                    self.assertEqual(sum(event[:3]==['shell','rm','-rf'] for event in events), 1)
                    self.assertEqual(sum(event[:3]==['shell','am','force-stop'] for event in events), 1 if failure=='timeout' else 0)
                    self.assertEqual(events[0][:3], ['shell','rm','-rf'])

    def test_cleanup_collects_before_shutdown_and_never_turns_a_failure_green(self):
        for start, fault, expected_status in ((0, '', 0), (0, 'pull', 1), (0, 'missing', 1),
                                              (7, 'pull', 7), (7, 'missing', 7), (0, 'reachability_missing', 1),
                                              (0, 'reachability_failed', 1), (7, 'reachability_failed', 7)):
            with self.subTest(start=start, fault=fault), tempfile.TemporaryDirectory() as directory:
                root = Path(directory); (root/'report').mkdir()
                shutil.copytree(ROOT/'tools', root/'tools', ignore=shutil.ignore_patterns('__pycache__'))
                screenshot_fixture(root/'device')
                reachability_fixture(root/'device/reachability')
                if fault == 'missing': (root/'device'/sorted(EXPECTED_SCREENSHOTS)[0]).unlink()
                if fault.startswith('reachability_'):
                    receipt=next((root/'device/reachability').glob('*.json'))
                    if fault=='reachability_missing': receipt.unlink()
                    else:
                        data=json.loads(receipt.read_text());data['success']=False;receipt.write_text(json.dumps(data))
                fake = root/'adb'
                fake.write_text('#!'+sys.executable+'\n'+r'''
import json, os, shutil, sys
with open('events','a') as out: out.write(json.dumps(sys.argv[1:])+'\n')
if sys.argv[1]=='pull':
    if os.environ['TEST_FAULT']=='pull': sys.exit(1)
    shutil.copytree('device',sys.argv[3])
''')
                fake.chmod(0o700)
                command = 'source "$CI_SCRIPT"; report="$PWD/report"; adb="$PWD/adb"; emulator_pid=""; TEST_API=35; vertical_started=1; phase=test; trap cleanup EXIT; exit "$INITIAL_STATUS"'
                result = subprocess.run(['bash','-c',command], cwd=root, capture_output=True, text=True, timeout=15,
                    env={**os.environ, 'CI_SCRIPT': str(ROOT/'tools/ci_emulator.sh'), 'INITIAL_STATUS': str(start), 'TEST_FAULT': fault})
                self.assertEqual(result.returncode, expected_status, result.stdout+result.stderr)
                events = [json.loads(line) for line in (root/'events').read_text().splitlines()]
                self.assertLess(next(i for i, event in enumerate(events) if event[0]=='pull'),
                                next(i for i, event in enumerate(events) if event[:2]==['emu','kill']))
                self.assertEqual((root/'report/vertical-locale-screenshots.json').exists(), fault not in ('pull','missing'))
                self.assertEqual((root/'report/vertical-control-reachability.json').exists(), not fault)


if __name__ == '__main__':
    unittest.main()
