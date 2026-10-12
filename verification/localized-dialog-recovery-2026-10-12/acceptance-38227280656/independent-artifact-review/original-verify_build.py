if not __debug__:
 raise RuntimeError('Acceptance verification requires ordinary Python; optimized mode is rejected')
import hashlib,io,json,zipfile
from pathlib import Path
R=Path(__file__).parent;sha=lambda b:hashlib.sha256(b).hexdigest();blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();manifest=json.load(open(R/'publication-manifest.json'))
z=zipfile.ZipFile(R/'candidate-build.zip');names=z.namelist();assert len(names)==len(set(names))
def unique(suffix):
 found=[n for n in names if n.endswith(suffix)];assert len(found)==1,(suffix,found);return found[0]
info=json.loads(z.read(unique('build-info.json')));apk=z.read(unique('app-debug.apk'));source=z.read(unique('AN-Paint-source.zip'))
assert info['commit']=='f008d110f83cb6390db941b9177062edb8ea212c';assert info['run_id']=='38227280656';assert info['build_variant']=='debug';assert info['apk_sha256']==sha(apk);assert info['source_sha256']==sha(source)
with zipfile.ZipFile(io.BytesIO(apk)) as az:
 assert az.read('assets/local-source/AN-Paint-source.zip')==source
 fonts=[p for p in (R/'checkout/Paintroid/src/main/assets/fonts').glob('*') if p.is_file()];assert len(fonts)==14
 for p in fonts:
  assert az.read('assets/fonts/'+p.name)==p.read_bytes(),p.name
with zipfile.ZipFile(io.BytesIO(source)) as sz:
 snames=sz.namelist();assert len(snames)==len(set(snames));expected=set();omissions=[]
 for e in manifest['leaves']:
  name='AN-Paint/'+e['path'];expected.add(name)
  if name not in snames:
   assert e['path'] in {'.gitignore','colorpicker/.gitignore','.idea/codeStyles/Project.xml'},e['path'];omissions.append(e['path'])
  else:assert blob(sz.read(name))==e['sha'],e['path']
 extras=[n for n in snames if not n.endswith('/') and n not in expected];prefixes=['AN-Paint/Paintroid/build/'+n+'/' for n in ['jxl-source','webp-source','heif-source','tiff-source']];assert all(any(n.startswith(p) for p in prefixes) for n in extras)
result=dict(head='71f4d288669858e7975ec4c094b7f47a9a1ff145',ci_merge=info['commit'],tree=manifest['tree'],run_id=38227280656,artifact_zip_sha256=sha((R/'candidate-build.zip').read_bytes()),apk_sha256=sha(apk),source_sha256=sha(source),embedded_source_equals_sidecar=True,remote_tracked_blobs_matched=len(expected)-len(omissions),archive_exclusions=omissions,extra_native_source_counts={p:sum(n.startswith(p) for n in extras) for p in prefixes},all_14_font_assets_match_develop=True,signing=info['signing'],build_variant=info['build_variant'],limit='Debug APK/source/font identity; no release or upgrade-signing claim.')
(R/'candidate-build-info.json').write_text(json.dumps(info,indent=2)+'\n');(R/'candidate-build-verification.json').write_text(json.dumps(result,indent=2)+'\n');(R/'candidate-app-debug.apk').write_bytes(apk);print(json.dumps(result,indent=2))
