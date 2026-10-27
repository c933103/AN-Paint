"""Finite reviewed missing-value additions, not a general preservation bypass."""
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture
import translation_catalogues as catalogues

NAME='galician_dutch_german_priority_wording.json'
TAGS=frozenset({'gl'})
MEMORY_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=frozenset((tag,'save20_unsupported_image_colour') for tag in TAGS)
SVG_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))
ADDITIONS=MEMORY_ADDITIONS|TAGGED_ADDITIONS|SVG_ADDITIONS


def current_row(tag,key):
    if (tag,key) not in ADDITIONS:raise ValueError('Outside exact reviewed addition set')
    data=fixture(NAME)
    if set(data['locales'])!={'gl','nl','de'}:raise ValueError('Exact three-locale fixture scope differs')
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

# Finite corrections to already-published Dutch/German expectations. Historical fixtures stay intact.
MEMORY_CORRECTIONS=frozenset((tag,'ui_d_d_pixels_2f_mp_exceeds_the_current') for tag in ('nl','de'))
WORDING_CORRECTIONS=MEMORY_CORRECTIONS|{('nl','ui_swap_foreground_background')}
def wording_successor(tag,key,historical_value):
    if (tag,key) not in WORDING_CORRECTIONS:raise ValueError('Outside exact reviewed correction set')
    data=fixture(NAME)
    if set(data['locales'])!={'gl','nl','de'}:raise ValueError('Correction locale scope differs')
    row=data['locales'][tag]['values']['string/'+key]
    if not {'source','source_attributes','previous_target','previous_attributes','attributes','target','display'} <= set(row):raise ValueError('Required reviewed fields absent: '+tag+'/'+key)
    source=ET.parse(catalogues.RES/'values/strings.xml').getroot().find(f"./string[@name='{key}']")
    if source is None or row['source']!=source.text or row['source_attributes']!=source.attrib:raise ValueError('Correction source differs')
    if row['previous_target']!=historical_value or row['previous_attributes']!={'name':key} or row['attributes']!={'name':key}:raise ValueError('Correction predecessor/attributes differ')
    if not isinstance(row['target'],str) or not row['target'] or row['target']==historical_value or row['display']!=display_text(row['target']):raise ValueError('Correction target/display differs')
    return row['target']
