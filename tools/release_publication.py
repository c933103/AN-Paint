"""Reconcile exact release identities and assets without destructive retries."""
import hashlib
import re
import subprocess
from urllib.parse import quote


def pages(api, endpoint):
    for page in range(1, 101):
        rows = api(f'{endpoint}?per_page=100&page={page}')
        if not isinstance(rows, list):
            raise ValueError('Expected a paginated GitHub list')
        yield from rows
        if len(rows) < 100:
            return
    raise ValueError('GitHub pagination exceeded the safety limit')


def tag_commit(api, repo, tag):
    # This endpoint returns [] for an absent tag, avoiding interpreting errors as absence.
    refs = api(f'repos/{repo}/git/matching-refs/tags/{quote(tag, safe="")}')
    if not isinstance(refs, list):
        raise ValueError('Expected a GitHub tag reference list')
    exact = [row for row in refs if row['ref'] == f'refs/tags/{tag}']
    if not exact:
        return None
    if len(exact) != 1:
        raise ValueError('Ambiguous release tag')
    obj = exact[0]['object']
    seen = set()
    for _ in range(16):
        sha = obj['sha']
        if not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{40}', sha):
            raise ValueError('Malformed tag object identity')
        if sha in seen:
            raise ValueError('Cyclic tag object')
        seen.add(sha)
        if obj['type'] == 'commit':
            return sha
        if obj['type'] != 'tag':
            raise ValueError('Release tag does not resolve to a commit')
        obj = api(f'repos/{repo}/git/tags/{sha}')['object']
    raise ValueError('Release tag chain exceeds the safety limit')


def verify_tag(api, repo, tag, commit, *, allow_missing):
    actual = tag_commit(api, repo, tag)
    if actual is None and allow_missing:
        return
    if actual != commit:
        raise ValueError('Release tag does not identify the verified commit')


def find_release(api, repo, tag):
    # Listing includes token-visible drafts, including drafts without a Git tag.
    matches = [row for row in pages(api, f'repos/{repo}/releases') if row['tag_name'] == tag]
    if len(matches) > 1:
        raise ValueError('Multiple releases use the requested tag')
    return matches[0] if matches else None


def verify_release(release, *, tag, commit, title, notes):
    if (release is None or release['tag_name'] != tag or release['target_commitish'] != commit
            or release['name'] != title or (release['body'] or '') != notes
            or release['prerelease'] is not False or type(release['draft']) is not bool
            or type(release['id']) is not int):
        raise ValueError('Existing release does not match the verified request')


def missing_assets(api, repo, release, expected):
    seen = set()
    for asset in pages(api, f'repos/{repo}/releases/{release["id"]}/assets'):
        name = asset['name']
        if name in seen or name not in expected:
            raise ValueError('Duplicate or unexpected release asset')
        seen.add(name)
        path, size, sha256 = expected[name]
        if (asset['state'] != 'uploaded' or type(asset['size']) is not int
                or asset['size'] != size or asset.get('digest') != 'sha256:' + sha256):
            raise ValueError('Existing release asset identity is incomplete or mismatched')
    return [row[0] for name, row in expected.items() if name not in seen]


def publish_verified_release(api, run, *, repo, tag, commit, title, notes_path, assets):
    expected = {}
    for path in assets:
        if path.name in expected:
            raise ValueError('Local asset names must be unique')
        data = path.read_bytes()
        expected[path.name] = (path, len(data), hashlib.sha256(data).hexdigest())
    notes = notes_path.read_bytes().decode('utf-8')
    verify_tag(api, repo, tag, commit, allow_missing=True)
    release = find_release(api, repo, tag)
    if release is None:
        try:
            run('gh', 'release', 'create', tag, '--repo', repo, '--target', commit,
                '--title', title, '--notes-file', notes_path, '--draft')
        except subprocess.CalledProcessError:
            # Only a readback can establish whether the uncertain create succeeded.
            release = find_release(api, repo, tag)
            if release is None:
                raise
        else:
            release = find_release(api, repo, tag)
    verify_release(release, tag=tag, commit=commit, title=title, notes=notes)
    verify_tag(api, repo, tag, commit, allow_missing=release['draft'])
    missing = missing_assets(api, repo, release, expected)
    if not release['draft']:
        if missing:
            raise ValueError('Published release is missing verified assets')
        return release['html_url']
    if missing:
        try:
            run('gh', 'release', 'upload', tag, '--repo', repo, *missing)
        except subprocess.CalledProcessError:
            # Do not retry an uncertain upload or overwrite anything. Reconcile it.
            if missing_assets(api, repo, release, expected):
                raise
        if missing_assets(api, repo, release, expected):
            raise ValueError('Draft is missing verified assets after upload')
    verify_tag(api, repo, tag, commit, allow_missing=True)
    publish_error = None
    try:
        run('gh', 'release', 'edit', tag, '--repo', repo, '--draft=false', '--latest')
    except subprocess.CalledProcessError as error:
        publish_error = error
    final = find_release(api, repo, tag)
    verify_release(final, tag=tag, commit=commit, title=title, notes=notes)
    if final['id'] != release['id'] or final['draft']:
        if publish_error:
            raise publish_error
        raise ValueError('Publication did not yield the matching published release')
    verify_tag(api, repo, tag, commit, allow_missing=False)
    if missing_assets(api, repo, final, expected):
        raise ValueError('Published release is missing verified assets')
    return final['html_url']
