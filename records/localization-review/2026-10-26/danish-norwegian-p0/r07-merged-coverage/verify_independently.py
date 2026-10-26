"""Separate DOM, Git-executable, CSV and receipt joins for the integrated coverage delta."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import xml.dom.minidom as DOM

REVIEWED_HEAD = 'f6b3e71fd1261935c4d97b20cbbbdcc79ed398ed'
REVIEWED_TREE = '16ff3d877650ad4ad3198ce19007e8606fcd080a'
BASE = 'df9bc04b848ab5e99457bc67265d771bb839ec9d'


def check(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        check(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def content(node):
    return ''.join(content(c) if c.nodeType == c.ELEMENT_NODE else
                   c.data if c.nodeType in (c.TEXT_NODE, c.CDATA_SECTION_NODE) else '' for c in node.childNodes)


def parse(path):
    document = DOM.parse(str(path))
    check(document.documentElement.tagName == 'resources', 'invalid resource root')
    containers, leaves, nodes = {}, {}, {}
    for node in document.documentElement.childNodes:
        if node.nodeType != node.ELEMENT_NODE:
            continue
        check(node.tagName in ('string','plurals','string-array'), 'unsupported resource node')
        name = node.getAttribute('name')
        key = node.tagName + '/' + name
        check(name and key not in nodes, 'missing/duplicate resource name')
        nodes[key] = node
        if node.getAttribute('translatable') == 'false':
            continue
        containers[key] = True
        if node.tagName == 'string':
            check(content(node), 'empty string')
            leaves[key] = content(node)
        else:
            children = [c for c in node.childNodes if c.nodeType == c.ELEMENT_NODE]
            check(children, 'empty container')
            for index, child in enumerate(children):
                check(child.tagName == 'item', 'invalid child')
                quantity = child.getAttribute('quantity') if node.tagName == 'plurals' else str(index)
                leaf = key + '[' + quantity + ']'
                check(quantity and leaf not in leaves and content(child), 'invalid/duplicate/empty leaf')
                leaves[leaf] = content(child)
    return containers, leaves, nodes


def run(a):
    check(a.source_tree == REVIEWED_TREE and a.source_commit not in (BASE,REVIEWED_HEAD), 'explicit integrated pin required')
    identity = load(a.report / 'source-identity.json')
    check(identity['merge_commit'] == a.source_commit and identity['tree'] == a.source_tree, 'identity receipt pin')
    check(identity['develop_at_check'] == a.source_commit, 'explicit develop ref receipt mismatch')
    check(identity['parents'] == [BASE,REVIEWED_HEAD] and identity['signature_verified'] is True and identity['merged'] is True, 'identity receipt evidence')
    check(identity['repository'] == 'c933103/AN-Paint' and identity['pr'] == 175 and identity['reviewed_head'] == REVIEWED_HEAD and identity['same_tree_as_reviewed_head'] is True, 'merge receipt project/review scope')
    rows = load(a.report / 'structural-per-locale.json')
    result = load(a.report / 'coverage-delta.json')
    bindings = load(a.report / 'source-bindings.json')
    filtered_tree = load(a.report / 'coverage-source-tree.json')
    scopes = load(a.report / 'review-scope-reconciliation.json')
    for document in (result, bindings, filtered_tree, scopes):
        check(document['source_commit'] == a.source_commit and document['source_tree'] == a.source_tree, 'incorrect explicit integrated identity')
        check(document['source_status'] == 'integrated source structurally verified; CI in progress in supplied source-identity snapshot', 'incorrect integrated-source/CI boundary')
    check(identity['actual_postmerge_status'] == 'in_progress' and identity['actual_postmerge_event'] == 'push' and result['workflow_results']['postmerge_run_id'] == identity['actual_postmerge_run'] and result['workflow_results']['status'] == 'in_progress in supplied source-identity receipt, not an assertion of current run status', 'pending postmerge CI boundary')
    check(result['baseline_commit'] == BASE and bindings['baseline_commit'] == BASE, 'baseline identity')
    check(len(rows) == len({r['tag'] for r in rows}) == 171, 'locale inventory')
    check([r['order'] for r in rows] == list(range(1,172)), 'locale order')
    before = load(a.baseline_report / 'structural-per-locale.json')
    old_summary = load(a.baseline_report / 'coverage-delta.json')
    old_by_tag = {r['tag']:r for r in before}
    check(len(before) == 171 and set(old_by_tag) == {r['tag'] for r in rows}, 'baseline tag inventory')
    tree = {e['path']:e for e in filtered_tree['tree']}
    files = {e['path']:e for e in bindings['files']}
    check(len(files) == len(bindings['files']) == len(tree) == len(filtered_tree['tree']) == 176, 'source binding inventory')
    check(files.keys() == tree.keys(), 'tree/source input keys')
    for path, record in files.items():
        raw = (a.source_root / path).read_bytes()
        actual = subprocess.check_output(['git','hash-object',str(a.source_root / path)], text=True).strip()
        check(actual == record['source_blob'] == tree[path]['sha'], 'Git source hash mismatch')
        check(hashlib.sha256(raw).hexdigest() == record['sha256'] and len(raw) == record['bytes'] == tree[path]['size'], 'source size/SHA256 mismatch')
        check(record['unchanged'] == (record['baseline_blob'] == actual), 'source unchanged flag')
    changed = [p for p,r in files.items() if not r['unchanged']]
    check(set(changed) == {'Paintroid/src/main/res/values-da/strings.xml','Paintroid/src/main/res/values-no/strings.xml'}, 'changed input scope')
    canonical, base_leaves, _ = parse(a.source_root / 'Paintroid/src/main/res/values/strings.xml')
    tier_data = load(a.source_root / 'translations/string-importance.json')['tiers']
    check({t['id']:len(t['keys']) for t in tier_data} == {'P0':92,'P1':249,'P2':305,'P3':71}, 'tier sizes')
    all_tier_keys = [key for t in tier_data for key in t['keys']]
    check(len(all_tier_keys) == len(set(all_tier_keys)) == len(canonical) == 717 and set(all_tier_keys) == set(canonical), 'tier partition')
    check(len(base_leaves) == 718, 'leaf denominator')
    sums, fields, new_nodes = {}, None, {}
    for row in rows:
        containers, leaves, nodes = parse(a.source_root / row['path'])
        calculated = {}
        for tier in tier_data + [{'id':'all','keys':list(canonical)}]:
            calculated[tier['id'] + '_present'] = sum(key in containers for key in tier['keys'])
            calculated[tier['id'] + '_missing'] = sum(key not in containers for key in tier['keys'])
        calculated['leaves_present'] = sum(key in leaves for key in base_leaves)
        calculated['leaves_missing'] = sum(key not in leaves for key in base_leaves)
        calculated['leaves_english_identical'] = sum(key in leaves and leaves[key] == value for key,value in base_leaves.items())
        calculated['leaves_source_different'] = sum(key in leaves and leaves[key] != value for key,value in base_leaves.items())
        check(all(row[key] == value for key,value in calculated.items()), 'DOM row recomputation mismatch')
        check(row['blob'] == files[row['path']]['source_blob'], 'row/blob binding')
        if row['tag'] not in ('da','no'):
            check(row == old_by_tag[row['tag']], 'changed other option')
        else:
            new_nodes[row['tag']] = nodes
        fields = list(calculated)
        for key,value in calculated.items():
            sums[key] = sums.get(key,0) + value
    check(sums == result['presence_totals'], 'aggregate mismatch')
    check({key:value-old_summary['presence_totals'][key] for key,value in sums.items()} == result['presence_delta'], 'delta mismatch')
    check(sums['all_present'] + sums['all_missing'] == 171*717 and sums['leaves_present'] + sums['leaves_missing'] == 171*718, 'aggregate denominator')
    with (a.report / 'structural-per-locale.csv').open(newline='', encoding='utf-8') as stream:
        csv_rows = list(csv.DictReader(stream))
    for row in csv_rows:
        for key in fields + ['order']:
            row[key] = int(row[key])
    check(csv_rows == rows, 'CSV/JSON mismatch')
    check(result['full_presence_options'] == sum(r['all_missing'] == 0 for r in rows) == 59 and result['zero_presence_options'] == sum(r['all_present'] == 0 for r in rows) == 31, 'full/zero groups')
    old_nodes, missing_pairs = {}, set()
    for tag,count in (('da',127),('no',115)):
        path = old_by_tag[tag]['path']
        old_blob = subprocess.check_output(['git','hash-object',str(a.baseline_source_root / path)], text=True).strip()
        check(old_blob == files[path]['baseline_blob'], 'prior source binding')
        _, _, old_nodes[tag] = parse(a.baseline_source_root / path)
        check(len(old_nodes[tag]) == count and len(new_nodes[tag]) == count+78, 'prior/new catalogue count')
        for key,node in old_nodes[tag].items():
            current = new_nodes[tag][key]
            check(content(node) == content(current) and dict(node.attributes.items()) == dict(current.attributes.items()) and node.tagName == current.tagName, 'inherited value/attribute changed')
        missing_pairs.update((tag,key) for key in new_nodes[tag].keys()-old_nodes[tag].keys())
        check(set(result['held_missing_identities_per_locale']).isdisjoint(new_nodes[tag]), 'held identity present')
        after = next(r for r in rows if r['tag'] == tag)
        check(after['P0_present'] == 87 and after['P0_missing'] == 5, 'P0 held coverage')
        check(result['locales_before'][tag] == old_by_tag[tag] and result['locales_after'][tag] == after, 'before/after summary')
    receipt_index = {}
    for receipt in scopes['review_receipts']:
        path = a.review_dir / receipt['file']
        check(hashlib.sha256(path.read_bytes()).hexdigest() == receipt['public_export_sha256'], 'review bytes differ')
        document = load(path)
        for verdict in document['verdicts']:
            pair = (receipt['locale'], verdict['identity'])
            check(pair not in receipt_index, 'duplicate review pair')
            receipt_index[pair] = (receipt, verdict, document)
    pairs, counts = set(), {'accept':0,'revise':0}
    for entry in scopes['new_review_scopes']:
        pair = (entry['locale'], entry['identity'])
        check(pair not in pairs and pair in missing_pairs, 'duplicate/not-new review pair')
        pairs.add(pair)
        receipt, verdict, document = receipt_index[pair]
        check(entry['public_review_sha256'] == receipt['public_export_sha256'], 'scope/receipt hash')
        for key in ('source','source_value_sha256_utf8','accepted_display_text','accepted_value_sha256_utf8','accepted_xml_text','accepted_xml_text_sha256_utf8','attributes','verdict'):
            check(entry[key] == verdict[key], 'scope/verdict mismatch')
        current = new_nodes[pair[0]][pair[1]]
        check(content(current) == entry['accepted_xml_text'] and dict(current.attributes.items()) == entry['attributes'], 'scope/current value')
        check(base_leaves[pair[1]] == entry['source'], 'scope/source value')
        qualification_fields = ('source_semantic_notes','author_semantic_qualifications','author_uncertainties','semantic_qualifications','review_rationale','reviewer_rationale','limits','remaining_limits')
        check(entry['receipt_qualifications'] == {k:verdict[k] for k in qualification_fields if k in verdict}, 'qualification changed or omitted')
        check(entry['receipt_global_boundaries'] == {k:document[k] for k in ('boundaries','acceptance_boundary','scope_guards') if k in document}, 'global qualification changed or omitted')
        counts[entry['verdict']] += 1
    check(len(pairs) == len(missing_pairs) == len(receipt_index) == 156 and pairs == missing_pairs, 'review join grain')
    check(counts == scopes['new_scope_verdict_counts'] == {'accept':149,'revise':7}, 'review scope counts')
    check(scopes['global_accepted_count'] is None and result['global_linguistic_categories_recomputed'] is False, 'unsupported global review total')
    verification = {'schema':'danish-norwegian-independent-coverage-validation-v1','source_commit':a.source_commit,'source_tree':a.source_tree,
        'source_status':result['source_status'],'rows':171,'coverage_inputs_Git_executable_and_SHA256_verified':176,
        'separate_DOM_all_presence_and_English_identity_fields_equal':True,'CSV_JSON_equal':True,
        'prior_values_and_attributes_preserved':{'da':127,'no':115},'unchanged_other_options':169,
        'review_join_exact_new_pairs':156,'independent_review_receipt_hashes_verified':8,
        'prior_scope_categories_not_reclassified':True,'native_linguistic_runtime_or_layout_judgment_added':False}
    return verification


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','report','baseline-report','baseline-source-root','review-dir'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--source-tree', required=True)
    a = parser.parse_args()
    result = run(a)
    (a.report / 'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
