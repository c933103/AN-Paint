import copy, unittest
from pathlib import Path
from unittest.mock import patch
import recompute_successor as s
ROOT=Path(__file__).resolve().parents[1]
PREVIOUS=ROOT.parent/'hr-bs-p0-20261026'
class SuccessorGuards(unittest.TestCase):
    def mutated(self,suffix,change):
        original=s.read
        def read(p):
            value=original(p)
            if str(p).endswith(suffix):
                value=copy.deepcopy(value);change(value)
            return value
        with patch.object(s,'read',read),self.assertRaises(ValueError):s.compute(ROOT,PREVIOUS)
    def test_positive_complete_source_and_DOM(self):
        d=s.compute(ROOT,PREVIOUS)['coverage-delta.json']
        self.assertEqual((7298,8434),(d['presence_totals']['P0_present'],d['presence_totals']['P0_missing']))
        self.assertEqual((157,214),(d['current_HR_BS_reviewed'],d['current_HR_BS_preserved']))
        self.assertIn('pending',d['actual_postmerge_status'])
    def test_wrong_merge(self):self.mutated('postmerge-ci/merge.json',lambda d:d.update(sha='0'*40))
    def test_wrong_merge_tree(self):self.mutated('postmerge-ci/merge.json',lambda d:d['tree'].update(sha='0'*40))
    def test_reversed_parents(self):self.mutated('postmerge-ci/merge.json',lambda d:d['parents'].reverse())
    def test_wrong_source_tree(self):self.mutated('source-head-tree.json',lambda d:d.update(sha='0'*40))
    def test_truncated_tree(self):self.mutated('source-head-tree.json',lambda d:d.update(truncated=True))
    def test_missing_source_blob(self):self.mutated('source-head-tree.json',lambda d:d['tree'].remove(next(e for e in d['tree'] if e['type']=='blob')))
    def test_corrupt_source_blob_binding(self):self.mutated('source-head-tree.json',lambda d:next(e for e in d['tree'] if e['type']=='blob').update(sha='0'*40))
    def test_wrong_baseline(self):self.mutated('actual-base-tree.json',lambda d:d.update(sha='0'*40))
    def test_changed_delta(self):self.mutated('checks/source-tree-plan.json',lambda d:d['changed'].pop())
    def test_injected_preservation_failure(self):self.mutated('croatian_bosnian_p0_wording.json',lambda d:d['preserved_values']['hr']['ui_brush'].update(value='corrupt'))
    def test_changed_reviewed_pair(self):self.mutated('croatian_bosnian_p0_wording.json',lambda d:d['dither_label_successor'].update(value='corrupt'))
    def test_DOM_disagreement(self):
        with patch.object(s,'dom',return_value=(set(),{})),self.assertRaises(ValueError):s.compute(ROOT,PREVIOUS)
    def test_picker_order(self):self.mutated('baseline/structural-per-locale.json',lambda d:d.reverse())
if __name__=='__main__':unittest.main()
