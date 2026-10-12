"""Exact M03 successor reversal; retain every historical source/catalogue hash."""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOGUE_PIN = '2bf39ff3c05322e4ecb10adbe90e8790b6d53580073cd412b128324db47852ef'
PRODUCTION_PIN = '27255affc9138de58320c994d215534e272f939e4e0e1935170fe857dc8a5220'


def pinned(name, digest):
    raw = (ROOT / 'tools/fixtures' / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise AssertionError(f'The pinned M03 scope changed: {name}')
    return json.loads(raw)


def catalogue_fixture():
    return pinned('commons_metadata_response_limit_scope.json', CATALOGUE_PIN)


def production_fixture():
    return pinned('commons_metadata_m03_production_scope.json', PRODUCTION_PIN)


def before_m03_catalogue(path, text):
    rows = {row['path']: row for row in catalogue_fixture()['entries']}
    if path not in rows:
        return text
    line = rows[path]['line']
    if text.count(line) != 1:
        raise AssertionError(f'{path}: expected exactly one approved M03 addition')
    return text.replace(line, '', 1)


def before_m03_production(path, text):
    rows = {row['path']: row for row in production_fixture()['entries']}
    if path not in rows:
        return text
    for edit in reversed(rows[path]['edits']):
        if text.count(edit['after']) != 1:
            raise AssertionError(f'{path}: expected the exact M03 producer/callback delta')
        text = text.replace(edit['after'], edit['before'], 1)
    return text
