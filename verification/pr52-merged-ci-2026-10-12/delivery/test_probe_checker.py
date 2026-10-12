"""Negative controls for this standalone retained-probe reviewer, using disposable receipts."""
import copy, hashlib, json, pathlib, shutil, tempfile, unittest, zipfile
from unittest.mock import patch
import audit_direction_probes as audit

REPO=None
CI=None

class ProbeCheckerTest(unittest.TestCase):
    def mutate_and_check(self, change, expected):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);probes=root/'probes';shutil.copytree(CI/'exact-script-generation',probes)
            summary=json.loads((probes/'summary.json').read_bytes())
            change(summary,probes)
            (probes/'summary.json').write_text(json.dumps(summary))
            archive=root/'probe.zip'
            with zipfile.ZipFile(archive,'w') as z:
                for p in sorted(probes.iterdir()):z.write(p,p.name)
            # Model an independently authenticated archive so deeper semantic
            # controls, rather than the outer hash guard alone, are exercised.
            with patch.object(audit,'ZIP_SHA',audit.sha(archive.read_bytes())):
                with self.assertRaisesRegex(ValueError,expected):audit.audit(REPO,probes,archive)

    def test_valid_current_receipts(self):
        self.assertEqual('PASS',audit.audit(REPO,CI/'exact-script-generation',CI/'exact-script-generation.zip')['status'])

    def test_summary_source_mismatch_rejected(self):
        self.mutate_and_check(lambda s,p:s.update({'tree':'0'*40}),'source/success mismatch')

    def test_extra_unreferenced_member_rejected(self):
        self.mutate_and_check(lambda s,p:(p/'unreferenced.log').write_text('unexpected'),'probe archive member inventory')

    def test_missing_log_member_rejected(self):
        self.mutate_and_check(lambda s,p:(p/'01-clean.log').unlink(),'probe archive member inventory')

    def test_missing_generated_output_rejected(self):
        self.mutate_and_check(lambda s,p:s['probes'][3]['generated_sha256'].clear(),'generated hash')

    def test_wrong_root_build_hash_rejected(self):
        self.mutate_and_check(lambda s,p:s.update({'root_build_sha256':'0'*64}),'build source hash')

    def test_false_success_rejected(self):
        self.mutate_and_check(lambda s,p:s.update({'success':False}),'source/success mismatch')

    def test_wrong_wrapper_hash_rejected(self):
        self.mutate_and_check(lambda s,p:s.update({'wrapper_sha256':'0'*64}),'wrapper source hash')

    def test_missing_clean_task_rejected_even_with_consistent_log_receipts(self):
        def change(s,p):
            probe=s['probes'][0];log=p/(probe['name']+'.log')
            text=audit.re.sub(r'^> Task :Paintroid:clean[^\n]*\n','',log.read_text(),flags=audit.re.M)
            log.write_text(text);probe['log_sha256']=audit.sha(log.read_bytes())
            probe['tasks']=[list(t) for t in audit.re.findall(r'^> Task (:[^\s]+)([^\n]*)$',text,audit.re.M)]
        self.mutate_and_check(change,'clean task receipt')

    def test_missing_generated_receipt_rejected(self):
        self.mutate_and_check(lambda s,p:s['probes'][3].pop('generated_sha256'),'generated receipt presence')

    def test_stale_generated_entry_rejected(self):
        self.mutate_and_check(lambda s,p:s['probes'][3]['generated_sha256'].update({'stale_probe.xml':'0'*64}),'generated hash')

    def test_wrong_generated_content_rejected(self):
        self.mutate_and_check(lambda s,p:s['probes'][3]['generated_sha256'].update({'values-b+ko+Kore+KR+anpaint/strings.xml':'0'*64}),'generated hash')

    def test_missing_probe_rejected(self):
        self.mutate_and_check(lambda s,p:s['probes'].pop(),'probe inventory')

    def test_changed_command_rejected(self):
        self.mutate_and_check(lambda s,p:s['probes'][3]['command'].append('-x'), 'command differs')

    def test_false_log_hash_rejected(self):
        self.mutate_and_check(lambda s,p:s['probes'][3].update({'log_sha256':'0'*64}),'log digest')

    def test_producer_order_rejected_even_with_consistent_log_receipts(self):
        def change(s,p):
            probe=s['probes'][3];log=p/(probe['name']+'.log');text=log.read_text()
            generator='> Task :Paintroid:generateExactScriptResources\n'
            text=text.replace(generator,'').replace('> Task :Paintroid:mergeDebugResources\n','> Task :Paintroid:mergeDebugResources\n'+generator)
            log.write_text(text);probe['log_sha256']=audit.sha(log.read_bytes())
            probe['tasks']=[list(t) for t in audit.re.findall(r'^> Task (:[^\s]+)([^\n]*)$',text,audit.re.M)]
        self.mutate_and_check(change,'producer ordering')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=pathlib.Path,required=True);parser.add_argument('--ci-root',type=pathlib.Path,required=True)
    args,unknown=parser.parse_known_args();REPO=args.repo;CI=args.ci_root
    unittest.main(argv=['test_probe_checker.py',*unknown])
