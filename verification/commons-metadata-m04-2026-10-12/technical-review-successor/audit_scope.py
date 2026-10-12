#!/usr/bin/env python3
"""Independent complete-M04 scope audit against explicit immutable Git base and accepted values."""
import argparse,hashlib,json,pathlib,subprocess,sys,unicodedata
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=pathlib.Path,required=True)
p.add_argument('--accepted',type=pathlib.Path,required=True)
p.add_argument('--frozen',type=pathlib.Path,required=True)
p.add_argument('--output',type=pathlib.Path,required=True)
a=p.parse_args();root=a.repo.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
BASE='4231edaac45d89c52f51e2b77d0f94a1176ad88c';TREE='c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*cmd):return subprocess.check_output(['git',*cmd],cwd=root)
def base(path):return git('show',BASE+':'+path)
assert git('rev-parse',BASE+'^{tree}').decode().strip()==TREE
accepted_raw=a.accepted.read_bytes();assert sha(accepted_raw)=='00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d'
accepted=json.loads(accepted_raw);assert len(accepted)==59
sys.path.insert(0,str(root/'tools'))
import translation_catalogues as cat
from test_translations import SCOPED_TAGS
from commons_metadata_m04_scope import catalogue_fixture,production_fixture,test_fixture,before_m04_catalogue,before_m04_production,before_m04_test
from commons_metadata_m04_font_scope import before_m04_font,before_m04_inventory
assert set(accepted)==SCOPED_TAGS
allowed=set();rows=[]
for fixture,reverse in [(catalogue_fixture,before_m04_catalogue),(production_fixture,before_m04_production),(test_fixture,before_m04_test)]:
 for row in fixture()['entries']:
  path=row['path'];raw=(root/path).read_bytes();old=base(path)
  assert reverse(path,raw.decode()).encode()==old,path
  assert sha(raw)==row['after_sha256'] and sha(old)==row['before_sha256'],path
  allowed.add(path);rows.append(dict(path=path,baseline_sha256=sha(old),current_sha256=sha(raw)))
entries=catalogue_fixture()['entries'];assert len(entries)==60
assert {r['tag'] for r in entries}=={'default'}|SCOPED_TAGS
controls={}
for row in entries:
 value=cat.read_strings(root/row['path'])['commons_metadata_query_failed']
 assert value==('Commons metadata query failed' if row['tag']=='default' else accepted[row['tag']]),row['tag']
 assert cat.placeholders(value)=={} and not cat.android_string_errors(value) and not cat.format_string_errors(value)
 controls[row['tag']]=[dict(index=i,codepoint=f'U+{ord(c):04X}',name=unicodedata.name(c,'UNNAMED'),category=unicodedata.category(c)) for i,c in enumerate(value) if unicodedata.category(c).startswith('C') or 0x180B<=ord(c)<=0x180F or 0xFE00<=ord(c)<=0xFE0F or ord(c)==0x202F]
assert accepted['mnc-Mong'].count('\u180e')==3
assert accepted['mn-Mong'].count('\u202f')==3
paths=cat.catalogue_paths();offered=set(cat.offered_tags());assert len(offered)==140 and len(offered-SCOPED_TAGS)==81
for tag in offered-SCOPED_TAGS:assert 'commons_metadata_query_failed' not in cat.read_strings(paths[tag]),tag
font='Paintroid/src/main/assets/fonts/anpaintnomui.ttf';inventory='Paintroid/src/main/assets/fonts/inventory.json'
assert before_m04_font((root/font).read_bytes())==base(font);assert before_m04_inventory((root/inventory).read_text()).encode()==base(inventory)
allowed.update((font,inventory))
adapters=['tools/'+s for s in ['test_commons_copy_credit_errors.py','test_commons_metadata_m03.py','test_commons_metadata_m03_font.py','test_locale_font_coverage.py','test_svg_error_translations.py','test_tiff_c023_wording.py']]
for path in adapters:
 assert (root/path).read_bytes()==(a.frozen/path).read_bytes(),path
allowed.update(adapters)
baseline_paths=git('ls-tree','-r','--name-only',BASE).decode().splitlines();unchanged=[];changed=[]
for path in baseline_paths:
 raw=(root/path).read_bytes();old=base(path)
 if raw!=old:
  assert path in allowed,('Unexpected baseline change',path)
  changed.append(path)
 else:unchanged.append(path)
assert set(changed)==allowed,('Missing/unexpected changed paths',set(changed)^allowed)
assert len(changed)==71
preserved=json.loads((root/'verification/commons-metadata-m04-2026-10-12/preserved-baseline.json').read_text())
for path,digest in preserved['untouched_paths'].items():assert sha(base(path))==digest==sha((root/path).read_bytes()),path
historical=[p for p in baseline_paths if p.startswith(('verification/','tools/fixtures/'))]
assert all(path in unchanged for path in historical)
# Compare the recovered original reviewer evidence bytes, never overwrite it.
old_review='verification/commons-metadata-m04-2026-10-12/technical-review-provisional'
for file in (a.frozen/old_review).rglob('*'):
 if file.is_file():assert file.read_bytes()==(root/old_review/file.relative_to(a.frozen/old_review)).read_bytes()
# Source binding excludes generated verification reports to avoid recursive report hashes.
manifest=[]
candidate_paths=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0'))-{''}
new_source={path for path in candidate_paths-set(baseline_paths) if not path.startswith('verification/')}
expected_new={'Paintroid/src/test/java/org/catrobat/paintroid/local/'+n for n in ['CommonsMetadataQueryFailureFlowTest.kt','CommonsMetadataQueryFailureTranslationTest.kt']}|{'tools/'+n for n in ['commons_metadata_m04_scope.py','commons_metadata_m04_font_scope.py','extend_nom_m04_ui_font.py','test_commons_metadata_m04.py','test_commons_metadata_m04_font.py','verify_nom_m04_renderer.py']}|{'tools/fixtures/'+n for n in ['commons_metadata_m04_font_scope.json','commons_metadata_m04_production_scope.json','commons_metadata_m04_test_scope.json','commons_metadata_query_failure_scope.json']}
assert new_source==expected_new,('Unexpected new source files',new_source^expected_new)
for record in git('ls-tree','-rz',BASE).split(b'\0'):
 if not record:continue
 head,path=record.split(b'\t',1);mode,kind,digest=head.decode().split();path=path.decode()
 assert kind=='blob' and mode in ('100644','100755'),path
 assert bool((root/path).stat().st_mode & 0o111)==(mode=='100755'),('Mode changed',path)
for path in sorted(candidate_paths):
 if path.startswith('verification/'):continue
 f=root/path
 if f.is_file():
  raw=f.read_bytes();manifest.append(dict(path=path,mode='100755' if f.stat().st_mode & 0o111 else '100644',bytes=len(raw),sha256=sha(raw),git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()))
result=dict(status='PASS',base_commit=BASE,base_tree=TREE,accepted_values_sha256=sha(accepted_raw),explicit_catalogues=60,scoped_languages=59,open_fallbacks=81,baseline_files=len(baseline_paths),unchanged_baseline_files=len(unchanged),changed_baseline_files=len(changed),new_source_files=len(new_source),preserved_paths=len(preserved['untouched_paths']),historical_files_unchanged=len(historical),deltas=rows,script_controls=controls,limits='Technical resource/source scope only; Android execution and language acceptance are separate')
(out/'scope-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(out/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('deltas','script_controls')},indent=2))
