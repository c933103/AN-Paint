"""Finite full-value review bindings; never language/native/runtime certification."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
TAGS=('yue-Latn','hak-Latn-TW','nan-Latn-TW')
RAW_DIGESTS={'yue-Latn': '6a46993f9c0d5cbec4f144067185d0bd700dfbc990d025863098f9621afeefcf', 'hak-Latn-TW': 'cd20748b24a8e9dc89cfdaa369f764af374cb3af564a74ab5477c0f1cc6bf3e3', 'nan-Latn-TW': 'e92d9d073906e05cf6a8f3afa4a658b06be914edb0885dacab8515c8ab110bfb'}
CANONICAL_DIGESTS={'yue-Latn': '22d2b6893ebc856214eba7124eb51e21086aa6244df1856e3973df061fce5715', 'hak-Latn-TW': '6620e3c757fd20a1e8bebd253d74dd8f22c0e979369693dcb56612c9b2e77934', 'nan-Latn-TW': 'e87936ef1c8a42f4e6199946534d70b7401eef0e829c3148557172d13cc01b24'}
def canonical(value):
    try:return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    except (TypeError,ValueError) as error:raise ValueError('Malformed review value') from error

def require_fixture(tag,data):
    if tag not in TAGS or hashlib.sha256(canonical(data)).hexdigest()!=CANONICAL_DIGESTS[tag]:
        raise ValueError('Complete immutable locale fixture differs')
    return data

def bound_fixture(tag):
    if tag not in TAGS:raise ValueError('Outside exact locale set')
    raw=(ROOT/'tools/fixtures/latin_sinitic_priority_wording'/f'{tag}.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=RAW_DIGESTS[tag]:raise ValueError('Raw review fixture differs')
    return require_fixture(tag,json.loads(raw))

# Only immutable digests escape initial binding, never the mutable parsed object.
ROW_MEMBERS=frozenset((tag,key,hashlib.sha256(canonical(row)).hexdigest()) for tag in TAGS for key,row in bound_fixture(tag)['rows'].items())
def require_row(tag,key,row):
    if (tag,key,hashlib.sha256(canonical(row)).hexdigest()) not in ROW_MEMBERS:
        raise ValueError('Whole independently reviewed row differs')
    return row

def require_shape(element,expected):
    if element is None or element.tag!=expected['type'] or element.attrib!=expected['attributes'] or (element.tail or '').strip():
        raise ValueError('Resource type, attributes or tail differs')
    value=expected['value']
    if element.tag=='string':
        if list(element) or element.text!=value:raise ValueError('Exact scalar value/children differ')
    elif element.tag=='plurals':
        if (element.text or '').strip() or len(element)!=len(value):raise ValueError('Plural parent text/size differs')
        quantities=[n.get('quantity') for n in element]
        if len(set(quantities))!=len(quantities) or set(quantities)!=set(value):raise ValueError('Plural quantity set differs')
        for n in element:
            q=n.get('quantity')
            if n.tag!='item' or n.attrib!=expected['children_attributes'][q] or list(n) or (n.tail or '').strip() or n.text!=value[q]:
                raise ValueError('Exact plural child differs')
    else:raise ValueError('Unexpected resource kind')

def expected_row(row):return {'type':row['type'],'attributes':row['attributes'],'value':row['reviewed_value'],'children_attributes':row['children_attributes']}
def require_reviewed_resource(tag,key,element,row=None):
    row=bound_fixture(tag)['rows'][key] if row is None else row
    require_row(tag,key,row);require_shape(element,expected_row(row));return element

def require_catalogue(tag,root,data=None):
    data=bound_fixture(tag) if data is None else require_fixture(tag,data)
    if root.tag!='resources' or root.attrib or (root.text or '').strip() or (root.tail or '').strip():raise ValueError('Malformed resources root')
    names=[n.get('name') for n in root]
    if len(set(names))!=len(names) or set(names)!=set(data['original_catalogue']):raise ValueError('Complete catalogue identities differ')
    for n in root:
        key=n.get('name');row=data['rows'].get(key)
        require_shape(n,expected_row(row) if row is not None else data['original_catalogue'][key])
    return root

def require_source(tag,root,data=None):
    data=bound_fixture(tag) if data is None else require_fixture(tag,data)
    if root.tag!='resources' or root.attrib or (root.text or '').strip() or (root.tail or '').strip():raise ValueError('Malformed source root')
    for key,row in data['rows'].items():
        nodes=[n for n in root if n.get('name')==key]
        if len(nodes)!=1:raise ValueError('Source identity duplicated or absent')
        source=row['source'];expected={'type':row['type'],'attributes':source['attributes'],'value':source['value'],'children_attributes':source.get('child_attributes',{})}
        require_shape(nodes[0],expected)
    return root

# Exact finite compiled-consumer source boundary.
JVM_PATH='Paintroid/src/test/java/org/catrobat/paintroid/local/LatinSiniticPriorityWordingTest.kt'
MAIN_PATH='Paintroid/src/test/java/org/catrobat/paintroid/local/AppLanguageTest.kt'
SAVE_BRANCHES='                "yue-Latn" -> {\n                    assertEquals("Cyu5 cyun4",wrapped.getString(R.string.ui_save))\n                    assertEquals("Cyu5 cyun4…",wrapped.getString(R.string.ui_save_a5d0d9))\n                }\n                "hak-Latn-TW" -> {\n                    assertEquals("Pó-sùn",wrapped.getString(R.string.ui_save))\n                    assertEquals("Pó-sùn…",wrapped.getString(R.string.ui_save_a5d0d9))\n                }\n                "nan-Latn-TW" -> {\n                    assertEquals("Pó-chûn",wrapped.getString(R.string.ui_save))\n                    assertEquals("Pó-chûn…",wrapped.getString(R.string.ui_save_a5d0d9))\n                }\n'
def require_jvm_source(text):
    # Inspect the finite immutable-fixture boundary; behavior is exercised by the JVM tests.
    # Do not pin a whole source file or reconstruct a historical class in a permanent test.
    fragments=(
        'assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)',
        'latinSiniticSameJson(JSONObject(boundRows.getValue(tag).getValue(key)),supplied)',
        'latinSiniticSameJson(latinSiniticBoundFixture(tag),supplied)',
        'return requireRow(tag,key,supplied)',
        'private fun expected(tag: String,key: String)=row(tag,key).getString("compiled_display")',
        'val quantity=if(values.has(selected)) selected else "other"',
        'assertEquals(expected(tag,"ui_fg"),ui(R.string.ui_fg))',
        'assertEquals(expected(tag,"ui_bg"),ui(R.string.ui_bg))',
        '@Test fun immutableReadersRejectCoordinatedRawDisplayAndWholeFixtureMutants()',
        '@Test fun cachedRowMutationCannotChangeACompiledExpectation()',
    )
    if any(fragment not in text for fragment in fragments):raise ValueError('Finite immutable JVM boundary or consumer missing')
    for tag,digest in RAW_DIGESTS.items():
        if '"'+tag+'" to "'+digest+'"' not in text:raise ValueError('JVM fixture digest differs')
    return text

def require_main_successor(text):
    if text.count(SAVE_BRANCHES)!=1:raise ValueError('Missing or duplicated complete Save branches')
    return text
