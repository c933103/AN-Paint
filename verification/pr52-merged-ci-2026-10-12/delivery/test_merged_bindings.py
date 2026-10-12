#!/usr/bin/env python3
"""Small checker-only controls for changed PR52 identity and schema; no app execution."""
import argparse, copy, json, pathlib, tempfile, unittest
import audit_artifact_bindings as artifacts
import audit_build_log as build
CI = None
REPORT = None
class MergedBindingControls(unittest.TestCase):
    def publication(self, key, value):
        d=json.loads((pathlib.Path(__file__).parent/'source-publication.json').read_bytes()); d[key]=value
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t)/'receipt.json'; p.write_text(json.dumps(d))
            with self.assertRaisesRegex(ValueError, 'publication differs: '+key): artifacts.audit(CI,p)
    def log_marker(self, old, new, pattern='ordered build marker missing'):
        raw=(CI/'build-job.log').read_bytes(); self.assertIn(old,raw); changed=raw.replace(old,new)
        expected=build.LOG_SHA
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t)/'log.txt'; p.write_bytes(changed)
            try:
                # Refresh digest only to isolate marker validation from whole-log corruption validation.
                build.LOG_SHA=build.sha(changed)
                with self.assertRaisesRegex(ValueError,pattern): build.audit(p,json.loads((REPORT/'delivery-result.json').read_bytes()))
            finally: build.LOG_SHA=expected
    def test_head_tree_wrong(self): self.publication('head_tree','0'*40)
    def test_head_wrong(self): self.publication('head','0'*40)
    def test_head_parent_order_wrong(self): self.publication('head_parents',['4a35933ff6b6d0013dac8743cc5eeac1c1033e05','71f4d288669858e7975ec4c094b7f47a9a1ff145'])
    def test_merge_parent_order_wrong(self): self.publication('merge_parents',[artifacts.HEAD,'484d1b31cb113c88351e6d0dbdaa0d503e5dd834'])
    def test_stale_base_wrong(self): self.publication('base','71f4d288669858e7975ec4c094b7f47a9a1ff145')
    def test_old_run_wrong(self): self.publication('run_id',38303992927)
    def test_wrong_pr_ref(self): self.log_marker(b'refs/remotes/pull/52/merge',b'refs/remotes/pull/55/merge')
    def test_wrong_checkout_base(self): self.log_marker(b'into 484d1b31cb113c88351e6d0dbdaa0d503e5dd834',b'into 71f4d288669858e7975ec4c094b7f47a9a1ff145')
    def test_missing_compile(self): self.log_marker(b'> Task :Paintroid:compileDebugKotlin',b'> Task :Paintroid:otherTask')
    def test_wrong_artifact_id(self): self.log_marker(b'Artifact ID 11773397420',b'Artifact ID 11771394989')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--ci-root',type=pathlib.Path,required=True);p.add_argument('--report',type=pathlib.Path,required=True)
    a,rest=p.parse_known_args();CI=a.ci_root;REPORT=a.report;unittest.main(argv=[__file__,*rest])
