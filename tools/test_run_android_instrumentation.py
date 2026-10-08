"""Protocol regression checks: adb returning zero is insufficient evidence."""
import json
import subprocess
import tempfile
from pathlib import Path
import unittest
from unittest import mock
import xml.etree.ElementTree as ET

from run_android_instrumentation import declared_tests, main, parse_protocol, select_tests, write_reports

OWNER = 'example.EditorTest'
EXPECTED = {(OWNER, 'draw'), (OWNER, 'save')}


def event(method, code, count=2, stack=None, owner=OWNER):
    output = (f'INSTRUMENTATION_STATUS: class={owner}\n'
              f'INSTRUMENTATION_STATUS: test={method}\n'
              f'INSTRUMENTATION_STATUS: numtests={count}\n')
    if stack:
        output += f'INSTRUMENTATION_STATUS: stack={stack}\n'
    return output + f'INSTRUMENTATION_STATUS_CODE: {code}\n'


def passing(method, count=2, owner=OWNER):
    return event(method, 1, count, owner=owner) + event(method, 0, count, owner=owner)


FINAL = 'INSTRUMENTATION_RESULT: stream=\nOK (2 tests)\nINSTRUMENTATION_CODE: -1\n'
VERTICAL = 'paint.anpaint.android.VerticalLocaleDeviceTest'
VERTICAL_TESTS = {(VERTICAL, name) for name in ('mongolian', 'manchu', 'xibe', 'nanai')}
GALLERY = 'paint.anpaint.android.GalleryDraftDeviceTest'


class ClassSelectionTest(unittest.TestCase):
    def test_real_app_inventory_is_partitioned_without_losing_or_repeating_methods(self):
        root = Path(__file__).resolve().parents[1] / 'app/src/androidTest'
        inventory = declared_tests(root)
        editor = select_tests(inventory, exclude_classes=[VERTICAL, GALLERY])
        gallery = select_tests(inventory, include_classes=[GALLERY])
        vertical = select_tests(inventory, include_classes=[VERTICAL])
        self.assertEqual(len(gallery), 3)
        self.assertEqual({owner for owner, _ in editor}, {'paint.anpaint.android.EditorDeviceTest'})
        self.assertEqual(editor | gallery | vertical, inventory)
        self.assertFalse(editor & gallery or editor & vertical or gallery & vertical)

    def test_complementary_class_runs_have_no_missing_or_duplicate_methods(self):
        inventory = EXPECTED | VERTICAL_TESTS
        editor = select_tests(inventory, exclude_classes=[VERTICAL])
        vertical = select_tests(inventory, include_classes=[VERTICAL])
        self.assertEqual(editor, EXPECTED)
        self.assertEqual(vertical, VERTICAL_TESTS)
        self.assertEqual(editor | vertical, inventory)
        self.assertFalse(editor & vertical)
        self.assertEqual(select_tests(inventory), inventory)
        self.assertEqual(select_tests(inventory, include_classes=[OWNER, VERTICAL]), inventory)

    def test_invalid_or_ambiguous_class_selectors_are_rejected(self):
        inventory = EXPECTED | VERTICAL_TESTS
        for options in (
            {'include_classes': ['example.Typo']},
            {'exclude_classes': ['example.Typo']},
            {'include_classes': [VERTICAL + '#mongolian']},
            {'include_classes': [OWNER + ',' + VERTICAL]},
            {'include_classes': [VERTICAL, VERTICAL]},
            {'exclude_classes': [VERTICAL, VERTICAL]},
            {'include_classes': [VERTICAL], 'exclude_classes': [OWNER]},
            {'exclude_classes': [OWNER, VERTICAL]},
        ):
            with self.subTest(options=options), self.assertRaises(ValueError):
                select_tests(inventory, **options)

    def test_empty_inventory_cannot_be_selected(self):
        with self.assertRaises(ValueError):
            select_tests(set())

    def test_cli_selection_matches_adb_filter_and_report_inventory(self):
        for flag, selected, argument in (
            ('--include-class', VERTICAL_TESTS, 'class'),
            ('--exclude-class', EXPECTED, 'notClass'),
        ):
            with self.subTest(flag=flag), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / 'source'
                source.mkdir()
                for owner, methods in ((OWNER, ['draw', 'save']),
                                       (VERTICAL, ['mongolian', 'manchu', 'xibe', 'nanai'])):
                    package, _, name = owner.rpartition('.')
                    (source / (name + '.kt')).write_text(
                        f'package {package}\nclass {name} {{\n' +
                        '\n'.join(f'@Test fun {method}() {{}}' for method in methods) + '\n}\n')
                apk = root / 'tests.apk'
                apk.touch()
                output = root / 'reports'
                component = 'example.test/androidx.test.runner.AndroidJUnitRunner'
                argv = ['runner', '--adb', 'test-adb', '--apk', str(apk),
                        '--source-tests', str(source), '--output', str(output),
                        '--suite', 'selected', '--component', component,
                        '--timeout-seconds', '180', flag, VERTICAL]

                def capture(command, log, deadline):
                    log.write_text(''.join(passing(name, len(selected), owner=owner)
                                           for owner, name in sorted(selected)) +
                                   'INSTRUMENTATION_CODE: -1\n')
                    return 0, False

                responses = [subprocess.CompletedProcess([], 0, 'Success\n', ''),
                             subprocess.CompletedProcess([], 0,
                                 f'instrumentation:{component} (target=example)\n', '')]
                with mock.patch('sys.argv', argv), \
                        mock.patch('run_android_instrumentation.subprocess.run', side_effect=responses), \
                        mock.patch('run_android_instrumentation.capture_live', side_effect=capture) as run, \
                        mock.patch('builtins.print'):
                    self.assertEqual(main(), 0)
                self.assertEqual(run.call_args.args, (
                    ['test-adb', 'shell', 'am', 'instrument', '-w', '-r',
                     '-e', argument, VERTICAL, component], output / 'instrumentation.log', 180))
                report = json.loads((output / 'summary.json').read_text())
                self.assertTrue(report['success'], report)
                self.assertEqual(report['expected_tests'], len(selected))
                self.assertEqual({(case['classname'], case['name']) for case in report['cases']}, selected)
                self.assertEqual(report['included_classes'], [VERTICAL] if argument == 'class' else [])
                self.assertEqual(report['excluded_classes'], [VERTICAL] if argument == 'notClass' else [])

    def test_unknown_class_fails_before_adb_and_still_writes_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'EditorTest.kt').write_text('package example\nclass EditorTest {\n@Test fun draw() {}\n}\n')
            output = root / 'reports'
            with mock.patch('sys.argv', ['runner', '--apk', str(root / 'tests.apk'),
                    '--source-tests', str(root), '--output', str(output), '--suite', 'selected',
                    '--include-class', 'example.Typo']), \
                    mock.patch('run_android_instrumentation.subprocess.run') as adb, \
                    mock.patch('builtins.print'):
                self.assertEqual(main(), 1)
            adb.assert_not_called()
            report = json.loads((output / 'summary.json').read_text())
            self.assertFalse(report['success'])
            self.assertIn('Included class not found in source inventory', '\n'.join(report['errors']))
            self.assertTrue((output / 'TEST-selected.xml').is_file())


class ProtocolTest(unittest.TestCase):
    def test_complete_success_matches_declared_methods(self):
        result = parse_protocol(passing('draw') + passing('save') + FINAL, EXPECTED)
        self.assertTrue(result['success'], result)
        self.assertEqual(result['completed_tests'], 2)

    def test_adb_zero_does_not_hide_assertion_failure(self):
        output = passing('draw') + event('save', 1) + event('save', -2, stack='AssertionError: pixels\n  at example.Save') + FINAL
        result = parse_protocol(output, EXPECTED, returncode=0)
        self.assertFalse(result['success'])
        self.assertEqual(result['cases'][1]['status'], 'failure')
        self.assertIn('at example.Save', result['cases'][1]['message'])

    def test_truncated_run_preserves_partial_result_and_errors(self):
        result = parse_protocol(passing('draw') + event('save', 1), EXPECTED, timed_out=True)
        self.assertFalse(result['success'])
        self.assertEqual(result['completed_tests'], 1)
        self.assertEqual(result['missing'], [(OWNER, 'save')])
        with tempfile.TemporaryDirectory() as directory:
            write_reports(Path(directory), 'native', result, 480)
            root = ET.parse(Path(directory) / 'TEST-native.xml').getroot()
            self.assertEqual(len(root.findall('testcase')), 3)
            self.assertEqual(root.find('testcase').get('name'), 'draw')
            self.assertEqual(root.get('errors'), '2')
            self.assertTrue((Path(directory) / 'summary.json').is_file())

    def test_ignored_and_assumption_skips_fail(self):
        for skip in (-3, -4):
            with self.subTest(skip=skip):
                result = parse_protocol(passing('draw') + event('save', skip) + FINAL, EXPECTED)
                self.assertFalse(result['success'])
                self.assertEqual(result['cases'][1]['status'], 'skipped')

    def test_missing_method_rejected_even_with_final_ok(self):
        result = parse_protocol(passing('draw', 1) + FINAL, EXPECTED)
        self.assertFalse(result['success'])
        self.assertEqual(result['missing'], [(OWNER, 'save')])

    def test_missing_final_result_and_runner_abort_fail(self):
        output = passing('draw') + passing('save')
        for ending in ('', 'INSTRUMENTATION_FAILED: Process crashed.\n',
                       'INSTRUMENTATION_RESULT: shortMsg=Process crashed.\nINSTRUMENTATION_CODE: 0\n'):
            with self.subTest(ending=ending):
                self.assertFalse(parse_protocol(output + ending, EXPECTED)['success'])

    def test_unexpected_duplicate_and_zero_tests_rejected(self):
        for output in (passing('draw') + passing('other') + FINAL,
                       passing('draw') + passing('draw') + passing('save') + FINAL,
                       FINAL):
            self.assertFalse(parse_protocol(output, EXPECTED)['success'])

    def test_same_line_annotations_are_included_in_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'EditorTest.kt'
            path.write_text('package example\nclass EditorTest {\n'
                            '@Test @Config(sdk = [35]) fun draw() {}\n'
                            '@Test\nfun save() {}\n}\n')
            self.assertEqual(declared_tests(Path(directory)), EXPECTED)
            path.write_text('package example\nclass EditorTest {\n@Test val unsupported = 1\n}\n')
            with self.assertRaises(ValueError):
                declared_tests(Path(directory))


if __name__ == '__main__':
    unittest.main()
