#!/usr/bin/env python3
"""Preserve bounded fresh regression inputs, including corrected notice captures."""
import argparse,hashlib,json,pathlib,zipfile
p=argparse.ArgumentParser();p.add_argument('--artifact-root',type=pathlib.Path,required=True);p.add_argument('--binding',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args();binding=json.loads(a.binding.read_text())
roots=['Paintroid/build/test-results/testDebugUnitTest','Paintroid/build/reports/commons-metadata-m04','Paintroid/build/reports/commons-metadata-m04-diagnostic','Paintroid/build/reports/commons-metadata-m04-painted-ink','build/reports/ci-phases'];files=[]
for directory in roots:
 for f in (a.artifact_root/directory).rglob('*'):
  if f.is_file() and (directory!='Paintroid/build/test-results/testDebugUnitTest' or f.suffix=='.xml'):files.append(f)
files.extend(f for f in (a.artifact_root/'Paintroid/build/reports/localized-dialog-layout').glob('*retained-vertical*') if f.is_file())
files=sorted(set(files));rows=[];target=a.out/'regression-replay-inputs.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in files:
  raw=f.read_bytes();name=str(f.relative_to(a.artifact_root));info=zipfile.ZipInfo(name,(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,raw)
  rows.append({'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
r={'purpose':'Expiry-safe subset of independently digest-verified fresh regression artifact. No APK or full source-tree duplication.','run_id':binding['run_id'],'tree':binding['tree'],'original_artifact_id':binding['regression_artifact_id'],'original_artifact_sha256':binding['regression_artifact_sha256'],'zip_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'zip_bytes':target.stat().st_size,'files':rows,'file_count':len(rows),'uncompressed_bytes':sum(x['bytes'] for x in rows)}
(a.out/'regression-replay-manifest.json').write_text(json.dumps(r,indent=2)+'\n');print(len(rows),'files',r['zip_bytes'],'compressed bytes')
