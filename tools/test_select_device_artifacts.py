"""Realistic duplicate-name/partial-rerun metadata; no Android execution claim."""
from pathlib import Path
import tempfile
import unittest

from select_device_artifacts import collection, select
from test_position_composition import ENV, SOURCE, fixture
from compose_device_reports import compose
import json

CHECKOUT, HEAD = 'a' * 40, 'b' * 40
ARGS = dict(run_id=123, attempt=2, checkout=CHECKOUT, head=HEAD, sdk=35)


def job(identity, group, attempt, start, end, result='success'):
    label = {'core': 'Core emulator API', 'position': 'Position dialog API'}[group]
    return dict(id=identity, name=f'{label} 35', run_id=123, head_sha=HEAD,
                run_attempt=attempt, status='completed', conclusion=result,
                started_at=f'2026-10-18T12:{start}:00Z', completed_at=f'2026-10-18T12:{end}:00Z')


def artifact(identity, group, minute):
    return dict(id=identity, name=f'emulator-{group}-api-35-{CHECKOUT}',
                workflow_run=dict(id=123, head_sha=HEAD), expired=False, digest='sha256:' + 'c' * 64,
                created_at=f'2026-10-18T12:{minute}:00Z', updated_at=f'2026-10-18T12:{minute}:00Z')


def metadata():
    # The later successful artifact has a LOWER ID than the old failed artifact.
    artifacts = [artifact(90, 'position', '19'), artifact(95, 'core', '20'), artifact(80, 'position', '29')]
    jobs = [job(1, 'core', 1, '10', '21'), job(2, 'position', 1, '10', '20', 'failure'),
            job(3, 'position', 2, '22', '30'), job(4, 'core', 2, '10', '21')]
    # GitHub carries successful unchanged jobs into attempt 2 with their original interval.
    return artifacts, jobs


class SelectDeviceArtifactsTest(unittest.TestCase):
    def test_reverse_ids_and_partial_reruns_select_actual_successful_intervals(self):
        artifacts, jobs = metadata()
        for a in (artifacts, list(reversed(artifacts))):
            for j in (jobs, list(reversed(jobs))):
                result = select(a, j, **ARGS)['selected']
                self.assertEqual(result['core']['artifact_id'], 95)
                self.assertEqual(result['position']['artifact_id'], 80)
                self.assertEqual(result['core']['job_record_run_attempt'], 2)
                self.assertEqual(result['core']['job_started_at'], '2026-10-18T12:10:00Z')

    def test_old_success_never_overrides_the_latest_failed_or_running_job(self):
        for status, conclusion in [('completed', 'failure'), ('in_progress', None), ('completed', 'cancelled')]:
            artifacts, jobs = metadata()
            jobs[1]['conclusion'] = 'success'
            jobs[2].update(status=status, conclusion=conclusion)
            with self.subTest(status=status, conclusion=conclusion), self.assertRaises(ValueError):
                select(artifacts, jobs, **ARGS)

    def test_ambiguous_job_or_artifacts_fail_instead_of_choosing_a_numeric_id(self):
        artifacts, jobs = metadata()
        for a, j in [(artifacts + [artifact(100, 'position', '28')], jobs),
                     (artifacts, jobs + [job(5, 'position', 2, '22', '30')])]:
            with self.assertRaises(ValueError):
                select(a, j, **ARGS)

    def test_expired_wrong_source_run_or_future_artifacts_are_rejected(self):
        mutations = [dict(expired=True), dict(expired='false'), dict(digest=''), dict(id=True),
                     dict(workflow_run=dict(id=999, head_sha=HEAD)),
                     dict(workflow_run=dict(id=123, head_sha='d' * 40)),
                     dict(name='emulator-position-api-35-' + 'd' * 40),
                     dict(created_at='2026-10-18T12:31:00Z', updated_at='2026-10-18T12:31:00Z'),
                     dict(updated_at='2026-10-18T12:28:00Z')]
        for mutation in mutations:
            artifacts, jobs = metadata(); artifacts[2].update(mutation)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                select(artifacts, jobs, **ARGS)

    def test_job_source_run_and_future_attempt_are_checked_before_selection(self):
        for mutation in [dict(head_sha='d' * 40), dict(run_id=999), dict(run_attempt=3),
                         dict(run_attempt=True), dict(completed_at='2026-10-18T12:21:00Z')]:
            artifacts, jobs = metadata(); jobs[2].update(mutation)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                select(artifacts, jobs, **ARGS)

    def test_wrong_sdk_missing_groups_and_invalid_identity_fail_closed(self):
        artifacts, jobs = metadata()
        for args in [dict(ARGS, sdk=30), dict(ARGS, attempt=0), dict(ARGS, checkout='not-a-sha'),
                     dict(ARGS, head='not-a-sha'), dict(ARGS, run_id=True)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                select(artifacts, jobs, **args)
        for a, j in [(artifacts[:1], jobs), (artifacts, jobs[:1])]:
            with self.assertRaises(ValueError):
                select(a, j, **ARGS)

    def test_pr_workflow_head_is_distinct_from_exact_checkout_in_artifact_name(self):
        artifacts, jobs = metadata()
        self.assertNotEqual(HEAD, CHECKOUT)
        receipt = select(artifacts, jobs, **ARGS)
        self.assertEqual(receipt['checkout'], CHECKOUT)
        self.assertEqual(receipt['workflow_head'], HEAD)
        with self.assertRaises(ValueError):
            select(artifacts, jobs, **dict(ARGS, head=CHECKOUT))

    def test_pagination_consumes_both_catalogues_and_preserves_query_parameters(self):
        artifacts, jobs = metadata(); calls = []
        def fetch(url):
            calls.append(url)
            key, rows = ('jobs', jobs) if '/jobs?' in url else ('artifacts', artifacts)
            page = int(url.rsplit('page=', 1)[1])
            return {'total_count': len(rows), key: rows[page - 1:page]}
        all_artifacts = collection(fetch, '/artifacts', 'artifacts')
        all_jobs = collection(fetch, '/jobs?filter=all', 'jobs')
        self.assertEqual(select(all_artifacts, all_jobs, **ARGS)['selected']['position']['artifact_id'], 80)
        self.assertEqual(len(calls), 7)
        self.assertIn('/jobs?filter=all&per_page=100&page=4', calls)

    def test_incomplete_changed_duplicate_or_unbounded_pagination_fails_closed(self):
        rows = [dict(id=1), dict(id=2)]
        cases = [
            [{'total_count': 2, 'jobs': rows[:1]}, {'total_count': 2, 'jobs': []}],
            [{'total_count': 2, 'jobs': rows[:1]}, {'total_count': 3, 'jobs': rows[1:]}],
            [{'total_count': 2, 'jobs': rows[:1]}, {'total_count': 2, 'jobs': rows[:1]}],
            [{'total_count': 1, 'jobs': rows}],
            [{'total_count': True, 'jobs': []}],
            [{'total_count': 21, 'jobs': [dict(id=n)]} for n in range(1, 21)],
        ]
        for pages in cases:
            queue = iter(pages)
            with self.subTest(pages=pages), self.assertRaises(ValueError):
                collection(lambda _: next(queue), '/jobs', 'jobs')

    def test_correct_selection_does_not_replace_the_unchanged_content_identity_gate(self):
        artifacts, jobs = metadata()
        self.assertEqual(select(artifacts, jobs, **ARGS)['selected']['position']['artifact_id'], 80)
        for attempt in ('2', '3'):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory); fixture(root, 35)
                path = root / 'position/device-identity.json'
                identity = json.loads(path.read_text()); identity['run_attempt'] = attempt
                path.write_text(json.dumps(identity))
                if attempt == '2':
                    result = compose(SOURCE, root / 'core', root / 'position', 35, dict(ENV, GITHUB_RUN_ATTEMPT='2'))
                    self.assertEqual(result['device_identity']['group_run_attempts'], {'core': 1, 'position': 2})
                else:
                    with self.assertRaises(ValueError):
                        compose(SOURCE, root / 'core', root / 'position', 35, dict(ENV, GITHUB_RUN_ATTEMPT='2'))

    def test_workflow_downloads_only_verified_ids_and_keeps_existing_caps_and_gate(self):
        workflow = (Path(__file__).resolve().parents[1] / '.github/workflows/android.yml').read_text()
        union = workflow.split('  device-union:', 1)[1]
        self.assertIn('timeout-minutes: 8', union)
        self.assertIn('actions: read', union)
        self.assertNotIn('actions: write', union)
        self.assertIn('select_device_artifacts.py --sdk ${{ matrix.api }}', union)
        self.assertEqual(union.count('artifact-ids: ${{ steps.artifacts.outputs.'), 2)
        self.assertNotIn('name: emulator-core-api-', union)
        self.assertNotIn('name: emulator-position-api-', union)
        self.assertIn('compose_device_reports.py compose --sdk ${{ matrix.api }}', union)
        self.assertIn('test "$CORE_RESULT" = success && test "$POSITION_RESULT" = success', union)


if __name__ == '__main__':
    unittest.main()
