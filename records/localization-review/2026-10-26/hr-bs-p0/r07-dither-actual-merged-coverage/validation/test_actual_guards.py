import hashlib,json,shutil,tempfile,unittest
from pathlib import Path
import join_actual as j
REAL=Path(__file__).resolve().parents[1]/'postmerge-ci'
PIN='13b1054284417f7130c7d3b6f26288887a90a3bd3a7534b5807f17671920f435'
class ActualGuards(unittest.TestCase):
    def reject(self,name,change):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);manifest=j.read(REAL/'manifest.json')
            for e in manifest['payloads']:shutil.copyfile(REAL/e['path'],root/e['path'])
            p=root/name;d=j.read(p);change(d);p.write_text(json.dumps(d)+'\n')
            for e in manifest['payloads']:
                b=(root/e['path']).read_bytes();e.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
            p=root/'manifest.json';p.write_text(json.dumps(manifest)+'\n');pin=hashlib.sha256(p.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):j.join(root,pin)
    def test_actual_positive(self):self.assertTrue(j.join(REAL,PIN)['all_five_families_verified'])
    def test_wrong_manifest_pin(self):
        with self.assertRaises(ValueError):j.join(REAL,'0'*64)
    def test_PR_event_substitution(self):self.reject('run-terminal.json',lambda d:d.update(event='pull_request'))
    def test_wrong_actual_head(self):self.reject('run-terminal.json',lambda d:d.update(head_sha=j.HEAD))
    def test_incomplete_run(self):self.reject('run-terminal.json',lambda d:d.update(status='in_progress'))
    def test_failed_job(self):self.reject('jobs-terminal.json',lambda d:d['jobs'][0].update(conclusion='failure'))
    def test_missing_artifact_provenance(self):self.reject('artifacts-terminal.json',lambda d:d['artifacts'][0].update(digest='sha256:'+'0'*64))
    def test_prior_PR_tested_commit(self):self.reject('artifact-source-binding.json',lambda d:d.update(tested_commit=j.HEAD))
    def test_source_count(self):self.reject('artifact-source-binding.json',lambda d:d.update(packaged_tracked_source_files_exact=1384))
    def test_unreviewed_scope_upgrade(self):self.reject('compiled-resource-verification.json',lambda d:d.update(current_HR_BS_reviewed_entries=158))
    def test_missing_exact_probe(self):self.reject('exact-script-verification.json',lambda d:d.update(probe_count=12))
    def test_JVM_failure(self):self.reject('hosted-regression-verification.json',lambda d:d['junit_totals'].update(failures=1))
    def test_missing_focused_case(self):self.reject('hosted-regression-verification.json',lambda d:d['focused_suites'][0]['cases'].pop())
    def test_skipped_API_case(self):self.reject('api35-terminal-verification.json',lambda d:d.update(app_source_bound_completed=46))
    def test_wrong_execution_bytes(self):self.reject('api35-terminal-verification.json',lambda d:d['composed_device_identity'].update(apk_sha256='0'*64))
    def test_selection_substitution(self):self.reject('api35-expected-selection.json',lambda d:d.update(workflow_head=j.HEAD))
if __name__=='__main__':unittest.main()
