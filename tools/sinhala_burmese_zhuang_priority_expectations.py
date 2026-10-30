"""Exact independently reviewed replacement SI/MY replacement and bounded ZA expectations, not fresh linguistic certification."""
import re
import hashlib
from functools import lru_cache
from copy import deepcopy
from pathlib import Path
from current_localization_contracts import fixture
NAME='sinhala_burmese_zhuang_priority_wording.json'
FIXTURE_SHA256='92c0f8eadd3374f82d8761fce44cff52bdd889f22d7cf7453f7172da20960388'

def validated_fixture_text(text):
    if hashlib.sha256(text.encode()).hexdigest()!=FIXTURE_SHA256:
        raise ValueError('Complete finite accepted SI/MY replacement and bounded ZA fixture differs')
    import json
    return json.loads(text)

@lru_cache(maxsize=1)
def _baseline():
    return validated_fixture_text((Path(__file__).resolve().parent/'fixtures/current_localization'/NAME).read_text())

def reviewed_fixture():
    return deepcopy(_baseline())

TAGS=frozenset({'si','my','za'})
ADDITION_TAGS=frozenset({'si','my'})
MEMORY_ADDITIONS=frozenset((tag,key) for tag in ADDITION_TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))

def current_row(tag,key):
    data=_baseline()
    if tag not in TAGS:raise ValueError('Outside recovered SI/MY replacement and bounded ZA scope')
    loc=data['locales'][tag]
    if key not in loc['accepted']:raise ValueError('No accepted complete value')
    previous=loc['predecessors'].get(key)
    return {'source':deepcopy(data['sources'][key]['value']),'target':deepcopy(loc['accepted'][key]),
            'attributes':dict(loc['attributes'][key]),'previous_target':previous['value'] if previous else None,
            'previous_attributes':dict(previous['attributes']) if previous else None,'changed':key in loc['changed']}

def display(tag,key):
    seen=set()
    while True:
        if key in seen:raise ValueError('Cyclic resource alias')
        seen.add(key)
        value=current_row(tag,key)['target']
        if not isinstance(value,str):raise ValueError('Expected string, not plural')
        if not value.startswith('@string/'):break
        key=value[len('@string/'):]
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m.group(1),m.group(1)),value)

def require_reviewed_fixture(data):
    # Compare mutable input to the separately loaded accepted complete baseline,
    # not to its own display field; coordinated target/display forgery fails.
    if data!=_baseline():raise ValueError('Recovered reviewed values or metadata differ')
    return data
