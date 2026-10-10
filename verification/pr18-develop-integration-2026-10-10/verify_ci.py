#!/usr/bin/env python3
"""Recheck downloaded PR18 CI bytes against the exact candidate source."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

SOURCE = Path(os.environ.get('ANPAINT_SOURCE_ROOT', Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(SOURCE / 'tools'))
from run_android_instrumentation import declared_tests, parse_protocol
from vertical_locale_matrix import app_partition, verify_app_reports, verify_screenshots


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def extract(archive, directory):
    directory.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, 'Corrupt ZIP member')
        for name in z.namelist():
            require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe ZIP path')
        z.extractall(directory)


def device(directory):
    from PIL import Image
    expected = declared_tests(SOURCE / 'app/src/androidTest', sdk_level=35)
    parts = app_partition(expected, 35)
    locations = {
        'ordinary': 'app/androidTest-results',
        'vertical': 'app-vertical/androidTest-results',
        'seed': 'app/accepted-credit-restart/seed',
        'verify': 'app/accepted-credit-restart/verify',
        'native': 'Paintroid/androidTest-results',
    }
    native = declared_tests(SOURCE / 'Paintroid/src/androidTest', sdk_level=35)
    expected_parts = dict(parts, native=native)
    reports = {}
    phase_results = {}
    for phase, relative in locations.items():
        path = directory / relative
        report = json.loads((path / 'summary.json').read_text())
        require(report['success'] is True and report['device_sdk'] == 35, f'{phase}: unsuccessful/wrong SDK')
        raw = parse_protocol((path / 'instrumentation.log').read_text(), expected_parts[phase],
                             returncode=report['returncode'], timed_out=report['timed_out'])
        for field in ('success', 'expected_tests', 'completed_tests', 'missing', 'unexpected', 'errors', 'cases'):
            require(raw[field] == report[field], f'{phase}: raw protocol differs: {field}')
        xml_files = list(path.glob('TEST-*.xml'))
        require(len(xml_files) == 1, f'{phase}: expected one XML suite')
        xml = ET.parse(xml_files[0]).getroot()
        require(int(xml.attrib['tests']) == len(expected_parts[phase]), f'{phase}: wrong XML total')
        require(not any(int(xml.attrib.get(k, 0)) for k in ('failures', 'errors', 'skipped')), f'{phase}: XML failure/skip')
        require({(c.attrib['classname'], c.attrib['name']) for c in xml.findall('testcase')} == expected_parts[phase],
                f'{phase}: wrong XML inventory')
        phase_results[phase] = {'tests': len(expected_parts[phase]), 'seconds': float(xml.attrib['time'])}
        if phase != 'native':
            reports[phase] = report
    coverage = verify_app_reports(expected, 35, reports)
    require(json.loads(json.dumps(coverage)) == json.loads((directory / 'app/coverage.json').read_text()),
            'Full app coverage receipt mismatch')
    require((directory / 'app/coverage.json').read_bytes() ==
            (directory / 'app/accepted-credit-restart/coverage.json').read_bytes(), 'Restart receipt mismatch')
    boundary = (directory / 'app/accepted-credit-restart/boundary.log').read_text()
    ordered_markers = ['Complete successful seed report verified; PID=', 'Gallery must still be the resumed activity',
                       'Force-stop verified live PID ', 'Verified target PID absent before normal verify instrumentation']
    positions = [boundary.find(marker) for marker in ordered_markers]
    require(all(p >= 0 for p in positions) and positions == sorted(positions), 'Restart sequence incomplete')
    require(re.search(r'topResumedActivity=.*MediaGalleryActivity', boundary), 'Gallery was not top resumed')
    seed_pid = str(reports['seed']['target_pid_before_instrumentation'])
    require(f'Complete successful seed report verified; PID={seed_pid}' in boundary and
            f'Force-stop verified live PID {seed_pid}' in boundary, 'Restart live PID mismatch')
    require('absent\nexit=0' in boundary, 'Missing explicit successful PID absence')
    screenshots = directory / 'app/vertical-locale-evidence'
    inventory = verify_screenshots(screenshots)
    require(inventory == json.loads((directory / 'vertical-locale-screenshots.json').read_text()), 'Screenshot receipt mismatch')
    decoded = {}
    for item in inventory['files']:
        with Image.open(screenshots / item['name']) as im:
            im.load()
            pixels = digest(im.convert('RGBA').tobytes())
            require(pixels not in decoded, f'Duplicate decoded screenshot: {item["name"]}')
            decoded[pixels] = item['name']
            item['decoded_rgba_sha256'] = pixels
    return {'phases': phase_results, 'coverage': coverage, 'screenshots': inventory,
            'restart_boundary': 'verified', 'visual_review': 'pending; decoding is not visual acceptance'}


def regression(directory):
    suites = list((directory / 'Paintroid/build/test-results').glob('**/TEST-*.xml'))
    require(bool(suites), 'Missing JVM XML')
    totals = dict(tests=0, failures=0, errors=0, skipped=0)
    for path in suites:
        root = ET.parse(path).getroot()
        for key in totals:
            totals[key] += int(root.attrib.get(key, 0))
        require(len(root.findall('testcase')) == int(root.attrib['tests']), 'JVM XML testcase mismatch')
    require(not any(totals[k] for k in ('failures', 'errors', 'skipped')), 'JVM failed/skipped tests')
    lint = list((directory / 'app/build/reports').glob('lint-results-*.xml'))
    require(len(lint) == 1, 'Expected one lint XML')
    issues = len(ET.parse(lint[0]).getroot().findall('issue'))
    require(issues == 0, 'Lint issues present')
    return {'jvm_suites': len(suites), 'jvm': totals, 'lint_issues': issues}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('kind', choices=('device', 'regression'))
    parser.add_argument('archive', type=Path)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    extract(args.archive, args.directory)
    result = {'archive_sha256': digest(args.archive.read_bytes()),
              'source_tree': '2ca29f84ce77e8d3be1aa2b7602fa6cca0ca6c31',
              'head': '66c6fd8411dd799c2d2ceb9250c1de500346f3f5',
              'run_id': 38067267565,
              'result': (device if args.kind == 'device' else regression)(args.directory)}
    output = args.directory.parent / (args.kind + '-receipt.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result if args.kind == 'regression' else
                     {k: v for k, v in result.items() if k != 'result'} | {'phases': result['result']['phases']}, indent=2))


if __name__ == '__main__':
    main()
