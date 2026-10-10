#!/usr/bin/env python3
"""Reproduce source extraction/hashes for the explicitly reviewed P07-008 scope.

Human semantic judgments are inputs in review-data.json; this script never derives
linguistic acceptance from byte equality, resource coverage, or script ranges.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '80c14372b0504bc44f9f2809ad477247fdc8100b'
RES = ROOT / 'Paintroid/src/main/res'
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
rows = json.loads((HERE / 'review-data.json').read_text())

def catalogue(folder):
    path = RES / folder / 'strings.xml'
    nodes = ET.parse(path).getroot()
    values = {n.get('name'): ''.join(n.itertext()) for n in nodes if n.tag == 'string'}
    lines = {m.group(1): number for number, line in enumerate(path.read_text().splitlines(), 1)
             if (m := re.search(r'<string name="([^"]+)"', line))}
    return path, nodes, values, lines

en_path, en_nodes, en, en_lines = catalogue('values')
br_path, br_nodes, br, br_lines = catalogue("values-pt-rBR")

def link(path, lines):
    return f'https://github.com/c933103/AN-Paint/blob/{BASE}/{path.relative_to(ROOT)}#L' + lines.replace('-', '-L')

inputs = {en_path, br_path}
occurrences = []
for identifier, key, surface, refs, judgment in rows:
    sources = []
    for ref in refs.split(';'):
        filename, lines = ref.split(':')
        path = JAVA / filename
        assert path.exists(), path
        inputs.add(path)
        sources.append(link(path, lines))
    occurrences.append(dict(id=identifier, resource_id=key, surface=surface,
                            english=en[key], portuguese=br[key],
                            english_source=link(en_path, str(en_lines[key])),
                            portuguese_source=link(br_path, str(br_lines[key])),
                            operation_sources=' ; '.join(sources), judgment=judgment))
with (HERE / 'occurrences.tsv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(occurrences[0]), delimiter='\t', lineterminator='\n')
    writer.writeheader(); writer.writerows(occurrences)

# Record every default-catalogue lexical candidate, including excluded file-copy
# and crop operations, so searching only the literal word clipboard is detectable.
pattern = re.compile(r'\b(?:copy|copies|copied|cut|paste|clipboard)\b', re.I)
lexical = [{'resource_id': k, 'in_occurrences': any(x['resource_id'] == k for x in occurrences),
            'english_source': link(en_path, str(en_lines[k]))} for k, v in en.items() if pattern.search(v)]
consumer_keys = ['ui_copy_an_area_or_use_file_insert_image', 'ui_the_arrow_on_the_left_directly_below_the']
retained_consumers = {key: [] for key in consumer_keys}
for path in (ROOT / 'Paintroid/src/main').rglob('*'):
    if path.suffix not in ('.kt', '.java', '.xml', '.html', '.js') or not path.is_file():
        continue
    if 'res' in path.parts and any(part.startswith('values') for part in path.parts):
        continue
    content = path.read_text()
    for key in consumer_keys:
        if key in content:
            retained_consumers[key].append(str(path.relative_to(ROOT)))
results = {'base_commit': BASE, 'base_tree': 'd9858229f98068bef9c6194c90d77610c5ecceec',
           'scope': 'P07-008 clipboard terminology and directly associated UI/error/help contexts only',
           'counts': {folder: {'translatable_strings': sum(n.tag == 'string' and n.get('translatable') != 'false' for n in nodes),
                              'plurals': sum(n.tag == 'plurals' for n in nodes)}
                      for folder, nodes in [('values', en_nodes), ('values-pt-rBR', br_nodes)]},
           'occurrence_count': len(occurrences),
           'unique_resource_count': len({r['resource_id'] for r in occurrences}),
           'default_lexical_candidates': lexical, 'retained_resource_production_consumers': retained_consumers,
           'inputs': [{'path': str(path.relative_to(ROOT)),
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'git_blob_sha1': hashlib.sha1(b'blob ' + str(len(path.read_bytes())).encode() + b'\0' + path.read_bytes()).hexdigest()}
                      for path in sorted(inputs)]}
(HERE / 'source-results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: results[k] for k in ('base_commit', 'counts', 'occurrence_count', 'unique_resource_count', 'retained_resource_production_consumers')}, indent=2))
