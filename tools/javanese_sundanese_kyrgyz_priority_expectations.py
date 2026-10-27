"""Bounded current expectations; complete original evidence stays on its immutable ref."""
from current_localization_contracts import fixture

NAME='javanese_sundanese_kyrgyz_priority_wording.json'
TAGS=frozenset({'jv','su','ky'})
MEMORY_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=TAGS
SVG_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))


def current_row(tag,key):
    data=fixture(NAME)
    if tag not in TAGS:raise ValueError('Outside exact reviewed locale set')
    locale=data['locales'][tag];source=data['sources'][key]
    if key not in locale['accepted']:raise ValueError('No accepted complete value')
    previous=locale['predecessors'].get(key)
    return {'source':source['source'],'target':locale['accepted'][key],
            'attributes':locale['target_attribute_exceptions'].get(key,{'name':key}),
            'previous_target':previous['target'] if previous else None,
            'previous_attributes':previous['attributes'] if previous else None,
            'changed':key in locale['changed'],'type':source['type']}


def display(tag,key):
    value=current_row(tag,key)['target']
    if isinstance(value,dict):return {quantity:_display(text) for quantity,text in value.items()}
    if value.startswith('@string/'):
        if tag not in ('jv','ky') or (key,value)!=('ui_save_a5d0d9','@string/ui_save'):
            raise ValueError('Only exact inherited Javanese/Kyrgyz Save aliases are accepted')
        return _display(current_row(tag,'ui_save')['target'])
    return _display(value)


def _display(value):
    import re
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),value)


# Finite successor to the original empty Sundanese option; historical fixture stays immutable.
SUNDANESE_OPTION_STATUS='partial-priority-reviewed'

def require_sundanese_option_successor(historical_row, xml):
    import xml.etree.ElementTree as ET
    from language_option_additions import require_untranslated_option
    if (historical_row.get('tag'),historical_row.get('name'),historical_row.get('catalogue')) != (
            'su','Sunda','Paintroid/src/main/res/values-b+su/strings.xml'):
        raise ValueError('Outside exact Sundanese option successor')
    # Preserve the original zero-coverage metadata contract, not an invented old translation.
    require_untranslated_option(historical_row,'<resources/>')
    data=fixture(NAME);locale=data['locales']['su'];accepted=locale['accepted']
    root=ET.fromstring(xml)
    if root.tag!='resources' or root.attrib or (root.text or '').strip():raise ValueError('Malformed current catalogue')
    if len(root)!=349 or {n.tag+'/'+n.get('name','') for n in root}!=set(locale['catalogue_identities']):
        raise ValueError('Exact accepted Sundanese typed identity set differs')
    if len(accepted)!=349 or locale['outside_review']:raise ValueError('Sundanese successor scope differs')
    for node in root:
        key=node.get('name');expected=accepted[key]
        if node.attrib!=locale['target_attribute_exceptions'].get(key,{'name':key}):raise ValueError('Exact target attributes differ')
        if node.tag=='string':
            if list(node) or node.text!=expected:raise ValueError('Exact accepted string differs')
        elif node.tag=='plurals':
            if (len(node)!=len(expected) or any(n.tag!='item' or set(n.attrib)!={'quantity'} or list(n) for n in node)
                    or {n.get('quantity'):n.text for n in node}!=expected):raise ValueError('Exact complete plural differs')
        else:raise ValueError('Unexpected resource type')
    return root
