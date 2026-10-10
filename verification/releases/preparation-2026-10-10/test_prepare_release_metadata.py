"""Synthetic metadata contracts. These are not app/device execution results."""
import copy
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

SOURCE = (Path(os.environ['ANPAINT_SOURCE']) if 'ANPAINT_SOURCE' in os.environ else
          next(parent for parent in Path(__file__).resolve().parents
               if (parent / 'tools/publish_github_release.py').is_file()))
sys.path.insert(0, str(SOURCE / 'tools'))
import prepare_release_metadata as prep
from app_instrumentation_matrix import app_partition, report_paths, PHASE_TIMEOUTS, SELECTED_PHASES
from run_android_instrumentation import declared_tests, source_tests_sha256, parse_protocol, write_reports


def protocol(wanted):
    output = ''
    for owner, name in sorted(wanted):
        for code in (1, 0):
            output += (f'INSTRUMENTATION_STATUS: class={owner}\nINSTRUMENTATION_STATUS: test={name}\n'
                       f'INSTRUMENTATION_STATUS: numtests={len(wanted)}\nINSTRUMENTATION_STATUS_CODE: {code}\n')
    return output + 'INSTRUMENTATION_CODE: -1\n'


def synthetic_device(root, sdk):
    app_source = SOURCE / 'app/src/androidTest'
    native_source = SOURCE / 'Paintroid/src/androidTest'
    expected = declared_tests(app_source, sdk_level=sdk)
    phases = app_partition(expected, sdk)
    locations = {k: p.parent for k, p in report_paths(root, sdk).items()}
    excludes = ['org.catrobat.paintroid.classic.UltraHdrImportTest'] if sdk == 30 else []
    phases['native'] = {x for x in declared_tests(native_source, sdk_level=sdk) if x[0] not in excludes}
    locations['native'] = root / 'Paintroid/androidTest-results'
    for phase, wanted in phases.items():
        source = native_source if phase == 'native' else app_source
        raw = protocol(wanted)
        result = parse_protocol(raw, wanted)
        result.update(device_sdk=sdk, source_tests_sha256=source_tests_sha256(source),
                      included_tests=sorted(f'{c}#{t}' for c, t in wanted) if phase in SELECTED_PHASES else [],
                      sdk_suppressed_tests=sorted(declared_tests(source) - declared_tests(source, sdk_level=sdk)),
                      excluded_classes=excludes if phase == 'native' else [],
                      timeout_seconds=180 if phase == 'native' else PHASE_TIMEOUTS[phase],
                      leave_target_running=phase == 'seed')
        locations[phase].mkdir(parents=True)
        write_reports(locations[phase], 'phase-' + phase, result, 1.0)
        (locations[phase] / 'instrumentation.log').write_text(raw)


class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.commit = 'a' * 40
        self.run_id = 123
        self.workflow = dict(id=123, status='completed', head_sha=self.commit, conclusion='success',
                             path='.github/workflows/android.yml', event='push', head_branch='develop')
        self.jobs = [dict(name=name, status='completed', conclusion='success') for name in (
            'Regression tests and lint', 'Build APK and corresponding source', 'Emulator API 30',
            'Emulator API 35', 'Exact-script resource generation')]
        self.info = dict(commit=self.commit, run_id='123', build_variant='release',
                         apk_sha256='b'*64, source_sha256='c'*64)

    def test_successful_exact_develop_release_compatible_with_actual_publisher(self):
        prep.verify_identity(self.workflow, self.jobs, self.info, self.commit, self.run_id)

    def test_pr_dispatch_branch_pending_failure_and_wrong_workflow_rejected(self):
        mutations = dict(event=['pull_request', 'workflow_dispatch'], head_branch=['feature'],
                         status=['in_progress'], conclusion=['failure', None], head_sha=['d'*40],
                         path=['.github/workflows/other.yml'], id=[122])
        for key, values in mutations.items():
            for value in values:
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    prep.verify_identity(dict(self.workflow, **{key:value}), self.jobs, self.info,
                                         self.commit, self.run_id)

    def test_every_required_job_is_mandatory_and_must_have_passed(self):
        for index in range(len(self.jobs)):
            for status in ('failure', 'skipped', None):
                jobs = copy.deepcopy(self.jobs); jobs[index]['conclusion'] = status
                with self.subTest(index=index, status=status), self.assertRaises(ValueError):
                    prep.verify_identity(self.workflow, jobs, self.info, self.commit, self.run_id)
            with self.assertRaises(ValueError):
                prep.verify_identity(self.workflow, self.jobs[:index]+self.jobs[index+1:], self.info,
                                     self.commit, self.run_id)

    def test_stale_debug_or_malformed_artifact_identity_rejected(self):
        for key, value in dict(commit='d'*40, run_id=122, build_variant='debug',
                               apk_sha256='PENDING', source_sha256='').items():
            with self.subTest(key=key), self.assertRaises(ValueError):
                prep.verify_identity(self.workflow, self.jobs, dict(self.info, **{key:value}),
                                     self.commit, self.run_id)


class JunitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.directory = self.root / 'regression'; self.directory.mkdir()
        self.path = self.directory / 'TEST-example.xml'
        self.path.write_text('<testsuite tests="1" failures="0" errors="0" skipped="0"><testcase classname="example.Test" name="works"/></testsuite>')
    def tearDown(self): self.temp.cleanup()
    def collect(self): return prep.collect_junit(self.directory, 'regression', self.root)

    def test_real_relative_path_and_fresh_hash(self):
        rows, suites = self.collect()
        self.assertEqual(suites, 1)
        self.assertEqual(rows[0]['report'], 'regression/TEST-example.xml')
        self.assertEqual(rows[0]['report_sha256'], prep.sha256(self.path))

    def test_duplicate_identities_across_different_reports_rejected(self):
        shutil.copy(self.path, self.directory / 'TEST-duplicate.xml')
        with self.assertRaises(ValueError): self.collect()

    def test_missing_empty_or_wrong_total_rejected(self):
        for text in ('<testsuite tests="0"/>', '<testsuite tests="2"><testcase classname="a" name="b"/></testsuite>'):
            self.path.write_text(text)
            with self.assertRaises(ValueError): self.collect()
        self.path.unlink()
        with self.assertRaises(ValueError): self.collect()

    def test_failure_error_and_skip_children_rejected_even_with_false_green_totals(self):
        for child in ('failure', 'error', 'skipped'):
            self.path.write_text(f'<testsuite tests="1"><testcase classname="a" name="b"><{child}/></testcase></testsuite>')
            with self.assertRaises(ValueError): self.collect()

    def test_failure_error_and_skip_totals_rejected_even_without_children(self):
        for field in ('failures', 'errors', 'skipped'):
            self.path.write_text(f'<testsuite tests="1" {field}="1"><testcase classname="a" name="b"/></testsuite>')
            with self.assertRaises(ValueError): self.collect()

    def test_disabled_case_and_symlink_escape_rejected(self):
        self.path.write_text('<testsuite tests="1"><testcase classname="a" name="b" status="notrun"/></testsuite>')
        with self.assertRaises(ValueError): self.collect()
        self.path.unlink()
        outside = self.root.parent / (self.root.name + '-outside.xml')
        try:
            outside.write_text('<testsuite tests="1"><testcase classname="a" name="b"/></testsuite>')
            self.path.symlink_to(outside)
            with self.assertRaises(ValueError): self.collect()
        finally: outside.unlink()


class DeviceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        synthetic_device(self.root / 'emulator30', 30)
        synthetic_device(self.root / 'emulator35', 35)
    def tearDown(self): self.temp.cleanup()
    def validate(self, sdk=35): return prep.validate_device(self.root / f'emulator{sdk}', SOURCE, sdk)

    def test_current_phase_split_union_and_all_raw_logs_synthetic(self):
        for sdk, total, app in ((30,95,22),(35,99,25)):
            result = self.validate(sdk)
            self.assertEqual(result['installed_tests'], total)
            self.assertEqual(result['app_tests'], app)
            rows, suites = prep.collect_junit(self.root/f'emulator{sdk}', f'emulator{sdk}', self.root)
            self.assertEqual(len(rows), total)
            self.assertEqual(suites, 5 if sdk == 30 else 7)
            gallery = next(x for x in rows if x['class'].endswith('GalleryDraftDeviceTest'))
            self.assertIn('app-gallery-draft/androidTest-results/TEST-phase-gallery-draft.xml', gallery['report'])
            vertical = next(x for x in rows if x['class'].endswith('VerticalLocaleDeviceTest'))
            self.assertIn('/app-vertical/', vertical['report'])
            if sdk == 35:
                seed = next(x for x in rows if x['class'].endswith('AcceptedCreditRestartSeedTest'))
                self.assertIn('/accepted-credit-restart/seed/', seed['report'])

    def test_missing_gallery_phase_rejected(self):
        report_paths(self.root/'emulator35',35)['gallery-draft'].unlink()
        with self.assertRaises((ValueError,FileNotFoundError)): self.validate()

    def test_stale_aggregate_xml_rejected(self):
        target = self.root/'emulator35/TEST-app-old.xml'; target.write_text('<testsuite/>')
        with self.assertRaises(ValueError): self.validate()

    def test_modified_raw_log_rejected_despite_green_summary(self):
        path = report_paths(self.root/'emulator35',35)['ordinary'].parent/'instrumentation.log'
        path.write_text(path.read_text().replace('INSTRUMENTATION_CODE: -1','INSTRUMENTATION_CODE: 0'))
        with self.assertRaises(ValueError): self.validate()

    def test_native_stale_source_digest_rejected(self):
        path = self.root/'emulator35/Paintroid/androidTest-results/summary.json'
        value = prep.read_json(path); value['source_tests_sha256'] = '0'*64
        path.write_text(json.dumps(value))
        with self.assertRaises(ValueError): self.validate()

    def test_mutated_phase_xml_inventory_rejected(self):
        path = next((self.root/'emulator35/app-gallery-draft').rglob('TEST-*.xml'))
        tree = ET.parse(path); tree.getroot().find('testcase').set('name','invented')
        tree.write(path)
        with self.assertRaises(ValueError): self.validate()

    def test_api30_cannot_claim_api35_restart_tests(self):
        shutil.copytree(self.root/'emulator35/app/accepted-credit-restart',
                        self.root/'emulator30/app/accepted-credit-restart')
        with self.assertRaises(ValueError): self.validate(30)


class LegacyReconciliationTests(unittest.TestCase):
    def test_behavior_changes_are_explicit_not_passing_old_test_names(self):
        current = {item for row in prep.SUPERSEDED.values() for item in row['current']}
        result = prep.reconcile_legacy(set(prep.SUPERSEDED), current)
        self.assertEqual(result['historical_feature_selectors_present'], 0)
        self.assertEqual(len(result['superseded_historical_selectors']), 2)
        self.assertTrue(all(row['reason'] for row in result['superseded_historical_selectors']))

    def test_each_replacement_is_mandatory(self):
        current = {item for row in prep.SUPERSEDED.values() for item in row['current']}
        for item in current:
            with self.subTest(item=item), self.assertRaises(ValueError):
                prep.reconcile_legacy(set(prep.SUPERSEDED), current - {item})

    def test_unexplained_disappearing_feature_fails_closed(self):
        with self.assertRaises(ValueError): prep.reconcile_legacy({('regression','Test','unknown')},set())


class AssembleTests(IdentityTests):
    def setUp(self):
        super().setUp()
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        synthetic_device(self.root/'emulator30',30); synthetic_device(self.root/'emulator35',35)
        directory = self.root/'regression/Paintroid/build/test-results/testReleaseUnitTest'; directory.mkdir(parents=True)
        (directory/'TEST-host.xml').write_text('<testsuite tests="1"><testcase classname="host.Test" name="works"/></testsuite>')
        directory = self.root/'regression/app/build/reports'; directory.mkdir(parents=True)
        (directory/'lint-results-release.xml').write_text('<issues/>')
        self.patch = dict(format=1,input_sha256='b'*64,output_sha256='d'*64)
        self.legacy = {'version':'OLD','commit':'OLD','feature_checks':{'checks':[
            dict(platform='regression',**{'class':'host.Test'},test='works',report='OLD',report_sha256='OLD')]}}
    def tearDown(self): self.temp.cleanup()
    def assemble(self):
        return prep.assemble(SOURCE,self.root,self.workflow,self.jobs,self.info,self.commit,123,'d'*64,self.patch,self.legacy)

    def test_synthetic_end_to_end_deterministic_no_old_identity_or_hashes(self):
        first = self.assemble(); second = self.assemble(); self.assertEqual(first,second)
        request, summary = first
        self.assertEqual(request['version'],'0.0.38'); self.assertEqual(request['version_code'],95)
        self.assertEqual(len(request['feature_checks']['checks']),195)
        self.assertEqual(summary['historical_feature_selectors_present'],1)
        self.assertNotIn('OLD',json.dumps(request))

    def test_bad_public_patch_hash_rejected(self):
        self.patch['input_sha256']='e'*64
        with self.assertRaises(ValueError):self.assemble()

    def test_missing_historical_feature_selector_rejected(self):
        self.legacy['feature_checks']['checks'][0]['test']='missing'
        with self.assertRaises(ValueError):self.assemble()

    def test_lint_issue_rejected(self):
        (self.root/'regression/app/build/reports/lint-results-release.xml').write_text('<issues><issue/></issues>')
        with self.assertRaises(ValueError):self.assemble()


if __name__ == '__main__': unittest.main()
