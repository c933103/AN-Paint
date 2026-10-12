#!/usr/bin/env python3
"""Independent retained-probe audit for the exact PR55 natural-relayout successor."""
import argparse,hashlib,json,pathlib,re,subprocess,zipfile
TREE='3dcc1a82f878ad7e0e708cff25ec8d493b88bbc6'
MERGE='de1b934e4786fd041638d00e72e880940328f7a9'
ZIP_SHA='afc79f2dc266251cc9713ebd902f418f0adb43dc2252872c363609593d4613eb'
RUN='38269993000'
ARTIFACT_ID='11756348317'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,msg):
    if not v:raise ValueError(msg)
def audit(repo,probes,archive):
    require(not ZIP_SHA.startswith('PENDING'),'Actual exact-script artifact digest pending')
    require(sha(archive.read_bytes())==ZIP_SHA,'exact-script ZIP digest mismatch')
    with zipfile.ZipFile(archive) as z:
        names=[n for n in z.namelist() if not n.endswith('/')]
        require(len(names)==len(set(names)),'duplicate probe ZIP path')
        require(set(names)=={p.name for p in probes.iterdir() if p.is_file()},'extracted probe inventory differs')
        for n in names:
            require(pathlib.PurePosixPath(n).name==n,'unexpected probe path')
            require(z.read(n)==(probes/n).read_bytes(),'probe extraction differs '+n)
    def original(p):return subprocess.check_output(['git','show',TREE+':'+p],cwd=repo)
    summary=json.loads((probes/'summary.json').read_bytes())
    require(summary['commit']==MERGE and summary['tree']==TREE and summary['success'] is True,'probe source/success mismatch')
    require(summary['excluded_task']==':Paintroid:bundleCorrespondingSource','unexpected excluded probe task')
    require(summary['wrapper_sha256']==sha(original('gradle/wrapper/gradle-wrapper.properties')),'wrapper source hash')
    require(summary['root_build_sha256']==sha(original('build.gradle')),'build source hash')
    expected=[('01-clean',[':Paintroid:clean']),('02-clean-debug-release',[':Paintroid:mergeDebugResources',':Paintroid:mergeReleaseResources']),('03-unchanged',[':Paintroid:generateExactScriptResources']),('04-input-change-and-stale-output',[':Paintroid:mergeDebugResources']),('05-restored-input-release',[':Paintroid:mergeReleaseResources']),('06-second-clean',[':Paintroid:clean']),('07-release-first-after-clean',[':Paintroid:mergeReleaseResources'])]
    require([p['name'] for p in summary['probes']]==[p[0] for p in expected], 'probe inventory')
    canon=original('Paintroid/src/main/res/values-b+ko+Kore+KR/strings.xml')
    generated='values-b+ko+Kore+KR+anpaint/strings.xml'
    checked=[]
    for (label,tasks),probe in zip(expected,summary['probes']):
        b=(probes/(label+'.log')).read_bytes(); log=b.decode()
        require(sha(b)==probe['log_sha256'],label+' log digest')
        require(probe['exit_code']==0 and 'BUILD SUCCESSFUL' in log and 'BUILD FAILED' not in log,label+' build unsuccessful')
        command=['bash','gradlew','--no-daemon','--max-workers=2','--parallel','--console=plain','-PnativeAbis=x86_64','-x',':Paintroid:bundleCorrespondingSource',*tasks]
        require(probe['command']==command,label+' command differs')
        observed=[list(t) for t in re.findall(r'^> Task (:[^\s]+)([^\n]*)$',log,re.M)]
        require(observed==probe['tasks'],label+' task receipt differs')
        if label not in ('01-clean','06-second-clean'):
            gens=[i for i,(name,state) in enumerate(observed) if name==':Paintroid:generateExactScriptResources']
            require(len(gens)==1,label+' generator count')
            require(observed[gens[0]][1].strip()==('UP-TO-DATE' if label=='03-unchanged' else ''),label+' generator state')
            for consumer in tasks:
                if consumer==':Paintroid:generateExactScriptResources': continue
                positions=[i for i,(n,s) in enumerate(observed) if n==consumer]
                require(len(positions)==1 and positions[0]>gens[0], label+' producer ordering')
        if 'generated_sha256' in probe:
            wanted=canon+(b'\n<!-- isolated incremental resource probe -->\n' if label=='04-input-change-and-stale-output' else b'')
            require(probe['generated_sha256']=={generated:sha(wanted)},label+' generated hash')
        checked.append({'path':label+'.log','sha256':sha(b)})
    return {'status':'PASS','merge':MERGE,'tree':TREE,'run_id':int(RUN),'artifact_id':int(ARTIFACT_ID),'artifact_sha256':ZIP_SHA,'artifact_digest_provenance':'Parent supplied GitHub digest; reviewer independently matched the ZIP digest, every extracted member, retained logs and exact source.', 'probes_checked':checked,'summary_sha256':sha((probes/'summary.json').read_bytes()),'limitation':'Retained real toolchain receipt/source/log verification, not a fresh Gradle execution or installed rendering claim.'}
def main():
    p=argparse.ArgumentParser()
    for key in ('repo','probes','artifact','output'):p.add_argument('--'+key,type=pathlib.Path,required=True)
    a=p.parse_args();r=audit(a.repo,a.probes,a.artifact);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
