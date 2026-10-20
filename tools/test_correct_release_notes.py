"""Behavior tests for the body-only, identity-guarded release correction."""
import copy
import json
from pathlib import Path
import subprocess
import unittest

from correct_release_notes import ASSET_FIELDS, RELEASE_FIELDS, asset_identity, correct, digest

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / 'verification/releases/0.0.39-notes-correction.json'


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self.request = json.loads(REQUEST.read_text())
        self.notes = REQUEST.with_name(self.request['notes_file']).read_text()
        self.old = 'Previous release notes\n'
        self.request['previous_body_sha256'] = digest(self.old)
        self.release = {**self.request['release'], 'body': self.old}
        self.assets = copy.deepcopy(self.request['assets'])
        self.tag = self.request['release']['target_commitish']
        self.calls = []
        self.fail = None

    def api(self, path):
        if '/git/matching-refs/tags/' in path:
            return [{'ref': 'refs/tags/v0.0.39', 'object': {'type': 'commit', 'sha': self.tag}}]
        if '/assets?' in path:
            return copy.deepcopy(self.assets)
        if path.endswith('/releases/418125792'):
            return copy.deepcopy(self.release)
        self.fail_test(path)

    def fail_test(self, path):
        raise AssertionError('Unexpected request: ' + path)

    def patch(self, path, data):
        self.calls.append((path, copy.deepcopy(data)))
        if self.fail == 'before':
            raise subprocess.CalledProcessError(1, 'gh')
        self.release.update(data)
        if self.fail == 'after':
            raise subprocess.CalledProcessError(1, 'gh')
        if self.fail == 'asset':
            self.assets[0]['digest'] = 'sha256:' + '0' * 64
        if self.fail == 'tag':
            self.tag = '0' * 40
        if self.fail == 'title':
            self.release['name'] = 'Different title'
        if self.fail == 'no-op':
            self.release['body'] = self.old

    def invoke(self, repo=None):
        return correct(self.api, self.patch, self.request, self.notes,
                       repo or self.request['repository'])

    def test_payload_changes_body_only_and_rerun_is_read_only(self):
        self.assertEqual(self.invoke()['status'], 'corrected')
        self.assertEqual(self.calls, [('repos/c933103/AN-Paint/releases/418125792', {'body': self.notes})])
        self.assertEqual(self.invoke()['status'], 'already_corrected')
        self.assertEqual(len(self.calls), 1)

    def test_reconciles_uncertain_success_without_retry(self):
        self.fail = 'after'
        self.assertEqual(self.invoke()['status'], 'corrected')
        self.assertEqual(len(self.calls), 1)

    def test_does_not_retry_uncertain_failure(self):
        self.fail = 'before'
        with self.assertRaises(subprocess.CalledProcessError):
            self.invoke()
        self.assertEqual(len(self.calls), 1)

    def test_unknown_existing_body_rejected_before_write(self):
        self.release['body'] += '\nAnother edit'
        with self.assertRaisesRegex(ValueError, 'body changed'):
            self.invoke()
        self.assertEqual(self.calls, [])

    def test_invalid_new_body_rejected_before_write(self):
        self.notes += 'unexpected'
        with self.assertRaisesRegex(ValueError, 'reviewed content'):
            self.invoke()
        self.assertEqual(self.calls, [])

    def test_wrong_repository_rejected_before_reads_or_writes(self):
        self.api = lambda path: self.fail_test(path)
        with self.assertRaisesRegex(ValueError, 'repository mismatch'):
            self.invoke('another/repository')
        self.assertEqual(self.calls, [])

    def test_changed_release_identity_rejected_before_write(self):
        for field in RELEASE_FIELDS:
            with self.subTest(field=field):
                original = self.release[field]
                self.release[field] = 'changed'
                with self.assertRaisesRegex(ValueError, 'identity changed'):
                    self.invoke()
                self.release[field] = original
        self.assertEqual(self.calls, [])

    def test_changed_asset_identity_rejected_before_write(self):
        for field in ASSET_FIELDS:
            with self.subTest(field=field):
                original = self.assets[0][field]
                self.assets[0][field] = 'changed'
                with self.assertRaises(ValueError):
                    self.invoke()
                self.assets[0][field] = original
        self.assertEqual(self.calls, [])

    def test_missing_unexpected_and_duplicate_assets_rejected(self):
        original = copy.deepcopy(self.assets)
        for assets in (original[:-1], original + [original[0]], original + [{**original[0], 'name': 'extra'}]):
            with self.subTest(assets=len(assets)):
                self.assets = assets
                with self.assertRaises(ValueError):
                    self.invoke()
        self.assertEqual(self.calls, [])

    def test_changed_tag_rejected_before_write(self):
        self.tag = '0' * 40
        with self.assertRaisesRegex(ValueError, 'tag object changed'):
            self.invoke()
        self.assertEqual(self.calls, [])

    def test_post_mutation_identity_or_body_change_never_reports_success(self):
        for failure in ('asset', 'tag', 'title', 'no-op'):
            with self.subTest(failure=failure):
                self.setUp()
                self.fail = failure
                with self.assertRaises(ValueError):
                    self.invoke()
                self.assertEqual(len(self.calls), 1)

    def test_manifest_binds_corrected_notes_and_sorted_assets(self):
        self.assertEqual(digest(self.old), self.request['previous_body_sha256'])
        self.assertEqual(digest(self.notes), self.request['corrected_body_sha256'])
        self.assertEqual(asset_identity(self.assets), self.assets)


if __name__ == '__main__':
    unittest.main()
