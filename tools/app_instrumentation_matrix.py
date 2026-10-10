#!/usr/bin/env python3
"""Exact SDK-aware union for ordinary/gallery/vertical-shards/restart invocations.

Uses the selector, source-digest and report conventions already reviewed in PR41.
No successful phase substitutes for a missing, skipped or failed method elsewhere.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from run_android_instrumentation import (Identity, RESTART_SEED, RESTART_VERIFY,
                                         declared_tests, source_tests_sha256)

from vertical_locale_matrix import VERTICAL, VERTICAL_METHODS, VERTICAL_SHARDS

GALLERY_DRAFT = 'paint.anpaint.android.GalleryDraftDeviceTest'
GALLERY_METHODS = {
    'cancelledRecreatedGalleryDraftKeepsTheOriginalDocumentAndCredits',
    'confirmedRecreatedGalleryDraftReturnsToTheCoveredRecreatedEditor',
    'savedFirstCreditSurvivesRecreationAndCancellationOfAnEmptySecondDraft',
}
PHASE_TIMEOUTS = {'ordinary': 180, 'gallery-draft': 90,
                  **{phase: 180 for phase in VERTICAL_SHARDS}, 'seed': 60, 'verify': 60}
SELECTED_PHASES = {'gallery-draft', *VERTICAL_SHARDS}


def app_partition(expected: set[Identity], sdk: int) -> dict[str, set[Identity]]:
    """Keep future ordinary methods; require an explicit update for new gallery cases."""
    if type(sdk) is not int or sdk not in (30, 35):
        raise ValueError('The emulator matrix supports SDK 30 or 35')
    gallery = {item for item in expected if item[0] == GALLERY_DRAFT}
    seed = {item for item in expected if item[0] == RESTART_SEED}
    verify = {item for item in expected if item[0] == RESTART_VERIFY}
    vertical = {item for item in expected if item[0] == VERTICAL}
    ordinary = expected - gallery - vertical - seed - verify
    shards = list(VERTICAL_SHARDS.values())
    if (vertical != {(VERTICAL, name) for name in VERTICAL_METHODS}
            or len(shards) != 2 or any(len(part) != 2 for part in shards)
            or shards[0] & shards[1] or set.union(*shards) != vertical):
        raise ValueError('Vertical shards must be an exact disjoint two-by-two source inventory')
    if gallery != {(GALLERY_DRAFT, method) for method in GALLERY_METHODS} or not ordinary:
        raise ValueError('The exact three gallery-draft methods and ordinary app tests are required')
    if len(seed) != 1 or len(verify) != 1:
        raise ValueError('The app inventory requires exactly one seed and one verify method')
    parts = {'ordinary': ordinary, 'gallery-draft': gallery, **VERTICAL_SHARDS}
    if sdk == 35:
        parts.update(seed=seed, verify=verify)
    return parts


def verify_app_reports(expected: set[Identity], sdk: int, reports: dict[str, dict],
                       source_digest: str, suppressed: set[Identity]) -> dict:
    if not isinstance(source_digest, str) or not re.fullmatch(r'[0-9a-f]{64}', source_digest):
        raise ValueError('Exact Kotlin test source digest is required')
    parts = app_partition(expected, sdk)
    if set(reports) != set(parts):
        raise ValueError('Completed reports must match every selected app phase exactly')
    completed: set[Identity] = set()
    counts = {}
    for phase, wanted in parts.items():
        report = reports[phase]
        identities = [(case['classname'], case['name']) for case in report['cases']]
        requested = sorted(f'{owner}#{name}' for owner, name in wanted) if phase in SELECTED_PHASES else []
        if (report.get('success') is not True or type(report.get('device_sdk')) is not int
                or report['device_sdk'] != sdk or report.get('source_tests_sha256') != source_digest
                or report.get('sdk_suppressed_tests') != [list(item) for item in sorted(suppressed)]
                or report.get('included_tests') != requested
                or report.get('timeout_seconds') != PHASE_TIMEOUTS[phase]
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
    if completed != expected - excluded or completed & suppressed:
        raise ValueError('App reports omit selected SDK-eligible source tests')
    return dict(success=True, device_sdk=sdk, source_tests_sha256=source_digest,
                timeout_seconds_by_phase={phase: PHASE_TIMEOUTS[phase] for phase in parts},
                ordinary_and_gallery_total_timeout_seconds=270,
                vertical_timeout_seconds_per_shard=180, vertical_total_timeout_seconds=360,
                receipt_scope="complete-composed-app-union",
                all_app_total_timeout_seconds=sum(PHASE_TIMEOUTS[phase] for phase in parts),
                declared_tests=len(expected | suppressed), sdk_eligible_tests=len(expected),
                sdk_suppressed_tests=sorted(suppressed),
                selected_tests=len(expected-excluded), explicitly_excluded_tests=sorted(excluded),
                completed_tests=len(completed), phases=counts, completed=sorted(completed))


def report_paths(root: Path, sdk: int) -> dict[str, Path]:
    if type(sdk) is not int or sdk not in (30, 35):
        raise ValueError('The emulator matrix supports SDK 30 or 35')
    paths = {'ordinary': root/'app/androidTest-results/summary.json',
             'gallery-draft': root/'app-gallery-draft/androidTest-results/summary.json'}
    paths.update({phase: root/'app-vertical'/phase.removeprefix('vertical-')/'androidTest-results/summary.json'
                  for phase in VERTICAL_SHARDS})
    if sdk == 35:
        paths.update({phase: root/f'app/accepted-credit-restart/{phase}/summary.json'
                      for phase in ('seed', 'verify')})
    return paths


def read_app_reports(root: Path, sdk: int) -> dict[str, dict]:
    paths = report_paths(root, sdk)
    wanted = set(paths.values())
    actual = set().union(*((root/name).rglob('summary.json')
                          for name in ('app', 'app-gallery-draft', 'app-vertical')))
    if actual != wanted:
        raise ValueError(f'Exact composed app report inventory required: missing={sorted(map(str, wanted-actual))}, '
                         f'unexpected={sorted(map(str, actual-wanted))}')
    return {phase: json.loads(path.read_text()) for phase, path in paths.items()}


def coverage_paths(root: Path) -> list[Path]:
    # All compatibility receipts attest the SAME complete union, never an
    # independently accepted subset. Clear all four before any validation.
    return [root/'app/coverage.json', root/'app/ordinary-gallery-coverage.json',
            root/'app/vertical-coverage.json', root/'app/accepted-credit-restart/coverage.json']


def verify_reports(source: Path, root: Path, sdk: int) -> dict:
    outputs = coverage_paths(root)
    for output in outputs:
        output.unlink(missing_ok=True)
    reports = read_app_reports(root, sdk)
    expected = declared_tests(source, sdk_level=sdk)
    result = verify_app_reports(expected, sdk, reports, source_tests_sha256(source),
                                declared_tests(source) - expected)
    content = json.dumps(result, indent=2)+'\n'
    selected_outputs = outputs if sdk == 35 else outputs[:-1]
    for output in selected_outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-tests', type=Path, required=True)
    parser.add_argument('--sdk', type=int, choices=(30, 35), required=True)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify_reports(args.source_tests, args.root, args.sdk)))


if __name__ == '__main__':
    main()
