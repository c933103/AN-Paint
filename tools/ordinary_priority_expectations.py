"""Finite complete reviewed values, detached from callers and production output.

Nine independently accepted corrections; retained context gives no additional priority credit.
"""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from finite_resource_values import _blank, _resource_map, _same_type_and_value, typed

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/current_localization/ordinary_priority_followthrough.json'
FIXTURE_SHA256 = '3941373cd41425e7fcbfa8afaeafd2f36b1588141ac7e469824225ff03732ee5'


def require(condition, message):
    if not condition:
        raise ValueError(message)


@lru_cache(maxsize=1)
def _baseline():
    raw = FIXTURE.read_bytes()
    require(sha256(raw).hexdigest() == FIXTURE_SHA256, 'Finite review fixture changed')
    data = json.loads(raw)
    require(data['schema'] == 1, 'Unexpected fixture schema')
    return data


def reviewed_fixture():
    return deepcopy(_baseline())


def require_reviewed_fixture(data):
    require(_same_type_and_value(data, _baseline()), 'Whole finite fixture differs from reviewed baseline')


def row(data, tag, identity):
    require_reviewed_fixture(data)
    require(tag in data['locales'], 'Unreviewed option')
    rows = data['locales'][tag]
    require(identity in rows, 'Unreviewed resource identity')
    return deepcopy(rows[identity])


def validate_resources(data, source, targets):
    require_reviewed_fixture(data)
    identities = {key for rows in data['locales'].values() for key in rows}
    canonical = _resource_map(source, identities)
    for tag, rows in data['locales'].items():
        actual = _resource_map(targets[tag], set(rows))
        for identity, expected in rows.items():
            require(canonical.get(identity) == expected['source'], 'Canonical typed value changed: ' + identity)
            require(actual.get(identity) == expected['target'], 'Complete typed target changed: ' + tag + '/' + identity)
    return True
