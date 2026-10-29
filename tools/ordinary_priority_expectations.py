"""Finite complete reviewed values, detached from callers and production output.

Six independently accepted corrections; retained context gives no additional priority credit.
"""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/current_localization/ordinary_priority_followthrough.json'
FIXTURE_SHA256 = 'aa8215c815c10b45517fbe482bcac44f514cb9c4468a5cfb39ac14b961c129a4'


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


def _same_type_and_value(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_same_type_and_value(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_same_type_and_value(x, y) for x, y in zip(a, b))
    return a == b


def require_reviewed_fixture(data):
    require(_same_type_and_value(data, _baseline()), 'Whole finite fixture differs from reviewed baseline')


def row(data, tag, identity):
    require_reviewed_fixture(data)
    require(tag in data['locales'], 'Unreviewed option')
    rows = data['locales'][tag]
    require(identity in rows, 'Unreviewed resource identity')
    return deepcopy(rows[identity])


def _blank(text):
    return text is None or not text.strip()


def typed(element):
    require(element.tag in {'string', 'plurals'}, 'Unexpected resource type')
    require(_blank(element.tail), 'Unexpected resource tail text')
    if element.tag == 'string':
        require(len(element) == 0, 'Unexpected string markup')
    else:
        require(_blank(element.text), 'Unexpected plural container text')
        for child in element:
            require(child.tag == 'item' and len(child) == 0, 'Unexpected plural item markup')
            require(_blank(child.tail), 'Unexpected plural item tail text')
    return {
        'type': element.tag,
        'attributes': dict(element.attrib),
        'value': element.text if element.tag == 'string' else [
            {'type': child.tag, 'attributes': dict(child.attrib), 'value': child.text}
            for child in element
        ],
    }


def _resource_map(path, expected_identities):
    root = ET.parse(path).getroot()
    require(root.tag == 'resources' and not root.attrib, 'Unexpected resource root')
    require(_blank(root.text) and _blank(root.tail), 'Unexpected resource root text')
    expected_names = {identity.split('/', 1)[1] for identity in expected_identities}
    result = {}
    seen_names = set()
    for element in root:
        require(_blank(element.tail), 'Unexpected resource tail text')
        name = element.get('name')
        if name not in expected_names:
            continue  # Unrelated resource types/values are not this finite oracle's scope.
        require(name not in seen_names, 'Duplicate reviewed name across resource types: ' + name)
        seen_names.add(name)
        identity = element.tag + '/' + name
        require(identity in expected_identities, 'Wrong type for reviewed resource: ' + name)
        result[identity] = typed(element)
    return result


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
