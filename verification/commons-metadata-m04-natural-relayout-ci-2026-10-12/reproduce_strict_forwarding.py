#!/usr/bin/env python3
"""Read-only reproduction of strictness lost only on newly delegated scope paths."""
import argparse,hashlib,json,pathlib,subprocess,sys
TREE='3dcc1a82f878ad7e0e708cff25ec8d493b88bbc6'
BASE='8f9f0d5399f88d173a508e0ce5c96682ca173ed4'
def check(v,m):
 if not v:raise ValueError(m)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
 for name in ('commons_metadata_m04_glyph_bounds_scope.py','commons_metadata_m04_receiver_scope.py'):
  check((a.repo/'tools'/name).read_bytes()==subprocess.check_output(['git','show',TREE+':tools/'+name],cwd=a.repo),'live helper differs from exact current tree')
 sys.path.insert(0,str(a.repo/'tools'));import commons_metadata_m04_glyph_bounds_scope as old;import commons_metadata_m04_receiver_scope as new
 rows=[]
 for path in sorted(new.PATHS-old.PATHS):
  before=subprocess.check_output(['git','show',BASE+':'+path],cwd=a.repo);current=(a.repo/path).read_bytes()
  try:new.before_receiver_fix(path,before,allow_original=False)
  except AssertionError:direct_rejected=True
  else:direct_rejected=False
  try:got=old.before_glyph_bounds(path,before,allow_original=False)
  except AssertionError:delegated_accepts=False
  else:delegated_accepts=got==before
  check(direct_rejected and delegated_accepts,'reported gap did not reproduce '+path)
  check(old.before_glyph_bounds(path,current,allow_original=False)==before,'current endpoint fails strict restoration')
  check(old.before_glyph_bounds(path,before,allow_original=True)==before,'historical idempotence differs')
  try:old.before_glyph_bounds(path,before+b'\n#unrelated\n',allow_original=False)
  except AssertionError:unrelated_rejected=True
  else:unrelated_rejected=False
  rows.append({'path':path,'before_sha256':hashlib.sha256(before).hexdigest(),'current_sha256':hashlib.sha256(current).hexdigest(),'direct_new_scope_rejects_reverted_bytes':direct_rejected,'delegating_old_scope_accepts_reverted_bytes_despite_allow_original_false':delegated_accepts,'unrelated_mutation_rejected':unrelated_rejected})
 check(len(rows)==2,'unexpected delegated path count')
 result={'status':'REPRODUCED_SCOPE_CONTRACT_GAP','head':'04b128889a4ff9159f199d1737bd07d41e22162d','tree':TREE,'review_comment':'https://github.com/c933103/AN-Paint/pull/55#discussion_r4249731672','paths':rows,'bounded_impact':'Only the newly delegated paths lose the explicit strict flag at this wrapper. Direct receiver-scope strict checks and current whole-file endpoint-hash tests still reject exact reverts; this is not proof of a bypass of the entire current host suite or an app rendering defect.','candidate':'Forward allow_original=allow_original in the early path-not-in-PATHS delegation, retain historical in-scope projection behavior, and add wrapper-entry strict revert tests.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
