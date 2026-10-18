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
