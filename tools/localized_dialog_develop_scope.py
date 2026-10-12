"""Narrow successor projections for immutable PR52 producer-union receipts."""
import hashlib
import json
from pathlib import Path

from commons_metadata_m03_scope import before_m03_catalogue
from commons_metadata_composition_scope import without_m03_production

ROOT = Path(__file__).resolve().parents[1]
SCOPE_PIN = '4490a83efe54132bdefb65aa12544de75f6402037d1573cae3cc7a52178e25af'


def scope():
    raw = (ROOT / 'tools/fixtures/localized_dialog_develop_successor_scope.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != SCOPE_PIN:
        raise AssertionError('The exact develop successor scope changed')
    return json.loads(raw)


def before_develop_successor(path, content):
    """Undo only explicit M03 and PR40 overlaps; no historic fixture is rewritten."""
    if path.startswith('Paintroid/src/main/res/') and path.endswith('/strings.xml'):
        return before_m03_catalogue(path, content.decode()).encode()
    if path in ('Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt',
                'Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt'):
        return without_m03_production(path, content.decode()).encode()
    rows = {row['path']: row for row in scope()['historical_overlaps']}
    if path not in rows:
        return content
    row = rows[path]
    if hashlib.sha256(content).hexdigest() != row['composed_sha256']:
        raise AssertionError(f'{path}: unapproved successor content')
    text = content.decode()
    for edit in reversed(row['edits']):
        if text.count(edit['after']) != 1:
            raise AssertionError(f'{path}: expected exact successor edit')
        text = text.replace(edit['after'], edit['before'], 1)
    restored = text.encode()
    if hashlib.sha256(restored).hexdigest() != row['pr52_sha256']:
        raise AssertionError(f'{path}: original PR52 endpoint was not restored')
    return restored
