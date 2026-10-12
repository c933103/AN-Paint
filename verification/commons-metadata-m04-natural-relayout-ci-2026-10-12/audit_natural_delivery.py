#!/usr/bin/env python3
"""Independent read-only PR55 natural-relayout successor archive/probe audit. Never executes archive content."""
import argparse, collections, hashlib, io, json, pathlib, re, subprocess, zipfile
TREE='3dcc1a82f878ad7e0e708cff25ec8d493b88bbc6'
MERGE='de1b934e4786fd041638d00e72e880940328f7a9'
RUN='38269993000'
ZIP_SHA='23d2ad7dc88f7f6272250b2e9bc869bab0047ab061d762e1ec109170fbe8c470'
FONT_SHA='6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006'
OMIT={'.gitignore','colorpicker/.gitignore','.idea/codeStyles/Project.xml'}
NATIVE=('jxl-source','webp-source','heif-source','tiff-source')
def sha(b): return hashlib.sha256(b).hexdigest()
def require(v, message):
    if not v: raise ValueError(message)
def members(z):
    names=z.namelist()
    require(len(names)==len(set(names)), 'duplicate ZIP member')
    for n in names:
        p=pathlib.PurePosixPath(n)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in n, 'unsafe ZIP name '+n)
    return {n for n in names if not n.endswith('/')}
def audit(repo, archive, probes):
    leaves={}
    for row in subprocess.check_output(['git','ls-tree','-rz',TREE],cwd=repo).split(b'\0'):
        if not row: continue
        meta,p=row.split(b'\t'); mode,kind,digest=meta.decode().split()
        require(kind=='blob','nonblob tracked leaf')
        leaves[p.decode()]=(mode,digest)
    def original(p): return subprocess.check_output(['git','show',TREE+':'+p],cwd=repo)
    raw=archive.read_bytes(); require(sha(raw)==ZIP_SHA,'outer artifact hash mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        members(outer)
        apk=outer.read('app/build/outputs/apk/debug/app-debug.apk')
        source=outer.read('build/delivery/AN-Paint-source.zip')
        info=json.loads(outer.read('build/delivery/build-info.json'))
        require(info['commit']==MERGE and str(info['run_id'])==RUN and info['build_variant']=='debug','build provenance')
        require(info['apk_sha256']==sha(apk) and info['source_sha256']==sha(source),'build hash mismatch')
    with zipfile.ZipFile(io.BytesIO(source)) as src:
        names=members(src)
        require(all(n.startswith('AN-Paint/') for n in names),'source ZIP root mismatch')
        paths={n[len('AN-Paint/'):] for n in names}
        require(set(leaves)-paths==OMIT,'unexpected tracked omissions')
        extras=paths-set(leaves)
        require(all(any(p.startswith('Paintroid/build/'+c+'/') for c in NATIVE) for p in extras),'non-native unexpected source')
        matched=[]
        for p in sorted(set(leaves)&paths):
            b=src.read('AN-Paint/'+p)
            digest=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            require(digest==leaves[p][1], 'source blob differs: '+p)
            matched.append(p)
    with zipfile.ZipFile(io.BytesIO(apk)) as az:
        apk_names=members(az)
        require(az.read('assets/local-source/AN-Paint-source.zip')==source, 'embedded source differs')
        font_prefix='Paintroid/src/main/assets/fonts/'
        fonts={p for p in leaves if p.startswith(font_prefix)}
        packaged={n for n in apk_names if n.startswith('assets/fonts/')}
        require(packaged=={'assets/fonts/'+p[len(font_prefix):] for p in fonts},'font path-set differs')
        for p in sorted(fonts):
            require(az.read('assets/fonts/'+p[len(font_prefix):])==original(p),'font asset differs: '+p)
        require(sha(az.read('assets/fonts/anpaintnomui.ttf'))==FONT_SHA, 'font digest')
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
    return {'status':'PASS','merge':MERGE,'tree':TREE,'run_id':RUN,'artifact_sha256':ZIP_SHA,'build_info':info,'tracked_leaves':len(leaves),'exact_source_blobs':len(matched),'omissions':sorted(OMIT),'native_extra_files':len(extras),'font_assets_exact':len(fonts),'font_sha256':FONT_SHA,'embedded_source_exact':True,'probe_summary_sha256':sha((probes/'summary.json').read_bytes()),'probes_checked':checked,'limits':['ZIP native-source extras constrained to existing four native source roots; their upstream content not independently reaudited.','No APK signature/upgrade-key, alignment, ABI, installed execution or pixel rendering claim.','Probe log/source/hash validation checks retained receipts; not an independent toolchain rerun.','Actual run/job conclusion and authenticity depend on parent-verified artifact provenance.']}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--archive',type=pathlib.Path,required=True);p.add_argument('--probes',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
    r=audit(a.repo,a.archive,a.probes);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
