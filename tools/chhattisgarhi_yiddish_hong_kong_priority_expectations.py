"""Exact finite review binding and strict resource shapes; not linguistic certification."""
from pathlib import Path
import priority_cohort_checks as cohort_checks
import xml.etree.ElementTree as E
from current_localization_contracts import fixture

ROOT=Path(__file__).resolve().parents[1]
FAMILY='chhattisgarhi_yiddish_hong_kong_priority_wording'
TAGS=('hne', 'yi', 'zh-HK')
FIXTURE_DIGESTS={'hne': '4a9e73f5deaef33414aa3f20b8cfd40a8483439114d84198ea0db9360e2b7460', 'yi': '7db4fa3eea530afc621ef96f3e8867f22c8c29a018a8e68e0ceb6f946b3c26de', 'zh-HK': 'd251030aed22110f057a75cc955e42892e278b7f08abf5c6bb1673bb6027e776'}
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
    if tag not in ('hne', 'yi') or key not in SHARED_KEYS:raise ValueError('Outside exact ten HNE/YI family additions')
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

