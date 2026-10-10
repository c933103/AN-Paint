#!/usr/bin/env python3
"""Validate exact-source PR41 CI artifacts; image decoding is not visual acceptance."""
import argparse
import collections
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

HEAD = '2e512e0c7817cd66a3ec54ca567fc154ea6c83b2'
TREE = 'fd9ccb67bba4d053eda1d939738b7af3b7c77ccb'
TESTED_MERGE = '76507261adbbf44162f724c3a2abb10ed15eb00a'
RUN_ID = 38069153905


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_extract(archive, directory):
    directory.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, 'Corrupt ZIP member')
        require(len(z.namelist()) == len(set(z.namelist())), 'Duplicate archive member')
        for name in z.namelist():
            require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe ZIP path')
        z.extractall(directory)


def device(directory, source):
    from PIL import Image
    from run_android_instrumentation import declared_tests, parse_protocol, source_tests_sha256
    from vertical_locale_matrix import app_partition, verify_app_reports, verify_screenshots, report_paths, read_app_reports
    from vertical_control_reachability import verify as verify_reachability
    app_source = source / 'app/src/androidTest'
    expected = declared_tests(app_source, sdk_level=35)
    parts = app_partition(expected, 35)
    locations = {phase: path.parent for phase, path in report_paths(directory, 35).items()}
    locations['native'] = directory / 'Paintroid/androidTest-results'
    bound_reports = read_app_reports(directory, 35)
    native_source = source / 'Paintroid/src/androidTest'
    native = declared_tests(native_source, sdk_level=35)
    expected_parts = dict(parts, native=native)
    require(len(expected) == 24 and len(native) == 74, 'Unexpected current source method totals')
    reports, phase_results = {}, {}
    for phase, path in locations.items():
        report = json.loads((path / 'summary.json').read_text())
        source_digest = source_tests_sha256(native_source if phase == 'native' else app_source)
        require(report['success'] is True and report['device_sdk'] == 35, f'{phase}: unsuccessful/wrong SDK')
        require(report['source_tests_sha256'] == source_digest, f'{phase}: source digest differs')
        require(report['returncode'] == 0 and report['timed_out'] is False, f'{phase}: process failed/timed out')
        require(report['timeout_seconds'] == (60 if phase in ('seed', 'verify') else 180), f'{phase}: changed budget')
        raw = parse_protocol((path / 'instrumentation.log').read_text(), expected_parts[phase],
                             returncode=report['returncode'], timed_out=report['timed_out'])
        for field in ('success', 'expected_tests', 'completed_tests', 'missing', 'unexpected', 'errors', 'cases'):
            require(raw[field] == report[field], f'{phase}: raw protocol differs: {field}')
        xml_files = list(path.glob('TEST-*.xml'))
        require(len(xml_files) == 1, f'{phase}: expected one XML suite')
        xml = ET.parse(xml_files[0]).getroot()
        require(int(xml.attrib['tests']) == len(expected_parts[phase]), f'{phase}: wrong XML total')
        require(not any(int(xml.attrib.get(k, 0)) for k in ('failures', 'errors', 'skipped')), f'{phase}: XML failure/skip')
        cases = [(c.attrib['classname'], c.attrib['name']) for c in xml.findall('testcase')]
        require(len(cases) == len(set(cases)) and set(cases) == expected_parts[phase], f'{phase}: wrong XML inventory')
        phase_results[phase] = {'tests': len(expected_parts[phase]), 'seconds': float(xml.attrib['time'])}
        if phase != 'native':
            require(report == bound_reports[phase], f'{phase}: report binding mismatch')
            reports[phase] = report
    coverage = verify_app_reports(expected, 35, reports, source_tests_sha256(app_source))
    require(json.loads(json.dumps(coverage)) == json.loads((directory / 'app/coverage.json').read_text()),
            'Full app coverage receipt mismatch')
    require((directory / 'app/coverage.json').read_bytes() ==
            (directory / 'app/accepted-credit-restart/coverage.json').read_bytes(), 'Restart receipt mismatch')
    boundary = (directory / 'app/accepted-credit-restart/boundary.log').read_text()
    markers = ['Complete successful seed report verified; PID=', 'Gallery must still be the resumed activity',
               'Force-stop verified live PID ', 'Verified target PID absent before normal verify instrumentation']
    positions = [boundary.find(marker) for marker in markers]
    require(all(p >= 0 for p in positions) and positions == sorted(positions), 'Restart sequence incomplete')
    require(re.search(r'topResumedActivity=.*MediaGalleryActivity', boundary), 'Gallery was not top resumed')
    seed_pid = str(reports['seed']['target_pid_before_instrumentation'])
    require(f'Complete successful seed report verified; PID={seed_pid}' in boundary and
            f'Force-stop verified live PID {seed_pid}' in boundary, 'Restart live PID mismatch')
    require('absent\nexit=0' in boundary, 'Missing explicit successful PID absence')
    screenshots = directory / 'app/vertical-locale-evidence'
    inventory = verify_screenshots(screenshots)
    require(inventory == json.loads((directory / 'vertical-locale-screenshots.json').read_text()), 'Screenshot receipt mismatch')
    reachability = verify_reachability(screenshots / 'reachability', 35)
    require(reachability == json.loads((directory / 'vertical-control-reachability.json').read_text()), 'Reachability receipt mismatch')
    decoded = []
    for path in sorted(screenshots.rglob('*.png')):
        with Image.open(path) as im:
            im.load()
            decoded.append({'path':path.relative_to(directory).as_posix(),'bytes':path.stat().st_size,
                            'sha256':digest(path.read_bytes()),'width':im.width,'height':im.height,
                            'decoded_rgba_sha256':digest(im.convert('RGBA').tobytes())})
    require(len(decoded) == 96, 'Expected 96 original screenshots')
    top = [row for row in decoded if Path(row['path']).parent.as_posix() == 'app/vertical-locale-evidence']
    require(len(top) == 32 and len({row['decoded_rgba_sha256'] for row in top}) == 32, 'Original capture states contain duplicate decoded images')
    pixels = {Path(row['path']).name:row['decoded_rgba_sha256'] for row in decoded}
    for case in reachability['cases']:
        name = case['case']
        require(pixels[name+'-minimum.png'] != pixels[name+'-maximum.png'], 'Endpoint pixels are identical: '+name)
    trace_results = []
    for path in sorted((screenshots/'reachability').glob('*.json')):
        receipt = json.loads(path.read_text())
        traces = [o for o in receipt['observations'] if o['kind'] == 'native-drag-trace']
        endpoints = [o for o in receipt['observations'] if o['kind'] == 'endpoint']
        require(len(traces) == len(endpoints), 'Trace/endpoint counts differ')
        for trace, endpoint in zip(traces,endpoints):
            prefix = receipt['case']+': '+str(trace['requested_quality'])
            require(trace['outcome'] == 'passed' and trace['observers_removed'] is True, prefix+': trace not passed/cleaned')
            require(trace['errors'] == [] and trace['dropped_events'] == 0 and trace['dropped_scroll_changes'] == 0,
                    prefix+': trace errors/dropped observations')
            actions = [e['action_masked'] for e in trace['events']]
            require(actions[0] == 0 and 2 in actions and actions[-1] == 1 and 3 not in actions,
                    prefix+': missing DOWN/MOVE/UP or CANCEL observed')
            wanted = trace['requested_quality']
            require(wanted in (1,100) and trace['before']['quality'] != wanted and
                    trace['after_injection']['quality'] == wanted and trace['after']['quality'] == wanted and
                    endpoint['value'] == wanted, prefix+': endpoint mismatch')
            before = trace['before']['seekbar']['parents']
            states = [e['state'] for e in trace['events']] + trace['scroll_changes'] + [trace['after_injection']]
            for state in states:
                parents = state['seekbar']['parents']
                require(len(parents) == len(before), prefix+': parent chain changed')
                require(all(p[a] == b[a] for p,b in zip(parents,before) for a in ('scroll_x','scroll_y')),
                        prefix+': ancestor scrolled')
            trace_results.append({'case':receipt['case'],'requested_quality':wanted,'events':len(actions),
                                  'ownership':'DOWN/MOVE/UP, no CANCEL, stationary ancestors, clean observer removal'})
    require(len(trace_results) == 28, 'Expected all 28 original native drags')
    return {'phases':phase_results,'installed_methods':sum(x['tests'] for x in phase_results.values()),
            'coverage':coverage,'screenshots':inventory,'reachability':reachability,
            'decoded_images':decoded,'native_drags':trace_results,'restart_boundary':'verified',
            'visual_review':'pending; decoding and model receipts are not visual acceptance'}


def regression(directory, source):
    suites = list((directory/'Paintroid/build/test-results').glob('**/TEST-*.xml'))
    require(bool(suites),'Missing JVM XML')
    totals = dict(tests=0,failures=0,errors=0,skipped=0)
    focus = {}
    for path in suites:
        root=ET.parse(path).getroot()
        for key in totals:totals[key] += int(root.attrib.get(key,0))
        require(len(root.findall('testcase')) == int(root.attrib['tests']),'JVM XML testcase mismatch')
        if any(name in path.name for name in ('NumericSliderGestureTest','VerticalTextRedrawTest','ImportSelectionTitleTest')):
            focus[path.name] = {k:int(root.attrib.get(k,0)) for k in totals}
    require(not any(totals[k] for k in ('failures','errors','skipped')),'JVM failed/skipped tests')
    require(len(focus) == 3,'Missing focused integration JVM suites')
    lint=list((directory/'app/build/reports').glob('lint-results-*.xml'))
    require(len(lint)==1,'Expected one lint XML')
    issues=len(ET.parse(lint[0]).getroot().findall('issue'));require(issues==0,'Lint issues present')
    return {'jvm_suites':len(suites),'jvm':totals,'focused_jvm_suites':focus,'lint_issues':issues}


def build(archive, manifest):
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'Corrupt build artifact')
        info=json.loads(z.read('build/delivery/build-info.json'))
        apk=z.read('app/build/outputs/apk/debug/app-debug.apk');source=z.read('build/delivery/AN-Paint-source.zip')
    require(digest(apk)==info['apk_sha256'] and digest(source)==info['source_sha256'],'Build-info digest mismatch')
    require(info['commit']==TESTED_MERGE and info['run_id']==str(RUN_ID),'Build identity mismatch')
    with zipfile.ZipFile(io.BytesIO(apk)) as z:
        require(z.read('assets/local-source/AN-Paint-source.zip')==source,'Embedded source mismatch')
    seen=set();extra=[];mismatches=[];native=collections.Counter()
    prefixes=tuple('Paintroid/build/'+p+'/' for p in ('jxl-source','webp-source','heif-source','tiff-source'))
    with zipfile.ZipFile(io.BytesIO(source)) as z:
        for n in z.namelist():
            if n.endswith('/'):continue
            p=n.removeprefix('AN-Paint/')
            if p not in manifest:
                if p.startswith(prefixes):native[p.split('/')[2]]+=1
                else:extra.append(p)
                continue
            data=z.read(n);actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if actual != manifest[p].split()[2]:mismatches.append(p)
            seen.add(p)
    require(not extra and not mismatches,{'extra':extra,'mismatches':mismatches})
    omitted=sorted(set(manifest)-seen)
    expected=sorted(p for p in manifest if '.idea' in Path(p).parts or Path(p).name=='.gitignore')
    require(omitted==expected,{'unexpected_omissions':omitted,'expected':expected})
    return {'build_info':info,'embedded_and_delivered_source_identical':True,'source_blobs_verified':len(seen),
            'omitted_tracked_paths':omitted,'additional_native_source_entries_by_declared_build_prefix':dict(native),
            'native_source_note':'Four declared bundled-source prefixes; their individual upstream blobs are not re-certified here.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('kind',choices=('device','regression','build'));p.add_argument('archive',type=Path)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True);args=p.parse_args();sys.path.insert(0,str(args.source/'tools'))
    if args.kind=='build':result=build(args.archive,json.loads(args.manifest.read_text())['candidate'])
    else:
        safe_extract(args.archive,args.directory)
        result=(device if args.kind=='device' else regression)(args.directory,args.source)
    out={'archive_sha256':digest(args.archive.read_bytes()),'source_tree':TREE,'head':HEAD,'run_id':RUN_ID,'tested_merge':TESTED_MERGE,'result':result}
    output=args.directory.parent/(args.kind+'-receipt.json');output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='result'}|{'result':result if args.kind!='device' else {'phases':result['phases'],'images':len(result['decoded_images']),'native_drags':len(result['native_drags'])}},indent=2))

if __name__=='__main__':main()
