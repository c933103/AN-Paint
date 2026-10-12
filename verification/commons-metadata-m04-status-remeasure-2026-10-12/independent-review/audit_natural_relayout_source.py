#!/usr/bin/env python3
"""Independent successor byte/mode audit; no project imports. Requires immutable base Git tree."""
import argparse, hashlib, json, pathlib, re, subprocess
BASE='8f9f0d5399f88d173a508e0ce5c96682ca173ed4'
FLOW='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
DEVICE='app/src/androidTest/java/paint/anpaint/android/GalleryViewportDeviceTest.kt'
FIXTURE='tools/fixtures/commons_metadata_m04_receiver_successor_scope.json'
MODIFIED={
 'Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt',FLOW,DEVICE,
 'tools/commons_metadata_m04_glyph_bounds_scope.py','tools/test_commons_metadata_m04_glyph_bounds.py'}
def sha(data): return hashlib.sha256(data).hexdigest()
def check(value,message):
 if not value: raise ValueError(message)
def methods(text):
 return re.findall(r'@Test\b(?:(?!\bfun\b).)*\bfun\s+(\w+)\s*\(',text,re.S)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True)
 p.add_argument('--reviewed-manifest',type=pathlib.Path,required=True)
 p.add_argument('--manifest-sha256',required=True);p.add_argument('--output',type=pathlib.Path,required=True)
 a=p.parse_args();repo=a.repo
 manifest_raw=a.reviewed_manifest.read_bytes();check(sha(manifest_raw)==a.manifest_sha256,'unreviewed manifest')
 manifest=json.loads(manifest_raw);check(manifest['base_tree']==BASE,'manifest base differs')
 def git(*args): return subprocess.check_output(['git',*args],cwd=repo)
 old={}
 for row in git('ls-tree','-rz',BASE).split(b'\0'):
  if not row: continue
  meta,path=row.split(b'\t');mode,kind,blob=meta.decode().split()
  check(kind=='blob','unexpected nonblob');old[path.decode()]=(mode,blob)
 check(len(old)==2117,'wrong baseline inventory')
 changed=[];unchanged=[]
 for path,(mode,blob) in old.items():
  f=repo/path;check(f.is_file() and not f.is_symlink(),'missing/nonregular baseline '+path)
  check(bool(f.stat().st_mode&0o111)==(mode=='100755'),'baseline mode changed '+path)
  raw=f.read_bytes();actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  (unchanged if actual==blob else changed).append(path)
 check(set(changed)==MODIFIED,'unexpected modified baseline scope: '+str(changed))
 source=manifest['source_files'];check(len(source)==len({r['path'] for r in source}),'duplicate manifest source')
 for row in source:
  raw=(repo/row['path']).read_bytes()
  check(bool((repo/row['path']).stat().st_mode&0o111)==(row['mode']=='100755'),'unreviewed source mode '+row['path'])
  check(sha(raw)==row['sha256'] and len(raw)==row['bytes'],'unreviewed current source '+row['path'])
 check(MODIFIED <= {r['path'] for r in source},'manifest omits a modified baseline')
 fixture_raw=(repo/FIXTURE).read_bytes();scope=json.loads(fixture_raw)
 check(scope['base_tree']==BASE and scope['failed_run']==38263619232,'fixture base/count differs')
 check(len(scope['entries'])==len(MODIFIED) and {r['path'] for r in scope['entries']}==MODIFIED,'inverse scope differs')
 helper=(repo/'tools/commons_metadata_m04_receiver_scope.py').read_text()
 check(re.search(r"SCOPE_PIN = '([0-9a-f]{64})'",helper)[1]==sha(fixture_raw),'fixture pin differs')
 endpoints=[]
 for row in scope['entries']:
  path=row['path'];before=git('show',BASE+':'+path);now=(repo/path).read_bytes()
  check(sha(before)==row['before_sha256'] and sha(now)==row['after_sha256'],'endpoint mismatch '+path)
  restored=now.decode()
  for edit in reversed(row['edits']):
   check(edit['after'] and restored.count(edit['after'])==1,'ambiguous inverse '+path)
   restored=restored.replace(edit['after'],edit['before'],1)
  check(restored.encode()==before,'inverse differs from immutable Git endpoint '+path)
  replay=before.decode()
  for edit in row['edits']:
   check(edit['before'] and replay.count(edit['before'])==1,'ambiguous forward '+path)
   replay=replay.replace(edit['before'],edit['after'],1)
  check(replay.encode()==now,'forward differs from reviewed source '+path)
  endpoints.append({'path':path,'before_sha256':sha(before),'after_sha256':sha(now),'bidirectional_edits':len(row['edits'])})
 for path,count in ((FLOW,18),(DEVICE,1)):
  original=methods(git('show',BASE+':'+path).decode());current=methods((repo/path).read_text())
  check(original==current and len(current)==count,'test identities changed '+path)
 paths=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0'))-{''}
 added=sorted(paths-set(old));newsource={p for p in added if not p.startswith('verification/')}
 check(newsource==set(manifest['new_source_paths']),'unreviewed new source scope: '+str(newsource))
 check(newsource<= {r['path'] for r in source},'manifest omits new source')
 check(all(any(p.startswith(prefix) for prefix in manifest['allowed_new_evidence_roots']) for p in added if p.startswith('verification/')),'unreviewed new evidence root')
 result={'status':'PASS','base_tree':BASE,'baseline_leaves':len(old),'unchanged_leaves':len(unchanged),
  'modified_leaves':len(changed),'bidirectional_exact_endpoints':endpoints,'new_source_paths':sorted(newsource),'new_evidence_paths_not_content_reviewed_here':[p for p in added if p.startswith('verification/')],
  'reviewed_manifest_sha256':sha(manifest_raw),'source_binding':source,'flow_test_methods':18,'installed_gallery_test_methods':1,
  'all_old_fonts_catalogues_fixtures_and_verification_bytes':'unchanged; all existing baseline mode bits unchanged',
  'limits':['This byte-level check does not execute Kotlin, Android, lint, or installed rendering.',
   'Source exactness does not establish measured-margin convergence or pixel containment on a device.']}
 a.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['source_binding','bidirectional_exact_endpoints']},indent=2))
if __name__=='__main__':main()
