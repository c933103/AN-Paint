"""Exact finite review binding and strict resource shapes; not linguistic certification."""
from pathlib import Path
import priority_cohort_checks as cohort_checks
import xml.etree.ElementTree as E
from current_localization_contracts import fixture

ROOT=Path(__file__).resolve().parents[1]
FAMILY='tibetan_dzongkha_valencian_priority_wording'
TAGS=('bo', 'dz', 'ca-ES-valencia')
FIXTURE_DIGESTS={'bo': '361d8dec09fbcfc24ada5929560eb3cc1faa46bcea72ab6e1890066dde8ff2c9', 'dz': '808ac8fae6095a533e9f7dee8f9935207764934766202cabec542fae2d5d8c2d', 'ca-ES-valencia': '7a1bb1dfaa72a5bb7189deae19dd223efb517b8a139f440440e50f6dc20b1ce8'}
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
    if tag != 'ca-ES-valencia' or key not in SHARED_KEYS:raise ValueError('Outside exact five Valencian family additions')
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


def inherited_held_display(tag, key, previous, parent_root=None, direct_root=None):
    """Exact direct successors precede parent inheritance, without changing historical fixtures."""
    from current_localization_contracts import RESIDUAL_KEYS, residual_rows, require_residual_or_previous
    if tag != 'ca-ES-valencia' or key not in RESIDUAL_KEYS['ca-ES-valencia']:
        return previous
    data = bound_fixture(tag)
    if (key in data['original_catalogue'] or key in data['values']
            or previous != data['held_display'][key]['display']):
        raise ValueError('Exact historical Valencian fallback differs')
    if direct_root is None:
        direct_root = E.parse(ROOT / data['catalogue_path']).getroot()
    direct_row = residual_rows().get((tag,key))
    if direct_row is not None:
        english = E.parse(ROOT / 'Paintroid/src/main/res/values/strings.xml').find(f"./string[@name='{key}']")
        if direct_row['source'] != english.text or direct_row['previous_target'] is not None:
            raise ValueError('Exact direct successor source/predecessor differs')
        nodes=direct_root.findall(f"./*[@name='{key}']")
        if len(nodes)!=1:raise ValueError('Exact direct successor identity differs')
        require_resource_shape(nodes[0], 'string', {'value':direct_row['target'], 'attributes':direct_row['attributes']})
        require_residual_or_previous(direct_root,tag,key)
        return decode_android(direct_row['target'])
    if direct_root.findall(f"./*[@name='{key}']"):
        raise ValueError('Inherited Catalan successor must remain directly absent in Valencian')
    row = residual_rows()[('ca', key)]
    if row['source'] != previous:
        raise ValueError('Exact Catalan parent fallback predecessor differs')
    if parent_root is None:
        parent_root = E.parse(ROOT / 'Paintroid/src/main/res/values-ca/strings.xml').getroot()
    raw = require_residual_or_previous(parent_root, 'ca', key)
    require_resource_shape(parent_root.find(f"./string[@name='{key}']"), 'string',
                           {'value': row['target'], 'attributes': row['attributes']})
    return decode_android(raw)


def current_sampled_modality_value(tag,historical):
    if tag != 'bo':return historical
    key='ui_sampled_resize_memory_explanation'
    data=bound_fixture(tag);row=data['values'][key]
    if row['previous_target']!={'value':historical,'attributes':{'name':key}}:
        raise ValueError('Exact historical Tibetan sampled-warning predecessor differs')
    actual=E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').find("./string[@name='"+key+"']")
    if row['source']!={'value':actual.text,'attributes':dict(actual.attrib)} or row['reviewed_attributes']!={'name':key} or row['type']!='string':
        raise ValueError('Sampled warning complete source/shape differs')
    return row['reviewed_value']
