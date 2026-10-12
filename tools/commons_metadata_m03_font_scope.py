"""Reverse only the pinned additive M03 glyph delta, preserving old font oracles."""
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_SCOPE_PIN = 'fd3aae2b126d17aaffb5d6a9cdc0f6d87cccc9b044fdf61a2fe5c876a935d956'


def font_fixture():
    data = (ROOT / 'tools/fixtures/commons_metadata_m03_font_scope.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != FONT_SCOPE_PIN:
        raise AssertionError('The pinned M03 one-glyph font delta changed')
    return json.loads(data)


def before_m03_font(data):
    scope = font_fixture()
    if len(data) != scope['after_bytes'] or hashlib.sha256(data).hexdigest() != scope['after_sha256']:
        raise AssertionError('Expected exactly the approved M03 font, without unrelated changes')
    for edit in reversed(scope['edits']):
        at = edit['after_offset']
        after = base64.b64decode(edit['after_base64'], validate=True)
        before = base64.b64decode(edit['before_base64'], validate=True)
        if data[at:at+len(after)] != after:
            raise AssertionError('M03 font reverse delta does not match at its exact offset')
        data = data[:at] + before + data[at+len(after):]
    if len(data) != scope['before_bytes'] or hashlib.sha256(data).hexdigest() != scope['before_sha256']:
        raise AssertionError('M03 font reversal did not restore the complete pinned historical font')
    return data
