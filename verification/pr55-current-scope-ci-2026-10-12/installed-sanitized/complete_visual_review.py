#!/usr/bin/env python3
"""Check every image is covered by exact-byte reuse or an explicit fresh review.

The review receipts record human-readable observations after actual viewing.
This verifies their identities and coverage; it does not itself inspect images.
"""
import argparse
import hashlib
import json
import pathlib

from audit_natural_artifacts import HEAD, TREE, MERGE, RUN, require


def sha(data): return hashlib.sha256(data).hexdigest()


def audit(root):
    path = root / 'visual-continuity-result.json'
    continuity = json.loads(path.read_bytes())
    common = dict(head=HEAD, tree=TREE, merge=MERGE, run_id=int(RUN))
    require(all(continuity[k] == v for k, v in common.items()), 'continuity run/source differs')
    require(continuity['total_images'] == len(continuity['images']) == 196,
            'continuity image inventory differs')
    review_pins, images, viewed = [], [], {}
    for api in (30, 35):
        path = root / f'api{api}-visual-inspection.json'
        if not path.exists(): continue
        raw = path.read_bytes(); receipt = json.loads(raw)
        require(all(receipt[k] == v for k, v in common.items()) and receipt['api'] == api,
                'fresh visual receipt source/run/API differs')
        require(receipt['status'] == 'ACTUALLY_INSPECTED_BOUNDED_NATIVE_FRAMES'
                and receipt['original_png_count'] == 96, 'fresh visual status/count differs')
        rows = [r for sheet in receipt['sheets'] for r in sheet['source_images']]
        require(len(rows) == len({r['path'] for r in rows}) == 96, 'duplicate/missing reviewed image')
        viewed[api] = {r['path']: r['sha256'] for r in rows}
        review_pins.append(dict(path=path.name, sha256=sha(raw)))
    for row in continuity['images']:
        result = dict(row)
        if row['exact_image_bytes_equal']:
            require(row['prior_sha256'] == row['current_sha256'], 'false identical byte claim')
            result['final_visual_status'] = 'REUSED_PREVIOUS_VIEW_BY_EXACT_IMAGE_BYTE_EQUALITY'
        else:
            require(row['kind'] == 'native' and
                    viewed.get(row['api'], {}).get(row['path']) == row['current_sha256'],
                    'changed image lacks exact fresh visual endorsement')
            result['final_visual_status'] = 'FRESHLY_INSPECTED_CHANGED_IMAGE'
        images.append(result)
    return common | dict(status='PASS_BOUNDED_VISUAL_REVIEW_WITH_EXPLICIT_REUSE',
        exact_image_byte_reuse=sum(r['exact_image_bytes_equal'] for r in images),
        freshly_inspected_changed_images=sum(not r['exact_image_bytes_equal'] for r in images),
        continuity_sha256=sha((root / 'visual-continuity-result.json').read_bytes()),
        prior_evidence_commit='f066e90b8fc7682023e0bf260da55959e6ebf9e5',
        fresh_visual_receipts=review_pins, images=images,
        limits='Coverage validation of explicit reviewer observations and exact image-byte reuse only. Fresh protocol, pixel, geometry/input and source/install checks are independently required. Not fluent-language, hardware, release, network or universal viewport acceptance.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args(); result = audit(args.review)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], result['exact_image_byte_reuse'], 'reused;', result['freshly_inspected_changed_images'], 'freshly viewed')
