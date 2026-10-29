"""Finite Nordic priority forward bindings; original receipts remain immutable."""
from copy import deepcopy
from current_localization_contracts import fixture
NAME = 'nordic_priority_wording.json'
TAGS = frozenset({'da', 'is', 'no'})
MEMORY_ADDITIONS = frozenset({('da','ui_no_resize_fits_decoder_memory'),('no','ui_no_resize_fits_decoder_memory'),('is','ui_no_resize_fits_decoder_memory'),('is','ui_assembly_source_memory_floor')})

def current_row(tag,key):
    if tag not in TAGS: raise ValueError('Outside Nordic locale scope')
    data=fixture(NAME); locale=data['locales'][tag]; source=data['sources'][key]
    if key not in locale['accepted']: raise ValueError('No bounded Nordic value')
    previous=locale['predecessors'].get(key)
    return {'source':source['source'],'target':locale['accepted'][key],
            'attributes':locale['target_attribute_exceptions'].get(key,{'name':key}),
            'previous_target':previous['target'] if previous else None,
            'previous_attributes':previous['attributes'] if previous else None,
            'changed':key in locale['changed']}

def current_value(tag,key,previous,attributes=None):
    if tag not in TAGS:return previous
    locale=fixture(NAME)['locales'][tag]
    if key not in locale['changed'] or key not in locale['predecessors']:return previous
    row=current_row(tag,key)
    if row['previous_target']!=previous or (attributes is not None and row['previous_attributes']!=attributes):
        raise ValueError('Nordic predecessor binding differs: '+tag+'/'+key)
    return row['target']

def current_fixture(name):
    data=deepcopy(fixture(name))
    for key,values in data.get('values',{}).items():
        for tag,value in values.items():
            if tag not in TAGS:continue
            row=current_row(tag,key)
            if row['source']!=values['default']:raise ValueError('Nordic source binding differs')
            values[tag]=current_value(tag,key,value,data['constraints'][key][tag]['attributes'])
    for tag,values in data.get('preserved_values',{}).items():
        for key,row in values.items():row['value']=current_value(tag,key,row['value'],row['attributes'])
    return data

def added_keys(tag):
    locale=fixture(NAME)['locales'][tag]
    return set(locale['changed'])-set(locale['predecessors'])

def display(tag,key):
    import re
    raw=current_row(tag,key)['target']
    if raw.startswith('@string/'):
        if (tag,key,raw)!=('is','ui_save_a5d0d9','@string/ui_save'):raise ValueError('Unexpected alias')
        return display(tag,'ui_save')
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),raw.removeprefix('"').removesuffix('"'))
