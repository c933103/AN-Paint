"""Strict receiver and status-remeasurement successor; no old fixture or failed checkpoint is repinned."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/commons_metadata_m04_receiver_successor_scope.json'
SCOPE_PIN = '6b9255e6dd666c2227e4b396a3057e6f8b42517f9cac8689ee0179e3e3317f7d'
PATHS = frozenset(['Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt', 'tools/commons_metadata_m04_glyph_bounds_scope.py', 'tools/test_commons_metadata_m04_glyph_bounds.py', 'Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt', 'app/src/androidTest/java/paint/anpaint/android/GalleryViewportDeviceTest.kt'])


def scope():
    raw = FIXTURE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SCOPE_PIN:
        raise AssertionError('Receiver successor fixture changed')
    return json.loads(raw)


def before_receiver_fix(path, content, *, allow_original=True):
    if path not in PATHS:
        return content
    row = next(row for row in scope()['entries'] if row['path'] == path)
    digest = hashlib.sha256(content).hexdigest()
    if allow_original and digest == row['before_sha256']:
        return content
    if digest != row['after_sha256']:
        raise AssertionError(f'{path}: unapproved receiver successor bytes')
    text = content.decode()
    for edit in reversed(row['edits']):
        if not edit['after'] or text.count(edit['after']) != 1:
            raise AssertionError(f'{path}: receiver edit is missing or duplicated')
        text = text.replace(edit['after'], edit['before'], 1)
    restored = text.encode()
    if hashlib.sha256(restored).hexdigest() != row['before_sha256']:
        raise AssertionError(f'{path}: original receiver endpoint was not restored')
    return restored
