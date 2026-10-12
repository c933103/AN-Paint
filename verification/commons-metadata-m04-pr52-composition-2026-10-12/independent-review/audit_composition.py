#!/usr/bin/env python3
"""Independent PR52/M04 audit against both immutable Git endpoints, not fixture declarations alone."""
import argparse,hashlib,json,pathlib,subprocess,sys
p=argparse.ArgumentParser(description=__doc__)
for a in ('repo','m04-repo','output'):p.add_argument('--'+a,type=pathlib.Path,required=True)
a=p.parse_args();root=a.repo.resolve();mrepo=a.m04_repo.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
P='71f4d288669858e7975ec4c094b7f47a9a1ff145';M='045004bb23ef762f1731982f7a0152fef0fc5507';D='4231edaac45d89c52f51e2b77d0f94a1176ad88c'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(repo,*args):return subprocess.check_output(['git',*args],cwd=repo)
def at(repo,ref,path):return git(repo,'show',ref+':'+path)
def inventory(repo,ref):
 rows={}
 for record in git(repo,'ls-tree','-rz',ref).split(b'\0'):
  if record:
   head,path=record.split(b'\t',1);mode,kind,blob=head.decode().split();assert kind=='blob';rows[path.decode()]=(mode,blob)
 return rows
assert git(root,'rev-parse',P+'^{tree}').decode().strip()=='815e265af5387111dcdaef66efac5d2091bbb56d'
assert git(mrepo,'rev-parse',M+'^{tree}').decode().strip()=='892e09280be9d668862ae5efada0ada163cc6bdb'
pi=inventory(root,P);mi=inventory(mrepo,M);assert len(pi)==1805 and len(mi)==1694
fraw=(root/'tools/fixtures/commons_metadata_m04_pr52_successor_scope.json').read_bytes();assert sha(fraw)=='479b2a2f4172521ee71e955024a409fe27f2621bde21f32630f6eaee7e05cc4b';f=json.loads(fraw)
def reverse(row,content):
 assert sha(content)==row['after_sha256'],row['path']
 text=content.decode()
 for edit in reversed(row['edits']):
  assert edit['after'] and text.count(edit['after'])==1,row['path']
  text=text.replace(edit['after'],edit['before'],1)
 restored=text.encode();assert sha(restored)==row['before_sha256'],row['path'];return restored
pr={r['path']:r for r in f['pr52_overlaps']};bi={r['path']:r for r in f['binary_overlaps']};un={r['path']:r for r in f['inherited_unchanged_paths']}
assert len(pr)==75 and len(bi)==1 and len(un)==1729
assert not (set(pr)&set(un) or set(pr)&set(bi) or set(un)&set(bi));assert set(pr)|set(bi)|set(un)==set(pi)
sys.path.insert(0,str(root/'tools'))
from commons_metadata_m04_font_scope import before_m04_font
for path,(mode,blob) in pi.items():
 current=(root/path).read_bytes();original=at(root,P,path)
 assert ('100755' if (root/path).stat().st_mode&0o111 else '100644')==mode,path
 if path in un:assert current==original and sha(current)==un[path]['sha256'],path
 elif path in pr:assert reverse(pr[path],current)==original,path
 else:assert before_m04_font(current)==original,path
# Full current byte equality for all historical fixtures and evidence from BOTH producers.
history={}
for name,repo,ref,entries in [('pr52',root,P,pi),('m04',mrepo,M,mi)]:
 checked=[]
 for path in entries:
  if path.startswith(('verification/','tools/fixtures/')):
   assert (root/path).read_bytes()==at(repo,ref,path),(name,path);checked.append(path)
 history[name]=len(checked)
for row in f['immutable_m04_inputs']:
 assert (root/row['path']).read_bytes()==at(mrepo,M,row['path']) and sha((root/row['path']).read_bytes())==row['sha256'],row['path']
for row in f['m04_overlaps']:
 assert reverse(row,(root/row['path']).read_bytes())==at(mrepo,M,row['path']),row['path']
# Resources: strip exactly one immutable M04 line to recover PR52 including C05/M02.
m04_scope=json.loads(at(mrepo,M,'tools/fixtures/commons_metadata_query_failure_scope.json'))
accepted_path='verification/commons-metadata-m04-2026-10-12/linguistic-review/successor-recovered/accepted-and-proposed-values-v4.json'
raw=(root/accepted_path).read_bytes();assert sha(raw)=='00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d';accepted=json.loads(raw)
import translation_catalogues as cat
from test_translations import SCOPED_TAGS
assert len(m04_scope['entries'])==60 and len(accepted)==59 and set(accepted)==SCOPED_TAGS
for row in m04_scope['entries']:
 path=row['path'];text=(root/path).read_text();assert text.count(row['line'])==1
 assert text.replace(row['line'],'',1).encode()==at(root,P,path),path
 actual=cat.read_strings(root/path)['commons_metadata_query_failed']
 assert actual==('Commons metadata query failed' if row['tag']=='default' else accepted[row['tag']]),row['tag']
paths=cat.catalogue_paths();fallback=set(cat.offered_tags())-SCOPED_TAGS;assert len(fallback)==81
for tag in fallback:assert 'commons_metadata_query_failed' not in cat.read_strings(paths[tag]),tag
assert accepted['mnc-Mong'].count('\u180e')==3 and accepted['mn-Mong'].count('\u202f')==3
# Direct independently defined production edits must produce the current source.
prefix='Paintroid/src/main/java/org/catrobat/paintroid/classic/'
path=prefix+'CommonsAttribution.kt';expected=at(root,P,path).decode();anchor='    private const val MAX_RESPONSE = 2 * 1024 * 1024'
expected=expected.replace(anchor,'    /** Application-owned API error presence; keep provider error fields out of UI text. */\n    class QueryFailureException: IOException()\n\n'+anchor,1).replace('if (root.has("error")) throw IOException("Commons metadata query failed")','if (root.has("error")) throw QueryFailureException()',1)
assert expected.encode()==(root/path).read_bytes()
path=prefix+'MediaGalleryActivity.kt';expected=at(root,P,path).decode().replace('        else error.message\n','        else if(error is CommonsAttribution.QueryFailureException) ui(R.string.commons_metadata_query_failed)\n        else error.message\n',1);assert expected.encode()==(root/path).read_bytes()
# Accepted PR52 Korean HTTP oracle plus the immutable standalone M04 query successor.
path='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsCopyCreditErrorTest.kt'
expected=at(mrepo,M,path).decode().replace('이미지 크레딧을 複寫할 수 없습니다: Commons metadata: HTTP 503','이미지 크레딧을 複寫할 수 없습니다: Commons 메타데이터: HTTP 503')
assert expected.encode()==(root/path).read_bytes()
# Every other standalone M04 flow assertion and the exact 59-entry Kotlin map remain fixed.
path='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
expected=at(mrepo,M,path).decode().replace('catch(error: IOException) {assertFalse(error is CommonsAttribution.QueryFailureException);assertEquals("Commons metadata: HTTP 503",error.message)}','catch(error: CommonsAttribution.HttpException) {assertEquals(503,error.status);assertNull(error.message)}',1)
assert expected.encode()==(root/path).read_bytes()
path='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureTranslationTest.kt'
assert (root/path).read_bytes()==at(mrepo,M,path)
# Check the claimed entire changed/new source inventory against real Git and local bytes.
sp=root/'verification/commons-metadata-m04-pr52-composition-2026-10-12/source-manifest.json';assert sha(sp.read_bytes())=='d23ba36229197b1a2d90849f6cc89a53d7c156de2707756456c088201c2591bc';claimed=json.loads(sp.read_text())['files'];assert len(claimed)==91
candidate=set(git(root,'ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0'))-{''}
changed=set()
for path in candidate:
 if path.startswith('verification/'):continue
 raw=(root/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 if path not in pi or blob!=pi[path][1]:changed.add(path)
assert changed=={r['path'] for r in claimed}
expected_new={'Paintroid/src/test/java/org/catrobat/paintroid/local/'+n for n in ['CommonsMetadataQueryFailureFlowTest.kt','CommonsMetadataQueryFailureTranslationTest.kt']}|{'tools/'+n for n in ['commons_metadata_m04_composition_scope.py','commons_metadata_m04_font_scope.py','commons_metadata_m04_scope.py','extend_nom_m04_ui_font.py','test_commons_metadata_m04.py','test_commons_metadata_m04_composition.py','test_commons_metadata_m04_font.py','verify_nom_m04_renderer.py']}|{'tools/fixtures/'+n for n in ['commons_metadata_m04_font_scope.json','commons_metadata_m04_pr52_successor_scope.json','commons_metadata_m04_production_scope.json','commons_metadata_m04_test_scope.json','commons_metadata_query_failure_scope.json']}
assert changed-set(pi)==expected_new
for path in expected_new:assert not (root/path).stat().st_mode&0o111,path
fresh_diff=git(root,'diff','--binary',P,'--',*[row['path'] for row in claimed])
assert sha(fresh_diff)=='d29ba081d5c98af5128c3654da7277cb87fcc6ca8378764cfece5eec413faa90'
assert fresh_diff==(root/'verification/commons-metadata-m04-pr52-composition-2026-10-12/source-vs-pr52.diff').read_bytes()
for row in claimed:
 raw=(root/row['path']).read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'];assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob']
result=dict(status='PASS',pr52_commit=P,m04_checkpoint=M,pr52_leaves=len(pi),pr52_exact_unchanged=len(un),pr52_exact_text_reversals=len(pr),pr52_exact_font_reversals=len(bi),m04_exact_reverse_endpoints=len(f['m04_overlaps']),immutable_m04_inputs=len(f['immutable_m04_inputs']),historical_fixture_and_evidence_files=history,catalogues=60,fixed_values=59,open_fallbacks=81,source_paths_changed_or_added=91,source_manifest_sha256=sha(sp.read_bytes()),production_edits_independently_reconstructed=True,korean_http_oracle_preserved=True,script_controls_preserved=True,limits='Source and fixture proof; Android execution remains separate')
(out/'independent-composition-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
