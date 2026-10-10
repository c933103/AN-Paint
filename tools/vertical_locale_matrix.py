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


def app_partition(expected: set[Identity], sdk: int) -> dict[str, set[Identity]]:
    """Account for every SDK-eligible method, including future ordinary classes."""
    if sdk not in (30, 35):
        raise ValueError('The emulator matrix supports SDK 30 or 35')
    vertical = {item for item in expected if item[0] == VERTICAL}
    seed = {item for item in expected if item[0] == RESTART_SEED}
    verify = {item for item in expected if item[0] == RESTART_VERIFY}
    ordinary = expected - vertical - seed - verify
    if vertical != {(VERTICAL, name) for name in VERTICAL_METHODS} or not ordinary:
        raise ValueError('The complete four-locale matrix and ordinary app tests are required')
    shards = list(VERTICAL_SHARDS.values())
    if (len(shards) != 2 or any(len(part) != 2 for part in shards) or shards[0] & shards[1]
            or set.union(*shards) != vertical):
        raise ValueError('Vertical shards must be an exact disjoint two-by-two source inventory')
    partitions = {'ordinary': ordinary, **VERTICAL_SHARDS}
    if len(seed) != 1 or len(verify) != 1:
        raise ValueError('The app inventory requires exactly one seed and one verify method')
    if sdk == 35:
        partitions.update(seed=seed, verify=verify)
    return partitions


def app_sdk(reports: dict[str, dict], requested_sdk: int) -> int:
    """Use one captured integer SDK for every phase and its source inventory."""
    if type(requested_sdk) is not int or requested_sdk not in (30, 35):
        raise ValueError('The emulator matrix supports SDK 30 or 35')
    phases = {'ordinary', *VERTICAL_SHARDS}
    if requested_sdk == 35:
        phases.update(('seed', 'verify'))
    if set(reports) != phases:
        raise ValueError('Completed reports must match every selected app phase exactly')
    captured = [report.get('device_sdk') for report in reports.values()]
    if any(type(sdk) is not int or sdk != requested_sdk for sdk in captured):
        raise ValueError('Every app phase must capture the requested integer device SDK')
    return captured[0]


def verify_app_reports(expected: set[Identity], sdk: int, reports: dict[str, dict],
                       source_digest: str) -> dict:
    if not isinstance(source_digest, str) or not re.fullmatch(r'[0-9a-f]{64}', source_digest):
        raise ValueError('Exact Kotlin test source digest is required')
    sdk = app_sdk(reports, sdk)
    partitions = app_partition(expected, sdk)
    if set(reports) != set(partitions):
        raise ValueError('Completed reports must match every selected app phase exactly')
    completed: set[Identity] = set()
    counts = {}
    for phase, wanted in partitions.items():
        report = reports[phase]
        identities = [(case['classname'], case['name']) for case in report['cases']]
        requested = sorted(f'{owner}#{name}' for owner, name in wanted) if phase in VERTICAL_SHARDS else []
        if (report.get('success') is not True or report.get('device_sdk') != sdk
                or report.get('source_tests_sha256') != source_digest
                or report.get('included_tests') != requested
                or report.get('timeout_seconds') != (60 if phase in ('seed', 'verify') else 180)
                or report.get('timed_out') is not False or report.get('returncode') != 0
                or report.get('errors') != [] or report.get('missing') != [] or report.get('unexpected') != []
                or report.get('leave_target_running') is not (phase == 'seed')
                or report.get('expected_tests') != len(wanted)
                or report.get('completed_tests') != len(wanted)
                or any(case['status'] != 'passed' for case in report['cases'])
                or len(identities) != len(set(identities)) or set(identities) != wanted
                or completed.intersection(identities)):
            raise ValueError(f'{phase} does not prove its exact successful SDK-specific inventory')
        completed.update(identities)
        counts[phase] = len(wanted)
    excluded = {item for item in expected if sdk == 30 and item[0] in (RESTART_SEED, RESTART_VERIFY)}
    if completed != expected - excluded:
        raise ValueError('App reports omit selected SDK-eligible source tests')
    return dict(success=True, device_sdk=sdk, source_tests_sha256=source_digest,
                vertical_timeout_seconds_per_shard=180, vertical_total_timeout_seconds=360,
                declared_tests=len(expected),
                selected_tests=len(expected-excluded), explicitly_excluded_tests=sorted(excluded),
                completed_tests=len(completed), phases=counts, completed=sorted(completed))


def report_paths(root: Path, sdk: int) -> dict[str, Path]:
    paths = {'ordinary': root/'app/androidTest-results/summary.json'}
    paths.update({phase: root/'app-vertical'/phase.removeprefix('vertical-')/'androidTest-results/summary.json'
                  for phase in VERTICAL_SHARDS})
    if sdk == 35:
        paths.update({phase: root/f'app/accepted-credit-restart/{phase}/summary.json'
                      for phase in ('seed', 'verify')})
    return paths


def read_app_reports(root: Path, sdk: int) -> dict[str, dict]:
    paths = report_paths(root, sdk)
    wanted = {paths[phase] for phase in VERTICAL_SHARDS}
    actual = set((root/'app-vertical').rglob('summary.json'))
    if actual != wanted:
        raise ValueError(f'Exact vertical shard report inventory required: '
                         f'missing={sorted(map(str, wanted-actual))}, unexpected={sorted(map(str, actual-wanted))}')
    return {phase: json.loads(path.read_text()) for phase, path in paths.items()}


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
        output = args.root/'app/coverage.json'
        restart_output = args.root/'app/accepted-credit-restart/coverage.json'
        # A failed verification must not leave an earlier successful union receipt.
        output.unlink(missing_ok=True)
        restart_output.unlink(missing_ok=True)
        completed = read_app_reports(args.root, args.sdk)
        sdk = app_sdk(completed, args.sdk)
        expected = declared_tests(args.source_tests, sdk_level=sdk)
        result = verify_app_reports(expected, sdk, completed, source_tests_sha256(args.source_tests))
        output.write_text(json.dumps(result, indent=2)+'\n')
        # Retain the accepted-credit evidence location for existing consumers.
        if args.sdk == 35:
            restart_output.write_text(output.read_text())
        print(json.dumps(result))
    else:
        result = verify_screenshots(args.directory)
        args.output.write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({'success': True, 'expected_screenshots': result['expected_screenshots']}))


if __name__ == '__main__':
    main()
