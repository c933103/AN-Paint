"""Finite source/target predecessor bindings for reviewed BR/AST/OC values."""
import re,hashlib,json
from current_localization_contracts import fixture
NAME='breton_asturian_occitan_priority_wording.json'
TAGS=frozenset({'br','ast','oc'})
# Bind this compact immutable reviewed fixture, never a whole-source snapshot.
FIXTURE_SHA256='fc5972a3a4c226fc21f902c405067b1102cb35c743bade667dc2a43a6a8645d9'
def require_fixture_binding(data):
    actual=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if actual!=FIXTURE_SHA256:raise ValueError('Complete reviewed fixture binding differs')
    return data

MEMORY_ADDITIONS=frozenset((t,k) for t in TAGS for k in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=TAGS
SVG_ADDITIONS=frozenset((t,k) for t in TAGS for k in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))
def current_row(tag,key):
    if tag not in TAGS:raise ValueError('Outside finite BR/AST/OC set')
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
        if key!='ui_save_a5d0d9' or value!='@string/ui_save':raise ValueError('Unreviewed alias')
        return _display(current_row(tag,'ui_save')['target'])
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
    return row['target']
