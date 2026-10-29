"""Exact finite review binding and strict resource shapes; not linguistic certification."""
from pathlib import Path
import priority_cohort_checks as cohort_checks
import xml.etree.ElementTree as E
from current_localization_contracts import fixture

ROOT=Path(__file__).resolve().parents[1]
FAMILY='sindhi_nigerian_pidgin_tok_pisin_priority_wording'
TAGS=('sd', 'pcm', 'tpi')
FIXTURE_DIGESTS={'sd': '0dacb4cb426395ffc642334864f436d30539ec756e88ce713135f78fbda7be4a', 'pcm': '352b5a36fd6458f0d8bcc8b6c70a865c03f2f0878fb9c1b26877516197ca1172', 'tpi': 'dea5e76a084fba9ff5edcbefb9d1478d5329d9a03c7be2d0f047a05d0aa22417'}
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
