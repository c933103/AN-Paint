"""Exact finite review binding and strict resource shapes; not linguistic certification."""
from pathlib import Path
import priority_cohort_checks as cohort_checks
import xml.etree.ElementTree as E
from current_localization_contracts import fixture

ROOT=Path(__file__).resolve().parents[1]
FAMILY='basque_frisian_uzbek_priority_wording'
TAGS=('eu-ES', 'fy', 'uz-Latn')
FIXTURE_DIGESTS={'eu-ES': '2519ddf5bfb67095b94a23df600e4d34d82aea7491ed5325f08a417f530f0a89', 'fy': '51b14daba8464bb861e79f1de856d6629f6ece9903c8e0a38a3f9d44513a2b2d', 'uz-Latn': '2dc82f3f2c33c57fd86d227981183a940991c6fe6d2dc067620623388a7efa17'}
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
    if (not isinstance(raw,str) or not raw.startswith('"') or not raw.endswith('"') or chr(92) in raw[1:-1]
            or row['display']!=raw[1:-1]):raise ValueError('Exact finite raw/display binding differs')
    return row


def reviewed_uzbek_script_row(row,data=None):
    """One reviewed addition replaces one historical English-fallback oracle."""
    old={'requested_tag':'uz-Latn','resource_tag':'uz-Latn','expected':{
        'ui_save':'Saqlash','ui_menu_file':'Fayl','language20_device_default':'Use device language'}}
    if row!=old:raise ValueError('Exact historical Uzbek routing row differs')
    data=bound_fixture('uz-Latn') if data is None else require_fixture_binding('uz-Latn',data)
    value=data['values']['language20_device_default']
    if (value['type']!='string' or 'previous_target' not in value or value['previous_target'] is not None
            or value['source']!={'value':'Use device language','attributes':{'name':'language20_device_default'}}
            or value['reviewed_attributes']!={'name':'language20_device_default'}
            or value['reviewed_value']!='"Qurilma tilidan foydalanish"'
            or value['display']!='Qurilma tilidan foydalanish'):
        raise ValueError('Exact reviewed Uzbek device-label addition differs')
    actual=E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').find("./string[@name='language20_device_default']")
    require_resource_shape(actual,'string',value['source'])
    return dict(row,expected=dict(row['expected'],language20_device_default=value['display']))
