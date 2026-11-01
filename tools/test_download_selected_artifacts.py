"""Exercise exact-ID transport and hash-before-extract, without network access."""
import hashlib
import copy
import json
import io
import os
from pathlib import Path
import stat
import shutil
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from download_selected_artifacts import download, extract, preflight, equivalence_main
from select_device_artifacts import select
from test_select_device_artifacts import ARGS, metadata, equivalence_metadata, review_metadata


def bundle(name='device-identity.json', data=b'original report'):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(name, data)
    return output.getvalue()


class DownloadSelectedArtifactsTest(unittest.TestCase):
    def test_lower_id_selected_from_duplicate_names_reaches_exact_rest_endpoint(self):
        artifacts, jobs = metadata()
        selected = select(artifacts, jobs, **ARGS)['selected']['position']
        data = bundle(); selected['digest'] = 'sha256:' + hashlib.sha256(data).hexdigest()
        calls = []
        def runner(command, **kwargs):
            calls.append((command, kwargs))
            kwargs['stdout'].write(data)
            return SimpleNamespace(returncode=0)
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'GH_DEBUG': 'api'}):
            root = Path(directory) / 'reports'
            download('c933103/AN-Paint', selected, root, runner)
            self.assertEqual((root / 'device-identity.json').read_bytes(), b'original report')
        self.assertEqual(calls[0][0], ['gh', 'api', '--hostname', 'github.com', '--method', 'GET',
            '/repos/c933103/AN-Paint/actions/artifacts/80/zip'])
        self.assertEqual(calls[0][1]['timeout'], 90)
        self.assertNotIn('GH_DEBUG', calls[0][1]['env'])
        self.assertFalse(calls[0][1]['check'])

    def test_failed_or_timed_out_transport_never_extracts(self):
        record = dict(artifact_id=80, digest='sha256:' + 'c' * 64)
        def failure(*args, **kwargs):
            kwargs['stdout'].write(bundle())
            return SimpleNamespace(returncode=1)
        def timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired('gh', 90)
        for runner, error in [(failure, ValueError), (timeout, subprocess.TimeoutExpired)]:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / 'reports'
                with self.assertRaises(error):
                    download('c933103/AN-Paint', record, root, runner)
                self.assertFalse(root.exists())

    def test_digest_mismatch_and_compressed_limit_fail_before_extraction(self):
        data = bundle(); digest = 'sha256:' + hashlib.sha256(data).hexdigest()
        def runner(*args, **kwargs):
            kwargs['stdout'].write(data); return SimpleNamespace(returncode=0)
        for expected, limit in [('sha256:' + '0' * 64, len(data)), (digest, len(data) - 1)]:
            with tempfile.TemporaryDirectory() as directory, patch('download_selected_artifacts.MAX_ARCHIVE', limit):
                root = Path(directory) / 'reports'
                with self.assertRaises(ValueError):
                    download('c933103/AN-Paint', dict(artifact_id=80, digest=expected), root, runner)
                self.assertFalse(root.exists())

        # Only explicitly identified APK/source bundles use the larger bound.
        with tempfile.TemporaryDirectory() as directory, patch('download_selected_artifacts.MAX_ARCHIVE', 1):
            root = Path(directory)/'build'
            download('c933103/AN-Paint', dict(artifact_id=80, digest=digest,
                     name='apk-and-source-'+'a'*40), root, runner, kind='apk-source')
            self.assertTrue((root/'device-identity.json').exists())
        with self.assertRaises(ValueError):
            download('c933103/AN-Paint', dict(artifact_id=80, digest=digest,
                     name='regression-and-lint-'+'a'*40), Path('unused'), runner, kind='apk-source')

    def test_invalid_identity_or_digest_never_invokes_transport(self):
        def runner(*args, **kwargs):
            self.fail('Invalid metadata reached transport')
        for repo, identity, digest in [('owner/name/other', 80, 'sha256:' + 'c' * 64),
                ('owner/name', True, 'sha256:' + 'c' * 64), ('owner/name', 80, 'not-a-digest')]:
            with self.assertRaises(ValueError):
                download(repo, dict(artifact_id=identity, digest=digest), Path('unused'), runner)

    def test_path_traversal_absolute_paths_backslashes_and_symlinks_fail_closed(self):
        link = zipfile.ZipInfo('link'); link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        for name in ['../escape', '/absolute', 'nested/../../escape', 'nested\\escape', link]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / 'reports'
                with self.assertRaises(ValueError):
                    extract(io.BytesIO(bundle(name)), root)
                self.assertFalse(root.exists())

    def test_existing_selection_receipt_and_reports_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); receipt = root / 'artifact-selection.json'
            receipt.write_text('original selection')
            with self.assertRaises(ValueError):
                extract(io.BytesIO(bundle('artifact-selection.json', b'overwritten')), root)
            self.assertEqual(receipt.read_text(), 'original selection')

    def test_expanded_limit_empty_archives_and_duplicate_members_fail_closed(self):
        empty = io.BytesIO()
        with zipfile.ZipFile(empty, 'w'): pass
        duplicate = io.BytesIO()
        with zipfile.ZipFile(duplicate, 'w') as archive:
            archive.writestr('same', 'first')
            with self.assertWarns(UserWarning): archive.writestr('same', 'second')
        for data, limit in [(bundle(), 1), (empty.getvalue(), 512), (duplicate.getvalue(), 512)]:
            with tempfile.TemporaryDirectory() as directory, patch('download_selected_artifacts.MAX_EXPANDED', limit):
                root = Path(directory) / 'reports'
                with self.assertRaises(ValueError): extract(io.BytesIO(data), root)
                self.assertFalse(root.exists())

    def test_preflight_binds_independent_metadata_before_accepting_original_artifacts(self):
        m, review = equivalence_metadata(), review_metadata()
        m['run']['pull_requests'] = []
        prefix = '/repos/c933103/AN-Paint'; original = m['tested_merge']['sha']
        groups = [('build', 'apk-and-source-'), ('tests', 'instrumentation-apks-'),
                  ('regression', 'regression-and-lint-'), ('exact', 'exact-script-generation-'),
                  ('core', 'emulator-core-api-35-'), ('position', 'emulator-position-api-35-')]
        artifacts = [dict(id=i+100, name=stem+original, expired=False, digest='sha256:'+'f'*64,
            workflow_run=dict(id=30, head_sha='b'*40), created_at='2026-11-01T10:30:00Z',
            updated_at='2026-11-01T10:30:00Z') for i, (_, stem) in enumerate(groups)]
        endpoints = {prefix+'/branches/develop': dict(protected=False, protection=dict(enabled=False, required_status_checks=dict(contexts=[], checks=[]))),
            prefix+'/rulesets?includes_parents=true&per_page=100': [], prefix: m['repository'], prefix+'/git/commits/'+'c'*40: m['merge'],
            prefix+'/git/commits/'+'d'*40: m['tested_merge'],
            prefix+'/git/commits/'+'a'*40: dict(tree=dict(sha='f'*40)),
            prefix+'/git/trees/'+'e'*40+'?recursive=1': dict(truncated=False, tree=[
                dict(type='blob', mode='100644', path='tools/policy.py', sha='f'*40),
                dict(type='blob', mode='100644', path='Paintroid/src/main/res/values-fr/strings.xml', sha='b'*40)]),
            prefix+'/git/trees/'+'f'*40+'?recursive=1': dict(truncated=False, tree=[
                dict(type='blob', mode='100644', path='tools/policy.py', sha='f'*40),
                dict(type='blob', mode='100644', path='Paintroid/src/main/res/values-fr/strings.xml', sha='a'*40)]),
            prefix+'/commits/'+'c'*40+'/pulls?per_page=100': copy.deepcopy(m['pull_requests']),
            prefix+'/commits/'+'b'*40+'/pulls?per_page=100': copy.deepcopy(m['pull_requests']),
            prefix+'/pulls/7': m['pull_requests'][0], prefix+'/actions/workflows/android.yml': dict(id=40),
            prefix+'/actions/workflows/android.yml/runs?event=pull_request&head_sha='+'b'*40+'&per_page=100&page=1': dict(total_count=1, workflow_runs=[m['run']]),
            prefix+'/actions/runs/30': m['run'],
            prefix+'/actions/runs/30/jobs?filter=all&per_page=100&page=1': dict(total_count=6, jobs=m['jobs']),
            prefix+'/actions/runs/30/artifacts?per_page=100&page=1': dict(total_count=6, artifacts=artifacts),
            prefix+'/issues/7/comments?per_page=100': [review['comment']],
            prefix+'/issues/comments/50': review['comment'],
            prefix+'/git/ref/heads/develop': dict(object=dict(sha='c'*40))}
        env = dict(GITHUB_REPOSITORY='c933103/AN-Paint', GITHUB_EVENT_NAME='push',
            GITHUB_REF='refs/heads/develop', GITHUB_SHA='c'*40, GITHUB_RUN_ATTEMPT='1', BUILD_VARIANT='debug')
        jobs = dict(build='build', regression='checks', exact='exact-script-resources', core='device', position='position')
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory); wrapper = checkout/'gradle/wrapper/gradle-wrapper.properties'
            wrapper.parent.mkdir(parents=True); wrapper.write_text('pinned distribution')
            def downloaded(repo, artifact, root, **kwargs):
                group = root.name
                if group == 'tests':
                    p = root/'app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk'
                    p.parent.mkdir(parents=True); p.write_bytes(b'test APK'); return
                relative = {'build':'build/delivery/observed-inputs.json', 'regression':'build/reports/ci-phases/observed-inputs.json'}.get(group, 'observed-inputs.json')
                packages = ['emulator/package.xml', 'system-images/android-35/google_apis/x86_64/package.xml'] if group in ('core','position') else ['platforms/android-35/package.xml','build-tools/35.0.0/package.xml','ndk/27.2.12479018/package.xml','cmake/3.22.1/package.xml']
                record = dict(commit=original, tree='e'*40, run_id='30', attempt='1', job=jobs[group],
                    image_os='ubuntu22', image_version='observed', java='observed Java17',
                    sdk_packages={p:dict(sha256='f'*64, revision=dict(major='35')) for p in packages},
                    runtime_dependencies=[dict(files={'actual.jar':'f'*64})], native_revision_inputs={'source/.anpaint-revision':'observed'},
                    gradle_wrapper_properties_sha256=hashlib.sha256(wrapper.read_bytes()).hexdigest())
                p = root/relative; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(record))
            with patch('download_selected_artifacts.subprocess.check_output', return_value='c'*40+'\n'), \
                    patch('download_selected_artifacts.download', side_effect=downloaded) as transfer, \
                    patch('compose_device_reports.verify_reuse_artifacts', return_value=dict(original_identity=dict(commit=original))) as verify:
                result = preflight(lambda url:copy.deepcopy(endpoints[url]), lambda node:copy.deepcopy(review['graphql']),
                    checkout, {'before':'a'*40}, env, checkout/'prior', m['now'])
                self.assertEqual(result['checkout'], original)
                self.assertEqual(result['association_proof'], 'unique-head-and-merge-pr')
                self.assertEqual(transfer.call_count, 6); verify.assert_called_once()
                self.assertEqual(verify.call_args.args[-1]['GITHUB_SHA'], original)
                self.assertNotEqual(result['merge'], original)
                # Code or Markdown changes cannot hide behind the resource-only exception.
                current_tree = endpoints[prefix+'/git/trees/'+'e'*40+'?recursive=1']['tree']
                current_tree[0]['sha'] = 'a'*40
                with self.assertRaises(ValueError):
                    preflight(lambda url:copy.deepcopy(endpoints[url]), lambda node:review['graphql'],
                              checkout, {'before':'a'*40}, env, checkout/'unused', m['now'])
                current_tree[0]['sha'] = 'f'*40
                for endpoint in (prefix+'/actions/workflows/android.yml/runs?event=pull_request&head_sha='+'b'*40+'&per_page=100&page=1', prefix+'/issues/7/comments?per_page=100',
                                 prefix+'/commits/'+'c'*40+'/pulls?per_page=100',
                                 prefix+'/commits/'+'b'*40+'/pulls?per_page=100'):
                    shutil.rmtree(checkout/'prior')
                    reads = {}
                    def changed(url):
                        reads[url] = reads.get(url, 0)+1
                        value = copy.deepcopy(endpoints[url])
                        if url == endpoint and reads[url] > 1:
                            if isinstance(value, list): value.append(dict(id=999, body='new summary'))
                            else:
                                value['workflow_runs'].append(dict(m['run'], id=99, conclusion='failure'))
                                value['total_count'] = 2
                        return value
                    with self.assertRaises(ValueError):
                        preflight(changed, lambda node:copy.deepcopy(review['graphql']), checkout,
                            {'before':'a'*40}, env, checkout/'prior', m['now'])

    def test_preflight_errors_clear_stale_acceptance_and_choose_normal_execution(self):
        with tempfile.TemporaryDirectory() as directory, patch('download_selected_artifacts.preflight', side_effect=ValueError('missing provenance')):
            root = Path(directory); event=root/'event.json'; event.write_text('{}')
            output=root/'output'; summary=root/'summary'
            old=os.getcwd()
            try:
                os.chdir(root)
                receipt=root/'build/reports/prior-evidence.json'; receipt.parent.mkdir(parents=True)
                receipt.write_text('{"reused":true}')
                with patch.dict(os.environ, GITHUB_EVENT_NAME='push', GITHUB_EVENT_PATH=str(event), GITHUB_OUTPUT=str(output), GITHUB_STEP_SUMMARY=str(summary)):
                    equivalence_main()
                self.assertFalse(json.loads(receipt.read_text())['reused'])
                self.assertEqual(output.read_text(), 'reused=false\n')
                event.write_text('{"number":7}')
                response = SimpleNamespace(stdout=json.dumps({'data':{'repository':{'pullRequest':{'id':'PR_example'}}}}).encode())
                with patch.dict(os.environ, GITHUB_EVENT_NAME='pull_request', GITHUB_REPOSITORY='c933103/AN-Paint', GITHUB_EVENT_PATH=str(event), GITHUB_OUTPUT=str(output), GITHUB_STEP_SUMMARY=str(summary)), patch('download_selected_artifacts.subprocess.run', return_value=response):
                    equivalence_main()
                self.assertEqual(json.loads(receipt.read_text())['review_metadata_api_access'], True)
                self.assertFalse(json.loads(receipt.read_text())['reused'])
            finally: os.chdir(old)

    def test_observed_input_mode_does_not_install_or_prepare_a_build(self):
        if not shutil.which('java'): self.skipTest('Java unavailable')
        checkout = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); package = root/'sdk/emulator/package.xml'
            package.parent.mkdir(parents=True)
            package.write_text('<repository><localPackage><revision><major>35</major></revision></localPackage></repository>')
            output = root/'observed.json'
            env = dict(os.environ, ANDROID_HOME=str(root/'sdk'), GITHUB_RUN_ID='1',
                       GITHUB_RUN_ATTEMPT='1', GITHUB_JOB='device', ImageOS='ubuntu22', ImageVersion='observed')
            env.pop('JAVA_HOME_17_X64', None)  # Build preparation would fail, observation must not install.
            subprocess.run(['bash', 'tools/ci_prepare_build.sh', '--record-inputs', str(output)],
                           cwd=checkout, env=env, check=True, timeout=30, capture_output=True)
            record = json.loads(output.read_text())
            self.assertEqual(record['sdk_packages']['emulator/package.xml']['revision'], {'major':'35'})
            self.assertEqual(record['sdk_packages']['emulator/package.xml']['sha256'], hashlib.sha256(package.read_bytes()).hexdigest())
            self.assertEqual(record['job'], 'device')
            self.assertTrue(record['java'])

    def test_exact_transport_stays_inside_original_composition_job_cap(self):
        workflow = (Path(__file__).resolve().parents[1] / '.github/workflows/android.yml').read_text()
        union = workflow.split('  device-union:', 1)[1]
        self.assertIn('timeout-minutes: 8', union)
        self.assertIn('timeout-minutes: 4', union)
        self.assertIn('download_selected_artifacts.py', union)
        self.assertNotIn('actions/download-artifact', union)
        self.assertIn('--core-root build/reports/android-api-${{ matrix.api }}', union)
        self.assertIn('--position-root build/reports/position-api-${{ matrix.api }}', union)
        self.assertIn('compose_device_reports.py compose', union)


if __name__ == '__main__':
    unittest.main()
