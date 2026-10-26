"""Recompute the pinned integrated PR176 coverage delta; no application code or network executes."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BASE_COMMIT = '05607f0d60131cc9148461ce595155d820748e4e'
BASE_TREE = '16ff3d877650ad4ad3198ce19007e8606fcd080a'
SOURCE_COMMIT = '6a42948a3ac7bad241d502f3b6c18ebf1c0327d8'
SOURCE_TREE = '65afa7b96a83c08e0ae08365166dec0520694356'
APPROVED_SHA256 = '809faecd60cfb032f4a03497ae50b7c6851b7ff3f520333b6019d97213543c93'
BASE_MANIFEST_SHA256 = '3d198344ba6ff805d61fb13f77b4143f95f1c6f432b50f2d2d245f4a93fc9abc'
REVIEWED_HEAD = 'a365f4b552448803c0bb48b3c44cdf508550eaf9'
STATUS = 'integrated source; actual postmerge CI pending'
LOCALES = {'ca': ('Paintroid/src/main/res/values-ca/strings.xml', 127),
           'ro': ('Paintroid/src/main/res/values-ro/strings.xml', 127)}
RECEIPTS = {'ca': ('ca-independent-review.json', '897469420007d15173f4a8b58cc8cd3ed53cea3738037bfb23b02216047a6e7d'),
            'ro': ('ro-independent-review.json', 'c13f44c483042ca15066706501a4015e64b807ea80af45ae41b9a955cbdd880a')}
SELECTED = {'string/' + key for key in ('ui_your_current_image_has_unsaved_changes', 'ui_could_not_save_image', 'ui_saved', 'ui_export_did_not_save23', 'ui_save_explanation23', 'ui_export_explanation23', 'ui_share_explanation34', 'ui_save_and_share', 'ui_save_and_share_41edb4', 'ui_the_image_was_saved_but_android_could_not')}
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


def verify_tree(tree):
    require(tree.get('truncated') is False and tree['sha'] == SOURCE_TREE, 'wrong/truncated integrated source tree')
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
        expected = SOURCE_TREE if not parent else bypath[parent]['sha']
        require(git(raw, 'tree') == expected, 'recursive Git tree hash mismatch: ' + parent)
    return {k: e for k, e in bypath.items() if e['type'] == 'blob'}


def verify_identity(identity):
    require(identity['pr'] == 176 and identity['pr_merged'] is True, 'merge project/PR scope')
    require(identity['source_commit'] == SOURCE_COMMIT and identity['source_tree'] == SOURCE_TREE, 'merge source pin')
    require(identity['ordered_parents'] == [BASE_COMMIT, REVIEWED_HEAD], 'merge parent order/identity')
    require(identity['github_signature_verified'] is True and identity['reviewed_and_merged_tree_identical'] is True and identity['reviewed_head'] == REVIEWED_HEAD, 'verified reviewed merge receipt')
    require(identity['explicit_develop_observed'] == SOURCE_COMMIT, 'explicit develop ref receipt')
    require(type(identity['run']['id']) is int and identity['run']['id'] == 40311048893 and identity['run']['head_sha'] == SOURCE_COMMIT and identity['run']['event'] == 'push', 'actual postmerge run identity')
    require(identity['run']['status'] in ('queued','in_progress') and identity['run']['conclusion'] is None, 'pending actual postmerge receipt boundary')
    require(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',identity['pr_merged_at'])), 'merge timestamp schema')


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
    require(summary_before['source_commit'] == provenance['source_commit'] == BASE_COMMIT and summary_before['source_tree'] == BASE_TREE, 'wrong baseline source')
    identity = bind(a.identity_receipt, 'source-identity.json')
    verify_identity(identity)
    tree = bind(a.source_tree_file, 'source-tree.json')
    blobs = verify_tree(tree)
    require(identity['local_source_blobs_freshly_git_verified'] == len(blobs) == 1373, 'whole-source receipt inventory')
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
        same = prior['source_blob'] == entry['sha']
        if not same:
            changed.append(path)
        source_bindings.append({'path': path, 'baseline_blob': prior['source_blob'], 'source_blob': entry['sha'],
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
    require({k:v for k,v in delta.items() if v} == {'P0_present':20,'P0_missing':-20,'all_present':20,'all_missing':-20,'leaves_present':20,'leaves_missing':-20,'leaves_source_different':20}, 'unexpected aggregate delta')
    prior_nodes = {}
    for tag, (path, count) in LOCALES.items():
        raw = (a.baseline_source_root / path).read_bytes()
        inputs.append(file_binding(a.baseline_source_root / path, 'baseline-source/' + path))
        require(git(raw) == baseline_files[path]['source_blob'] and sha(raw) == baseline_files[path]['sha256'], 'wrong prior catalogue bytes')
        _, _, old = parse(raw)
        new = locale_nodes[tag]
        require(len(old) == count and len(new) == count + 10, 'locale value count')
        for key, node in old.items():
            require(key in new and fingerprint(node) == fingerprint(new[key]), 'changed inherited value: ' + tag + '/' + key)
        require(set(new) - set(old) <= tiers['P0'], 'non-P0 addition')
        require(HOLDS.isdisjoint(new), 'held identity present')
        require(len(tiers['P0'] - new.keys()) == 73 and len((tiers['P0'] - new.keys()) - HOLDS) == 68, 'remaining P0 missing/outside-batch counts differ')
        require(new.keys() - old.keys() == SELECTED, 'new identity scope differs')
        prior_nodes[tag] = old
    require({tag:next(r for r in rows if r['tag'] == tag)['all_present'] for tag in ('nn','da','no')} == {'nn':190,'da':205,'no':193}, 'previous added locale scope changed')
    inherited = bind(a.baseline_report / 'review-scope-reconciliation.json', 'baseline-report/review-scope-reconciliation.json')
    require(inherited['source_commit'] == BASE_COMMIT and inherited['source_tree'] == BASE_TREE, 'inherited scope source')
    inherited_binding = dict(inputs[-1])
    review = bind(a.review_dir / 'approved-values.json', 'reviews/approved-values.json')
    require(inputs[-1]['sha256'] == APPROVED_SHA256, 'wrong approved manifest')
    require(review['schema_version'] == 1 and review['source_commit'] == BASE_COMMIT and review['source_tree'] == BASE_TREE, 'review source/schema')
    require(set(review['locales']) == set(LOCALES), 'review locale scope')
    receipts, verdicts, documents = {}, {}, {}
    for tag, (name, expected_hash) in RECEIPTS.items():
        document = bind(a.review_dir / name, 'reviews/' + name)
        require(inputs[-1]['sha256'] == expected_hash, 'original receipt hash mismatch')
        require(document['source_commit'] == BASE_COMMIT and document['source_tree'] == BASE_TREE and document['locale'] == tag, 'receipt source/locale')
        require(document['target_path'] == LOCALES[tag][0] and document['schema_version'] == 1, 'receipt path/schema')
        require(review['global_qualifications'][tag] == document['global_qualifications'], 'normalized global qualification differs')
        documents[tag] = document
        receipts[name] = dict(inputs[-1], file=name, locale=tag, public_export_sha256=expected_hash,
                              public_record='https://github.com/c933103/AN-Paint/blob/137b2917329a1dcf85bbc78b2d9581101cbcb649/records/localization-review/2026-10-26/catalan-romanian-p0-save/r02-reviewed/' + name)
        entries = document['entries' if tag == 'ca' else 'verdicts']
        require(len(entries) == 10, 'independent verdict count')
        for verdict in entries:
            pair = (tag, verdict['identity'])
            require(pair not in verdicts, 'duplicate reviewed pair')
            verdicts[pair] = verdict
    new_scopes, decisions, per_locale = [], collections.Counter(), {}
    for tag, entries in review['locales'].items():
        require(len(entries) == len({e['identity'] for e in entries}) == 10, 'approved per-locale grain')
        require({e['identity'] for e in entries} == SELECTED == locale_nodes[tag].keys() - prior_nodes[tag].keys(), 'unmatched new reviewed identities')
        local_decisions = collections.Counter()
        for entry in entries:
            key = entry['identity']; pair = (tag, key)
            require(pair in verdicts, 'missing independent verdict')
            verdict = verdicts[pair]
            name, receipt_hash = RECEIPTS[tag]
            require(entry['review_file'] == name and entry['review_sha256'] == receipt_hash, 'approved receipt linkage')
            comparisons = {'source':'source', 'source_sha256':'source_value_sha256_utf8', 'display':'final_display_text',
                'display_sha256':'final_display_sha256_utf8' if tag == 'ca' else 'final_value_sha256_utf8',
                'xml_text':'final_xml_text', 'xml_text_sha256':'final_xml_text_sha256_utf8',
                'attributes':'final_attributes' if tag == 'ca' else 'attributes', 'qualifications':'qualifications', 'confidence':'confidence'}
            require(all(entry[k] == verdict[v] for k,v in comparisons.items()), 'normalized/review value or qualification mismatch')
            require(verdict['priority'] == 'P0' and verdict['verdict'] == 'accept' and verdict['accepted_unchanged' if tag == 'ca' else 'candidate_unchanged'] is True, 'not unchanged accepted P0')
            require(entry['verdict'] == 'accept unchanged', 'nonaccepted normalized scope')
            node = locale_nodes[tag][key]
            require(not list(node) and node.text == entry['xml_text'] and node.attrib == entry['attributes'], 'current XML/review mismatch')
            require(base[key] == entry['source'] and sha(entry['source'].encode()) == entry['source_sha256'], 'review source mismatch')
            require(sha(node.text.encode()) == entry['xml_text_sha256'] and sha(entry['display'].encode()) == entry['display_sha256'], 'review target hash mismatch')
            require(tokens(entry['source']) == tokens(entry['display']), 'format token mismatch')
            require(verdict['candidate_display_text'] == entry['display'] and verdict['candidate_value_sha256_utf8'] == entry['display_sha256'], 'unchanged candidate mismatch')
            decisions['accept unchanged'] += 1; local_decisions['accept unchanged'] += 1
            new_scopes.append(dict(entry, locale=tag, public_review_sha256=receipt_hash,
                                   source_and_current_target_hash_matched=True, baseline_target_absent=True,
                                   original_full_value_verdict=verdict,
                                   receipt_global_qualifications=documents[tag]['global_qualifications']))
        per_locale[tag] = dict(local_decisions)
    require(len(new_scopes) == len(verdicts) == 20 and decisions == {'accept unchanged':20}, 'final reviewed scope accounting')
    remaining = {tag: {'all_missing_P0': sorted(tiers['P0'] - locale_nodes[tag].keys()),
                      'explicit_no_current_consumer_holds': sorted(HOLDS),
                      'other_missing_P0_outside_this_batch': sorted((tiers['P0'] - locale_nodes[tag].keys()) - HOLDS),
                      'missing_count':73, 'explicit_hold_count':5, 'outside_batch_count':68,
                      'outside_batch_is_not_new_hold_or_defect_judgment':True} for tag in LOCALES}
    out = a.out; out.mkdir(parents=True, exist_ok=True)
    (out / 'source-identity.json').write_bytes(a.identity_receipt.read_bytes())
    emit(out, 'structural-per-locale.json', rows)
    with (out / 'structural-per-locale.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    emit(out, 'coverage-source-tree.json', {'source_commit':SOURCE_COMMIT,'source_tree':SOURCE_TREE,'source_status':STATUS,
         'truncated':False,'full_blob_count':len(blobs),'tree':[blobs[p] for p in sorted(source)]})
    emit(out, 'source-bindings.json', {'baseline_commit':BASE_COMMIT,'source_commit':SOURCE_COMMIT,'source_tree':SOURCE_TREE,'source_status':STATUS,
         'files':source_bindings,'unchanged_source_files':174,'changed_source_files':2})
    emit(out, 'input-bindings.json', {'source_commit':SOURCE_COMMIT,'source_tree':SOURCE_TREE,'source_status':STATUS,
         'all_paths_are_public_roles_not_execution_locations':True,'files':inputs})
    emit(out, 'review-scope-reconciliation.json', {'source_commit':SOURCE_COMMIT,'source_tree':SOURCE_TREE,'source_status':STATUS,
         'new_disjoint_bounded_AI_whole_value_scopes':20,'new_scope_verdict_counts':dict(decisions),'per_locale_verdict_counts':per_locale,
         'prior_catalogue_values_preserved':{'ca':127,'ro':127},'other_option_catalogues_unchanged':169,
         'prior_categories':{'accepted':'preserved; not recounted','qualified':'preserved; not upgraded','clause_only':'preserved; not upgraded',
            'author_only':'preserved; not upgraded','historical':'preserved; not upgraded or revoked','unmatched':'preserved; not guessed','synthetic':'preserved; not upgraded'},
         'global_accepted_count':None,'global_count_not_recomputed_reason':'This is an exact missing-only source delta, not a rerun or replacement of the inherited review ledger. Only the 20 previously absent locale/identity pairs are newly receipt-bound; all prior source values and their prior scope classifications remain unchanged.',
         'native_or_whole_language_certifications':0,'new_review_scopes':new_scopes,'review_receipts':list(receipts.values()),
         'original_receipt_global_qualifications':review['global_qualifications'],
         'inherited_scope_binding':inherited_binding,
         'remaining_missing_P0_classification':remaining,
         'static_composition_examples':{tag:doc['static_composition_examples'] for tag,doc in documents.items()}})
    result = {'schema':'catalan-romanian-integrated-coverage-delta-v1','baseline_commit':BASE_COMMIT,'baseline_tree':BASE_TREE,
         'source_commit':SOURCE_COMMIT,'source_tree':SOURCE_TREE,'source_status':STATUS,'options':171,'canonical_containers':717,'canonical_leaves':718,
         'tiers':{k:len(v) for k,v in tiers.items()},'presence_totals':totals,'presence_delta':delta,
         'full_presence_options':sum(r['all_missing']==0 for r in rows),'zero_presence_options':sum(r['all_present']==0 for r in rows),
         'locales_before':{tag:next(r for r in rows_before if r['tag']==tag) for tag in LOCALES},
         'locales_after':{tag:next(r for r in rows if r['tag']==tag) for tag in LOCALES},
         'unchanged_options':169,'unchanged_previous_added_locales':{'nn':190,'da':205,'no':193},'held_missing_identities_per_locale':sorted(HOLDS),
         'remaining_missing_P0_classification':remaining,
         'new_reviewed_pairs':20,'review_scope':'bounded independent AI whole-value linguistic/source-static; per-entry/global qualifications preserved, not native-human/device/layout/whole-language acceptance',
         'global_linguistic_categories_recomputed':False,'absence_implies_defect':False,'English_identical_implies_defect':False,
         'counting_policy':'Same XML-decoded exact leaf-text comparison as prior structural snapshot; quote wrapping is not normalized and runtime fallback is not counted as target presence.',
         'workflow_results':{'postmerge_run_id':identity['run']['id'],'status':identity['run']['status'] + ' in supplied source-identity receipt; not an assertion of later current status','status_observation':None,'associated_merge_timestamp':identity['pr_merged_at'],'status_observation_basis':'Receipt has no separate check timestamp; the associated merge timestamp is not a claimed CI polling time. Later terminal evidence must be recorded separately.','PR_results_are_not_postmerge_results':True},
         'source_identity_proof':'Supplied public authenticated-connector merge identity receipt is byte-bound and checked locally for commit/tree/ordered parents/signature/develop reference and pending actual postmerge identity; this computation performs no fresh network commit-graph verification.',
         'holds_preserved':['five explicit no-current-consumer P0 holds per ca/ro; 68 other missing P0 values per locale are outside this batch, not newly held','five missing P0 identities per nn/da/no','P1/paired-warning boundaries','global scoped59/fallback112','PR56 never-merge','PR159 freeze','PR113 held/retarget','Help callback/archive identity','interrupted archive','release pause']}
    emit(out, 'coverage-delta.json', result)
    print(json.dumps({'source_commit':SOURCE_COMMIT,'source_status':STATUS,'totals':totals,'delta':delta,'reviewed_pairs':20,'verdict_counts':dict(decisions)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','source-tree-file','identity-receipt','baseline-report','baseline-source-root','review-dir','out'):
        parser.add_argument('--' + name, type=Path, required=True)
    run(parser.parse_args())


if __name__ == '__main__':
    main()
