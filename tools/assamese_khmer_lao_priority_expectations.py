"""Bounded current expectations; complete original evidence stays on its immutable ref."""
from current_localization_contracts import fixture
import priority_cohort_checks as _cohort_checks

NAME='assamese_khmer_lao_priority_wording.json'
TAGS=frozenset({'as','km','lo'})
MEMORY_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=TAGS
SVG_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))


def current_row(tag,key):
    return _cohort_checks.current_row(tag, key, NAME, TAGS, fixture)


def display(tag,key):
    value=current_row(tag,key)['target']
    if isinstance(value,dict):return {quantity:_display(text) for quantity,text in value.items()}
    if value.startswith('@string/'):
        if tag not in ('km','lo') or (key,value)!=('ui_save_a5d0d9','@string/ui_save'):
            raise ValueError('Only exact inherited Khmer/Lao Save aliases are accepted')
        return _display(current_row(tag,'ui_save')['target'])
    return _display(value)


def _display(value):
    import re
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),value)


# Finite successor to the original empty Assamese option; historical fixture stays immutable.
ASSAMESE_OPTION_STATUS='partial-priority-reviewed'

def require_assamese_option_successor(historical_row, xml):
    import xml.etree.ElementTree as ET
    from language_option_additions import require_untranslated_option
    from current_localization_contracts import residual_rows, require_residual_or_previous
    from priority_cohort_checks import require_resource_shape
    if (historical_row.get('tag'),historical_row.get('name'),historical_row.get('catalogue')) != (
            'as','অসমীয়া','Paintroid/src/main/res/values-b+as/strings.xml'):
        raise ValueError('Outside exact Assamese option successor')
    # Preserve the original zero-coverage metadata contract, not an invented old translation.
    require_untranslated_option(historical_row,'<resources/>')
    data=fixture(NAME);locale=data['locales']['as'];accepted=locale['accepted']
    successors={key:row for (tag,key),row in residual_rows().items() if tag=='as'}
    root=ET.fromstring(xml)
    if root.tag!='resources' or root.attrib or (root.text or '').strip():raise ValueError('Malformed current catalogue')
    if len(root)!=349+len(successors) or {n.tag+'/'+n.get('name','') for n in root}!=set(locale['catalogue_identities'])|{'string/'+key for key in successors}:
        raise ValueError('Exact accepted Assamese typed identity set differs')
    if len(accepted)!=349 or locale['outside_review']:raise ValueError('Assamese successor scope differs')
    for node in root:
        key=node.get('name')
        if key in successors:
            row=successors[key];source=data['sources'][key]
            if (key in accepted or row['previous_target'] is not None or source['type']!='string'
                    or row['source']!=source['source'] or row['attributes']!=source['attributes']):
                raise ValueError('Assamese residual source/predecessor differs')
            require_residual_or_previous(root,'as',key)
            require_resource_shape(node,'string',{'value':row['target'],'attributes':row['attributes']})
            continue
        expected=accepted[key]
        if node.attrib!=locale['target_attribute_exceptions'].get(key,{'name':key}):raise ValueError('Exact target attributes differ')
        if node.tag=='string':
            if list(node) or node.text!=expected:raise ValueError('Exact accepted string differs')
        elif node.tag=='plurals':
            if (len(node)!=len(expected) or any(n.tag!='item' or set(n.attrib)!={'quantity'} or list(n) for n in node)
                    or {n.get('quantity'):n.text for n in node}!=expected):raise ValueError('Exact complete plural differs')
        else:raise ValueError('Unexpected resource type')
    return root
