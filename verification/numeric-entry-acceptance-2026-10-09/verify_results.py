#!/usr/bin/env python3
"""Verify retained PR27 result files, XML totals and installed runner inventories."""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(name):
    return json.loads((ROOT / name).read_text())


def archive(name, manifest_name):
    entries = read_json(manifest_name)
    require(len({e['path'] for e in entries}) == len(entries), 'Duplicate manifest path')
    result = {}
    with zipfile.ZipFile(ROOT / name) as z:
        require(len(z.namelist()) == len(set(z.namelist())), 'Duplicate ZIP path')
        require(set(z.namelist()) == {e['path'] for e in entries}, 'Archive/manifest inventory mismatch')
        for entry in entries:
            data = z.read(entry['path'])
            require(len(data) == entry['bytes'], 'Entry byte count mismatch')
            require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'Entry hash mismatch')
            result[entry['path']] = data
    return result


def main():
    record = read_json('acceptance.json')
    require(record['head_tree'] == record['ci_tested_tree'], 'Different tested tree')
    for entry in record['files']:
        require(Path(entry['path']).name == entry['path'], 'File must be local to bundle')
        data = (ROOT / entry['path']).read_bytes()
        require(len(data) == entry['bytes'], 'File byte count mismatch')
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'File SHA-256 mismatch')
        require(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == entry['git_blob'], 'Git blob mismatch')
    units = archive('unit-and-lint-xml.zip', 'unit-and-lint-manifest.json')
    total = dict(tests=0, failures=0, errors=0, skipped=0)
    lint = 0
    for name, data in units.items():
        root = ET.fromstring(data)
        if name.endswith('lint-results-debug.xml'):
            lint += len(root.findall('issue'))
            continue
        cases = root.findall('testcase')
        require(len(cases) == int(root.get('tests', 0)), 'Suite count mismatch')
        require(not any(c.find(tag) is not None for c in cases for tag in ('failure', 'error', 'skipped')), 'Unsuccessful unit case')
        for key in total:
            total[key] += int(root.get(key, 0))
    require(total == record['jvm'], 'JUnit totals mismatch')
    require(lint == record['lint_issues'] == 0, 'Lint mismatch')
    device = archive('device-results.zip', 'device-manifest.json')
    summaries = read_json('all-device-cases.json')['summaries']
    require({x['path'] for x in summaries} == {n for n in device if n.endswith('summary.json')}, 'Device summary inventory mismatch')
    device_total = 0
    for entry in summaries:
        data = json.loads(device[entry['path']])
        require(data == entry['summary'], 'Device summary changed')
        cases = data['cases']
        require(data['success'] and not data['missing'] and not data['unexpected'] and not data['errors'], 'Device result unsuccessful')
        require(len(cases) == data['expected_tests'] == data['completed_tests'], 'Device count mismatch')
        require(len({(x['classname'], x['name']) for x in cases}) == len(cases), 'Duplicate device case')
        require(all(x['status'] == 'passed' for x in cases), 'Unsuccessful device case')
        device_total += len(cases)
    require(device_total == record['api35']['tests'], 'Installed total mismatch')
    print(json.dumps({'jvm': total, 'lint_issues': lint, 'api35_cases': device_total, 'result': 'passed'}, sort_keys=True))


if __name__ == '__main__':
    main()
