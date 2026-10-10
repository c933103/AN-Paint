#!/usr/bin/env python3
"""Fail-closed receipts for native vertical Save reachability; not pixel review."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
from vertical_locale_matrix import LOCALES, ORIENTATIONS

STATES = ('before', 'minimum', 'maximum', 'filename', 'description', 'cancel-ready', 'choose-ready', 'returned')
CASES = {f'{locale}-{orientation}' for locale in LOCALES for orientation in ORIENTATIONS}
LABELS = {'quality label and readout', 'complete quality control', 'filename field',
          'filename preview', 'JPEG explanation', 'Cancel action', 'Choose location action'}


def contains(outer, inner):
    if (not isinstance(outer, list) or not isinstance(inner, list) or len(outer) != 4 or len(inner) != 4
            or any(type(v) is not int for v in outer+inner)):
        return False
    l,t,r,b = outer; il,it,ir,ib = inner
    return l <= il < ir <= r and t <= it < ib <= b


def complete(geometry):
    return (isinstance(geometry, dict) and geometry.get('fully_visible') is True
            and contains(geometry.get('visible'), geometry.get('raw')))


def verify(directory: Path, sdk: int | None = None) -> dict:
    expected = {f'{case}-{state}.png' for case in CASES for state in STATES} | {f'{case}.json' for case in CASES}
    actual = {p.name for p in directory.iterdir()} if directory.is_dir() else set()
    if actual != expected:
        raise ValueError(f'Reachability inventory mismatch: missing={sorted(expected-actual)}, unexpected={sorted(actual-expected)}')
    files=[]; result=[]
    for case in sorted(CASES):
        path=directory/f'{case}.json'; receipt=json.loads(path.read_text())
        confirmed=100 if case.endswith('-landscape') else 1
        if (receipt.get('case') != case or receipt.get('success') is not True or 'failure' in receipt
                or type(receipt.get('device_sdk')) is not int or receipt['device_sdk'] not in (30,35)
                or receipt.get('endpoint_values') != [1,100]
                or receipt.get('cancel_preserved_quality') is not True
                or type(receipt.get('remembered_quality_before_cancel')) is not int
                or not 1 <= receipt['remembered_quality_before_cancel'] <= 100
                or type(receipt.get('cancel_draft_quality')) is not int
                or not 1 <= receipt['cancel_draft_quality'] <= 100
                or receipt['cancel_draft_quality'] == receipt['remembered_quality_before_cancel']
                or receipt.get('canvas_and_document_preserved') is not True
                or type(receipt.get('confirmed_quality')) is not int or receipt['confirmed_quality'] != confirmed
                or type(receipt.get('destination_requests')) is not int or receipt['destination_requests'] != 1
                or receipt.get('destination_action') != 'android.intent.action.CREATE_DOCUMENT'
                or receipt.get('destination_mime') != 'image/jpeg'
                or not isinstance(receipt.get('filename'),str) or not receipt['filename'].endswith('.jpg')
                or receipt.get('destination_filename') != receipt['filename']
                or set(receipt.get('screenshots',[])) != {f'{case}-{s}.png' for s in STATES}
                or len(receipt['screenshots']) != len(STATES)):
            raise ValueError(f'Incomplete successful native-flow receipt: {case}')
        observations=receipt.get('observations',[])
        reached=[o for o in observations if o.get('kind')=='reachable']
        if not LABELS <= {o.get('label') for o in reached} or any(not complete(o.get('geometry')) for o in reached):
            raise ValueError(f'Complete control/label bounds not proved: {case}')
        endpoints=[o for o in observations if o.get('kind')=='endpoint']
        if not {1,100} <= {o.get('value') for o in endpoints}:
            raise ValueError(f'Both native quality endpoints not proved: {case}')
        for e in endpoints:
            if (e.get('value') not in (1,100) or type(e.get('before')) is not int
                    or not 1 <= e['before'] <= 100 or e['before']==e['value']
                    or not complete(e.get('geometry')) or not complete(e.get('seekbar'))
                    or not contains(e['seekbar']['visible'],e.get('thumb'))):
                raise ValueError(f'Endpoint input/effect/full-thumb bounds not proved: {case}')
            for key in ('from','to'):
                p=e.get(key,[])
                if (not isinstance(p,list) or len(p)!=2 or any(type(v) is not int for v in p)
                        or not contains(e['seekbar']['visible'],[p[0],p[1],p[0]+1,p[1]+1])):
                    raise ValueError(f'Native endpoint touch outside visible control: {case}')
        captures={o.get('state'):o for o in observations if o.get('kind')=='capture'}
        if set(captures) != set(STATES)-{'returned'}:
            raise ValueError(f'Missing capture-time state observations: {case}')
        if captures['cancel-ready'].get('quality') != receipt['cancel_draft_quality']:
            raise ValueError(f'Cancel screenshot does not show the distinct draft quality: {case}')
        if any(o.get('filename') != receipt['filename'] for o in captures.values()):
            raise ValueError(f'Draft filename lost: {case}')
        for state,value in (('minimum',1),('maximum',100)):
            c=captures[state]
            if (c.get('quality')!=value or not complete(c.get('geometry')) or not complete(c.get('seekbar'))
                    or not complete(c.get('readout')) or not contains(c['seekbar']['visible'],c.get('thumb'))):
                raise ValueError(f'Endpoint capture not complete: {case}/{state}')
        before=[o for o in observations if o.get('kind')=='scroll-before']
        after=[o for o in observations if o.get('kind')=='scroll-after']
        if (type(receipt.get('native_scroll_gestures')) is not int or receipt['native_scroll_gestures']<1
                or receipt['native_scroll_gestures']!=len(before) or len(before)!=len(after)
                or not any(b.get('geometry')!=a.get('geometry') for b,a in zip(before,after))):
            raise ValueError(f'Native scroll motion not proved: {case}')
        hashes={}
        for state in STATES:
            name=f'{case}-{state}.png'; data=(directory/name).read_bytes()
            if (len(data)<33 or data[:16]!=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'):
                raise ValueError(f'Invalid PNG header: {name}')
            w,h=struct.unpack('>II',data[16:24])
            if not w or not h or (w>h)!=case.endswith('-landscape'):
                raise ValueError(f'Unexpected screenshot orientation: {name}')
            hashes[state]=hashlib.sha256(data).hexdigest()
            files.append(dict(name=name,bytes=len(data),width=w,height=h,sha256=hashes[state]))
        if hashes['minimum']==hashes['maximum']:
            raise ValueError(f'Identical minimum/maximum captures: {case}')
        files.append(dict(name=path.name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        result.append(dict(case=case,device_sdk=receipt['device_sdk'],confirmed_quality=confirmed))
    if len({c['device_sdk'] for c in result}) != 1 or (sdk is not None and any(c['device_sdk'] != sdk for c in result)):
        raise ValueError('Reachability cases disagree on requested device SDK')
    return dict(success=True,cases=result,screenshots=len(CASES)*len(STATES),files=files,
                scope='Native input/state/bounds receipts. Every actual PNG still requires independent visual review.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--sdk',type=int,choices=(30,35),required=True)
    args=parser.parse_args();result=verify(args.directory,args.sdk)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(success=True,cases=len(result['cases']),screenshots=result['screenshots'])))


if __name__=='__main__': main()
