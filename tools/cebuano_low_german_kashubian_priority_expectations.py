"""Exact finite review binding and strict resource shapes; not linguistic certification."""
from pathlib import Path
import priority_cohort_checks as cohort_checks
import xml.etree.ElementTree as E
from current_localization_contracts import fixture

ROOT=Path(__file__).resolve().parents[1]
FAMILY='cebuano_low_german_kashubian_priority_wording'
TAGS=('ceb', 'nds', 'csb')
FIXTURE_DIGESTS={'ceb': 'f71850668bfbdd33fd1e65a7c05f5897c8256873d8e96e902a94a96d3e49196b', 'nds': '931b1a5c138f9099330a12aabe63941c47e317abc5d3e11c53848106990fdb8b', 'csb': '3671cbda287487e385e75cd40368588fa895d3aab99de30d7a8e57666cdc5de5'}
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
    if tag not in ('nds','csb') or key not in SHARED_KEYS:raise ValueError('Outside exact ten NDS/CSB family additions')
    data=bound_fixture(tag) if data is None else require_fixture_binding(tag,data)
    row=data['values'][key]
    actual=E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').find("./string[@name='"+key+"']")
    if actual is None or actual.attrib!={'name':key} or list(actual) or row['source']!={'value':actual.text,'attributes':dict(actual.attrib)}:
        raise ValueError('Actual English source/type/attributes differ')
    if (historical_value is not None or already_present or 'previous_target' not in row or row['previous_target'] is not None
            or row['type']!='string' or row['reviewed_attributes']!={'name':key}):
        raise ValueError('Finite addition type/history/attributes differ')
    raw=row['reviewed_value']
    if not isinstance(raw,str) or row['display']!=decode_android(raw):raise ValueError('Exact finite raw/display binding differs')
    return row


def decode_android(raw):
    import re
    if raw.startswith('"') and raw.endswith('"'):raw=raw[1:-1]
    else:raw=re.sub(r'\s+',' ',raw).strip()
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),raw)
