from pathlib import Path
import json,tempfile,shutil,unittest
import recompute_coverage as c
R=Path(__file__).resolve().parent
class Guards(unittest.TestCase):
 def reject(self,filename,mutate):
  with tempfile.TemporaryDirectory() as t:
   i=Path(t)/'inputs';shutil.copytree(R/'inputs',i);p=i/filename;d=json.loads(p.read_text());mutate(d);p.write_text(json.dumps(d))
   with self.assertRaises(ValueError):c.compute(i,R.parent/'source',R.parent/'base-source')
 def test_baseline_not_relabelled(self):self.reject('baseline/manifest.json',lambda d:d.update(source_commit=c.HEAD))
 def test_baseline_rows_not_recounted(self):self.reject('baseline/structural-per-locale.json',lambda d:d[0].update(P0_present=92))
 def test_approved_scope_not_expanded(self):self.reject('approved-manifest.json',lambda d:d.update(preserved_values=216))
 def test_review_not_expanded(self):self.reject('review/hr-review.json',lambda d:d['entries'].append(d['entries'][0]))
 def test_source_tree_not_substituted(self):self.reject('source-head-tree.json',lambda d:d.update(sha=c.BASE_TREE))
 def test_context_not_substituted(self):self.reject('review/shared-source-context.json',lambda d:d.update(source_commit=c.HEAD))
 def test_source_safe_paths(self):
  for p in ['../out','/tmp/out','a\\b']:
   with self.assertRaises(ValueError):c.safe(R,p)
if __name__=='__main__':unittest.main()
