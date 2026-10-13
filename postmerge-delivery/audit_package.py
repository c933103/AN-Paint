#!/usr/bin/env python3
"""Read-only current PR59 package, local tree, native-source and runtime notice audit."""
import argparse,ast,hashlib,json,pathlib,re,struct,subprocess,zipfile

ROOT=pathlib.Path(__file__).resolve().parent
REPO=None
TREE='5194abcd7521c26b97a3e4bbffec36911272323a'
BASE='cf1ffdb16e4e8401edce81a50b16ad6f21cdcaa8'
DELIVERY=ROOT/'delivery'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,message):
    if not v:raise ValueError(message)
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def source(p):return git('show',TREE+':'+p)
def assignments(script,name):
    nodes=ast.parse(source(script))
    for node in nodes.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError('Missing '+name)

def main():
    require(git('write-tree').decode().strip()==TREE,'staged tree changed')
    tracked={}
    for row in git('ls-tree','-rz',TREE).split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t');mode,kind,oid=meta.decode().split()
        require(kind=='blob','nonblob entry')
        p=path.decode();raw=(REPO/p).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid,'local content differs: '+p)
        require(bool((REPO/p).stat().st_mode&0o111)==(mode=='100755'),'local mode differs: '+p)
        tracked[p]=(mode,oid)
    delta=git('diff','--name-status',BASE,TREE).decode().splitlines()
    apk=DELIVERY/'app/build/outputs/apk/debug/app-debug.apk'
    raw=apk.read_bytes()
    libraries=[]
    expected_abis={'arm64-v8a':(2,183),'armeabi-v7a':(1,40),'x86':(1,3),'x86_64':(2,62)}
    expected_libs={'libanpaint_'+x+'.so' for x in ['heif','jxl','tiff','webp']}
    with zipfile.ZipFile(apk) as z:
        libnames={n for n in z.namelist() if n.startswith('lib/') and n.endswith('.so')}
        require(libnames=={'lib/'+abi+'/'+lib for abi in expected_abis for lib in expected_libs},'native library inventory')
        for n in sorted(libnames):
            data=z.read(n);entry=z.getinfo(n);abi=n.split('/')[1]
            require(data[:4]==b'\x7fELF' and data[5]==1,'unexpected ELF header')
            bits,machine=expected_abis[abi]
            require(data[4]==bits and struct.unpack_from('<H',data,18)[0]==machine,'ELF ABI mismatch: '+n)
            if bits==2:phoff=struct.unpack_from('<Q',data,32)[0];entsize,count=struct.unpack_from('<HH',data,54)
            else:phoff=struct.unpack_from('<I',data,28)[0];entsize,count=struct.unpack_from('<HH',data,42)
            loads=[]
            for i in range(count):
                off=phoff+i*entsize
                if bits==2:p_type,flags,offset,vaddr,paddr,filesz,memsz,align=struct.unpack_from('<IIQQQQQQ',data,off)
                else:p_type,offset,vaddr,paddr,filesz,memsz,flags,align=struct.unpack_from('<IIIIIIII',data,off)
                if p_type==1:
                    require(align>=16384 and offset%16384==vaddr%16384,'ELF LOAD alignment failed: '+n)
                    loads.append({'offset':offset,'virtual_address':vaddr,'alignment':align})
            require(loads,'ELF no LOAD segments: '+n)
            localname,extra=struct.unpack_from('<HH',raw,entry.header_offset+26)
            data_offset=entry.header_offset+30+localname+extra
            require(entry.compress_type==zipfile.ZIP_STORED and data_offset%16384==0,'APK native ZIP alignment failed: '+n)
            libraries.append({'path':n,'bytes':len(data),'sha256':sha(data),'elf_class_bits':64 if bits==2 else 32,'elf_machine':machine,'zip_data_offset':data_offset,'zip_stored':True,'load_segments':loads})
        native_notice=json.loads((DELIVERY/'build/reports/native-runtime-notices.json').read_bytes())
        notice=z.read('assets/legal/NATIVE_RUNTIME_NOTICES.txt')
        require(sha(notice)==native_notice['generated_asset_sha256'],'native notice receipt mismatch')
        require(notice==(DELIVERY/'Paintroid/src/main/assets/legal/NATIVE_RUNTIME_NOTICES.txt').read_bytes(),'separate native notice mismatch')
        legal=z.read('assets/legal/THIRD_PARTY_NOTICES.txt')
        require(legal==(DELIVERY/'Paintroid/src/main/assets/legal/THIRD_PARTY_NOTICES.txt').read_bytes(),'separate third-party notice mismatch')
        require(notice in legal,'native notice aggregate missing')
        deps=json.loads((DELIVERY/'app/build/runtime-dependencies.json').read_bytes())
        coordinates=[':'.join(d[k] for k in ('group','name','version')) for d in deps]
        require(len(coordinates)==len(set(coordinates)),'duplicate dependency inventory')
        require(all(('\n'+c+'\n').encode() in legal for c in coordinates),'runtime component notice missing')
    markers=[]
    with zipfile.ZipFile(DELIVERY/'build/delivery/AN-Paint-source.zip') as z:
        for codec in ('jxl','heif'):
            script='tools/fetch_'+codec+'_sources.py'
            for subdir,repo,rev in assignments(script,'SOURCES'):
                name='AN-Paint/Paintroid/build/'+codec+'-source/'+(subdir+'/' if subdir else '')+'.anpaint-revision'
                require(z.read(name).decode()==rev,'native marker mismatch: '+name)
                markers.append({'codec':codec,'subdirectory':subdir,'repository':repo,'revision':rev})
        rev=assignments('tools/fetch_webp_sources.py','REVISION')
        require(z.read('AN-Paint/Paintroid/build/webp-source/.anpaint-revision').decode()==rev,'webp revision marker')
        markers.append({'codec':'webp','subdirectory':'','repository':'webmproject/libwebp','revision':rev})
        for name,version,url,digest in assignments('tools/fetch_tiff_sources.py','SOURCES'):
            marker='AN-Paint/Paintroid/build/tiff-source/'+name+'/.anpaint-revision'
            require(z.read(marker).decode()==f'{name}-{version} sha256:{digest}\n','TIFF source revision marker: '+name)
            markers.append({'codec':'tiff','subdirectory':name,'version':version,'source_url':url,'archive_sha256':digest})
    signature=(ROOT/'apksigner.log').read_text();badging=(ROOT/'apk-badging.log').read_text()
    cert=re.findall(r'^Signer #1 certificate SHA-256 digest: (\w+)$',signature,re.M)
    require(len(cert)==1 and re.fullmatch(r'[0-9a-f]{64}',cert[0]) and 'Signer #1 certificate DN: C=US, O=Android, CN=Android Debug' in signature,'CI debug certificate identity missing')
    require('Verifies\n' in signature and 'Number of signers: 1' in signature,'signature verification result')
    require('Verified using v1 scheme (JAR signing): true' in signature and 'Verified using v2 scheme (APK Signature Scheme v2): true' in signature,'signature schemes')
    release_cert=re.search(r'^CERT = "([0-9a-f]+)"',source('tools/publish_github_release.py').decode(),re.M)[1]
    require(cert[0]!=release_cert,'unexpected release signer')
    require("package: name='paint.anpaint.android' versionCode='95' versionName='0.0.38'" in badging,'package/version differs')
    require("minSdkVersion:'21'" in badging and "targetSdkVersion:'35'" in badging,'SDK identity differs')
    require('application-debuggable' in badging,'expected debug flag absent')
    result={'status':'PASS_BOUNDED_PACKAGE_AUDIT','tree':TREE,'local_content_and_modes_equal':len(tracked),'source_delta_from_develop':delta,'apk_sha256':sha(raw),'package':'paint.anpaint.android','version_name':'0.0.38','version_code':95,'min_sdk':21,'target_sdk':35,'debuggable':True,'native_libraries':libraries,'four_abis_exact':True,'elf_and_apk_native_16k_alignment_pass':True,'signature':{'schemes_v1_v2_valid':True,'certificate_sha256':cert[0],'ci_debug_identity':True,'matches_existing_upgrade_certificate':False,'release_or_upgrade_delivery':False,'apksigner_warning_count':signature.count('WARNING:')},'source_native_revision_markers':markers,'runtime_dependencies_in_notice':coordinates,'native_runtime_notice_receipt':native_notice,'limits':['CI debug delivery only; the existing private upgrade certificate is different.','Native source revision markers and complete archived bytes were checked; upstream archives were not independently refetched.','This package audit does not execute native libraries, Android UI, installed tests or release publication.',f"Apksigner emits {signature.count('WARNING:')} v1 META-INF metadata warnings; v2 signature verifies and raw warnings are retained."]}
    (ROOT/'package-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: exact local tree, 16 ABI-matching native libraries, ELF and APK 16KB alignment, debug package/signature, source revision markers and runtime notice inventory.')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=pathlib.Path,required=True)
    args=parser.parse_args();REPO=args.repo
    main()
