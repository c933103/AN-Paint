"""Exact PR52/M04 projections; original producer fixtures remain immutable."""
import hashlib
import json
from pathlib import Path

from commons_metadata_m04_scope import before_m04_catalogue
from commons_metadata_m04_diagnostic_scope import before_diagnostic
from commons_metadata_m02_scope import before_m02_catalogue
from hungarian_attribution_c05_scope import before_c05

ROOT = Path(__file__).resolve().parents[1]
SCOPE_PIN = '479b2a2f4172521ee71e955024a409fe27f2621bde21f32630f6eaee7e05cc4b'
FIXTURE = ROOT / 'tools/fixtures/commons_metadata_m04_pr52_successor_scope.json'


def scope():
    raw = FIXTURE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SCOPE_PIN:
        raise AssertionError('The exact PR52/M04 successor fixture changed')
    return json.loads(raw)


def reverse(path, content, rows, strict=True):
    row = next((row for row in rows if row['path'] == path), None)
    if row is None:
        return content
    if strict and hashlib.sha256(content).hexdigest() != row['after_sha256']:
        raise AssertionError(f'{path}: unapproved PR52/M04 successor content')
    text = content.decode()
    for edit in reversed(row['edits']):
        if not edit['after'] or text.count(edit['after']) != 1:
            raise AssertionError(f'{path}: expected one exact PR52/M04 successor edit')
        text = text.replace(edit['after'], edit['before'], 1)
    restored = text.encode()
    if strict and hashlib.sha256(restored).hexdigest() != row['before_sha256']:
        raise AssertionError(f'{path}: original producer endpoint was not restored')
    return restored


def before_composed_m04(path, content):
    """Recover the exact current-PR52 endpoint for its historical source checks."""
    return reverse(path, before_diagnostic(path, content), scope()['pr52_overlaps'])


def before_m04_composed_production(path, text):
    """Undo only M04 fragments; caller retains its original complete-file oracle."""
    rows = [row for row in scope()['pr52_overlaps'] if row['kind'] == 'production']
    return reverse(path, before_diagnostic(path, text.encode()), rows, strict=False).decode()


def as_standalone_m04_bytes(path, content):
    """Preserve M04's original hashes without erasing accepted PR52 behavior."""
    return reverse(path, before_diagnostic(path, content), scope()['m04_overlaps'])


def as_standalone_m04(path, text):
    if path.startswith('Paintroid/src/main/res/') and path.endswith('/strings.xml'):
        return before_c05(path, before_m02_catalogue(path, text))
    return as_standalone_m04_bytes(path, text.encode()).decode()
