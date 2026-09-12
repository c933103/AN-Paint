"""Protocol regression checks: adb returning zero is insufficient evidence."""
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from run_android_instrumentation import declared_tests, parse_protocol, write_reports

OWNER = 'example.EditorTest'
EXPECTED = {(OWNER, 'draw'), (OWNER, 'save')}


def event(method, code, count=2, stack=None):
    output = (f'INSTRUMENTATION_STATUS: class={OWNER}\n'
              f'INSTRUMENTATION_STATUS: test={method}\n'
              f'INSTRUMENTATION_STATUS: numtests={count}\n')
    if stack:
        output += f'INSTRUMENTATION_STATUS: stack={stack}\n'
    return output + f'INSTRUMENTATION_STATUS_CODE: {code}\n'


def passing(method, count=2):
    return event(method, 1, count) + event(method, 0, count)


FINAL = 'INSTRUMENTATION_RESULT: stream=\nOK (2 tests)\nINSTRUMENTATION_CODE: -1\n'


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
