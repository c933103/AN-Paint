#!/usr/bin/env python3
"""Exact current installed artifact-byte and extraction binding only."""
import argparse,pathlib,json,zipfile,hashlib
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,require
def archive_pins():
 b=json.loads((pathlib.Path(__file__).resolve().parent/'artifact-binding.json').read_bytes())
 return {int(api):(v['artifact_id'],v['sha256'],v['job_id']) for api,v in b['emulators'].items()}

def audit(p,apis=(30,35)):
 rows=[]
 pins=archive_pins();require(set(apis)<=set(pins),'required selected artifact pins missing')
 for sdk in apis:
  aid,digest,job=pins[sdk]
  archive=p/f'api{sdk}.zip';root=p/f'api{sdk}'
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
 p=argparse.ArgumentParser();p.add_argument('--artifacts',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--apis',type=int,nargs='+',choices=(30,35),default=[30,35]);a=p.parse_args();r=audit(a.artifacts,a.apis);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
