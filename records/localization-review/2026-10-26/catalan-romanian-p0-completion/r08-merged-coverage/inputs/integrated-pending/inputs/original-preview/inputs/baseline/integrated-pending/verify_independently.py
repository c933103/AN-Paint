"""Separate DOM, Git-executable, CSV and receipt joins for the integrated coverage delta."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import xml.dom.minidom as DOM

SOURCE = 'ce796879f4568a27b9d905a8e8db639dd0a93a30'
TREE = 'f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c'
BASE = '6a42948a3ac7bad241d502f3b6c18ebf1c0327d8'


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
    rows = load(a.report / 'structural-per-locale.json')
    result = load(a.report / 'coverage-delta.json')
    bindings = load(a.report / 'source-bindings.json')
    filtered_tree = load(a.report / 'coverage-source-tree.json')
    scopes = load(a.report / 'review-scope-reconciliation.json')
    for document in (result, bindings, filtered_tree, scopes):
        check(document['source_commit'] == SOURCE and document['source_tree'] == TREE, 'incorrect fixed head identity')
        check(document['source_status'] == 'integrated source; actual postmerge CI pending in supplied identity receipt', 'incorrect provisional boundary')
    corrected_manifest=a.corrected_report/'manifest.json'
    check(hashlib.sha256(corrected_manifest.read_bytes()).hexdigest()=='cdb497d05be1894167c8d3c25e611ebc75f0f1411c794d064e1ee55ab600607d','preserved corrected provisional manifest')
    for record in load(corrected_manifest)['files']:
        raw=(a.corrected_report/record['path']).read_bytes();check(hashlib.sha256(raw).hexdigest()==record['sha256'] and len(raw)==record['bytes'],'corrected provisional payload changed')
    check(rows==load(a.corrected_report/'structural-per-locale.json'),'merged rows differ from corrected provisional head')
    merge=load(a.report/'source-identity.json')
    check(hashlib.sha256((a.report/'source-identity.json').read_bytes()).hexdigest()=='4cbfeb2373ea2de1b93a615317a0dde8095f7be63b14c4a28931390ad4f24a85','merge receipt exact bytes')
    check(merge['merge_commit']==SOURCE and merge['source_tree']==TREE and merge['ordered_parents']==[BASE,'10acbff912812b938bf2626be1e8a9e84e7aa7bc'] and merge['github_signature_verified'] is True and merge['develop_at_verification']==SOURCE and merge['reviewed_tree_exact_match'] is True,'merge source/parents/signature/develop')
    check(merge['actual_postmerge_run']==40327501312 and merge['actual_postmerge_event']=='push' and merge['actual_postmerge_status']=='pending at this identity record; terminal results separate','actual postmerge pending boundary')
    pr_gate=load(a.report/'corrected-pr-terminal-gates.json');pr_runtime=load(a.report/'corrected-pr-regression-verification.json');pr_tested=load(a.report/'corrected-pr-tested-merge-identity.json')
    check(hashlib.sha256((a.report/'corrected-pr-terminal-gates.json').read_bytes()).hexdigest()=='588d31de90bac36227a225e7bb27fdf1076626a600495ebe18d0307cdf4801c1' and hashlib.sha256((a.report/'corrected-pr-regression-verification.json').read_bytes()).hexdigest()=='9c634cb734b7a5d12ad00a4ab85f3ddbdae7ef2ff4cc36199ecc83fbcee4fc0c','corrected PR receipts')
    check(pr_gate['run']['id']==pr_runtime['run_id']==40323966400 and pr_gate['run']['head_sha']==pr_runtime['reviewed_head']==pr_tested['reviewed_head']=='10acbff912812b938bf2626be1e8a9e84e7aa7bc' and pr_gate['run']['event']=='pull_request' and pr_gate['run']['conclusion']=='success','PR runtime proof source/event')
    check(pr_runtime['tested_commit']==pr_tested['tested_commit']=='fb6b356d6fd87ecbdf79ddc816a92fd87fbfda17' and pr_tested['source_tree']==TREE and pr_tested['ordered_parents']==[BASE,'10acbff912812b938bf2626be1e8a9e84e7aa7bc'] and pr_tested['github_signature_verified'] is True,'PR runtime synthetic source proof')
    tagged=[s for s in pr_runtime['focused_suites'] if s['class']=='TaggedColourImportTest']
    check(len(tagged)==1 and any(c['name']=='everyOfferedLanguageResolvesItsScopedMessageOrExplicitEnglishFallback' and c['passed'] is True for c in tagged[0]['cases']) and all(c['passed'] is True for c in tagged[0]['cases']),'PR inherited oracle passed')
    expected_workflow={'actual_postmerge_run':40327501312,'actual_postmerge_status':'pending in supplied source-identity receipt','receipt_verified_at':merge['verified_at'],'corrected_PR_run':40323966400,'corrected_PR_outcome':'success','PR_results_are_not_postmerge_results':True}
    check(result['workflow_results']==expected_workflow,'PR and actual postmerge results conflated')
    previous_manifest=a.previous_report/'manifest.json'
    check(hashlib.sha256(previous_manifest.read_bytes()).hexdigest()=='49cd2dae0dee1c9fe7bbe2373d47e1f0fb4551dfb33eaa1a2fa874d99efa2fd0','preserved original manifest')
    for record in load(previous_manifest)['files']:
        raw=(a.previous_report/record['path']).read_bytes();check(hashlib.sha256(raw).hexdigest()==record['sha256'] and len(raw)==record['bytes'],'original payload changed')
    check(rows==load(a.previous_report/'structural-per-locale.json'),'test-only correction changed structural rows')
    correction=load(a.report/'head-correction-provenance.json')
    check(correction['source_commit']==SOURCE and correction['source_tree']==TREE and correction['prior_head']=='06a2e4078efa1fe8ef8ea37b186ece0431633f08' and correction['prior_tree']=='949f87f736d4d12de2a92a1834ad35332ab01a1a','correction head pins')
    check(correction['unchanged_blob_identities']==1374 and correction['production_files_changed']==0 and correction['review_value_changes']==0 and correction['original_failed_run']==40319792630 and correction['original_failed_run_result']=='failure','correction outcome/scope')
    expected_changes={'Paintroid/src/test/java/org/catrobat/paintroid/local/TaggedColourImportTest.kt','tools/test_current_localization_contracts.py'}
    check(len(correction['changed_source_files'])==2 and {f['path'] for f in correction['changed_source_files']}==expected_changes,'correction two-test scope')
    expected_prior_blobs={'Paintroid/src/test/java/org/catrobat/paintroid/local/TaggedColourImportTest.kt':'dc0e7ee4580ad9594cfcbbe22b2b616a1c472b13','tools/test_current_localization_contracts.py':'05e17a1223f5fa9c6de4d0121adc3a731f5c33fe'}
    check(correction['prior_manifest_sha256']=='49cd2dae0dee1c9fe7bbe2373d47e1f0fb4551dfb33eaa1a2fa874d99efa2fd0' and correction['corrected_head_CI']=='PR run 40323966400 completed successfully; actual postmerge results separate','correction historical manifest/current CI boundary')
    for record in correction['changed_source_files']:
        check(record['prior_blob']==expected_prior_blobs[record['path']],'prior changed-test blob identity')
        raw=(a.source_root/record['path']).read_bytes();actual=subprocess.check_output(['git','hash-object',str(a.source_root/record['path'])],text=True).strip()
        check(actual==record['source_blob'] and hashlib.sha256(raw).hexdigest()==record['sha256'] and len(raw)==record['bytes'],'corrected test identity')
    for name,expected in [('original-failed-head-gates.json','99e566303b32d2b3d828a3b2cde215b9c339016f6aa64b5e5edc67d53f306e60'),('original-failed-regression-verification.json','6182c9f733e2d9f69c6f980f040cbe2389d95f752bbbd52133d76756847ad8c3')]:
        check(hashlib.sha256((a.report/name).read_bytes()).hexdigest()==expected,'original failure receipt rewritten')
    check(result['head_correction_provenance_file']=='head-correction-provenance.json','missing correction pointer')
    check(result['baseline_commit'] == BASE and bindings['baseline_commit'] == BASE, 'baseline identity')
    check(type(rows) is list and all(type(r) is dict for r in rows), 'row schema')
    check(result['schema'] == 'catalan-romanian-import-integrated-coverage-delta-v1' and result['options'] == 171 and result['canonical_containers'] == 717 and result['canonical_leaves'] == 718, 'declared report schema/denominators')
    check(result['tiers'] == {'P0':92,'P1':249,'P2':305,'P3':71}, 'declared tiers')
    check(filtered_tree['truncated'] is False and filtered_tree['full_blob_count'] == 1376, 'full tree boundary')
    check(bindings['unchanged_source_files'] == 174 and bindings['changed_source_files'] == 2, 'changed input count')
    check(len(rows) == len({r['tag'] for r in rows}) == 171, 'locale inventory')
    check([r['order'] for r in rows] == list(range(1,172)), 'locale order')
    terminal_manifest_path=a.baseline_terminal_report/'manifest.json'
    check(hashlib.sha256(terminal_manifest_path.read_bytes()).hexdigest()=='41218e2f71cf6ced9c44cd800b39a23616c788eb28ee08d3e35a2b03b9ec532a','baseline terminal manifest')
    terminal_manifest=load(terminal_manifest_path)
    for record in terminal_manifest['files']:
        raw=(a.baseline_terminal_report/record['path']).read_bytes()
        check(hashlib.sha256(raw).hexdigest()==record['sha256'] and len(raw)==record['bytes'],'baseline terminal file bytes')
    check((a.report/'baseline-source-identity.json').read_bytes()==(a.baseline_report/'source-identity.json').read_bytes(),'historical baseline receipt changed')
    check((a.report/'baseline-terminal-status.json').read_bytes()==(a.baseline_terminal_report/'terminal-status-supplement.json').read_bytes(),'baseline terminal receipt changed')
    historical=load(a.report/'baseline-source-identity.json');terminal=load(a.report/'baseline-terminal-status.json')
    check(historical['source_commit']==BASE and historical['run']['id']==40311048893 and historical['run']['status']=='in_progress' and historical['run']['conclusion'] is None,'historical baseline pending observation')
    check(terminal['source_commit']==BASE and terminal['source_tree']=='65afa7b96a83c08e0ae08365166dec0520694356' and terminal['run']['id']==40311048893 and terminal['run']['head']==BASE and terminal['run']['event']=='push' and terminal['run']['status']=='completed' and terminal['run']['conclusion']=='success','baseline terminal distinction')
    expected_status={'historical_pending_source_receipt_preserved':True,'actual_postmerge_terminal_run':40311048893,'actual_postmerge_terminal_status':'completed','actual_postmerge_terminal_conclusion':'success','actual_postmerge_terminal_updated_at':terminal['run']['updated_at'],'immutable_report_record':'501c89a0b4e3c908571870f2ef16b1be8eddcfff','baseline_pending_observation_is_not_current_status':True,'new_PR_CI_results_not_inferred':True}
    check(result['baseline_status_evidence']==expected_status,'baseline historical/current distinction')
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
    sums, fields, new_nodes, tagged_colour_present = {}, None, {}, []
    for row in rows:
        containers, leaves, nodes = parse(a.source_root / row['path'])
        if 'string/save20_unsupported_image_colour' in containers:tagged_colour_present.append(row['tag'])
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
    expected_family={'identity':'string/save20_unsupported_image_colour','target_value_present_options':70,'target_value_absent_options':101,'present_tags':tagged_colour_present,'absent_tags':[r['tag'] for r in rows if r['tag'] not in tagged_colour_present],'qualification':'Only this selected P0 resource family; not a replacement for global scoped59/fallback112, not 70 new acceptances or whole-locale acceptance.'}
    expected_runtime={'identity':'string/save20_unsupported_image_colour','direct_catalogue_options':70,'parent_inherited_options':1,'English_default_options':100,'parent_inherited_map':{'ca-ES-valencia':'ca'},'structural_presence_unchanged':[70,101],'new_Valencian_review_acceptance':False,'corrected_PR_runtime_oracle_pass_verified':True,'corrected_PR_run':40323966400,'corrected_PR_tested_commit':'fb6b356d6fd87ecbdf79ddc816a92fd87fbfda17','actual_postmerge_runtime_oracle_pass_not_claimed':True,'evidence_basis':'Original failed JVM evidence observed ca-ES-valencia resolving parent ca rather than English. The corrected PR run 40323966400 passed the complete TaggedColourImportTest oracle at its source-bound synthetic merge. Its runtime partition is 70 direct + 1 parent-inherited + 100 English. This is PR proof, not a new Valencian linguistic acceptance or a claim that actual postmerge run 40327501312 has passed.'}
    check(result['separate_runtime_resolution_qualification']==expected_runtime and 'ca-ES-valencia' in expected_family['absent_tags'] and 'ca' in tagged_colour_present,'runtime inheritance versus structural/acceptance distinction')
    check(len(tagged_colour_present)==70 and result['single_selected_key_structural_presence']==expected_family,'tagged-colour single-key/global distinction')
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
    for tag,count in (('ca',137),('ro',137)):
        path = old_by_tag[tag]['path']
        old_blob = subprocess.check_output(['git','hash-object',str(a.baseline_source_root / path)], text=True).strip()
        check(old_blob == files[path]['baseline_blob'], 'prior source binding')
        _, _, old_nodes[tag] = parse(a.baseline_source_root / path)
        check(len(old_nodes[tag]) == count and len(new_nodes[tag]) == count+13, 'prior/new catalogue count')
        for key,node in old_nodes[tag].items():
            current = new_nodes[tag][key]
            check(content(node) == content(current) and dict(node.attributes.items()) == dict(current.attributes.items()) and node.tagName == current.tagName, 'inherited value/attribute changed')
        missing_pairs.update((tag,key) for key in new_nodes[tag].keys()-old_nodes[tag].keys())
        check(set(result['held_missing_identities_per_locale']).isdisjoint(new_nodes[tag]), 'held identity present')
        after = next(r for r in rows if r['tag'] == tag)
        check(after['P0_present'] == 32 and after['P0_missing'] == 60 and after['all_present'] == 150, 'P0 held coverage')
        check(result['locales_before'][tag] == old_by_tag[tag] and result['locales_after'][tag] == after, 'before/after summary')
    holds = {'string/' + key for key in ('formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png')}
    selected = {'string/' + key for key in ('formats22_animation_message', 'formats22_animation_poster', 'formats22_animation_still', 'formats22_animation_title', 'formats22_animation_unknown', 'formats22_ascii_description', 'formats22_open_still', 'formats22_pdf_raster_hint', 'save20_gif_description', 'save20_invalid_name', 'save20_lossy_quality_description', 'save20_unsupported_image_colour', 'ui_higher_quality_usually_makes_a_larger_file_lossless')}
    check(missing_pairs == {(tag,key) for tag in ('ca','ro') for key in selected}, 'selected identity drift')
    check(set(result['held_missing_identities_per_locale']) == holds, 'held set drift')
    p0 = next(set(t['keys']) for t in tier_data if t['id'] == 'P0')
    for tag in ('ca','ro'):
        missing = p0-new_nodes[tag].keys()
        expected = {'all_missing_P0':sorted(missing), 'explicit_no_current_consumer_holds':sorted(holds),
                    'other_missing_P0_outside_this_batch':sorted(missing-holds), 'missing_count':60,
                    'explicit_hold_count':5, 'outside_batch_count':55, 'outside_batch_is_not_new_hold_or_defect_judgment':True}
        check(len(missing) == 60 and len(missing-holds) == 55 and holds <= missing, 'missing/held/outside counts')
        check(result['remaining_missing_P0_classification'][tag] == scopes['remaining_missing_P0_classification'][tag] == expected, 'missing/held/outside classification')
    check(result['unchanged_previous_added_locales'] == {'nn':190,'da':205,'no':193}, 'inherited locale summary')
    for tag,count in (('nn',190),('da',205),('no',193)):
        row = next(r for r in rows if r['tag'] == tag)
        _,_,nodes = parse(a.source_root / row['path'])
        check(row['all_present'] == count and holds.isdisjoint(nodes), 'prior locale/hold preservation')
    expected_hashes = {'ca':'bc246f0db6a4adfaf55a0f900759587c7a8e2b4766b1a6ad7154b9f7ef38bf0f',
                       'ro':'27974f24343259f1f04cf666035e0e7738161a43a81f812a95048045f914d09d'}
    receipt_index, documents, receipt_locales = {}, {}, set()
    check(len(scopes['review_receipts']) == 2, 'receipt inventory')
    for receipt in scopes['review_receipts']:
        tag=receipt['locale']; check(tag in expected_hashes and tag not in receipt_locales, 'receipt locale duplication')
        receipt_locales.add(tag)
        check(receipt['file'] == tag+'-independent-review.json', 'receipt filename')
        path = a.review_dir / receipt['file']
        check(hashlib.sha256(path.read_bytes()).hexdigest() == receipt['public_export_sha256'] == expected_hashes[tag], 'review bytes differ')
        document = load(path); documents[tag]=document
        check(document['locale'] == tag and document['source_commit'] == BASE and document['source_tree'] == '65afa7b96a83c08e0ae08365166dec0520694356', 'receipt source identity')
        for verdict in document['entries' if tag == 'ca' else 'verdicts']:
            pair = (tag, verdict['identity'])
            check(pair not in receipt_index, 'duplicate review pair')
            receipt_index[pair] = (receipt, verdict, document)
    approved_path=a.review_dir/'approved-values.json'
    check(hashlib.sha256(approved_path.read_bytes()).hexdigest() == '0234033168c0b947805928f1bd64362c784b027f1cf58d9a35d32348d4fa1232', 'approved manifest hash')
    approved=load(approved_path)
    normalized={(tag,e['identity']):e for tag,entries in approved['locales'].items() for e in entries}
    check(len(normalized) == 26, 'normalized scope inventory')
    pairs, counts = set(), {'accept':0,'revise':0}
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
                 'attributes':'final_attributes' if pair[0]=='ca' else 'attributes','qualifications':'qualifications','confidence':'confidence','rationale':'rationale','original_candidate_display':'candidate_display_text','original_candidate_display_sha256':'candidate_value_sha256_utf8'}
        check(all(entry[k] == verdict[v] for k,v in mapping.items()), 'scope/verdict mismatch')
        current = new_nodes[pair[0]][pair[1]]
        check(content(current) == entry['xml_text'] and dict(current.attributes.items()) == entry['attributes'], 'scope/current value')
        check(base_leaves[pair[1]] == entry['source'], 'scope/source value')
        for field in ('source','display','xml_text'):
            check(hashlib.sha256(entry[field].encode()).hexdigest() == entry[field+'_sha256'], 'scope text hash')
        check(entry['receipt_global_qualifications'] == document['global_qualifications'], 'global qualification changed or omitted')
        check(entry['source_and_current_target_hash_matched'] is True and entry['baseline_target_absent'] is True, 'scope proof flags')
        decision=verdict['verdict']
        check(verdict['priority'] == 'P0' and decision in ('accept','revise'), 'scope kind drift')
        check(entry['verdict'] == ('accepted unchanged' if decision=='accept' else 'accepted exact independently reviewed replacement'), 'normalized acceptance kind')
        check(verdict['accepted_unchanged' if pair[0]=='ca' else 'candidate_unchanged'] is (decision=='accept'), 'decision unchanged flag')
        check((pair==('ca','string/formats22_ascii_description')) == (decision=='revise'), 'exact revision identity')
        check(hashlib.sha256(entry['original_candidate_display'].encode()).hexdigest()==entry['original_candidate_display_sha256'] and ((entry['original_candidate_display']==entry['display']) == (decision=='accept')), 'original candidate/final distinction')
        counts[decision] += 1
    check(len(pairs) == len(missing_pairs) == len(receipt_index) == 26 and pairs == missing_pairs, 'review join grain')
    check(counts == scopes['new_scope_verdict_counts'] == {'accept':25,'revise':1}, 'review scope counts')
    check(scopes['per_locale_verdict_counts'] == {'ca':{'accept':12,'revise':1},'ro':{'accept':13}}, 'locale verdict count')
    check(scopes['new_disjoint_bounded_AI_whole_value_scopes'] == result['new_reviewed_pairs'] == 26, 'new scope count')
    check(scopes['original_receipt_global_qualifications'] == {tag:doc['global_qualifications'] for tag,doc in documents.items()}, 'receipt globals changed')
    check(scopes['static_composition_examples'] == {tag:doc['static_composition_examples'] for tag,doc in documents.items()}, 'static examples changed')
    inherited_path=a.baseline_report/'review-scope-reconciliation.json'
    inherited=scopes['inherited_scope_binding']; raw=inherited_path.read_bytes()
    check(inherited['sha256'] == hashlib.sha256(raw).hexdigest() and inherited['bytes'] == len(raw) and inherited['git_blob_sha1'] == subprocess.check_output(['git','hash-object',str(inherited_path)],text=True).strip(), 'inherited scope binding')
    check(scopes['global_accepted_count'] is None and result['global_linguistic_categories_recomputed'] is False, 'unsupported global review total')
    check(scopes['native_or_whole_language_certifications'] == 0 and result['absence_implies_defect'] is False and result['English_identical_implies_defect'] is False, 'unsupported acceptance/defect claim')
    expected_categories={'accepted':'preserved; not recounted','qualified':'preserved; not upgraded','clause_only':'preserved; not upgraded','author_only':'preserved; not upgraded','historical':'preserved; not upgraded or revoked','unmatched':'preserved; not guessed','synthetic':'preserved; not upgraded'}
    check(scopes['prior_categories'] == expected_categories, 'inherited scope reclassification')
    expected_holds=['five explicit no-current-consumer P0 holds per ca/ro; 55 other missing P0 values per locale are outside this batch, not newly held','five missing P0 identities per nn/da/no','P1/paired-warning boundaries','global scoped59/fallback112','PR56 never-merge','PR159 freeze','PR113 held/retarget','Help callback/archive identity','interrupted archive','release pause']
    check(result['holds_preserved'] == expected_holds, 'prior hold/pause reclassification')
    check(scopes['prior_catalogue_values_preserved'] == {'ca':137,'ro':137} and scopes['other_option_catalogues_unchanged'] == result['unchanged_options'] == 169, 'preservation summary')
    verification = {'schema':'catalan-romanian-independent-coverage-validation-v1','source_commit':SOURCE,'source_tree':TREE,
        'source_status':result['source_status'],'rows':171,'coverage_inputs_Git_executable_and_SHA256_verified':176,
        'separate_DOM_all_presence_and_English_identity_fields_equal':True,'CSV_JSON_equal':True,
        'prior_values_and_attributes_preserved':{'ca':137,'ro':137},'unchanged_other_options':169,
        'review_join_exact_new_pairs':26,'independent_review_receipt_hashes_verified':2,
        'missing_P0_per_locale':60,'explicit_held_P0_per_locale':5,'outside_batch_not_newly_held_P0_per_locale':55,
        'full_original_per_entry_and_global_qualifications_and_static_examples_preserved':True,
        'baseline_historical_pending_and_separate_terminal_preserved':True,'tagged_colour_single_key_structural_present_absent':[70,101],
        'test_only_head_correction_preserves_all_structural_rows_and_original_failure':True,'runtime_parent_inheritance_not_new_acceptance':True,
        'actual_merge_identity_and_pending_push_separate_from_passing_PR_runtime':True,
        'prior_scope_categories_not_reclassified':True,'native_linguistic_runtime_or_layout_judgment_added':False}
    return verification


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','report','corrected-report','previous-report','baseline-report','baseline-terminal-report','baseline-source-root','review-dir'):
        parser.add_argument('--' + name, type=Path, required=True)
    a = parser.parse_args()
    result = run(a)
    (a.report / 'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
