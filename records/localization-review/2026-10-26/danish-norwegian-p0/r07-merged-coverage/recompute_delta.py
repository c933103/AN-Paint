"""Recompute an explicitly pinned integrated PR175-source delta; no application code or network executes."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BASE_COMMIT = 'df9bc04b848ab5e99457bc67265d771bb839ec9d'
BASE_TREE = '8ca5fc4f3989cf8c9307432d5e5c28ceef698251'
REVIEWED_HEAD = 'f6b3e71fd1261935c4d97b20cbbbdcc79ed398ed'
REVIEWED_TREE = '16ff3d877650ad4ad3198ce19007e8606fcd080a'
APPROVED_SHA256 = 'ecafd7485336b095c59c9c3103b93cabdf909f03da0da5526aa031367c2f657e'
BASE_MANIFEST_SHA256 = 'a2723d00972df6203224378cf8b7a29727e419bb1ddeaab2692c89bb8652552b'
STATUS = 'integrated source structurally verified; CI in progress in supplied source-identity snapshot'
LOCALES = {'da': ('Paintroid/src/main/res/values-da/strings.xml', 127),
           'no': ('Paintroid/src/main/res/values-no/strings.xml', 115)}
HOLDS = {'string/formats22_derived_exported', 'string/ui_save_as',
         'string/ui_save_as_jpeg', 'string/ui_save_as_jpeg_xl', 'string/ui_save_as_png'}
CANONICAL = 'Paintroid/src/main/res/values/strings.xml'
TAGS = 'Paintroid/src/main/res/values/app_language_tags.xml'
IMPORTANCE = 'translations/string-importance.json'
FORMAT_TOKEN = re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, 'duplicate JSON key: ' + key)
        value[key] = item
    return value


def read(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(data, kind='blob'):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def emit(folder, name, data):
    (folder / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def file_binding(path, public_name):
    raw = path.read_bytes()
    return {'path': public_name, 'bytes': len(raw), 'sha256': sha(raw), 'git_blob_sha1': git(raw)}


def parse(raw):
    root = ET.fromstring(raw)
    require(root.tag == 'resources', 'invalid resource root')
    containers, leaves, nodes, names = {}, {}, {}, set()
    for node in root:
        require(node.tag in ('string', 'plurals', 'string-array'), 'unexpected catalogue resource type')
        name = node.get('name')
        require(bool(name) and name not in names, 'missing or duplicate resource name')
        names.add(name)
        identity = node.tag + '/' + name
        nodes[identity] = node
        if node.get('translatable') == 'false':
            continue
        if node.tag == 'string':
            value = ''.join(node.itertext())
            require(bool(value), 'empty string resource: ' + identity)
            containers[identity] = value
            leaves[identity] = value
        else:
            values = {}
            for index, item in enumerate(node):
                require(item.tag == 'item', 'invalid resource child')
                quantity = item.get('quantity') if node.tag == 'plurals' else str(index)
                require(quantity is not None and quantity not in values, 'missing or duplicate resource item')
                if node.tag == 'plurals':
                    require(quantity in {'zero', 'one', 'two', 'few', 'many', 'other'}, 'unknown plural quantity')
                value = ''.join(item.itertext())
                require(bool(value), 'empty resource item')
                values[quantity] = value
                leaves[identity + '[' + quantity + ']'] = value
            require(bool(values), 'empty resource container')
            containers[identity] = values
    return containers, leaves, nodes


def fingerprint(node):
    return node.tag, sorted(node.attrib.items()), node.text, tuple(fingerprint(c) for c in node)


def tokens(text):
    require('%' not in FORMAT_TOKEN.sub('', text), 'invalid/unescaped format token')
    return collections.Counter(FORMAT_TOKEN.findall(text))


def verify_tree(tree, expected_tree):
    require(tree.get('truncated') is False and tree['sha'] == expected_tree, 'wrong/truncated head tree')
    entries = tree['tree']
    bypath = {e['path']: e for e in entries}
    require(len(bypath) == len(entries), 'duplicate tree path')
    children = collections.defaultdict(list)
    for e in entries:
        path = Path(e['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe tree path')
        require(e['type'] in ('blob', 'tree'), 'unsupported tree entry')
        require(e['mode'] in ('100644', '100755', '120000', '040000'), 'unexpected tree mode')
        require(bool(re.fullmatch('[0-9a-f]{40}', e['sha'])), 'malformed tree SHA')
        children[path.parent.as_posix() if path.parent.as_posix() != '.' else ''].append(e)
    for parent, contents in children.items():
        raw = b''
        for e in sorted(contents, key=lambda x: (Path(x['path']).name + ('/' if x['type'] == 'tree' else '')).encode()):
            mode = e['mode'].lstrip('0')
            raw += mode.encode() + b' ' + Path(e['path']).name.encode() + b'\0' + bytes.fromhex(e['sha'])
        expected = expected_tree if not parent else bypath[parent]['sha']
        require(git(raw, 'tree') == expected, 'recursive Git tree hash mismatch: ' + parent)
    return {k: e for k, e in bypath.items() if e['type'] == 'blob'}


def run(a):
    inputs = []
    def bind(path, role):
        inputs.append(file_binding(path, role))
        return read(path)

    manifest = bind(a.baseline_report / 'manifest.json', 'baseline-report/manifest.json')
    require(inputs[-1]['sha256'] == BASE_MANIFEST_SHA256, 'wrong baseline report manifest')
    for record in manifest['files']:
        raw = (a.baseline_report / record['path']).read_bytes()
        require(sha(raw) == record['sha256'] and git(raw) == record['git_blob_sha1'] and len(raw) == record['bytes'], 'baseline report file changed')
    rows_before = bind(a.baseline_report / 'structural-per-locale.json', 'baseline-report/structural-per-locale.json')
    summary_before = bind(a.baseline_report / 'coverage-delta.json', 'baseline-report/coverage-delta.json')
    provenance = bind(a.baseline_report / 'source-bindings.json', 'baseline-report/source-bindings.json')
    require(len(rows_before) == 171 and len({r['tag'] for r in rows_before}) == 171, 'baseline row inventory')
    require(summary_before['merged_commit'] == provenance['merged_commit'] == BASE_COMMIT and summary_before['merged_tree'] == BASE_TREE, 'wrong baseline source')
    require(bool(re.fullmatch('[0-9a-f]{40}', a.source_commit)) and a.source_commit not in (BASE_COMMIT, REVIEWED_HEAD), 'explicit merge commit required')
    require(a.source_tree == REVIEWED_TREE, 'tree differs from this reviewed batch')
    require(a.postmerge_run_id > 0, 'postmerge run identity required')
    identity = bind(a.identity_receipt, 'source-identity.json')
    require(identity['merge_commit'] == a.source_commit and identity['tree'] == a.source_tree, 'identity receipt pin mismatch')
    require(identity['develop_at_check'] == a.source_commit, 'explicit develop ref receipt mismatch')
    require(identity['parents'] == [BASE_COMMIT, REVIEWED_HEAD] and identity['signature_verified'] is True, 'merge parents/signature receipt')
    require(identity['repository'] == 'c933103/AN-Paint' and identity['pr'] == 175 and identity['merged'] is True and identity['reviewed_head'] == REVIEWED_HEAD and identity['same_tree_as_reviewed_head'] is True, 'merge receipt project/review scope')
    require(identity['actual_postmerge_run'] == a.postmerge_run_id and identity['actual_postmerge_event'] == 'push' and identity['actual_postmerge_status'] == 'in_progress', 'pending actual postmerge run binding')
    tree = bind(a.source_tree_file, 'source-tree.json')
    blobs = verify_tree(tree, a.source_tree)
    require(identity['local_source_blobs_git_verified'] == len(blobs), 'supplied whole-source inventory count differs from tree')
    baseline_files = {f['path']: f for f in provenance['files']}
    require(len(baseline_files) == len(provenance['files']) == 176, 'baseline input inventory')
    catalogue_paths = {str(p.relative_to(a.source_root)) for p in (a.source_root / 'Paintroid/src/main/res').glob('values*/strings.xml')}
    tree_catalogues = {p for p in blobs if re.fullmatch(r'Paintroid/src/main/res/values[^/]*/strings\.xml', p)}
    require(len(catalogue_paths) == 174 and catalogue_paths == tree_catalogues, 'checkout/tree catalogue inventory differs')
    require(set(baseline_files) == catalogue_paths | {TAGS, IMPORTANCE}, 'coverage input inventory changed')
    source, source_bindings, changed = {}, [], []
    for path, prior in baseline_files.items():
        raw = (a.source_root / path).read_bytes()
        entry = blobs[path]
        require(git(raw) == entry['sha'] and len(raw) == entry['size'], 'integrated source/tree mismatch: ' + path)
        source[path] = raw
        same = prior['merged_blob'] == entry['sha']
        if not same:
            changed.append(path)
        source_bindings.append({'path': path, 'baseline_blob': prior['merged_blob'], 'source_blob': entry['sha'],
                                'sha256': sha(raw), 'bytes': len(raw), 'mode': entry['mode'], 'unchanged': same})
    require(set(changed) == {v[0] for v in LOCALES.values()}, 'unexpected changed coverage input')
    base, base_leaves, base_nodes = parse(source[CANONICAL])
    require(len(base) == 717 and len(base_leaves) == 718, 'canonical denominator drift')
    arrays = ET.fromstring(source[TAGS]).findall('string-array')
    require(len(arrays) == 1 and all(n.tag == 'item' and n.text for n in arrays[0]), 'invalid picker inventory')
    tags = [n.text for n in arrays[0]]
    require(len(tags) == len(set(tags)) == 171 and tags == [r['tag'] for r in rows_before], 'picker order/inventory drift')
    tier_data = json.loads(source[IMPORTANCE].decode('utf-8'), object_pairs_hook=unique)['tiers']
    tiers = {t['id']: set(t['keys']) for t in tier_data}
    require(len(tiers) == len(tier_data) == 4 and {k:len(v) for k,v in tiers.items()} == {'P0':92,'P1':249,'P2':305,'P3':71}, 'tier inventory')
    require(all(len(t['keys']) == len(set(t['keys'])) for t in tier_data), 'duplicate tier identity')
    require(sum(map(len, tiers.values())) == len(set.union(*tiers.values())) == len(base) and set.union(*tiers.values()) == set(base), 'tier partition')
    rows, locale_nodes = [], {}
    for before in rows_before:
        path = before['path']
        containers, leaves, nodes = parse(source[path])
        row = {k: before[k] for k in ('order','tag','path')}
        row['blob'] = blobs[path]['sha']
        for tier, keys in {**tiers, 'all': set(base)}.items():
            row[tier + '_present'] = len(keys & containers.keys())
            row[tier + '_missing'] = len(keys - containers.keys())
        present = base_leaves.keys() & leaves.keys()
        row.update(leaves_present=len(present), leaves_missing=len(base_leaves.keys() - leaves.keys()),
                   leaves_english_identical=sum(leaves[k] == base_leaves[k] for k in present),
                   leaves_source_different=sum(leaves[k] != base_leaves[k] for k in present))
        if row['tag'] not in LOCALES:
            require(row == before, 'unexpected other-locale row delta: ' + row['tag'])
        else:
            locale_nodes[row['tag']] = nodes
        rows.append(row)
    metrics = [k for k in rows[0] if k not in ('order','tag','path','blob')]
    totals = {k: sum(r[k] for r in rows) for k in metrics}
    delta = {k: totals[k] - summary_before['presence_totals'][k] for k in metrics}
    require({k:v for k,v in delta.items() if v} == {'P0_present':156,'P0_missing':-156,'all_present':156,'all_missing':-156,'leaves_present':156,'leaves_missing':-156,'leaves_source_different':156}, 'unexpected aggregate delta')
    prior_nodes = {}
    for tag, (path, count) in LOCALES.items():
        raw = (a.baseline_source_root / path).read_bytes()
        inputs.append(file_binding(a.baseline_source_root / path, 'baseline-source/' + path))
        require(git(raw) == baseline_files[path]['merged_blob'] and sha(raw) == baseline_files[path]['sha256'], 'wrong prior catalogue bytes')
        _, _, old = parse(raw)
        new = locale_nodes[tag]
        require(len(old) == count and len(new) == count + 78, 'locale value count')
        for key, node in old.items():
            require(key in new and fingerprint(node) == fingerprint(new[key]), 'changed inherited value: ' + tag + '/' + key)
        require(set(new) - set(old) <= tiers['P0'], 'non-P0 addition')
        require(HOLDS.isdisjoint(new), 'held identity present')
        require(tiers['P0'] - new.keys() == HOLDS, 'remaining P0 holds differ')
        prior_nodes[tag] = old
    require(next(r for r in rows if r['tag'] == 'nn')['all_present'] == 190, 'Nynorsk scope changed')
    review = bind(a.review_dir / 'approved-values.json', 'reviews/approved-values.json')
    require(inputs[-1]['sha256'] == APPROVED_SHA256, 'wrong approved manifest')
    require(review['source_commit'] == BASE_COMMIT and review['source_tree'] == BASE_TREE and review['reviewed_values'] == 156, 'review source/count')
    require(set(review['locales']) == set(LOCALES) and set(review['held_missing_identities_per_locale']) == HOLDS, 'review locale/hold scope')
    receipt_map = bind(a.review_dir / 'review-receipt-bindings.json', 'reviews/review-receipt-bindings.json')
    require(receipt_map['source_commit'] == BASE_COMMIT, 'review receipt baseline')
    receipts, verdicts = {}, {}
    for receipt in receipt_map['receipts']:
        name = receipt['file']
        require(Path(name).name == name and name not in receipts, 'duplicate/unsafe receipt')
        document = bind(a.review_dir / name, 'reviews/' + name)
        require(inputs[-1]['sha256'] == receipt['public_export_sha256'], 'public receipt hash mismatch')
        require(document['source_commit'] == BASE_COMMIT and document['source_tree'] == BASE_TREE and document['locale'] == receipt['locale'], 'receipt source/locale')
        receipts[name] = {k: v for k, v in receipt.items() if k != 'metadata_changes'}
        for verdict in document['verdicts']:
            pair = (receipt['locale'], verdict['identity'])
            require(pair not in verdicts, 'duplicate reviewed pair')
            verdicts[pair] = (name, verdict, document)
    new_scopes, decisions, per_locale = [], collections.Counter(), {}
    for tag, entries in review['locales'].items():
        require(len(entries) == len({e['identity'] for e in entries}) == 78, 'approved per-locale grain')
        require({e['identity'] for e in entries} == locale_nodes[tag].keys() - prior_nodes[tag].keys(), 'unmatched new reviewed identities')
        local_decisions = collections.Counter()
        for entry in entries:
            key = entry['identity']; pair = (tag, key)
            require(pair in verdicts, 'missing independent verdict')
            name, verdict, document = verdicts[pair]
            require(entry['review_file'] == name and entry['original_review_sha256'] == receipts[name]['original_review_sha256'], 'approved receipt linkage')
            for field in ('source','source_value_sha256_utf8','accepted_display_text','accepted_value_sha256_utf8','accepted_xml_text','accepted_xml_text_sha256_utf8','attributes','verdict'):
                require(entry[field] == verdict[field], 'approved/review mismatch: ' + field)
            node = locale_nodes[tag][key]
            require(not list(node) and node.text == entry['accepted_xml_text'] and node.attrib == entry['attributes'], 'current XML/review mismatch')
            require(base[key] == entry['source'] and sha(entry['source'].encode()) == entry['source_value_sha256_utf8'], 'review source mismatch')
            require(sha(node.text.encode()) == entry['accepted_xml_text_sha256_utf8'] and sha(entry['accepted_display_text'].encode()) == entry['accepted_value_sha256_utf8'], 'review target hash mismatch')
            require(tokens(entry['source']) == tokens(entry['accepted_display_text']), 'format token mismatch')
            require(entry['verdict'] in ('accept','revise'), 'nonaccepted final scope')
            decisions[entry['verdict']] += 1; local_decisions[entry['verdict']] += 1
            qualification_fields = ('source_semantic_notes','author_semantic_qualifications','author_uncertainties','semantic_qualifications','review_rationale','reviewer_rationale','limits','remaining_limits')
            new_scopes.append(dict(entry, locale=tag, public_review_sha256=receipts[name]['public_export_sha256'],
                                   source_and_current_target_hash_matched=True,
                                   baseline_target_absent=True,
                                   receipt_qualifications={k: verdict[k] for k in qualification_fields if k in verdict},
                                   receipt_global_boundaries={k: document[k] for k in ('boundaries','acceptance_boundary','scope_guards') if k in document}))
        per_locale[tag] = dict(local_decisions)
    require(len(new_scopes) == len(verdicts) == 156 and decisions == {'accept':149,'revise':7}, 'final reviewed scope accounting')
    out = a.out; out.mkdir(parents=True, exist_ok=True)
    emit(out, 'structural-per-locale.json', rows)
    with (out / 'structural-per-locale.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    (out / 'source-identity.json').write_bytes(a.identity_receipt.read_bytes())
    emit(out, 'coverage-source-tree.json', {'source_commit':a.source_commit,'source_tree':a.source_tree,'source_status':STATUS,
         'truncated':False,'full_blob_count':len(blobs),'tree':[blobs[p] for p in sorted(source)]})
    emit(out, 'source-bindings.json', {'baseline_commit':BASE_COMMIT,'source_commit':a.source_commit,'source_tree':a.source_tree,'source_status':STATUS,
         'files':source_bindings,'unchanged_source_files':174,'changed_source_files':2})
    emit(out, 'input-bindings.json', {'source_commit':a.source_commit,'source_tree':a.source_tree,'source_status':STATUS,
         'all_paths_are_public_roles_not_execution_locations':True,'files':inputs})
    emit(out, 'review-scope-reconciliation.json', {'source_commit':a.source_commit,'source_tree':a.source_tree,'source_status':STATUS,
         'new_disjoint_bounded_AI_whole_value_scopes':156,'new_scope_verdict_counts':dict(decisions),'per_locale_verdict_counts':per_locale,
         'prior_catalogue_values_preserved':{'da':127,'no':115},'other_option_catalogues_unchanged':169,
         'prior_categories':{'accepted':'preserved; not recounted','qualified':'preserved; not upgraded','clause_only':'preserved; not upgraded',
            'author_only':'preserved; not upgraded','historical':'preserved; not upgraded or revoked','unmatched':'preserved; not guessed','synthetic':'preserved; not upgraded'},
         'global_accepted_count':None,'global_count_not_recomputed_reason':'This is an exact missing-only source delta, not a rerun or replacement of the inherited review ledger. Only the 156 previously absent locale/identity pairs are newly receipt-bound; all prior source values and their prior scope classifications remain unchanged.',
         'native_or_whole_language_certifications':0,'new_review_scopes':new_scopes,'review_receipts':list(receipts.values())})
    result = {'schema':'danish-norwegian-integrated-coverage-delta-v1','baseline_commit':BASE_COMMIT,'baseline_tree':BASE_TREE,
         'source_commit':a.source_commit,'source_tree':a.source_tree,'source_status':STATUS,'options':171,'canonical_containers':717,'canonical_leaves':718,
         'tiers':{k:len(v) for k,v in tiers.items()},'presence_totals':totals,'presence_delta':delta,
         'full_presence_options':sum(r['all_missing']==0 for r in rows),'zero_presence_options':sum(r['all_present']==0 for r in rows),
         'locales_before':{tag:next(r for r in rows_before if r['tag']==tag) for tag in LOCALES},
         'locales_after':{tag:next(r for r in rows if r['tag']==tag) for tag in LOCALES},
         'unchanged_options':169,'nn_unchanged_containers':190,'held_missing_identities_per_locale':sorted(HOLDS),
         'new_reviewed_pairs':156,'review_scope':'bounded independent AI whole-value linguistic/source-static; per-entry/global qualifications preserved, not native-human/device/layout/whole-language acceptance',
         'global_linguistic_categories_recomputed':False,'absence_implies_defect':False,'English_identical_implies_defect':False,
         'counting_policy':'Same XML-decoded exact leaf-text comparison as prior structural snapshot; quote wrapping is not normalized and runtime fallback is not counted as target presence.',
         'workflow_results':{'postmerge_run_id':a.postmerge_run_id,'status':'in_progress in supplied source-identity receipt, not an assertion of current run status','status_time_basis':'Receipt accompanies the merge at 2026-10-26T08:53:33Z; receipt has no separate check timestamp. Later terminal evidence is recorded separately.','PR_results_are_not_postmerge_results':True},
         'source_identity_proof':'Supplied authenticated-connector public commit verification receipt is hash-bound and its exact commit/tree/parents/signature fields are checked locally. This computation does not fetch or re-verify the remote commit graph.',
         'holds_preserved':['five missing P0 identities per da/no','five Nynorsk missing P0 identities','P1/paired-warning boundaries','global scoped59/fallback112','PR56 never-merge','PR159 freeze','PR113 held/retarget','Help callback/archive identity','interrupted archive','release pause']}
    emit(out, 'coverage-delta.json', result)
    print(json.dumps({'source_commit':a.source_commit,'source_status':STATUS,'totals':totals,'delta':delta,'reviewed_pairs':156,'verdict_counts':dict(decisions)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','source-tree-file','identity-receipt','baseline-report','baseline-source-root','review-dir','out'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--source-tree', required=True)
    parser.add_argument('--postmerge-run-id', type=int, required=True)
    run(parser.parse_args())


if __name__ == '__main__':
    main()
