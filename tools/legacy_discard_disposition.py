"""Finite later disposition of a historical hold; not an active-dialog repair.

Receipt: PR56 issuecomment-6541291852. One existing Pashto refinement and
one unchanged Basque acceptance, separate from the frozen residual packets.
"""
from pathlib import Path
import xml.etree.ElementTree as E
from priority_cohort_checks import require_resource_shape

KEY = 'ui_discard'
PREVIOUS = {'value': 'رد کړئ', 'attributes': {'name': KEY}}
CURRENT = {'value': 'بدلونونه پرېږدئ', 'attributes': {'name': KEY}}
UNCHANGED = {'value': 'Baztertu aldaketak', 'attributes': {'name': KEY}}
ROOT = Path(__file__).resolve().parents[1]


def require_successor(tag, key, element, previous):
    if (tag, key) != ('ps', KEY) or previous != PREVIOUS:
        raise ValueError('Outside exact Discard identity/predecessor')
    source = E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot()
    nodes = source.findall(f"./*[@name='{KEY}']")
    if len(nodes) != 1:
        raise ValueError('Discard source missing or duplicated')
    require_resource_shape(nodes[0], 'string', {'value': 'Discard', 'attributes': {'name': KEY}})
    require_resource_shape(element, 'string', CURRENT)


def require_current_or_historical(tag, key, element, previous):
    if (tag, key) == ('ps', KEY):
        return require_successor(tag, key, element, previous)
    require_resource_shape(element, 'plurals' if isinstance(previous['value'], dict) else 'string', previous)
