"""Exact finite review binding and strict resource shapes; not linguistic certification."""
from pathlib import Path
import priority_cohort_checks as cohort_checks
import xml.etree.ElementTree as E
from current_localization_contracts import fixture

ROOT=Path(__file__).resolve().parents[1]
FAMILY='sorani_uyghur_tatar_priority_wording'
TAGS=('ckb', 'ug', 'tt-Cyrl')
FIXTURE_DIGESTS={'ckb': 'ee3f601926b06c8e050e6500b7222ea26407e754601ef994d51a5a6056a0e519', 'ug': '8b25a0b4ac3dc1e1090362c8bbe326c3c3125713373b89f081a9a49004c6225d', 'tt-Cyrl': '2cf0a4a9e846004da633e19479a8614c572435aa355d668e2d004edbec7283d1'}
SHARED_KEYS=frozenset({'ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory',
    'commons_svg_original_size_too_large','commons_svg_original_size_unavailable','save20_unsupported_image_colour'})

def require_fixture_binding(tag,data):
    return cohort_checks.require_fixture_binding(tag, data, TAGS, FIXTURE_DIGESTS)

def bound_fixture(tag):
    return cohort_checks.bound_fixture(tag, TAGS, FAMILY, fixture, require_fixture_binding)

def require_resource_shape(element,kind,expected):
    return cohort_checks.require_resource_shape(element, kind, expected)

def require_edited_resource(tag,key,element,data=None):
    return cohort_checks.require_edited_resource(tag, key, element, data, bound_fixture, require_fixture_binding, require_resource_shape)

def require_catalogue(tag,root,data=None):
    return cohort_checks.require_catalogue(tag, root, data, bound_fixture, require_fixture_binding, require_resource_shape)

def require_shared_row(tag,key,data=None,historical_value=None,already_present=False):
    if tag not in TAGS or key not in SHARED_KEYS:raise ValueError('Outside exact fifteen family additions')
    data=bound_fixture(tag) if data is None else require_fixture_binding(tag,data)
    row=data['values'][key]
    actual=E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').find("./string[@name='"+key+"']")
    if actual is None or actual.attrib!={'name':key} or list(actual) or row['source']!={'value':actual.text,'attributes':dict(actual.attrib)}:
        raise ValueError('Actual English source/type/attributes differ')
    if (historical_value is not None or already_present or 'previous_target' not in row or row['previous_target'] is not None
            or row['type']!='string' or row['reviewed_attributes']!={'name':key}):
        raise ValueError('Finite addition type/history/attributes differ')
    raw=row['reviewed_value']
    if not isinstance(raw,str) or chr(92) in raw or raw.startswith(chr(34)) or raw.endswith(chr(34)) or row['display']!=raw:
        raise ValueError('Exact finite unquoted raw/display binding differs')
    return row


def reviewed_tatar_script_row(row,data=None):
    """One reviewed addition replaces one historical English-fallback oracle."""
    old={'requested_tag':'tt-Cyrl','resource_tag':'tt-Cyrl','expected':{
        'ui_save':'Саклау','ui_menu_file':'Файл','language20_device_default':'Use device language'}}
    if row!=old:raise ValueError('Exact historical Tatar routing row differs')
    data=bound_fixture('tt-Cyrl') if data is None else require_fixture_binding('tt-Cyrl',data)
    value=data['values']['language20_device_default']
    if (value['type']!='string' or 'previous_target' not in value or value['previous_target'] is not None
            or value['source']!={'value':'Use device language','attributes':{'name':'language20_device_default'}}
            or value['reviewed_attributes']!={'name':'language20_device_default'}
            or value['reviewed_value']!='Җайланма телен куллану'
            or value['display']!='Җайланма телен куллану'):
        raise ValueError('Exact reviewed Tatar device-label addition differs')
    actual=E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').find("./string[@name='language20_device_default']")
    require_resource_shape(actual,'string',value['source'])
    return dict(row,expected=dict(row['expected'],language20_device_default=value['display']))
