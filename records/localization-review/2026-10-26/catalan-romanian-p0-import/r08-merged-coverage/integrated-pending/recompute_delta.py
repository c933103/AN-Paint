"""Recompute the pinned integrated PR177 coverage delta; no application code or network executes."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BASE_COMMIT = '6a42948a3ac7bad241d502f3b6c18ebf1c0327d8'
BASE_TREE = '65afa7b96a83c08e0ae08365166dec0520694356'
SOURCE_COMMIT = 'ce796879f4568a27b9d905a8e8db639dd0a93a30'
SOURCE_TREE = 'f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c'
APPROVED_SHA256 = '0234033168c0b947805928f1bd64362c784b027f1cf58d9a35d32348d4fa1232'
BASE_MANIFEST_SHA256 = 'a52598bf8ef983a2016a7e8f0fab6e6843cf368bb7f4ea6cd708e6be6ceabe7b'
STATUS = 'integrated source; actual postmerge CI pending in supplied identity receipt'
LOCALES = {'ca': ('Paintroid/src/main/res/values-ca/strings.xml', 137),
           'ro': ('Paintroid/src/main/res/values-ro/strings.xml', 137)}
RECEIPTS = {'ca': ('ca-independent-review.json', 'bc246f0db6a4adfaf55a0f900759587c7a8e2b4766b1a6ad7154b9f7ef38bf0f'),
            'ro': ('ro-independent-review.json', '27974f24343259f1f04cf666035e0e7738161a43a81f812a95048045f914d09d')}
SELECTED = {'string/' + key for key in ('formats22_animation_message', 'formats22_animation_poster', 'formats22_animation_still', 'formats22_animation_title', 'formats22_animation_unknown', 'formats22_ascii_description', 'formats22_open_still', 'formats22_pdf_raster_hint', 'save20_gif_description', 'save20_invalid_name', 'save20_lossy_quality_description', 'save20_unsupported_image_colour', 'ui_higher_quality_usually_makes_a_larger_file_lossless')}
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


def verify_tree(tree, expected_tree=SOURCE_TREE):
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
    baseline_identity = bind(a.baseline_report / 'source-identity.json', 'baseline-report/source-identity.json')
    require(baseline_identity['source_commit'] == BASE_COMMIT and baseline_identity['source_tree'] == BASE_TREE and baseline_identity['run']['id'] == 40311048893 and baseline_identity['run']['status'] == 'in_progress', 'historical baseline identity')
    terminal_manifest = bind(a.baseline_terminal_report / 'manifest.json', 'baseline-terminal-report/manifest.json')
    require(inputs[-1]['sha256'] == '41218e2f71cf6ced9c44cd800b39a23616c788eb28ee08d3e35a2b03b9ec532a', 'wrong baseline terminal manifest')
    for record in terminal_manifest['files']:
        raw = (a.baseline_terminal_report / record['path']).read_bytes()
        require(sha(raw) == record['sha256'] and git(raw) == record['git_blob_sha1'] and len(raw) == record['bytes'], 'baseline terminal package changed')
    terminal = bind(a.baseline_terminal_report / 'terminal-status-supplement.json', 'baseline-terminal-report/terminal-status-supplement.json')
    require(terminal['source_commit'] == BASE_COMMIT and terminal['source_tree'] == BASE_TREE and terminal['run']['id'] == 40311048893 and terminal['run']['head'] == BASE_COMMIT and terminal['run']['event'] == 'push' and terminal['run']['status'] == 'completed' and terminal['run']['conclusion'] == 'success', 'separate baseline terminal result')
    baseline_status = {'historical_pending_source_receipt_preserved':True,'actual_postmerge_terminal_run':40311048893,'actual_postmerge_terminal_status':'completed','actual_postmerge_terminal_conclusion':'success','actual_postmerge_terminal_updated_at':terminal['run']['updated_at'],'immutable_report_record':'501c89a0b4e3c908571870f2ef16b1be8eddcfff','baseline_pending_observation_is_not_current_status':True,'new_PR_CI_results_not_inferred':True}
    rows_before = bind(a.baseline_report / 'structural-per-locale.json', 'baseline-report/structural-per-locale.json')
    summary_before = bind(a.baseline_report / 'coverage-delta.json', 'baseline-report/coverage-delta.json')
    provenance = bind(a.baseline_report / 'source-bindings.json', 'baseline-report/source-bindings.json')
    require(len(rows_before) == 171 and len({r['tag'] for r in rows_before}) == 171, 'baseline row inventory')
    require(summary_before['source_commit'] == provenance['source_commit'] == BASE_COMMIT and summary_before['source_tree'] == BASE_TREE, 'wrong baseline source')
    corrected_manifest = bind(a.corrected_report/'manifest.json','corrected-provisional-report/manifest.json')
    require(inputs[-1]['sha256']=='cdb497d05be1894167c8d3c25e611ebc75f0f1411c794d064e1ee55ab600607d','corrected provisional manifest')
    for record in corrected_manifest['files']:
        raw=(a.corrected_report/record['path']).read_bytes()
        require(sha(raw)==record['sha256'] and git(raw)==record['git_blob_sha1'] and len(raw)==record['bytes'],'corrected provisional payload changed')
    merge=bind(a.merge_identity,'source-identity.json')
    require(inputs[-1]['sha256']=='4cbfeb2373ea2de1b93a615317a0dde8095f7be63b14c4a28931390ad4f24a85','merge identity receipt bytes')
    require(merge['repository']=='c933103/AN-Paint' and merge['merge_commit']==SOURCE_COMMIT and merge['source_tree']==SOURCE_TREE and merge['ordered_parents']==[BASE_COMMIT,'10acbff912812b938bf2626be1e8a9e84e7aa7bc'] and merge['github_signature_verified'] is True and merge['reviewed_tree_exact_match'] is True,'actual merge source/parents/signature')
    require(merge['develop_at_verification']==SOURCE_COMMIT and merge['source_tracked_blobs']==1376 and merge['reviewed_head']=='10acbff912812b938bf2626be1e8a9e84e7aa7bc','explicit develop/reviewed source identity')
    require(merge['pull_request']['number']==177 and merge['pull_request']['merged'] is True and merge['pull_request']['merge_commit_sha']==SOURCE_COMMIT and merge['actual_postmerge_run']==40327501312 and merge['actual_postmerge_event']=='push' and merge['actual_postmerge_status']=='pending at this identity record; terminal results separate','pending actual postmerge binding')
    pr_gate=bind(a.pr_terminal_dir/'terminal-gates.json','corrected-pr/terminal-gates.json')
    require(inputs[-1]['sha256']=='588d31de90bac36227a225e7bb27fdf1076626a600495ebe18d0307cdf4801c1' and pr_gate['run']['id']==40323966400 and pr_gate['run']['head_sha']=='10acbff912812b938bf2626be1e8a9e84e7aa7bc' and pr_gate['run']['event']=='pull_request' and pr_gate['run']['conclusion']=='success','corrected PR gate identity/outcome')
    pr_regression=bind(a.pr_terminal_dir/'hosted-regression-verification.json','corrected-pr/hosted-regression-verification.json')
    require(inputs[-1]['sha256']=='9c634cb734b7a5d12ad00a4ab85f3ddbdae7ef2ff4cc36199ecc83fbcee4fc0c' and pr_regression['run_id']==40323966400 and pr_regression['reviewed_head']=='10acbff912812b938bf2626be1e8a9e84e7aa7bc' and pr_regression['junit_totals']=={'tests':1361,'failures':0,'errors':0,'skipped':0},'corrected PR runtime receipt')
    pr_tested=bind(a.pr_terminal_dir/'tested-merge-identity.json','corrected-pr/tested-merge-identity.json')
    require(pr_tested['tested_commit']==pr_regression['tested_commit']=='fb6b356d6fd87ecbdf79ddc816a92fd87fbfda17' and pr_tested['source_tree']==SOURCE_TREE and pr_tested['reviewed_head']=='10acbff912812b938bf2626be1e8a9e84e7aa7bc' and pr_tested['ordered_parents']==[BASE_COMMIT,'10acbff912812b938bf2626be1e8a9e84e7aa7bc'] and pr_tested['github_signature_verified'] is True,'corrected PR synthetic tested-source binding')
    tagged=[s for s in pr_regression['focused_suites'] if s['class']=='TaggedColourImportTest']
    require(len(tagged)==1 and any(c['name']=='everyOfferedLanguageResolvesItsScopedMessageOrExplicitEnglishFallback' and c['passed'] is True for c in tagged[0]['cases']) and all(c['passed'] is True for c in tagged[0]['cases']),'actual inherited runtime oracle passed in PR')
    tree = bind(a.source_tree_file, 'source-tree.json')
    blobs = verify_tree(tree)
    prior_manifest = bind(a.previous_report / 'manifest.json', 'previous-provisional-report/manifest.json')
    require(inputs[-1]['sha256'] == '49cd2dae0dee1c9fe7bbe2373d47e1f0fb4551dfb33eaa1a2fa874d99efa2fd0', 'original provisional manifest')
    for record in prior_manifest['files']:
        raw = (a.previous_report / record['path']).read_bytes()
        require(sha(raw) == record['sha256'] and git(raw) == record['git_blob_sha1'] and len(raw) == record['bytes'], 'original provisional payload changed')
    prior_tree = bind(a.previous_head_tree, 'previous-provisional-head-tree.json')
    prior_blobs = verify_tree(prior_tree, '949f87f736d4d12de2a92a1834ad35332ab01a1a')
    changed_paths = {p for p in prior_blobs.keys() | blobs.keys() if prior_blobs.get(p,{}).get('sha') != blobs.get(p,{}).get('sha')}
    expected_changes = {'Paintroid/src/test/java/org/catrobat/paintroid/local/TaggedColourImportTest.kt','tools/test_current_localization_contracts.py'}
    require(changed_paths == expected_changes and prior_blobs.keys() == blobs.keys() and len(blobs)==1376, 'correction exceeds two test files')
    correction_files = []
    for path in sorted(changed_paths):
        raw=(a.source_root/path).read_bytes()
        require(git(raw)==blobs[path]['sha'] and len(raw)==blobs[path]['size'],'corrected test source hash')
        correction_files.append({'path':path,'prior_blob':prior_blobs[path]['sha'],'source_blob':blobs[path]['sha'],'sha256':sha(raw),'bytes':len(raw)})
    failed_gate = bind(a.failure_evidence/'failed-head-gates.json','original-failed-head/failed-head-gates.json')
    require(inputs[-1]['sha256']=='99e566303b32d2b3d828a3b2cde215b9c339016f6aa64b5e5edc67d53f306e60','original failed gate hash')
    failed = bind(a.failure_evidence/'failed-regression-verification.json','original-failed-head/failed-regression-verification.json')
    require(inputs[-1]['sha256']=='6182c9f733e2d9f69c6f980f040cbe2389d95f752bbbd52133d76756847ad8c3','original failed regression hash')
    require(failed_gate['run']['id']==40319792630 and failed_gate['run']['head_sha']=='06a2e4078efa1fe8ef8ea37b186ece0431633f08' and failed_gate['run']['conclusion']=='failure' and failed['junit_totals']['failures']==1 and len(failed['failed_cases'])==1 and 'ca-ES-valencia' in failed['failed_cases'][0]['message'],'original failed run identity/outcome')
    correction = {'prior_head':'06a2e4078efa1fe8ef8ea37b186ece0431633f08','prior_tree':'949f87f736d4d12de2a92a1834ad35332ab01a1a','prior_manifest_sha256':'49cd2dae0dee1c9fe7bbe2373d47e1f0fb4551dfb33eaa1a2fa874d99efa2fd0','changed_source_files':correction_files,'unchanged_blob_identities':1374,'production_files_changed':0,'review_value_changes':0,'original_failed_run':40319792630,'original_failed_run_result':'failure','original_failure_record':'https://github.com/c933103/AN-Paint/tree/fe8f255de677c1a1a843f70a4c7800f40916cc5a/records/localization-review/2026-10-26/catalan-romanian-p0-import/r04-original-head-failure','reviewed_corrected_head':'10acbff912812b938bf2626be1e8a9e84e7aa7bc','corrected_PR_terminal_records_commit':'4700fd58aa4e5637793157eaadeffafa2d261b84','corrected_head_CI':'PR run 40323966400 completed successfully; actual postmerge results separate'}

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
        require(git(raw) == entry['sha'] and len(raw) == entry['size'], 'head source/tree mismatch: ' + path)
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
    rows, locale_nodes, tagged_colour_present = [], {}, []
    for before in rows_before:
        path = before['path']
        containers, leaves, nodes = parse(source[path])
        row = {k: before[k] for k in ('order','tag','path')}
        row['blob'] = blobs[path]['sha']
        if 'string/save20_unsupported_image_colour' in containers: tagged_colour_present.append(row['tag'])
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
    require({k:v for k,v in delta.items() if v} == {'P0_present':26,'P0_missing':-26,'all_present':26,'all_missing':-26,'leaves_present':26,'leaves_missing':-26,'leaves_source_different':26}, 'unexpected aggregate delta')
    require(rows == read(a.corrected_report/'structural-per-locale.json'),'merged rows differ from reviewed corrected head')
    require(rows == read(a.previous_report/'structural-per-locale.json'),'structural rows changed in test-only correction')
    require(len(tagged_colour_present) == 70, 'selected tagged-colour key structural count')
    single_key_scope = {'identity':'string/save20_unsupported_image_colour','target_value_present_options':70,'target_value_absent_options':101,'present_tags':tagged_colour_present,'absent_tags':[tag for tag in tags if tag not in tagged_colour_present],'qualification':'Only this selected P0 resource family; not a replacement for global scoped59/fallback112, not 70 new acceptances or whole-locale acceptance.'}
    require('ca-ES-valencia' in single_key_scope['absent_tags'] and 'ca' in tagged_colour_present,'parent-inheritance structural preconditions')
    runtime_qualification = {'identity':'string/save20_unsupported_image_colour','direct_catalogue_options':70,'parent_inherited_options':1,'English_default_options':100,'parent_inherited_map':{'ca-ES-valencia':'ca'},'structural_presence_unchanged':[70,101],'new_Valencian_review_acceptance':False,'corrected_PR_runtime_oracle_pass_verified':True,'corrected_PR_run':40323966400,'corrected_PR_tested_commit':'fb6b356d6fd87ecbdf79ddc816a92fd87fbfda17','actual_postmerge_runtime_oracle_pass_not_claimed':True,'evidence_basis':'Original failed JVM evidence observed ca-ES-valencia resolving parent ca rather than English. The corrected PR run 40323966400 passed the complete TaggedColourImportTest oracle at its source-bound synthetic merge. Its runtime partition is 70 direct + 1 parent-inherited + 100 English. This is PR proof, not a new Valencian linguistic acceptance or a claim that actual postmerge run 40327501312 has passed.'}
    prior_nodes = {}
    for tag, (path, count) in LOCALES.items():
        raw = (a.baseline_source_root / path).read_bytes()
        inputs.append(file_binding(a.baseline_source_root / path, 'baseline-source/' + path))
        require(git(raw) == baseline_files[path]['source_blob'] and sha(raw) == baseline_files[path]['sha256'], 'wrong prior catalogue bytes')
        _, _, old = parse(raw)
        new = locale_nodes[tag]
        require(len(old) == count and len(new) == count + 13, 'locale value count')
        for key, node in old.items():
            require(key in new and fingerprint(node) == fingerprint(new[key]), 'changed inherited value: ' + tag + '/' + key)
        require(set(new) - set(old) <= tiers['P0'], 'non-P0 addition')
        require(HOLDS.isdisjoint(new), 'held identity present')
        require(len(tiers['P0'] - new.keys()) == 60 and len((tiers['P0'] - new.keys()) - HOLDS) == 55, 'remaining P0 missing/outside-batch counts differ')
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
                              public_record='https://github.com/c933103/AN-Paint/blob/9049ae41bee76f0d74c9160bb738d19aff6abe90/records/localization-review/2026-10-26/catalan-romanian-p0-import/r02-reviewed/' + name)
        entries = document['entries' if tag == 'ca' else 'verdicts']
        require(len(entries) == 13, 'independent verdict count')
        for verdict in entries:
            pair = (tag, verdict['identity'])
            require(pair not in verdicts, 'duplicate reviewed pair')
            verdicts[pair] = verdict
    new_scopes, decisions, per_locale = [], collections.Counter(), {}
    for tag, entries in review['locales'].items():
        require(len(entries) == len({e['identity'] for e in entries}) == 13, 'approved per-locale grain')
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
                'attributes':'final_attributes' if tag == 'ca' else 'attributes', 'qualifications':'qualifications', 'confidence':'confidence','rationale':'rationale','original_candidate_display':'candidate_display_text','original_candidate_display_sha256':'candidate_value_sha256_utf8'}
            require(all(entry[k] == verdict[v] for k,v in comparisons.items()), 'normalized/review value or qualification mismatch')
            decision = verdict['verdict']
            require(verdict['priority'] == 'P0' and decision in ('accept','revise'), 'not accepted/revised P0')
            require(verdict['accepted_unchanged' if tag == 'ca' else 'candidate_unchanged'] is (decision == 'accept'), 'unchanged decision flag differs')
            require(entry['verdict'] == ('accepted unchanged' if decision == 'accept' else 'accepted exact independently reviewed replacement'), 'nonaccepted normalized scope')
            require((tag,key,decision) != ('ca','string/formats22_ascii_description','accept') and (decision != 'revise' or (tag,key) == ('ca','string/formats22_ascii_description')), 'unexpected revision scope')
            node = locale_nodes[tag][key]
            require(not list(node) and node.text == entry['xml_text'] and node.attrib == entry['attributes'], 'current XML/review mismatch')
            require(base[key] == entry['source'] and sha(entry['source'].encode()) == entry['source_sha256'], 'review source mismatch')
            require(sha(node.text.encode()) == entry['xml_text_sha256'] and sha(entry['display'].encode()) == entry['display_sha256'], 'review target hash mismatch')
            require(tokens(entry['source']) == tokens(entry['display']), 'format token mismatch')
            require(sha(entry['original_candidate_display'].encode()) == entry['original_candidate_display_sha256'], 'original candidate hash')
            require((entry['original_candidate_display'] == entry['display']) == (decision == 'accept'), 'candidate/final decision mismatch')
            decisions[decision] += 1; local_decisions[decision] += 1
            new_scopes.append(dict(entry, locale=tag, public_review_sha256=receipt_hash,
                                   source_and_current_target_hash_matched=True, baseline_target_absent=True,
                                   original_full_value_verdict=verdict,
                                   receipt_global_qualifications=documents[tag]['global_qualifications']))
        per_locale[tag] = dict(local_decisions)
    require(len(new_scopes) == len(verdicts) == 26 and decisions == {'accept':25,'revise':1}, 'final reviewed scope accounting')
    remaining = {tag: {'all_missing_P0': sorted(tiers['P0'] - locale_nodes[tag].keys()),
                      'explicit_no_current_consumer_holds': sorted(HOLDS),
                      'other_missing_P0_outside_this_batch': sorted((tiers['P0'] - locale_nodes[tag].keys()) - HOLDS),
                      'missing_count':60, 'explicit_hold_count':5, 'outside_batch_count':55,
                      'outside_batch_is_not_new_hold_or_defect_judgment':True} for tag in LOCALES}
    out = a.out; out.mkdir(parents=True, exist_ok=True)
    (out / 'baseline-source-identity.json').write_bytes((a.baseline_report / 'source-identity.json').read_bytes())
    (out / 'baseline-terminal-status.json').write_bytes((a.baseline_terminal_report / 'terminal-status-supplement.json').read_bytes())
    emit(out, 'head-correction-provenance.json', dict(correction,source_commit=SOURCE_COMMIT,source_tree=SOURCE_TREE,source_status=STATUS))
    (out/'original-failed-head-gates.json').write_bytes((a.failure_evidence/'failed-head-gates.json').read_bytes())
    (out/'original-failed-regression-verification.json').write_bytes((a.failure_evidence/'failed-regression-verification.json').read_bytes())
    (out/'source-identity.json').write_bytes(a.merge_identity.read_bytes())
    for public_name,source_name in [('corrected-pr-terminal-gates.json','terminal-gates.json'),('corrected-pr-regression-verification.json','hosted-regression-verification.json'),('corrected-pr-tested-merge-identity.json','tested-merge-identity.json')]:
        (out/public_name).write_bytes((a.pr_terminal_dir/source_name).read_bytes())
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
         'new_disjoint_bounded_AI_whole_value_scopes':26,'new_scope_verdict_counts':dict(decisions),'per_locale_verdict_counts':per_locale,
         'prior_catalogue_values_preserved':{'ca':137,'ro':137},'other_option_catalogues_unchanged':169,
         'prior_categories':{'accepted':'preserved; not recounted','qualified':'preserved; not upgraded','clause_only':'preserved; not upgraded',
            'author_only':'preserved; not upgraded','historical':'preserved; not upgraded or revoked','unmatched':'preserved; not guessed','synthetic':'preserved; not upgraded'},
         'global_accepted_count':None,'global_count_not_recomputed_reason':'This is an exact missing-only source delta, not a rerun or replacement of the inherited review ledger. Only the 26 previously absent locale/identity pairs are newly receipt-bound; all prior source values and their prior scope classifications remain unchanged.',
         'native_or_whole_language_certifications':0,'new_review_scopes':new_scopes,'review_receipts':list(receipts.values()),
         'original_receipt_global_qualifications':review['global_qualifications'],
         'inherited_scope_binding':inherited_binding,
         'remaining_missing_P0_classification':remaining,
         'static_composition_examples':{tag:doc['static_composition_examples'] for tag,doc in documents.items()}})
    result = {'schema':'catalan-romanian-import-integrated-coverage-delta-v1','baseline_commit':BASE_COMMIT,'baseline_tree':BASE_TREE,'baseline_status_evidence':baseline_status,
         'single_selected_key_structural_presence':single_key_scope,'separate_runtime_resolution_qualification':runtime_qualification,'head_correction_provenance_file':'head-correction-provenance.json',
         'source_commit':SOURCE_COMMIT,'source_tree':SOURCE_TREE,'source_status':STATUS,'options':171,'canonical_containers':717,'canonical_leaves':718,
         'tiers':{k:len(v) for k,v in tiers.items()},'presence_totals':totals,'presence_delta':delta,
         'full_presence_options':sum(r['all_missing']==0 for r in rows),'zero_presence_options':sum(r['all_present']==0 for r in rows),
         'locales_before':{tag:next(r for r in rows_before if r['tag']==tag) for tag in LOCALES},
         'locales_after':{tag:next(r for r in rows if r['tag']==tag) for tag in LOCALES},
         'unchanged_options':169,'unchanged_previous_added_locales':{'nn':190,'da':205,'no':193},'held_missing_identities_per_locale':sorted(HOLDS),
         'remaining_missing_P0_classification':remaining,
         'new_reviewed_pairs':26,'review_scope':'bounded independent AI whole-value linguistic/source-static; per-entry/global qualifications preserved, not native-human/device/layout/whole-language acceptance',
         'global_linguistic_categories_recomputed':False,'absence_implies_defect':False,'English_identical_implies_defect':False,
         'counting_policy':'Same XML-decoded exact leaf-text comparison as prior structural snapshot; quote wrapping is not normalized and runtime fallback is not counted as target presence.',
         'workflow_results':{'actual_postmerge_run':40327501312,'actual_postmerge_status':'pending in supplied source-identity receipt','receipt_verified_at':merge['verified_at'],'corrected_PR_run':40323966400,'corrected_PR_outcome':'success','PR_results_are_not_postmerge_results':True},'source_identity_proof':'The supplied authenticated-connector merge receipt is byte-bound and its ordered parents, signature, explicit develop ref, tree and pending push identity are checked locally; no fresh network verification is performed.',
         'holds_preserved':['five explicit no-current-consumer P0 holds per ca/ro; 55 other missing P0 values per locale are outside this batch, not newly held','five missing P0 identities per nn/da/no','P1/paired-warning boundaries','global scoped59/fallback112','PR56 never-merge','PR159 freeze','PR113 held/retarget','Help callback/archive identity','interrupted archive','release pause']}
    emit(out, 'coverage-delta.json', result)
    print(json.dumps({'source_commit':SOURCE_COMMIT,'source_status':STATUS,'totals':totals,'delta':delta,'reviewed_pairs':26,'verdict_counts':dict(decisions)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','source-tree-file','corrected-report','merge-identity','pr-terminal-dir','previous-report','previous-head-tree','failure-evidence','baseline-report','baseline-terminal-report','baseline-source-root','review-dir','out'):
        parser.add_argument('--' + name, type=Path, required=True)
    run(parser.parse_args())


if __name__ == '__main__':
    main()
