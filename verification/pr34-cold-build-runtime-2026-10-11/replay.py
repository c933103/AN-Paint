#!/usr/bin/env python3
"""Strictly replay complete620 artifact evidence; no auxiliary fallback."""
import argparse,importlib.util,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--artifacts',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verifier',root/'verify_ci.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);sys.path.insert(0,str(a.source/'tools'))
m.require(subprocess.check_output(['git','write-tree'],cwd=a.source,text=True).strip()==m.TREE,'Wrong source tree');subprocess.run(['git','diff','--quiet'],cwd=a.source,check=True)
manifest={}
for row in subprocess.check_output(['git','ls-tree','-rz',m.TREE],cwd=a.source).split(b'\0'):
 if row:
  meta,path=row.decode().split('\t',1);manifest[path]=meta
for name,e in json.loads((root/'archive-manifest.json').read_text())['archives'].items():
 data=(a.artifacts/(name+'.zip')).read_bytes();m.require(len(data)==e['bytes'] and m.digest(data)==e['sha256'],'Archive mismatch: '+name)
results={'build':m.build(a.artifacts/'build.zip',manifest)}
for kind in ['regression','generator']:
 out=a.artifacts/('replayed-'+kind);m.safe_extract(a.artifacts/(kind+'.zip'),out);results[kind]=getattr(m,kind)(out,a.source)
for sdk in [30,35]:
 out=a.artifacts/('replayed-device'+str(sdk));m.safe_extract(a.artifacts/('device'+str(sdk)+'.zip'),out);results['device'+str(sdk)]=m.device(out,a.source,sdk)
(a.artifacts/'replayed-results.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS: all strict source/runtime/auxiliary checks. Parent actual-pixel review is separately recorded.')
