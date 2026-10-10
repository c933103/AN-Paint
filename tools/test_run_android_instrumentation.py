"""Protocol regression checks: adb returning zero is insufficient evidence."""
import copy
import json
import subprocess
import sys
import tempfile
from unittest.mock import patch
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from run_android_instrumentation import (declared_tests, parse_protocol, write_reports, main,
    RESTART_SEED, RESTART_VERIFY, restart_partition, verify_restart_reports)

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


class SdkInventoryTest(unittest.TestCase):
    def inventory(self, body, sdk, class_annotation=''):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'EditorTest.kt'
            path.write_text('package example\n' + class_annotation + '\nclass EditorTest {\n' + body + '\n}\n')
            return declared_tests(Path(directory), sdk_level=sdk)

    def test_method_bounds_are_inclusive_and_all_inventory_is_preserved(self):
        body = ('@Test @SdkSuppress(minSdkVersion=30, maxSdkVersion=35) fun draw() {}\n'
                '@Test fun save() {}')
        self.assertEqual(self.inventory(body, None), EXPECTED)
        for sdk in (30, 35):
            self.assertEqual(self.inventory(body, sdk), EXPECTED)
        for sdk in (29, 36):
            self.assertEqual(self.inventory(body, sdk), {(OWNER, 'save')})

    def test_class_bounds_and_method_override_match_androidx_precedence(self):
        body = ('@SdkSuppress(minSdkVersion=29, maxSdkVersion=30) @Test fun draw() {}\n'
                '@Test fun save() {}')
        annotation = '@SdkSuppress(minSdkVersion=33, maxSdkVersion=35)'
        self.assertEqual(self.inventory(body, 30, annotation), {(OWNER, 'draw')})
        self.assertEqual(self.inventory(body, 35, annotation), {(OWNER, 'save')})
        self.assertEqual(self.inventory(body, 36, annotation), set())
        self.assertEqual(self.inventory(body, None, annotation), EXPECTED)

    def test_max_only_and_qualified_annotations(self):
        body = ('@Test @androidx.test.filters.SdkSuppress(maxSdkVersion = 30) fun draw() {}\n'
                '@Test fun save() {}')
        self.assertEqual(self.inventory(body, 30), EXPECTED)
        self.assertEqual(self.inventory(body, 35), {(OWNER, 'save')})

    def test_malformed_unknown_and_unsupported_sdk_annotations_fail_closed(self):
        bad = ['minSdkVersion=33, maxSdkVersion=30', 'minSdkVersion=-1',
               'minSdkVersion=0', 'minSdkVersion=Build.VERSION_CODES.TIRAMISU',
               'minSdkVersion=33, minSdkVersion=34', 'unknown=30',
               'excludedSdks=[30]', 'codeName="Tiramisu"', '',
               'minSdkVersion=33,', 'minSdkVersion=33 + 1']
        for arguments in bad:
            for sdk in (None, 30, 35):
                with self.subTest(arguments=arguments, sdk=sdk), self.assertRaises(ValueError):
                    self.inventory('@Test @SdkSuppress(' + arguments + ') fun draw() {}', sdk)
        for annotation in ('@SdkSuppress', '@SdkSuppress(minSdkVersion=(33))',
                           '@other.SdkSuppress(minSdkVersion=33)',
                           '@SdkSuppress(minSdkVersion=30) @SdkSuppress(maxSdkVersion=35)'):
            with self.subTest(annotation=annotation), self.assertRaises(ValueError):
                self.inventory('@Test ' + annotation + ' fun draw() {}', 30)

    def test_unassociated_sdk_annotation_and_duplicate_ineligible_methods_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory('@SdkSuppress(minSdkVersion=33) val unsupported = 1\n@Test fun draw() {}', 30)
        with self.assertRaises(ValueError):
            self.inventory('@Test @SdkSuppress(minSdkVersion=33) fun draw() {}\n'
                           '@Test @SdkSuppress(minSdkVersion=33) fun draw() {}', 30)
        for sdk in (0, -1, '30', True):
            with self.subTest(sdk=sdk), self.assertRaises(ValueError):
                self.inventory('@Test fun draw() {}', sdk)

    def test_api30_protocol_accepts_only_eligible_methods_and_api35_requires_both(self):
        body = ('@Test fun draw() {}\n@Test @SdkSuppress(minSdkVersion=33) fun save() {}')
        actual30 = passing('draw', 1) + 'INSTRUMENTATION_CODE: -1\n'
        self.assertTrue(parse_protocol(actual30, self.inventory(body, 30))['success'])
        self.assertFalse(parse_protocol(actual30, self.inventory(body, 35))['success'])
        self.assertFalse(parse_protocol(FINAL, self.inventory(body, 30))['success'])
        actual35 = passing('draw') + passing('save') + FINAL
        self.assertTrue(parse_protocol(actual35, self.inventory(body, 35))['success'])
        self.assertFalse(parse_protocol(actual35, self.inventory(body, 30))['success'])


class RestartModeTest(unittest.TestCase):
    def invoke(self, *, seed_mode=True, live='123', excluded=True, truncated=False, sdk='35'):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); source=root/'sources'; source.mkdir()
            for owner, method in ((RESTART_SEED, 'seed'), (RESTART_VERIFY, 'verify'), (OWNER, 'draw')):
                package, name=owner.rsplit('.',1)
                (source/(name+'.kt')).write_text(f'package {package}\nclass {name} {{ @Test fun {method}() {{}} }}\n')
            apk=root/'test.apk';apk.touch()
            args=['runner','--apk',str(apk),'--source-tests',str(source),'--output',str(root/'report'),
                  '--suite','seed','--component','test/Runner']
            if seed_mode:args.append('--leave-target-running')
            if excluded:args+=['--exclude-class',RESTART_VERIFY,'--exclude-class',OWNER]
            commands=[]
            def run(command, **kwargs):
                commands.append(command)
                if command[1:]==['shell','getprop','ro.build.version.sdk']:
                    return subprocess.CompletedProcess(command,0,sdk+'\n','')
                if command[1]=='install':return subprocess.CompletedProcess(command,0,'Success\n','')
                if command[1:]==['shell','pm','list','instrumentation']:
                    return subprocess.CompletedProcess(command,0,'instrumentation:test/Runner (target=paint.anpaint.android)\n','')
                if command[1:]==['shell','pidof','paint.anpaint.android']:
                    if not live:raise subprocess.CalledProcessError(1,command)
                    return subprocess.CompletedProcess(command,0,live+'\n','')
                raise AssertionError(command)
            def capture(command, log, deadline):
                commands.append(command)
                output=''.join(f'INSTRUMENTATION_STATUS: class={RESTART_SEED}\n'
                               f'INSTRUMENTATION_STATUS: test=seed\n'
                               f'INSTRUMENTATION_STATUS: numtests=1\nINSTRUMENTATION_STATUS_CODE: {code}\n'
                               for code in (1,0))
                log.write_text(output+('' if truncated else 'INSTRUMENTATION_CODE: -1\n'))
                return 0,False
            with patch.object(sys,'argv',args), patch('run_android_instrumentation.subprocess.run',side_effect=run), \
                    patch('run_android_instrumentation.capture_live',side_effect=capture):
                status=main()
            return status,commands,json.loads((root/'report/summary.json').read_text())

    def test_device_sdk_query_is_recorded_and_invalid_result_fails_closed(self):
        status,commands,report=self.invoke()
        self.assertEqual(status,0)
        self.assertIn(['adb','shell','getprop','ro.build.version.sdk'],commands)
        self.assertEqual(report['device_sdk'],35)
        self.assertEqual(report['sdk_suppressed_tests'],[])
        for sdk in ('', 'SDK35', '0', '35\\n30'):
            with self.subTest(sdk=sdk):
                status,commands,report=self.invoke(sdk=sdk)
                self.assertEqual(status,1)
                self.assertFalse(any(c[1]=='install' for c in commands))

    def test_seed_emits_both_required_options_and_keeps_strict_complete_report(self):
        status,commands,report=self.invoke()
        self.assertEqual(status,0)
        command=commands[-1]
        self.assertIn('--no-restart',command)
        i=command.index('waitForActivitiesToComplete')
        self.assertEqual(command[i-1:i+2],['-e','waitForActivitiesToComplete','false'])
        self.assertTrue(report['leave_target_running'])
        self.assertEqual(report['target_pid_before_instrumentation'],123)
        self.assertEqual(report['completed_tests'],1)

    def test_normal_mode_preserves_original_command_and_cleanup_defaults(self):
        status,commands,report=self.invoke(seed_mode=False)
        self.assertEqual(status,0)
        self.assertNotIn('--no-restart',commands[-1])
        self.assertNotIn('waitForActivitiesToComplete',commands[-1])
        self.assertFalse(report['leave_target_running'])

    def test_seed_mode_rejects_extra_methods_and_unavailable_or_multiple_pids(self):
        for kwargs in ({'excluded':False},{'live':''},{'live':'123 456'}):
            with self.subTest(kwargs=kwargs):
                status,commands,report=self.invoke(**kwargs)
                self.assertEqual(status,1)
                self.assertFalse(report['success'])
                self.assertFalse(any('instrument' in command for command in commands))

    def test_seed_mode_does_not_accept_truncated_success(self):
        status,_,report=self.invoke(truncated=True)
        self.assertEqual(status,1)
        self.assertIn('Missing or unsuccessful final instrumentation result',str(report['errors']))

    def test_partition_covers_future_classes_and_rejects_missing_or_duplicate_phases(self):
        expected={(OWNER,'draw'),('example.FutureTest','future'),(RESTART_SEED,'seed'),(RESTART_VERIFY,'verify')}
        parts=restart_partition(expected)
        reports=[dict(success=True,device_sdk=35,expected_tests=len(part),completed_tests=len(part),
                      leave_target_running=(i==1),cases=[dict(classname=owner,name=name,status='passed')
                                                       for owner,name in sorted(part)])
                 for i,part in enumerate(parts)]
        self.assertEqual(verify_restart_reports(expected,reports)['completed_tests'],4)
        self.assertEqual(verify_restart_reports(expected,reports)['device_sdk'],35)
        for invalid in (None, 30, 36, '35', True):
            for phase in range(3):
                changed=copy.deepcopy(reports)
                if invalid is None:changed[phase].pop('device_sdk')
                else:changed[phase]['device_sdk']=invalid
                with self.subTest(sdk=invalid,phase=phase), self.assertRaises(ValueError):
                    verify_restart_reports(expected,changed)
        self.assertIn(('example.FutureTest','future'),parts[0])
        for bad in (reports[:2], [reports[0],reports[1],reports[1]]):
            with self.assertRaises(ValueError):verify_restart_reports(expected,bad)
        for missing in (expected-{(RESTART_SEED,'seed')},expected|{(RESTART_VERIFY,'extra')}):
            with self.assertRaises(ValueError):restart_partition(missing)
        reports[0]['cases'].pop()
        with self.assertRaises(ValueError):verify_restart_reports(expected,reports)


if __name__ == '__main__':
    unittest.main()

