#!/usr/bin/env python3
"""Bind independently executed core/position evidence before accepting their union."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import stat
import zipfile

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



def verify_source_bundle(checkout, archive):
    """Compare bundled tracked bytes to the caller-qualified checkout index, not ZIP claims."""
    entries = subprocess.check_output(['git', '-C', str(checkout), 'ls-files', '--stage', '-z'])
    tracked = {}
    excluded = {'.gitignore', '.idea/codeStyles/Project.xml', 'colorpicker/.gitignore'}
    for entry in entries.split(b'\0'):
        if not entry: continue
        metadata, name = entry.split(b'\t', 1)
        mode, oid, stage = metadata.decode().split()
        name = name.decode('utf-8')
        if stage != '0' or mode not in ('100644', '100755') or len(oid) != 40:
            raise ValueError('Unsupported source index entry')
        if name not in excluded: tracked[name] = oid
    if not tracked or not 0 < archive.stat().st_size <= 512 * 1024 * 1024:
        raise ValueError('Missing or oversized corresponding source')
    native = tuple('Paintroid/build/' + codec + '-source/' for codec in ('jxl', 'webp', 'heif', 'tiff'))
    seen, matched = set(), set()
    with zipfile.ZipFile(archive) as bundle:
        members = bundle.infolist()
        if len(members) > 100000 or sum(m.file_size for m in members) > 2 * 1024**3:
            raise ValueError('Corresponding source exceeds inventory bounds')
        for member in members:
            path = PurePosixPath(member.filename)
            normalized = path.as_posix()
            if (not member.filename or path.is_absolute() or '..' in path.parts
                    or '\\' in member.filename or normalized in seen
                    or stat.S_ISLNK(member.external_attr >> 16) or member.flag_bits & 1
                    or member.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)
                    or member.file_size > 128 * 1024 * 1024
                    or not (normalized.startswith('AN-Paint/') or (normalized == 'AN-Paint' and member.is_dir()))):
                raise ValueError('Unsafe corresponding-source member')
            seen.add(normalized)
            if member.is_dir(): continue
            name = normalized.removeprefix('AN-Paint/')
            if name in tracked:
                digest = hashlib.sha1(f'blob {member.file_size}\0'.encode())
                with bundle.open(member) as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''): digest.update(chunk)
                if digest.hexdigest() != tracked[name]:
                    raise ValueError('Bundled tracked source differs: ' + name)
                matched.add(name)
            elif not name.startswith(native):
                raise ValueError('Unexpected corresponding-source file: ' + name)
    if matched != tracked.keys():
        raise ValueError('Corresponding source omits tracked files')
    return len(matched)


def verify_reuse_artifacts(checkout, prebuilt, core, position, original_environ):
    """Validate bytes already authenticated by the caller; this does NOT qualify a run.

    Caller MUST independently establish successful required jobs from unchanged trusted
    producers, GitHub run/review/tree association, API archive digests, and original
    observed-input identities (including regression and exact-script artifacts).
    This helper does not re-parse successful jobs as a second test-result authority.
    Original S/R identities remain original; no artifact is relabelled as merge M.
    """
    for output in coverage_paths(core) + [core/'composed-device-identity.json']:
        output.unlink(missing_ok=True)
    source = checkout / 'app/src/androidTest'
    identity = checkout_identity(source, original_environ)
    if identity['run_attempt'] != '1' or identity['build_variant'] != 'debug':
        raise ValueError('Reuse only supports original attempt-one debug evidence')
    build = json.loads((prebuilt/'build/delivery/build-info.json').read_text())
    if any(build.get(key) != identity[key] for key in ('commit', 'run_id', 'build_variant')):
        raise ValueError('Original build identity mismatch')
    files = dict(apk_sha256=prebuilt/'app/build/outputs/apk/debug/app-debug.apk',
                 source_sha256=prebuilt/'build/delivery/AN-Paint-source.zip',
                 test_apk_sha256=prebuilt/'app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk')
    hashes = {key: sha256(path) for key, path in files.items()}
    if any(build.get(key) != hashes[key] for key in ('apk_sha256', 'source_sha256')):
        raise ValueError('Original build byte hashes mismatch')
    tracked_count = verify_source_bundle(checkout, files['source_sha256'])
    for root in (core, position):
        device = json.loads((root/'device-identity.json').read_text())
        if any(device.get(key) != value for key, value in hashes.items()):
            raise ValueError('Device evidence differs from actual prebuilt bytes')
    result = compose(source, core, position, 35, original_environ)
    return dict(original_identity=identity, byte_hashes=hashes, tracked_files=tracked_count,
                device=result)


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
