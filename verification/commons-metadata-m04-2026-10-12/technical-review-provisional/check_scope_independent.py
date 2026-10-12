#!/usr/bin/env python3
"""Compare M04 exact-delta reversals directly to immutable Git baseline bytes."""
import hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path('/workspace/shared/anpaint-m04-20261012');OUT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from commons_metadata_m04_scope import production_fixture,test_fixture,before_m04_production,before_m04_test
from commons_metadata_m04_font_scope import before_m04_font,before_m04_inventory
sha=lambda b:hashlib.sha256(b).hexdigest()
def base(p):return subprocess.check_output(['git','show','HEAD:'+p],cwd=ROOT)
assert subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,text=True).strip()=='c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1'
rows=[]
for fixture,reverse in [(production_fixture,before_m04_production),(test_fixture,before_m04_test)]:
 for row in fixture()['entries']:
  p=row['path'];actual=(ROOT/p).read_bytes();original=base(p)
  assert reverse(p,actual.decode()).encode()==original,p
  assert sha(original)==row['before_sha256'] and sha(actual)==row['after_sha256'],p
  rows.append(dict(path=p,baseline_sha256=sha(original),current_sha256=sha(actual),exact_reversal_to_git_baseline=True))
p='Paintroid/src/main/assets/fonts/anpaintnomui.ttf';assert before_m04_font((ROOT/p).read_bytes())==base(p)
p='Paintroid/src/main/assets/fonts/inventory.json';assert before_m04_inventory((ROOT/p).read_text()).encode()==base(p)
data=json.loads((ROOT/'verification/commons-metadata-m04-2026-10-12/preserved-baseline.json').read_text())
for p,digest in data['untouched_paths'].items():
 assert sha(base(p))==digest,p
 assert (ROOT/p).read_bytes()==base(p),p
historical=[]
for p in subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD'],cwd=ROOT,text=True).splitlines():
 if p.startswith('verification/') or p.startswith('tools/fixtures/'):
  assert (ROOT/p).read_bytes()==base(p),p
  historical.append(p)
(OUT/'source-scope-independent-check.json').write_text(json.dumps(dict(status='PASS',base_commit='4231edaac45d89c52f51e2b77d0f94a1176ad88c',base_tree=data['base_tree'],production_and_test_deltas=rows,preserved_baseline_paths=len(data['untouched_paths']),historical_evidence_and_fixture_files_unchanged=len(historical),limits='Catalogue and all-language test still pending at this initial review'),indent=2)+'\n')
print((OUT/'source-scope-independent-check.json').read_text())
