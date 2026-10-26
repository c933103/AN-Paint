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


def download(repo, artifact, root, runner=subprocess.run):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository')
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
        if not 0 < archive.stat().st_size <= MAX_ARCHIVE:
            raise ValueError('Archive exceeds compressed report bound')
        with archive.open('rb') as stream:
            checksum = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                checksum.update(chunk)
            actual = checksum.hexdigest()
        if digest != 'sha256:' + actual:
            raise ValueError('Downloaded artifact SHA-256 mismatch')
        extract(archive, root)


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
    main()
