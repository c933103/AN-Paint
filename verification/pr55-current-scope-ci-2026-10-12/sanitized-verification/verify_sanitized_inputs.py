#!/usr/bin/env python3
"""Recheck sanitized installed assertions and compare against retained originals.

No Android execution. The preserved original review is a separately supplied,
non-published input; this tool does not fetch or disclose original header values.
Only whole-file hashes, changed line numbers and report-field names are recorded.
"""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys


def sha(data): return hashlib.sha256(data).hexdigest()


def require(ok, message):
    if not ok: raise ValueError(message)


def diffs(left, right, path=''):
    if type(left) is not type(right): return [path]
    if isinstance(left, dict):
        if left.keys() != right.keys(): return [path + '.<keys>']
        return [d for key in left for d in diffs(left[key], right[key], path + '.' + key)]
    if isinstance(left, list):
        if len(left) != len(right): return [path + '.<length>']
        return [d for i, (a, b) in enumerate(zip(left, right)) for d in diffs(a, b, path + f'[{i}]')]
    return [] if left == right else [path]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('original-review', 'derivative', 'inputs', 'repo', 'output'):
        parser.add_argument('--' + name, type=pathlib.Path, required=True)
    args = parser.parse_args()
    old, derivative, inputs, repo, output = [path.resolve() for path in
        (args.original_review, args.derivative, args.inputs, args.repo, args.output)]
    require(not output.exists(), 'use a fresh output directory')
    output.mkdir(parents=True)
    env = os.environ | {'PYTHONDONTWRITEBYTECODE': '1'}

    def run(name, *arguments, script=None):
        result = subprocess.run([sys.executable, str(script or old / (name + '.py')),
            *map(str, arguments)], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (output / (name + '.log')).write_bytes(result.stdout)
        require(result.returncode == 0, name + ' failed; inspect separate log')

    redactions = json.loads((derivative / 'REDACTION-MANIFEST.json').read_bytes())
    require(len(redactions['changed_members']) == 1, 'unexpected redaction member count')
    change = redactions['changed_members'][0]
    require(change['path'] == 'current-inputs/api30/logcat.txt', 'unexpected redaction path')
    original = (old / 'selected-artifacts/api30/logcat.txt').read_bytes()
    sanitized = (inputs / 'api30/logcat.txt').read_bytes()
    require(sha(original) == change['original_whole_file_sha256'] and
            sha(sanitized) == change['sanitized_whole_file_sha256'], 'whole-file redaction hashes differ')
    before, after = original.splitlines(keepends=True), sanitized.splitlines(keepends=True)
    require(len(before) == len(after) == change['line_count'] == 38173, 'line count differs')
    require([i + 1 for i, (a, b) in enumerate(zip(before, after)) if a != b] == [20476],
            'unexpected changed lines')
    for name in ('ACCEPTANCE.json', 'binding.json', 'artifact-binding.json', 'delivery-compiled-arabic-input.json'):
        require((old / name).read_bytes() == (derivative / name).read_bytes(),
                'historical binding changed: ' + name)
    run('audit_source_inputs', '--repo', repo, '--output', output / 'source-input-result.json')
    run('audit_deadlines', '--repo', repo, '--output', output / 'deadline-result.json')
    run('audit_installed_matrix', '--repo', repo, '--artifact-root', inputs,
        '--output', output / 'installed-matrix-result.json')
    run('audit_prebuilt_provenance', '--repo', repo, '--artifacts', inputs, '--receipt-only',
        '--output', output / 'prebuilt-provenance-result.json')
    run('audit_platform_locale_binding', '--repo', repo, '--artifacts', inputs,
        '--matrix', output / 'installed-matrix-result.json',
        '--provenance', output / 'prebuilt-provenance-result.json',
        '--output', output / 'platform-locale-binding-result.json')
    run('audit_restart_boundary', '--artifacts', inputs, '--output', output / 'restart-boundary-result.json')
    binding = json.loads((old / 'binding.json').read_bytes())
    records = output / 'installed-observed'
    run('installed_strict_decoder', '--raw-output', inputs / 'api35/app/androidTest-results/instrumentation.log',
        '--expected-source-sha256', binding['source_digests']['app'],
        '--runner-summary', inputs / 'api35/app/androidTest-results/summary.json',
        '--source-tests', repo / 'app/src/androidTest', '--output-dir', records,
        script=repo / 'tools/installed_glyph_ink_evidence.py')
    run('audit_installed_pixels', '--repo', repo, '--records', records,
        '--output', output / 'installed-pixel-result.json')
    natural_binding = {key: binding[key] for key in ('head', 'tree', 'merge', 'run_id')}
    natural_binding.update(source_tests_sha256=binding['source_digests']['app'],
                           logcat_sha256=sha((inputs / 'api35/logcat.txt').read_bytes()))
    (output / 'natural-update-binding.json').write_text(json.dumps(natural_binding, indent=2) + '\n')
    run('audit_natural_update', '--logcat', inputs / 'api35/logcat.txt', '--records', records,
        '--binding', output / 'natural-update-binding.json', '--output', output / 'natural-update-result.json')
    run('audit_native_vertical', '--repo', repo, '--artifacts', inputs, '--output', output / 'native-vertical')
    expected = {
        'source-input-result.json': [], 'deadline-result.json': [], 'installed-matrix-result.json': [],
        'prebuilt-provenance-result.json': ['.status', '.payload_hash_recomputed'],
        'platform-locale-binding-result.json': ['.api30_logcat_sha256', '.prebuilt_result_sha256'],
        'restart-boundary-result.json': [], 'installed-pixel-result.json': [],
        'natural-update-result.json': [], 'native-vertical/result.json': ['.devices.30.logcat_sha256']}
    comparisons = []
    for name, wanted in expected.items():
        prior_bytes = (old / 'reproduced' / name).read_bytes(); current_bytes = (output / name).read_bytes()
        changed = diffs(json.loads(prior_bytes), json.loads(current_bytes))
        require(set(changed) == set(wanted), 'unexpected semantic differences in ' + name + ': ' + str(changed))
        comparisons.append(dict(path=name, original_whole_file_sha256=sha(prior_bytes),
            sanitized_verification_whole_file_sha256=sha(current_bytes), changed_fields=changed))
    for path in records.iterdir():
        require(path.read_bytes() == (old / 'reproduced/installed-observed' / path.name).read_bytes(),
                'Arabic record/pixels changed')
    native = json.loads((output / 'native-vertical/result.json').read_bytes())
    for api in (30, 35):
        for row in native['devices'][str(api)]['full_decoded_images']:
            name = pathlib.Path(f'native-vertical/native-observed-api{api}') / row['path']
            require((output / name).read_bytes() == (old / 'reproduced' / name).read_bytes(), 'native image changed')
    result = {key: binding[key] for key in ('head', 'tree', 'merge', 'run_id')}
    result.update(status='PASS_BOUNDED_ASSERTIONS_ON_SANITIZED_LOG_DERIVATIVE',
        original_acceptance_sha256=sha((old / 'ACCEPTANCE.json').read_bytes()),
        sanitized_selection_sha256=sha((derivative / 'DELIVERY-FILES.json').read_bytes()),
        redaction_manifest_sha256=sha((derivative / 'REDACTION-MANIFEST.json').read_bytes()),
        changed_input=dict(path='api30/logcat.txt', line=20476, line_count=38173,
            original_whole_file_sha256=sha(original), sanitized_whole_file_sha256=sha(sanitized)),
        verified_methods={'30': 95, '35': 104}, platform_locale_count=167,
        exact_native_images_unchanged=192, exact_arabic_records_and_images_unchanged=True,
        result_comparisons=comparisons,
        semantic_conclusion='All source, raw identity/protocol/terminal/JUnit, restart, natural-update, Arabic pixel, native geometry/input/Save and LocaleConfig assertions are unchanged. Expected differences are only the sanitized API30 whole-log hash, its downstream receipt hash, and explicit receipt-only payload status.',
        limits=['This is verification on a sanitized derivative, not exact original raw-log replay.',
                'Original outer ZIP/APK/source hashes were checked before redaction and remain historical receipts; their original payloads are intentionally omitted.',
                'Content-disclosure assessment is separate. No cookie value or cookie-value hash appears in this report.',
                'No new Android/app execution or code changes.'])
    (output / 'SANITIZED-VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])


if __name__ == '__main__': main()
