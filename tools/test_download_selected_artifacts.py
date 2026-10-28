"""Exercise exact-ID transport and hash-before-extract, without network access."""
import hashlib
import io
import os
from pathlib import Path
import stat
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from download_selected_artifacts import download, extract
from select_device_artifacts import select
from test_select_device_artifacts import ARGS, metadata


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
