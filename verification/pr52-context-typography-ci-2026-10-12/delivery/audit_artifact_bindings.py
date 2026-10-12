#!/usr/bin/env python3
"""Recheck every member of both retained artifact ZIPs against extraction and metadata."""
import argparse,json,pathlib,zipfile
from audit_direction_delivery import require,sha,TREE,HEAD,MERGE,RUN
BASE='484d1b31cb113c88351e6d0dbdaa0d503e5dd834'
PARENT='eb7451d320ba56e1ece6b1b55797da653966051d'
PUBLICATION_SHA='7ee33eb8674bf6d2bf9eff17bb2d2cb4b82e8b36af4e88b815d4b8851d496989'
EXPECTED={'apk-and-source':(11778765976,'1e68d26f4e6f2d159aff4229c20bdcc4b503620d9c6cf0b76ddab2771812b7b4','apk-and-source'), 'exact-script':(11778631396,'4bc45ce05cb5c4a680e5ca31c5fd9c0bb03725160b9aa24f24f9a1be2fc7bfb1','exact-script-generation')}
def check_publication(publication):
    wanted={'schema':1,'repository':'c933103/AN-Paint','head':HEAD,'head_tree':TREE,'head_parents':[PARENT],'base':BASE,'synthetic_merge':MERGE,'synthetic_merge_tree':TREE,'synthetic_merge_parents':[BASE,HEAD],'run_id':int(RUN),'run_attempt':1,'run_status':'completed','run_conclusion':'success','run_url':'https://github.com/c933103/AN-Paint/actions/runs/'+RUN}
    for k,v in wanted.items():require(publication[k]==v,'publication differs: '+k)
    require(publication['remote_verification']=={'tree':TREE,'leaves':1095,'all_content_modes_equal':True},'remote source verification differs')
def audit(root,publication_path,scopes=None):
    raw=publication_path.read_bytes();require(sha(raw)==PUBLICATION_SHA,'frozen publication digest differs');publication=json.loads(raw);check_publication(publication);rows=[]
    jobs=publication['jobs'];require(len(jobs)==5 and len({j['id'] for j in jobs})==5 and all(j['run_id']==int(RUN) and j['status']=='completed' and j['conclusion']=='success' for j in jobs),'terminal job receipts differ')
    selected_jobs=[j for j in jobs if j['id'] in (115045254696,115045254981)]
    require({(j['id'],j['name']) for j in selected_jobs}=={(115045254696,'Build APK and corresponding source'),(115045254981,'Exact-script resource generation')},'build/probe job identity differs')
    for folder in scopes or EXPECTED:
        artifact_id,digest,artifact_name=EXPECTED[folder]
        archive=root/(folder+'.zip');metadata=root/(folder+'-metadata.json');record=json.loads(metadata.read_bytes())
        matches=[r for r in publication['artifacts'] if r['id']==artifact_id];require(matches==[record],'publication artifact receipt differs')
        require(record['id']==artifact_id,'artifact metadata ID differs')
        require(record['digest']=='sha256:'+digest,'metadata digest differs')
        require(record['size_in_bytes']==archive.stat().st_size,'metadata size differs')
        require(record['expired'] is False,'artifact expired at supplied receipt')
        run=record['workflow_run'];require(run['id']==int(RUN) and run['head_sha']==HEAD,'metadata source/run differs')
        require(record['name']==artifact_name+'-'+MERGE,'artifact name differs')
        require(sha(archive.read_bytes())==digest,'artifact ZIP differs')
        with zipfile.ZipFile(archive) as z:
            names=z.namelist();require(len(names)==len(set(names)),'duplicate ZIP name')
            for name in names:
                p=pathlib.PurePosixPath(name);require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,'unsafe member')
            files={n for n in names if not n.endswith('/')};extracted=root/folder
            require(not any(p.is_symlink() for p in extracted.rglob('*')),'extracted symlink')
            require(files=={p.relative_to(extracted).as_posix() for p in extracted.rglob('*') if p.is_file()},'extraction inventory differs')
            members=[]
            for name in sorted(files):
                data=z.read(name);require((extracted/name).read_bytes()==data,'extraction content differs: '+name)
                members.append({'path':name,'sha256':sha(data),'bytes':len(data)})
        rows.append({'artifact_id':artifact_id,'metadata_sha256':sha(metadata.read_bytes()),'archive':archive.name,'sha256':digest,'bytes':archive.stat().st_size,'members_exact':members})
    return {'status':'PASS','head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'run_attempt':1,'publication_metadata_sha256':sha(raw),'artifacts':rows,'parent_reported_terminal_jobs':[{'id':j['id'],'name':j['name'],'status':j['status'],'conclusion':j['conclusion']} for j in jobs],'selected_build_probe_jobs':[j['id'] for j in selected_jobs],'limits':['Offline binding to parent-verified GitHub receipts; remote GitHub was not independently queried.','Terminal success is from the supplied parent-verified receipt; this audit independently reviews only delivery/probe/build inputs. Regression and installed acceptance are separate.']}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('ci-root','publication','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
    p.add_argument('--scope',choices=tuple(EXPECTED),action='append');a=p.parse_args()
    result=audit(a.ci_root,a.publication,a.scope);a.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS: both artifacts, all ZIP/extracted members and source/run metadata bind exactly.')
