#!/usr/bin/env python3
"""Run an already-built Android test APK with a deadline and fail-closed reports.

This deliberately does not invoke Gradle: emulator jobs test the exact APKs from
one build job. Android's instrumentation protocol, not adb's exit code alone,
determines success. Reports are written even after installation/runner failures.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

Identity = tuple[str, str]


def declared_tests(directory: Path) -> set[Identity]:
    expected: set[Identity] = set()
    for path in sorted(directory.rglob('*.kt')):
        source = path.read_text()
        package = re.search(r'^package\s+([\w.]+)', source, re.M)
        owner = re.search(r'^(?:(?:internal|public|open|abstract)\s+)*class\s+(\w+)', source, re.M)
        methods = re.findall(
            r'@Test\b(?:\([^)]*\))?\s*(?:@[\w.]+(?:\([^)]*\))?\s*)*'
            r'(?:(?:public|internal|suspend)\s+)*fun\s+(`[^`]+`|\w+)\s*\(', source)
        if len(methods) != len(re.findall(r'@Test\b', source)):
            raise ValueError(f'Unparsed @Test in {path}; update the test inventory parser')
        if methods and not (package and owner):
            raise ValueError(f'Cannot identify the test class in {path}')
        for method in methods:
            identity = (package.group(1) + '.' + owner.group(1), method.strip('`'))
            if identity in expected:
                raise ValueError(f'Duplicate declared test: {identity}')
            expected.add(identity)
    if not expected:
        raise ValueError(f'No declared test methods in {directory}')
    return expected


def parse_protocol(output: str, expected: set[Identity], *, returncode: int | None = 0,
                   timed_out: bool = False, run_errors: list[str] | None = None) -> dict:
    """Parse raw `am instrument -w -r` output, rejecting incomplete test runs."""
    cases: list[dict] = []
    errors = list(run_errors or [])
    fields: dict[str, str] = {}
    last_field = None
    started: set[Identity] = set()
    completed: set[Identity] = set()
    final_codes: list[int] = []
    declared_counts: set[int] = set()
    for line in output.splitlines():
        if line.startswith('INSTRUMENTATION_STATUS: '):
            key, separator, value = line[len('INSTRUMENTATION_STATUS: '):].partition('=')
            if separator:
                fields[key] = value
                last_field = key
        elif line.startswith('INSTRUMENTATION_STATUS_CODE: '):
            try:
                code = int(line.split(':', 1)[1])
            except ValueError:
                errors.append(f'Malformed status code: {line}')
                fields, last_field = {}, None
                continue
            identity = (fields.get('class', ''), fields.get('test', ''))
            if 'numtests' in fields:
                try:
                    declared_counts.add(int(fields['numtests']))
                except ValueError:
                    errors.append(f'Malformed numtests: {fields["numtests"]}')
            if code in (1, 0, -1, -2, -3, -4):
                if not all(identity):
                    errors.append(f'Test status {code} has no class/method: {fields}')
                elif code == 1:
                    if identity in started or identity in completed:
                        errors.append(f'Duplicate test start: {identity}')
                    started.add(identity)
                else:
                    if identity in completed:
                        errors.append(f'Duplicate test result: {identity}')
                    # Android reports @Ignore directly, without a start event.
                    if code not in (-3, -4) and identity not in started:
                        errors.append(f'Test ended without a start event: {identity}')
                    completed.add(identity)
                    status = {0: 'passed', -1: 'error', -2: 'failure',
                              -3: 'skipped', -4: 'skipped'}[code]
                    cases.append({'classname': identity[0], 'name': identity[1],
                                  'status': status,
                                  'message': fields.get('stack', fields.get('stream', '')).strip()})
            else:
                errors.append(f'Unknown instrumentation status {code}: {fields}')
            fields, last_field = {}, None
        elif line.startswith('INSTRUMENTATION_CODE: '):
            try:
                final_codes.append(int(line.split(':', 1)[1]))
            except ValueError:
                errors.append(f'Malformed final result: {line}')
            last_field = None
        elif line.startswith(('INSTRUMENTATION_FAILED:', 'INSTRUMENTATION_ABORTED:')):
            errors.append(line)
            last_field = None
        elif line.startswith('INSTRUMENTATION_RESULT: '):
            key, _, value = line[len('INSTRUMENTATION_RESULT: '):].partition('=')
            if key in ('shortMsg', 'longMsg'):
                errors.append(f'Runner {key}: {value}')
            last_field = None
        elif last_field is not None:
            # Stack traces and stream fields span several protocol lines.
            fields[last_field] += '\n' + line

    if timed_out:
        errors.append('Instrumentation exceeded its deadline')
    if returncode != 0:
        errors.append(f'adb exited with status {returncode}')
    if final_codes != [-1]:
        errors.append(f'Missing or unsuccessful final instrumentation result: {final_codes}')
    if fields:
        errors.append('Truncated instrumentation status bundle')
    if not completed:
        errors.append('No tests completed')
    if not expected:
        errors.append('Expected test inventory is empty')
    if declared_counts != {len(expected)}:
        errors.append(f'Runner test counts {sorted(declared_counts)} do not match {len(expected)} declared methods')
    missing, unexpected = expected - completed, completed - expected
    if missing:
        errors.append(f'{len(missing)} declared test method(s) did not complete')
        for owner, name in sorted(missing):
            cases.append({'classname': owner, 'name': name, 'status': 'error',
                          'message': 'Test started but did not finish' if (owner, name) in started
                                     else 'Declared test was not executed'})
    if unexpected:
        errors.append(f'Unexpected tests: {sorted(unexpected)}')
    failed = [case for case in cases if case['status'] != 'passed']
    return {'success': not errors and not failed, 'expected_tests': len(expected),
            'completed_tests': len(completed), 'missing': sorted(missing),
            'unexpected': sorted(unexpected), 'errors': errors, 'cases': cases,
            'returncode': returncode, 'timed_out': timed_out}


def write_reports(output: Path, suite: str, result: dict, elapsed: float) -> None:
    cases = list(result['cases'])
    if result['errors']:
        cases.append({'classname': suite, 'name': '__instrumentation_run__',
                      'status': 'error', 'message': '\n'.join(result['errors'])})
    root = ET.Element('testsuite', name=suite, tests=str(len(cases)),
                      failures=str(sum(c['status'] == 'failure' for c in cases)),
                      errors=str(sum(c['status'] == 'error' for c in cases)),
                      skipped=str(sum(c['status'] == 'skipped' for c in cases)),
                      time=f'{elapsed:.3f}')
    for case in cases:
        node = ET.SubElement(root, 'testcase', classname=case['classname'], name=case['name'])
        if case['status'] != 'passed':
            child = ET.SubElement(node, case['status'], message=case['message'].split('\n')[0])
            child.text = case['message']
    # Android logs can contain control bytes not legal in XML 1.0.
    for element in root.iter():
        for key, value in element.attrib.items():
            element.set(key, re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', value))
        if element.text:
            element.text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', element.text)
    ET.indent(root)
    safe_suite = re.sub(r'[^\w.-]', '_', suite)
    ET.ElementTree(root).write(output / f'TEST-{safe_suite}.xml', encoding='utf-8', xml_declaration=True)
    (output / 'summary.json').write_text(json.dumps({**result, 'elapsed_seconds': elapsed}, indent=2) + '\n')


def capture_live(command: list[str], log: Path, deadline_seconds: int) -> tuple[int, bool]:
    """Drain output continuously while enforcing the wall-clock deadline."""
    timed_out = False
    deadline = time.monotonic() + deadline_seconds
    with log.open('wb') as saved:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                while selector.get_map():
                    if time.monotonic() >= deadline:
                        timed_out = True
                        process.kill()
                        break
                    for key, _ in selector.select(timeout=min(0.25, max(0, deadline - time.monotonic()))):
                        data = os.read(key.fileobj.fileno(), 65536)
                        if not data:
                            selector.unregister(key.fileobj)
                        else:
                            saved.write(data)
                            saved.flush()
                            print(data.decode('utf-8', errors='replace'), end='', flush=True)
                remaining = max(0.01, deadline - time.monotonic())
                try:
                    process.wait(timeout=remaining)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    process.kill()
                # Kill closes adb's pipe; preserve any last buffered result lines.
                tail, _ = process.communicate(timeout=5)
                if tail:
                    saved.write(tail)
                    print(tail.decode('utf-8', errors='replace'), end='', flush=True)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
    return process.returncode, timed_out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', default='adb')
    parser.add_argument('--apk', type=Path, required=True, help='Already-built instrumentation test APK')
    parser.add_argument('--source-tests', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--suite', required=True)
    parser.add_argument('--component', help='test.package/androidx.test.runner.AndroidJUnitRunner')
    parser.add_argument('--exclude-class', action='append', default=[])
    parser.add_argument('--timeout-seconds', type=int, default=480)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    log = args.output / 'instrumentation.log'
    log.write_text('')
    started = time.monotonic()
    expected: set[Identity] = set()
    errors: list[str] = []
    returncode, timed_out = None, False
    component, target = args.component, None
    try:
        if args.timeout_seconds <= 0:
            raise ValueError('--timeout-seconds must be positive')
        expected = declared_tests(args.source_tests)
        unknown_exclusions = set(args.exclude_class) - {owner for owner, _ in expected}
        if unknown_exclusions:
            raise ValueError(f'Excluded class not found in source inventory: {sorted(unknown_exclusions)}')
        expected = {item for item in expected if item[0] not in args.exclude_class}
        if not expected:
            raise ValueError('Exclusions removed every declared test')
        if not args.apk.is_file():
            raise ValueError(f'Test APK not found: {args.apk}')
        installed = subprocess.run([args.adb, 'install', '-r', '-t', str(args.apk)],
                                   capture_output=True, text=True, timeout=60)
        (args.output / 'install.log').write_text(installed.stdout + installed.stderr)
        if installed.returncode or not re.search(r'^Success\s*$', installed.stdout, re.M):
            raise RuntimeError(f'Test APK installation failed: {installed.stdout}{installed.stderr}')
        instrumentation = subprocess.run([args.adb, 'shell', 'pm', 'list', 'instrumentation'],
                                         capture_output=True, text=True, timeout=15, check=True)
        available = dict(re.findall(r'^instrumentation:(\S+)\s+\(target=([^)]*)\)', instrumentation.stdout, re.M))
        if component is None:
            if len(available) != 1:
                raise ValueError(f'Pass --component; installed instrumentation is ambiguous: {sorted(available)}')
            component = next(iter(available))
        if component not in available:
            raise ValueError(f'Instrumentation {component} was not installed; found {sorted(available)}')
        target = available[component]
        command = [args.adb, 'shell', 'am', 'instrument', '-w', '-r']
        if args.exclude_class:
            command += ['-e', 'notClass', ','.join(args.exclude_class)]
        command.append(component)
        returncode, timed_out = capture_live(command, log, args.timeout_seconds)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        errors.append(str(error))
    finally:
        if timed_out and target:
            try:
                subprocess.run([args.adb, 'shell', 'am', 'force-stop', target],
                               capture_output=True, timeout=10)
            except (OSError, subprocess.SubprocessError):
                pass  # Emulator job cleanup still terminates the device.
        result = parse_protocol(log.read_text(errors='replace'), expected, returncode=returncode,
                                timed_out=timed_out, run_errors=errors)
        result['component'] = component
        result['excluded_classes'] = args.exclude_class
        write_reports(args.output, args.suite, result, time.monotonic() - started)
    print(json.dumps({key: result[key] for key in ('success', 'expected_tests', 'completed_tests', 'errors')}, indent=2))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
