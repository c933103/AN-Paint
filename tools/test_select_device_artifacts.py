"""Realistic duplicate-name/partial-rerun metadata; no Android execution claim."""
from pathlib import Path
import tempfile
import unittest

from select_device_artifacts import (collection, select, EQUIVALENT_JOBS, qualify_equivalent_run,
                                     verify_trusted_producers, verify_exact_head_review)
import copy
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


def equivalence_metadata():
    base, head, merged, tested, tree = (letter * 40 for letter in 'abcde')
    commit = lambda sha: dict(sha=sha, tree=dict(sha=tree), parents=[dict(sha=base), dict(sha=head)])
    repo = dict(id=10, full_name='c933103/AN-Paint')
    pr = dict(id=20, number=7, merged=True, state='closed', merge_commit_sha=merged,
              base=dict(ref='develop', repo=repo), head=dict(sha=head, ref='translation/example', repo=repo), labels=[],
              merged_at='2026-11-01T12:00:00Z')
    run = dict(id=30, run_attempt=1, event='pull_request', status='completed', conclusion='success',
               workflow_id=40, path='.github/workflows/android.yml', head_sha=head, head_branch='translation/example',
               repository=repo, head_repository=repo, pull_requests=[dict(id=20, number=7)],
               run_started_at='2026-11-01T10:00:00Z', updated_at='2026-11-01T11:00:00Z')
    jobs = [dict(id=i, name=name, run_id=30, head_sha=head, run_attempt=1,
                 status='completed', conclusion='success', started_at='2026-11-01T10:00:00Z',
                 completed_at='2026-11-01T11:00:00Z') for i, name in enumerate(sorted(EQUIVALENT_JOBS), 1)]
    return dict(repository=repo, merge=commit(merged), tested_merge=commit(tested),
                pull_requests=[pr], run=run, jobs=jobs, push_before=base,
                now='2026-11-01T12:30:00Z', workflow_id=40)


def review_metadata():
    head = 'b' * 40
    state = dict(code_review=dict(commit_sha=head, status='completed', has_any_findings=False,
                                 has_unresolved_findings=False),
                 security_review=dict(commit_sha=head, status='completed', has_any_findings=None,
                                      has_unresolved_findings=None))
    security = dict(headSha=head, repository='c933103/AN-Paint', pullRequestNumber=7,
                    status='completed', mergeGateEnabled=False)
    body = '<!-- codex-review-state:v1 ' + json.dumps(state) + ' -->\n' + \
           '<!-- codex-security-review:v1 ' + json.dumps(security) + ' -->'
    comment = dict(id=50, node_id='IC_example', body=body,
                   issue_url='https://api.github.com/repos/c933103/AN-Paint/issues/7',
                   user=dict(id=199175422, type='Bot', node_id='BOT_kgDOC98s_g'),
                   performed_via_github_app=dict(id=1144995),
                   created_at='2026-11-01T10:00:00Z', updated_at='2026-11-01T11:00:00Z')
    graphql = dict(id='IC_example', body=body, author=dict(__typename='Bot', id='BOT_kgDOC98s_g'),
                   editor=dict(__typename='Bot', id='BOT_kgDOC98s_g'), lastEditedAt='2026-11-01T11:00:00Z')
    return dict(head=head, pull_request=7, comment=comment, graphql=graphql,
                merged_at='2026-11-01T12:00:00Z')


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
        self.assertIn('download_selected_artifacts.py', union)
        self.assertNotIn('actions/download-artifact', union)
        self.assertNotIn('name: emulator-core-api-', union)
        self.assertNotIn('name: emulator-position-api-', union)
        self.assertIn('compose_device_reports.py compose --sdk ${{ matrix.api }}', union)
        self.assertIn('test "$CORE_RESULT" = success && test "$POSITION_RESULT" = success', union)

    def test_equivalence_metadata_retains_original_checkout_and_run_not_current_identity(self):
        data = equivalence_metadata(); result = qualify_equivalent_run(**data)
        self.assertEqual(result['checkout'], 'd' * 40)
        self.assertEqual(result['merge'], 'c' * 40)
        self.assertEqual(result['run_id'], 30)
        self.assertEqual(result['executed_jobs'], sorted(EQUIVALENT_JOBS))
        data['jobs'].append(dict(data['jobs'][0], id=8, name='Verify recent same-tree PR evidence'))
        self.assertEqual(qualify_equivalent_run(**data)['run_attempt'], 1)
        self.assertEqual(result['association_proof'], 'direct-run-pr')
        data['run']['pull_requests'] = []
        data['head_associations'] = copy.deepcopy(data['pull_requests'])
        data['merge_associations'] = copy.deepcopy(data['pull_requests'])
        self.assertEqual(qualify_equivalent_run(**data)['association_proof'], 'unique-head-and-merge-pr')
        for field in ('head_associations', 'merge_associations'):
            for mutate in (
                lambda d: d.update({field: []}),
                lambda d: d[field].append(copy.deepcopy(d[field][0])),
                lambda d: d[field][0].update(id=99),
                lambda d: d[field][0].update(number=99),
                lambda d: d[field][0]['head'].update(sha='f'*40),
                lambda d: d[field][0]['head'].update(ref='another-branch'),
                lambda d: d[field][0]['head'].update(repo=dict(id=99)),
                lambda d: d[field][0]['base'].update(ref='other'),
                lambda d: d[field][0]['base'].update(repo=dict(id=99)),
                lambda d: d['run'].update(head_branch='another-branch'),
                lambda d: d['run'].update(pull_requests=[dict(id=99, number=7)]),
                lambda d: d['run'].update(pull_requests=None),
                lambda d: d['tested_merge']['parents'][0].update(sha='f'*40),
            ):
                changed = copy.deepcopy(data); mutate(changed)
                with self.subTest(field=field, mutation=mutate), self.assertRaises(ValueError):
                    qualify_equivalent_run(**changed)

    def test_equivalence_rejects_wrong_repo_pr_merge_parents_tree_labels_or_workflow(self):
        mutations = [
            lambda d: d['repository'].update(full_name='other/repo'),
            lambda d: d['merge']['parents'].pop(),
            lambda d: d.update(push_before='f' * 40),
            lambda d: d['tested_merge']['tree'].update(sha='f' * 40),
            lambda d: d['tested_merge']['parents'].reverse(),
            lambda d: d['pull_requests'].append(copy.deepcopy(d['pull_requests'][0])),
            lambda d: d['pull_requests'][0].update(merged=False),
            lambda d: d['pull_requests'][0].update(merge_commit_sha='f' * 40),
            lambda d: d['pull_requests'][0]['base'].update(ref='other'),
            lambda d: d['pull_requests'][0]['head'].update(repo=dict(id=99)),
            lambda d: d['pull_requests'][0]['labels'].append(dict(name='ci:full-android')),
            lambda d: d['pull_requests'][0]['labels'].append(dict(name='ci:release-android')),
            lambda d: d['run'].update(workflow_id=99),
            lambda d: d['run'].update(path='other.yml'),
            lambda d: d['run'].update(head_sha='f' * 40),
            lambda d: d['run'].update(head_repository=dict(id=99)),
            lambda d: d['run'].update(pull_requests=[]),
        ]
        for mutate in mutations:
            data = equivalence_metadata(); mutate(data)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError): qualify_equivalent_run(**data)

    def test_equivalence_requires_direct_first_attempt_all_executed_jobs_and_freshness(self):
        mutations = [
            lambda d: d['run'].update(event='push'),
            lambda d: d['run'].update(run_attempt=2),
            lambda d: d['run'].update(run_attempt=True),
            lambda d: d['run'].update(conclusion='cancelled'),
            lambda d: d['jobs'].pop(),
            lambda d: d['jobs'].append(copy.deepcopy(d['jobs'][0])),
            lambda d: d['jobs'][0].update(name='Core emulator API 30'),
            lambda d: d['jobs'][0].update(conclusion='skipped'),
            lambda d: d['jobs'][0].update(status='in_progress'),
            lambda d: d['jobs'][0].update(run_attempt=2),
            lambda d: d['jobs'][0].update(run_id=31),
            lambda d: d['jobs'][0].update(started_at='2026-11-01T12:00:00Z'),
            lambda d: d.update(now='2026-11-01T13:00:01Z'),
            lambda d: d.update(now='2026-11-01T11:59:59Z'),
            lambda d: d['pull_requests'][0].update(merged_at='2026-11-02T11:00:01Z') or d.update(now='2026-11-02T11:30:00Z'),
        ]
        for mutate in mutations:
            data = equivalence_metadata(); mutate(data)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError): qualify_equivalent_run(**data)

    def test_equivalence_producer_maps_must_be_nonempty_and_identical(self):
        before = {'tools/select_device_artifacts.py': 'a' * 40}
        self.assertEqual(verify_trusted_producers(before, dict(before), dict(before)), before)
        for maps in [({}, {}, {}), (before, {}, before), (before, before, dict(before, extra='b'*40)),
                     ({'bad': 'not-a-blob'},) * 3]:
            with self.assertRaises(ValueError): verify_trusted_producers(*maps)

    def test_exact_head_review_requires_app_bot_and_same_node_editor_not_display_names(self):
        data = review_metadata(); self.assertEqual(verify_exact_head_review(**data)['head'], 'b' * 40)
        mutations = [
            lambda d: d['comment']['user'].update(id=1),
            lambda d: d['comment'].update(performed_via_github_app=dict(id=1)),
            lambda d: d['comment'].update(issue_url='https://api.github.com/repos/other/repo/issues/7'),
            lambda d: d['graphql'].update(id='other'),
            lambda d: d['graphql'].update(body='forged'),
            lambda d: d['graphql'].update(author=dict(__typename='User', id='BOT_kgDOC98s_g')),
            lambda d: d['graphql'].update(editor=dict(__typename='User', id='owner')),
            lambda d: d['graphql'].pop('editor'),
            lambda d: d['graphql'].update(lastEditedAt=None, editor=None),
            lambda d: d['graphql'].update(lastEditedAt='2026-11-01T10:30:00Z'),
            lambda d: d['comment'].update(updated_at='2026-11-01T12:00:01Z'),
        ]
        for mutate in mutations:
            data = review_metadata(); mutate(data)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError): verify_exact_head_review(**data)
        data = review_metadata(); data['comment']['updated_at'] = data['comment']['created_at']
        data['graphql'].update(lastEditedAt=None, editor=None)
        verify_exact_head_review(**data)

    def test_review_stale_security_findings_enabled_gate_and_duplicate_markers_fail_closed(self):
        changes = [
            ('"has_any_findings": false', '"has_any_findings": true'),
            ('"has_unresolved_findings": false', '"has_unresolved_findings": null'),
            ('"status": "completed"', '"status": "running"'),
            ('"headSha": "' + 'b'*40, '"headSha": "' + 'f'*40),
            ('"mergeGateEnabled": false', '"mergeGateEnabled": true'),
            ('"pullRequestNumber": 7', '"pullRequestNumber": 8'),
            ('"repository": "c933103/AN-Paint"', '"repository": "other/repo"'),
        ]
        for old, new in changes:
            data = review_metadata(); body = data['comment']['body'].replace(old, new)
            data['comment']['body'] = data['graphql']['body'] = body
            with self.subTest(change=new), self.assertRaises(ValueError): verify_exact_head_review(**data)
        for suffix in ('\n' + review_metadata()['comment']['body'],
                       '\n<!-- codex-review-state:v1 malformed -->', ''):
            data = review_metadata()
            body = data['comment']['body'] + suffix if suffix else data['comment']['body'].replace('"code_review":', '"code_review":{},"code_review":')
            data['comment']['body'] = data['graphql']['body'] = body
            with self.assertRaises(ValueError): verify_exact_head_review(**data)


if __name__ == '__main__':
    unittest.main()
