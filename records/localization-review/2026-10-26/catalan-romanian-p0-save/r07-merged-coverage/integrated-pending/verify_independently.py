"""Separate DOM, Git-executable, CSV and receipt joins for the integrated coverage delta."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import xml.dom.minidom as DOM

SOURCE = '6a42948a3ac7bad241d502f3b6c18ebf1c0327d8'
TREE = '65afa7b96a83c08e0ae08365166dec0520694356'
BASE = '05607f0d60131cc9148461ce595155d820748e4e'


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
    identity=load(a.report/'source-identity.json')
    check(identity['pr']==176 and identity['pr_merged'] is True, 'merge receipt scope')
    check(identity['source_commit']==SOURCE and identity['source_tree']==TREE and identity['explicit_develop_observed']==SOURCE, 'merge commit/tree/develop pin')
    check(identity['ordered_parents']==[BASE,'a365f4b552448803c0bb48b3c44cdf508550eaf9'] and identity['reviewed_head']=='a365f4b552448803c0bb48b3c44cdf508550eaf9', 'merge parent/reviewed head identity')
    check(identity['github_signature_verified'] is True and identity['reviewed_and_merged_tree_identical'] is True and identity['local_source_blobs_freshly_git_verified']==1373, 'source verification receipt')
    check(type(identity['run']['id']) is int and identity['run']['id']==40311048893 and identity['run']['head_sha']==SOURCE and identity['run']['event']=='push' and identity['run']['status'] in ('queued','in_progress') and identity['run']['conclusion'] is None, 'pending actual postmerge receipt')
    inputs=load(a.report/'input-bindings.json')['files']
    receipts=[e for e in inputs if e['path']=='source-identity.json'];check(len(receipts)==1, 'merge receipt binding inventory')
    raw=(a.report/'source-identity.json').read_bytes();receipt=receipts[0]
    check(receipt['sha256']==hashlib.sha256(raw).hexdigest() and receipt['bytes']==len(raw) and receipt['git_blob_sha1']==subprocess.check_output(['git','hash-object',str(a.report/'source-identity.json')],text=True).strip(), 'merge receipt byte binding')
    rows = load(a.report / 'structural-per-locale.json')
    result = load(a.report / 'coverage-delta.json')
    bindings = load(a.report / 'source-bindings.json')
    filtered_tree = load(a.report / 'coverage-source-tree.json')
    scopes = load(a.report / 'review-scope-reconciliation.json')
    for document in (result, bindings, filtered_tree, scopes):
        check(document['source_commit'] == SOURCE and document['source_tree'] == TREE, 'incorrect fixed integrated identity')
        check(document['source_status'] == 'integrated source; actual postmerge CI pending', 'incorrect pending integrated boundary')
    check(result['workflow_results']['postmerge_run_id']==identity['run']['id'] and result['workflow_results']['PR_results_are_not_postmerge_results'] is True and result['workflow_results']['status']==identity['run']['status']+' in supplied source-identity receipt; not an assertion of later current status', 'postmerge status distinction')
    check(result['workflow_results']['status_observation'] is None and result['workflow_results']['associated_merge_timestamp']==identity['pr_merged_at'], 'unsupported CI observation timestamp')
    check(result['baseline_commit'] == BASE and bindings['baseline_commit'] == BASE, 'baseline identity')
    check(type(rows) is list and all(type(r) is dict for r in rows), 'row schema')
    check(result['schema'] == 'catalan-romanian-integrated-coverage-delta-v1' and result['options'] == 171 and result['canonical_containers'] == 717 and result['canonical_leaves'] == 718, 'declared report schema/denominators')
    check(result['tiers'] == {'P0':92,'P1':249,'P2':305,'P3':71}, 'declared tiers')
    check(filtered_tree['truncated'] is False and filtered_tree['full_blob_count'] == 1373, 'full tree boundary')
    check(bindings['unchanged_source_files'] == 174 and bindings['changed_source_files'] == 2, 'changed input count')
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
    check(set(changed) == {'Paintroid/src/main/res/values-ca/strings.xml','Paintroid/src/main/res/values-ro/strings.xml'}, 'changed input scope')
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
        check(set(row) == set(calculated) | {'order','tag','path','blob'} and type(row['order']) is int, 'row field schema')
        check(all(type(row[key]) is int and row[key] == value for key,value in calculated.items()), 'DOM row recomputation mismatch')
        check(row['path'] == old_by_tag[row['tag']]['path'], 'row path identity')
        check(row['blob'] == files[row['path']]['source_blob'], 'row/blob binding')
        if row['tag'] not in ('ca','ro'):
            check(row == old_by_tag[row['tag']], 'changed other option')
        else:
            new_nodes[row['tag']] = nodes
        fields = list(calculated)
        for key,value in calculated.items():
            sums[key] = sums.get(key,0) + value
    check(sums == result['presence_totals'] and all(type(v) is int for v in result['presence_totals'].values()), 'aggregate mismatch')
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
    for tag,count in (('ca',127),('ro',127)):
        path = old_by_tag[tag]['path']
        old_blob = subprocess.check_output(['git','hash-object',str(a.baseline_source_root / path)], text=True).strip()
        check(old_blob == files[path]['baseline_blob'], 'prior source binding')
        _, _, old_nodes[tag] = parse(a.baseline_source_root / path)
        check(len(old_nodes[tag]) == count and len(new_nodes[tag]) == count+10, 'prior/new catalogue count')
        for key,node in old_nodes[tag].items():
            current = new_nodes[tag][key]
            check(content(node) == content(current) and dict(node.attributes.items()) == dict(current.attributes.items()) and node.tagName == current.tagName, 'inherited value/attribute changed')
        missing_pairs.update((tag,key) for key in new_nodes[tag].keys()-old_nodes[tag].keys())
        check(set(result['held_missing_identities_per_locale']).isdisjoint(new_nodes[tag]), 'held identity present')
        after = next(r for r in rows if r['tag'] == tag)
        check(after['P0_present'] == 19 and after['P0_missing'] == 73 and after['all_present'] == 137, 'P0 held coverage')
        check(result['locales_before'][tag] == old_by_tag[tag] and result['locales_after'][tag] == after, 'before/after summary')
    holds = {'string/' + key for key in ('formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png')}
    selected = {'string/' + key for key in ('ui_your_current_image_has_unsaved_changes','ui_could_not_save_image','ui_saved','ui_export_did_not_save23','ui_save_explanation23','ui_export_explanation23','ui_share_explanation34','ui_save_and_share','ui_save_and_share_41edb4','ui_the_image_was_saved_but_android_could_not')}
    check(missing_pairs == {(tag,key) for tag in ('ca','ro') for key in selected}, 'selected identity drift')
    check(set(result['held_missing_identities_per_locale']) == holds, 'held set drift')
    p0 = next(set(t['keys']) for t in tier_data if t['id'] == 'P0')
    for tag in ('ca','ro'):
        missing = p0-new_nodes[tag].keys()
        expected = {'all_missing_P0':sorted(missing), 'explicit_no_current_consumer_holds':sorted(holds),
                    'other_missing_P0_outside_this_batch':sorted(missing-holds), 'missing_count':73,
                    'explicit_hold_count':5, 'outside_batch_count':68, 'outside_batch_is_not_new_hold_or_defect_judgment':True}
        check(len(missing) == 73 and len(missing-holds) == 68 and holds <= missing, 'missing/held/outside counts')
        check(result['remaining_missing_P0_classification'][tag] == scopes['remaining_missing_P0_classification'][tag] == expected, 'missing/held/outside classification')
    check(result['unchanged_previous_added_locales'] == {'nn':190,'da':205,'no':193}, 'inherited locale summary')
    for tag,count in (('nn',190),('da',205),('no',193)):
        row = next(r for r in rows if r['tag'] == tag)
        _,_,nodes = parse(a.source_root / row['path'])
        check(row['all_present'] == count and holds.isdisjoint(nodes), 'prior locale/hold preservation')
    expected_hashes = {'ca':'897469420007d15173f4a8b58cc8cd3ed53cea3738037bfb23b02216047a6e7d',
                       'ro':'c13f44c483042ca15066706501a4015e64b807ea80af45ae41b9a955cbdd880a'}
    receipt_index, documents, receipt_locales = {}, {}, set()
    check(len(scopes['review_receipts']) == 2, 'receipt inventory')
    for receipt in scopes['review_receipts']:
        tag=receipt['locale']; check(tag in expected_hashes and tag not in receipt_locales, 'receipt locale duplication')
        receipt_locales.add(tag)
        check(receipt['file'] == tag+'-independent-review.json', 'receipt filename')
        path = a.review_dir / receipt['file']
        check(hashlib.sha256(path.read_bytes()).hexdigest() == receipt['public_export_sha256'] == expected_hashes[tag], 'review bytes differ')
        document = load(path); documents[tag]=document
        check(document['locale'] == tag and document['source_commit'] == BASE and document['source_tree'] == '16ff3d877650ad4ad3198ce19007e8606fcd080a', 'receipt source identity')
        for verdict in document['entries' if tag == 'ca' else 'verdicts']:
            pair = (tag, verdict['identity'])
            check(pair not in receipt_index, 'duplicate review pair')
            receipt_index[pair] = (receipt, verdict, document)
    approved_path=a.review_dir/'approved-values.json'
    check(hashlib.sha256(approved_path.read_bytes()).hexdigest() == '809faecd60cfb032f4a03497ae50b7c6851b7ff3f520333b6019d97213543c93', 'approved manifest hash')
    approved=load(approved_path)
    normalized={(tag,e['identity']):e for tag,entries in approved['locales'].items() for e in entries}
    check(len(normalized) == 20, 'normalized scope inventory')
    pairs, counts = set(), {'accept unchanged':0}
    for entry in scopes['new_review_scopes']:
        pair = (entry['locale'], entry['identity'])
        check(pair not in pairs and pair in missing_pairs, 'duplicate/not-new review pair')
        pairs.add(pair)
        receipt, verdict, document = receipt_index[pair]
        check(entry['public_review_sha256'] == receipt['public_export_sha256'], 'scope/receipt hash')
        check(all(entry[k] == v for k,v in normalized[pair].items()), 'scope/approved manifest mismatch')
        check(entry['original_full_value_verdict'] == verdict, 'full original verdict changed or omitted')
        mapping={'source':'source','source_sha256':'source_value_sha256_utf8','display':'final_display_text','xml_text':'final_xml_text',
                 'xml_text_sha256':'final_xml_text_sha256_utf8','display_sha256':'final_display_sha256_utf8' if pair[0]=='ca' else 'final_value_sha256_utf8',
                 'attributes':'final_attributes' if pair[0]=='ca' else 'attributes','qualifications':'qualifications','confidence':'confidence'}
        check(all(entry[k] == verdict[v] for k,v in mapping.items()), 'scope/verdict mismatch')
        current = new_nodes[pair[0]][pair[1]]
        check(content(current) == entry['xml_text'] and dict(current.attributes.items()) == entry['attributes'], 'scope/current value')
        check(base_leaves[pair[1]] == entry['source'], 'scope/source value')
        for field in ('source','display','xml_text'):
            check(hashlib.sha256(entry[field].encode()).hexdigest() == entry[field+'_sha256'], 'scope text hash')
        check(entry['receipt_global_qualifications'] == document['global_qualifications'], 'global qualification changed or omitted')
        check(entry['source_and_current_target_hash_matched'] is True and entry['baseline_target_absent'] is True, 'scope proof flags')
        check(verdict['priority'] == 'P0' and verdict['verdict'] == 'accept' and entry['verdict'] == 'accept unchanged', 'scope kind drift')
        counts[entry['verdict']] += 1
    check(len(pairs) == len(missing_pairs) == len(receipt_index) == 20 and pairs == missing_pairs, 'review join grain')
    check(counts == scopes['new_scope_verdict_counts'] == {'accept unchanged':20}, 'review scope counts')
    check(scopes['per_locale_verdict_counts'] == {'ca':{'accept unchanged':10},'ro':{'accept unchanged':10}}, 'locale verdict count')
    check(scopes['new_disjoint_bounded_AI_whole_value_scopes'] == result['new_reviewed_pairs'] == 20, 'new scope count')
    check(scopes['original_receipt_global_qualifications'] == {tag:doc['global_qualifications'] for tag,doc in documents.items()}, 'receipt globals changed')
    check(scopes['static_composition_examples'] == {tag:doc['static_composition_examples'] for tag,doc in documents.items()}, 'static examples changed')
    inherited_path=a.baseline_report/'review-scope-reconciliation.json'
    inherited=scopes['inherited_scope_binding']; raw=inherited_path.read_bytes()
    check(inherited['sha256'] == hashlib.sha256(raw).hexdigest() and inherited['bytes'] == len(raw) and inherited['git_blob_sha1'] == subprocess.check_output(['git','hash-object',str(inherited_path)],text=True).strip(), 'inherited scope binding')
    check(scopes['global_accepted_count'] is None and result['global_linguistic_categories_recomputed'] is False, 'unsupported global review total')
    check(scopes['native_or_whole_language_certifications'] == 0 and result['absence_implies_defect'] is False and result['English_identical_implies_defect'] is False, 'unsupported acceptance/defect claim')
    expected_categories={'accepted':'preserved; not recounted','qualified':'preserved; not upgraded','clause_only':'preserved; not upgraded','author_only':'preserved; not upgraded','historical':'preserved; not upgraded or revoked','unmatched':'preserved; not guessed','synthetic':'preserved; not upgraded'}
    check(scopes['prior_categories'] == expected_categories, 'inherited scope reclassification')
    expected_holds=['five explicit no-current-consumer P0 holds per ca/ro; 68 other missing P0 values per locale are outside this batch, not newly held','five missing P0 identities per nn/da/no','P1/paired-warning boundaries','global scoped59/fallback112','PR56 never-merge','PR159 freeze','PR113 held/retarget','Help callback/archive identity','interrupted archive','release pause']
    check(result['holds_preserved'] == expected_holds, 'prior hold/pause reclassification')
    check(scopes['prior_catalogue_values_preserved'] == {'ca':127,'ro':127} and scopes['other_option_catalogues_unchanged'] == result['unchanged_options'] == 169, 'preservation summary')
    verification = {'schema':'catalan-romanian-independent-coverage-validation-v1','source_commit':SOURCE,'source_tree':TREE,
        'source_status':result['source_status'],'supplied_merge_receipt_commit_tree_parents_signature_develop_and_pending_run_verified':True,
        'actual_postmerge_run':identity['run']['id'],'actual_postmerge_status_in_supplied_receipt':identity['run']['status'],
        'rows':171,'coverage_inputs_Git_executable_and_SHA256_verified':176,
        'separate_DOM_all_presence_and_English_identity_fields_equal':True,'CSV_JSON_equal':True,
        'prior_values_and_attributes_preserved':{'ca':127,'ro':127},'unchanged_other_options':169,
        'review_join_exact_new_pairs':20,'independent_review_receipt_hashes_verified':2,
        'missing_P0_per_locale':73,'explicit_held_P0_per_locale':5,'outside_batch_not_newly_held_P0_per_locale':68,
        'full_original_per_entry_and_global_qualifications_and_static_examples_preserved':True,
        'prior_scope_categories_not_reclassified':True,'native_linguistic_runtime_or_layout_judgment_added':False}
    return verification


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','report','baseline-report','baseline-source-root','review-dir'):
        parser.add_argument('--' + name, type=Path, required=True)
    a = parser.parse_args()
    result = run(a)
    (a.report / 'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
