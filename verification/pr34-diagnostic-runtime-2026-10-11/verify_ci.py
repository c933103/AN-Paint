#!/usr/bin/env python3
"""Validate exact-source PR34/PR41 combined CI artifacts; image decoding is not visual acceptance."""
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

HEAD = '9b62193455f3794192fe7e8b8ef6c3360d6e297f'
TREE = 'd071e57d5774a639b7352f0cfa876b8922b4d899'
TESTED_MERGE = 'da8c027eb0e2c018c225240df0638b53a85d5e24'
RUN_ID = 38081755104


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


def device(directory, source, sdk):
    from PIL import Image
    from run_android_instrumentation import declared_tests, parse_protocol, source_tests_sha256
    from vertical_locale_matrix import verify_screenshots
    from app_instrumentation_matrix import app_partition, verify_app_reports, report_paths, read_app_reports, PHASE_TIMEOUTS, coverage_paths
    from vertical_control_reachability import verify as verify_reachability
    from vertical_evidence_transport import extract as extract_transport
    import tempfile
    transport_receipt = json.loads((directory / 'vertical-locale-export.json').read_text())
    with tempfile.TemporaryDirectory() as temporary:
        reconstructed = Path(temporary) / 'evidence'
        transport = extract_transport(directory / 'vertical-locale-export', reconstructed, sdk)
        require(transport == transport_receipt, 'Transport receipt differs from bounded raw ZIP validation')
        original = directory / 'app/vertical-locale-evidence'
        relative = {p.relative_to(reconstructed).as_posix() for p in reconstructed.rglob('*') if p.is_file()}
        require(relative == {p.relative_to(original).as_posix() for p in original.rglob('*') if p.is_file()},
                'Transport/host evidence path inventory differs')
        for name in relative:
            require((reconstructed / name).read_bytes() == (original / name).read_bytes(),
                    'Transport/host evidence bytes differ: ' + name)
    app_source = source / 'app/src/androidTest'
    expected = declared_tests(app_source, sdk_level=sdk)
    parts = app_partition(expected, sdk)
    locations = {phase: path.parent for phase, path in report_paths(directory, sdk).items()}
    locations['native'] = directory / 'Paintroid/androidTest-results'
    bound_reports = read_app_reports(directory, sdk)
    native_source = source / 'Paintroid/src/androidTest'
    native = declared_tests(native_source, sdk_level=sdk)
    if sdk == 30:
        native = {item for item in native if item[0] != 'org.catrobat.paintroid.classic.UltraHdrImportTest'}
    expected_parts = dict(parts, native=native)
    require(len(expected) == (24 if sdk == 30 else 25) and len(native) == (73 if sdk == 30 else 74), 'Unexpected current source method totals')
    reports, phase_results = {}, {}
    for phase, path in locations.items():
        report = json.loads((path / 'summary.json').read_text())
        source_digest = source_tests_sha256(native_source if phase == 'native' else app_source)
        require(report['success'] is True and report['device_sdk'] == sdk, f'{phase}: unsuccessful/wrong SDK')
        require(report['source_tests_sha256'] == source_digest, f'{phase}: source digest differs')
        require(report['returncode'] == 0 and report['timed_out'] is False, f'{phase}: process failed/timed out')
        require(report['timeout_seconds'] == (180 if phase == 'native' else PHASE_TIMEOUTS[phase]), f'{phase}: changed budget')
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
        phase_results[phase] = {'tests': len(expected_parts[phase]), 'seconds': report['elapsed_seconds'], 'timeout_seconds': report['timeout_seconds']}
        require(abs(float(xml.attrib['time']) - report['elapsed_seconds']) < 0.002, f'{phase}: XML elapsed time mismatch')
        if phase in ('ordinary', 'gallery-draft'):
            target = 150 if phase == 'ordinary' else 70
            require(report['elapsed_seconds'] <= target, f'{phase}: inadequate original timing margin')
        if phase != 'native':
            require(report == bound_reports[phase], f'{phase}: report binding mismatch')
            reports[phase] = report
    coverage = verify_app_reports(expected, sdk, reports, source_tests_sha256(app_source),
                                  declared_tests(app_source)-expected)
    require(json.loads(json.dumps(coverage)) == json.loads((directory / 'app/coverage.json').read_text()),
            'Full app coverage receipt mismatch')
    selected_receipts = coverage_paths(directory) if sdk == 35 else coverage_paths(directory)[:-1]
    require(len({path.read_bytes() for path in selected_receipts}) == 1, 'Complete union compatibility receipts differ')
    if sdk == 35:
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
    else:
        status = (directory/'app/accepted-credit-restart/verify-status.txt').read_text()
        require('API35-only; both phase classes excluded on API30' in status, 'API30 exclusions not explicit')
        require(not coverage_paths(directory)[-1].exists(), 'API30 stale restart receipt')
    screenshots = directory / 'app/vertical-locale-evidence'
    inventory = verify_screenshots(screenshots)
    require(inventory == json.loads((directory / 'vertical-locale-screenshots.json').read_text()), 'Screenshot receipt mismatch')
    reachability = verify_reachability(screenshots / 'reachability', sdk)
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
            'decoded_images':decoded,'native_drags':trace_results,'restart_boundary':'verified' if sdk == 35 else 'explicit API30 exclusion',
            'application_log_oracles':application_log_oracles(directory,sdk),
            'visual_review':'pending; decoding and model receipts are not visual acceptance'}



def application_log_oracles(directory, sdk):
    lines=(directory/'logcat.txt').read_text().splitlines()
    def rows(tag):
        marker=tag+': '
        return [json.loads(line.split(marker,1)[1]) for line in lines
                if marker in line and line.split(marker,1)[1].startswith('{')]
    korean=rows('ExactScriptResourceTest')
    require([row['phase'] for row in korean]==['mixed-selected','mixed-after-rotation','ordinary-selected','mixed-reselected'], 'Exact four Korean picker/rotation phases required')
    for row in korean:
        mixed=row['phase']!='ordinary-selected';tag='ko-Kore-KR' if mixed else 'ko-KR';verb='複寫' if mixed else '복사'
        require(row['api']==sdk and all(row[k]==tag for k in ('requested_tag','persisted_tag','default_tag')), 'Public Korean identity changed')
        require(row['platform_tag']==(tag if sdk>=33 else None), 'Platform Korean identity mismatch')
        require(row['configured_tag']==('ko-Kore-KR-anpaint' if mixed else 'ko-KR'), 'Private Korean resource variant mismatch')
        expected={'ui_save':'貯藏' if mixed else '저장','commons_credit_copy_failed':f'이미지 크레딧을 {verb}할 수 없습니다.',
                  'commons_credit_copy_failed_reason':f'이미지 크레딧을 {verb}할 수 없습니다: probe',
                  'commons_credit_copy_out_of_memory':f'이미지 크레딧을 {verb}할 메모리가 부족합니다.'}
        require(row['strings']==expected, 'Korean exact mixed/ordinary strings mismatch')
    before,after=korean[:2]
    require(before['orientation']!=after['orientation'] and
            (before['screen_width_dp'],before['screen_height_dp'])!=(after['screen_width_dp'],after['screen_height_dp']),
            'Korean real display rotation missing')
    viewport=[row for row in rows('GalleryViewportDeviceTest') if 'locale' in row]
    require(len(viewport)==4 and {(row['locale'],row['orientation']) for row in viewport}==
            {('fr',1),('fr',2),('mn-Mong',1),('mn-Mong',2)}, 'Exact font/viewport locale and orientation matrix required')
    for row in viewport:
        require(row['font_scale']==2 and row['browser_width']>0 and row['browser_height']>=row['required_reserve']>0,
                'Real font/viewport reserve not proven')
        require(row['provider']=='real installed WebView; verified rejecting proxy; local HTML','Unexpected viewport provider evidence')
    processes={}
    for line in lines:
        match=re.match(r'^\S+\s+\S+\s+(\d+)\s+\d+\s+I\s+TestRunner: started: .+\((paint\.anpaint\.android\.[^)]+)\)$',line)
        if match:processes.setdefault(match[2],set()).add(int(match[1]))
    gallery=processes.get('paint.anpaint.android.GalleryDraftDeviceTest',set())
    ordinary=processes.get('paint.anpaint.android.EditorDeviceTest',set())
    require(len(gallery)==len(ordinary)==1 and not gallery&ordinary,'Gallery cold process is not distinct from ordinary app')
    startup=(directory/'startup.log').read_text()
    completed=re.findall(r'\[\+(\d+)s\] Instrumentation complete \(result 0\)',startup)
    require(len(completed)==1 and int(completed[0])<2160, 'Complete script did not finish within corrected configured outer window')
    return {'korean_phases':korean,'viewport_phases':viewport,'test_processes':{k:sorted(v) for k,v in processes.items()},
            'gallery_cold_process_distinct':True,'instrumentation_complete_at_seconds':int(completed[0])}


def generator(directory, source):
    report=json.loads((directory/'summary.json').read_text())
    require(report['success'] is True and report['commit']==TESTED_MERGE and report['tree']==TREE,'Generator exact source/identity mismatch')
    labels=['01-clean','02-clean-debug-release','03-unchanged','04-input-change-and-stale-output','05-restored-input-release','06-second-clean','07-release-first-after-clean']
    require([p['name'] for p in report['probes']]==labels,'Generator missing/extra/reordered stage')
    for row in report['probes']:
        require(row['exit_code']==0 and digest((directory/(row['name']+'.log')).read_bytes())==row['log_sha256'],'Generator failed/log binding mismatch')
        excluded=[row['command'][i+1] for i,x in enumerate(row['command']) if x=='-x']
        require(excluded==[':Paintroid:bundleCorrespondingSource'],'Unexpected generator task exclusion')
    require(report['wrapper_sha256']==digest((source/'gradle/wrapper/gradle-wrapper.properties').read_bytes()),'Generator wrapper mismatch')
    require(report['root_build_sha256']==digest((source/'build.gradle').read_bytes()),'Generator root build mismatch')
    canonical=source/'Paintroid/src/main/res/values-b+ko+Kore+KR/strings.xml'
    expected={'values-b+ko+Kore+KR+anpaint/strings.xml':digest(canonical.read_bytes())}
    for index in (1,4,6):require(report['probes'][index]['generated_sha256']==expected,'Generated bytes differ from canonical source')
    require(report['probes'][3]['generated_sha256']!=expected,'Input mutation did not regenerate distinct bytes')
    return report


def regression(directory, source):
    suites = list((directory/'Paintroid/build/test-results').glob('**/TEST-*.xml'))
    require(bool(suites),'Missing JVM XML')
    totals = dict(tests=0,failures=0,errors=0,skipped=0)
    focus = {}
    identities = []
    for path in suites:
        root=ET.parse(path).getroot()
        for key in totals:totals[key] += int(root.attrib.get(key,0))
        require(len(root.findall('testcase')) == int(root.attrib['tests']),'JVM XML testcase mismatch')
        identities.extend((case.attrib['classname'], case.attrib['name']) for case in root.findall('testcase'))
        if any(name in path.name for name in ('NumericSliderGestureTest','VerticalTextRedrawTest','ImportSelectionTitleTest')):
            focus[path.name] = {k:int(root.attrib.get(k,0)) for k in totals}
    require(not any(totals[k] for k in ('failures','errors','skipped')),'JVM failed/skipped tests')
    required = json.loads(Path(__file__).with_name('expected-jvm-union.json').read_text())
    require(len(identities) == len(set(identities)), 'Duplicate combined JVM cases')
    require(set(identities) == {tuple(item) for item in required['identities']}, 'Combined JVM inventory differs from exact accepted-parent union')
    require(totals['tests'] == 793, 'Expected all 793 combined JVM cases')
    require(len(focus) == 3,'Missing focused integration JVM suites')
    lint=list((directory/'app/build/reports').glob('lint-results-*.xml'))
    require(len(lint)==1,'Expected one lint XML')
    issues=len(ET.parse(lint[0]).getroot().findall('issue'));require(issues==0,'Lint issues present')
    return {'jvm_suites':len(suites),'jvm':totals,'exact_parent_jvm_union_verified':True,'focused_jvm_suites':focus,'lint_issues':issues}


def build(archive, manifest):
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'Corrupt build artifact')
        info=json.loads(z.read('build/delivery/build-info.json'))
        require(info['build_variant'] == 'release', 'Final combined validation must be release-configured')
        apk=z.read('app/build/outputs/apk/release/app-release.apk');source=z.read('build/delivery/AN-Paint-source.zip')
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
    p=argparse.ArgumentParser();p.add_argument('kind',choices=('device','regression','build','generator'));p.add_argument('archive',type=Path)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True);p.add_argument('--sdk',type=int,choices=(30,35));args=p.parse_args();sys.path.insert(0,str(args.source/'tools'))
    if args.kind=='build':result=build(args.archive,json.loads(args.manifest.read_text())['candidate'])
    else:
        safe_extract(args.archive,args.directory)
        result=device(args.directory,args.source,args.sdk) if args.kind=='device' else (generator if args.kind=='generator' else regression)(args.directory,args.source)
    out={'archive_sha256':digest(args.archive.read_bytes()),'source_tree':TREE,'head':HEAD,'run_id':RUN_ID,'tested_merge':TESTED_MERGE,'result':result}
    output=args.directory.parent/(args.kind+(str(args.sdk) if args.sdk else '')+'-receipt.json');output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='result'}|{'result':result if args.kind!='device' else {'phases':result['phases'],'images':len(result['decoded_images']),'native_drags':len(result['native_drags'])}},indent=2))

if __name__=='__main__':main()
