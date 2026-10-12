#!/usr/bin/env python3
"""Recheck retained GitHub artifact ZIPs, complete extractions and metadata for this run."""
import argparse, hashlib, json, pathlib, zipfile
from audit_migration_delivery import require, sha, TREE, HEAD, MERGE, RUN

EXPECTED={
 'apk-and-source':(11760314237,'a9134a6575b8e61a1b90cf63309b455da1dabeaaa68f6b55faa7bcec63cdf1a8'),
 'exact-script':(11760916005,'dcde889303bb63f0dbdc10006df2148d03e0725d9e7115b019052d5b7ed86d73'),
}

def audit(root):
    manifest=(root/'source-publication.json').read_bytes();publication=json.loads(manifest)
    for key,value in [('head',HEAD),('tree',TREE),('merge',MERGE),('run_id',int(RUN))]:
        require(publication[key]==value,'publication differs: '+key)
    rows=[]
    for folder,(artifact_id,digest) in EXPECTED.items():
        archive=root/(folder+'.zip');record=[r for r in publication['artifacts'] if r['id']==artifact_id]
        require(len(record)==1,'artifact metadata absent/duplicate')
        record=record[0];workflow=record['workflow_run']
        require(record['digest']=='sha256:'+digest,'metadata digest differs')
        require(record['size_in_bytes']==archive.stat().st_size,'metadata size differs')
        require(workflow['id']==int(RUN) and workflow['head_sha']==HEAD,'metadata source/run differs')
        require(record['name']==('exact-script-generation' if folder=='exact-script' else folder)+'-'+MERGE,'artifact name differs')
        require(sha(archive.read_bytes())==digest,'artifact ZIP differs')
        with zipfile.ZipFile(archive) as z:
            names=z.namelist();require(len(names)==len(set(names)),'duplicate ZIP name')
            for name in names:
                p=pathlib.PurePosixPath(name)
                require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,'unsafe member')
            files={n for n in names if not n.endswith('/')}
            require(files=={p.relative_to(root/folder).as_posix() for p in (root/folder).rglob('*') if p.is_file()},'extraction inventory differs')
            members=[]
            for name in sorted(files):
                b=z.read(name);require((root/folder/name).read_bytes()==b,'extraction content differs: '+name)
                members.append({'path':name,'sha256':sha(b),'bytes':len(b)})
        rows.append({'artifact_id':artifact_id,'archive':archive.name,'sha256':digest,'bytes':archive.stat().st_size,'members_exact':members})
    return {'status':'PASS','head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'publication_metadata_sha256':sha(manifest),'artifacts':rows,'limit':'Metadata is the supplied parent-verified GitHub receipt; this offline audit does not independently query GitHub or assert overall run success.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ci-root',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
    result=audit(a.ci_root);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: both expected artifact ZIP digests and every extracted file exactly match the retained GitHub metadata and archives.')
if __name__=='__main__':main()
