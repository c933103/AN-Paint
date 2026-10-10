#!/usr/bin/env python3
"""Validate bounded, app-owned synthetic exports before atomic evidence extraction."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import zipfile

from vertical_locale_matrix import LOCALES, ORIENTATIONS, SCREENS
from vertical_control_reachability import STATES

METHODS = {
    'mnc-Mong': 'manchuPickerRibbonToolsAndJpegUseNativeInputInBothOrientations',
    'lzh-Hant': 'literaryChinesePickerRibbonToolsAndJpegUseNativeInputInBothOrientations',
    'en-XV': 'verticalEnglishPickerRibbonToolsAndJpegUseNativeInputInBothOrientations',
    'qaa-Zsye-XV': 'verticalEmojiPickerRibbonToolsAndJpegUseNativeInputInBothOrientations',
}
MAX_FILE = 2 * 1024 * 1024
MAX_CASE = 8 * 1024 * 1024
MAX_TOTAL = 32 * 1024 * 1024
MAX_MANIFEST = 64 * 1024
MANIFEST_FIELDS = {'version', 'owner', 'locale', 'method', 'device_sdk', 'complete', 'files'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def paths(locale):
    require(locale in METHODS, 'Unknown export locale')
    return {f'{locale}-{orientation}-{screen}.png' for orientation in ORIENTATIONS for screen in SCREENS} | {
        f'reachability/{locale}-{orientation}-{state}.png' for orientation in ORIENTATIONS for state in STATES} | {
        f'reachability/{locale}-{orientation}.json' for orientation in ORIENTATIONS}


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate manifest JSON key')
        result[key] = value
    return result


def bounded_digest(stream, expected, destination=None):
    count = 0
    digest = hashlib.sha256()
    while True:
        block = stream.read(min(65536, expected - count + 1))
        if not block:
            break
        count += len(block)
        require(count <= expected, 'Export exceeds declared byte count')
        digest.update(block)
        if destination is not None:
            destination.write(block)
    require(count == expected, 'Truncated export data')
    return digest.hexdigest()


def inspect_archive(archive, locale, sdk):
    require(not archive.is_symlink() and archive.is_file(), 'Nonregular export ZIP')
    size = archive.stat().st_size
    require(0 < size <= MAX_CASE, 'Oversize or empty export ZIP')
    with archive.open('rb') as stream:
        archive_digest = bounded_digest(stream, size)
    expected = paths(locale)
    with zipfile.ZipFile(archive) as zipped:
        members = zipped.infolist()
        names = [item.filename for item in members]
        require(len(names) == len(set(names)) == 27 and set(names) == expected | {'manifest.json'},
                'Export member inventory mismatch')
        for member in members:
            mode = member.external_attr >> 16
            require(not member.is_dir() and stat.S_IFMT(mode) in (0, stat.S_IFREG), 'Nonregular ZIP member')
            require(not member.flag_bits & 1, 'Encrypted ZIP member')
            require(member.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED), 'Unexpected ZIP compression')
            limit = MAX_MANIFEST if member.filename == 'manifest.json' else MAX_FILE
            require(0 < member.file_size <= limit and 0 <= member.compress_size <= MAX_CASE, 'Oversize ZIP member')
        require(sum(item.file_size for item in members if item.filename != 'manifest.json') <= MAX_CASE,
                'Oversize uncompressed locale export')
        manifest = json.loads(zipped.read('manifest.json'), object_pairs_hook=strict_object)
        require(isinstance(manifest, dict) and set(manifest) == MANIFEST_FIELDS, 'Unknown manifest fields')
        require(type(manifest['version']) is int and manifest['version'] == 1 and
                manifest['owner'] == 'paint.anpaint.android' and manifest['locale'] == locale and
                manifest['method'] == METHODS[locale] and type(manifest['device_sdk']) is int and
                manifest['device_sdk'] == sdk and manifest['complete'] is True, 'Incomplete or foreign export manifest')
        entries = manifest['files']
        require(isinstance(entries, list) and len(entries) == 26, 'Incomplete export file records')
        seen = set()
        for entry in entries:
            require(isinstance(entry, dict) and set(entry) == {'path', 'bytes', 'sha256'}, 'Malformed export file record')
            name = entry['path']
            require(isinstance(name, str) and name in expected and name not in seen, 'Duplicate or unsafe export path')
            seen.add(name)
            require(type(entry['bytes']) is int and 0 < entry['bytes'] <= MAX_FILE and
                    entry['bytes'] == zipped.getinfo(name).file_size, 'Export length metadata mismatch')
            require(isinstance(entry['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', entry['sha256']), 'Malformed export digest')
            with zipped.open(name) as stream:
                require(bounded_digest(stream, entry['bytes']) == entry['sha256'], 'Export content digest mismatch')
        require(seen == expected, 'Missing export file record')
    return {'locale': locale, 'method': METHODS[locale], 'device_sdk': sdk,
            'zip_sha256': archive_digest, 'zip_bytes': size, 'files': entries}


def extract(exports: Path, destination: Path, sdk: int):
    require(type(sdk) is int and sdk in (30, 35), 'Expected API30 or API35')
    require(not exports.is_symlink() and exports.is_dir(), 'Missing or nonregular export directory')
    require({p.name for p in exports.iterdir()} == {f'{locale}.zip' for locale in LOCALES},
            'Missing/extra/renamed locale ZIP')
    require(not os.path.lexists(destination), 'Evidence destination must be fresh')
    # Validate all manifests and content before creating any evidence destination.
    receipts = [inspect_archive(exports / f'{locale}.zip', locale, sdk) for locale in LOCALES]
    require(sum(entry['bytes'] for receipt in receipts for entry in receipt['files']) <= MAX_TOTAL,
            'Combined evidence size exceeded')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.vertical-evidence-', dir=destination.parent) as temporary:
        staged = Path(temporary) / 'evidence'
        staged.mkdir()
        for receipt in receipts:
            archive = exports / (receipt['locale'] + '.zip')
            with archive.open('rb') as stream:
                require(bounded_digest(stream, receipt['zip_bytes']) == receipt['zip_sha256'], 'Export changed after validation')
            with zipfile.ZipFile(archive) as zipped:
                for entry in receipt['files']:
                    path = staged / entry['path']
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with zipped.open(entry['path']) as stream, path.open('xb') as output:
                        require(bounded_digest(stream, entry['bytes'], output) == entry['sha256'], 'Export changed during extraction')
        require(not os.path.lexists(destination), 'Evidence destination appeared during validation')
        os.rename(staged, destination)
    return {'success': True, 'transport': 'app-owned-mediastore-downloads-v1', 'device_sdk': sdk,
            'data_files': 104, 'uncompressed_bytes': sum(e['bytes'] for r in receipts for e in r['files']),
            'locales': receipts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exports', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--sdk', type=int, choices=(30, 35), required=True)
    args = parser.parse_args()
    args.receipt.unlink(missing_ok=True)
    result = extract(args.exports, args.output, args.sdk)
    args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'success': True, 'data_files': result['data_files'], 'device_sdk': args.sdk}))


if __name__ == '__main__':
    main()
