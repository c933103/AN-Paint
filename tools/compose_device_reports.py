#!/usr/bin/env python3
"""Bind independently executed core/position evidence before accepting their union."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

from app_instrumentation_matrix import (coverage_paths, read_app_reports, report_paths,
                                         verify_app_reports, verify_reports)
from run_android_instrumentation import declared_tests, source_tests_sha256


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checkout_identity(source, environ):
    commit, run, attempt, variant = (environ[key] for key in
        ('GITHUB_SHA', 'GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT', 'BUILD_VARIANT'))
    if (not re.fullmatch(r'[0-9a-f]{40}', commit) or not re.fullmatch(r'[1-9][0-9]*', run) or not re.fullmatch(r'[1-9][0-9]*', attempt)
            or variant not in ('debug', 'release')):
        raise ValueError('Exact Actions checkout/run/attempt/variant identity required')
    return dict(commit=commit, run_id=run, run_attempt=attempt, build_variant=variant,
                source_tests_sha256=source_tests_sha256(source))


def record(source, prebuilt, root, sdk, group, environ):
    (root/'device-identity.json').unlink(missing_ok=True)
    identity = checkout_identity(source, environ)
    build = json.loads((prebuilt/'build/delivery/build-info.json').read_text())
    if any(build.get(key) != identity[key] for key in ('commit', 'run_id', 'build_variant')):
        raise ValueError('Prebuilt APK artifact does not match this checkout/run/variant')
    variant = identity['build_variant']
    main = sha256(prebuilt/f'app/build/outputs/apk/{variant}/app-{variant}.apk')
    source_zip = sha256(prebuilt/'build/delivery/AN-Paint-source.zip')
    if main != build.get('apk_sha256') or source_zip != build.get('source_sha256'):
        raise ValueError('Prebuilt APK/source bytes do not match build identity')
    identity.update(device_sdk=sdk, apk_sha256=main, source_sha256=source_zip,
        test_apk_sha256=sha256(prebuilt/f'app/build/outputs/apk/androidTest/{variant}/app-{variant}-androidTest.apk'))
    root.mkdir(parents=True, exist_ok=True)
    (root/'device-identity.json').write_text(json.dumps(dict(group=group, **identity), indent=2)+'\n')
    return identity


def compose(source, core, position, sdk, environ):
    # Failed composition must never retain a prior complete receipt.
    for output in coverage_paths(core) + [core/'composed-device-identity.json']:
        output.unlink(missing_ok=True)
    expected_identity = checkout_identity(source, environ)
    current_attempt = int(expected_identity.pop('run_attempt'))
    attempts = {}
    eligible = declared_tests(source, sdk_level=sdk)
    suppressed = declared_tests(source)-eligible
    identities = []
    for group, root in (('core', core), ('position', position)):
        identity = json.loads((root/'device-identity.json').read_text())
        attempt = identity.pop('run_attempt', None)
        if (not isinstance(attempt, str) or not re.fullmatch(r'[1-9][0-9]*', attempt)
                or int(attempt) > current_attempt):
            raise ValueError('Evidence requires a positive run attempt no later than the current attempt')
        attempts[group] = int(attempt)
        if identity.pop('group', None) != group or identity.get('device_sdk') != sdk:
            raise ValueError('Wrong evidence group or SDK')
        if any(identity.get(key) != value for key, value in expected_identity.items()):
            raise ValueError('Evidence does not match this checkout/run/variant/test source')
        if any(not re.fullmatch(r'[0-9a-f]{64}', identity.get(key, ''))
               for key in ('apk_sha256', 'source_sha256', 'test_apk_sha256')):
            raise ValueError('Complete prebuilt APK/source identity required')
        verify_app_reports(eligible, sdk, read_app_reports(root, sdk, group),
                           expected_identity['source_tests_sha256'], suppressed, group)
        identities.append(identity)
    if identities[0] != identities[1]:
        raise ValueError('Core and position jobs did not execute the same prebuilt APKs/source')
    for phase, path in report_paths(position, sdk, 'position').items():
        target = report_paths(core, sdk, 'position')[phase]
        target.parent.mkdir(parents=True, exist_ok=True)
        # Preserve raw output and JUnit siblings, not just successful summaries.
        shutil.copytree(path.parent, target.parent, dirs_exist_ok=True)
    result = verify_reports(source, core, sdk)
    result['device_identity'] = dict(**identities[0], group_run_attempts=attempts,
                                     composed_in_run_attempt=current_attempt)
    for output in coverage_paths(core):
        if output.exists(): output.write_text(json.dumps(result, indent=2)+'\n')
    (core/'composed-device-identity.json').write_text(json.dumps(result['device_identity'], indent=2)+'\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('record', 'compose'))
    parser.add_argument('--sdk', type=int, choices=(30, 35), required=True)
    parser.add_argument('--source-tests', type=Path, default=Path('app/src/androidTest'))
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--position-root', type=Path)
    parser.add_argument('--prebuilt', type=Path, default=Path('build/prebuilt'))
    parser.add_argument('--group', choices=('core', 'position'))
    args = parser.parse_args()
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if actual != os.environ['GITHUB_SHA']:
        raise ValueError('Working checkout does not match Actions SHA')
    if args.action == 'record':
        if not args.group: parser.error('record requires --group')
        result = record(args.source_tests, args.prebuilt, args.root, args.sdk, args.group, os.environ)
    else:
        if args.position_root is None: parser.error('compose requires --position-root')
        result = compose(args.source_tests, args.root, args.position_root, args.sdk, os.environ)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
