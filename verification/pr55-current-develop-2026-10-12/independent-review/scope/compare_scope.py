#!/usr/bin/env python3
"""One-time PR55 integration comparison, deliberately outside normal application CI.

Uses explicit Git trees and the candidate index; never temporary HEAD identities.
Reads repositories only. Emits a bounded JSON summary, not full-tree inventories.
Standard-library Python 3 plus Git. No Android or application test execution.
"""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

PR55_COMMIT = '6d603af92ee26d852af62cd1006468ef8472bfcf'
PR55_TREE = 'd2379b932cc976bb5347515887ecdfc4729ee70d'
DEVELOP_COMMIT = '484d1b31cb113c88351e6d0dbdaa0d503e5dd834'
DEVELOP_TREE = '8d4e32c937cf9ab2d1efa7ca378d20341166f492'
INCOMING_BASE_TREE = 'c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1'
FROZEN_TREE = 'b5d8cbeac9bf6d613ed7c3be787aa984826daafd'
ADDED_TAGS = set('as ch chr ha ht ig ln mi nch nhe nhw nv pcm qug quh quy quz sa sm so su tg tpi wo yo yua zu'.split())
FIX = 'tools/fixtures/current_localization/'
JVM = 'Paintroid/src/test/java/org/catrobat/paintroid/local/'
REGISTRATION = {'Paintroid/src/main/res/values/app_language_names.xml',
                'Paintroid/src/main/res/values/app_language_tags.xml',
                'Paintroid/src/main/res/xml/app_locales.xml'}
JVM_NAMES = ('AppLanguageTest CommonsCopyCreditTranslationTest CommonsHelpProviderTranslationTest '
             'CommonsMetadataHttpTranslationTest CommonsMetadataQueryFailureTranslationTest '
             'CommonsMetadataResponseLimitTranslationTest DeviceLanguagePickerTest '
             'GalleryBackDirectionTest LocaleNumberInputTest LocaleTooltipTest').split()
WORDING = ('commons_copy_credit_current_wording.json commons_metadata_current_wording.json '
           'commons_svg_current_wording.json help_commons_provider_current_contract.json').split()
FIXTURE_NAMES = WORDING + ['commons_import_current_wording.json', 'locale_contract_scope.json', 'wording-provenance.json']
ALLOWED_MODIFIED = REGISTRATION | {JVM+n+'.kt' for n in JVM_NAMES} | {FIX+n for n in FIXTURE_NAMES} | {
    'CI.md', 'TRANSLATING.md', 'tools/current_localization_contracts.py',
    'tools/test_commons_import_change_translations.py', 'tools/test_current_localization_contracts.py',
    'tools/test_help_commons_provider.py', 'translations/language-options.json', 'verification/README.md'}
OPTION_FILES = {'tools/fixtures/language_option_additions_20261012.json',
                'tools/fixtures/language_option_additions_20261012_second.json',
                'tools/language_option_additions.py', 'tools/test_language_option_additions.py',
                'tools/test_language_option_additions_second.py'}
CATALOGUES = {f'Paintroid/src/main/res/values-b+{t}/strings.xml' for t in ADDED_TAGS}
RETIRED = {'tools/fixtures/language_option_historical_evidence.json',
           'tools/test_commons_copy_credit_errors.py', 'tools/test_commons_metadata_m03.py'}
ARCHIVE_PREFIXES = ('verification/language-options-2026-10-12/',
                    'verification/language-options-second-2026-10-12/',
                    'verification/language-options-superseded-162-2026-10-12/')

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def manifest(repo, ref=None):
    result = {}
    data = git(repo, 'ls-tree', '-rz', ref) if ref else git(repo, 'ls-files', '-sz')
    for record in data.split(b'\0'):
        if not record: continue
        meta, path = record.split(b'\t', 1)
        a, b, c = meta.decode().split()
        if ref:
            if b != 'blob': raise ValueError('Unexpected non-blob: '+path.decode())
            result[path.decode()] = (a, c)
        else:
            if c != '0': raise ValueError('Unmerged index: '+path.decode())
            result[path.decode()] = (a, b)
    return result

def object_hash(kind, data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()

def tree_hash(files):
    root = {}
    for path, item in files.items():
        node = root
        parts = path.split('/')
        for part in parts[:-1]: node = node.setdefault(part, {})
        node[parts[-1]] = item
    def digest(node):
        data = b''
        for name in sorted(node, key=lambda n: (n+'/' if isinstance(node[n], dict) else n).encode()):
            value = node[name]
            mode, sha = ('40000', digest(value)) if isinstance(value, dict) else value
            data += mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)
        return object_hash('tree', data)
    return digest(root)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', required=True, type=Path)
    parser.add_argument('--develop', required=True, type=Path)
    parser.add_argument('--incoming-base', required=True, type=Path)
    args = parser.parse_args()
    c, d, p, b = (manifest(args.candidate), manifest(args.develop, DEVELOP_TREE),
                  manifest(args.candidate, PR55_TREE), manifest(args.incoming_base, INCOMING_BASE_TREE))
    failures = []
    passed = []
    def check(name, condition):
        (passed if condition else failures).append(name)
    def raw(repo, files, path): return git(repo, 'cat-file', 'blob', files[path][1])
    def cc(path): return raw(args.candidate, c, path)
    def pp(path): return raw(args.candidate, p, path)
    def dd(path): return raw(args.develop, d, path)
    def cj(path): return json.loads(cc(path))
    def pj(path): return json.loads(pp(path))
    def dj(path): return json.loads(dd(path))
    candidate_tree = tree_hash(c)
    check('candidate index equals frozen tree', candidate_tree == FROZEN_TREE)
    check('accepted tree pins verified independently', (tree_hash(p), tree_hash(d), tree_hash(b)) == (PR55_TREE, DEVELOP_TREE, INCOMING_BASE_TREE))
    worktree_differences = []
    for path, (mode, sha) in c.items():
        item = args.candidate/path
        if item.is_symlink():
            actual_mode, data = '120000', os.readlink(item).encode()
        elif item.is_file():
            actual_mode, data = ('100755' if item.stat().st_mode & 0o111 else '100644'), item.read_bytes()
        else:
            worktree_differences.append(path); continue
        if (actual_mode, object_hash('blob', data)) != (mode, sha): worktree_differences.append(path)
    check('every candidate worktree byte and executable mode matches index', not worktree_differences)
    check('no untracked source files', not git(args.candidate, 'ls-files', '--others', '--exclude-standard').strip())
    changed = {x for x in c.keys() & p.keys() if c[x] != p[x]}
    added, deleted = c.keys()-p.keys(), p.keys()-c.keys()
    check('all accepted PR55 paths retained', not deleted)
    check('only enumerated 28 paths modified', changed == ALLOWED_MODIFIED)
    check('only 27 empty catalogues and five compact option files added', added == CATALOGUES | OPTION_FILES)
    check('all other accepted bytes and modes preserved', all(c.get(x) == v for x, v in p.items() if x not in ALLOWED_MODIFIED))
    exact_develop = CATALOGUES | REGISTRATION | {'translations/language-options.json', 'tools/fixtures/language_option_additions_20261012.json'}
    exact_develop |= {JVM+n+'.kt' for n in JVM_NAMES if n not in {'CommonsHelpProviderTranslationTest', 'CommonsMetadataHttpTranslationTest', 'CommonsMetadataQueryFailureTranslationTest'}}
    check('all accepted registration, metadata, 27 catalogues and nonconflicting JVM edits match develop bytes/modes', all(c[x] == d[x] for x in exact_develop))
    check('all 27 added catalogues structurally empty', all((lambda root: root.tag == 'resources' and not root.attrib and not list(root) and not (root.text or '').strip())(ET.fromstring(cc(x))) for x in CATALOGUES))
    second = 'tools/fixtures/language_option_additions_20261012_second.json'
    expected = dj(second); expected.pop('baseline_sha256')
    check('second fixture retains all factual identities/sources/scope, dropping only snapshot gate', cj(second) == expected)
    # Documentation changes describe current inventory and archive policy only.
    expected_doc = dd('TRANSLATING.md').decode()
    doc_replacements = {
        'no translated entries yet: all 695 translatable source strings and the one plural\nresource currently use default English fallback. Selecting a language is not a':
        'no translated entries yet: all current translatable source strings and plural\nresources use default English fallback. Selecting a language is not a',
        'and status. Historical 140-choice/81-fallback evidence is preserved unchanged;\ncurrent regression checks compose it with these six explicit additions.':
        'and status. Historical 140-choice/81-fallback evidence remains available in the\n[immutable archive](verification/README.md). Current regressions check the live\nresources and the explicit current scope directly.',
        'Each new catalogue has **0/695 translatable strings and 0/1 plural resources**;\nall 696 app resource keys use default-English fallback pending actual translation.':
        'Each new catalogue has **zero translated strings and plural resources**;\nall current translatable keys use default-English fallback pending actual translation.',
        'Historical 140-choice evidence and the first six-option fixture remain unchanged;\ncurrent regressions compose both additions into **27 new options and 108 partial\ncatalogues**. The earlier unpublished 162-choice candidate is superseded; its':
        'The explicit current scope preserves the original 59 scoped catalogues and all\n81 existing fallback identities, adding **27 empty catalogues for 108 fallbacks**.\nIt checks current identity, status, resource values and fallback behavior without\nreconstructing historical snapshots. The earlier unpublished 162-choice candidate is superseded; its',
    }
    for old, new in doc_replacements.items(): expected_doc = expected_doc.replace(old, new)
    check('translation instructions differ only for current counts and archive policy', cc('TRANSLATING.md').decode() == expected_doc)
    for name in WORDING:
        check('exact wording and constraints preserved: '+name, cc(FIX+name) == pp(FIX+name).replace(b'default-plus-59-with-81-open-fallbacks', b'default-plus-59-with-108-open-fallbacks'))
    scope, old_scope = cj(FIX+'locale_contract_scope.json'), pj(FIX+'locale_contract_scope.json')
    offered = [n.text for n in ET.fromstring(cc('Paintroid/src/main/res/values/app_language_tags.xml')).findall('.//item')]
    fallback = scope['fallback_tags']
    check('explicit scope is unchanged 59 plus exact old 81 and accepted 27', scope['scoped_tags'] == old_scope['scoped_tags'] and len(scope['scoped_tags']) == 59 and len(fallback) == 108 and len(set(fallback)) == 108 and set(fallback) == set(old_scope['fallback_tags']) | ADDED_TAGS)
    check('scope metadata preserves default, schema and synthetic controls', all(scope[k] == v for k, v in old_scope.items() if k not in {'scope_id', 'fallback_tags', 'fallback_policy'}))
    check('current 167 picker has exact disjoint scope equality', len(offered) == len(set(offered)) == 167 and not set(scope['scoped_tags']) & set(fallback) and set(offered) == set(scope['scoped_tags']) | set(fallback))
    original, integrated = pj(FIX+'commons_import_current_wording.json'), cj(FIX+'commons_import_current_wording.json')
    expected = copy.deepcopy(original); expected['remaining_other_offered_locales'] = sorted(set(original['remaining_other_offered_locales']) | ADDED_TAGS)
    check('imports preserve all exact values and only extend explicit fallback set', integrated == expected and integrated['remaining_other_offered_locales'] == fallback)
    old_provenance, provenance = pj(FIX+'wording-provenance.json'), cj(FIX+'wording-provenance.json')
    integration = provenance['scope'].pop('current_integration')
    check('old 59/81 provenance preserved; new integration separate', provenance == old_provenance and integration['accepted_develop_commit'] == DEVELOP_COMMIT and set(integration['added_fallback_tags']) == ADDED_TAGS and integration['current_scoped_count'] == 59 and integration['current_fallback_count'] == 108)
    for name in ('CommonsMetadataHttpTranslationTest', 'CommonsMetadataQueryFailureTranslationTest'):
        path = JVM+name+'.kt'
        expected = pp(path).replace(b'all140Tags', b'allOfferedTags').replace(b'assertEquals(140,AppLanguage.tags(context).size)', b'assertEquals(167,AppLanguage.tags(context).size)').replace(b'assertEquals(81,fallbacks)', b'assertEquals(108,fallbacks)')
        check('only method identity and inventory numbers change: '+name, cc(path) == expected)
    path = JVM+'CommonsHelpProviderTranslationTest.kt'
    expected = pp(path).replace(b'other81OfferedTags', b'otherOfferedTags').replace(b'assertEquals(81,remaining.size)', b'assertEquals(108,remaining.size)')
    check('Help retains PR55 Hungarian UI test and only updates fallback identity/count', cc(path) == expected)
    check('CI.md only updates explicit fallback count', cc('CI.md') == pp('CI.md').replace(b'81 open fallbacks', b'108 open fallbacks'))
    # Compare the actual incoming delta, not all historical files removed by the earlier accepted migration.
    incoming = {x for x in d.keys() | b.keys() if d.get(x) != b.get(x)}
    omitted = incoming-c.keys()
    archived = {x for x in incoming if x.startswith(ARCHIVE_PREFIXES)}
    check('incoming delta exactly 80 paths', len(incoming) == 80)
    check('only 30 generated evidence files and three approved retired files omitted', len(archived) == 30 and omitted == archived | RETIRED)
    check('no incoming archive directory imported', not any(x.startswith(ARCHIVE_PREFIXES) for x in c))
    readme = cc('verification/README.md').decode()
    check('all three omitted evidence directories linked at immutable accepted develop', all('https://github.com/c933103/AN-Paint/tree/'+DEVELOP_COMMIT+'/'+x.rstrip('/') in readme for x in ARCHIVE_PREFIXES))
    protected = {x for x in p if x.startswith(('Paintroid/src/main/java/', 'Paintroid/src/main/cpp/', 'app/src/main/', 'Paintroid/src/androidTest/', 'app/src/androidTest/', '.github/workflows/')) or x.endswith(('.gradle', '.ttf', '.otf')) or re.search(r'(licen[sc]e|notice|copyright)', x, re.I) or x.startswith('verification/releases/') or x == 'verification/legacy-font-metadata.json'}
    check('production, fonts/legal, installed guards, build/native graph, workflow and release inputs preserved', all(c.get(x) == p[x] for x in protected))
    # Imported tests keep five meaningful methods; precisely two historical gates retire.
    removed_methods = set()
    for path in ('tools/test_language_option_additions.py', 'tools/test_language_option_additions_second.py'):
        tests = lambda data: {n.name for n in ast.walk(ast.parse(data)) if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}
        old, new = tests(dd(path)), tests(cc(path))
        removed_methods |= old-new
        check('meaningful imported methods retained: '+path, len(old & new) == (2 if path.endswith('additions.py') else 3))
    check('only two authorized imported historical methods removed', removed_methods == {'test_historical_disposition_evidence_remains_byte_identical', 'test_removing_only_the_twenty_one_rows_restores_original_146_inventories'})
    changed_python = {x for x in changed | added if x.endswith('.py')}
    check('changed Python does not introduce historical snapshot/hash/inverse gate dependencies', not any(re.search(r'\b(?:hashlib|sha256|baseline_sha256|language_option_historical_evidence|subprocess|requests|urllib)\b', cc(x).decode()) for x in changed_python))
    # Execute only new pure validators; no suite, filesystem mutation or generated module caches.
    namespace = {'__file__': str(args.candidate/'tools/current_localization_contracts.py')}
    validator_ast = ast.parse(cc('tools/current_localization_contracts.py'))
    validator_ast.body = [node for node in validator_ast.body if isinstance(node, ast.FunctionDef) and node.name == 'require_locale_scope']
    exec(compile(validator_ast, '<current pure scope validator>', 'exec'), namespace)
    validate = namespace['require_locale_scope']; validate(scope, set(scope['scoped_tags']), offered)
    mutations = []
    for field in ('scoped_tags', 'fallback_tags'):
        for kind in ('missing-group', 'empty-group', 'missing-tag', 'duplicate-tag', 'unknown-tag'):
            data = copy.deepcopy(scope)
            if kind == 'missing-group': del data[field]
            elif kind == 'empty-group': data[field] = []
            elif kind == 'missing-tag': data[field].pop()
            elif kind == 'duplicate-tag': data[field].append(data[field][0])
            else: data[field][0] = 'zz-unknown'
            mutations.append((field+'/'+kind, data, offered))
    for tag in ADDED_TAGS:
        data = copy.deepcopy(scope); data['fallback_tags'].remove(tag); mutations.append(('missing/'+tag, data, offered))
    data = copy.deepcopy(scope); data['fallback_tags'].append(data['scoped_tags'][0]); mutations.append(('overlap', data, offered))
    mutations.append(('duplicate-offered', scope, offered+[offered[0]]))
    rejected = 0
    for name, data, inventory in mutations:
        try: validate(data, set(scope['scoped_tags']), inventory)
        except ValueError: rejected += 1
        else: failures.append('scope validator accepts '+name)
    check('all 39 scope corruption controls reject', rejected == len(mutations) == 39)
    check('index unchanged during review', manifest(args.candidate) == c)
    result = {
        'status': 'PASS' if not failures else 'FAIL',
        'candidate_tree': candidate_tree,
        'accepted_pr55': {'commit': PR55_COMMIT, 'tree': PR55_TREE},
        'accepted_develop': {'commit': DEVELOP_COMMIT, 'tree': DEVELOP_TREE},
        'incoming_base_tree': INCOMING_BASE_TREE,
        'temporary_local_HEAD_used_as_provenance': False,
        'counts': {'candidate_paths': len(c), 'accepted_pr55_paths': len(p), 'unchanged_accepted_paths': len(p)-len(changed), 'modified_paths': len(changed), 'added_paths': len(added), 'deleted_paths': len(deleted), 'protected_paths': len(protected), 'exact_develop_paths': len(exact_develop), 'empty_catalogues': len(CATALOGUES), 'offered': len(offered), 'scoped': len(scope['scoped_tags']), 'fallbacks': len(fallback), 'incoming_delta': len(incoming), 'archived_incoming_evidence': len(archived), 'scope_corruptions_rejected': rejected},
        'checks_passed': passed, 'failures': failures, 'worktree_differences': worktree_differences,
        'limits': ['Scope/preservation comparison, not linguistic re-review.', 'No normal or optimized full host aggregate run.', 'No Android/JVM/native/build/installed execution or new acceptance claim.', 'Remote commit/tree pins supplied and verified by parent; this script verifies their local exact tree bytes.']}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return bool(failures)

if __name__ == '__main__':
    sys.exit(main())
