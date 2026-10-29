"""Readable current wording expectations, not a permanent fixture fingerprint.

The checked-in JSON is the reviewable oracle. Load it afresh for caller-owned
comparisons; never derive expected text from the XML under test. Schema,
placeholder and display checks detect independent damage, not coordinated edits
to both an oracle and its implementation. Git review/evidence owns that boundary.
"""
from copy import deepcopy
import json
from pathlib import Path
import re
from translation_catalogues import android_string_errors, format_string_errors, placeholders

ROOT = Path(__file__).resolve().parents[1]
TAGS = ('tt-Latn', 'ain-Latn', 'mn-Mong')
FIXTURE_FIELDS = {'schema_version', 'locale', 'catalogue_path', 'limits',
                  'rows', 'held', 'priority_identities'}
ROW_FIELDS = {'identity', 'type', 'source', 'previous_target', 'reviewed_value',
              'reviewed_display', 'attributes', 'children_attributes', 'decision',
              'compiled_display'}
RESOURCE_FIELDS = {'type', 'attributes', 'value', 'children_attributes'}
QUANTITIES = {'zero', 'one', 'two', 'few', 'many', 'other'}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _keys(value, keys, message):
    _require(isinstance(value, dict) and set(value) == keys, message)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, 'Duplicate JSON member: ' + key)
        result[key] = value
    return result


def decode_display(raw):
    """The bounded escaping used by these fixtures; compiled JVM checks remain required."""
    _require(isinstance(raw, str), 'Non-string display input')
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    else:
        raw = re.sub(r'[ \t\r\n]+', ' ', raw).strip(' \t\r\n')
    return re.sub(r'\\(.)', lambda m: {'n': '\n', 't': '\t', 'r': '\r'}.get(m[1], m[1]), raw)


def _resource(key, resource):
    _keys(resource, RESOURCE_FIELDS, 'Resource fields differ')
    kind, attrs, value = resource['type'], resource['attributes'], resource['value']
    _require(kind in ('string', 'plurals'), 'Unsupported resource kind')
    _require(isinstance(attrs, dict) and attrs.get('name') == key
             and set(attrs) <= {'name', 'formatted'}
             and ('formatted' not in attrs or attrs['formatted'] in ('true', 'false')),
             'Resource attributes differ')
    if kind == 'string':
        _require(isinstance(value, str) and bool(value), 'Empty/non-string scalar')
        _keys(resource['children_attributes'], set(), 'Scalar child attributes')
        values = [value]
    else:
        _require(isinstance(value, dict) and 'other' in value and set(value) <= QUANTITIES,
                 'Plural quantities differ')
        _require(all(isinstance(v, str) and v for v in value.values()), 'Empty/non-string plural')
        _require(resource['children_attributes'] == {q: {'quantity': q} for q in value},
                 'Plural child attributes differ')
        values = value.values()
    for text in values:
        _require(not android_string_errors(text), 'Invalid Android quoting')
        _require(not format_string_errors(text, attrs.get('formatted') != 'false'),
                 'Invalid format syntax')


def _validate_row(key, row):
    _keys(row, ROW_FIELDS, 'Row fields differ')
    _resource(key, expected_row(row))
    _require(row['identity'] == row['type'] + '/' + key, 'Row identity differs')
    _keys(row['source'], {'value', 'attributes', 'child_attributes'}, 'Source fields differ')
    _resource(key, {'type': row['type'], 'value': row['source']['value'],
                   'attributes': row['source']['attributes'],
                   'children_attributes': row['source']['child_attributes']})
    _require(row['decision'] in ('edited', 'retained'), 'Unknown disposition')
    previous = row['previous_target']
    if previous is not None:
        _resource(key, previous)
    if row['decision'] == 'retained':
        _require(previous == expected_row(row), 'Retained value differs from previous value')
    _require(row['reviewed_display'] == row['compiled_display'], 'Display projections differ')
    raw, display = row['reviewed_value'], row['compiled_display']
    if row['type'] == 'string':
        _require(isinstance(display, str) and bool(display), 'Non-string/empty display')
        pairs = [(raw, display, row['source']['value'])]
    else:
        _require(isinstance(display, dict) and set(display) == set(raw), 'Display plural quantities differ')
        pairs = [(text, display[q], row['source']['value'].get(q, row['source']['value']['other']))
                 for q, text in raw.items()]
    for text, shown, source in pairs:
        if not text.startswith('@string/'):
            _require(decode_display(text) == shown, 'Raw/display transformation differs')
        _require(placeholders(shown) == placeholders(source), 'Placeholder index/type/precision differs')


def validate_fixture(tag, data):
    """Validate format and semantics without pinning wording to a second snapshot."""
    _require(tag in TAGS, 'Outside exact locale set')
    _keys(data, FIXTURE_FIELDS, 'Fixture fields differ')
    _require(type(data['schema_version']) is int and data['schema_version'] == 1, 'Unknown schema')
    _require(data['locale'] == tag, 'Fixture locale differs')
    _require(data['catalogue_path'] == 'Paintroid/src/main/res/values-b+' + tag.replace('-', '+') + '/strings.xml',
             'Fixture catalogue path differs')
    _require(isinstance(data['limits'], str) and bool(data['limits']), 'Missing scope limits')
    rows, held, identities = data['rows'], data['held'], data['priority_identities']
    _require(isinstance(rows, dict) and isinstance(held, dict) and rows and held, 'Empty/malformed scope')
    _require(not set(rows) & set(held), 'Accepted/held scope overlaps')
    _require(isinstance(identities, list) and all(isinstance(i, str) for i in identities)
             and len(identities) == len(set(identities)), 'Duplicate/malformed priority identities')
    for key, row in rows.items():
        _validate_row(key, row)
    for key, entry in held.items():
        _keys(entry, {'previous', 'status', 'type', 'compiled_display'}, 'Held fields differ')
        _require(entry['type'] == 'string' and isinstance(entry['compiled_display'], str), 'Held display type differs')
        previous = entry['previous']
        _require(entry['status'] == ('held_absent' if previous is None else 'held_unchanged'), 'Held status differs')
        if previous is not None:
            _resource(key, previous)
            _require(previous['type'] == 'string' and decode_display(previous['value']) == entry['compiled_display'],
                     'Held display differs')
    declared = {row['identity'] for row in rows.values()} | {'string/' + key for key in held}
    _require(set(identities) <= declared, 'Priority identity missing its disposition')
    # Only current fixture references are resolved, never historical snapshots.
    for key, row in rows.items():
        raw = row['reviewed_value']
        if row['type'] == 'string' and raw.startswith('@string/'):
            seen = {key}
            while raw.startswith('@string/'):
                reference = raw[len('@string/'):]
                _require(reference not in seen and reference in rows, 'Unknown/cyclic string reference')
                seen.add(reference)
                target = rows[reference]
                _require(target['type'] == 'string', 'Alias target is not a string')
                raw = target['reviewed_value']
            _require(decode_display(raw) == row['compiled_display'], 'Alias display differs')
    return data


def _read_fixture(tag):
    _require(tag in TAGS, 'Outside exact locale set')
    path = ROOT / 'tools/fixtures/exact_script_priority_wording' / f'{tag}.json'
    return validate_fixture(tag, json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=_unique_object))


def bound_fixture(tag):
    """Return a fresh caller-owned copy of the current readable expectation file."""
    return _read_fixture(tag)


def require_fixture(tag, data):
    validate_fixture(tag, data)
    expected = _read_fixture(tag)
    _require(data['priority_identities'] == expected['priority_identities'], 'Supplied priority scope differs')
    for group in ('rows', 'held'):
        _require(set(data[group]) == set(expected[group]), 'Supplied resource scope differs')
        for key, row in data[group].items():
            _require(row == expected[group][key], f'Supplied {group} value differs: {tag}/{key}')
    return data


def require_row(tag, key, row):
    _validate_row(key, row)
    expected = _read_fixture(tag)['rows']
    _require(key in expected and row == expected[key], 'Supplied reviewed row differs')
    return row


def _has_xml_text(value):
    """Only XML's space/tab/CR/LF count as ignorable structural whitespace."""
    return bool((value or '').strip(' \t\r\n'))


def require_shape(element,expected):
    if element is None or element.tag!=expected['type'] or element.attrib!=expected['attributes'] or _has_xml_text(element.tail):
        raise ValueError('Resource type, attributes or tail differs')
    value=expected['value']
    if element.tag=='string':
        if list(element) or element.text!=value:raise ValueError('Exact scalar value/children differ')
    elif element.tag=='plurals':
        if _has_xml_text(element.text) or len(element)!=len(value):raise ValueError('Plural parent text/size differs')
        quantities=[n.get('quantity') for n in element]
        if len(set(quantities))!=len(quantities) or set(quantities)!=set(value):raise ValueError('Plural quantity set differs')
        for n in element:
            q=n.get('quantity')
            if n.tag!='item' or n.attrib!=expected['children_attributes'][q] or list(n) or _has_xml_text(n.tail) or n.text!=value[q]:
                raise ValueError('Exact plural child differs')
    else:raise ValueError('Unexpected resource kind')

def expected_row(row):return {'type':row['type'],'attributes':row['attributes'],'value':row['reviewed_value'],'children_attributes':row['children_attributes']}
def require_reviewed_resource(tag,key,element,row=None):
    row=bound_fixture(tag)['rows'][key] if row is None else row
    require_row(tag,key,row);require_shape(element,expected_row(row));return element

def require_catalogue(tag,root,data=None):
    """Bind current reviewed/held behavior, not an unrelated historical catalogue."""
    data=bound_fixture(tag) if data is None else require_fixture(tag,data)
    if root.tag!='resources' or root.attrib or _has_xml_text(root.text) or _has_xml_text(root.tail):raise ValueError('Malformed resources root')
    names=[n.get('name') for n in root]
    if any(not name for name in names) or len(set(names))!=len(names):raise ValueError('Resource identities absent or duplicated')
    by_name={n.get('name'):n for n in root}
    # Generic XML integrity does not freeze unrelated values or identity inventories.
    for n in root:
        if _has_xml_text(n.tail):raise ValueError('Nonwhitespace resource tail')
        if n.tag=='string':
            if list(n):raise ValueError('Scalar has children')
        elif n.tag=='plurals':
            quantities=[child.get('quantity') for child in n]
            if _has_xml_text(n.text) or not quantities or any(not q for q in quantities) or len(set(quantities))!=len(quantities):raise ValueError('Malformed plural parent/identities')
            for child in n:
                if child.tag!='item' or list(child) or _has_xml_text(child.tail):raise ValueError('Malformed plural child')
        else:raise ValueError('Unexpected resource kind')
    for key,row in data['rows'].items():
        require_shape(by_name.get(key),expected_row(row))
    for key,held in data['held'].items():
        previous=held['previous']
        if previous is None:
            if key in by_name:raise ValueError('Held absence changed')
        else:require_shape(by_name.get(key),previous)
    return root

def require_source(tag,root,data=None):
    data=bound_fixture(tag) if data is None else require_fixture(tag,data)
    if root.tag!='resources' or root.attrib or _has_xml_text(root.text) or _has_xml_text(root.tail):raise ValueError('Malformed source root')
    for key,row in data['rows'].items():
        nodes=[n for n in root if n.get('name')==key]
        if len(nodes)!=1:raise ValueError('Source identity duplicated or absent')
        source=row['source'];expected={'type':row['type'],'attributes':source['attributes'],'value':source['value'],'children_attributes':source.get('child_attributes',{})}
        require_shape(nodes[0],expected)
    return root

# These are exact family boundaries, not blanket acceptance of the catalogue.
MEMORY_ADDITIONS=frozenset(('tt-Latn',k) for k in ('ui_no_resize_fits_decoder_memory','ui_assembly_source_memory_floor'))
SVG_KEYS=frozenset(('commons_svg_original_size_unavailable','commons_svg_original_size_too_large'))
TAGGED_KEY='save20_unsupported_image_colour'
def require_addition(tag,key,historical,english,already_present=False):
    if not ((tag,key) in MEMORY_ADDITIONS or (tag=='tt-Latn' and key in SVG_KEYS|{TAGGED_KEY})):
        raise ValueError('Outside exact new family pairs')
    row=bound_fixture(tag)['rows'][key]
    require_row(tag,key,row)
    if historical is not None or already_present or row['previous_target'] is not None or row['decision']!='edited':raise ValueError('Exact historical absence differs')
    if row['source']!={'value':english,'attributes':{'name':key},'child_attributes':{}} or row['attributes']!={'name':key} or row['type']!='string':raise ValueError('Whole source or resource shape differs')
    return row

# Exact finite compiled-consumer source boundary.

JVM_PATH='Paintroid/src/test/java/org/catrobat/paintroid/local/ExactScriptPriorityWordingTest.kt'
MAIN_PATH='Paintroid/src/test/java/org/catrobat/paintroid/local/AppLanguageTest.kt'
SAVE_BRANCHES='                "tt-Latn" -> {\n                    assertEquals("Saqlaw",wrapped.getString(R.string.ui_save))\n                    assertEquals("Saqlaw…",wrapped.getString(R.string.ui_save_a5d0d9))\n                }\n'
def require_jvm_source(text):
    # Check consumer wiring only; JVM execution establishes the actual behavior.
    # Do not pin a whole source file or reconstruct a historical class in a permanent test.
    fragments=(
        'assertEquals(tag,data.getString("locale"))',
        'exactScriptSameJson(currentRow(tag,key),supplied)',
        'exactScriptSameJson(current.get(field),supplied.get(field))',
        'return requireRow(tag,key,supplied)',
        'private fun expected(tag: String,key: String)=row(tag,key).getString("compiled_display")',
        'val quantity=if(values.has(selected)) selected else "other"',
        'assertEquals(expected(tag,"ui_fg"),ui(R.string.ui_fg))',
        'assertEquals(expected(tag,"ui_bg"),ui(R.string.ui_bg))',
        'assertEquals("Expected tooltip ownership $tag",vertical,VerticalText.uiVertical(button.context))',
        'assertEquals(description,LocaleTooltip.logicalText(button).toString())',
        'assertTrue("Category button attached $tag",button.isAttachedToWindow)',
        'if(visible) controller.visible().windowFocusChanged(true)',
        'activity.setContentView(button);idle()',
        'categoryAccessibilityTracksEveryActualToolAndExpansionState() = forEachLocale(visible=true)',
        'categoryTooltipChecksRejectCaptionLogicalNativeAndAccessibilityCorruption() = forEachLocale(visible=true)',
        '"detached" -> (button.parent as android.view.ViewGroup).removeView(button)',
        'if(vertical) assertNull("No duplicate native tooltip $tag",button.tooltipText)',
        'else assertEquals(description,button.tooltipText.toString())',
        'assertEquals(description,node.tooltipText.toString())',
        'requireCategoryCaptionAndTooltip(tag,button,ui(category.labelId),description)',
        '@Test fun categoryTooltipChecksRejectCaptionLogicalNativeAndAccessibilityCorruption()',
        '@Test fun readersRejectCallerOwnedCoordinatedRawDisplayAndScopeMutants()',
        '@Test fun cachedRowMutationCannotChangeACompiledExpectation()',
    )
    if any(fragment not in text for fragment in fragments):raise ValueError('Current JVM expectation boundary or consumer missing')
    return text

def require_main_successor(text):
    if text.count(SAVE_BRANCHES)!=1:raise ValueError('Missing or duplicated complete Save branches')
    return text

def require_tagged_jvm_source(text):
    for fragment in ('exactScriptSameJson(current,row)','assertFalse(expected.has(tag));assertTrue(row.isNull("previous_target"))','assertEquals(setOf("tt-Latn"),supplied.keys().asSequence().toSet())','addExactScript(expected,exactScriptExpectations())','assertEquals(140, expected.length())','assertEquals(141, expected.length())','assertEquals(141, expected.length())\n        assertEquals(30, 171 - expected.length())','@Test fun exactScriptTaggedRejectsCoordinatedFixtureAndPredecessorMutations()'):
        if text.count(fragment)!=1:raise ValueError('Finite tagged consumer/binding differs')
    return text


def reviewed_tatar_latin_script_row(historical):
    """Only the exact three-key historical routing row receives this reviewed label."""
    old={'requested_tag':'tt-Latn','resource_tag':'tt-Latn','expected':{
        'ui_save':'Saqlaw','ui_menu_file':'Fayl','language20_device_default':'Use device language'}}
    if historical!=old:raise ValueError('Complete Tatar-Latin historical routing row differs')
    data=bound_fixture('tt-Latn')
    for key in old['expected']:require_row('tt-Latn',key,data['rows'][key])
    for key in ('ui_save','ui_menu_file'):
        if data['rows'][key]['compiled_display']!=old['expected'][key]:raise ValueError('Retained routing label differs')
    row=data['rows']['language20_device_default']
    if row['previous_target'] is not None or row['decision']!='edited' or row['source']!={'value':'Use device language','attributes':{'name':'language20_device_default'},'child_attributes':{}}:
        raise ValueError('Exact device-label source/absence differs')
    result=deepcopy(historical);result['expected']['language20_device_default']=row['compiled_display']
    return result
