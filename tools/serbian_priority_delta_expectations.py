"""Finite Serbian accepted delta; no full-P1 or retained-wording acceptance implied."""
from functools import lru_cache
from current_localization_contracts import fixture
FIXTURE='serbian_priority_delta_wording.json'
TAGS=frozenset({'sr-Cyrl','sr-Latn'})
MEMORY_ADDITIONS=frozenset((tag,'ui_no_resize_fits_decoder_memory') for tag in TAGS)
# Only the finite reviewed delta/context fixture is bound, never application source files.
# Its context statuses remain retained/pending; this digest does not grant language credit.
FIXTURE_SHA256='11eb6ba37f8521033694cf3c84770efcc0bf370ac63f118b91a608c20b37bb47'
def validated_fixture_text(text):
    import hashlib,json
    if hashlib.sha256(text.encode('utf-8')).hexdigest()!=FIXTURE_SHA256:
        raise ValueError('Finite Serbian delta/context fixture differs')
    return json.loads(text)
@lru_cache(maxsize=1)
def _baseline():
    from pathlib import Path
    return validated_fixture_text((Path(__file__).resolve().parent/'fixtures/current_localization'/FIXTURE).read_bytes().decode('utf-8'))
def require_reviewed_fixture(data):
    if data!=_baseline():raise ValueError('Serbian delta values or context/metadata differ')
    return data
def reviewed_fixture():
    from copy import deepcopy
    return deepcopy(_baseline())
def cohort():
    from copy import deepcopy
    data=require_reviewed_fixture(fixture(FIXTURE))
    if data.get('schema_version')!=1 or set(data.get('locales',{}))!=TAGS:
        raise ValueError('Serbian delta locale/schema differs')
    return deepcopy(data['locales'])
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
