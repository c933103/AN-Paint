#!/usr/bin/env python3
"""Exact SDK-aware union for ordinary/gallery/dialog/vertical-shards/restart invocations.

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
POSITION = 'paint.anpaint.android.AssemblyPositionDeviceTest'
POSITION_SHARDS = {
    'position-ainu-manchu': {(POSITION, method) for method in (
        'ainuKanaPositionTextAndNativeEditing', 'ainuLatinPositionTextAndNativeEditing',
        'manchuPositionColumnsAndNativeEditing')},
    'position-tibetan-jeju-nom': {(POSITION, method) for method in (
        'tibetanPositionTextAndNativeEditing', 'dzongkhaPositionTextAndNativeEditing',
        'jejuPositionTextAndNativeEditing', 'nomPositionTextAndNativeEditing')},
}
SUPPORTED_SDKS = (21, 24, 30, 35)
DIALOG = 'paint.anpaint.android.LocalizedDialogDeviceTest'
COLOUR = 'paint.anpaint.android.ColourViewportDeviceTest'
COLOUR_METHODS = {
    'normalAdvancedColourKeepsFiniteViewportAndFixedControls',
    'retainedColourStateSurvivesRotationImeCancelAndReopen',
    'hungarianColourCaptionsFitPortraitAndLandscape',
    'largeEnglishColourCaptionsAndPreviewRemainReachable',
    'largeHungarianColourCaptionsAndPreviewRemainReachable',

}
DIALOG_METHODS = {
    'aboutThirdPartyNoticeRetainsRotationAndNativeFooterFlow',
    'aboutArtworkNoticeCompletesNativeFooterFlow',
    'aboutGimpTranslationNoticeCompletesNativeFooterFlow',
    'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation',
}
PHASE_TIMEOUTS = {'ordinary': 180, 'gallery-draft': 90, 'dialog': 300,
                  **{phase: 180 for phase in (*VERTICAL_SHARDS, *POSITION_SHARDS)}, 'seed': 60, 'verify': 60}
SELECTED_PHASES = {'gallery-draft', 'dialog', *VERTICAL_SHARDS, *POSITION_SHARDS}


def selected_phases(parts: dict, group: str) -> dict:
    if group not in ('all', 'core', 'position'):
        raise ValueError('Unknown app report group')
    return {phase: value for phase, value in parts.items()
            if group == 'all' or (phase in POSITION_SHARDS) == (group == 'position')}


def app_partition(expected: set[Identity], sdk: int) -> dict[str, set[Identity]]:
    """Keep future ordinary methods; require an explicit update for new gallery cases."""
    if type(sdk) is not int or sdk not in SUPPORTED_SDKS:
        raise ValueError('The emulator matrix supports SDK 21, 24, 30 or 35')
    gallery = {item for item in expected if item[0] == GALLERY_DRAFT}
    seed = {item for item in expected if item[0] == RESTART_SEED}
    verify = {item for item in expected if item[0] == RESTART_VERIFY}
    vertical = {item for item in expected if item[0] == VERTICAL}
    dialog = {item for item in expected if item[0] in (DIALOG, COLOUR)}
    position = {item for item in expected if item[0] == POSITION}
    ordinary = expected - gallery - dialog - vertical - seed - verify - position
    if position != (set.union(*POSITION_SHARDS.values()) if sdk >= 30 else set()):
        raise ValueError('Position shards require the exact seven source identities and lower-SDK suppression')
    shards = list(VERTICAL_SHARDS.values())
    if sdk < 30:
        # These whole classes are SDK-suppressed by their source annotations.
        # An unexpected eligible method is a mismatch, never quietly excluded.
        if gallery or vertical or ordinary:
            raise ValueError('Legacy app omission requires no eligible ordinary, gallery or vertical methods')
    elif (vertical != {(VERTICAL, name) for name in VERTICAL_METHODS}
            or len(shards) != 2 or any(len(part) != 2 for part in shards)
            or shards[0] & shards[1] or set.union(*shards) != vertical):
        raise ValueError('Vertical shards must be an exact disjoint two-by-two source inventory')
    if sdk >= 30 and (gallery != {(GALLERY_DRAFT, method) for method in GALLERY_METHODS} or not ordinary):
        raise ValueError('The exact three gallery-draft methods and ordinary app tests are required')
    if len(seed) != 1 or len(verify) != 1:
        raise ValueError('The app inventory requires exactly one seed and one verify method')
    if dialog != ({(DIALOG, method) for method in DIALOG_METHODS} |
                  {(COLOUR, method) for method in COLOUR_METHODS} if sdk == 35 else set()):
        raise ValueError('The exact nine API35 method/class pairs and lower-SDK suppression are required')
    parts = {}
    if sdk >= 30:
        parts.update({'ordinary': ordinary, 'gallery-draft': gallery, **VERTICAL_SHARDS, **POSITION_SHARDS})
    if sdk == 35:
        parts.update(dialog=dialog, seed=seed, verify=verify)
    return parts


def verify_app_reports(expected: set[Identity], sdk: int, reports: dict[str, dict],
                       source_digest: str, suppressed: set[Identity], group: str = 'all') -> dict:
    if not isinstance(source_digest, str) or not re.fullmatch(r'[0-9a-f]{64}', source_digest):
        raise ValueError('Exact Kotlin test source digest is required')
    all_parts = app_partition(expected, sdk)
    parts = selected_phases(all_parts, group)
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
    excluded = {item for item in expected if sdk < 35 and item[0] in (RESTART_SEED, RESTART_VERIFY)}
    deferred = set().union(*(value for phase, value in all_parts.items() if phase not in parts))
    if completed != expected - excluded - deferred or completed & suppressed:
        raise ValueError('App reports omit selected SDK-eligible source tests')
    return dict(success=True if parts else None,
                execution_status='passed' if parts else 'not-run-no-sdk-eligible-selected-tests',
                inventory_validated=True, device_sdk=sdk, source_tests_sha256=source_digest,
                timeout_seconds_by_phase={phase: PHASE_TIMEOUTS[phase] for phase in parts},
                dialog_timeout_seconds=300 if sdk == 35 else 0,
                colour_scope=('source-bound-positive-normal-font; API35 en-US/hu 2x 640x320 mdpi '
                              'preview-rail reachability and Cancel only; whole-dialog and universal 2x not accepted'
                              if sdk == 35 else 'installed colour not selected on this SDK; model coverage is separate'),
                ordinary_and_gallery_total_timeout_seconds=sum(PHASE_TIMEOUTS[phase] for phase in parts
                                                               if phase in ('ordinary', 'gallery-draft')),
                vertical_timeout_seconds_per_shard=180 if sdk >= 30 else None,
                vertical_total_timeout_seconds=sum(PHASE_TIMEOUTS[phase] for phase in parts if phase in VERTICAL_SHARDS),
                receipt_scope=("complete-composed-app-union" if group == 'all' else f"partial-{group}-app-union")
                              if parts else "sdk-ineligible-app-omission",
                deferred_tests=sorted(deferred),
                all_app_total_timeout_seconds=sum(PHASE_TIMEOUTS[phase] for phase in parts),
                declared_tests=len(expected | suppressed), sdk_eligible_tests=len(expected),
                sdk_suppressed_tests=sorted(suppressed),
                selected_tests=len(expected-excluded-deferred), explicitly_excluded_tests=sorted(excluded),
                completed_tests=len(completed), phases=counts, completed=sorted(completed))


def report_paths(root: Path, sdk: int, group: str = 'all') -> dict[str, Path]:
    if type(sdk) is not int or sdk not in SUPPORTED_SDKS:
        raise ValueError('The emulator matrix supports SDK 21, 24, 30 or 35')
    paths = {}
    if sdk >= 30:
        paths['ordinary'] = root/'app/androidTest-results/summary.json'
        paths['gallery-draft'] = root/'app-gallery-draft/androidTest-results/summary.json'
        paths.update({phase: root/'app-vertical'/phase.removeprefix('vertical-')/'androidTest-results/summary.json'
                      for phase in VERTICAL_SHARDS})
        paths.update({phase: root/'app-position'/phase.removeprefix('position-')/'androidTest-results/summary.json'
                      for phase in POSITION_SHARDS})
    if sdk == 35:
        paths['dialog'] = root/'app-dialog/androidTest-results/summary.json'
        paths.update({phase: root/f'app/accepted-credit-restart/{phase}/summary.json'
                      for phase in ('seed', 'verify')})
    return selected_phases(paths, group)


def read_app_reports(root: Path, sdk: int, group: str = 'all') -> dict[str, dict]:
    paths = report_paths(root, sdk, group)
    wanted = set(paths.values())
    actual = set().union(*((root/name).rglob('summary.json')
                          for name in ('app', 'app-gallery-draft', 'app-dialog', 'app-vertical', 'app-position')))
    if actual != wanted:
        raise ValueError(f'Exact composed app report inventory required: missing={sorted(map(str, wanted-actual))}, '
                         f'unexpected={sorted(map(str, actual-wanted))}')
    return {phase: json.loads(path.read_text()) for phase, path in paths.items()}


def coverage_paths(root: Path) -> list[Path]:
    # All compatibility receipts attest the SAME complete union, never an
    # independently accepted subset. Clear all four before any validation.
    return [root/'app/coverage.json', root/'app/ordinary-gallery-coverage.json',
            root/'app/vertical-coverage.json', root/'app/accepted-credit-restart/coverage.json']


def verify_reports(source: Path, root: Path, sdk: int, group: str = 'all') -> dict:
    outputs = coverage_paths(root)
    for output in outputs + [root/'core-coverage.json', root/'position-coverage.json']:
        output.unlink(missing_ok=True)
    reports = read_app_reports(root, sdk, group)
    expected = declared_tests(source, sdk_level=sdk)
    result = verify_app_reports(expected, sdk, reports, source_tests_sha256(source),
                                declared_tests(source) - expected, group)
    content = json.dumps(result, indent=2)+'\n'
    if group != 'all':
        selected_outputs = [root/f'{group}-coverage.json']
    elif sdk == 35:
        selected_outputs = outputs
    elif sdk >= 30:
        selected_outputs = outputs[:-1]
    else:
        selected_outputs = outputs[:1]
    for output in selected_outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-tests', type=Path, required=True)
    parser.add_argument('--sdk', type=int, choices=SUPPORTED_SDKS, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--group', choices=('all', 'core', 'position'), default='all')
    args = parser.parse_args()
    print(json.dumps(verify_reports(args.source_tests, args.root, args.sdk, args.group)))


if __name__ == '__main__':
    main()
