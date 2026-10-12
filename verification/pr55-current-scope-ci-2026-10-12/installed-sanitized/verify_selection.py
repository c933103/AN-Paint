#!/usr/bin/env python3
"""Read-only SHA-256 verification of the frozen deliverable selection."""
import hashlib
import json
import pathlib

root = pathlib.Path(__file__).resolve().parent
manifest = json.loads((root / 'DELIVERY-FILES.json').read_bytes())
seen = set()
for row in manifest['files']:
    path = pathlib.PurePosixPath(row['path'])
    if path.is_absolute() or '..' in path.parts or '\\' in row['path'] or row['path'] in seen:
        raise ValueError('unsafe/duplicate selection path')
    seen.add(row['path']); data = (root / path).read_bytes()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('frozen selection differs: ' + row['path'])
if len(seen) != manifest['file_count']:
    raise ValueError('selection count differs')
print('PASS', len(seen), 'frozen selected files')
