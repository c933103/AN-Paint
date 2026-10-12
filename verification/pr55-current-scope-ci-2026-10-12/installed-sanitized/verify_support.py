#!/usr/bin/env python3
"""Verify frozen support bytes and optionally materialize safely; execute no code."""
import argparse
import hashlib
import json
import pathlib
import tarfile

from audit_natural_artifacts import HEAD, TREE, MERGE, RUN, require

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=pathlib.Path)
args = parser.parse_args()
root = pathlib.Path(__file__).resolve().parent
manifest = json.loads((root / 'SUPPORTING-INPUTS.json').read_bytes())
require(manifest['head'] == HEAD and manifest['tree'] == TREE
        and manifest['merge'] == MERGE and manifest['run_id'] == int(RUN), 'support binding differs')
archive = root / manifest['archive']['path']; data = archive.read_bytes()
require(len(data) == manifest['archive']['bytes']
        and hashlib.sha256(data).hexdigest() == manifest['archive']['sha256'], 'support archive differs')
expected = {row['path']: row for row in manifest['files']}
require(len(expected) == manifest['file_count']
        and sum(row['bytes'] for row in expected.values()) == manifest['expanded_bytes']
        and manifest['expanded_bytes'] < 160 * 1024 * 1024, 'support inventory/budget differs')
if args.output:
    require(not args.output.exists(), 'use a fresh output directory')
    args.output.mkdir(parents=True)
with tarfile.open(archive, 'r:gz') as tar:
    members = tar.getmembers()
    require(len(members) == len(expected) and {m.name for m in members} == set(expected), 'support member inventory differs')
    for member in members:
        path = pathlib.PurePosixPath(member.name)
        require(member.isfile() and not path.is_absolute() and '..' not in path.parts
                and '\\' not in member.name, 'unsafe support member')
        pin = expected[member.name]; raw = tar.extractfile(member).read()
        require(member.size == pin['bytes'] == len(raw)
                and hashlib.sha256(raw).hexdigest() == pin['sha256'], 'support member differs')
        if args.output:
            target = args.output / member.name; target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
print('PASS', len(expected), 'selected support files;', len(data), 'compressed bytes')
