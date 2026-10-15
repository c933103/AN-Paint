#!/usr/bin/env python3
"""Validate this bounded data checkpoint against a supplied merged source checkout.

Usage: python validate_merged_assembly_reconciliation.py SOURCE [PREVIOUS_TRACKER_DATA]
No network access, application execution, or new linguistic acceptance occurs.
"""
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from validate_entry_review import validate as validate_internal

HERE = Path(__file__).resolve().parent
REV = 'e53b2e6aaaa9ac231cfdd38485e28ee9d638e870'
# SHA-256 of newline-joined sorted resource paths from this pinned source.
EXPECTED_PATHS_SHA256 = 'a668c272bd68c7c67fd0bd1ba9ff2dea23a4596cec3520cddf3d7e0add3d94fe'
FRENCH_PAIRS = {('fr', key) for key in (
    'string/ui_add_up_to_20_images_with_android_s',
    'string/ui_drop_at_a_highlighted_edge_right_top_aligned',
    'plurals/ui_crop_preview_images')}
CROP_PAIRS = {(tag, 'plurals/ui_crop_preview_images') for tag in ('lt', 'ar', 'ru', 'ja')}

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
    require(pair in FRENCH_PAIRS | CROP_PAIRS, 'Unexpected successor pair')
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

def values(path):
    result = {}
    for element in ET.parse(path).getroot():
        if element.tag not in ('string', 'plurals') or element.attrib.get('translatable') == 'false':
            continue
        key = element.tag + '/' + element.attrib['name']
        require(key not in result, 'Duplicate source key: ' + key)
        result[key] = ({item.attrib['quantity']: ''.join(item.itertext()) for item in element}
                       if element.tag == 'plurals' else ''.join(element.itertext()))
    return result

def check_pairs(receipts, fixture, english, catalogues):
    pairs = {(item['tag'], item['key']): item for item in receipts['receipts']}
    require(len(pairs) == len(receipts['receipts']) == 3002, 'Active pair count/identity changed')
    for pair, item in pairs.items():
        require(item['current_english_sha256'] == value_hash(english[pair[1]]), 'Current English mismatch: ' + str(pair))
        require(item['current_localized_sha256'] == value_hash(catalogues[pair[0]][pair[1]]), 'Current target mismatch: ' + str(pair))
    require(len(fixture['complete_french_pairs']) == 7, 'French accepted scope changed')
    require({(item['tag'], item['key']) for item in fixture['complete_french_pairs']} == FRENCH_PAIRS | CROP_PAIRS,
            'Successor fixture must contain each of the seven distinct pairs')
    for complete in fixture['complete_french_pairs']:
        pair = (complete['tag'], complete['key'])
        item = pairs[pair]
        check_successor_scope(item, pair)
        require(complete['english'] == english[pair[1]] and complete['localized'] == catalogues[pair[0]][pair[1]], 'Complete French pair differs from source')
        require(item['state'] == 'reviewed_current' and item.get('finding_status') != 'open', 'French disposition not resolved')
        for kind, value in [('english', complete['english']), ('localized', complete['localized'])]:
            require(complete[kind + '_sha256'] == item['reviewed_' + kind + '_sha256'] == item['current_' + kind + '_sha256'] == value_hash(value), 'French accepted hash mismatch')
    require(len(fixture['stale_other_pairs']) == 3, 'Stale scope changed')
    for stale in fixture['stale_other_pairs']:
        item = pairs[(stale['tag'], stale['key'])]
        require(item['state'] == 'needs_rereview', 'Source-stale pair promoted')
        require(item['reviewed_english_sha256'] == stale['reviewed_english_sha256'] != stale['current_english_sha256'] == item['current_english_sha256'], 'Stale English history lost')
        require(item['reviewed_localized_sha256'] == item['current_localized_sha256'] == stale['localized_sha256'], 'Unchanged localized history lost')
    return pairs

def validate(source, previous=None):
    summary = validate_internal(HERE)
    receipts = read(HERE / 'entry-review-receipts.json')
    counts = read(HERE / 'entry-review-counts.json')
    identities = read(HERE / 'source-identities.json')
    fixture = read(HERE / 'fr-assembly-merged-reconciliation-20261015.json')
    successor = read(HERE / 'four-crop-merged-reconciliation-20261015.json')
    fixture['source_revision'] = successor['source_revision']
    fixture['complete_french_pairs'] += successor['complete_crop_pairs']
    resolved = {(item['tag'], item['key']) for item in successor['complete_crop_pairs']}
    fixture['stale_other_pairs'] = [item for item in fixture['stale_other_pairs'] if (item['tag'], item['key']) not in resolved]
    require(summary['source_revision'] == fixture['source_revision'] == REV, 'Wrong source revision')
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
    pairs = check_pairs(receipts, fixture, english, catalogues)
    for tag in ['ms', 'id', 'ja', 'zh-HK']:
        item = pairs[(tag, 'string/ui_rendering_images')]
        require(item['state'] == 'needs_rereview' and item.get('finding_status') == 'open', 'Paused processing hold changed')
    rows = {row['tag']: row for row in counts['languages']}
    table_files = [HERE / 'current-entry-review.md']
    for candidate in [HERE / 'TRANSLATION_PROGRESS.md', HERE.parents[1] / 'TRANSLATION_PROGRESS.md', HERE / 'new-body.md']:
        if candidate.exists() and candidate not in table_files:
            table_files.append(candidate)
    for file in table_files:
        section = file.read_text().split('### Current per-language entry counts', 1)[1].split('### Preserved earlier review checkpoints', 1)[0]
        seen = []
        for line in section.splitlines():
            match = re.match(r'\| `([^`]+)`', line)
            if not match:
                continue
            tag = match.group(1)
            seen.append(tag)
            require([int(cell.strip()) for cell in line.split('|')[2:7]] == [rows[tag][key] for key in ['reviewed_current', 'needs_rereview', 'unreviewed_or_unknown', 'missing', 'total']], 'Table row mismatch: ' + tag)
        require(seen == list(rows) and len(seen) == 171, 'Table languages changed')
    if previous:
        old = read(previous / 'entry-review-receipts.json')
        before = {(item['tag'], item['key']): item for item in old['receipts']}
        changed = {pair for pair in pairs if pairs[pair] != before[pair]}
        intended = {(item['tag'], item['key']) for item in fixture['complete_french_pairs']} | {(item['tag'], item['key']) for item in fixture['stale_other_pairs']}
        require(pairs.keys() == before.keys() and changed == intended, 'Unexpected active-pair edit')
        require(receipts['superseded_receipts'][:42] == old['superseded_receipts'] and len(receipts['superseded_receipts']) == 56, 'Prior history changed')
        for item in receipts['superseded_receipts'][42:52]:
            require(all(item[key] == value for key, value in before[(item['tag'], item['key'])].items()), 'Historical record differs')
        for item in receipts['superseded_receipts'][52:]:
            require(item['state'] == 'needs_rereview' and item['source_pair_status'] == 'current_english_changed_since_complete_review', 'Intermediate source hold lost')
            require(all(item[key] == value for key, value in before[(item['tag'], item['key'])].items() if key not in ('state', 'current_english_sha256')), 'Intermediate review history changed')
        require(receipts['partial_reviews'] == old['partial_reviews'] and len(receipts['partial_reviews']) == 56, 'Partial evidence changed')
        require(all(receipts['cohorts'][key] == value for key, value in old['cohorts'].items()), 'Old cohort changed')
        require(read(HERE / 'validation.json')['prior_checkpoint_validation'] == read(previous / 'validation.json'), 'Prior validation changed')
        for tag in ['ms', 'id', 'ja', 'zh-HK']:
            require(pairs[(tag, 'string/ui_rendering_images')] == before[(tag, 'string/ui_rendering_images')], 'Paused record modified')
        for filename in ['TRANSLATION_PROGRESS.md', 'current-entry-review.md']:
            current = HERE / filename
            if not current.exists(): current = HERE.parents[1] / filename
            require(current.read_text().split('### Preserved earlier review checkpoints', 1)[1] == (previous / filename).read_text().split('### Preserved earlier review checkpoints', 1)[1], 'Historical prose changed')
    control = copy.deepcopy(receipts)
    stale = fixture['stale_other_pairs'][0]
    next(item for item in control['receipts'] if (item['tag'], item['key']) == (stale['tag'], stale['key']))['state'] = 'reviewed_current'
    try:
        check_pairs(control, fixture, english, catalogues)
    except ValueError:
        pass
    else:
        raise ValueError('Negative control accepted stale promotion')
    control = copy.deepcopy(receipts)
    control['receipts'][0]['current_localized_sha256'] = 'bad'
    try:
        check_pairs(control, fixture, english, catalogues)
    except ValueError:
        pass
    else:
        raise ValueError('Negative control accepted bad target hash')
    return {'status': 'PASS', 'source_revision': REV, 'source_identity_files': identity_count, 'active_english_hashes': 3002, 'active_localized_hashes': 3002, 'catalogue_partitions': 171, 'table_files': len(table_files), 'resolved_french_pairs': 3, 'source_stale_pairs': 3, 'resolved_crop_pairs': 4, 'accepted_crop_quantity_forms': 14, 'unaffected_active_pairs': 2992, 'superseded_history': 56, 'partial_records': 56, 'processing_holds': 4, 'negative_controls': 2, 'previous_checkpoint_compared': bool(previous), 'strict_validator': summary}

if __name__ == '__main__':
    result = validate(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) > 2 else None)
    print(json.dumps(result, indent=2))
