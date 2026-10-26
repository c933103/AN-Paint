"""Correct only an existing release's body, preserving its verified identity/assets."""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from release_publication import pages, verify_tag
from urllib.parse import quote


ASSET_FIELDS = ('id', 'name', 'label', 'state', 'size', 'digest', 'content_type',
                'created_at', 'updated_at', 'browser_download_url')
RELEASE_FIELDS = ('id', 'tag_name', 'target_commitish', 'name', 'draft', 'prerelease',
                  'immutable', 'created_at', 'published_at', 'html_url')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def asset_identity(assets):
    identities = [{key: asset[key] for key in ASSET_FIELDS} for asset in assets]
    if len({a['name'] for a in identities}) != len(identities):
        raise ValueError('Duplicate asset names')
    return sorted(identities, key=lambda a: a['name'])


def verify_state(api, request):
    repo, expected = request['repository'], request['release']
    refs = api(f"repos/{repo}/git/matching-refs/tags/{quote(expected['tag_name'], safe='')}")
    exact = [row for row in refs if row['ref'] == 'refs/tags/' + expected['tag_name']]
    if (len(exact) != 1 or {key: exact[0]['object'][key] for key in ('type', 'sha')}
            != request['tag_object']):
        raise ValueError('Release tag object changed')
    verify_tag(api, repo, expected['tag_name'], expected['target_commitish'], allow_missing=False)
    release = api(f"repos/{repo}/releases/{expected['id']}")
    if {key: release[key] for key in RELEASE_FIELDS} != expected:
        raise ValueError('Existing release identity changed')
    assets = asset_identity(pages(api, f"repos/{repo}/releases/{expected['id']}/assets"))
    if assets != request['assets']:
        raise ValueError('Existing release assets changed')
    return release


def correct(api, patch, request, notes, repo):
    """One body-only PATCH at most; reconcile uncertain results rather than retrying."""
    if repo != request['repository']:
        raise ValueError('Correction repository mismatch')
    expected = request['release']
    if (set(expected) != set(RELEASE_FIELDS) or type(expected['id']) is not int
            or expected['draft'] is not False or expected['prerelease'] is not False
            or not re.fullmatch(r'v\d+\.\d+\.\d+', expected['tag_name'])
            or not re.fullmatch(r'[0-9a-f]{40}', expected['target_commitish'])):
        raise ValueError('Invalid published release identity')
    if not notes.strip() or digest(notes) != request['corrected_body_sha256']:
        raise ValueError('Corrected notes do not match the reviewed content')
    before = verify_state(api, request)
    current = before['body'] or ''
    if current == notes:
        return {'status': 'already_corrected', 'url': before['html_url'],
                'body_sha256': digest(current)}
    if digest(current) != request['previous_body_sha256']:
        raise ValueError('Release body changed since this correction was prepared')
    error = None
    try:
        patch(f"repos/{repo}/releases/{expected['id']}", {'body': notes})
    except subprocess.CalledProcessError as failure:
        error = failure
    after = verify_state(api, request)
    if (after['body'] or '') != notes:
        if error:
            raise error
        raise ValueError('Release body correction was not confirmed')
    return {'status': 'corrected', 'url': after['html_url'], 'body_sha256': digest(notes)}


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path], text=True))


def patch(path, body):
    # Never pass title, tag, target, publication flags or assets to the mutation.
    subprocess.run(['gh', 'api', '--method', 'PATCH', path, '--input', '-'],
                   input=json.dumps(body), text=True, check=True, stdout=subprocess.DEVNULL)


def main(request_path):
    request = json.loads(request_path.read_text(encoding='utf-8'))
    filename = request['notes_file']
    if Path(filename).name != filename:
        raise ValueError('Notes must be adjacent to the reviewed request')
    notes = request_path.with_name(filename).read_bytes().decode('utf-8')
    result = correct(api, patch, request, notes, os.environ['GITHUB_REPOSITORY'])
    out = Path('build/release-notes-correction'); out.mkdir(parents=True, exist_ok=True)
    (out / 'result.json').write_text(json.dumps({**result, 'release': request['release'],
        'assets': request['assets'], 'request_sha256': hashlib.sha256(request_path.read_bytes()).hexdigest()},
        indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
