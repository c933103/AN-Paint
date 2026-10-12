#!/usr/bin/env python3
"""Independent read-only PR52 resource-context typography delivery archive/probe audit. Never executes archive content."""
import argparse, collections, hashlib, io, json, pathlib, re, struct, subprocess, zipfile
TREE='cf1ffdb16e4e8401edce81a50b16ad6f21cdcaa8'
MERGE='a73e9482253d9774c14af72951697390d9f0141a'
RUN='38319915849'
ZIP_SHA='1e68d26f4e6f2d159aff4229c20bdcc4b503620d9c6cf0b76ddab2771812b7b4'
FONT_SHA='6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006'
HEAD='ff8553d29a4c135c16b00beadf9cabba1e8d6fae'
ARTIFACT_ID=11778765976
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
    bundler=original('Paintroid/build.gradle').decode()
    declarations=re.findall(r"\[([^\]]+)\]\.each \{ codec ->",bundler)
    declared=[re.findall(r"'([^']+)'",d) for d in declarations if 'jxl-source' in d]
    require(declared==[list(NATIVE)],'current native source roots declaration differs')
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
            require((src.getinfo('AN-Paint/'+p).external_attr>>16 & 0o777)==(int(leaves[p][0],8)&0o777), 'source executable mode differs: '+p)
            matched.append({'path':p,'git_mode':leaves[p][0],'git_blob_sha1':leaves[p][1],'sha256':sha(b),'bytes':len(b),'bundled':True})
        native_roots=[]
        for root in NATIVE:
            root_paths=sorted(p for p in extras if p.startswith('Paintroid/build/'+root+'/'))
            require(root_paths,'declared native source root missing: '+root)
            records=[{'path':p,'sha256':sha(src.read('AN-Paint/'+p)),'mode':oct(src.getinfo('AN-Paint/'+p).external_attr>>16 & 0o777)} for p in root_paths]
            native_roots.append({'root':'Paintroid/build/'+root,'files':len(records),'ordered_path_content_mode_manifest_sha256':sha(json.dumps(records,sort_keys=True,separators=(',',':')).encode())})
    source_manifest=matched+[{'path':p,'git_mode':leaves[p][0],'git_blob_sha1':leaves[p][1],'sha256':sha(original(p)),'bytes':len(original(p)),'bundled':False} for p in sorted(OMIT)]
    source_manifest.sort(key=lambda row:row['path'])
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
        legal_prefix='Paintroid/src/main/assets/legal/'
        legal={p for p in leaves if p.startswith(legal_prefix)}
        require({n for n in apk_names if n.startswith('assets/legal/')}=={'assets/legal/'+p[len(legal_prefix):] for p in legal},'legal asset path-set differs')
        for p in sorted(legal):
            require(az.read('assets/legal/'+p[len(legal_prefix):])==original(p),'legal asset differs: '+p)
        asset_manifest=[{'path':'assets/'+p[len('Paintroid/src/main/assets/'):],'bytes':len(original(p)),'sha256':sha(original(p))} for p in sorted(fonts|legal)]
        inventory=json.loads(az.read('assets/fonts/inventory.json'))
        require(len({r['id'] for r in inventory})==len(inventory),'duplicate font ID')
        require({r['asset'] for r in inventory}=={n[len('assets/'):] for n in packaged if n!='assets/fonts/inventory.json'},'font inventory differs from actual files')
        font_records=[]
        for row in inventory:
            require(sha(az.read('assets/'+row['asset']))==row['sha256'],'font inventory digest mismatch: '+row['id'])
            font_records.append({'id':row['id'],'sha256':row['sha256'],'ui_only':row.get('ui_only',False),'licence_file':row['licence_file'],'individual_notice_present':('assets/'+row['licence_file']) in apk_names})
        fixture=json.loads(original('tools/fixtures/current_localization/nom_current_font_contract.json'))
        dist=fixture['distribution'];norm=lambda x:' '.join(x.split())
        notice=norm(az.read('assets/'+dist['notice']).decode())
        require(len(dist['licence_contracts'])==2,'licence contract inventory')
        for contract in dist['licence_contracts']:
            require(len(contract['required_paragraphs'])=={'MIT':5,'OFL-1.1':21}[contract['licence']],'licence paragraph inventory')
            upstream=norm(az.read('assets/'+contract['source_notice']).decode())
            for paragraph in contract['required_paragraphs']:
                require(norm(paragraph) in notice and norm(paragraph) in upstream,'licence paragraph omitted')
            for attribution in contract.get('source_only_attribution',[]):
                require(norm(attribution) in upstream,'source attribution omitted')
        for path in dist['aggregates']:
            require(notice in norm(az.read('assets/'+path).decode()),'combined notice not in aggregate: '+path)
        for row in fixture['immutable_input_provenance']:
            for field in ('copyright','sha256','git_blob_sha1'):
                if field in row: require(row[field] in notice,'upstream notice provenance omitted: '+field)
        nom_row=next(r for r in inventory if r['id']==fixture['inventory_id'])
        for field in ('name','licence','modified','ui_only'):
            require(nom_row.get(field)==dist[field],'Nom inventory '+field)
        require(nom_row['licence_file']==dist['notice'],'Nom notice path')
        data=az.read('assets/'+fixture['font_asset']);name_table=None
        for i in range(struct.unpack_from('>H',data,4)[0]):
            tag,_,offset,size=struct.unpack_from('>4sIII',data,12+16*i)
            if tag==b'name': name_table=data[offset:offset+size]
        require(name_table is not None,'font name table absent')
        _,count,storage=struct.unpack_from('>HHH',name_table);names={}
        for i in range(count):
            platform,encoding,language,nameid,size,start=struct.unpack_from('>HHHHHH',name_table,6+12*i)
            raw=name_table[storage+start:storage+start+size]
            if platform in (0,3): val=raw.decode('utf-16-be')
            elif platform==1 and encoding==0: val=raw.decode('mac_roman')
            else: continue
            names.setdefault(nameid,set()).add(val)
        for nameid,expected in ((1,dist['name']),(4,dist['name']),(6,dist['postscript_name']),(13,dist['embedded_licence']),(14,dist['embedded_licence_url'])):
            require(names.get(nameid)=={expected},'embedded Nom name/licence mismatch')
        unresolved=[row for row in font_records if not row['individual_notice_present']]
        # Report existing broken metadata references separately; aggregated notices are present.
        aggregated=az.read('assets/legal/FONT_NOTICES.txt').decode()
        for row in inventory:
            require(row['name'] in aggregated,'font attribution absent from aggregate: '+row['id'])
        require(norm(aggregated) in norm(az.read('assets/legal/THIRD_PARTY_NOTICES.txt').decode()),'font aggregate absent from third-party notices')
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
        if label in ('01-clean','06-second-clean'):
            cleaned=[state.strip() for name,state in observed if name==':Paintroid:clean']
            require(len(cleaned)==1 and cleaned[0] in ('','UP-TO-DATE'),label+' clean task receipt')
        if label not in ('01-clean','06-second-clean'):
            gens=[i for i,(name,state) in enumerate(observed) if name==':Paintroid:generateExactScriptResources']
            require(len(gens)==1,label+' generator count')
            require(observed[gens[0]][1].strip()==('UP-TO-DATE' if label=='03-unchanged' else ''),label+' generator state')
            for consumer in tasks:
                if consumer==':Paintroid:generateExactScriptResources': continue
                positions=[i for i,(n,s) in enumerate(observed) if n==consumer]
                require(len(positions)==1 and positions[0]>gens[0], label+' producer ordering')
        require(('generated_sha256' in probe)==(label in ('02-clean-debug-release','04-input-change-and-stale-output','05-restored-input-release','07-release-first-after-clean')),label+' generated receipt presence')
        if 'generated_sha256' in probe:
            wanted=canon+(b'\n<!-- isolated incremental resource probe -->\n' if label=='04-input-change-and-stale-output' else b'')
            require(probe['generated_sha256']=={generated:sha(wanted)},label+' generated hash')
        checked.append({'path':label+'.log','sha256':sha(b)})
    return {'status':'PASS','merge':MERGE,'tree':TREE,'run_id':RUN,'head':HEAD,'artifact_id':ARTIFACT_ID,'artifact_sha256':ZIP_SHA,'source_archive_modes_exact':True,'source_members_manifest':source_manifest,'native_source_roots':native_roots,'font_legal_manifest':asset_manifest,'legal_assets_exact':len(legal),'font_inventory_records':font_records,'nom_mit_ofl_paragraphs_preserved':True,'nom_embedded_names_licence_preserved':True,'unresolved_individual_font_notice_paths':unresolved,'build_info':info,'tracked_leaves':len(leaves),'exact_source_blobs':len(matched),'omissions':sorted(OMIT),'native_extra_files':len(extras),'font_assets_exact':len(fonts),'font_sha256':FONT_SHA,'embedded_source_exact':True,'probe_summary_sha256':sha((probes/'summary.json').read_bytes()),'probes_checked':checked,'limits':['ZIP native-source extras constrained to existing four native source roots; their upstream content not independently reaudited.','No APK signature/upgrade-key, alignment, ABI, installed execution or pixel rendering claim.','Probe log/source/hash validation checks retained receipts; not an independent toolchain rerun.','Actual run/job conclusion and authenticity depend on parent-verified artifact provenance.']}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--archive',type=pathlib.Path,required=True);p.add_argument('--probes',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
    r=audit(a.repo,a.archive,a.probes)
    rows=r.pop('source_members_manifest')
    raw=''.join(json.dumps(row,sort_keys=True,separators=(',',':'))+'\n' for row in rows).encode()
    r['source_members_manifest']={'records':len(rows),'sha256':sha(raw),'encoding':'UTF-8 JSONL; rows sorted by path; JSON keys sorted with compact separators; newline after every row','retained':False,'reconstruction':'audit() derives all records from the current Git tree and actual corresponding-source ZIP; no duplicate full-tree manifest is delivered.','content_mismatches':[],'mode_mismatches':[]}
    for field,filename in [('font_legal_manifest','font-legal-manifest.jsonl')]:
        rows=r.pop(field)
        raw=''.join(json.dumps(row,sort_keys=True,separators=(',',':'))+'\n' for row in rows).encode()
        (a.output.parent/filename).write_bytes(raw)
        r[field]={'file':filename,'sha256':sha(raw),'records':len(rows)}
    a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS: exact corresponding/embedded source, native roots, font/legal assets and retained generation receipts.')
if __name__=='__main__':main()
