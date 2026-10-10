#!/usr/bin/env python3
"""Reassemble the exact historical standalone PR34 evidence ZIP; fail closed."""
import base64
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'archive-parts.json').read_text())
expected = {row['path'] for row in manifest['parts']}
actual = {str(path.relative_to(root)) for path in (root / 'archive-parts').glob('*.b64')}
assert actual == expected, 'Missing or unexpected archive part'
chunks = []
for row in manifest['parts']:
    encoded = (root / row['path']).read_bytes()
    assert hashlib.sha256(encoded).hexdigest() == row['encoded_sha256'], row['path']
    chunk = base64.b64decode(encoded.strip(), validate=True)
    assert len(chunk) == row['bytes'], row['path']
    assert hashlib.sha256(chunk).hexdigest() == row['sha256'], row['path']
    chunks.append(chunk)
data = b''.join(chunks)
assert len(data) == manifest['bytes']
assert hashlib.sha256(data).hexdigest() == manifest['sha256']
assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == manifest['git_blob_sha']
output = root / manifest['file_name']
output.write_bytes(data)
print(f"Verified {len(data)} bytes: {manifest['sha256']} -> {output.name}")
