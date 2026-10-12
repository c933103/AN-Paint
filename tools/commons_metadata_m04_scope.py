"""Exact M04 successor reversal, preserving every earlier scope fixture and hash."""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOGUE_PIN = '1c023ad1bda141ba65dd4a350a0db72ce5ccc25589bdb25f5680896caa61d1f0'
PRODUCTION_PIN = '52bd33137cc886e11fba8a22abf1979be1e0c820e736540e7c1fb0f4d10cfa01'
TEST_PIN = 'cac97f16c2e846c7b372a1f37db05c42dc5bc2f3732c80995be513da91721fa1'


def pinned(name, digest):
    raw = (ROOT / 'tools/fixtures' / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise AssertionError(f'The pinned M04 scope changed: {name}')
    return json.loads(raw)


def catalogue_fixture():
    return pinned('commons_metadata_query_failure_scope.json', CATALOGUE_PIN)


def production_fixture():
    return pinned('commons_metadata_m04_production_scope.json', PRODUCTION_PIN)


def test_fixture():
    return pinned('commons_metadata_m04_test_scope.json', TEST_PIN)


def before_m04_catalogue(path, text):
    rows = {row['path']: row for row in catalogue_fixture()['entries']}
    if path not in rows:
        return text
    line = rows[path]['line']
    if text.count(line) != 1:
        raise AssertionError(f'{path}: expected exactly one approved M04 addition')
    return text.replace(line, '', 1)


def reverse_edits(path, text, fixture):
    rows = {row['path']: row for row in fixture['entries']}
    if path not in rows:
        return text
    for edit in reversed(rows[path]['edits']):
        if text.count(edit['after']) != 1:
            raise AssertionError(f'{path}: expected the exact M04 delta')
        text = text.replace(edit['after'], edit['before'], 1)
    return text


def before_m04_production(path, text):
    return reverse_edits(path, text, production_fixture())


def before_m04_test(path, text):
    return reverse_edits(path, text, test_fixture())
