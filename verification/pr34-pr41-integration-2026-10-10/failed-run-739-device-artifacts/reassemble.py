#!/usr/bin/env python3
"""Verify retained failed-run device archives and reconstruct the exact API35 ZIP.

Run: python3 reassemble.py --output /a/new/output/directory
No archive is extracted. The output directory must not already exist.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
EXPECTED30 = 'a676f3ee8e164864e613c3a696256391bc096df1492763b399641234e8ad12b2'
EXPECTED35 = 'a813678e7a67623567a5b7e890449be7c822c8af38463db22c2a3db9f1463ca6'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def read_checked(path, size, expected):
    require(not path.is_symlink() and path.is_file(), f'Not a regular retained file: {path.name}')
    require(path.stat().st_size == size, f'Wrong size: {path.name}')
    with path.open('rb') as handle:
        data = handle.read(size + 1)
    require(len(data) == size and hashlib.sha256(data).hexdigest() == expected,
            f'Checksum mismatch: {path.name}')
    return data

def verify(directory=ROOT):
    manifest = json.loads((directory / 'manifest.json').read_text())
    require(manifest['run_id'] == 38073935029 and manifest['conclusion'] == 'failure', 'Wrong run/scope')
    a = manifest['device30']; b = manifest['device35']
    require((a['path'], a['bytes'], a['sha256']) == ('device30.zip', 630778, EXPECTED30), 'Wrong API30 identity')
    require((b['path'], b['bytes'], b['sha256']) == ('device35.zip', 5106985, EXPECTED35), 'Wrong API35 identity')
    data30 = read_checked(directory / a['path'], a['bytes'], a['sha256'])
    expected_names = [f'device35.zip.part-{i:03d}' for i in range(20)]
    require([part['path'] for part in b['parts']] == expected_names, 'Wrong part order/inventory')
    require(sorted(p.name for p in directory.glob('device35.zip.part-*')) == expected_names, 'Missing/extra parts')
    pieces = []
    for i, part in enumerate(b['parts']):
        size = min(262144, b['bytes'] - i * 262144)
        require(part['bytes'] == size, 'Wrong bounded part size')
        pieces.append(read_checked(directory / part['path'], size, part['sha256']))
    data35 = b''.join(pieces)
    require(len(data35) == 5106985 and hashlib.sha256(data35).hexdigest() == EXPECTED35, 'Wrong reconstructed ZIP')
    for data in (data30, data35):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            require(archive.testzip() is None, 'Damaged retained ZIP')
    return data35

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = verify()
    if args.output is not None:
        require(not args.output.exists() and not args.output.is_symlink(), 'Output must be fresh')
        args.output.mkdir(parents=False)
        with (args.output / 'device35.zip').open('xb') as handle:
            handle.write(data)
    print(json.dumps({'run_id': 38073935029, 'conclusion': 'failure',
                      'device30_sha256': EXPECTED30, 'device35_sha256': EXPECTED35,
                      'device35_bytes': len(data), 'exact_archives_verified': True}))

if __name__ == '__main__':
    main()
