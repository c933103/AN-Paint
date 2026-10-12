#!/usr/bin/env python3
"""Package bounded immutable inputs; never change original artifacts."""
import argparse,gzip,hashlib,io,json,pathlib,tarfile,zipfile
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,require,sha

def main():
 p=argparse.ArgumentParser();p.add_argument('--artifacts',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();root=a.artifacts;out=a.output;out.mkdir(parents=True,exist_ok=True)
 paths=set();origins={};archives=[]
 for api in (30,35):
  ar=root/f'emulator-api-{api}.zip';arcroot=root/f'emulator-api-{api}'
  with zipfile.ZipFile(ar) as z:
   members=[]
   for n in z.namelist():
    if n.endswith('/'):continue
    b=z.read(n);require(b==(arcroot/n).read_bytes(),'ZIP/extraction differs '+n);entry={'path':n,'bytes':len(b),'sha256':sha(b)};members.append(entry)
    origins[(arcroot/n).relative_to(root).as_posix()]={'archive':ar.name,'member':n}
   archives.append({'name':ar.name,'sha256':sha(ar.read_bytes()),'members':members})
  for summary in arcroot.rglob('summary.json'):
   paths.add(summary)
   paths.update(summary.parent.glob('TEST-*.xml'))
   paths.update(summary.parent/n for n in ('instrumentation.log','install.log') if (summary.parent/n).exists())
  paths.add(root/f'emulator-api-{api}-job.log')
 paths.update((root/'emulator-api-35/app').rglob('*coverage.json'))
 paths.update(root/'emulator-api-35/app/accepted-credit-restart'/n for n in ('boundary.log','verify-status.txt'))
 paths.update(root/n for n in ('emulator-api-35/logcat.txt','source-publication.json','apk-and-source/build/delivery/build-info.json'))
 records=[]
 with (out/'raw-inputs.tar.gz').open('wb') as file:
  with gzip.GzipFile(filename='',mode='wb',fileobj=file,mtime=0,compresslevel=9) as gz:
   with tarfile.open(fileobj=gz,mode='w|',format=tarfile.USTAR_FORMAT) as tar:
    for q in sorted(paths):
     rel=q.relative_to(root).as_posix();raw=q.read_bytes();info=tarfile.TarInfo(rel);info.size=len(raw);info.mode=0o644;info.mtime=0;tar.addfile(info,io.BytesIO(raw));records.append({'path':rel,'bytes':len(raw),'sha256':sha(raw),'origin':origins.get(rel,{'kind':'full job log or supplied publication/build receipt'})})
 b=out/'raw-inputs.tar.gz';manifest={'schema':1,'head':HEAD,'merge':MERGE,'tree':TREE,'run_id':int(RUN),'archive':{'path':b.name,'bytes':b.stat().st_size,'sha256':sha(b.read_bytes())},'file_count':len(records),'expanded_bytes':sum(x['bytes'] for x in records),'files':records,'limitations':'All selected raw inputs remain exact. Original outer emulator/APK/source archives and payloads are omitted; original full archive/payload hash checks are preserved receipts, not rerun by receipt replay.'}
 (out/'RAW-INPUTS.json').write_text(json.dumps(manifest,indent=2)+'\n');(out/'ORIGINAL-ARCHIVE-MEMBERS.json').write_text(json.dumps({'head':HEAD,'tree':TREE,'run_id':int(RUN),'archives':archives},indent=2)+'\n');print(json.dumps({k:v for k,v in manifest.items() if k not in ('files','limitations')},indent=2))
if __name__=='__main__':main()
