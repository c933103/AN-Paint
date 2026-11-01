#!/usr/bin/env python3
"""Select exact artifact IDs from successful job intervals, never name/ID order."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import time
from urllib.request import HTTPRedirectHandler, Request, build_opener

GROUP_JOBS = {'core': 'Core emulator API', 'position': 'Position dialog API'}


def positive(value):
    if type(value) is not int or value <= 0:
        raise ValueError('Positive integer identity required')
    return value


def timestamp(value):
    if not isinstance(value, str) or not value.endswith('Z'):
        raise ValueError('UTC timestamp required')
    parsed = datetime.fromisoformat(value[:-1] + '+00:00')
    if parsed.tzinfo != timezone.utc:
        raise ValueError('UTC timestamp required')
    return parsed


def select(artifacts, jobs, *, run_id, attempt, checkout, head, sdk):
    positive(run_id); positive(attempt)
    if sdk not in (30, 35) or any(not re.fullmatch(r'[0-9a-f]{40}', sha) for sha in (checkout, head)):
        raise ValueError('Exact checkout/head and supported SDK required')
    selected = {}
    for group, label in GROUP_JOBS.items():
        matching = [job for job in jobs if job.get('name') == f'{label} {sdk}']
        if not matching:
            raise ValueError(f'Missing {group} job')
        for job in matching:
            positive(job.get('id')); positive(job.get('run_attempt'))
            if (job.get('run_id') != run_id or job.get('head_sha') != head
                    or job['run_attempt'] > attempt):
                raise ValueError(f'Wrong run/head or future {group} job attempt')
        latest = max(job['run_attempt'] for job in matching)
        current = [job for job in matching if job['run_attempt'] == latest]
        if len(current) != 1:
            raise ValueError(f'Ambiguous latest {group} job')
        job = current[0]
        if job.get('status') != 'completed' or job.get('conclusion') != 'success':
            raise ValueError(f'Latest {group} job did not succeed')
        start, end = timestamp(job['started_at']), timestamp(job['completed_at'])
        if end < start:
            raise ValueError('Inverted job interval')
        name = f'emulator-{group}-api-{sdk}-{checkout}'
        candidates = []
        for artifact in artifacts:
            if artifact.get('name') != name:
                continue
            workflow = artifact.get('workflow_run', {})
            if workflow.get('id') != run_id or workflow.get('head_sha') != head:
                raise ValueError(f'Wrong run/head for {group} artifact')
            created, updated = timestamp(artifact['created_at']), timestamp(artifact['updated_at'])
            if updated < created:
                raise ValueError('Inverted artifact interval')
            if start <= created <= updated <= end:
                candidates.append(artifact)
        if len(candidates) != 1:
            raise ValueError(f'Expected exactly one {group} artifact in successful job interval')
        artifact = candidates[0]
        positive(artifact.get('id'))
        if artifact.get('expired') is not False or not re.fullmatch(r'sha256:[0-9a-f]{64}', artifact.get('digest', '')):
            raise ValueError('Nonexpired artifact with SHA-256 digest required')
        selected[group] = dict(artifact_id=artifact['id'], name=name, digest=artifact['digest'],
            created_at=artifact['created_at'], updated_at=artifact['updated_at'],
            job_id=job['id'], job_record_run_attempt=job['run_attempt'],
            job_started_at=job['started_at'], job_completed_at=job['completed_at'])
    return dict(run_id=run_id, current_attempt=attempt, checkout=checkout, workflow_head=head,
                device_sdk=sdk, selected=selected)


# This qualifies independently fetched metadata, not the contents of an uploaded
# equivalence receipt. The caller still verifies original artifact bytes/reports.
EQUIVALENT_JOBS = frozenset((
    'Regression tests and lint', 'Exact-script resource generation',
    'Build APK and corresponding source', 'Core emulator API 35',
    'Position dialog API 35', 'Emulator API 35',
))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def commit_identity(commit):
    sha, tree = commit.get('sha'), commit.get('tree', {}).get('sha')
    parents = [parent.get('sha') for parent in commit.get('parents', [])]
    require(all(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{40}', value)
                for value in (sha, tree, *parents)), 'Exact Git commit/tree/parent identities required')
    return sha, tree, parents


def verify_trusted_producers(before, tested, current):
    """Caller constructs COMPLETE producer path/blob maps from Git trees."""
    require(isinstance(before, dict) and bool(before), 'Trusted producer map is missing')
    require(before == tested == current, 'Executable evidence producers changed')
    require(all(isinstance(path, str) and path and isinstance(blob, str)
                and re.fullmatch(r'[0-9a-f]{40}', blob) for path, blob in before.items()),
            'Invalid producer blob identity')
    # Returning the map does not certify the caller omitted no executable paths.
    return dict(before)


def qualify_equivalent_run(*, repository, merge, tested_merge, pull_requests,
                           run, jobs, push_before, now, workflow_id):
    """Narrow ordinary-merge policy; unsupported or missing facts fail closed.

    Inputs are GitHub REST repository/PR/run/job and Git commit objects. Job
    success is necessary, never sufficient: artifact/content and review checks
    are separate mandatory caller steps. No current-run identity is fabricated.
    """
    repo_id = positive(repository.get('id'))
    require(repository.get('full_name') == 'c933103/AN-Paint', 'Wrong repository')
    merged_sha, tree, parents = commit_identity(merge)
    tested_sha, tested_tree, tested_parents = commit_identity(tested_merge)
    require(len(parents) == 2 and parents[0] == push_before,
            'Only immediate ordinary two-parent merges qualify')
    base, head = parents
    require(tested_parents == parents and tested_tree == tree,
            'Tested merge parents/tree differ from actual merge')
    require(len(pull_requests) == 1, 'Unique associated merged PR required')
    pr = pull_requests[0]
    positive(pr.get('id')); number = positive(pr.get('number'))
    require(pr.get('merged') is True and pr.get('state') == 'closed'
            and pr.get('merge_commit_sha') == merged_sha,
            'PR is not the actual merged change')
    require(pr.get('base', {}).get('ref') == 'develop'
            and pr.get('head', {}).get('sha') == head
            and pr.get('base', {}).get('repo', {}).get('id') == repo_id
            and pr.get('head', {}).get('repo', {}).get('id') == repo_id,
            'PR base/head/repository association differs')
    labels = pr.get('labels')
    require(isinstance(labels, list) and all(isinstance(label, dict) and isinstance(label.get('name'), str)
                                           for label in labels), 'PR label policy missing')
    require(not {'ci:release-android', 'ci:full-android'} & {label['name'] for label in labels},
            'Release/full-matrix changes must execute normally')
    merged_at, checked_at = timestamp(pr.get('merged_at')), timestamp(now)
    require(0 <= (checked_at - merged_at).total_seconds() <= 3600,
            'Immediate-merge verification window expired or future dated')
    run_id = positive(run.get('id')); positive(workflow_id)
    require(run.get('run_attempt') == 1 and type(run.get('run_attempt')) is int
            and run.get('event') == 'pull_request'
            and run.get('status') == 'completed' and run.get('conclusion') == 'success',
            'Only directly executed successful first-attempt PR runs qualify')
    require(run.get('workflow_id') == workflow_id
            and run.get('path') == '.github/workflows/android.yml'
            and run.get('head_sha') == head
            and run.get('repository', {}).get('id') == repo_id
            and run.get('head_repository', {}).get('id') == repo_id,
            'Run workflow/head/repository association differs')
    associated = run.get('pull_requests')
    require(isinstance(associated, list) and len(associated) == 1
            and associated[0].get('number') == number and associated[0].get('id') == pr['id'],
            'Run does not independently identify this PR')
    require(isinstance(jobs, list) and len({job.get('id') for job in jobs}) == len(jobs),
            'Missing or duplicate job identities')
    names = [job.get('name') for job in jobs]
    require(len(names) == len(set(names)) and EQUIVALENT_JOBS <= set(names)
            and set(names) <= EQUIVALENT_JOBS | {'Verify recent same-tree PR evidence'},
            'Required executed job inventory differs')
    completions = []
    for job in jobs:
        positive(job.get('id'))
        require(job.get('run_id') == run_id and job.get('head_sha') == head
                and type(job.get('run_attempt')) is int and job['run_attempt'] == 1,
                'Job run/head/attempt differs')
        require(job.get('status') == 'completed' and job.get('conclusion') == 'success',
                'Job was not successfully executed')
        start, end = timestamp(job.get('started_at')), timestamp(job.get('completed_at'))
        require(start <= end <= merged_at, 'Job interval is inverted or after merge')
        completions.append(end)
    completed_at = max(completions)
    require(0 <= (merged_at - completed_at).total_seconds() <= 24 * 3600,
            'Prior execution freshness expired')
    require(timestamp(run.get('run_started_at')) <= completed_at
            <= timestamp(run.get('updated_at')) <= merged_at, 'Run time association differs')
    return dict(repository_id=repo_id, merge=merged_sha, base=base, head=head,
                checkout=tested_sha, tree=tree, pull_request=number,
                run_id=run_id, run_attempt=1, build_variant='debug', device_sdk=35,
                executed_jobs=sorted(EQUIVALENT_JOBS),
                prior_completed_at=completed_at.isoformat().replace('+00:00', 'Z'),
                merged_at=pr['merged_at'], checked_at=now,
                policy='immediate-merge-prior-environment-v1')


def verify_exact_head_review(*, head, pull_request, comment, graphql, merged_at):
    """Bind an exact-head clean marker to its REST app/bot and GraphQL editor.

    Caller fetches the unique current summary independently and repeats the
    identity/body fetch before accepting reuse. No display-name or comment-text
    assertion can substitute for those GitHub actor identities.
    """
    require(isinstance(head, str) and re.fullmatch(r'[0-9a-f]{40}', head), 'Exact review head required')
    positive(pull_request); positive(comment.get('id'))
    bot = 'BOT_kgDOC98s_g'
    user = comment.get('user', {})
    require(user.get('id') == 199175422 and user.get('type') == 'Bot'
            and user.get('node_id') == bot
            and comment.get('performed_via_github_app', {}).get('id') == 1144995,
            'Review is not from the trusted app AND bot')
    require(comment.get('issue_url') == f'https://api.github.com/repos/c933103/AN-Paint/issues/{pull_request}',
            'Review belongs to another PR')
    body = comment.get('body')
    require(isinstance(body, str) and len(body) <= 65536
            and graphql.get('id') == comment.get('node_id')
            and isinstance(comment.get('node_id'), str)
            and graphql.get('body') == body
            and graphql.get('author') == {'__typename': 'Bot', 'id': bot},
            'REST/GraphQL review identity, body or author differs')
    require('lastEditedAt' in graphql and 'editor' in graphql, 'Review edit provenance missing')
    created, updated = timestamp(comment.get('created_at')), timestamp(comment.get('updated_at'))
    require(created <= updated <= timestamp(merged_at), 'Review was changed after merge or has invalid times')
    if graphql['lastEditedAt'] is None:
        require(graphql['editor'] is None and created == updated, 'Unedited review provenance is ambiguous')
    else:
        edited = timestamp(graphql['lastEditedAt'])
        require(graphql['editor'] == {'__typename': 'Bot', 'id': bot}
                and created <= edited <= timestamp(merged_at)
                and abs((edited - updated).total_seconds()) < 1,
                'Review last edit is not bound to the same bot/time')

    def marker(name):
        matches = re.findall(r'<!-- ' + re.escape(name) + r' (\{.*?\})\s*-->', body, re.S)
        require(len(matches) == 1 and body.count('<!-- ' + name) == 1,
                'Unique completed review markers required')
        def unique(pairs):
            result = {}
            for key, value in pairs:
                require(key not in result, 'Duplicate review JSON field')
                result[key] = value
            return result
        value = json.loads(matches[0], object_pairs_hook=unique)
        require(isinstance(value, dict), 'Review marker must be an object')
        return value
    review, security = marker('codex-review-state:v1'), marker('codex-security-review:v1')
    code, state = review.get('code_review', {}), review.get('security_review', {})
    require(isinstance(code, dict) and isinstance(state, dict), 'Review states must be objects')
    require(code.get('commit_sha') == head and code.get('status') == 'completed'
            and code.get('has_any_findings') is False and code.get('has_unresolved_findings') is False,
            'Code review is stale, incomplete or has findings')
    require(state.get('commit_sha') == head and state.get('status') == 'completed'
            and security.get('headSha') == head and security.get('status') == 'completed'
            and security.get('repository') == 'c933103/AN-Paint'
            and type(security.get('pullRequestNumber')) is int
            and security['pullRequestNumber'] == pull_request
            and security.get('mergeGateEnabled') is False,
            'Security review is stale, incomplete or requires unsupported gate evaluation')
    return dict(comment_id=comment['id'], node_id=comment['node_id'], head=head,
                updated_at=comment['updated_at'], app_id=1144995, bot_id=199175422,
                security_gate_enabled=False)


def collection(fetch, endpoint, key):
    """Read every page; missing, changing or duplicate records fail closed."""
    result, seen, total = [], set(), None
    for page in range(1, 21):
        separator = '&' if '?' in endpoint else '?'
        data = fetch(f'{endpoint}{separator}per_page=100&page={page}')
        count, rows = data.get('total_count'), data.get(key)
        if type(count) is not int or count < 0 or not isinstance(rows, list):
            raise ValueError('Invalid paginated collection')
        if total is not None and count != total:
            raise ValueError('Collection changed during pagination')
        total = count
        for row in rows:
            identity = positive(row.get('id'))
            if identity in seen:
                raise ValueError('Duplicate paginated identity')
            seen.add(identity); result.append(row)
        if len(result) == total:
            return result
        if not rows or len(result) > total:
            raise ValueError('Incomplete or inconsistent collection')
    raise ValueError('Collection exceeds bounded pagination')


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk', type=int, choices=(30, 35), required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    args.receipt.unlink(missing_ok=True)
    repo = os.environ['GITHUB_REPOSITORY']
    if (not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo)
            or os.environ.get('GITHUB_API_URL', 'https://api.github.com') != 'https://api.github.com'):
        raise ValueError('Expected public GitHub API and repository identity')
    run, attempt = int(os.environ['GITHUB_RUN_ID']), int(os.environ['GITHUB_RUN_ATTEMPT'])
    positive(run); positive(attempt)
    checkout = os.environ['GITHUB_SHA']
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    head = event['pull_request']['head']['sha'] if os.environ['GITHUB_EVENT_NAME'] == 'pull_request' else checkout
    deadline = time.monotonic() + 45
    opener = build_opener(NoRedirect())

    def fetch(endpoint):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ValueError('Artifact selection exceeded its request budget')
        request = Request('https://api.github.com' + endpoint, headers={
            'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': 'Bearer ' + os.environ['GH_TOKEN']})
        with opener.open(request, timeout=min(10, remaining)) as response:
            data = response.read(4 * 1024 * 1024 + 1)
        if len(data) > 4 * 1024 * 1024:
            raise ValueError('Oversized Actions metadata response')
        return json.loads(data)

    root = f'/repos/{repo}/actions/runs/{run}'
    artifacts = collection(fetch, root + '/artifacts', 'artifacts')
    jobs = collection(fetch, root + '/jobs?filter=all', 'jobs')
    receipt = select(artifacts, jobs, run_id=run, attempt=attempt, checkout=checkout, head=head, sdk=args.sdk)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    # IDs are validated integers; no external string reaches the Actions output protocol.
    with Path(os.environ['GITHUB_OUTPUT']).open('a') as output:
        for group, value in receipt['selected'].items():
            output.write(f"{group}={value['artifact_id']}\n")
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
