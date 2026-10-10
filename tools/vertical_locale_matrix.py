#!/usr/bin/env python3
"""Fail-closed inventory and screenshot receipts for the installed locale matrix."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

from run_android_instrumentation import (Identity, RESTART_SEED, RESTART_VERIFY,
                                         declared_tests, source_tests_sha256)

VERTICAL = 'paint.anpaint.android.VerticalLocaleDeviceTest'
VERTICAL_METHODS = {
    'manchuPickerRibbonToolsAndJpegUseNativeInputInBothOrientations',
    'literaryChinesePickerRibbonToolsAndJpegUseNativeInputInBothOrientations',
    'verticalEnglishPickerRibbonToolsAndJpegUseNativeInputInBothOrientations',
    'verticalEmojiPickerRibbonToolsAndJpegUseNativeInputInBothOrientations',
}
VERTICAL_SHARDS = {
    'vertical-english-manchu': {
        (VERTICAL, 'verticalEnglishPickerRibbonToolsAndJpegUseNativeInputInBothOrientations'),
        (VERTICAL, 'manchuPickerRibbonToolsAndJpegUseNativeInputInBothOrientations'),
    },
    'vertical-literary-chinese-emoji': {
        (VERTICAL, 'literaryChinesePickerRibbonToolsAndJpegUseNativeInputInBothOrientations'),
        (VERTICAL, 'verticalEmojiPickerRibbonToolsAndJpegUseNativeInputInBothOrientations'),
    },
}
LOCALES = ('mnc-Mong', 'lzh-Hant', 'en-XV', 'qaa-Zsye-XV')
ORIENTATIONS = ('portrait', 'landscape')
SCREENS = ('workspace', 'save-initial', 'format-popup', 'jpeg-quality')
EXPECTED_SCREENSHOTS = {f'{tag}-{orientation}-{screen}.png'
                        for tag in LOCALES for orientation in ORIENTATIONS for screen in SCREENS}


# Compatibility entry points use the authoritative composed app verifier.
# Imports are lazy because the composed module imports the fixed shard constants.
def app_partition(expected: set[Identity], sdk: int) -> dict[str, set[Identity]]:
    from app_instrumentation_matrix import app_partition as composed_partition
    return composed_partition(expected, sdk)


def verify_app_reports(expected: set[Identity], sdk: int, reports: dict[str, dict],
                       source_digest: str, suppressed: set[Identity] | None = None) -> dict:
    from app_instrumentation_matrix import verify_app_reports as composed_verify
    return composed_verify(expected, sdk, reports, source_digest,
                           set() if suppressed is None else suppressed)


def report_paths(root: Path, sdk: int) -> dict[str, Path]:
    from app_instrumentation_matrix import report_paths as composed_paths
    return composed_paths(root, sdk)


def read_app_reports(root: Path, sdk: int) -> dict[str, dict]:
    from app_instrumentation_matrix import read_app_reports as composed_read
    return composed_read(root, sdk)


def verify_screenshots(directory: Path) -> dict:
    actual = {path.name for path in directory.glob('*.png')}
    if actual != EXPECTED_SCREENSHOTS:
        raise ValueError(f'Screenshot matrix mismatch: missing={sorted(EXPECTED_SCREENSHOTS-actual)}, '
                         f'unexpected={sorted(actual-EXPECTED_SCREENSHOTS)}')
    files = []
    content_owners = {}
    for name in sorted(actual):
        data = (directory/name).read_bytes()
        if (len(data) < 33 or data[:8] != b'\x89PNG\r\n\x1a\n'
                or data[8:16] != b'\x00\x00\x00\rIHDR'):
            raise ValueError(f'Invalid PNG header: {name}')
        width, height = struct.unpack('>II', data[16:24])
        if not width or not height:
            raise ValueError(f'Empty PNG dimensions: {name}')
        digest = hashlib.sha256(data).hexdigest()
        if digest in content_owners:
            raise ValueError(f'Duplicate screenshot content: {content_owners[digest]} and {name}')
        content_owners[digest] = name
        files.append(dict(name=name, bytes=len(data), width=width, height=height, sha256=digest))
    # Inventory, header and exact-duplicate checks do not certify rendered state.
    # Reviewers still inspect every actual image.
    return dict(success=True, expected_screenshots=32, files=files)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    reports = commands.add_parser('verify-reports')
    reports.add_argument('--source-tests', type=Path, required=True)
    reports.add_argument('--sdk', type=int, choices=(30, 35), required=True)
    reports.add_argument('--root', type=Path, required=True)
    screenshots = commands.add_parser('verify-screenshots')
    screenshots.add_argument('directory', type=Path)
    screenshots.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'verify-reports':
        from app_instrumentation_matrix import verify_reports
        print(json.dumps(verify_reports(args.source_tests, args.root, args.sdk)))
    else:
        result = verify_screenshots(args.directory)
        args.output.write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({'success': True, 'expected_screenshots': result['expected_screenshots']}))


if __name__ == '__main__':
    main()
