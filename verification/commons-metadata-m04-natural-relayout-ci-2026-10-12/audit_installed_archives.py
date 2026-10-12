#!/usr/bin/env python3
"""Exact current installed artifact-byte and extraction binding only."""
import argparse,pathlib,json,zipfile,hashlib
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,require
PINS={30:(11757895416,'33041ec744e46a2943e7f76c8a0465e93dd230f06663a2d4e36028294d0cb198',114885575577),35:(11756584812,'44d9a9033818d91189d6a9c3a9051f8aa83ea6b5714eb790c1f69c931c87993e',114885575693)}
def audit(p):
 rows=[]
 for sdk,(aid,digest,job) in PINS.items():
  archive=p/f'emulator-api-{sdk}.zip';root=p/f'emulator-api-{sdk}'
  require(hashlib.sha256(archive.read_bytes()).hexdigest()==digest,'official digest differs')
  with zipfile.ZipFile(archive) as z:
   names=[n for n in z.namelist() if not n.endswith('/')];require(len(names)==len(set(names)),'duplicate ZIP member')
   for n in names:
    q=pathlib.PurePosixPath(n);require(not q.is_absolute() and '..' not in q.parts and '\\' not in n,'unsafe member')
    require(z.read(n)==(root/n).read_bytes(),'extracted member differs '+n)
   require(set(names)=={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file()},'extraction has missing/extra file')
  rows.append({'sdk':sdk,'artifact_id':aid,'job_id':job,'sha256':digest,'members':len(names)})
 return {'status':'PASS','head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'artifacts':rows,'limit':'Writer supplied official artifact digests and remote provenance; this check authenticates local ZIP/extraction bytes, not installation by itself.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--artifacts',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.artifacts);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
