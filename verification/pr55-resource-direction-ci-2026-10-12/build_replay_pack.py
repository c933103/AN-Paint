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
r={'purpose':'Expiry-safe subset of the independently digest-verified original regression artifact; not a replacement claim about the original ZIP','run_id':38285607590,'tree':'ab6f5497e147e81d4c50f4954ea87f364be087aa','original_artifact_id':11764101989,'original_artifact_sha256':'459d6ddd95b4ae8f3126477cf8d45d8c01182bf4b342ddb3f1e77e68abae9e7e','zip_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'zip_bytes':target.stat().st_size,'files':rows,'file_count':len(rows),'uncompressed_bytes':sum(x['bytes'] for x in rows)}
(a.out/'regression-replay-manifest.json').write_text(json.dumps(r,indent=2)+'\n');print(len(rows),'files',r['zip_bytes'],'compressed bytes')
