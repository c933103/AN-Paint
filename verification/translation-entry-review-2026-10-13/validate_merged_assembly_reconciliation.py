#!/usr/bin/env python3
"""Verify this exact review-data checkpoint against pinned merged source.

Usage: python validate_merged_assembly_reconciliation.py SOURCE [PREVIOUS_TRACKER_DATA]
No network request, application execution, or new linguistic acceptance occurs.
Historical PR96/PR99 gates remain exact; three fresh unchanged-value reviews have
separate complete-review, durable evidence and source-binding gates.
"""
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from validate_entry_review import validate as validate_internal

HERE = Path(__file__).resolve().parent
REV = 'e53b2e6aaaa9ac231cfdd38485e28ee9d638e870'
PRECEDING_TRACKER = 'f507f4c4d8fde2731434ad5ee2b122d747ec6d6d'
EXPECTED_PATHS_SHA256 = 'a668c272bd68c7c67fd0bd1ba9ff2dea23a4596cec3520cddf3d7e0add3d94fe'
COHORT = 'ASSEMBLY-CURRENT-PAIR-REREVIEW-20261015'
HELP_KEY = 'string/ui_add_up_to_20_images_with_android_s'
CROP_KEY = 'plurals/ui_crop_preview_images'
FRENCH_PAIRS = {('fr', key) for key in (HELP_KEY, 'string/ui_drop_at_a_highlighted_edge_right_top_aligned', CROP_KEY)}
CROP_PAIRS = {(tag, CROP_KEY) for tag in ('lt', 'ar', 'ru', 'ja')}
CURRENT_PAIRS = {('ja', HELP_KEY), ('zh-HK', HELP_KEY), ('zh-HK', CROP_KEY)}
PAUSED_PAIRS = {(tag, 'string/ui_rendering_images') for tag in ('ms', 'id', 'ja', 'zh-HK')}
FIXTURE = 'current-assembly-pair-reconciliation-20261015.json'
# Exact final independent reports published and read back before reconciliation.
CURRENT_REVIEW_BINDINGS = {'ja': {'path': 'current-assembly-review-evidence/japanese-review.json',
        'sha256': 'bebad46b4d2c2abf2fa2125af9d6c74427eafa502b641ba97f90ffc8e516e5c2',
        'durable_receipt': 'https://github.com/c933103/AN-Paint/blob/1422e223df2c9a06dc3c959fb326abdc9e0ac8d7/verification/current-assembly-help-review-20261015/japanese.json',
        'review_id': 'JA-ASSEMBLY-COMPLETE-CURRENT-20261015',
        'final': True,
        'reviewed_source_revision': 'e53b2e6aaaa9ac231cfdd38485e28ee9d638e870'},
 'zh-HK': {'path': 'current-assembly-review-evidence/hk-review.json',
           'sha256': '05615a99edde6bd04ecc21b04eb1fcbfdc1589d0e591e132c1c236bdb2e97975',
           'durable_receipt': 'https://github.com/c933103/AN-Paint/blob/1422e223df2c9a06dc3c959fb326abdc9e0ac8d7/verification/current-assembly-help-review-20261015/hong-kong.json',
           'review_id': 'HK-ASSEMBLY-CURRENT-20261015-E53B2E6',
           'final': True,
           'reviewed_source_revision': 'e53b2e6aaaa9ac231cfdd38485e28ee9d638e870'}}
PRESERVED_HASHES = {'preserved_cohorts_sha256': '46f1359193cbfbb4f7d76e47a9574804aad05dfaebefd211bfada893ba40fcb3',
 'preserved_history_sha256': 'd12163e9584a3962a8e95bd1bce68f3950be6b4b9dd65a873d95271dedc25734',
 'preserved_partial_sha256': 'ed40cde25ca4466446799cf432a0a2989a5a1a2b23db0816e2e360e6feda35dd',
 'unaffected_active_receipts_sha256': '4cab6a37dcc25d8c2d2e36041c28738af32c405b71c746a6b8463144d314ccc5'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def value_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def blob_hash(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def check_identity_scope(identities, counts):
    require(identities.get('source_revision') == REV, 'Identity source revision changed')
    paths = [item['path'] for item in identities['current_source_files']]
    require(len(paths) == len(set(paths)) == 182, 'Expected 182 unique source identity paths')
    require(hashlib.sha256('\n'.join(sorted(paths)).encode()).hexdigest() == EXPECTED_PATHS_SHA256,
            'Source identity path set differs from pinned source')
    catalogues = [row['catalogue_path'] for row in counts['languages']]
    require(len(catalogues) == len(set(catalogues)) == 171, 'Expected 171 unique catalogues')
    require(set(catalogues) <= set(paths), 'Catalogue missing from source identities')
    return len(paths)


def check_successor_scope(item, pair):
    """Original seven corrected-value gates are intentionally not relaxed."""
    require(pair in FRENCH_PAIRS | CROP_PAIRS, 'Unexpected historical successor pair')
    is_french = pair in FRENCH_PAIRS
    evidence = ('https://github.com/c933103/AN-Paint/pull/96#issuecomment-6188585935'
                if is_french else 'https://github.com/c933103/AN-Paint/pull/99#issuecomment-6192351710')
    revision = '244c37c4558a90b1e210885a3c7312dd754d7345' if is_french else REV
    require((item.get('disposition'), item.get('review_scope')) ==
            ('accepted_static', 'complete_linguistic_and_static_source_context'),
            'Successor requires complete static/linguistic scope: ' + str(pair))
    require(item.get('source') == item.get('independent_review_source') == evidence,
            'Successor evidence source mismatch: ' + str(pair))
    require(item.get('reviewed_source_revision') == item.get('merged_revision') == revision,
            'Successor reviewed/merged revision mismatch: ' + str(pair))
    require(item.get('correction_applied') is True, 'Successor correction not applied')


def check_current_review_scope(item, pair, complete, binding):
    require(pair in CURRENT_PAIRS, 'Unexpected current-review pair')
    expected = {
        'cohort': COHORT,
        'state': 'reviewed_current',
        'disposition': 'accepted_static',
        'review_scope': 'complete_linguistic_and_static_source_context',
        'review_kind': 'complete_current_pair_rereview',
        'review_decision': 'accept_unchanged',
        'reviewed_source_revision': REV,
        'merged_revision': REV,
        'correction_applied': False,
        'localized_value_unchanged': True,
        'source_pair_status': 'resolved_by_complete_pair_review',
        'source': binding['durable_receipt'],
        'independent_review_source': binding['durable_receipt'],
        'complete_review_report_sha256': binding['sha256'],
        'complete_review_report_path': binding['path'],
        'review_id': binding['review_id'],
    }
    for field, value in expected.items():
        require(field in item and type(item[field]) is type(value) and item[field] == value,
                'Current review metadata mismatch: ' + str(pair) + ' ' + field)
    require(item.get('finding_status') != 'open', 'Current review retains an open finding')
    require(complete.get('decision') == 'accept_unchanged' and complete.get('complete_value_review') is True,
            'Final complete-value acceptance missing')
    require(complete.get('review_id') == binding['review_id'] and complete.get('review_evidence') == binding['durable_receipt'],
            'Complete pair evidence mismatch')
    require(complete.get('reviewed_source_revision') == REV, 'Complete pair revision mismatch')
    require(not any(field in item for field in ('source_pair_changed_at_revision', 'source_pair_change_source', 'source_pair_review_note')),
            'Resolved pair retains stale-state metadata')


def values(path):
    result = {}
    for element in ET.parse(path).getroot():
        if element.tag not in ('string', 'plurals') or element.attrib.get('translatable') == 'false':
            continue
        key = element.tag + '/' + element.attrib['name']
        require(key not in result, 'Duplicate source key: ' + key)
        if element.tag == 'plurals':
            quantities = [item.attrib['quantity'] for item in element]
            require(len(quantities) == len(set(quantities)), 'Duplicate plural quantity: ' + key)
            value = {item.attrib['quantity']: ''.join(item.itertext()) for item in element}
        else:
            value = ''.join(element.itertext())
        result[key] = value
    return result


def valid_evidence_url(url):
    return re.fullmatch(r'https://github\.com/c933103/AN-Paint/(?:pull/56#issuecomment-[0-9]+|blob/[0-9a-f]{40}/[^?#]+\.json)', url) is not None


def normalized_review_pairs(tag, report):
    require(report.get('source_revision') == REV, 'Report source revision differs')
    if tag == 'ja':
        require(report.get('review_scope') == 'complete_element' and report.get('decision') == 'accept_unchanged', 'Japanese review is not complete acceptance')
        require(report.get('required_correction') is False and report.get('replacement_candidate') is None, 'Japanese correction still required')
        require(report.get('paragraph_count') == 7 and report.get('full_clause_unit_count') == len(report['clause_dispositions']) == 32, 'Japanese clause coverage differs')
        require(all(x.get('disposition') == 'accept_unchanged' and x.get('english_full_clause') and x.get('japanese_full_clause') for x in report['clause_dispositions']), 'Japanese incomplete clause acceptance')
        return [{'tag': 'ja', 'key': HELP_KEY, 'english': report['reviewed_english_value'],
                 'localized': report['reviewed_localized_value'], 'english_sha256': report['reviewed_english_sha256'],
                 'localized_sha256': report['reviewed_localized_sha256'], 'decision': 'accept_unchanged', 'complete_value_review': True}]
    require(tag == 'zh-HK', 'Unexpected review locale')
    require(report.get('status') == 'complete_current_pair_review' and report.get('review_scope') == 'complete_linguistic_and_static_source_context', 'HK review is not complete')
    require(report.get('decisions') == {'accepted_unchanged': 2, 'correction_required': 0, 'unapproved_replacements': 0}, 'HK acceptance not final')
    require(len(report['rows']) == 2 and {x['key'] for x in report['rows']} == {HELP_KEY, CROP_KEY}, 'HK full pair set differs')
    results = []
    for row in report['rows']:
        require(row.get('tag') == tag and row.get('disposition') == 'accepted_unchanged' and row.get('scope') == 'complete_linguistic_and_static_source_context', 'HK pair incomplete acceptance')
        require(row.get('review_id') == report.get('review_id'), 'HK pair review ID mismatch')
        if row['key'] == HELP_KEY:
            paragraphs = row['paragraph_reviews']
            require(len(paragraphs) == 7 and [x['paragraph'] for x in paragraphs] == list(range(1, 8)), 'HK paragraph coverage differs')
            for kind in ('english', 'localized'):
                require('\\n\\n'.join(x[kind] for x in paragraphs) == row[kind], 'HK paragraphs omit text')
            require(all(x['verdict'] == 'pass_unchanged' and x['clauses'] and all(c['verdict'] == 'pass_unchanged' for c in x['clauses']) for x in paragraphs), 'HK paragraph/clauses not all accepted')
        else:
            for field, values_field, quantities, verdict in (
                ('source_form_reviews', 'english', {'one', 'other'}, 'reviewed_in_full'),
                ('target_form_reviews', 'localized', {'other'}, 'pass_unchanged'),
            ):
                forms = row[field]
                require(len(forms) == len(quantities) and {x['quantity'] for x in forms} == quantities, 'HK plural form omitted/duplicated')
                require({x['quantity']: x['full_value'] for x in forms} == row[values_field], 'HK plural form text mismatch')
                require(all(x['verdict'] == verdict for x in forms), 'HK plural form not fully reviewed')
        results.append({**{k: row[k] for k in ('tag', 'key', 'english', 'localized', 'english_sha256', 'localized_sha256')},
                        'decision': 'accept_unchanged', 'complete_value_review': True})
    return results


def check_review_artifacts(directory, fixture, source=None):
    bindings = fixture['review_bindings']
    require(bindings == CURRENT_REVIEW_BINDINGS, 'Final independent review bindings changed')
    exact = {(x['tag'], x['key']): x for x in fixture['complete_pairs']}
    context_paths = set()
    for tag, binding in bindings.items():
        require(valid_evidence_url(binding.get('durable_receipt', '')), 'Durable final receipt missing: ' + tag)
        require(binding.get('final') is True and binding.get('reviewed_source_revision') == REV, 'Review not final or not current: ' + tag)
        require(bool(binding.get('review_id')), 'Missing review identity')
        path = Path(binding['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'Unsafe report path')
        data = (directory / path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == binding['sha256'], 'Complete review artifact hash mismatch: ' + tag)
        report = json.loads(data)
        require(report.get('review_id') == binding['review_id'], 'Complete report review ID mismatch')
        for reviewed in normalized_review_pairs(tag, report):
            pair = (reviewed['tag'], reviewed['key'])
            for field in ('english', 'localized', 'english_sha256', 'localized_sha256'):
                require(reviewed[field] == exact[pair][field], 'Complete report does not match accepted pair')
        if source:
            if tag == 'ja':
                files = [(x['path'], x['git_blob_sha1'], x['resource_file_sha256']) for x in report['source_identities']]
                files += [(x['path'], x['sha'], x['local_file_sha256']) for x in report['context_identities']]
                require(len(files) == 12, 'Japanese source/context identity coverage differs')
            else:
                files = [(x['path'], x['git_blob_sha'], x['sha256']) for x in report['source_identities']]
                require(len(files) == 9, 'HK source/context identity coverage differs')
            for relative, git_sha, sha256 in files:
                file_path = Path(relative)
                require(not file_path.is_absolute() and '..' not in file_path.parts, 'Unsafe source/context path')
                content = (source / relative).read_bytes()
                require(blob_hash(content) == git_sha and hashlib.sha256(content).hexdigest() == sha256,
                        'Fresh review source/context identity mismatch: ' + relative)
                context_paths.add(relative)
    return len(context_paths)


def check_pairs(receipts, historical, fixture, english, catalogues):
    pairs = {(item['tag'], item['key']): item for item in receipts['receipts']}
    require(len(pairs) == len(receipts['receipts']) == 3002, 'Active pair count/identity changed')
    for pair, item in pairs.items():
        require(item['current_english_sha256'] == value_hash(english[pair[1]]), 'Current English mismatch: ' + str(pair))
        require(item['current_localized_sha256'] == value_hash(catalogues[pair[0]][pair[1]]), 'Current target mismatch: ' + str(pair))
    require(len(historical) == 7 and {(x['tag'], x['key']) for x in historical} == FRENCH_PAIRS | CROP_PAIRS,
            'Historical fixture must contain each of the seven distinct pairs')
    complete_pairs = fixture['complete_pairs']
    require(len(complete_pairs) == 3 and {(x['tag'], x['key']) for x in complete_pairs} == CURRENT_PAIRS,
            'Current fixture must contain each of the three distinct pairs')
    for complete in historical + complete_pairs:
        pair = (complete['tag'], complete['key'])
        item = pairs[pair]
        if pair in CURRENT_PAIRS:
            check_current_review_scope(item, pair, complete, fixture['review_bindings'][pair[0]])
            require(complete.get('localized_unchanged') is True, 'Unchanged-value review missing')
        else:
            check_successor_scope(item, pair)
        require(complete['english'] == english[pair[1]] and complete['localized'] == catalogues[pair[0]][pair[1]],
                'Complete pair differs from source: ' + str(pair))
        require(item['state'] == 'reviewed_current' and item.get('finding_status') != 'open', 'Accepted disposition not resolved')
        for kind in ('english', 'localized'):
            require(complete[kind + '_sha256'] == item['reviewed_' + kind + '_sha256'] ==
                    item['current_' + kind + '_sha256'] == value_hash(complete[kind]),
                    'Accepted hash mismatch: ' + str(pair))
        if pair == ('zh-HK', CROP_KEY):
            require(set(complete['english']) == {'one', 'other'} and set(complete['localized']) == {'other'},
                    'HK complete plural forms changed')
            require(complete.get('quantity_forms') == 1 and complete.get('english_quantity_forms') == 2,
                    'HK plural quantity metadata mismatch')
    require(not any(x.get('source_pair_status') == 'current_english_changed_since_complete_review' for x in pairs.values()),
            'Unresolved source-stale pair remains')
    return pairs


def check_history(receipts, fixture, previous=None):
    require({key: fixture.get(key) for key in PRESERVED_HASHES} == PRESERVED_HASHES, 'Preceding checkpoint preservation bindings changed')
    originals = fixture['superseded_predecessors']
    require(len(originals) == 3 and {(x['tag'], x['key']) for x in originals} == CURRENT_PAIRS, 'Wrong predecessor scope')
    require(len(receipts['superseded_receipts']) == 59, 'Superseded history count changed')
    require(value_hash(receipts['superseded_receipts'][:56]) == fixture['preserved_history_sha256'], 'Prior superseded history changed')
    require(len(receipts['partial_reviews']) == 56 and value_hash(receipts['partial_reviews']) == fixture['preserved_partial_sha256'],
            'Partial evidence changed')
    old_cohorts = {key: value for key, value in receipts['cohorts'].items() if key != COHORT}
    require(value_hash(old_cohorts) == fixture['preserved_cohorts_sha256'], 'Earlier cohort changed')
    pairs = {(x['tag'], x['key']): x for x in receipts['receipts']}
    unaffected = [x for x in receipts['receipts'] if (x['tag'], x['key']) not in CURRENT_PAIRS]
    require(len(unaffected) == 2999 and value_hash(unaffected) == fixture['unaffected_active_receipts_sha256'], 'Unaffected active receipt changed')
    for original, archived in zip(originals, receipts['superseded_receipts'][56:]):
        pair = (original['tag'], original['key'])
        require(original['state'] == 'needs_rereview' and original.get('source_pair_status') == 'current_english_changed_since_complete_review',
                'Predecessor was not a source-stale receipt')
        require(original['reviewed_english_sha256'] != original['current_english_sha256'], 'Predecessor stale English history lost')
        require(original['reviewed_localized_sha256'] == original['current_localized_sha256'] == pairs[pair]['reviewed_localized_sha256'],
                'Unchanged localized history lost')
        expected = dict(original, superseded_by=COHORT, superseded_at_source=REV,
                        resolution_source=fixture['review_bindings'][pair[0]]['durable_receipt'])
        require(archived == expected, 'Superseded original record not preserved exactly')
    for pair in PAUSED_PAIRS:
        require(pairs[pair]['state'] == 'needs_rereview' and pairs[pair].get('finding_status') == 'open', 'Paused processing hold changed')
    if previous:
        old = read(previous / 'entry-review-receipts.json')
        before = {(x['tag'], x['key']): x for x in old['receipts']}
        require(pairs.keys() == before.keys(), 'Active pair identity changed')
        require({pair for pair in pairs if pairs[pair] != before[pair]} == CURRENT_PAIRS, 'Unexpected active-pair edit')
        require(receipts['superseded_receipts'][:56] == old['superseded_receipts'], 'Prior history changed')
        require(originals == [x for x in old['receipts'] if (x['tag'], x['key']) in CURRENT_PAIRS], 'Original predecessor changed')
        require(receipts['partial_reviews'] == old['partial_reviews'], 'Partial evidence changed')
        require(old_cohorts == old['cohorts'], 'Previous cohorts changed')
        for pair in PAUSED_PAIRS:
            require(pairs[pair] == before[pair], 'Paused record modified')


def check_tables(directory, counts, previous=None):
    rows = {row['tag']: row for row in counts['languages']}
    files = [directory / 'current-entry-review.md']
    for candidate in (directory / 'TRANSLATION_PROGRESS.md', directory.parents[1] / 'TRANSLATION_PROGRESS.md', directory / 'new-body.md'):
        if candidate.exists() and candidate not in files and (candidate.name != 'new-body.md' or '### Current per-language entry counts' in candidate.read_text(encoding='utf-8')):
            files.append(candidate)
    for file in files:
        text = file.read_text(encoding='utf-8')
        require('### Current per-language entry counts' in text, 'Required current table marker missing: ' + str(file))
        section = text.split('### Current per-language entry counts', 1)[1].split('### Preserved earlier review checkpoints', 1)[0]
        seen = []
        for line in section.splitlines():
            match = re.match(r'\| `([^`]+)`', line)
            if match:
                tag = match.group(1)
                seen.append(tag)
                require(tag in rows, 'Unknown table language')
                require([int(cell.strip()) for cell in line.split('|')[2:7]] ==
                        [rows[tag][key] for key in ('reviewed_current', 'needs_rereview', 'unreviewed_or_unknown', 'missing', 'total')],
                        'Table row mismatch: ' + tag)
        require(seen == list(rows) and len(seen) == 171, 'Table languages changed')
        if previous and (previous / file.name).exists():
            require(text.split('### Preserved earlier review checkpoints', 1)[1] ==
                    (previous / file.name).read_text(encoding='utf-8').split('### Preserved earlier review checkpoints', 1)[1],
                    'Historical prose changed')
    return len(files)


def validate(source, previous=None, directory=HERE):
    if read(directory / 'entry-review-counts.json')['source_revision'] == '0aa6c89c9d3a4d133a8b231e7002783b60ead46d':
        from validate_position_reconciliation import validate as validate_position
        return validate_position(source, previous, directory)
    summary = validate_internal(directory)
    receipts = read(directory / 'entry-review-receipts.json')
    counts = read(directory / 'entry-review-counts.json')
    identities = read(directory / 'source-identities.json')
    fixture = read(directory / FIXTURE)
    historical = read(directory / 'fr-assembly-merged-reconciliation-20261015.json')['complete_french_pairs']
    historical += read(directory / 'four-crop-merged-reconciliation-20261015.json')['complete_crop_pairs']
    require(summary['source_revision'] == fixture['source_revision'] == REV, 'Wrong source revision')
    require(fixture['preceding_tracker_revision'] == PRECEDING_TRACKER and fixture['excluded_unmerged_prs'] == [67], 'Checkpoint/exclusion scope changed')
    identity_count = check_identity_scope(identities, counts)
    for item in identities['current_source_files']:
        data = (source / item['path']).read_bytes()
        require(blob_hash(data) == item['git_blob_sha'], 'Source blob mismatch: ' + item['path'])
        require(hashlib.sha256(data).hexdigest() == item['sha256'], 'Source SHA256 mismatch')
    english = values(source / 'Paintroid/src/main/res/values/strings.xml')
    require(set(english) == set(identities['resource_keys']) and len(english) == 700, 'Source denominator changed')
    catalogues = {row['tag']: values(source / row['catalogue_path']) for row in counts['languages']}
    for row in counts['languages']:
        present = sum(bool(value) for key, value in catalogues[row['tag']].items() if key in english)
        require(row['present'] == present and row['missing'] == 700 - present, 'Catalogue coverage mismatch: ' + row['tag'])
    review_context_count = check_review_artifacts(directory, fixture, source)
    check_pairs(receipts, historical, fixture, english, catalogues)
    check_history(receipts, fixture, previous)
    cohort = receipts['cohorts'][COHORT]
    require(cohort.get('source_revision') == REV and cohort.get('complete_pairs') == fixture['complete_pairs'] and cohort.get('review_bindings') == fixture['review_bindings'], 'New cohort differs from accepted fixture')
    require(cohort.get('counts') == {'accepted_static': 3, 'total': 3, 'complete_help_elements': 2, 'help_paragraphs': 14, 'localized_plural_forms': 1, 'english_plural_forms': 2}, 'New cohort count/scope mismatch')
    require(identities.get('current_assembly_pair_rereview') == fixture, 'Source-identity review binding mismatch')
    validation = read(directory / 'validation.json')
    require(validation.get('summary') == counts['summary'] and validation.get('preceding_tracker_revision') == PRECEDING_TRACKER, 'Validation summary/checkpoint differs')
    require(validation.get('resolved_existing_receipts') == 3 and validation.get('new_unique_receipts') == 0 and validation.get('source_stale_pairs_remaining') == 0 and validation.get('unchanged_active_receipts') == 2999, 'Validation reconciliation counts differ')
    table_count = check_tables(directory, counts, previous)
    if previous:
        old_ids = read(previous / 'source-identities.json')
        require(identities['current_source_files'] == old_ids['current_source_files'] and identities['resource_keys'] == old_ids['resource_keys'],
                'Data-only review changed source identities')
        require(read(directory / 'validation.json')['prior_checkpoint_validation'] == read(previous / 'validation.json'), 'Prior validation changed')
        for filename in ('fr-assembly-merged-reconciliation-20261015.json', 'four-crop-merged-reconciliation-20261015.json'):
            require((directory / filename).read_bytes() == (previous / filename).read_bytes(), 'Historical fixture changed')
    return {
        'status': 'PASS', 'source_revision': REV, 'preceding_tracker_revision': PRECEDING_TRACKER,
        'source_identity_files': identity_count, 'fresh_review_source_context_files': review_context_count, 'active_english_hashes': 3002, 'active_localized_hashes': 3002,
        'catalogue_partitions': 171, 'table_files': table_count, 'resolved_french_pairs': 3,
        'resolved_crop_pairs': 4, 'accepted_crop_quantity_forms': 14, 'fresh_unchanged_current_pairs': 3,
        'fresh_complete_help_elements': 2, 'fresh_help_paragraphs': 14,
        'fresh_hk_plural_target_forms': 1, 'fresh_hk_plural_english_forms': 2,
        'source_stale_pairs': 0, 'unaffected_active_pairs_since_preceding_tracker': 2999,
        'superseded_history': 59, 'partial_records': 56, 'processing_holds': 4,
        'previous_checkpoint_compared': bool(previous), 'strict_validator': summary,
        'verification_kind': 'Fresh mechanical recomputation; independent complete linguistic/static review evidence is separately bound. No application tests or device/native-speaker certification.',
    }


if __name__ == '__main__':
    print(json.dumps(validate(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) > 2 else None), indent=2))
