"""Bounded current expectations; complete original evidence stays on its immutable ref."""
from current_localization_contracts import fixture

NAME='yoruba_zulu_xhosa_priority_wording.json'
TAGS=frozenset({'yo','zu','xh'})
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
    if value.startswith('@string/'):raise ValueError('No aliases in exact HA/IG/LN additions')
    return _display(value)


def _display(value):
    import re
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),value)




# Two exact empty-option successors; Xhosa is an inherited catalogue, not a new option.
YO_ZU_OPTION_TAGS=frozenset({'yo','zu'})
# Finite current successors; the original zero-coverage language-option fixture remains immutable.
PRIORITY_OPTION_STATUS='partial-priority-reviewed'

def require_priority_option_successor(historical_row,xml):
    import xml.etree.ElementTree as ET
    from language_option_additions import require_untranslated_option
    tag=historical_row.get('tag')
    names={'yo':'Yorùbá','zu':'isiZulu'}
    if tag not in YO_ZU_OPTION_TAGS or historical_row.get('name')!=names[tag] or historical_row.get('catalogue')!=f'Paintroid/src/main/res/values-b+{tag}/strings.xml':
        raise ValueError('Outside exact Yoruba/Zulu option successors')
    require_untranslated_option(historical_row,'<resources/>')
    locale=fixture(NAME)['locales'][tag];accepted=locale['accepted'];root=ET.fromstring(xml)
    if root.tag!='resources' or root.attrib or (root.text or '').strip():raise ValueError('Malformed current catalogue')
    if len(root)!=346 or {n.tag+'/'+n.get('name','')for n in root}!=set(locale['catalogue_identities']):raise ValueError('Exact accepted typed identity set differs')
    if len(accepted)!=346 or locale['outside_review']:raise ValueError('Exact empty predecessor successor scope differs')
    for node in root:
        key=node.get('name');expected=accepted[key]
        if node.attrib!=locale['target_attribute_exceptions'].get(key,{'name':key}):raise ValueError('Exact target attributes differ')
        if node.tag=='string':
            if list(node) or node.text!=expected:raise ValueError('Exact accepted string differs')
        elif node.tag=='plurals':
            if len(node)!=len(expected) or any(n.tag!='item' or set(n.attrib)!={'quantity'} or list(n)for n in node) or {n.get('quantity'):n.text for n in node}!=expected:raise ValueError('Exact complete plural differs')
        else:raise ValueError('Unexpected resource type')
    return root
