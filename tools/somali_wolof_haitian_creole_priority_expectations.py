"""Bounded current expectations; complete original evidence stays on its immutable ref."""
from current_localization_contracts import fixture

NAME='somali_wolof_haitian_creole_priority_wording.json'
TAGS=frozenset({'so','wo','ht'})
MEMORY_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=TAGS
SVG_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))


def require_fixture_binding(data):
    import hashlib,json
    digest=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if digest!='2a138467d806a99948d8edfff815ff580fcf4599f821a6cd731bb2e288ed7197':raise ValueError('Complete reviewed trio fixture binding differs')
    return data


def _bound_row(data,tag,key):
    if tag not in TAGS:raise ValueError('Outside exact reviewed locale set')
    locale=data['locales'][tag];source=data['sources'][key]
    if key not in locale['accepted']:raise ValueError('No accepted complete value')
    if key not in locale['previous_targets'] or locale['previous_targets'][key] is not None or key in locale['predecessors']:
        raise ValueError('Every exact addition needs an explicit null predecessor and no prior attributes')
    return {'source':source['source'],'source_attributes':source['attributes'],'target':locale['accepted'][key],
            'attributes':locale['target_attribute_exceptions'].get(key,{'name':key}),
            'previous_target':locale['previous_targets'][key],'previous_attributes':None,
            'changed':key in locale['changed'],'type':source['type']}


def current_row(tag,key):
    return _bound_row(require_fixture_binding(fixture(NAME)),tag,key)


def display_row(row):
    value=row['target']
    if isinstance(value,dict):return {quantity:_display(text) for quantity,text in value.items()}
    if value.startswith('@string/'):raise ValueError('No aliases in exact SO/WO/HT additions')
    return _display(value)


def display(tag,key):
    return display_row(current_row(tag,key))


def require_addition(tag,key,english,historical_value=None,already_present=False,row=None):
    allowed=MEMORY_ADDITIONS|SVG_ADDITIONS|{(tag,'save20_unsupported_image_colour')for tag in TAGS}
    if (tag,key) not in allowed:raise ValueError('Outside exact fifteen family additions')
    if row is None:row=current_row(tag,key)
    bound=_bound_row(require_fixture_binding(fixture(NAME)),tag,key)
    if row!=bound:raise ValueError('Complete current row differs from exact reviewed binding')
    from pathlib import Path
    import xml.etree.ElementTree as ET
    actual=ET.parse(Path(__file__).resolve().parents[1]/'Paintroid/src/main/res/values/strings.xml').find("./string[@name='"+key+"']")
    if actual is None or actual.attrib!={'name':key} or actual.text!=row['source']:raise ValueError('Actual English source/type/attributes differ')
    if (historical_value is not None or already_present or row['previous_target'] is not None or row['previous_attributes'] is not None
            or not row['changed'] or row['type']!='string' or row['source']!=english
            or row['source_attributes']!={'name':key} or row['attributes']!={'name':key}
            or not isinstance(row['target'],str) or not row['target'] or row['target'].startswith('@')):
        raise ValueError('Exact family source/type/attributes/history/addition differs: '+tag+'/'+key)
    return row['target']


def _display(value):
    import re
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return re.sub(r'\\(.)',lambda m:{'n':'\n','t':'\t','r':'\r'}.get(m[1],m[1]),value)





# Three finite successors to existing options, never additions to the picker.
SO_WO_HT_OPTION_TAGS=TAGS
PRIORITY_OPTION_STATUS='partial-priority-reviewed'
FIXTURE_SHA256='cbd9e458561e044f52f6c5c4622574b3f27e72dd50a1b04ec26c3d45494fb836'

def require_priority_option_successor(historical_row,xml):
    import hashlib,json
    from pathlib import Path
    import xml.etree.ElementTree as ET
    from language_option_additions import SECOND_ADDITIONS_PATH, require_untranslated_option
    root_path=Path(__file__).resolve().parents[1]
    tag=historical_row.get('tag')
    if tag not in SO_WO_HT_OPTION_TAGS:raise ValueError('Outside exact Somali/Wolof/Haitian Creole option successors')
    historical=next(r for r in json.loads(SECOND_ADDITIONS_PATH.read_text())['languages'] if r['tag']==tag)
    if historical_row!=historical:raise ValueError('Original complete option row differs')
    require_untranslated_option(historical_row,'<resources/>')
    raw=(root_path/'tools/fixtures/current_localization'/NAME).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=FIXTURE_SHA256:raise ValueError('Complete reviewed trio fixture differs')
    data=json.loads(raw);locale=data['locales'][tag];accepted=locale['accepted'];count={'so':345,'wo':345,'ht':345}[tag]
    if locale['catalogue_path']!=historical['catalogue'] or len(accepted)!=count or locale['outside_review'] or locale['held_present'] or locale['predecessors'] or locale['unchanged_accepted']:
        raise ValueError('Exact empty predecessor successor scope differs')
    if len(locale['changed'])!=count or set(locale['changed'])!=set(accepted) or locale['previous_targets']!={key:None for key in accepted}:
        raise ValueError('Exact additions must bind every explicit null predecessor')
    root=ET.fromstring(xml)
    if root.tag!='resources' or root.attrib or (root.text or '').strip() or (root.tail or '').strip():raise ValueError('Malformed current catalogue')
    if len(root)!=count or {n.tag+'/'+n.get('name','')for n in root}!=set(locale['catalogue_identities']):raise ValueError('Exact accepted typed identity set differs')
    english={node.get('name'):node for node in ET.parse(root_path/'Paintroid/src/main/res/values/strings.xml').getroot()}
    for node in root:
        key=node.get('name');expected=accepted[key];source=data['sources'][key];original=english[key]
        source_value={n.get('quantity'):n.text for n in original} if original.tag=='plurals' else original.text
        if source!={'type':original.tag,'source':source_value,'attributes':original.attrib}:raise ValueError('Complete English source binding differs')
        if node.tag!=source['type'] or node.attrib!=locale['target_attribute_exceptions'].get(key,{'name':key}):raise ValueError('Exact target type or attributes differ')
        if (node.tail or '').strip():raise ValueError('Unexpected resource tail')
        if node.tag=='string':
            if list(node) or node.text!=expected:raise ValueError('Exact accepted string differs')
        elif node.tag=='plurals':
            if ((node.text or '').strip() or len(node)!=len(expected)
                    or any(n.tag!='item' or set(n.attrib)!={'quantity'} or list(n) or (n.tail or '').strip()for n in node)
                    or {n.get('quantity'):n.text for n in node}!=expected):raise ValueError('Exact complete plural differs')
        else:raise ValueError('Unexpected resource type')
    return root
