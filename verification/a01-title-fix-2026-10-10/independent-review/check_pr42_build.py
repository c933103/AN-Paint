from pathlib import Path
import zipfile,hashlib,io,json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'independent-review'
archive=ROOT/'ci-artifacts/pr42-apk-and-source-11666282138.zip'
with zipfile.ZipFile(archive) as z:
 assert len(z.namelist())==len(set(z.namelist()))
 info=json.loads(z.read('build/delivery/build-info.json'))
 apk=z.read('app/build/outputs/apk/debug/app-debug.apk');source=z.read('build/delivery/AN-Paint-source.zip')
 assert info['run_id']=='38041522544' and info['commit']=='424cf44986195bab369b75c472d4ee1168c59e9c'
 assert info['apk_sha256']==hashlib.sha256(apk).hexdigest()
 assert info['source_sha256']==hashlib.sha256(source).hexdigest()
 with zipfile.ZipFile(io.BytesIO(apk)) as a:
  assert len(a.namelist())==len(set(a.namelist()))
  assert a.read('assets/local-source/AN-Paint-source.zip')==source
  abis=sorted(set(p.split('/')[1] for p in a.namelist() if p.startswith('lib/') and p.endswith('.so')))
 with zipfile.ZipFile(io.BytesIO(source)) as s:
  assert len(s.namelist())==len(set(s.namelist()))
  names=set(s.namelist());manifest=json.loads((ROOT/'base-manifest.json').read_text())
  manifest_files={x['path']:x['sha'] for x in manifest['files']}
  candidate=json.loads((ROOT/'evidence/candidate-manifest.json').read_text())
  manifest_files.update({x['path']:x['git_blob_sha'] for x in candidate['files']})
  def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  matched=[];excluded=[];different=[]
  # Exact repository packaging exclusions, rather than silently requiring files omitted by the task.
  for path,expected in manifest_files.items():
   name='AN-Paint/'+path
   if name not in names:excluded.append(path);continue
   actual=blob(s.read(name))
   if actual!=expected:different.append({'path':path,'expected':expected,'actual':actual})
   else:matched.append(path)
  included_generated=[n for n in names if not n.endswith('/') and n.startswith('AN-Paint/') and n[len('AN-Paint/'):] not in manifest_files]
  source_files=[]
  for x in candidate['files']:
   data=s.read('AN-Paint/'+x['path']);assert hashlib.sha256(data).hexdigest()==x['sha256']
   source_files.append({'path':x['path'],'blob':blob(data),'sha256':hashlib.sha256(data).hexdigest()})
  result={'artifact_id':11666282138,'artifact_sha256':hashlib.file_digest(archive.open('rb'),'sha256').hexdigest(),'build_info':info,'embedded_source_identical':True,'apk_abis':abis,'candidate_source_files':source_files,'tracked_source_matched':len(matched),'tracked_source_not_bundled':excluded,'tracked_source_differing':different,'untracked_bundled_file_count':len(included_generated),'untracked_prefix_counts':{}}
  from collections import Counter
  result['untracked_prefix_counts']=dict(Counter('/'.join(n.split('/')[:4]) for n in included_generated))
  assert sorted(excluded)==['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore'],excluded
  assert different==[],different
(OUT/'pr42-build-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
