"""Exact finite review binding and strict resource shapes; not linguistic certification."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as E
from current_localization_contracts import fixture

ROOT=Path(__file__).resolve().parents[1]
FAMILY='tibetan_dzongkha_valencian_priority_wording'
TAGS=('bo', 'dz', 'ca-ES-valencia')
FIXTURE_DIGESTS={'bo': '80168ffc78a88fb3de1ac1a9b0753bfca01bef916633827e88398231c76acd27', 'dz': '031887b9934680ba595fea935ec9aaf89e35bab92e9d66a837d031b78c6e25ed', 'ca-ES-valencia': 'ae8d8cee0386817fcc6a52b0b00abc1abcb720ce288217273243803671310b6d'}
SHARED_KEYS=frozenset({'ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory',
    'commons_svg_original_size_too_large','commons_svg_original_size_unavailable','save20_unsupported_image_colour'})

def require_fixture_binding(tag,data):
    if tag not in TAGS:raise ValueError('Outside exact locale set')
    try:raw=json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    except (TypeError,ValueError) as error:raise ValueError('Malformed review fixture') from error
    if hashlib.sha256(raw).hexdigest()!=FIXTURE_DIGESTS[tag]:raise ValueError('Complete canonical review fixture differs: '+tag)
    return data

def bound_fixture(tag):
    if tag not in TAGS:raise ValueError('Outside exact locale set')
    return require_fixture_binding(tag,fixture(FAMILY+'/'+tag+'.json'))

def require_resource_shape(element,kind,expected):
    if element is None or element.tag!=kind or element.attrib!=expected['attributes']:
        raise ValueError('Exact resource type/attributes differ')
    if (element.tail or '').strip():raise ValueError('Unexpected resource tail')
    if kind=='string':
        if list(element) or element.text!=expected['value']:raise ValueError('Exact child-free string differs')
    elif kind=='plurals':
        values=expected['value'];attrs=expected['children_attributes']
        if (element.text or '').strip() or len(element)!=len(values):raise ValueError('Plural parent text/count differs')
        quantities=[node.get('quantity') for node in element]
        if len(set(quantities))!=len(quantities) or set(quantities)!=set(values):raise ValueError('Exact plural quantity set differs')
        for node in element:
            q=node.get('quantity')
            if node.tag!='item' or node.attrib!=attrs[q] or list(node) or (node.tail or '').strip() or node.text!=values[q]:
                raise ValueError('Exact child-free plural item/attributes/tail differs')
    else:raise ValueError('Unexpected resource type')

def require_edited_resource(tag,key,element,data=None):
    data=bound_fixture(tag) if data is None else require_fixture_binding(tag,data)
    if key not in data['values']:raise ValueError('Outside exact reviewed edit set')
    row=data['values'][key]
    expected={'value':row['reviewed_value'],'attributes':row['reviewed_attributes']}
    if row['type']=='plurals':expected['children_attributes']=row['reviewed_children_attributes']
    require_resource_shape(element,row['type'],expected)

def require_catalogue(tag,root,data=None):
    data=bound_fixture(tag) if data is None else require_fixture_binding(tag,data)
    if root.tag!='resources' or root.attrib or (root.text or '').strip() or (root.tail or '').strip():
        raise ValueError('Malformed resource root')
    expected=set(data['original_catalogue'])|set(data['values'])
    names=[node.get('name') for node in root]
    if len(set(names))!=len(names) or set(names)!=expected:raise ValueError('Exact complete catalogue identity set differs')
    for node in root:
        key=node.get('name')
        if key in data['values']:
            row=data['values'][key];value={'value':row['reviewed_value'],'attributes':row['reviewed_attributes']}
            if row['type']=='plurals':value['children_attributes']=row['reviewed_children_attributes']
            require_resource_shape(node,row['type'],value)
        else:
            old=data['original_catalogue'][key]
            require_resource_shape(node,'plurals' if isinstance(old['value'],dict) else 'string',old)
    return root

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
