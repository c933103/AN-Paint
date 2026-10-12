#!/usr/bin/env python3
"""Current-develop integration JUnit/render/ink audit; prior scripts remain frozen.

Use the downloaded, externally source-bound regression artifact. This program
cannot derive GitHub run authenticity from JUnit or pixels. It never marks
image shaping/readability as manually reviewed. Frozen checkout is read-only.
"""
import argparse, collections, hashlib, json, pathlib, subprocess, sys, re
import xml.etree.ElementTree as ET
TREE='b5d8cbeac9bf6d613ed7c3be787aa984826daafd'
HEAD='b0697fd58a2a37fb94e351f4c4ec68757b0f6b5e'
MERGE='e3dc717586539f8bbfe2ae3e3aae87e83db16d19'
RUN='38296205283'
TAGS=('en-GB','ain-Kana','ain-Latn','bo','ryu','fr','ar','ja','vi-Hani','mn-Mong','mnc-Mong','lzh-Hant','en-XV','qaa-Zsye-XV')
EVIDENCE='Robolectric NATIVE rendering, not installed-device capture'
def sha(b):return hashlib.sha256(b).hexdigest()
def read_source(repo,path):return subprocess.check_output(['git','show',TREE+':'+path],cwd=repo)
def records(counter):return [{'classname':c,'name':n,'count':v} for (c,n),v in sorted(counter.items()) if v]
def junit_audit(directory,expected):
    errors=[]; files=[]; cases=[]; failures=[]; skipped=[]
    for path in sorted(directory.rglob('TEST-*.xml')) if directory.exists() else []:
        data=path.read_bytes();files.append({'path':str(path.relative_to(directory)),'sha256':sha(data)})
        try: root=ET.fromstring(data)
        except ET.ParseError as ex:errors.append(str(path)+': '+str(ex));continue
        for suite in root.iter('testsuite'):
            immediate=suite.findall('testcase')
            if 'tests' in suite.attrib and int(suite.get('tests'))!=len(immediate):errors.append(str(path)+': declared test count mismatch')
            for field,tag in [('failures','failure'),('errors','error'),('skipped','skipped')]:
                if field in suite.attrib and int(suite.get(field))!=sum(bool(c.findall(tag)) for c in immediate):errors.append(str(path)+': declared '+field+' mismatch')
        for case in root.iter('testcase'):
            key=(case.get('classname',''),case.get('name',''));cases.append(key)
            if not all(key):errors.append(str(path)+': testcase identity missing')
            for tag in ('failure','error','skipped'):
                for node in case.findall(tag):
                    record={'classname':key[0],'name':key[1],'kind':tag,'type':node.get('type'),'message':node.get('message'),'detail':node.text or '', 'xml':str(path.relative_to(directory))}
                    (skipped if tag=='skipped' else failures).append(record)
    actual=collections.Counter(cases); wanted=collections.Counter(tuple(x) for x in expected)
    missing=wanted-actual;extra=actual-wanted;duplicates={k:v for k,v in actual.items() if v>1}
    ok=bool(files) and not any((errors,failures,skipped,missing,extra,duplicates))
    return {'status':'PASS' if ok else 'FAIL','expected_count':sum(wanted.values()),'actual_count':len(cases),'passing_testcases':len(cases)-len({(x['classname'],x['name']) for x in failures+skipped}),'missing':records(missing),'unexpected':records(extra),'duplicates':records(duplicates),'failures_and_errors':failures,'skipped':skipped,'parse_or_count_errors':errors,'xml_files':files}
def messages(repo):
    sys.path.insert(0,str(repo/'tools'))
    import translation_catalogues as cat
    paths=cat.catalogue_paths()
    def resources(p):return {n.get('name'):''.join(n.itertext()) for n in ET.fromstring(read_source(repo,p)) if n.tag=='string'}
    defaults=resources('Paintroid/src/main/res/values/strings.xml');out={}
    for tag in TAGS:
        values=defaults|resources(str(paths[tag].relative_to(repo)))
        for action,key in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]:
            raw=values[key].replace('%1$s',values['commons_metadata_query_failed']).replace("\\'","'")
            require('\\' not in raw and '"' not in raw,'unsupported Android quotation syntax')
            out[(tag,action)]=raw
    return out

def current_inventory(repo):
    from run_android_instrumentation import ANNOTATIONS
    expected=[];sources=[]
    for p in sorted((repo/'Paintroid/src/test').rglob('*.kt')):
        source=read_source(repo,str(p.relative_to(repo))).decode()
        package=re.search(r'^package\s+([\w.]+)',source,re.M)
        owners=list(re.finditer(r'^[ \t]*(?P<annotations>'+ANNOTATIONS+r')?(?:(?:internal|public|open|abstract)\s+)*class\s+(?P<owner>\w+)',source,re.M))
        owner=next((o for o in owners if o.group('owner')==p.stem),None)
        matches=list(re.finditer(r'(?P<annotations>'+ANNOTATIONS+r')(?:(?:public|internal|suspend)\s+)*fun\s+(?P<method>`[^`]+`|\w+)\s*\(',source))
        methods=[m for m in matches if re.search(r'@Test\b',m.group('annotations'))]
        require(len(methods)==len(re.findall(r'@Test\b',source)),'unparsed source tests '+str(p))
        if not methods:continue
        require(package and owner and '@Ignore' not in source,'unsupported class/ignored test '+str(p))
        def sdks(annotations):
            configs=re.findall(r'@Config\(([^)]*)\)',annotations)
            values=[re.search(r'\bsdk\s*=\s*\[([^]]+)\]',c) for c in configs if re.search(r'\bsdk\s*=',c)]
            require(all(values) and len(values)<=1,'unparsed SDK config')
            if not values:return None
            require(re.fullmatch(r'[\d,\s]+',values[0].group(1)),'nonliteral SDK config')
            return [int(x.strip()) for x in values[0].group(1).split(',')]
        default=sdks(owner.group('annotations') or '') or [None]
        for method in methods:
            sdk=sdks(method.group('annotations')) or default
            name=method.group('method').strip('`')
            expected.extend((package.group(1)+'.'+owner.group('owner'),name+(f'[{v}]' if i<len(sdk)-1 else '')) for i,v in enumerate(sdk))
        sources.append({'path':str(p.relative_to(repo)),'sha256':sha(source.encode()),'declared_methods':len(methods)})
    require(len(set(expected))==len(expected),'duplicate source execution identities')
    return {'expected':expected,'sources':sources,'scope':'Current Kotlin @Test declarations expanded by literal class/method @Config SDK lists; final selected SDK uses the unsuffixed Robolectric identity. No historical inventory fixture.'}

def render_audit(directory,expected_messages):
    from PIL import Image
    wanted={f'api35-{tag}-{w}x{h}-font{scale}-{action}':(tag,w,h,scale,action) for tag in TAGS for w,h in [(320,640),(640,320)] for scale in (1.0,2.0) for action in ('copy','insert')}
    present={p.name:p for p in directory.iterdir() if p.is_file()} if directory.exists() else {}
    required={stem+suffix for stem in wanted for suffix in ('.png','.json')}
    missing=sorted(required-set(present));unexpected=sorted(set(present)-required);problems=[];checked=[]
    for stem,(tag,w,h,scale,action) in sorted(wanted.items()):
        png=present.get(stem+'.png');metadata=present.get(stem+'.json')
        if png is None or metadata is None:continue
        try:
            data=json.loads(metadata.read_bytes());reason=expected_messages[(tag,action)]
            expected={'evidence_kind':EVIDENCE,'locale':tag,'font_scale':scale,'action':action,'message':reason,'all_characters_laid_out':True}
            scroll=data.get('status_parent_scroll_x')
            if type(scroll) is not int or scroll<0:problems.append({'file':metadata.name,'reason':'invalid status scrollX'})
            if tag not in ('lzh-Hant','qaa-Zsye-XV') and scroll!=0:problems.append({'file':metadata.name,'reason':'reading-start scrollX must be zero for this direction'})
            expected['status_parent_scroll_x']=scroll
            if data!=expected:problems.append({'file':metadata.name,'reason':'JSON mismatch','expected':expected,'actual':data})
            with Image.open(png) as im:
                im.load()
                if im.format!='PNG' or im.size!=(w*2,h*2):problems.append({'file':png.name,'reason':'format or xhdpi dimensions differ','format':im.format,'size':im.size})
                if all(lo==hi for lo,hi in im.convert('RGB').getextrema()):problems.append({'file':png.name,'reason':'uniform image'})
                size=list(im.size)
            checked.append({'stem':stem,'dimensions':size,'png_sha256':sha(png.read_bytes()),'json_sha256':sha(metadata.read_bytes()),'status_parent_scroll_x':scroll,'u180e_count':data.get('message','').count('\u180e'),'u202f_count':data.get('message','').count('\u202f')})
        except Exception as ex:problems.append({'file':stem,'reason':str(ex)})
    return {'status':'PASS' if not (missing or unexpected or problems) else 'FAIL','expected_pairs':112,'complete_pairs_checked':len(checked),'missing_files':missing,'unexpected_files':unexpected,'errors':problems,'pairs':checked,'visual_review':'UNRUN by this script; inspect actual pixels and maintain scroll/reachability limits. JSON text and PNG existence do not prove shaping.'}

VERTICAL={'mn-Mong','mnc-Mong','lzh-Hant','en-XV','qaa-Zsye-XV'}
DIAGNOSTIC_EVIDENCE='Robolectric NATIVE pre-assertion diagnostic; not installed-device or acceptance evidence'

def require(v,message):
    if not v:raise ValueError(message)

def finite_json(path):
    def no_constant(value):raise ValueError('nonfinite JSON number '+value)
    return json.loads(path.read_bytes(),parse_constant=no_constant)

def ink_metrics(image,data):
    """Independently recompute producer alpha-pixel statistics from actual PNG."""
    alpha=image.convert('RGBA').getchannel('A');w,h=image.size
    margin=data['expanded_layout_margin_px'];lw=data['layout_width'];lh=data['layout_height']
    require(type(margin) is int and margin>=32,'invalid expanded margin')
    require((w,h)==(lw+2*margin,lh+2*margin),'expanded raster dimensions')
    def count(box):
        crop=alpha.crop(box);return crop.width*crop.height-crop.histogram()[0]
    edges={'left':count((0,0,1,h))>0,'right':count((w-1,0,w,h))>0,'top':count((0,0,w,1))>0,'bottom':count((0,h-1,w,h))>0}
    require(edges==data['expanded_canvas_edge_touch'],'canvas edge-contact receipt differs from pixels')
    result=[]
    for line in data['lines']:
        y0=max(0,margin+line['top']);y1=min(h,margin+line['bottom'])
        require(type(y0) is int and type(y1) is int and y0<=y1,'invalid line box')
        box=alpha.crop((0,y0,w,y1)).getbbox()
        left=None if box is None else box[0]-margin;right=None if box is None else box[2]-margin
        outside=count((0,y0,margin,y1))+count((margin+lw,y0,w,y1))
        require((left,right,outside)==(line['ink_left'],line['ink_right_exclusive'],line['ink_pixels_outside_layout']), 'line '+str(line['line'])+' ink receipt differs from pixels')
        result.append({'line':line['line'],'ink_left':left,'ink_right_exclusive':right,'ink_pixels_outside_layout':outside})
    return edges,result

def diagnostic_audit(directory,expected_messages):
    from PIL import Image
    wanted={f'api35-{tag}-640x320-font1.0-{action}-before-checks':(tag,action) for tag in TAGS for action in ('copy','insert')}
    needed={stem+suffix for stem in wanted for suffix in ('.png','-expanded-layout.png','.json')}|{'normal-landscape-outcomes.json'}
    present={p.name:p for p in directory.iterdir() if p.is_file()} if directory.exists() else {}
    missing=sorted(needed-present.keys());extra=sorted(present.keys()-needed);errors=[];profiles=[];guards=[];observations=[]
    for stem,(tag,action) in sorted(wanted.items()):
        if any(stem+s not in present for s in ('.png','-expanded-layout.png','.json')):continue
        try:
            data=finite_json(present[stem+'.json']);expected=expected_messages[(tag,action)]
            require(data['evidence_kind']==DIAGNOSTIC_EVIDENCE,'diagnostic classification')
            require(data['locale']==tag and data['action']==action and data['font_scale']==1.0 and data['configured_font_scale']==1.0,'profile fields')
            require(data['message']==expected and data['accessibility_text']==expected,'diagnostic full message/accessibility text')
            require(data['viewport_width']==1280 and data['viewport_height']==640 and data['density']==2.0,'viewport/density')
            require(type(data['layout_width']) is int and data['layout_width']>0,'invalid layout width')
            require(len(data['lines'])==data['line_count'] and data['line_count']>0,'line inventory')
            utf16=expected.encode('utf-16-le');end=0
            for index,line in enumerate(data['lines']):
                require(line['line']==index and line['start']==end and line['end']>=end,'line range/inventory')
                require(line['text']==utf16[line['start']*2:line['end']*2].decode('utf-16-le'),'UTF16 line text differs')
                end=line['end'];guard=line['left']>=-1.0 and line['right']<=data['layout_width']+1.0
                require(type(line['original_horizontal_guard']) is bool and guard==line['original_horizontal_guard'],'guard boolean differs from exact unchanged formula')
                if not guard:
                    row={'profile':stem,'line':index,'left':line['left'],'right':line['right'],'layout_width':data['layout_width'],'text':line['text'],'ink_pixels_outside_layout':line['ink_pixels_outside_layout']}
                    (observations if tag in VERTICAL else guards).append(row)
            require(data['all_characters_laid_out']==(end==len(utf16)//2),'laid-out receipt differs')
            with Image.open(present[stem+'.png']) as screen:
                screen.load();require(screen.format=='PNG' and screen.size==(1280,640),'diagnostic root image dimensions/format')
            with Image.open(present[stem+'-expanded-layout.png']) as ink:
                ink.load();require(ink.format=='PNG','expanded format');edges,lines=ink_metrics(ink,data)
            profiles.append({'profile':stem,'guard_applies':tag not in VERTICAL,'line_count':data['line_count'],'original_guard_booleans':[line['original_horizontal_guard'] for line in data['lines']],'edge_contact':edges,'independent_pixel_metrics':lines,'files':[{'name':stem+s,'sha256':sha(present[stem+s].read_bytes())} for s in ('.json','.png','-expanded-layout.png')]})
        except Exception as ex:errors.append({'profile':stem,'error':str(ex)})
    outcomes=None
    if 'normal-landscape-outcomes.json' in present:
        try:
            outcomes=finite_json(present['normal-landscape-outcomes.json'])
            require(outcomes['completed_profiles']==28 and outcomes['expected_profiles']==28,'outcome profile count')
            require(isinstance(outcomes['failures'],list) and all(isinstance(s,str) for s in outcomes['failures']),'failure list')
            require(outcomes['all_profiles_passed']==(not outcomes['failures']),'outcome boolean/list mismatch')
            require(outcomes['evidence_kind']=='Current source-bound structural/readability checks; exact raster differences require separate review','outcomes classification')
            require(outcomes['pixel_acceptance_role']=='Exact raster reports are unmasked diagnostics; all_profiles_passed does not imply exact pixel equality or disposition of review_required frames','pixel acceptance role')
            require(outcomes['advance_guard_role']=='Diagnostic only; original_horizontal_guard=false is not a claim of painted-ink clipping','advance diagnostic role')
        except Exception as ex:errors.append({'profile':'normal-landscape-outcomes','error':str(ex)})
    return {'integrity_status':'PASS' if not (missing or extra or errors) else 'FAIL','expected_profiles':28,'checked_profiles':len(profiles),'missing':missing,'unexpected':extra,'errors':errors,'applicable_horizontal_guard_failures':guards,'vertical_line_guard_observations_not_acceptance_oracles':observations,'outcomes':outcomes,'profiles':profiles,'pixel_review':'UNRUN by script. Before repair conclusions inspect actual root and expanded pixels for failing profiles; finite canvas edge contact and native line-box limits remain.'}

def bind_archive(archive,root,binding):
    import zipfile
    require(not TREE.startswith('PENDING') and not HEAD.startswith('PENDING') and not MERGE.startswith('PENDING') and not RUN.startswith('PENDING'),'actual publication binding is pending')
    require(binding['tree']==TREE,'unexpected successor tree')
    for key in ('head','merge'):
        require(len(binding[key])==40 and all(c in '0123456789abcdef' for c in binding[key]),'missing actual '+key)
    require(binding['head']==HEAD and binding['merge']==MERGE and str(binding['run_id'])==RUN,'actual publication/run binding mismatch')
    digest=binding.get('regression_artifact_sha256')
    require(isinstance(digest,str) and len(digest)==64,'artifact digest still pending')
    require(sha(archive.read_bytes())==binding['regression_artifact_sha256'],'regression archive hash mismatch')
    with zipfile.ZipFile(archive) as z:
        names=[n for n in z.namelist() if not n.endswith('/')]
        require(len(set(names))==len(names),'duplicate artifact paths')
        for n in names:
            p=pathlib.PurePosixPath(n);require(not p.is_absolute() and '..' not in p.parts and '\\' not in n,'unsafe artifact path')
            require(z.read(n)==(root/n).read_bytes(),'extracted artifact mismatch '+n)
        actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
        require(actual==set(names),'extraction has stale/extra files')
    return len(names)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('repo','artifact','extracted','binding','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
    a=p.parse_args();binding=finite_json(a.binding);checked=bind_archive(a.artifact,a.extracted,binding)
    global TAGS
    flow=read_source(a.repo,'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt').decode()
    source_tags=re.search(r'for\(tag in listOf\(([^)]*)\)\)',flow[flow.index('private fun readable('):]).group(1)
    TAGS=tuple(re.findall(r'"([^"\n]+)"',source_tags))
    sys.path.insert(0,str(a.repo/'tools'))
    inventory=current_inventory(a.repo)
    expected=messages(a.repo);base=a.extracted/'Paintroid/build'
    result={'binding':binding,'binding_limit':'Run/source authenticity is externally verified by parent; this audit verifies downloaded bytes and pinned source expectations.','artifact_files_exact':checked,'junit':junit_audit(base/'test-results/testDebugUnitTest',inventory['expected']),'success_renders':render_audit(base/'reports/commons-metadata-m04',expected),'diagnostics':diagnostic_audit(base/'reports/commons-metadata-m04-diagnostic',expected)}
    import audit_integration_ink as ink
    control_fragment=flow[flow.index('private fun inkOracleNegativeControls('):]
    ink.CONTROL_TAGS=tuple(re.findall(r'"([^"\n]+)"',re.search(r'for\(tag in listOf\(([^)]*)\)\)',control_fragment).group(1)))
    ink.TAGS=tuple(t for t in TAGS if t not in VERTICAL)
    ink_audit=ink.audit
    result['current_source_inventory']=inventory
    result['painted_ink']=ink_audit(base/'reports/commons-metadata-m04-painted-ink',expected)
    result['visual_and_installed_acceptance']='UNRUN by this automated checker; all review-required positives need a fresh explicit disposition'
    a.output.with_name('current-profile-messages.json').write_text(json.dumps([{'locale':t,'action':act,'message':m} for (t,act),m in expected.items()],ensure_ascii=False,indent=2)+'\n')
    result['automated_artifact_checks']='PASS' if result['junit']['status']==result['success_renders']['status']==result['diagnostics']['integrity_status']==result['painted_ink']['status']=='PASS' and result['diagnostics']['outcomes']['all_profiles_passed'] else 'FAIL'
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'automated_artifact_checks':result['automated_artifact_checks'],'junit':result['junit']['status'],'jvm_cases':result['junit']['actual_count'],'success_render_pairs':result['success_renders']['complete_pairs_checked'],'diagnostic_integrity':result['diagnostics']['integrity_status'],'diagnostic_profiles':result['diagnostics']['checked_profiles'],'old_advance_diagnostic_violations':result['diagnostics']['applicable_horizontal_guard_failures'],'ink_frames':result['painted_ink']['checked_frames'],'ink_status':result['painted_ink']['status']},ensure_ascii=False,indent=2))
    sys.exit(0 if result['automated_artifact_checks']=='PASS' else 1)
if __name__=='__main__':main()
