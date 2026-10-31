"""Finite source/target predecessor bindings for reviewed ARY/MN/TOK values."""
import re,hashlib,json
from current_localization_contracts import fixture
NAME='moroccan_arabic_mongolian_toki_pona_priority_wording.json'
TAGS=frozenset({'ary','mn-Cyrl-MN','tok'})
ADDITION_TAGS=frozenset({'ary','tok'})
# MN existing family values remain on their exact historical bindings.
# Bind this compact immutable reviewed fixture, never a whole-source snapshot.
FIXTURE_SHA256='72b601aea75611f744bde3549209e3803d74675f6222b2699cb30f6adcf9213c'
def require_fixture_binding(data):
    actual=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if actual!=FIXTURE_SHA256:raise ValueError('Complete reviewed fixture binding differs')
    return data

MEMORY_ADDITIONS=frozenset((t,k) for t in ADDITION_TAGS for k in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=ADDITION_TAGS
SVG_ADDITIONS=frozenset((t,k) for t in ADDITION_TAGS for k in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))
def current_row(tag,key):
    if tag not in TAGS:raise ValueError('Outside finite ARY/MN/TOK set')
    data=require_fixture_binding(fixture(NAME));locale=data['locales'][tag]
    if key not in locale['accepted']:raise ValueError('No accepted current value')
    source=data['sources'][key];previous=locale['predecessors'].get(key)
    return {'source':source['source'],'source_attributes':source['attributes'],'target':locale['accepted'][key],
            'attributes':locale['target_attribute_exceptions'].get(key,{'name':key}),
            'previous_target':previous['target'] if previous else None,
            'previous_attributes':previous['attributes'] if previous else None,
            'type':source['type'],'changed':key in locale['changed']}
def _display(value):
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return re.sub(r'\\(u[0-9a-fA-F]{4}|.)',lambda m:chr(int(m[1][1:],16)) if m[1].startswith('u') else {'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),value)
def display(tag,key):
    value=current_row(tag,key)['target']
    if isinstance(value,dict):return {q:_display(v)for q,v in value.items()}
    if value.startswith('@string/'):
        if (tag,key,value)!=('mn-Cyrl-MN','ui_draw26','@string/ui_drawing23'):raise ValueError('Unreviewed alias')
        return _display(current_row(tag,'ui_drawing23')['target'])
    return _display(value)


def require_addition(tag,key,english,historical_value=None,already_present=False):
    allowed=MEMORY_ADDITIONS|SVG_ADDITIONS|{(t,'save20_unsupported_image_colour')for t in TAGGED_ADDITIONS}
    if (tag,key) not in allowed:raise ValueError('Outside finite family addition')
    row=current_row(tag,key)
    if historical_value is not None or already_present or row['previous_target'] is not None or row['previous_attributes'] is not None:
        raise ValueError('Historical family addition must be absent: '+tag+'/'+key)
    if (not row['changed'] or row['type']!='string' or row['source']!=english or row['source_attributes']!={'name':key} or row['attributes']!={'name':key}
            or not isinstance(row['target'],str) or not row['target'] or row['target'].startswith('@')):
        raise ValueError('Exact family source/type/attributes/addition differs: '+tag+'/'+key)
    from current_localization_contracts import residual_rows
    successor=residual_rows().get((tag,key))
    if successor is not None:
        if successor['previous_target']!=row['target'] or successor['source']!=english or successor['attributes']!=row['attributes']:raise ValueError('Exact family successor differs')
        return successor['target']
    return row['target']


def reviewed_mongolian_script_row(row,data=None):
    """Exact accepted MN action label succeeds one immutable historical routing row."""
    old={'requested_tag':'mn-Cyrl-MN','resource_tag':'mn-Cyrl-MN','expected':{
        'ui_save':'Хадгалах','ui_menu_file':'Файл','language20_device_default':'Төхөөрөмжийн хэл'}}
    if row!=old:raise ValueError('Exact historical Mongolian routing row differs')
    data=require_fixture_binding(fixture(NAME) if data is None else data)
    key='language20_device_default';locale=data['locales']['mn-Cyrl-MN']
    source={'type':'string','source':'Use device language','attributes':{'name':key}}
    previous={'type':'string','target':'Төхөөрөмжийн хэл','attributes':{'name':key}}
    if (data['sources'][key]!=source or locale['predecessors'][key]!=previous
            or locale['accepted'][key]!='Төхөөрөмжийн хэлийг ашиглах'
            or key not in locale['changed'] or key in locale['target_attribute_exceptions']):
        raise ValueError('Exact reviewed Mongolian device action differs')
    from pathlib import Path
    import xml.etree.ElementTree as E
    node=E.parse(Path(__file__).resolve().parents[1]/'Paintroid/src/main/res/values/strings.xml').find("./string[@name='"+key+"']")
    if node is None or node.attrib!=source['attributes'] or node.text!=source['source'] or len(node):
        raise ValueError('Current English device-language source differs')
    return dict(row,expected=dict(row['expected'],language20_device_default=locale['accepted'][key]))
