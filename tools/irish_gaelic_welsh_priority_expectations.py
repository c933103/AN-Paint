"""Finite reviewed missing-value additions, not a general preservation bypass."""
import xml.etree.ElementTree as ET
import hashlib,json
from current_localization_contracts import fixture
import translation_catalogues as catalogues

NAME='irish_gaelic_welsh_priority_wording.json'
TAGS=frozenset({'ga','gd','cy'})
# Exact finite reviewed fixture, not a whole-source snapshot.
FIXTURE_SHA256='a9d5b5b04943d5923d738b7a814467bd195601232d283953112a086d98866db6'
def require_fixture_binding(data):
    actual=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if actual!=FIXTURE_SHA256:raise ValueError('Complete reviewed fixture binding differs')
    return data

MEMORY_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=frozenset((tag,'save20_unsupported_image_colour') for tag in TAGS)
SVG_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))
ADDITIONS=MEMORY_ADDITIONS|TAGGED_ADDITIONS|SVG_ADDITIONS


def current_row(tag,key):
    if (tag,key) not in ADDITIONS:raise ValueError('Outside exact reviewed addition set')
    data=require_fixture_binding(fixture(NAME))
    if set(data['locales'])!={'ga','gd','cy'}:raise ValueError('Exact three-locale fixture scope differs')
    row=data['locales'][tag]['values']['string/'+key]
    if not {'source','source_attributes','previous_target','previous_attributes','attributes','target','display'} <= set(row):raise ValueError('Required reviewed fields absent: '+tag+'/'+key)
    source=ET.parse(catalogues.RES/'values/strings.xml').getroot().find(f"./string[@name='{key}']")
    if source is None or row['source']!=source.text or row['source_attributes']!=source.attrib:
        raise ValueError('Complete reviewed English source differs: '+tag+'/'+key)
    if row['previous_target'] is not None or row['previous_attributes'] is not None or row['attributes']!={'name':key}:
        raise ValueError('Reviewed addition requires exact historical absence: '+tag+'/'+key)
    if not isinstance(row['target'],str) or not row['target'] or row['display']!=display_text(row['target']):
        raise ValueError('Complete reviewed target/display differs: '+tag+'/'+key)
    return row


def display_text(value):
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return value.replace(r'\n','\n').replace(r"\'", "'").replace(r'\"','"')


def display(tag,key):return current_row(tag,key)['display']

