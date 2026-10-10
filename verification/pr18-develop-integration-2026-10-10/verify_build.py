import io,zipfile,json,hashlib,collections
from pathlib import Path
root=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(root/'build.zip') as z:
 info=json.loads(z.read('build/delivery/build-info.json'));apk=z.read('app/build/outputs/apk/debug/app-debug.apk');source=z.read('build/delivery/AN-Paint-source.zip')
 if sha(apk)!=info['apk_sha256'] or sha(source)!=info['source_sha256']:raise ValueError('Build-info digest mismatch')
 if info['commit']!='5c791111d6b29035a59267125d0a6e02e4603e0b' or info['run_id']!='38067267565':raise ValueError('Build identity mismatch')
 with zipfile.ZipFile(io.BytesIO(apk)) as a:
  if a.read('assets/local-source/AN-Paint-source.zip')!=source:raise ValueError('APK embedded source differs')
 manifest=json.loads((root/'composition.json').read_text())['candidate'];seen=set();extra=[];mismatches=[];native=collections.Counter()
 prefixes=tuple('Paintroid/build/'+p+'/' for p in ('jxl-source','webp-source','heif-source','tiff-source'))
 with zipfile.ZipFile(io.BytesIO(source)) as s:
  for n in s.namelist():
   if n.endswith('/'):continue
   p=n.removeprefix('AN-Paint/')
   if p not in manifest:
    if p.startswith(prefixes):native[p.split('/')[2]]+=1
    else:extra.append(p)
    continue
   data=s.read(n);expected=manifest[p].split()[2];actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   if expected!=actual:mismatches.append(p)
   seen.add(p)
  if extra or mismatches:raise ValueError({'extra':extra,'mismatches':mismatches})
 omitted=sorted(set(manifest)-seen)
 expected_omissions=sorted(p for p in manifest if '.idea' in Path(p).parts or Path(p).name=='.gitignore')
 if omitted!=expected_omissions:raise ValueError({'unexpected_omissions':omitted,'expected':expected_omissions})
 result={'run_id':38067267565,'artifact_id':11676230206,'artifact_sha256':sha((root/'build.zip').read_bytes()),'head':'66c6fd8411dd799c2d2ceb9250c1de500346f3f5','executed_merge':info['commit'],'executed_tree':'2ca29f84ce77e8d3be1aa2b7602fa6cca0ca6c31','current_synthetic_merge':'c60c1b79503cebeb4e28bd0b9d9b381aad455fa2','current_synthetic_tree':'2ca29f84ce77e8d3be1aa2b7602fa6cca0ca6c31','build_info':info,'embedded_and_delivered_source_identical':True,'source_blobs_verified':len(seen),'omitted_tracked_paths':omitted,'additional_native_source_entries_by_declared_build_prefix':dict(native),'native_source_note':'Additional source trees are the four prefixes explicitly bundled by Paintroid/build.gradle; their individual upstream blobs are not re-certified by this tracked-source comparison.'}
 (root/'build-receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
