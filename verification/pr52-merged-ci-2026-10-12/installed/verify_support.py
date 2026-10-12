#!/usr/bin/env python3
"""Verify and safely extract this exact compact current evidence archive."""
import argparse,hashlib,json,pathlib,tarfile
p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();here=pathlib.Path(__file__).resolve().parent;report=json.loads((here/'SUPPORTING-INPUTS.json').read_bytes());archive=here/report['archive']['path'];raw=archive.read_bytes()
def require(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
require(len(raw)==report['archive']['bytes'] and sha(raw)==report['archive']['sha256'],'archive integrity differs');require(not a.output.exists(),'fresh output required');a.output.mkdir(parents=True);pins={x['path']:x for x in report['files']};seen=set()
with tarfile.open(archive) as tar:
 for item in tar:
  q=pathlib.PurePosixPath(item.name);require(item.isfile() and not q.is_absolute() and '..' not in q.parts and '\\' not in item.name,'unsafe member');require(item.name in pins and item.name not in seen,'unexpected/duplicate member');seen.add(item.name);b=tar.extractfile(item).read();expected=pins[item.name];require(item.size==len(b)==expected['bytes'] and sha(b)==expected['sha256'],'member differs');out=a.output/item.name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
require(seen==set(pins),'missing members');print(json.dumps({'status':'PASS_EXACT_SUPPORT_BYTES','kind':report['kind'],'files':len(seen),'selected_apis':report['selected_apis']},indent=2))
