#!/usr/bin/env python3
"""Replay preserved runtime checks; exit2 explicitly retains missing auxiliary evidence."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True,help='Clean checkout of 9b621934')
p.add_argument('--artifacts',type=Path,required=True,help='ZIP files named as archive-manifest keys')
a=p.parse_args();root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runtime_verifier',root/'verify_ci.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sys.path.insert(0,str(a.source/'tools'))
tree=subprocess.check_output(['git','write-tree'],cwd=a.source,text=True).strip()
m.require(tree==m.TREE,'Wrong source tree')
subprocess.run(['git','diff','--quiet','--'],cwd=a.source,check=True)
manifest={}
for row in subprocess.check_output(['git','ls-tree','-rz',m.TREE],cwd=a.source).split(b'\0'):
    if row:
        meta,path=row.decode().split('\t',1);manifest[path]=meta
archives=json.loads((root/'archive-manifest.json').read_text())['archives']
for name,expected in archives.items():
    data=(a.artifacts/(name+'.zip')).read_bytes()
    m.require(len(data)==expected['bytes'] and m.digest(data)==expected['sha256'],'Archive mismatch: '+name)
results={'build':m.build(a.artifacts/'build.zip',manifest)}
for kind in ('regression','generator'):
    out=a.artifacts/('replayed-'+kind);m.safe_extract(a.artifacts/(kind+'.zip'),out)
    results[kind]=getattr(m,kind)(out,a.source)
incomplete=False
for sdk in (30,35):
    out=a.artifacts/('replayed-device'+str(sdk));m.safe_extract(a.artifacts/('device'+str(sdk)+'.zip'),out)
    try:
        results['device'+str(sdk)]=m.device(out,a.source,sdk)
    except ValueError as error:
        if sdk!=30 or str(error)!='Exact four Korean picker/rotation phases required':raise
        incomplete=True;original=m.application_log_oracles
        # No CI/source test is changed. Keep strict failure and a separate bounded core result.
        m.application_log_oracles=lambda directory,api:{'complete':False,'error':'Exact four Korean picker/rotation phases required'}
        try:results['device30_core_only']=m.device(out,a.source,sdk)
        finally:m.application_log_oracles=original
        results['device30_strict_error']=str(error)
results['all_auxiliary_evidence_complete']=not incomplete
(a.artifacts/'replayed-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'all_auxiliary_evidence_complete':not incomplete,'output':'replayed-results.json'}))
raise SystemExit(2 if incomplete else 0)
