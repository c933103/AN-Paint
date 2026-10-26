"""Recompute this report's identity unions and totals from saved JSON evidence.
Standard library only. Does not execute application source or tests, access the
network, or mutate a repository. Run beside the staged report files.
"""
import collections, gzip, hashlib, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent

def read(name):
    data = (ROOT / name).read_bytes()
    return json.loads(gzip.decompress(data) if name.endswith('.gz') else data)

def sha(data):
    return hashlib.sha256(data).hexdigest()

manifest = read('manifest.json')
for row in manifest['files']:
    data = (ROOT / row['path']).read_bytes()
    assert len(data) == row['bytes'], row['path']
    assert sha(data) == row['sha256'], row['path']
    if 'decompressed_sha256' in row:
        raw = gzip.decompress(data)
        assert sha(raw) == row['decompressed_sha256'], row['path']

objects = {}
for path in sorted(ROOT.glob('evidence-objects-*.json.gz')):
    objects.update(read(path.name))
for digest, obj in objects.items():
    encoded = json.dumps(obj, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':')).encode()
    assert sha(encoded) == digest
rows = []
for suffix in ('historical', 'additional'):
    rows.extend(read('current-evidence-union-' + suffix + '.json.gz')['rows'])
identities = {(r['tag'], r['key']) for r in rows}
assert len(identities) == len(rows) == 13898
for row in rows:
    for ref in row['evidence']:
        assert ref['object_sha256'] in objects
counts = collections.Counter(r['category'] for r in rows)
assert counts == {'independent_bounded_published': 4753,
                  'author_only_current': 8181,
                  'historical_bounded_scope_only': 963,
                  'fresh_unpublished_independent': 1}
bridge = read('historical-9465-continuity.json.gz')['rows']
assert len(bridge) == len({(r['tag'], r['key']) for r in bridge}) == 9465
unchanged = sum(r['source_exact'] and r['target_exact'] for r in bridge)
changed = [r for r in bridge if not (r['source_exact'] and r['target_exact'])]
assert unchanged == 9422 and len(changed) == 43
assert sum(r['current_independent_bound'] for r in changed) == 42
locale = read('per-locale-final.json')
assert len(locale) == len({r['tag'] for r in locale}) == 171
expected = {'all_present': 49726, 'all_missing': 72881,
            'P0_present': 6196, 'P0_missing': 9536,
            'P1_present': 19529, 'P1_missing': 23050,
            'leaves_english_identical': 7039,
            'leaves_source_different': 42721}
for key, total in expected.items():
    assert sum(r[key] for r in locale) == total
for row in locale:
    own = [r for r in rows if r['tag'] == row['tag']]
    assert sum(r['category'] == 'independent_bounded_published' for r in own) == row['independent_published']
print(json.dumps({'source': manifest['source'], 'presence': expected,
                  'evidence_categories_not_uniform_acceptance': dict(counts),
                  'historical_unchanged': unchanged,
                  'published_successors': 42, 'fresh_unpublished_successor': 1},
                 indent=2))
