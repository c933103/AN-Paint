"""Strict, reversible PR52 + PR51 source composition, not runtime acceptance."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/dialog_colour_composition_scope.json'
FIXTURE_SHA256 = '5922b9630353492f7941bc536b82f3a0eda3cab7610c4c22d8971e5f4b9cc1cd'


def digest(value):
    return hashlib.sha256(value).hexdigest()


def scope():
    raw = FIXTURE.read_bytes()
    if digest(raw) != FIXTURE_SHA256:
        raise ValueError('Combined source disposition fixture changed')
    return json.loads(raw)


def before_colour_composition(path, content):
    """Recover exact accepted PR52 bytes only from its pinned composed successor."""
    rows = [row for row in scope()['replaced_pr52_paths'] if row['path'] == path]
    if not rows:
        return content
    if len(rows) != 1:
        raise ValueError('Duplicate source disposition')
    row = rows[0]
    if digest(content) != row['after_sha256']:
        raise ValueError('Source exceeds the explicit colour composition scope: ' + path)
    before = (ROOT / row['historical_path']).read_bytes()
    if digest(before) != row['before_sha256']:
        raise ValueError('Historical PR52 endpoint changed: ' + path)
    return before
