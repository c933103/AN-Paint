#!/usr/bin/env python3
"""Recheck retained GitHub artifact ZIPs, complete extractions and metadata for this run."""
import argparse, hashlib, json, pathlib, zipfile
from audit_direction_delivery import require, sha, TREE, HEAD, MERGE, RUN

EXPECTED={
 'apk-and-source':(11773397420,'8a51ba66aeccd1646556db9fc0af584eb21d6ea1f1fd0b7c3b1ac75d02cc4cfb'),
 'exact-script-generation':(11773442101,'f06e0b59e4fe7d30e3eac3d127a2ba12e38fbcc86298a223bbf53f86ca798e37'),
}

def audit(root,publication_path,scopes=None):
    manifest=publication_path.read_bytes();publication=json.loads(manifest)
    for key,value in [('base','484d1b31cb113c88351e6d0dbdaa0d503e5dd834'),('head_parents',['71f4d288669858e7975ec4c094b7f47a9a1ff145','4a35933ff6b6d0013dac8743cc5eeac1c1033e05']),('merge_tree',TREE),('merge_parents',['484d1b31cb113c88351e6d0dbdaa0d503e5dd834',HEAD]),('head',HEAD),('head_tree',TREE),('merge',MERGE),('run_id',int(RUN)),('repository','c933103/AN-Paint'),('remote_provenance_verified',True)]:
        require(publication[key]==value,'publication differs: '+key)
    run=publication['run']
    require(run['id']==int(RUN) and run['head_sha']==HEAD and run['event']=='pull_request' and run['path']=='.github/workflows/android.yml' and run['run_attempt']==publication['run_attempt']==1, 'nested run binding differs')
    prs=run['pull_requests']
    require(len(prs)==1 and prs[0]['number']==52 and prs[0]['head']['sha']==HEAD and prs[0]['base']['sha']==publication['base'], 'nested PR52 head/base binding differs')
    rows=[]
    for folder in scopes or EXPECTED:
        artifact_id,digest=EXPECTED[folder]
        archive=root/(folder+'.zip');metadata_path=root/(folder+'.metadata.json')
        record=json.loads(metadata_path.read_bytes());require(record['id']==artifact_id,'artifact metadata ID differs')
        workflow=record['workflow_run']
        require(record['digest']=='sha256:'+digest,'metadata digest differs')
        require(record['size_in_bytes']==archive.stat().st_size,'metadata size differs')
        require(workflow['id']==int(RUN) and workflow['head_sha']==HEAD,'metadata source/run differs')
        require(record['name']==('exact-script-generation' if folder=='exact-script-generation' else folder)+'-'+MERGE,'artifact name differs')
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
        rows.append({'artifact_id':artifact_id,'metadata_sha256':sha(metadata_path.read_bytes()),'archive':archive.name,'sha256':digest,'bytes':archive.stat().st_size,'members_exact':members})
    return {'status':'PASS','head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'publication_metadata_sha256':sha(manifest),'artifacts':rows,'limit':'Metadata is the supplied parent-verified GitHub receipt; this offline audit does not independently query GitHub or assert overall run success.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ci-root',type=pathlib.Path,required=True);p.add_argument('--publication',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--scope',choices=tuple(EXPECTED),action='append');a=p.parse_args()
    result=audit(a.ci_root,a.publication,a.scope);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: selected artifact ZIP digests and every extracted file exactly match the retained GitHub metadata and archives.')
if __name__=='__main__':main()
