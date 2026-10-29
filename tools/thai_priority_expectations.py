"""Exact independently reviewed replacement Thai replacement expectations, not fresh linguistic certification."""
import re
import hashlib
from functools import lru_cache
from copy import deepcopy
from pathlib import Path
from current_localization_contracts import fixture
NAME='thai_priority_replacement.json'
FIXTURE_SHA256='0dffad5b3b729fa57da3feb781b9e97edd12e108200f5e4076356cbc1697d1f6'

def validated_fixture_text(text):
    if hashlib.sha256(text.encode()).hexdigest()!=FIXTURE_SHA256:
        raise ValueError('Complete finite accepted Thai replacement fixture differs')
    import json
    return json.loads(text)

@lru_cache(maxsize=1)
def _baseline():
    return validated_fixture_text((Path(__file__).resolve().parent/'fixtures/current_localization'/NAME).read_text())

def reviewed_fixture():
    return deepcopy(_baseline())

TAGS=frozenset({'th'})
MEMORY_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))

def current_row(tag,key):
    data=_baseline()
    if tag not in TAGS:raise ValueError('Outside recovered Thai replacement scope')
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
