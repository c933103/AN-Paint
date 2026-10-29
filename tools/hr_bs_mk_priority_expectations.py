"""Finite source/previous-value bindings for HR/BS/MK; historical fixtures stay intact."""
from functools import lru_cache
from current_localization_contracts import fixture

FIXTURE = 'croatian_bosnian_macedonian_priority_wording.json'
TAGS = frozenset({'hr', 'bs', 'mk'})

@lru_cache(maxsize=1)
def cohort():
    data=fixture(FIXTURE)
    if data.get('schema_version') != 1 or set(data.get('locales', {})) != TAGS:
        raise ValueError('HR/BS/MK locale/schema scope differs')
    return data['locales']


def row(tag, key):
    return cohort()[tag]['values'].get(key) or cohort()[tag].get('context',{})[key]


def current_value(tag, key, previous, attributes=None, source=None):
    item=cohort().get(tag, {}).get('values', {}).get(key)
    if item is None or not item['changed']:
        return previous
    if previous != item['previous']:
        raise ValueError(tag+'/'+key+': previous value differs')
    if attributes is not None and attributes != item['attributes']:
        raise ValueError(tag+'/'+key+': attributes differ')
    if source is not None and source != item['source']:
        raise ValueError(tag+'/'+key+': English source differs')
    return item['target']


def added_keys(tag):
    return {k for k,r in cohort().get(tag,{}).get('values',{}).items() if r['previous'] is None}


def current_display(tag,key):
    return row(tag,key)['display']


def addition(tag,key,source,previous):
    item=row(tag,key)
    if previous is not None or item['previous'] is not None:
        raise ValueError('HR/BS/MK addition requires absent prior value')
    if source != item['source'] or item['attributes'] != {'name':key}:
        raise ValueError('HR/BS/MK addition source/attributes differ')
    return item['target']

MEMORY_ADDITIONS=frozenset({('hr','ui_no_resize_fits_decoder_memory'),('bs','ui_no_resize_fits_decoder_memory'),('mk','ui_no_resize_fits_decoder_memory'),('mk','ui_assembly_source_memory_floor')})
