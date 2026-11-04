#!/usr/bin/env python3
"""Recompute direct catalogue coverage from a pinned AN-Paint Git revision.

Read-only, Python standard library, no network. Does not claim linguistic quality,
human acceptance, runtime fallback resolution, or whole-app localization.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

RES = 'Paintroid/src/main/res/'
KINDS = ('string', 'plurals', 'string-array')
TEST_TAGS = {'en-XV', 'qaa-Zsye-XV'}
REPOSITORY = 'https://github.com/c933103/AN-Paint'

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def read_revision(repo, ref):
    sha = git(repo, 'rev-parse', '--verify', ref + '^{commit}').decode().strip()
    tree = git(repo, 'ls-tree', '-r', '-z', sha, RES).split(b'\0')
    manifest, files = [], {}
    for entry in tree:
        if not entry:
            continue
        metadata, encoded_path = entry.split(b'\t', 1)
        mode, kind, blob = metadata.decode().split()
        path = encoded_path.decode()
        if kind != 'blob' or not (re.fullmatch(RES + r'values[^/]*/[^/]+\.xml', path)
                                  or path == RES + 'xml/app_locales.xml'):
            continue
        content = git(repo, 'cat-file', 'blob', blob)
        actual = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        assert actual == blob, path
        files[path] = content
        manifest.append({'path': path, 'git_blob_sha': blob, 'sha256': hashlib.sha256(content).hexdigest()})
    return sha, manifest, files

def tag_from_path(path):
    folder = path.split('/')[-2]
    if folder == 'values':
        return None
    if folder.startswith('values-b+'):
        return folder[len('values-b+'):].replace('+', '-')
    tag = folder[len('values-'):].replace('-r', '-')
    return {'in': 'id', 'iw': 'he', 'ji': 'yi'}.get(tag, tag)

def resources(content):
    out, duplicates = {}, []
    for node in ET.fromstring(content):
        if node.tag not in KINDS:
            continue
        key = node.tag + '/' + node.attrib['name']
        if key in out:
            duplicates.append(key)
        if node.tag == 'string':
            values = {'value': ''.join(node.itertext())}
        else:
            values = {item.attrib.get('quantity', str(i)): ''.join(item.itertext())
                      for i, item in enumerate(node.findall('item'))}
        out[key] = {'values': values, 'translatable': node.get('translatable') != 'false'}
    return out, duplicates

def build_report(sha, manifest, files):
    defaults, duplicate_defaults = {}, []
    for path, content in files.items():
        if path.startswith(RES + 'values/'):
            current, dup = resources(content)
            duplicate_defaults.extend(dup + sorted(defaults.keys() & current.keys()))
            defaults.update(current)
    baseline = {k: v for k, v in defaults.items() if v['translatable']}
    tags = [n.text for n in ET.fromstring(files[RES + 'values/app_language_tags.xml']).findall("string-array[@name='app_language_tags']/item")]
    names_root = ET.fromstring(files[RES + 'values/app_language_names.xml'])
    names = [''.join(n.itertext()) for n in names_root.findall("string-array[@name='app_language_names']/item")]
    system_tags = [n.attrib['{http://schemas.android.com/apk/res/android}name'] for n in ET.fromstring(files[RES + 'xml/app_locales.xml'])]
    assert len(tags) == len(names) and tags == system_tags and len(tags) == len(set(tags))
    assert not duplicate_defaults
    catalogues = {tag_from_path(p): p for p in files if p.endswith('/strings.xml') and tag_from_path(p)}
    rows, validation_errors = [], []
    for tag, name in zip(tags, names):
        path = catalogues.get(tag)
        current, dup = resources(files[path]) if path else ({}, [])
        validation_errors.extend(f'{tag}: duplicate {k}' for k in dup)
        matched = set(baseline) & set(current)
        # Empty entries are present but not counted as covered text.
        blank = sorted(k for k in matched if not current[k]['values'] or
                       any(not v.strip() for v in current[k]['values'].values()))
        covered = matched - set(blank)
        missing = sorted(set(baseline) - set(current))
        references, unresolved_references, english_equal = [], [], []
        for key in covered:
            if key.startswith('string/'):
                value = current[key]['values']['value']
                if value.startswith('@string/'):
                    references.append(key)
                    if 'string/' + value[8:] not in current:
                        unresolved_references.append(key)
                elif current[key]['values'] == baseline[key]['values']:
                    english_equal.append(key)
        plural_quantities = {k.split('/', 1)[1]: list(current[k]['values'])
                             for k in covered if k.startswith('plurals/')}
        row = {
            'tag': tag, 'display_name': name,
            'type': 'test_mode' if tag in TEST_TAGS else ('english_region' if tag.startswith('en-') else 'non_english_locale'),
            'catalogue_path': path,
            'catalogue_url': f'{REPOSITORY}/blob/{sha}/{path}' if path else None,
            'direct_present_nonempty': len(covered), 'total_translatable_resources': len(baseline),
            'direct_coverage_percent': round(100 * len(covered) / len(baseline), 2),
            'strings_present': sum(k.startswith('string/') for k in covered),
            'strings_total': sum(k.startswith('string/') for k in baseline),
            'plurals_present': sum(k.startswith('plurals/') for k in covered),
            'plurals_total': sum(k.startswith('plurals/') for k in baseline),
            'string_arrays_present': sum(k.startswith('string-array/') for k in covered),
            'string_arrays_total': sum(k.startswith('string-array/') for k in baseline),
            'missing_resource_count': len(missing), 'missing_resource_keys': missing,
            'blank_resource_keys': blank,
            'catalogue_presence': ('no_catalogue' if not path else 'all_source_keys_present' if not missing and not blank else 'partial_source_keys'),
            'local_reference_keys': sorted(references), 'reference_target_absent_in_exact_catalogue': sorted(unresolved_references),
            'literal_equal_to_english_count': len(english_equal), 'literal_equal_to_english_keys': sorted(english_equal),
            'plural_quantities': plural_quantities,
            'quality_acceptance': 'not_established_by_structural_scan',
        }
        rows.append(row)
    aliases = [n.text for n in names_root.findall("string-array[@name='app_language_aliases']/item")]
    alias_targets = [n.text for n in names_root.findall("string-array[@name='app_language_alias_targets']/item")]
    assert len(aliases) == len(alias_targets)
    return {
        'schema_version': 1, 'repository': REPOSITORY, 'source_revision': sha,
        'scope': 'Exact canonical source catalogue presence; not translation quality or runtime fallback resolution.',
        'denominator': dict(Counter(k.split('/')[0] for k in baseline)),
        'excluded_nontranslatable': sorted(set(defaults) - set(baseline)),
        'summary': {'offered_choices': len(rows), 'type_counts': dict(Counter(r['type'] for r in rows)),
                    'catalogue_presence_counts': dict(Counter(r['catalogue_presence'] for r in rows)),
                    'full_non_english_catalogues': sum(r['type']=='non_english_locale' and r['catalogue_presence']=='all_source_keys_present' for r in rows),
                    'picker_matches_system_inventory': tags == system_tags,
                    'all_catalogue_references_have_local_targets': all(not r['reference_target_absent_in_exact_catalogue'] for r in rows)},
        'aliases': dict(zip(aliases, alias_targets)),
        'unoffered_auxiliary_catalogues': {t: p for t, p in catalogues.items() if t not in tags},
        'validation_errors': validation_errors,
        'source_files': manifest, 'locales': rows,
    }

def markdown(report):
    sha = report['source_revision']
    summary = report['summary']
    denominator = report['denominator']
    total = sum(denominator.values())
    all_keys = summary['catalogue_presence_counts'].get('all_source_keys_present', 0)
    partial = summary['catalogue_presence_counts'].get('partial_source_keys', 0)
    kinds = summary['type_counts']
    lines = [
        '# AN Paint per-language translation catalogue baseline', '',
        f'Pinned source: [`{sha}`]({REPOSITORY}/commit/{sha}).', '',
        f"{summary['offered_choices']} offered choices: {kinds.get('non_english_locale', 0)} non-English locale/script/region choices, {kinds.get('english_region', 0)} English regional choices, and {kinds.get('test_mode', 0)} explicitly labelled test modes. Device default is a setting, not a separate language.", '',
        f"The source denominator is **{denominator.get('string', 0)} translatable strings + {denominator.get('plurals', 0)} plural resources + {denominator.get('string-array', 0)} string-arrays = {total} resource keys**. Entries marked translatable=false are excluded.", '',
        f"**{all_keys} exact catalogues have every source key present**; **{partial} are partial**; **{summary['catalogue_presence_counts'].get('no_catalogue', 0)} choices have no exact catalogue**. Structural presence is not accepted linguistic completion.", '',
        '## Definitions and limitations', '',
        '- Present means a nonempty exact-catalogue entry for a translatable default key. A plural is one resource regardless of quantity count; this does not certify every language-required plural form. Local string references count as present; all reference targets are present in the same catalogue.',
        '- Missing means absent in this exact source catalogue. Android may resolve it from a parent, sibling, shared or default resource. These figures do not assert that every missing key displays English. For example, fa-IR and ca-ES-valencia have potential same-language parents.',
        '- The percentage is key presence, not a translation-quality score. Strings equal to English are NOT subtracted: proper names, format identifiers, symbols and numeric templates can legitimately match. JSON records literal equality only as a review aid and excludes resource aliases from that comparison.',
        '- Canonical locale strings.xml files are directly maintained source. Historical JSON catalogues/coverage and imported snapshots are provenance, not live coverage. The generated ko-Kore-KR-anpaint resource directory is a build-time routing mirror of ko-Kore-KR; it contributes no extra language or progress. es and ko source catalogues are unoffered auxiliaries, not separate picker choices.',
        '- The September 28 reset withdrew earlier completion/verification claims. Do not mark a language accepted from this scan. Review state, bounded accepted corrections, pending PRs and release state must be tracked separately.',
        '- This scan does not count hardcoded UI text, dependency strings, external content or verbatim licence bodies. It does not run Android UI/layout tests and does not prove a build is released.', '',
        '## Every offered choice', '',
        f"S = nonempty direct string keys out of {denominator.get('string', 0)}; P = direct plural resources out of {denominator.get('plurals', 0)}; missing and coverage use {total} total keys. “All keys” is structural only. Every row still needs language/semantic acceptance tracked separately.", '',
        '| Locale / canonical catalogue | Display name | Kind | S | P | Missing | Presence | Coverage |',
        '|---|---|---|---:|---:|---:|---|---:|',
    ]
    for r in report['locales']:
        kind = {'test_mode':'Test mode', 'english_region':'English', 'non_english_locale':'Locale'}[r['type']]
        status = 'All keys' if r['catalogue_presence']=='all_source_keys_present' else 'Partial'
        name = r['display_name'].replace('|', '\\|')
        lines.append(f"| [{r['tag']}]({r['catalogue_url']}) | {name} | {kind} | {r['strings_present']} | {r['plurals_present']} | {r['missing_resource_count']} | {status} | {r['direct_coverage_percent']:.2f}% |")
    lines += ['', '## Reproduce', '',
              'Run from any clone that contains the pinned commit (read-only; Python standard library):', '',
              '```sh', f'python3 scan_translation_coverage.py --repo /path/to/AN-Paint --ref {sha} --out ./coverage-output', '```', '',
              'The script reads Git objects at the requested commit, verifies each blob hash, checks exact picker/system inventory equality, excludes translatable=false resources, counts nonempty canonical entries and writes JSON plus this Markdown. JSON includes every missing key, literal-equal-English review keys, local references, locale aliases and input SHA-256/Git-blob provenance.', '',
              'This scanner does not execute the repository’s structural/placeholder validator or Android tests. Separate verification receipts must identify the exact revision and checks actually performed. A missing-key count is not a localization-quality verdict.', '',
              f'Source workflow: [TRANSLATING.md]({REPOSITORY}/blob/{sha}/TRANSLATING.md); [picker tags]({REPOSITORY}/blob/{sha}/{RES}values/app_language_tags.xml); [picker names and aliases]({REPOSITORY}/blob/{sha}/{RES}values/app_language_names.xml); [Android inventory]({REPOSITORY}/blob/{sha}/{RES}xml/app_locales.xml); [build-time routing mirror]({REPOSITORY}/blob/{sha}/Paintroid/build.gradle).', '']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--ref', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args=parser.parse_args()
    sha, manifest, files=read_revision(args.repo, args.ref)
    report=build_report(sha, manifest, files)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    (args.out/'coverage.md').write_text(markdown(report))
    print(json.dumps({'revision':sha, **report['summary']}, indent=2))
    if report['validation_errors']:
        raise SystemExit('Validation failed; see coverage.json')

if __name__=='__main__':
    main()
