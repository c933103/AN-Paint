"""Negative controls only: staged commits must not masquerade as current PR heads."""
from pathlib import Path
from types import SimpleNamespace
import tempfile,json,unittest
import rebind_source_identity as r
ROOT=Path(__file__).resolve().parent
class RebindGuards(unittest.TestCase):
 def test_original_or_malformed_identity_cannot_relabel_preview(self):
  for head,tree in [(r.OLD_HEAD,r.OLD_TREE),('wrong','a'*40),('a'*40,'wrong')]:
   a=SimpleNamespace(head=head,tree=tree)
   with self.subTest(head=head,tree=tree),self.assertRaises(ValueError):r.run(a)
 def test_staged_commit_without_matching_publication_state_does_not_write_inputs(self):
  fixed=ROOT.parent/'fixed-head-tree.json'
  tree='385bd19a6cd68c7b8ce9644f157e4acb4e4cf93e'
  before={n:(ROOT/'inputs'/n).read_bytes() for n in ('identity.json','source-head-tree.json')}
  with tempfile.TemporaryDirectory() as tmp:
   state=Path(tmp)/'synthetic-stale-publication-state.json'
   state.write_text(json.dumps({'head':r.OLD_HEAD,'tree':r.OLD_TREE,'pr':180,'source_base':r.BASE}))
   a=SimpleNamespace(head='6b7cbfceefe66f7a78a46e792f57b49455384e18',tree=tree,tree_file=fixed,source_root=ROOT.parent/'source',publication_state=state)
   with self.assertRaises(ValueError):r.run(a)
  self.assertEqual(before,{n:(ROOT/'inputs'/n).read_bytes() for n in before})
if __name__=='__main__':unittest.main()
