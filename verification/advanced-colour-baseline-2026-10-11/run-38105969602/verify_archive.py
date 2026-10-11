#!/usr/bin/env python3
"""Reassemble and verify the archived evidence without extracting or executing it."""
from pathlib import Path
import hashlib
import io
import json
import zipfile


def verify(root):
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    archive = manifest['archive']
    chunks = []
    for part in manifest['parts']:
        path = Path(part['path'])
        if path.name != str(path):
            raise ValueError('Part path must be a basename')
        data = (root / path).read_bytes()
        if len(data) != part['bytes'] or len(data) > archive['max_part_bytes']:
            raise ValueError('Part size mismatch: ' + str(path))
        if hashlib.sha256(data).hexdigest() != part['sha256']:
            raise ValueError('Part SHA-256 mismatch: ' + str(path))
        chunks.append(data)
    if len(chunks) != archive['part_count']:
        raise ValueError('Part count mismatch')
    data = b''.join(chunks)
    if len(data) != archive['bytes'] or hashlib.sha256(data).hexdigest() != archive['sha256']:
        raise ValueError('Archive byte count or SHA-256 mismatch')
    records = {row['path']: row for row in manifest['members']}
    with zipfile.ZipFile(io.BytesIO(data)) as packed:
        names = packed.namelist()
        if len(names) != archive['member_count'] or len(names) != len(records) or set(names) != set(records):
            raise ValueError('Member names/count mismatch')
        if packed.testzip() is not None:
            raise ValueError('ZIP CRC check failed')
        for name, row in records.items():
            payload = packed.read(name)
            if len(payload) != row['bytes'] or hashlib.sha256(payload).hexdigest() != row['sha256']:
                raise ValueError('Member byte count or SHA-256 mismatch: ' + name)
    name = Path(archive['filename'])
    if name.name != str(name):
        raise ValueError('Archive filename must be a basename')
    destination = root / name
    if destination.exists() and destination.read_bytes() != data:
        raise ValueError('Refusing to overwrite a different archive')
    destination.write_bytes(data)
    print(json.dumps({'verified': True, 'sha256': archive['sha256'], 'bytes': len(data), 'members': len(records), 'parts': len(chunks)}, indent=2))


if __name__ == '__main__':
    verify(Path(__file__).resolve().parent)
