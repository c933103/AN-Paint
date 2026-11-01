#!/usr/bin/env python3
"""Download the exact selected REST IDs without name-based SDK filtering."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import zipfile

from select_device_artifacts import positive

MAX_ARCHIVE = 128 * 1024 * 1024
MAX_EXPANDED = 512 * 1024 * 1024


def extract(archive, root):
    """Validate the whole archive before extraction; never overwrite evidence."""
    with zipfile.ZipFile(archive) as bundle:
        members = bundle.infolist()
        if not members or len(members) > 10000 or sum(m.file_size for m in members) > MAX_EXPANDED:
            raise ValueError('Archive exceeds bounded report inventory')
        seen = set()
        for member in members:
            path = PurePosixPath(member.filename)
            mode = member.external_attr >> 16
            if (not member.filename or path.is_absolute() or '..' in path.parts
                    or '\\' in member.filename or path.as_posix() in seen
                    or stat.S_ISLNK(mode) or member.flag_bits & 1
                    or member.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)):
                raise ValueError('Unsafe or unsupported archive member')
            seen.add(path.as_posix())
            target = root.joinpath(*path.parts)
            if target.exists() or target.is_symlink():
                raise ValueError('Artifact would overwrite existing evidence')
        root.mkdir(parents=True, exist_ok=True)
        bundle.extractall(root)


def download(repo, artifact, root, runner=subprocess.run, *, kind="reports"):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository')
    # Only the existing universal APK/source bundle exceeds the report bound.
    if kind not in ('reports', 'apk-source') or (kind == 'apk-source' and not
            re.fullmatch(r'apk-and-source-[0-9a-f]{40}', artifact.get('name', ''))):
        raise ValueError('Explicit bounded artifact type required')
    limit = 256 * 1024 * 1024 if kind == 'apk-source' else MAX_ARCHIVE
    identity = positive(artifact.get('artifact_id'))
    digest = artifact.get('digest', '')
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', digest):
        raise ValueError('Selected SHA-256 digest required')
    # gh follows the REST archive redirect without re-listing or selecting by name.
    # Existing ephemeral GH_TOKEN is consumed by gh, never printed or passed as an argument.
    env = dict(os.environ); env.pop('GH_DEBUG', None)
    with tempfile.TemporaryDirectory() as directory:
        archive = Path(directory) / 'artifact.zip'
        with archive.open('wb') as output:
            result = runner(['gh', 'api', '--hostname', 'github.com', '--method', 'GET',
                f'/repos/{repo}/actions/artifacts/{identity}/zip'],
                stdout=output, stderr=subprocess.PIPE, timeout=90, env=env, check=False)
        if result.returncode:
            raise ValueError(f'Exact artifact {identity} download failed (exit {result.returncode})')
        if not 0 < archive.stat().st_size <= limit:
            raise ValueError('Archive exceeds compressed report bound')
        with archive.open('rb') as stream:
            checksum = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                checksum.update(chunk)
            actual = checksum.hexdigest()
        if digest != 'sha256:' + actual:
            raise ValueError('Downloaded artifact SHA-256 mismatch')
        extract(archive, root)


def preflight(fetch, graphql, checkout, event, environ, root, now):
    """Independently qualify prior evidence; exceptions always mean normal execution."""
    from select_device_artifacts import (collection, qualify_equivalent_run, require,
        timestamp, verify_exact_head_review, verify_trusted_producers)
    from compose_device_reports import verify_reuse_artifacts
    import time
    from datetime import timedelta
    began = time.monotonic()
    repo = environ['GITHUB_REPOSITORY']
    require(repo == 'c933103/AN-Paint' and environ['GITHUB_EVENT_NAME'] == 'push'
            and environ['GITHUB_REF'] == 'refs/heads/develop'
            and environ['BUILD_VARIANT'] == 'debug' and environ['GITHUB_RUN_ATTEMPT'] == '1',
            'Only first-attempt ordinary develop pushes may reuse evidence')
    prefix = '/repos/' + repo
    merge_sha = environ['GITHUB_SHA']
    require(subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'],
            text=True).strip() == merge_sha, 'Checkout differs from actual push')
    repository = fetch(prefix)
    def policy():
        branch = fetch(prefix + '/branches/develop')
        rules = fetch(prefix + '/rulesets?includes_parents=true&per_page=100')
        require(branch.get('protected') is False
                and branch.get('protection', {}).get('enabled') is False
                and branch['protection']['required_status_checks'].get('contexts') == []
                and branch['protection']['required_status_checks'].get('checks') == []
                and rules == [], 'Additional or unavailable required policy: full execution required')
        return dict(protected=False, inherited_rulesets=[])
    original_policy = policy()
    merge = fetch(prefix + '/git/commits/' + merge_sha)
    require(len(merge['parents']) == 2 and merge['parents'][0]['sha'] == event['before'],
            'Not an immediate two-parent merge')
    base, head = [p['sha'] for p in merge['parents']]

    def producers(tree):
        data = fetch(prefix + '/git/trees/' + tree + '?recursive=1')
        require(data.get('truncated') is False, 'Incomplete Git tree')
        rows = [x for x in data['tree'] if x['type'] != 'tree']
        require(rows and all(x['type'] == 'blob' and x['mode'] in ('100644', '100755') for x in rows),
                'Unsupported tracked input mode')
        # Narrow initial policy, not an open-ended executable-script inventory.
        # Only existing canonical translation strings.xml bytes may change.
        immutable = {x['path']: x['sha'] for x in rows if not re.fullmatch(
            r'Paintroid/src/main/res/values(?:-[A-Za-z0-9+]+)?/strings[.]xml', x['path'])}
        return immutable, {x['path']: x['mode'] for x in rows}

    before = producers(fetch(prefix + '/git/commits/' + base)['tree']['sha'])
    current = producers(merge['tree']['sha'])
    require(before[1] == current[1], 'Tracked paths or modes changed')
    verify_trusted_producers(before[0], current[0], current[0])
    # This check is early: the introducing policy merge always takes full fallback.
    associations = fetch(prefix + '/commits/' + merge_sha + '/pulls?per_page=100')
    require(isinstance(associations, list) and len(associations) == 1,
            'Ambiguous associated PR')
    pr = fetch(prefix + '/pulls/' + str(associations[0]['number']))
    workflow = fetch(prefix + '/actions/workflows/android.yml')
    runs = collection(fetch, prefix + '/actions/workflows/android.yml/runs?event=pull_request&head_sha='
                      + head, 'workflow_runs')
    require(len(runs) == 1, 'Ambiguous or superseded prior run')
    run = fetch(prefix + '/actions/runs/' + str(runs[0]['id']))
    run_path = prefix + '/actions/runs/' + str(run['id'])
    jobs = collection(fetch, run_path + '/jobs?filter=all', 'jobs')
    artifacts = collection(fetch, run_path + '/artifacts', 'artifacts')
    builds = [a for a in artifacts if re.fullmatch(r'apk-and-source-[0-9a-f]{40}', a['name'])]
    require(len(builds) == 1, 'Ambiguous original checkout artifact')
    original = builds[0]['name'].removeprefix('apk-and-source-')
    tested = fetch(prefix + '/git/commits/' + original)
    qualified = qualify_equivalent_run(repository=repository, merge=merge, tested_merge=tested,
        pull_requests=[pr], run=run, jobs=jobs, push_before=event['before'], now=now,
        workflow_id=workflow['id'])
    # Bounded list read: a full page is conservatively ambiguous, never truncated acceptance.
    comments = fetch(prefix + '/issues/' + str(pr['number']) + '/comments?per_page=100')
    require(isinstance(comments, list) and len(comments) < 100, 'Review inventory exceeds bound')
    summaries = [c for c in comments if 'codex-review-state:v1' in c.get('body', '')]
    require(len(summaries) == 1, 'Unique current review summary missing')
    comment = summaries[0]
    editor = graphql(comment['node_id'])
    review = verify_exact_head_review(head=head, pull_request=pr['number'], comment=comment,
        graphql=editor, merged_at=pr['merged_at'])
    groups = {
        'build': ('Build APK and corresponding source', 'apk-and-source-'),
        'tests': ('Build APK and corresponding source', 'instrumentation-apks-'),
        'regression': ('Regression tests and lint', 'regression-and-lint-'),
        'exact': ('Exact-script resource generation', 'exact-script-generation-'),
        'core': ('Core emulator API 35', 'emulator-core-api-35-'),
        'position': ('Position dialog API 35', 'emulator-position-api-35-'),
    }
    selected = {}
    for group, (job_name, stem) in groups.items():
        job = next(j for j in jobs if j['name'] == job_name)
        candidates = [a for a in artifacts if a['name'] == stem + original]
        require(len(candidates) == 1, 'Ambiguous original ' + group + ' artifact')
        artifact = candidates[0]
        require(artifact.get('expired') is False
                and artifact['workflow_run']['id'] == run['id']
                and artifact['workflow_run']['head_sha'] == head
                and timestamp(job['started_at']) <= timestamp(artifact['created_at'])
                <= timestamp(artifact['updated_at']) <= timestamp(job['completed_at']),
                'Artifact is not from its successful job interval')
        selected[group] = dict(artifact_id=artifact['id'], name=artifact['name'], digest=artifact['digest'])
        download(repo, selected[group], root/group,
                 kind='apk-source' if group == 'build' else 'reports')
    test_apk = Path('app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk')
    target = root/'build'/test_apk
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists(): raise ValueError('Unexpected duplicate test APK')
    import shutil
    shutil.copyfile(root/'tests'/test_apk, target)
    original_env = dict(GITHUB_SHA=original, GITHUB_RUN_ID=str(run['id']),
                        GITHUB_RUN_ATTEMPT='1', BUILD_VARIANT='debug')
    evidence = verify_reuse_artifacts(checkout, root/'build', root/'core', root/'position', original_env)
    observed = {}
    expected_jobs = dict(build='build', regression='checks', exact='exact-script-resources',
                         core='device', position='position')
    for group, relative in {'build': 'build/delivery/observed-inputs.json',
            'regression': 'build/reports/ci-phases/observed-inputs.json',
            'exact': 'observed-inputs.json', 'core': 'observed-inputs.json',
            'position': 'observed-inputs.json'}.items():
        value = json.loads((root/group/relative).read_text())
        require(value['commit'] == original and value['tree'] == qualified['tree']
                and value['run_id'] == str(run['id']) and value['attempt'] == '1'
                and value['image_os'] and value['image_version'] and value['java']
                and value['sdk_packages'] and value['job'] == expected_jobs[group]
                and value['gradle_wrapper_properties_sha256'] == hashlib.sha256(
                    (checkout/'gradle/wrapper/gradle-wrapper.properties').read_bytes()).hexdigest(),
                'Missing original environment provenance')
        required_packages = {'emulator/package.xml', 'system-images/android-35/google_apis/x86_64/package.xml'} if group in ('core', 'position') else {
            'platforms/android-35/package.xml', 'build-tools/35.0.0/package.xml',
            'ndk/27.2.12479018/package.xml', 'cmake/3.22.1/package.xml'}
        require(required_packages <= value['sdk_packages'].keys(), 'Missing observed SDK inputs')
        require(all(re.fullmatch(r'[0-9a-f]{64}', p['sha256']) and p['revision']
                    for p in value['sdk_packages'].values()), 'Invalid observed package identity')
        if group in ('build', 'regression'):
            require(value.get('native_revision_inputs'), 'Missing prior native revision inputs')
        if group in ('build', 'regression', 'exact'):
            require(value['runtime_dependencies'] and all(d['files'] for d in value['runtime_dependencies']),
                    'Missing original dependency byte inventory')
        observed[group] = value
    # Re-fetch mutable selection facts after downloads. Never accept a stale race.
    require(fetch(prefix + '/git/ref/heads/develop')['object']['sha'] == merge_sha,
            'Develop advanced during verification')
    require(policy() == original_policy
            and fetch(prefix + '/pulls/' + str(pr['number'])) == pr
            and fetch(prefix + '/issues/' + str(pr['number']) + '/comments?per_page=100') == comments
            and collection(fetch, prefix + '/actions/workflows/android.yml/runs?event=pull_request&head_sha=' + head,
                           'workflow_runs') == runs, 'Policy, PR, review inventory or execution set changed')
    require(fetch(run_path) == run
            and collection(fetch, run_path + '/jobs?filter=all', 'jobs') == jobs
            and collection(fetch, run_path + '/artifacts', 'artifacts') == artifacts,
            'Prior run metadata changed during verification')
    require(fetch(prefix + '/issues/comments/' + str(comment['id'])) == comment
            and graphql(comment['node_id']) == editor,
            'Review changed during verification')
    require((timestamp(now) + timedelta(seconds=time.monotonic() - began) - timestamp(pr['merged_at'])).total_seconds() <= 3600,
            'Post-merge verification window expired during downloads')
    return dict(qualified, review=review, artifacts=selected, observed_inputs=observed, branch_policy=original_policy,
                original_identity=evidence['original_identity'],
                statement='Prior executed environment accepted; no fresh merge build or release qualification.')


def equivalence_main():
    from datetime import datetime, timezone
    import time
    root = Path('build/prior-evidence')
    receipt = Path('build/reports/prior-evidence.json')
    receipt.unlink(missing_ok=True)
    result = dict(reused=False, reason='Normal execution required')
    deadline = time.monotonic() + 600
    env = dict(os.environ); env.pop('GH_DEBUG', None)
    def request(endpoint, fields=()):
        remaining = deadline - time.monotonic()
        if remaining <= 0: raise ValueError('Preflight request budget expired')
        command = ['gh', 'api', '--hostname', 'github.com', '--method', 'POST' if fields else 'GET', endpoint]
        for key, value in fields: command += ['-f', key + '=' + value]
        data = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=min(20, remaining), check=True).stdout
        if len(data) > 4 * 1024 * 1024: raise ValueError('Oversized metadata')
        return json.loads(data)
    def graphql(node):
        # A query only, not a mutation; same existing token and repository scope.
        query = 'query($id:ID!){node(id:$id){... on IssueComment{id body lastEditedAt author{__typename ... on Bot{id}} editor{__typename ... on Bot{id}}}}}'
        data = request('graphql', [('query', query), ('id', node)])
        if data.get('errors'): raise ValueError('Review editor provenance unavailable')
        return data['data']['node']
    try:
        if root.exists(): raise ValueError('Stale preflight workspace')
        event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
        if os.environ.get('GITHUB_EVENT_NAME') == 'pull_request':
            # Cheap access probe on the normal path; never accepts or skips PR tests.
            if os.environ.get('GITHUB_REPOSITORY') != 'c933103/AN-Paint':
                raise ValueError('Unexpected probe repository')
            number = event.get('number')
            if type(number) is not int or number <= 0: raise ValueError('Missing PR identity')
            query = ('{repository(owner:"c933103",name:"AN-Paint"){pullRequest(number:'
                     + str(number) + '){id comments(last:1){nodes{id lastEditedAt editor{__typename ... on Bot{id}}}}}}}')
            probe = request('graphql', [('query', query)])
            if probe.get('errors') or not probe['data']['repository']['pullRequest']['id']:
                raise ValueError('Review editor API access unavailable')
            result = dict(reused=False, reason='PR qualification always executes normally',
                          review_metadata_api_access=True)
        else:
            result = dict(reused=True, **preflight(request, graphql, Path.cwd(), event,
                os.environ, root, datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')))
    except Exception as error:
        # No output is eligible until every verification succeeds. Do not expose
        # remote bodies, credentials or subprocess stderr in this public receipt.
        result = dict(reused=False, reason='Full fallback: ' + type(error).__name__
                      + ((': ' + str(error)[:200]) if isinstance(error, ValueError) else ''))
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2)+'\n')
    with Path(os.environ['GITHUB_OUTPUT']).open('a') as out:
        out.write('reused=' + str(result['reused']).lower() + '\n')
    with Path(os.environ['GITHUB_STEP_SUMMARY']).open('a') as out:
        out.write('Prior PR evidence verified; full jobs are skipped, not rerun.\n' if result['reused']
                  else 'Normal full verification selected (no prior evidence accepted).\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--core-root', type=Path, required=True)
    parser.add_argument('--position-root', type=Path, required=True)
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text())
    for group, root in [('core', args.core_root), ('position', args.position_root)]:
        download(os.environ['GITHUB_REPOSITORY'], receipt['selected'][group], root)
        print(f"Verified and extracted exact {group} artifact {receipt['selected'][group]['artifact_id']}")


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--equivalence-preflight']:
        equivalence_main()
    else:
        main()
