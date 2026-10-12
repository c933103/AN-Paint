"""Exact painted-ink successor projection, preserving both failed PR55 checkpoints."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/commons_metadata_m04_painted_ink_successor_scope.json'
SCOPE_PIN = '3e7fb249d1334ee1bb9b0ecbe647a9a34b83452e248e772854a40e7721a9efdf'


def scope():
    raw = FIXTURE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SCOPE_PIN:
        raise AssertionError('The exact painted-ink successor fixture changed')
    return json.loads(raw)


def before_painted_ink(path, content, *, allow_original=True):
    """Idempotent for stacked historical oracles; live-source tests require exact new hashes."""
    row = next((row for row in scope()['entries'] if row['path'] == path), None)
    if row is None:
        return content
    digest = hashlib.sha256(content).hexdigest()
    if allow_original and digest == row['before_sha256']:
        return content
    if digest != row['after_sha256']:
        raise AssertionError(f'{path}: unapproved painted-ink successor content')
    text = content.decode()
    for edit in reversed(row['edits']):
        if not edit['after'] or text.count(edit['after']) != 1:
            raise AssertionError(f'{path}: expected one exact painted-ink successor edit')
        text = text.replace(edit['after'], edit['before'], 1)
    restored = text.encode()
    if hashlib.sha256(restored).hexdigest() != row['before_sha256']:
        raise AssertionError(f'{path}: diagnostic source endpoint was not restored')
    return restored
