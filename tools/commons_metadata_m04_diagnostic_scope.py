"""Exact reversible PR55 diagnostic-only successor; frozen producer fixtures stay unchanged."""
import hashlib
import json
from pathlib import Path

from commons_metadata_m04_painted_ink_scope import before_painted_ink

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/commons_metadata_m04_diagnostic_successor_scope.json'
SCOPE_PIN = 'b41ec5e2d53ea0cb8cc64f9cef5d6cd8800e3c2b9e8a07828d647eef7a895356'


def scope():
    raw = FIXTURE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SCOPE_PIN:
        raise AssertionError('The exact PR55 diagnostic successor fixture changed')
    return json.loads(raw)


def before_diagnostic(path, content):
    """Restore the exact failed PR55 source before applying older producer projections."""
    content = before_painted_ink(path, content)
    row = next((row for row in scope()['entries'] if row['path'] == path), None)
    if row is None:
        return content
    if hashlib.sha256(content).hexdigest() != row['after_sha256']:
        raise AssertionError(f'{path}: unapproved PR55 diagnostic successor content')
    text = content.decode()
    for edit in reversed(row['edits']):
        if not edit['after'] or text.count(edit['after']) != 1:
            raise AssertionError(f'{path}: expected one exact diagnostic successor edit')
        text = text.replace(edit['after'], edit['before'], 1)
    restored = text.encode()
    if hashlib.sha256(restored).hexdigest() != row['before_sha256']:
        raise AssertionError(f'{path}: failed PR55 source endpoint was not restored')
    return restored
