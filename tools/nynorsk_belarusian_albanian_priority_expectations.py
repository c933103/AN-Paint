"""Finite prior-reviewed NN/BE/SQ integration; historical receipts stay immutable."""
from copy import deepcopy
from current_localization_contracts import fixture
import translation_catalogues as cat
import xml.etree.ElementTree as ET
NAME='nynorsk_belarusian_albanian_priority_wording.json'
TAGS=frozenset({'nn','be','sq'})
MEMORY_ADDITIONS=frozenset({('nn','ui_no_resize_fits_decoder_memory')}|{(t,k)for t in ('be','sq')for k in ('ui_no_resize_fits_decoder_memory','ui_assembly_source_memory_floor')})
COLOUR_TAGS=frozenset({'be','sq'})
def current_row(tag,key):
    if tag not in TAGS:raise ValueError('Outside exact trio')
    d=fixture(NAME);loc=d['locales'][tag];identity='string/'+key;src=d['sources'][identity]
    if key not in loc['accepted']:raise ValueError('Not an accepted scalar')
    old=loc['predecessors'].get(identity)
    return {'changed':identity in loc['changed'],'source':src['source'],'source_attributes':src['attributes'],'target':loc['accepted'][key],
            'attributes':loc['target_attribute_exceptions'].get(key,{'name':key}),
            'previous_target':None if old is None else old['target'],
            'previous_attributes':None if old is None else old['attributes']}
def require_addition(tag,key):
    if (tag,key)not in MEMORY_ADDITIONS|{(t,'save20_unsupported_image_colour')for t in COLOUR_TAGS}|{(t,k)for t in TAGS for k in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable')}:raise ValueError('Outside finite shared additions')
    r=current_row(tag,key);node=ET.parse(cat.RES/'values/strings.xml').getroot().find(f"./string[@name='{key}']")
    if node is None or (node.text,node.attrib)!=(r['source'],r['source_attributes']):raise ValueError('English source differs')
    if r['previous_target']is not None or r['previous_attributes']is not None or r['attributes']!={'name':key}:raise ValueError('Expected exact prior absence and scalar identity')
    return r
def current_value(tag,key,previous,attributes=None):
    if tag not in TAGS:return previous
    l=fixture(NAME)['locales'][tag];i='string/'+key
    if i not in l['changed']or i not in l['predecessors']:return previous
    r=current_row(tag,key)
    if previous!=r['previous_target']or(attributes is not None and attributes!=r['previous_attributes']):raise ValueError('Exact predecessor differs')
    return r['target']
def current_fixture(name):
    d=deepcopy(fixture(name))
    if name not in ('nynorsk_p0_remaining_wording.json','nynorsk_save_wording.json'):raise ValueError('Outside two historical fixtures')
    for k,v in d['values'].items():
        r=current_row('nn',k)
        if v['default']!=r['source']:raise ValueError('English predecessor differs')
        v['nn']=current_value('nn',k,v['nn'],d['constraints'][k]['nn']['attributes'])
    for k,r in d.get('preserved_values',{}).items():r['value']=current_value('nn',k,r['value'],r['attributes'])
    return d
def added_keys(tag):
    l=fixture(NAME)['locales'][tag];return {i.split('/')[1]for i in l['changed']if i not in l['predecessors']}
COMPILED_WHITESPACE = {
    ('sq','ui_new_image'): ('Imazh i ri ', 'Imazh i ri'),
    ('sq','ui_watercolor'): ('Akuarel ', 'Akuarel'),
}
def compiled_display(tag,key,value):
    import re
    if (tag,key) in COMPILED_WHITESPACE:
        raw,compiled=COMPILED_WHITESPACE[(tag,key)]
        if value!=raw:raise ValueError('Exact inherited unquoted whitespace binding differs')
        return compiled
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),value.removeprefix('"').removesuffix('"'))
def display(tag,key):
    value=current_row(tag,key)['target']
    if value.startswith('@string/'):
        if key!='ui_save_a5d0d9'or value!='@string/ui_save':raise ValueError('Unreviewed alias')
        return display(tag,'ui_save')
    return compiled_display(tag,key,value)
