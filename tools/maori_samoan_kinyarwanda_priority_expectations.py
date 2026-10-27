"""Finite reviewed missing-value additions, not a general preservation bypass."""
import xml.etree.ElementTree as ET
import hashlib,json
from current_localization_contracts import fixture
import translation_catalogues as catalogues

NAME='maori_samoan_kinyarwanda_priority_wording.json'
TAGS=frozenset({'mi','sm','rw'})
# Exact finite reviewed fixture, not a whole-source snapshot.
FIXTURE_SHA256='3bad4326747611f24aaa263ac16c4c354f842e3e77ff6f3807cdb1fc674da77b'
def require_fixture_binding(data):
    actual=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if actual!=FIXTURE_SHA256:raise ValueError('Complete reviewed fixture binding differs')
    return data

MEMORY_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory'))
TAGGED_ADDITIONS=frozenset((tag,'save20_unsupported_image_colour') for tag in TAGS)
SVG_ADDITIONS=frozenset((tag,key) for tag in TAGS for key in ('commons_svg_original_size_too_large','commons_svg_original_size_unavailable'))
ADDITIONS=MEMORY_ADDITIONS|TAGGED_ADDITIONS|SVG_ADDITIONS


def current_row(tag,key):
    if (tag,key) not in ADDITIONS:raise ValueError('Outside exact reviewed addition set')
    data=require_fixture_binding(fixture(NAME))
    if set(data['locales'])!={'mi','sm','rw'}:raise ValueError('Exact three-locale fixture scope differs')
    row=data['locales'][tag]['values']['string/'+key]
    if not {'source','source_attributes','previous_target','previous_attributes','attributes','target','display'} <= set(row):raise ValueError('Required reviewed fields absent: '+tag+'/'+key)
    source=ET.parse(catalogues.RES/'values/strings.xml').getroot().find(f"./string[@name='{key}']")
    if source is None or row['source']!=source.text or row['source_attributes']!=source.attrib:
        raise ValueError('Complete reviewed English source differs: '+tag+'/'+key)
    if row['previous_target'] is not None or row['previous_attributes'] is not None or row['attributes']!={'name':key}:
        raise ValueError('Reviewed addition requires exact historical absence: '+tag+'/'+key)
    if not isinstance(row['target'],str) or not row['target'] or row['display']!=display_text(row['target']):
        raise ValueError('Complete reviewed target/display differs: '+tag+'/'+key)
    return row


def display_text(value):
    if value.startswith('"') and value.endswith('"'):value=value[1:-1]
    return value.replace(r'\n','\n').replace(r"\'", "'").replace(r'\"','"')


def display(tag,key):return current_row(tag,key)['display']


def require_empty_option_successor(historical_row, xml):
    from language_option_additions import SECOND_ADDITIONS_PATH, require_untranslated_option
    tag=historical_row.get('tag')
    if tag not in {'mi','sm'}:raise ValueError('Outside exact MI/SM empty-option successor')
    old=next(r for r in json.loads(SECOND_ADDITIONS_PATH.read_text())['languages'] if r['tag']==tag)
    if historical_row!=old:raise ValueError('Historical option metadata differs')
    require_untranslated_option(historical_row,'<resources/>')
    loc=require_fixture_binding(fixture(NAME))['locales'][tag]
    if loc['context'] or len(loc['values'])!=348:raise ValueError('Exact empty predecessor scope differs')
    root=ET.fromstring(xml)
    if root.tag!='resources' or root.attrib or (root.text or '').strip():raise ValueError('Malformed catalogue')
    identities=[n.tag+'/'+n.get('name','') for n in root]
    if len(identities)!=len(set(identities)) or set(identities)!=set(loc['values']):raise ValueError('Exact accepted identity set differs')
    for node in root:
        row=loc['values'][node.tag+'/'+node.get('name')]
        if row['previous_target'] is not None or row['previous_attributes'] is not None:raise ValueError('Exact absence differs')
        if node.attrib!=row['attributes'] or (node.tail or '').strip():raise ValueError('Exact attributes/tail differ')
        if node.tag=='string':
            if list(node) or node.text!=row['target']:raise ValueError('Complete string differs')
        elif node.tag=='plurals':
            target=row['target']
            if (node.text or '').strip() or len(node)!=len(target):raise ValueError('Complete plural differs')
            if {n.get('quantity') for n in node}!=set(target):raise ValueError('Quantity set differs')
            for child in node:
                q=child.get('quantity')
                if child.tag!='item' or child.attrib!={'quantity':q} or list(child) or (child.tail or '').strip() or child.text!=target[q]:raise ValueError('Complete plural child differs')
        else:raise ValueError('Unexpected type')
    return root
