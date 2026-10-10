#!/usr/bin/env python3
"""Prepare offline release metadata from fresh, already provenance-verified reports.

No network, signing, source modification, merge, or release publication occurs.
The parent must bind downloaded artifacts to the successful exact develop run.
This helper replays instrumentation logs and resolves feature checks by identity,
never by a historical hard-coded TEST-app.xml location.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from string import Template
import xml.etree.ElementTree as ET


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def collect_junit(directory, platform, evidence_root):
    paths = sorted(directory.rglob('TEST-*.xml'))
    require(paths, f'{platform}: no JUnit reports')
    checks, seen = [], set()
    for path in paths:
        require(path.resolve().is_relative_to(evidence_root.resolve()), 'Report escaped evidence root')
        root = ET.parse(path).getroot()
        require(root.tag == 'testsuite', f'{path}: expected one testsuite')
        cases = root.findall('testcase')
        require(cases and int(root.attrib['tests']) == len(cases), f'{path}: empty/wrong test total')
        require(all(int(root.attrib.get(key, '0')) == 0 for key in ('failures', 'errors', 'skipped')),
                f'{path}: failed, errored or skipped suite')
        digest = sha256(path)
        for case in cases:
            identity = (case.attrib['classname'], case.attrib['name'])
            require(all(identity) and identity not in seen, f'{platform}: duplicate/empty identity {identity}')
            require(not any(case.find(key) is not None for key in ('failure', 'error', 'skipped')),
                    f'{path}: unsuccessful test {identity}')
            require(case.attrib.get('status', 'passed') not in ('notrun', 'disabled', 'skipped'),
                    f'{path}: unexecuted test {identity}')
            seen.add(identity)
            checks.append({'platform': platform, 'class': identity[0], 'test': identity[1],
                           'status': 'passed', 'report': path.relative_to(evidence_root).as_posix(),
                           'report_sha256': digest})
    return sorted(checks, key=lambda x: (x['class'], x['test'])), len(paths)


def validate_device(directory, source, sdk):
    from app_instrumentation_matrix import (app_partition, read_app_reports, report_paths,
                                            verify_app_reports, PHASE_TIMEOUTS)
    from run_android_instrumentation import declared_tests, parse_protocol, source_tests_sha256
    app_source = source / 'app/src/androidTest'
    native_source = source / 'Paintroid/src/androidTest'
    expected_app = declared_tests(app_source, sdk_level=sdk)
    reports = read_app_reports(directory, sdk)
    coverage = verify_app_reports(expected_app, sdk, reports, source_tests_sha256(app_source),
                                  declared_tests(app_source) - expected_app)
    phases = app_partition(expected_app, sdk)
    locations = {key: path.parent for key, path in report_paths(directory, sdk).items()}
    native = declared_tests(native_source, sdk_level=sdk)
    exclusions = ['org.catrobat.paintroid.classic.UltraHdrImportTest'] if sdk == 30 else []
    native = {item for item in native if item[0] not in exclusions}
    phases['native'] = native
    locations['native'] = directory / 'Paintroid/androidTest-results'
    expected_xml = set()
    for phase, location in locations.items():
        report = read_json(location / 'summary.json')
        source_path = native_source if phase == 'native' else app_source
        require(report['success'] is True and report['device_sdk'] == sdk, f'{phase}: failed/wrong SDK')
        require(report['source_tests_sha256'] == source_tests_sha256(source_path), f'{phase}: stale test source')
        require(report['returncode'] == 0 and report['timed_out'] is False, f'{phase}: interrupted run')
        require(report['timeout_seconds'] == (180 if phase == 'native' else PHASE_TIMEOUTS[phase]),
                f'{phase}: altered timeout')
        if phase == 'native':
            require(report['excluded_classes'] == exclusions and report['included_tests'] == [],
                    'Unexpected native selector')
            require(report['sdk_suppressed_tests'] == [list(x) for x in sorted(
                declared_tests(native_source) - declared_tests(native_source, sdk_level=sdk))],
                'Native SDK suppression differs from source')
        raw = parse_protocol((location / 'instrumentation.log').read_text(encoding='utf-8'), phases[phase],
                             returncode=report['returncode'], timed_out=report['timed_out'])
        for key in ('success', 'expected_tests', 'completed_tests', 'missing', 'unexpected', 'errors', 'cases'):
            require(raw[key] == report[key], f'{phase}: raw log/summary mismatch: {key}')
        xml = list(location.glob('TEST-*.xml'))
        require(len(xml) == 1, f'{phase}: expected one XML report')
        expected_xml.add(xml[0])
        cases = ET.parse(xml[0]).getroot().findall('testcase')
        identities = [(c.attrib['classname'], c.attrib['name']) for c in cases]
        require(len(identities) == len(set(identities)) and set(identities) == phases[phase],
                f'{phase}: XML does not match source inventory')
    require(set(directory.rglob('TEST-*.xml')) == expected_xml, 'Unexpected/stale emulator XML report')
    return {'installed_tests': sum(map(len, phases.values())), 'native_tests': len(native),
            'app_tests': coverage['completed_tests'], 'app_phases': coverage['phases'],
            'sdk_suppressed_tests': coverage['sdk_suppressed_tests'],
            'explicitly_excluded_tests': coverage['explicitly_excluded_tests']}


def verify_identity(workflow, jobs, info, commit, run_id):
    from publish_github_release import verify_jobs
    require(re.fullmatch(r'[0-9a-f]{40}', commit) is not None, 'Full commit SHA required')
    require(type(run_id) is int and run_id > 0, 'Positive run ID required')
    verify_jobs(workflow, jobs, commit)
    require(workflow.get('status') == 'completed' and workflow.get('id') == run_id,
            'Workflow ID/status mismatch')
    require(info['commit'] == commit and int(info['run_id']) == run_id and info['build_variant'] == 'release',
            'Build artifact identity/variant mismatch')
    for key in ('apk_sha256', 'source_sha256'):
        require(re.fullmatch(r'[0-9a-f]{64}', info[key]) is not None, f'Invalid {key}')
    require(any(job['name'] == 'Exact-script resource generation' and job['status'] == 'completed'
                and job['conclusion'] == 'success' for job in jobs), 'Exact-script generation not passed')



# These are changes of behavior, not mere aliases. Preserve the historical
# identity in the audit summary and require each current replacement separately.
SUPERSEDED = {
    ('regression', 'org.catrobat.paintroid.local.CursorDrawingTest',
     'movingAndTappingNeverToggleInkAndCancelRollsBack'): {
        'reason': 'Cursor taps now toggle ink; off-cursor positioning and cancelled gestures remain non-painting.',
        'current': [
            ('regression', 'org.catrobat.paintroid.local.CursorDrawingTest',
             'touchesAwayFromTheCursorNeverToggleInkAndCancelRollsBack'),
            ('regression', 'org.catrobat.paintroid.local.CursorDrawingTest',
             'tappingTheCursorTogglesInkWithoutPaintingAndDraggingItStillDraws'),
            ('regression', 'org.catrobat.paintroid.local.CursorDrawingTest',
             'cancelledCursorTapDoesNotEnableInkAndCancelledCursorDragRestoresTheImage')],
    },
    ('regression', 'org.catrobat.paintroid.local.ViewportAndVerticalTextTest',
     'canvasDisplayDoesNotBlendNeighbouringPixelsWhenZoomedInOrOut'): {
        'reason': 'Reduced previews now filter neighbouring pixels; magnified pixels stay crisp and source pixels remain unchanged.',
        'current': [
            ('regression', 'org.catrobat.paintroid.local.ViewportAndVerticalTextTest',
             'canvasDisplayFiltersOnlyReducedPreviewsAndPreservesSourcePixels'),
            ('regression', 'org.catrobat.paintroid.local.CanvasBitmapOverviewTest',
             'onePixelStrokesRemainVisibleAtReducedScalesWithoutChangingSourcePixels'),
            ('regression', 'org.catrobat.paintroid.local.CanvasBitmapOverviewTest',
             'magnifiedPixelsStayCrispAndCachedOverviewRefreshesAfterAnEdit')],
    },
}


def reconcile_legacy(legacy, current):
    superseded = []
    missing = legacy - current
    require(missing <= set(SUPERSEDED), f'Unexplained missing historical feature selectors: {sorted(missing - set(SUPERSEDED))}')
    for identity in sorted(missing):
        change = SUPERSEDED[identity]
        require(set(change['current']) <= current, f'Current replacement checks missing for {identity}')
        superseded.append({'historical_selector': identity, **change})
    return {'historical_feature_selectors_present': len(legacy & current),
            'superseded_historical_selectors': superseded}


def assemble(source, evidence, workflow, jobs, info, commit, run_id, signed_hash, public_patch, legacy_request):
    verify_identity(workflow, jobs, info, commit, run_id)
    require(re.fullmatch(r'[0-9a-f]{64}', signed_hash) is not None, 'Final signed APK SHA-256 required')
    require(public_patch.get('format') == 1 and public_patch['input_sha256'] == info['apk_sha256']
            and public_patch['output_sha256'] == signed_hash, 'Public signing patch identity mismatch')
    gradle = (source / 'build.gradle').read_text(encoding='utf-8')
    require(re.search(r"androidVersionCode\s*=\s*95\b", gradle) and
            re.search(r"androidVersionName\s*=\s*'0\.0\.38'", gradle), 'Unexpected version/code')
    checks, jvm_suites = collect_junit(evidence / 'regression/Paintroid/build/test-results/testReleaseUnitTest',
                                     'regression', evidence)
    summary = {'jvm_tests': len(checks), 'jvm_suites': jvm_suites, 'devices': {}}
    lint = evidence / 'regression/app/build/reports/lint-results-release.xml'
    require(ET.parse(lint).getroot().find('issue') is None, 'Release lint contains issues')
    summary['lint_issues'] = 0
    for sdk in (30, 35):
        directory = evidence / f'emulator{sdk}'
        device = validate_device(directory, source, sdk)
        extra, _ = collect_junit(directory, f'emulator{sdk}', evidence)
        require(len(extra) == device['installed_tests'], 'Device test counts differ')
        summary['devices'][str(sdk)] = device
        checks.extend(extra)
    identities = {(c['platform'], c['class'], c['test']) for c in checks}
    legacy = {(c['platform'], c['class'], c['test']) for c in legacy_request['feature_checks']['checks']}
    reconciliation = reconcile_legacy(legacy, identities)
    # Store every current passing test. The old request supplies identities only;
    # its old version, source, run, report locations and hashes never enter output.
    checks.sort(key=lambda x: (x['platform'], x['class'], x['test']))
    request = {'version': '0.0.38', 'version_code': 95, 'commit': commit, 'run_id': run_id,
               'apk_sha256': signed_hash, 'feature_checks': {'checks': checks}}
    summary.update(commit=commit, run_id=run_id, ci_apk_sha256=info['apk_sha256'],
                   signed_apk_sha256=signed_hash, source_sha256=info['source_sha256'],
                   **reconciliation, feature_checks=len(checks))
    return request, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'evidence-root', 'workflow', 'jobs', 'build-info', 'public-signing-patch',
                 'legacy-request', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--run-id', required=True, type=int)
    parser.add_argument('--signed-apk-sha256', required=True)
    parser.add_argument('--notes-template', type=Path, default=Path(__file__).with_name('0.0.38-notes.template.md'))
    args = parser.parse_args()
    sys.path.insert(0, str(args.source.resolve() / 'tools'))
    jobs = read_json(args.jobs)
    jobs = jobs['jobs'] if isinstance(jobs, dict) else jobs
    request, summary = assemble(args.source, args.evidence_root, read_json(args.workflow), jobs,
                               read_json(args.build_info), args.commit, args.run_id, args.signed_apk_sha256,
                               read_json(args.public_signing_patch), read_json(args.legacy_request))
    notes = Template(args.notes_template.read_text(encoding='utf-8')).substitute(
        COMMIT=args.commit, RUN_URL=f'https://github.com/c933103/AN-Paint/actions/runs/{args.run_id}',
        JVM_TESTS=summary['jvm_tests'], JVM_SUITES=summary['jvm_suites'],
        API30_TESTS=summary['devices']['30']['installed_tests'],
        API35_TESTS=summary['devices']['35']['installed_tests'],
        APK_SHA256=args.signed_apk_sha256, SOURCE_SHA256=summary['source_sha256'])
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'request.json').write_text(json.dumps(request, indent=2) + '\n', encoding='utf-8')
    (args.output / 'metadata-validation.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    (args.output / '0.0.38-notes.md').write_text(notes, encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
