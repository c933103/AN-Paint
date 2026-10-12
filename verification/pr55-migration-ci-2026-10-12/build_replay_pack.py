#!/usr/bin/env python3
"""Package bounded raw current-run regression evidence; no APK/tree duplicates."""
import argparse,hashlib,json,pathlib,zipfile
p=argparse.ArgumentParser();p.add_argument('--artifact-root',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
roots=['Paintroid/build/test-results/testDebugUnitTest','Paintroid/build/reports/commons-metadata-m04','Paintroid/build/reports/commons-metadata-m04-diagnostic','Paintroid/build/reports/commons-metadata-m04-painted-ink','build/reports/ci-phases']
files=[]
for directory in roots:
 for f in (a.artifact_root/directory).rglob('*'):
  if f.is_file() and (directory!='Paintroid/build/test-results/testDebugUnitTest' or f.suffix=='.xml'):files.append(f)
files=sorted(set(files));rows=[];target=a.out/'regression-replay-inputs.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in files:
  raw=f.read_bytes();name=str(f.relative_to(a.artifact_root));info=zipfile.ZipInfo(name,(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,raw)
  rows.append({'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
r={'purpose':'Expiry-safe subset of the independently digest-verified original regression artifact; not a replacement claim about the original ZIP','run_id':38279470164,'tree':'592a60877524c5c118695cb45a4d0d5cd257b25a','original_artifact_id':11760918110,'original_artifact_sha256':'572211509c1e72f342d99e4417f1312cb32964dd3decc56222dc9323e49f1c6d','zip_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'zip_bytes':target.stat().st_size,'files':rows,'file_count':len(rows),'uncompressed_bytes':sum(x['bytes'] for x in rows)}
(a.out/'regression-replay-manifest.json').write_text(json.dumps(r,indent=2)+'\n');print(len(rows),'files',r['zip_bytes'],'compressed bytes')
