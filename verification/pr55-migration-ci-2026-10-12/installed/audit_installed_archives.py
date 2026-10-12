#!/usr/bin/env python3
"""Exact current installed artifact-byte and extraction binding only."""
import argparse,pathlib,json,zipfile,hashlib
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,require
PINS={30:(11761685563,'19da71039753da8626a80fa85eb31247fe6b72eac2a8a6fbc8e021c66e2f7a84',114915086474),35:(11760988700,'d1c567cb7341e6c56ad3b4d355e04ca7bbad78f1193ae0bb51baa38bcbb2a3bf',114915086555)}
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
