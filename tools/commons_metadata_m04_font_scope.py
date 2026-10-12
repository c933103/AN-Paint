"""Reverse only the pinned additive M04 glyph delta, preserving old font oracles."""
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_SCOPE_PIN = '0ec5bc3a2323b7373deb932956ceaacb3e070407ba6db7add9fb38dcd8dcf5df'


def font_fixture():
    data = (ROOT / 'tools/fixtures/commons_metadata_m04_font_scope.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != FONT_SCOPE_PIN:
        raise AssertionError('The pinned M04 three-glyph font delta changed')
    return json.loads(data)


def before_m04_font(data):
    scope = font_fixture()
    if len(data) != scope['after_bytes'] or hashlib.sha256(data).hexdigest() != scope['after_sha256']:
        raise AssertionError('Expected exactly the approved M04 font, without unrelated changes')
    for edit in reversed(scope['edits']):
        at = edit['after_offset']
        after = base64.b64decode(edit['after_base64'], validate=True)
        before = base64.b64decode(edit['before_base64'], validate=True)
        if data[at:at+len(after)] != after:
            raise AssertionError('M04 font reverse delta does not match at its exact offset')
        data = data[:at] + before + data[at+len(after):]
    if len(data) != scope['before_bytes'] or hashlib.sha256(data).hexdigest() != scope['before_sha256']:
        raise AssertionError('M04 font reversal did not restore the complete pinned historical font')
    return data


def before_m04_inventory(text):
    scope = font_fixture()
    if text.count(scope['after_sha256']) != 1:
        raise AssertionError('Expected exactly the M04 font inventory entry')
    return text.replace(scope['after_sha256'], scope['before_sha256'], 1)
