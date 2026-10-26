#!/usr/bin/env python3
"""Validate downloaded exact-script artifact digest, source pin and all expected exits."""
import argparse,hashlib,json,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);p.add_argument('--commit',required=True);p.add_argument('--tree',required=True);p.add_argument('--reviewed-pr-head',required=True);p.add_argument('--run-id',type=int,required=True);p.add_argument('--artifact-id',type=int,required=True);p.add_argument('--sha256',required=True);a=p.parse_args()
def need(ok,msg):
 if not ok:raise ValueError(msg)
r=a.directory;archive=r/'exact-script.zip';need(hashlib.sha256(archive.read_bytes()).hexdigest()==a.sha256,'archive digest');z=zipfile.ZipFile(archive);names=z.namelist();need(len(names)==len(set(names)),'duplicate member');d=json.loads(z.read('summary.json'));need(d['commit']==a.commit and d['tree']==a.tree and d['success'] is True,'source identity/result');need(len(d['probes'])==len({x['name'] for x in d['probes']})==13,'probe inventory');probes=[]
for probe in d['probes']:
 need(hashlib.sha256(z.read(probe['name']+'.log')).hexdigest()==probe['log_sha256'],'probe log hash');need((probe['exit_code']==0)==probe['expected_success'],'unexpected exit');probes.append({k:probe[k] for k in ['name','exit_code','expected_success','log_sha256']})
need(sum(not x['expected_success'] for x in probes)==1 and next(x for x in probes if not x['expected_success'])['name']=='06-reserved-app-variant-rejected','deliberate negative probe')
out={'schema_version':1,'artifact_id':a.artifact_id,'archive_sha256':a.sha256,'run_id':a.run_id,'reviewed_pr_head':a.reviewed_pr_head,'source_commit':a.commit,'tree':a.tree,'probe_count':13,'all_log_hashes_and_expected_exits_verified':True,'probes':probes,'limits':'Exact-script resource generation only; deliberate reserved-variant rejection is expected. Not language/layout/native-human or release acceptance.'};(r/'exact-script-verification.json').write_text(json.dumps(out,indent=2)+'\n');print('13 exact-script probes and expected negative verified')
