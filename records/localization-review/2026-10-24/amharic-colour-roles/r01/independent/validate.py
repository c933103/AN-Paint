"""Read-only integrity and exact-record checks for this review packet."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
source = root / 'input'
sha256 = lambda data: hashlib.sha256(data).hexdigest()
gitblob = lambda data: hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
read = lambda p: json.loads(p.read_text())

assert sha256((source / 'MANIFEST.json').read_bytes()) == 'bedd1144d33e9e54b4edb3e915877ec515f3dd355be7339c29ed203a26667842'
manifest = read(source / 'MANIFEST.json')
assert len(manifest['files']) == 32
for path, digest in manifest['files'].items():
    assert sha256((source / path).read_bytes()) == digest, path
bindings = read(source / 'source-bindings.json')
assert len(bindings) == 12
for path, binding in bindings.items():
    assert gitblob((source / binding['local_complete_copy']).read_bytes()) == binding['git_blob'], path

positive = read(source / 'lexical-evidence/exact-records.json')
excluded = read(source / 'lexical-evidence/excluded-fuzzy-and-other-context-records.json')
assert (len(positive), len(excluded)) == (10, 27)
assert all(r.get('fuzzy') is not True and not r.get('obsolete') for r in positive)
blocks = 0
for record in positive + excluded:
    for part in record.get('pair', {'record': record}).values():
        path = source / 'lexical-evidence' / part.get('file', record.get('file'))
        lines = path.read_text().splitlines()
        actual = '\n'.join(lines[part['line_start'] - 1:part.get('line_end', part['line_start'])])
        assert actual.strip() == part['exact_record'].strip(), record['id']
        assert sha256(part['exact_record'].encode()) == part['record_sha256'], record['id']
        blocks += 1
assert blocks == 39

keys = ['ui_foreground_colour', 'ui_background_colour', 'ui_swap23']
occurrences = []
for path in sorted((source / 'source').rglob('*.kt')):
    for number, line in enumerate(path.read_text().splitlines(), 1):
        for key in keys:
            if re.search(r'R\.string\.' + key + r'\b', line):
                occurrences.append({'key': key, 'path': str(path.relative_to(source / 'source')), 'line': number, 'source_line': line})
sortkey = lambda x: (x['path'], x['line'], x['key'])
expected = read(source / 'direct-consumer-occurrences.json')['occurrences']
assert sorted(occurrences, key=sortkey) == sorted(expected, key=sortkey)
assert len(occurrences) == 6
for key in ['ui_swap_foreground_background', 'ui_edit_foreground']:
    assert not any(re.search(r'R\.string\.' + key + r'\b', p.read_text()) for p in (source / 'source').rglob('*.kt'))

names = []
for locale in ['values', 'values-b+am']:
    resource = ET.parse(source / 'source/Paintroid/src/main/res' / locale / 'strings.xml').getroot()
    names.append({e.attrib.get('name') for e in resource if e.tag in ['string', 'plurals', 'string-array'] and e.attrib.get('translatable') != 'false'})
assert (len(names[0]), len(names[1]), len(names[0] - names[1])) == (717, 12, 705)
assert all(key not in names[1] for key in keys)

extra = root / 'additional-evidence'
retrieval = read(extra / 'retrieval.json')
data = (extra / 'gtk-am-properties.po').read_bytes()
assert gitblob(data) == retrieval['tool_git_blob'] == 'a056ddf20d6af1ad71264d9cae4afda264914671'
assert sha256(data) == retrieval['sha256']
records = read(extra / 'exact-records.json')
assert len(records) == 4
for record in records:
    actual = '\n'.join(data.decode().splitlines()[record['line_start'] - 1:record['line_end']])
    assert actual == record['exact_record']
    assert sha256(actual.encode()) == record['sha256']
    assert '#, fuzzy' not in actual and '#~' not in actual
    assert not record['fuzzy'] and not record['obsolete']

decisions = read(root / 'decisions.json')
assert decisions['outcome'] == {'retain': 2, 'revise': 0, 'hold': 1}
assert [r['key'] for r in decisions['decisions']] == keys
assert [r['value'] for r in decisions['decisions']] == ['የፊት ለፊት ቀለም', 'የመደብ ቀለም', 'ቀለሞችን ያለዋውጡ']
print('PASS: 32 input hashes; 12 source blobs; 39 input lexical blocks; six live references; 717/12/705 counts; new GTK blob and four non-fuzzy records; exact decisions.')
