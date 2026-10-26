import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import recompute_actual as r
class Promotion(unittest.TestCase):
 def test_no_promotion_without_actual_evidence(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);a=SimpleNamespace(inputs=p,source_root=p,baseline_source_root=p,actual_evidence=None,actual_manifest_sha256=None,out=p/'out')
   with patch.object(r.source,'compute',return_value={}),self.assertRaises(ValueError):r.run(a)
   self.assertFalse(a.out.exists())
 def test_wrong_actual_manifest_pin_rejected(self):
  p=Path(__file__).resolve().parent/'actual-evidence';e=r.read(p/'coverage-terminal-envelope.json')
  with self.assertRaises(ValueError):r.actual.join_actual(e,p,'0'*64)
if __name__=='__main__':unittest.main()
