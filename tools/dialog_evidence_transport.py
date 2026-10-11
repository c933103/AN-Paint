#!/usr/bin/env python3
"""Verify exact API35 installed-dialog exports; partial failures remain diagnostics."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import zipfile

from vertical_evidence_transport import bounded_digest, require, strict_object

OWNER = 'paint.anpaint.android'
TEST_CLASS = OWNER + '.LocalizedDialogDeviceTest'
METHOD_SCREENS = {
    'aboutRowsOpenThreeNoticesWithReachableNativeFooters': [
        '0-about-portrait.png', '1-about-landscape.png',
        '2-notice-0-initial.png', '3-notice-0-portrait.png',
        '4-notice-1-initial.png', '5-notice-2-initial.png'],
    'retainedCreditDialogKeepsDraftSelectionAndNativeListenersAcrossRotation': [
        '0-credit-landscape.png', '1-credit-portrait.png'],
    'unchangedAdvancedColourReportsShortLandscapeLimitation': [
        '0-colour-limitation.png', '1-colour-cancelled.png'],
}
MAX_FILE = 2 * 1024 * 1024
MAX_CASE = 24 * 1024 * 1024
MAX_TOTAL = 3 * MAX_CASE
MAX_MANIFEST = 64 * 1024
PNG = b'\x89PNG\r\n\x1a\n'


def source_binding(summary):
    require(isinstance(summary, dict) and summary.get('success') is True
            and type(summary.get('device_sdk')) is int and summary.get('device_sdk') == 35 and summary.get('timed_out') is False
            and summary.get('returncode') == 0, 'Successful API35 dedicated dialog report required')
    digest = summary.get('source_tests_sha256')
    require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest),
            'Exact dialog test-source digest required')
    cases = summary.get('cases')
    require(isinstance(cases, list), 'Dialog report cases missing')
    relevant = [case for case in cases if case.get('classname') == TEST_CLASS]
    require(len(relevant) == len(METHOD_SCREENS)
            and {c.get('name') for c in relevant} == set(METHOD_SCREENS)
            and all(c.get('status') == 'passed' for c in relevant),
            'All three exact installed-dialog methods must pass in dedicated dialog report')
    require(len(cases) == 3 and summary.get('expected_tests') == 3
            and summary.get('completed_tests') == 3 and summary.get('missing') == []
            and summary.get('unexpected') == [] and summary.get('errors') == []
            and summary.get('included_tests') == sorted(TEST_CLASS + '#' + name for name in METHOD_SCREENS),
            'Exact selected three-method dialog phase required')
    return digest


def rectangle(value):
    require(isinstance(value, list) and len(value) == 4
            and all(type(v) is int for v in value), 'Malformed measured rectangle')
    require(value[2] >= value[0] and value[3] >= value[1], 'Negative rectangle size')
    return value


def contains(outer, inner):
    a, b = rectangle(outer), rectangle(inner)
    return a[0] <= b[0] < b[2] <= a[2] and a[1] <= b[1] < b[3] <= a[3]


def verify_receipt(receipt, method, digest):
    require(isinstance(receipt, dict) and type(receipt.get('schema')) is int and receipt.get('schema') == 1
            and receipt.get('test_class') == TEST_CLASS and receipt.get('test_method') == method
            and type(receipt.get('device_sdk')) is int and receipt.get('device_sdk') == 35 and receipt.get('package') == OWNER
            and receipt.get('outcome') == 'passed' and 'failure' not in receipt,
            'Incomplete or foreign dialog receipt')
    require(receipt.get('source_tests_sha256') == digest and
            receipt.get('source_binding') == 'runner-supplied-needs-host-comparison',
            'Dialog receipt is not bound to exact dialog-phase source')
    require(receipt.get('screenshots') == METHOD_SCREENS[method], 'Incomplete dialog screenshot inventory')
    observations = receipt.get('observations')
    require(isinstance(observations, list) and 0 < len(observations) <= 512,
            'Missing or excessive observations')
    require(all(isinstance(item, dict) for item in observations), 'Malformed observation')
    lines = [x for x in observations if x.get('kind') == 'caption-line-reached']
    require(lines, 'No measured caption reachability')
    for line in lines:
        require(contains(line['geometry']['visible'], line['line_rect']), 'Caption line is clipped')
    captions = [x for x in observations if x.get('kind') == 'intrinsic-caption']
    require(captions and all(type(c.get('lines')) is int and c['lines'] > 0
            and type(c.get('layout_height')) is int and c['layout_height'] > 0
            and type(c.get('available_text_height')) is int
            and c['layout_height'] <= c['available_text_height'] for c in captions),
            'Intrinsic caption clipping or missing metrics')
    for caption in captions:
        metrics = caption.get('line_metrics')
        require(isinstance(metrics, list) and len(metrics) == caption['lines']
                and type(caption.get('caption_length')) is int and caption['caption_length'] > 0
                and type(caption.get('layout_width')) is int and caption['layout_width'] > 0
                and metrics[-1].get('end') == caption['caption_length'], 'Missing caption line metrics')
        for metric in metrics:
            require(isinstance(metric, dict) and type(metric.get('ellipsis')) is int and metric['ellipsis'] == 0
                    and type(metric.get('left')) in (int, float) and type(metric.get('right')) in (int, float)
                    and -1 <= metric['left'] <= metric['right'] <= caption['layout_width'] + 1,
                    'Ellipsized or horizontally clipped caption')
    before = [x for x in observations if x.get('kind') == 'pointer-before']
    after = [x for x in observations if x.get('kind') == 'pointer-injected']
    require(before and len(before) == len(after) and [x.get('label') for x in before]
            == [x.get('label') for x in after], 'Incomplete pointer observation')
    for pointer in before:
        tap = pointer.get('tap')
        require(isinstance(tap, list) and len(tap) == 2 and all(type(v) is int for v in tap), 'Invalid pointer')
        bounds = rectangle(pointer['geometry']['visible'])
        require(bounds[0] <= tap[0] < bounds[2] and bounds[1] <= tap[1] < bounds[3], 'Pointer outside visible control')
    required = {
        list(METHOD_SCREENS)[0]: ['notice copy', 'other terms', 'notice done'],
        list(METHOD_SCREENS)[1]: ['credit save', 'credit copy', 'credit done'],
        list(METHOD_SCREENS)[2]: ['colour cancel'],
    }[method]
    require(set(required) <= {item.get('label') for item in before}, 'Required native footer actions absent')
    if method == 'unchangedAdvancedColourReportsShortLandscapeLimitation':
        verify_colour_limitation(receipt, observations)



def verify_colour_limitation(receipt, observations):
    classification = 'baseline-identical-source-limitation-characterization'
    require(receipt.get('case_classification') == classification
            and receipt.get('positive_viewport_accepted') is False
            and receipt.get('untouched_baseline_installed') == 'pending',
            'Colour characterization must not claim positive or baseline-device acceptance')
    measured = [o for o in observations if o.get('kind') == 'colour-limitation-characterization']
    cancelled = [o for o in observations if o.get('kind') == 'colour-limitation-cancelled']
    require(len(measured) == len(cancelled) == 1, 'Missing exact colour limitation/cancellation observations')
    state, end = measured[0], cancelled[0]
    require(state.get('classification') == classification and state.get('positive_viewport_accepted') is False
            and state.get('untouched_baseline_installed') == 'pending' and state.get('device_sdk') == 35
            and type(state.get('font_scale')) in (int, float) and state.get('font_scale') == 1,
            'Colour characterization scope changed')
    require(state['display']['width'] == 640 and state['display']['height'] == 320
            and rectangle(state['display']['raw']) == [0, 0, 640, 320], 'Colour display scope changed')
    for field in ('display', 'dialog', 'holder', 'holder_parent', 'inner', 'inner_content'):
        geometry = state[field]
        raw = rectangle(geometry['raw'])
        rectangle(geometry['visible'])
        require(type(geometry.get('width')) is int and type(geometry.get('height')) is int
                and geometry['width'] == raw[2] - raw[0] and geometry['height'] == raw[3] - raw[1]
                and type(geometry.get('measured_width')) is int and type(geometry.get('measured_height')) is int
                and 'layout_width' in geometry and 'layout_height' in geometry,
                'Missing or inconsistent colour geometry')
    require(state['holder']['width'] > 0 and state['holder']['height'] > 0
            and state['inner']['width'] > 0 and state['inner']['height'] == 0
            and state['inner_content']['height'] > 0, 'Expected zero-viewport limitation was not established')
    require(isinstance(state.get('fixed'), list) and len(state['fixed']) == 3
            and {g.get('tag') for g in state['fixed']} == {'colour_advanced_tab', 'custom_colours_panel', 'add_custom_colour'},
            'Fixed-control measurements missing')
    for geometry in state['fixed']:
        rectangle(geometry['raw']); rectangle(geometry['visible'])
    require(type(end.get('commit_callbacks')) is int and end.get('commit_callbacks') == 0
            and type(end.get('closed_callbacks')) is int and end.get('closed_callbacks') == 1
            and end.get('dialog_showing') is False and end.get('positive_viewport_accepted') is False
            and end.get('untouched_baseline_installed') == 'pending',
            'Native Cancel did not close exactly once without committing')


def inspect_archive(archive, method, digest):
    require(not archive.is_symlink() and archive.is_file(), 'Nonregular dialog ZIP')
    size = archive.stat().st_size
    require(0 < size <= MAX_CASE, 'Empty or oversized dialog ZIP')
    with archive.open('rb') as stream:
        archive_digest = bounded_digest(stream, size)
    expected = {'receipt.json', *METHOD_SCREENS[method]}
    with zipfile.ZipFile(archive) as zipped:
        members = zipped.infolist()
        names = [entry.filename for entry in members]
        require(len(names) == len(set(names)) and set(names) == expected | {'manifest.json'},
                'Incomplete, extra or unsafe dialog export members')
        for member in members:
            require(not member.is_dir() and stat.S_IFMT(member.external_attr >> 16) in (0, stat.S_IFREG)
                    and not member.flag_bits & 1 and member.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED),
                    'Nonregular or unsupported dialog ZIP member')
            require(0 < member.file_size <= (MAX_MANIFEST if member.filename == 'manifest.json' else MAX_FILE)
                    and 0 <= member.compress_size <= MAX_CASE, 'Oversized dialog ZIP member')
        require(sum(m.file_size for m in members) <= MAX_CASE, 'Oversized uncompressed dialog case')
        manifest = json.loads(zipped.read('manifest.json'), object_pairs_hook=strict_object)
        require(isinstance(manifest, dict) and set(manifest) == {'schema', 'owner', 'method', 'device_sdk', 'test_passed', 'files'}
                and type(manifest['schema']) is int and manifest['schema'] == 1 and manifest['owner'] == OWNER
                and manifest['method'] == method and type(manifest['device_sdk']) is int
                and manifest['device_sdk'] == 35 and manifest['test_passed'] is True,
                'Incomplete or foreign dialog manifest')
        entries = manifest['files']
        require(isinstance(entries, list) and len(entries) == len(expected), 'Missing file records')
        seen = set()
        for entry in entries:
            require(isinstance(entry, dict) and set(entry) == {'path', 'bytes', 'sha256'}, 'Malformed file record')
            name = entry['path']
            require(isinstance(name, str) and name in expected and name not in seen, 'Duplicate or unsafe record path')
            seen.add(name)
            require(type(entry['bytes']) is int and 0 < entry['bytes'] <= MAX_FILE
                    and entry['bytes'] == zipped.getinfo(name).file_size, 'File length mismatch')
            require(isinstance(entry['sha256'], str) and re.fullmatch('[0-9a-f]{64}', entry['sha256']), 'Malformed digest')
            with zipped.open(name) as stream:
                require(bounded_digest(stream, entry['bytes']) == entry['sha256'], 'File digest mismatch')
            if name.endswith('.png'):
                with zipped.open(name) as stream:
                    require(stream.read(8) == PNG, 'Non-PNG screenshot')
        require(seen == expected, 'Missing export records')
        verify_receipt(json.loads(zipped.read('receipt.json'), object_pairs_hook=strict_object), method, digest)
    return {'method': method, 'zip_bytes': size, 'zip_sha256': archive_digest, 'files': entries}


def extract(exports, destination, dialog_summary):
    digest = source_binding(json.loads(dialog_summary.read_text(), object_pairs_hook=strict_object))
    require(not exports.is_symlink() and exports.is_dir(), 'Missing dialog export directory')
    require({p.name for p in exports.iterdir()} == {m + '.zip' for m in METHOD_SCREENS}, 'Wrong dialog export inventory')
    require(not os.path.lexists(destination), 'Dialog destination must be fresh')
    receipts = [inspect_archive(exports / (method + '.zip'), method, digest) for method in METHOD_SCREENS]
    require(sum(e['bytes'] for r in receipts for e in r['files']) <= MAX_TOTAL, 'Combined dialog evidence oversized')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.dialog-evidence-', dir=destination.parent) as temporary:
        staged = Path(temporary) / 'evidence'
        staged.mkdir()
        for receipt in receipts:
            archive = exports / (receipt['method'] + '.zip')
            with archive.open('rb') as stream:
                require(bounded_digest(stream, receipt['zip_bytes']) == receipt['zip_sha256'], 'Dialog ZIP changed')
            folder = staged / receipt['method']
            folder.mkdir()
            with zipfile.ZipFile(archive) as zipped:
                for entry in receipt['files']:
                    with zipped.open(entry['path']) as source, (folder / entry['path']).open('xb') as output:
                        require(bounded_digest(source, entry['bytes'], output) == entry['sha256'], 'Dialog data changed')
        require(not os.path.lexists(destination), 'Destination appeared during validation')
        os.rename(staged, destination)
    return {'success': True, 'scope': 'installed-api35-dialog-behaviour-and-explicit-colour-limitation', 'source_tests_sha256': digest,
            'source_report': 'dedicated dialog instrumentation summary', 'device_sdk': 35,
            'cases': receipts, 'colour_case_classification': 'baseline-identical-source-limitation-characterization',
            'positive_colour_viewport_accepted': False, 'untouched_baseline_installed': 'pending',
            'large_text_short_landscape_advanced_colour': 'not-accepted-diagnostic-only'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exports', type=Path)
    parser.add_argument('--dialog-summary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    args.receipt.unlink(missing_ok=True)
    result = extract(args.exports, args.output, args.dialog_summary)
    args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'success': True, 'cases': len(result['cases']), 'device_sdk': 35}))


if __name__ == '__main__':
    main()
