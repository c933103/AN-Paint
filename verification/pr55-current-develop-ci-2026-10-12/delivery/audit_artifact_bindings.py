#!/usr/bin/env python3
"""Recheck retained GitHub artifact ZIPs, complete extractions and metadata for this run."""
import argparse, hashlib, json, pathlib, zipfile
from audit_direction_delivery import require, sha, TREE, HEAD, MERGE, RUN

EXPECTED={
 'apk-and-source':(11767854139,'166167f4a05bf3ce6b0fb7300122fe6f89c85b2210bec24a96a566377a6acc85'),
 'exact-script':(11768517779,'57548245e01888b5cc87fee0310ece493b50649a816bf48edab408405268d794'),
}

def audit(root,publication_path,scopes=None):
    manifest=publication_path.read_bytes();publication=json.loads(manifest)
    for key,value in [('base','71f4d288669858e7975ec4c094b7f47a9a1ff145'),('ordered_parents',['6d603af92ee26d852af62cd1006468ef8472bfcf','484d1b31cb113c88351e6d0dbdaa0d503e5dd834']),('merge_tree',TREE),('merge_parents',['71f4d288669858e7975ec4c094b7f47a9a1ff145',HEAD]),('head',HEAD),('tree',TREE),('merge',MERGE),('run_id',int(RUN))]:
        require(publication[key]==value,'publication differs: '+key)
    require(publication['remote_source_verification']=={'tree':TREE,'leaves':1094,'all_contents_and_modes':True},'coordinator remote source verification receipt differs')
    rows=[]
    for folder in scopes or EXPECTED:
        artifact_id,digest=EXPECTED[folder]
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
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ci-root',type=pathlib.Path,required=True);p.add_argument('--publication',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--scope',choices=tuple(EXPECTED),action='append');a=p.parse_args()
    result=audit(a.ci_root,a.publication,a.scope);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: selected artifact ZIP digests and every extracted file exactly match the retained GitHub metadata and archives.')
if __name__=='__main__':main()
