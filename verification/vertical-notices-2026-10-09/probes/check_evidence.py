#!/usr/bin/env python3
"""Revalidate recorded evidence, without rerunning native tests.

All acceptance checks remain active under python -O. --self-test exercises both
normal and optimized invocations, using isolated copies and synthetic corruption.
"""
from pathlib import Path, PurePosixPath
import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_FILES = set('''README.md
artifact-manifest.json
data/host-api30.tsv.gz
data/host-api35.tsv.gz
data/measurements-api30.tsv.gz
data/measurements-api35.tsv.gz
data/routes-api30.tsv.gz
data/routes-api35.tsv.gz
data/transitions-api30.tsv.gz
data/transitions-api35.tsv.gz
dependencies.json
execution.json
fixture-ledger.json
images/api30-en-xv-clipped.png
images/api30-en-xv-reference.png
images/api35-lzh-clipped.png
images/api35-lzh-reference.png
inputs.json
integration-audit.json
logs/compile.log
logs/host-api30.log
logs/host-api35.log
logs/host-python.log
logs/lifecycle-api30.log
logs/lifecycle-api35.log
logs/measurement-api30.log
logs/measurement-api35.log
logs/transitions-api30.log
logs/transitions-api35.log
probe-sources.json
probes/NoticeColours.kt
probes/NoticeTransitionProbe.kt
probes/ProbeSubsetRunner.kt
probes/VerticalNoticeHostProbe.kt
probes/VerticalNoticeMeasurementProbe.kt
probes/check_evidence.py
probes/check_runner_inputs.py
probes/run.py
provenance.json
run-plan.json
run-status.json
runner-input-checks.json
summary.json'''.splitlines())
DERIVED = {'README.md', 'artifact-manifest.json', 'probes/check_evidence.py', 'provenance.json'}
FROZEN_COMMIT = '3f8bb0f64cfad485a1e725223d3475d8d60f9e5b'
INTEGRATION_COMMIT = '748a03d496b6b053f9dba1835a11f7d9748275f7'


class InvalidEvidence(Exception):
    pass


def require(condition, message):
    if not condition:
        raise InvalidEvidence(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(value):
    require(isinstance(value, str) and value, 'Unsafe manifest/source path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and bool(path.parts) and str(path) == value and
            all(part not in ('.', '..') for part in path.parts) and
            '\\' not in value and ':' not in value,
            'Unsafe manifest/source path: ' + value)
    return path


def read_json(root, name):
    return json.loads((root / name).read_text())


def read_rows(root, name):
    data = gzip.decompress((root / 'data' / name).read_bytes()).decode()
    return list(csv.DictReader(io.StringIO(data), delimiter='\t'))


def verify(root, repo):
    manifest = read_json(root, 'artifact-manifest.json')
    require(isinstance(manifest, list), 'Manifest must be a list')
    paths = []
    for item in manifest:
        path = str(safe_path(item['path']))
        require(type(item['bytes']) is int and item['bytes'] >= 0,
                'Invalid manifest byte count: ' + path)
        require(isinstance(item['sha256'], str) and
                re.fullmatch('[0-9a-f]{64}', item['sha256']),
                'Invalid manifest digest: ' + path)
        paths.append(path)
    require(len(paths) == len(set(paths)), 'Duplicate manifest entries')
    require(set(paths) == EXPECTED_FILES - {'artifact-manifest.json'},
            'Incomplete or unexpected manifest entries')
    all_paths = list(root.rglob('*'))
    require(not any(path.is_symlink() for path in all_paths), 'Symlink in evidence package')
    actual = {str(path.relative_to(root)) for path in all_paths if path.is_file()}
    require(actual == EXPECTED_FILES, 'Unlisted or missing package files')
    for item in manifest:
        data = (root / item['path']).read_bytes()
        require(len(data) == item['bytes'] and digest(data) == item['sha256'],
                'Artifact byte/hash mismatch: ' + item['path'])

    audit = read_json(root, 'integration-audit.json')
    require(audit['measured_commit'] == FROZEN_COMMIT and
            audit['integration_base_commit'] == INTEGRATION_COMMIT,
            'Unexpected provenance commits')
    frozen = read_json(root, 'inputs.json')
    records = audit['source_delta']['inputs']
    audited = {item['path']: item for item in records}
    require(len(audited) == len(records) == len(frozen) == 15 and
            set(audited) == {item['path'] for item in frozen},
            'Source inventory mismatch')
    for item in frozen:
        path = str(safe_path(item['path']))
        record = audited[path]
        require(record['frozen_sha256'] == item['sha256'], 'Frozen source metadata mismatch: ' + path)
        data = (repo / path).read_bytes()
        require(digest(data) in {item['sha256'], record['integration_sha256']},
                'Unaudited source bytes: ' + path)
        projection = record.get('projection')
        if projection and projection['kind'] == 'catalogue-values':
            values = {e.attrib['name']: ''.join(e.itertext()) for e in ET.fromstring(data) if e.tag == 'string'}
            selected = {key: values[key] for key in projection['keys']}
            encoded = json.dumps(selected, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
            require(digest(encoded) == projection['sha256'], 'Measured catalogue projection mismatch: ' + path)
        elif projection and projection['kind'] == 'exact-caller-line':
            require(data.decode().count(projection['text']) == projection['occurrences'] == 1,
                    'Cursor caller projection mismatch: ' + path)
        elif projection:
            raise InvalidEvidence('Unknown source projection: ' + path)

    status = read_json(root, 'run-status.json')
    execution = read_json(root, 'execution.json')
    plan = read_json(root, 'run-plan.json')
    expected_plan = ['compile'] + [f'{suite}-api{api}' for api in (30, 35)
                                 for suite in ('measurement', 'host', 'transitions', 'lifecycle')]
    require(status == {'state': 'completed', 'planned_stages': 9, 'completed_stages': 9},
            'Incomplete historical stage status')
    require(plan == expected_plan and [item['stage'] for item in execution] == plan and
            len(execution) == 9 and all(item['state'] == 'passed' and item['exit_code'] == 0 for item in execution),
            'Inconsistent historical stage execution')
    rejections = read_json(root, 'runner-input-checks.json')
    require(len(rejections) == 3 and all(item['passed'] is True and item['exit_code'] == 2 for item in rejections),
            'Historical runner input checks incomplete')
    summary = read_json(root, 'summary.json')
    require(summary['source_commit'] == FROZEN_COMMIT, 'Summary source mismatch')
    require(summary['normal_host_tests'] == 304 and summary['selected_native_test_executions'] == 32 and
            summary['runner_input_rejection_checks'] == 3, 'Inconsistent summary execution totals')
    for api, expected_fits, expected_clips in ((30, 390, 72), (35, 420, 78)):
        key = str(api)
        shape = read_rows(root, f'measurements-api{api}.tsv.gz')
        host = read_rows(root, f'host-api{api}.tsv.gz')
        routes = read_rows(root, f'routes-api{api}.tsv.gz')
        transitions = read_rows(root, f'transitions-api{api}.tsv.gz')
        require(len(shape) == summary['shaping_sweep'][key]['rows'] == 4320,
                'Inconsistent shaping count: ' + key)
        require(len(host) == summary['attached_host'][key]['rows'] == 560,
                'Inconsistent attached-host count: ' + key)
        fits = [item for item in host if item['fits'] == 'true']
        clipped = [item for item in fits if int(item['outsideBodyPixels']) > 0]
        require(len(fits) == summary['attached_host'][key]['nominal_fits'] == expected_fits,
                'Inconsistent nominal-fit count: ' + key)
        require(len(clipped) == summary['attached_host'][key]['actually_clipped_fitting_cases'] == expected_clips and
                all(item['key'] == 'unsupported-zwj-file' for item in clipped),
                'Inconsistent clipped-case count: ' + key)
        require(len(routes) == len({item['tag'] for item in routes}) == 140 and
                {item['tag'] for item in routes if item['route'] == 'foreground-horizontal'} == {'vi-Hani', 'wuu-Hans'},
                'Inconsistent route evidence: ' + key)
        require(len(transitions) == summary['transitions'][key]['rows'] == 20, 'Inconsistent transition count: ' + key)
        require(summary['transitions'][key]['resized_rows'] == [item for item in transitions if item['phase'] == 'resized'],
                'Inconsistent resized-row summary: ' + key)
        require(summary['routes'][key] == {'picker_tags': 140, 'foreground_horizontal': ['vi-Hani', 'wuu-Hans'],
                                         'system_toast_count': 138, 'vertical_profiles_remain_system_owned': True},
                'Inconsistent route summary: ' + key)
        representative = [item for item in summary['counterexample']['representative_rows'] if item['sdk'] == key]
        require(len(representative) == 3 and all(item in host for item in representative),
                'Inconsistent counterexample summary: ' + key)
        for suite, count in (('measurement', 1), ('host', 2), ('transitions', 1)):
            expected = f'OK ({count} test' + ('s' if count != 1 else '') + ')'
            require(expected in (root / 'logs' / f'{suite}-api{api}.log').read_text(), 'Historical native log mismatch')
        require('RUN=12 FAIL=0 IGNORED=0' in (root / 'logs' / f'lifecycle-api{api}.log').read_text(),
                'Historical lifecycle log mismatch')
    host_log = (root / 'logs/host-python.log').read_text()
    require('Ran 304 tests' in host_log and '\nOK\n' in host_log, 'Historical host log mismatch')
    fresh = audit['fresh_validation']
    require(fresh['source_commit'] == INTEGRATION_COMMIT and fresh['tests'] == 307 and
            fresh['exit_code'] == fresh['failures'] == fresh['skips'] == 0 and
            digest(fresh['log'].encode()) == fresh['log_sha256'] and
            'Ran 307 tests' in fresh['log'] and '\nOK\n' in fresh['log'],
            'Recovery-time host result mismatch')

    recovery = audit['recovery']
    historical = recovery['historical_artifacts']
    require(recovery['verified_original_files'] == len(historical) == 42 and
            len({item['path'] for item in historical}) == 42 and
            {item['path'] for item in historical} == EXPECTED_FILES - {'integration-audit.json'},
            'Historical recovery inventory mismatch')
    require(set(recovery['new_recovery_revisions']) == DERIVED and recovery['new_files'] == ['integration-audit.json'],
            'Recovery revision classification mismatch')
    preserved = [item for item in historical if item['publication_classification'] == 'byte-exact historical artifact']
    require(len(preserved) == recovery['publication_byte_exact_original_files'] == 38 and
            {item['path'] for item in preserved} == EXPECTED_FILES - DERIVED - {'integration-audit.json'},
            'Preserved historical inventory mismatch')
    for item in preserved:
        data = (root / item['path']).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(len(data) == item['bytes'] and digest(data) == item['sha256'] and blob == item['git_blob'],
                'Preserved historical artifact changed: ' + item['path'])


def self_test(repo):
    """Changes only temporary copies; every child runs the same published checker."""
    results = []
    cases = [('baseline', None), ('changed-bytes', 'Artifact byte/hash mismatch'),
             ('truncated-bytes', 'Artifact byte/hash mismatch'),
             ('omitted-entry', 'Incomplete or unexpected manifest entries'),
             ('duplicate-entry', 'Duplicate manifest entries'),
             ('unsafe-path', 'Unsafe manifest/source path'),
             ('missing-file', 'Unlisted or missing package files'),
             ('source-mismatch', 'Unaudited source bytes'),
             ('stage-status', 'Incomplete historical stage status'),
             ('stage-execution', 'Inconsistent historical stage execution'),
             ('count-metadata', 'Inconsistent shaping count')]
    for name, expected_error in cases:
        with tempfile.TemporaryDirectory(prefix='an-evidence-check-') as directory:
            temp = Path(directory)
            package = temp / 'package'
            shutil.copytree(ROOT, package)
            source = repo
            def write_json(path, value):
                (package / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
            def refresh_manifest(path):
                manifest = read_json(package, 'artifact-manifest.json')
                data = (package / path).read_bytes()
                for item in manifest:
                    if item['path'] == path:
                        item.update(bytes=len(data), sha256=digest(data))
                write_json('artifact-manifest.json', manifest)
            if name == 'changed-bytes':
                path = package / 'summary.json'; path.write_bytes(path.read_bytes() + b'\n')
            elif name == 'truncated-bytes':
                path = package / 'data/host-api30.tsv.gz'; path.write_bytes(path.read_bytes()[:-1])
            elif name in ('omitted-entry', 'duplicate-entry', 'unsafe-path'):
                manifest = read_json(package, 'artifact-manifest.json')
                if name == 'omitted-entry': manifest.pop()
                elif name == 'duplicate-entry': manifest.append(dict(manifest[0]))
                else: manifest[0]['path'] = '../outside'
                write_json('artifact-manifest.json', manifest)
            elif name == 'missing-file':
                (package / 'logs/compile.log').unlink()
            elif name == 'source-mismatch':
                source = temp / 'source'
                for item in read_json(ROOT, 'inputs.json'):
                    path = str(safe_path(item['path']))
                    destination = source / path; destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(repo / path, destination)
                path = source / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt'
                path.write_bytes(path.read_bytes() + b'\n')
            elif name == 'stage-status':
                data = read_json(package, 'run-status.json'); data['completed_stages'] = 8
                write_json('run-status.json', data); refresh_manifest('run-status.json')
            elif name == 'stage-execution':
                data = read_json(package, 'execution.json'); data[-1]['state'] = 'failed'; data[-1]['exit_code'] = 1
                write_json('execution.json', data); refresh_manifest('execution.json')
            elif name == 'count-metadata':
                data = read_json(package, 'summary.json'); data['shaping_sweep']['30']['rows'] = 1
                write_json('summary.json', data); refresh_manifest('summary.json')
            for optimized in (False, True):
                command = [sys.executable] + (['-O'] if optimized else [])
                command += [str(package / 'probes/check_evidence.py'), '--source-root', str(source)]
                result = subprocess.run(command, capture_output=True, text=True, timeout=30)
                okay = result.returncode == 0 if expected_error is None else result.returncode == 1 and expected_error in result.stderr
                require(okay, f'Self-test failed: {name}, optimized={optimized}: {result.stdout} {result.stderr}')
                results.append({'case': name, 'optimized': optimized, 'expected': 'pass' if expected_error is None else 'reject',
                                'exit_code': result.returncode, 'passed': True})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=ROOT.parents[1])
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    try:
        verify(ROOT, args.source_root.resolve())
        if args.self_test:
            print(json.dumps(self_test(args.source_root.resolve()), indent=2))
        else:
            print('Recorded historical evidence verified (not a native rerun): 304 host tests, 32 selected native test executions, 8640 shaping rows, 1120 attached-host rows, 280 route checks and 40 transition rows.')
    except (InvalidEvidence, OSError, ValueError, KeyError, TypeError, AttributeError, ET.ParseError, EOFError) as error:
        print('Evidence validation failed: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
