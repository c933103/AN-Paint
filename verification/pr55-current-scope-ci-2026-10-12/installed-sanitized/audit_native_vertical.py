#!/usr/bin/env python3
"""Source-derived native vertical export, geometry, input and Save telemetry audit.
This replays retained evidence; it never executes Android or changes source/artifacts.
Every decoded frame still requires actual visual review.
"""
import argparse,collections,io,json,pathlib,re,sys,zipfile
from PIL import Image
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,require,sha,read_source

SAVE_FIELDS='default activity target rootLocale dialogLocale application selected busy draft saved attached raw visible root form columns'.split()
RECT=re.compile(r'Rect\((-?\d+), (-?\d+) - (-?\d+), (-?\d+)\)')
LINE=re.compile(r'^\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\s+\d+\s+\d+\s+I\s+VerticalLocaleDeviceTest\s*:\s*(\S+) Save (before|touch=ACTION_(?:DOWN|UP|CANCEL)|failure) (.+)$')
def strict(pairs):
 d={}
 for k,v in pairs:require(k not in d,'duplicate JSON field '+k);d[k]=v
 return d
def read_json(p):return json.loads(p.read_bytes(),object_pairs_hook=strict)
def parse_save(raw, cases, opens):
 require(len(raw)<=128*1024*1024,'bounded logcat exceeded')
 rows=[];groups=collections.defaultdict(list)
 for no,line in enumerate(raw.decode('utf-8').splitlines(),1):
  if not re.search(r'VerticalLocaleDeviceTest\s*:\s*\S+ Save ',line):continue
  m=LINE.fullmatch(line);require(m is not None,'malformed Save telemetry line '+str(no));case,phase,rest=m.groups();require(case in cases,'unexpected Save case '+case)
  keys=list(re.finditer(r'(?:^| )([A-Za-z]+)=',rest));require([x[1] for x in keys]==SAVE_FIELDS,'Save fields incomplete, duplicate or reordered')
  d={x[1]:rest[x.end():keys[i+1].start() if i+1<len(keys) else len(rest)] for i,x in enumerate(keys)}
  for k in ('busy','attached','root'):require(d[k] in ('true','false'),'nonboolean Save '+k);d[k]=d[k]=='true'
  for k in ('draft','saved'):require(re.fullmatch(r'\d+',d[k]),'invalid Save generation');d[k]=int(d[k])
  for k in ('raw','visible'):
   r=RECT.fullmatch(d[k]);require(r is not None,'malformed Save bounds '+k);d[k]=list(map(int,r.groups()))
  for k in ('form','columns'):require(d[k]=='absent' or re.fullmatch(r'\d+x\d+',d[k]),'malformed Save dimensions')
  locale=case.rsplit('-',1)[0]
  require(d['selected']==locale and all(d[k].split(',')[0]==locale for k in ('activity','target','rootLocale')),'Save rendering resource locale differs from selected')
  require(phase!='failure','Save failed; telemetry remains diagnostic only')
  rec=dict(line_number=no,case=case,phase=phase,state=d);rows.append(rec)
  if phase=='before':groups[case].append([])
  require(groups[case],'Save touch before snapshot');groups[case][-1].append(rec)
 require(set(groups)==set(cases),'Save telemetry missing case')
 summaries=[]
 for case in sorted(cases):
  require(len(groups[case])==opens,'source-derived Save call count differs '+case)
  for i,g in enumerate(groups[case]):
   phases=[r['phase'] for r in g];require(phases[0]=='before' and phases[-1]=='touch=ACTION_UP','Save input has no final native UP')
   down=False
   for r in g[1:]:
    if r['phase']=='touch=ACTION_DOWN':require(not down,'overlapping DOWN');down=True
    else:require(down,'endpoint without DOWN');down=False
   require(not down,'unterminated Save gesture');last=g[-1]['state'];l,t,r,b=last['raw'];vl,vt,vr,vb=last['visible']
   require(last['attached'] and not last['busy'] and vl<vr and vt<vb and vl<=(l+r)//2<vr and vt<=(t+b)//2<vb,'final Save UP target center not reachable/ready')
  summaries.append(dict(case=case,opens=len(groups[case]),snapshots=sum(map(len,groups[case])),process_locales=sorted({r['state']['default'] for g in groups[case] for r in g}),application_locales=sorted({r['state']['application'] for g in groups[case] for r in g}),dialog_resource_locales_observed=sorted({r['state']['dialogLocale'] for g in groups[case] for r in g})))
 return dict(status='PASS_BOUNDED_SAVE_TELEMETRY',opens_per_case=opens,cases=summaries,records=rows,limitations='Snapshots are before/click dispatch and failure only. A successful pre-click absent dialog is not post-mount dialog-resource telemetry; mounted geometry and execution are separate receipts.')

def audit(repo,artifacts,out,apis=(30,35)):
 for name in ('vertical_locale_matrix.py','vertical_evidence_transport.py','vertical_control_reachability.py','run_android_instrumentation.py'):
  require(read_source(repo,'tools/'+name)==(repo/'tools'/name).read_bytes(),'source helper differs '+name)
 sys.path.insert(0,str(repo/'tools'))
 import vertical_locale_matrix as vm,vertical_evidence_transport as vt,vertical_control_reachability as vr
 src=read_source(repo,'app/src/androidTest/java/paint/anpaint/android/VerticalLocaleDeviceTest.kt').decode()
 body=src.split('private fun checkLocale(',1)[1].split('private fun orient(',1)[0]
 opens=len(re.findall(r'^\s*openSave\(\)\s*$',body,re.M));require(opens>0,'no source Save opens')
 cases={f'{tag}-{o}' for tag in vm.LOCALES for o in vm.ORIENTATIONS};result={}
 for api in apis:
  root=artifacts/f'api{api}';dest=out/f'native-observed-api{api}';transport=vt.extract(root/'vertical-locale-export',dest,api)
  require(transport==read_json(root/'vertical-locale-export.json'),'transport receipt differs')
  screen=vm.verify_screenshots(dest);reach=vr.verify(dest/'reachability',api)
  require(screen==read_json(root/'vertical-locale-screenshots.json'),'screenshot receipt differs')
  require(reach==read_json(root/'vertical-control-reachability.json'),'native reachability receipt differs')
  images=[];receipts=[];original=root/'app/vertical-locale-evidence'
  for f in sorted(dest.rglob('*')):
   if not f.is_file():continue
   rel=f.relative_to(dest).as_posix();raw=f.read_bytes()
   if original.exists():require(raw==(original/rel).read_bytes(),'original extraction differs '+rel)
   if f.suffix=='.png':
    with Image.open(io.BytesIO(raw)) as im:
     im.load();require(im.format=='PNG' and im.mode in ('RGB','RGBA'),'unsupported full PNG')
     w,h=im.size;require(0<w*h<=16000000 and (w>h)==('-landscape-' in f.name),'decoded screenshot orientation')
     require(len(im.getcolors(256) or [])>1 or im.getcolors(256) is None,'blank screenshot')
     images.append(dict(path=rel,bytes=len(raw),sha256=sha(raw),width=w,height=h,mode=im.mode))
   else:receipts.append(dict(path=rel,sha256=sha(raw),receipt=read_json(f)))
  require(len(images)==len(vm.EXPECTED_SCREENSHOTS)+len(cases)*len(vr.STATES),'source-derived PNG count differs')
  if original.exists():require({f.relative_to(original).as_posix() for f in original.rglob('*') if f.is_file()}=={f.relative_to(dest).as_posix() for f in dest.rglob('*') if f.is_file()},'original extraction inventory differs')
  raw=(root/'logcat.txt').read_bytes();telemetry=parse_save(raw,cases,opens)
  result[str(api)]=dict(status='PASS_BOUNDED_NATIVE_VERTICAL',sdk=api,cases=len(cases),png_count=len(images),transport=transport,screenshot_receipt=screen,reachability_receipt=reach,full_decoded_images=images,case_receipts=receipts,save_telemetry=telemetry,logcat_sha256=sha(raw))
 return dict(status='PASS_BOUNDED_NATIVE_VERTICAL',head=HEAD,tree=TREE,merge=MERGE,run_id=int(RUN),devices=result,limits='Actual source-bound native test receipts and preserved screenshots. Needs separately validated protocols/test-APK provenance and actual visual review. No physical-device, fluent-language or external destination/provider execution claim.')
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for k in ('repo','artifacts','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 p.add_argument('--apis',type=int,nargs='+',choices=(30,35),default=[30,35])
 a=p.parse_args();require(not a.output.exists(),'use a fresh native output directory');a.output.mkdir(parents=True);r=audit(a.repo,a.artifacts,a.output,a.apis);(a.output/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({api:{k:d[k] for k in ('status','cases','png_count')} for api,d in r['devices'].items()},indent=2))
