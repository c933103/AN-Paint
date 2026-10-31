"""Finite source correction and Swedish successor to the explicit manual hold.

The full revised pair was reviewed together; this is not an active Help caller.
Historical fixtures remain unchanged and do not certify the revised wording.
"""
from pathlib import Path
import xml.etree.ElementTree as E
from current_localization_contracts import fixture
from priority_cohort_checks import require_resource_shape

ROOT = Path(__file__).resolve().parents[1]
KEY = 'ui_the_arrow_on_the_left_directly_below_the'
ATTRIBUTES = {'name': KEY, 'formatted': 'false'}


def decision():
    data = fixture('swedish_legacy_manual_successor.json')
    if (set(data) != {'schema_version', 'key', 'attributes', 'review',
                     'previous_source', 'previous_swedish', 'source', 'swedish'}
            or type(data['schema_version']) is not int or data['schema_version'] != 1
            or data['key'] != KEY or data['attributes'] != ATTRIBUTES
            or data['previous_swedish'] is not None
            or not all(isinstance(data[k], str) and data[k] for k in
                       ('previous_source', 'source', 'swedish', 'review'))
            or data['source'] == data['previous_source']):
        raise ValueError('Outside exact Swedish legacy-manual decision')
    return data


def require_successor(tag, key, element, previous):
    data = decision()
    old = {'value': data['previous_source'], 'attributes': ATTRIBUTES} if tag == 'default' else None
    if tag not in ('default', 'sv') or key != KEY or previous != old:
        raise ValueError('Outside exact manual identity/predecessor')
    source = E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot()
    nodes = source.findall(f"./*[@name='{KEY}']")
    if len(nodes) != 1:
        raise ValueError('Manual source missing or duplicated')
    require_resource_shape(nodes[0], 'string', {'value': data['source'], 'attributes': ATTRIBUTES})
    require_resource_shape(element, 'string', {
        'value': data['source' if tag == 'default' else 'swedish'], 'attributes': ATTRIBUTES})
