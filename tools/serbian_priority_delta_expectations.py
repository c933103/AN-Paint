"""Finite Serbian accepted delta; no full-P1 or retained-wording acceptance implied."""
from functools import lru_cache
from current_localization_contracts import fixture
FIXTURE='serbian_priority_delta_wording.json'
TAGS=frozenset({'sr-Cyrl','sr-Latn'})
MEMORY_ADDITIONS=frozenset((tag,'ui_no_resize_fits_decoder_memory') for tag in TAGS)
@lru_cache(maxsize=1)
def cohort():
    data=fixture(FIXTURE)
    if data.get('schema_version')!=1 or set(data.get('locales',{}))!=TAGS:
        raise ValueError('Serbian delta locale/schema differs')
    return data['locales']
def row(tag,key):return cohort()[tag]['values'].get(key) or cohort()[tag]['context'][key]
def current_value(tag,key,previous,attributes,source):
    item=cohort().get(tag,{}).get('values',{}).get(key)
    if item is None:return previous
    if not item['changed'] or item['review_status']!='accepted_delta' or item['previous']!=previous:
        raise ValueError('Serbian delta previous/review binding differs: '+tag+'/'+key)
    if item['attributes']!=attributes or item['source']!=source:
        raise ValueError('Serbian delta source/attributes differ: '+tag+'/'+key)
    return item['target']
def addition(tag,key,source,previous):
    item=row(tag,key)
    if previous is not None or item['previous'] is not None:
        raise ValueError('Serbian delta addition requires explicit absence')
    return current_value(tag,key,previous,{'name':key},source)
