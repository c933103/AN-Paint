"""Exact measured glyph-bounds successor projection; all failed checkpoints stay immutable."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/commons_metadata_m04_glyph_bounds_successor_scope.json'
SCOPE_PIN = '824cb01cbd9f9c9edf3e7283b1ccdc18da7c0e7bb1fc88a4a59a3a38ff4a0639'
PATHS = frozenset(['Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt', 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt', 'app/src/androidTest/java/paint/anpaint/android/GalleryViewportDeviceTest.kt', 'tools/commons_metadata_m04_painted_ink_scope.py', 'tools/test_commons_metadata_m04_painted_ink.py', 'tools/test_commons_metadata_m04_composition.py','tools/commons_metadata_m04_composition_scope.py'])


def scope():
    raw = FIXTURE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SCOPE_PIN:
        raise AssertionError('The exact glyph-bounds successor fixture changed')
    return json.loads(raw)


def before_glyph_bounds(path, content, *, allow_original=True):
    """Idempotent for stacked historical oracles; live-source tests require exact new hashes."""
    if path not in PATHS:
        return content
    row = next((row for row in scope()['entries'] if row['path'] == path), None)
    if row is None:
        return content
    digest = hashlib.sha256(content).hexdigest()
    if allow_original and digest == row['before_sha256']:
        return content
    if digest != row['after_sha256']:
        raise AssertionError(f'{path}: unapproved glyph-bounds successor content')
    text = content.decode()
    for edit in reversed(row['edits']):
        if not edit['after'] or text.count(edit['after']) != 1:
            raise AssertionError(f'{path}: expected one exact glyph-bounds successor edit')
        text = text.replace(edit['after'], edit['before'], 1)
    restored = text.encode()
    if hashlib.sha256(restored).hexdigest() != row['before_sha256']:
        raise AssertionError(f'{path}: strict painted-ink source endpoint was not restored')
    return restored
