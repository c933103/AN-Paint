#!/usr/bin/env python3
"""Reuse only byte-identical, previously viewed images after fresh diagnostics.

This does not inspect changed images. It emits their exact paths for separate
viewing. No Android execution, source edits, or prior-review writes are performed.
"""
import argparse
import hashlib
import json
import pathlib

from audit_natural_artifacts import HEAD, TREE, MERGE, RUN, require


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def audit(prior, current):
    manifest = read(prior / 'DELIVERY-FILES.json')
    pins = {row['path']: row for row in manifest['files']}

    def frozen(name):
        data = (prior / name).read_bytes()
        pin = pins[name]
        require(len(data) == pin['bytes'] and sha(data) == pin['sha256'],
                'prior frozen visual receipt differs: ' + name)
        return json.loads(data)

    accepted = frozen('ACCEPTANCE.json')
    require(accepted['head'] == 'e19c766eb3eaedc1b3cd3657bb92864f81a9498a'
            and accepted['tree'] == 'dc1ba97dacc573ead73729297eb739ecb244dcf5'
            and accepted['status'] == 'PASS_BOUNDED_INSTALLED_SCOPE_AND_PLATFORM_DISCOVERY',
            'prior visual review binding differs')
    fresh = read(current / 'result.json')
    require(fresh['audit_integrity_status'] == 'PASS'
            and fresh['installed_gate_status'] == 'PASS'
            and fresh['native_vertical_status'] == 'PASS_BOUNDED_NATIVE_VERTICAL'
            and fresh['platform_locale_discovery_status'] == 'PASS_BOUND_INSTALLED_PLATFORM_LOCALE_DISCOVERY',
            'fresh installed diagnostic gates must pass first')
    native = read(current / 'native-vertical/result.json')
    pixels = read(current / 'installed-pixel-result.json')
    require(native['head'] == pixels['head'] == HEAD
            and native['tree'] == pixels['tree'] == TREE
            and native['merge'] == pixels['merge'] == MERGE
            and str(native['run_id']) == str(pixels['run_id']) == RUN
            and pixels['status'] == 'PASS', 'fresh visual diagnostics binding differs')
    rows = []
    receipt_pins = []
    for api in (30, 35):
        name = f'api{api}-visual-inspection.json'
        receipt = frozen(name)
        require(receipt['status'] == 'ACTUALLY_INSPECTED_BOUNDED_NATIVE_FRAMES'
                and receipt['api'] == api and receipt['original_png_count'] == 96,
                'prior native visual endorsement differs')
        prior_images = [image for sheet in receipt['sheets'] for image in sheet['source_images']]
        original = {row['path']: row['sha256'] for row in prior_images}
        require(len(original) == len(prior_images) == 96, 'prior PNG identity inventory differs')
        new = {row['path']: row for row in native['devices'][str(api)]['full_decoded_images']}
        require(set(new) == set(original), 'fresh native image inventory differs')
        for path in sorted(new):
            old_path = prior / f'reproduced/native-vertical/native-observed-api{api}' / path
            new_path = current / f'native-vertical/native-observed-api{api}' / path
            old_bytes, new_bytes = old_path.read_bytes(), new_path.read_bytes()
            require(sha(old_bytes) == original[path], 'prior PNG differs from actually viewed input')
            require(sha(new_bytes) == new[path]['sha256'], 'fresh PNG differs from diagnostic input')
            equal = old_bytes == new_bytes
            rows.append({'kind': 'native', 'api': api, 'path': path,
                         'prior_sha256': sha(old_bytes), 'current_sha256': sha(new_bytes),
                         'exact_image_bytes_equal': equal,
                         'visual_status': 'REUSE_PREVIOUS_VIEW_BY_BYTE_EQUALITY' if equal else 'FRESH_VISUAL_INSPECTION_REQUIRED'})
        receipt_pins.append({'path': name, 'sha256': pins[name]['sha256']})
    name = 'arabic-visual-inputs.json'
    arabic = frozen(name)
    require(arabic['status'] == 'ACTUALLY_VIEWED_FOUR_ORIGINAL_RGBA_INPUTS'
            and len(arabic['images']) == 4, 'prior Arabic visual endorsement differs')
    new_images = {f"{route['route']}-{kind}.png": row['sha256']
                  for route in pixels['routes'] for kind, row in route['png'].items()}
    require(set(new_images) == {pathlib.PurePosixPath(row['path']).name for row in arabic['images']},
            'fresh Arabic image inventory differs')
    for image in arabic['images']:
        path = pathlib.PurePosixPath(image['path']).name
        old_bytes = (prior / image['path']).read_bytes()
        new_bytes = (current / 'installed-observed' / path).read_bytes()
        require(sha(old_bytes) == image['sha256'], 'prior viewed Arabic PNG differs')
        require(sha(new_bytes) == new_images[path], 'fresh Arabic diagnostic PNG differs')
        equal = old_bytes == new_bytes
        rows.append({'kind': 'arabic', 'api': 35, 'path': path,
                     'prior_sha256': sha(old_bytes), 'current_sha256': sha(new_bytes),
                     'exact_image_bytes_equal': equal,
                     'visual_status': 'REUSE_PREVIOUS_VIEW_BY_BYTE_EQUALITY' if equal else 'FRESH_VISUAL_INSPECTION_REQUIRED'})
    receipt_pins.append({'path': name, 'sha256': pins[name]['sha256']})
    require(len(rows) == 196, 'total fresh image inventory differs')
    changed = [row for row in rows if not row['exact_image_bytes_equal']]
    return {'status': 'PASS_EXACT_IMAGE_BYTE_CONTINUITY' if not changed else 'CHANGED_IMAGES_NEED_VISUAL_REVIEW',
            'head': HEAD, 'tree': TREE, 'merge': MERGE, 'run_id': int(RUN),
            'prior_head': accepted['head'], 'prior_tree': accepted['tree'], 'prior_run_id': accepted['run_id'],
            'prior_manifest_sha256': sha((prior / 'DELIVERY-FILES.json').read_bytes()),
            'prior_visual_receipts': receipt_pins,
            'fresh_diagnostic_results': [{'path': name, 'sha256': sha((current / name).read_bytes())}
                for name in ('result.json', 'native-vertical/result.json', 'installed-pixel-result.json',
                             'natural-update-result.json', 'platform-locale-binding-result.json')],
            'total_images': len(rows), 'exactly_identical_images': len(rows) - len(changed),
            'changed_images': len(changed), 'images': rows,
            'limits': ['Only prior visual conclusions for exact image-byte matches are reused.',
                       'Fresh source, protocol, transport, geometry/input, natural-update, pixel and installation diagnostics remain required.',
                       'Changed images require fresh explicit visual inspection; this program does not perform viewing.',
                       'No physical-device, live network, fluent-language, Android Settings visibility or translation-completeness acceptance.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('prior', 'current', 'output'):
        parser.add_argument('--' + key, type=pathlib.Path, required=True)
    args = parser.parse_args()
    result = audit(args.prior, args.current)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ('status', 'total_images', 'exactly_identical_images', 'changed_images')}, indent=2))
