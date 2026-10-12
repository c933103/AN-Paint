#!/usr/bin/env python3
"""Checker controls for fresh typography publication, artifact and build receipts."""
import argparse,copy,json,pathlib,shutil,tempfile,unittest
from unittest.mock import patch
import audit_artifact_bindings as artifacts
import audit_build_log as build
CI=None
REPORT=None
class PublicationControls(unittest.TestCase):
    def publication(self,key,value):
        p=json.loads((pathlib.Path(__file__).parent/'source-publication.json').read_bytes());p[key]=value
        with self.assertRaisesRegex(ValueError,'publication differs: '+key):artifacts.check_publication(p)
    def test_valid_publication(self):artifacts.check_publication(json.loads((pathlib.Path(__file__).parent/'source-publication.json').read_bytes()))
    def test_wrong_head(self):self.publication('head','0'*40)
    def test_wrong_tree(self):self.publication('head_tree','0'*40)
    def test_wrong_parent(self):self.publication('head_parents',[artifacts.HEAD])
    def test_wrong_merge_tree(self):self.publication('synthetic_merge_tree','0'*40)
    def test_wrong_merge_parents(self):self.publication('synthetic_merge_parents',[artifacts.HEAD,artifacts.BASE])
    def test_wrong_base(self):self.publication('base','0'*40)
    def test_wrong_run(self):self.publication('run_id',38308218307)
    def test_wrong_attempt(self):self.publication('run_attempt',2)
    def test_pending_run(self):self.publication('run_status','in_progress')
    def test_failed_run(self):self.publication('run_conclusion','failure')
    def test_wrong_repository(self):self.publication('repository','c933103/other')
    def test_remote_inventory(self):
        p=json.loads((pathlib.Path(__file__).parent/'source-publication.json').read_bytes());p['remote_verification']['leaves']=1094
        with self.assertRaisesRegex(ValueError,'remote source verification'):artifacts.check_publication(p)
class ArtifactControls(unittest.TestCase):
    def check_mutation(self,change,message):
        with tempfile.TemporaryDirectory() as t:
            root=pathlib.Path(t)
            for n in ('exact-script.zip','exact-script-metadata.json'):shutil.copyfile(CI/n,root/n)
            shutil.copytree(CI/'exact-script',root/'exact-script')
            change(root)
            publication=json.loads((pathlib.Path(__file__).parent/'source-publication.json').read_bytes())
            changed_meta=json.loads((root/'exact-script-metadata.json').read_bytes())
            publication['artifacts']=[changed_meta if row['id']==11778631396 else row for row in publication['artifacts']]
            receipt=root/'publication.json';receipt.write_text(json.dumps(publication))
            with patch.object(artifacts,'PUBLICATION_SHA',artifacts.sha(receipt.read_bytes())):
                with self.assertRaisesRegex(ValueError,message):artifacts.audit(root,receipt,['exact-script'])
    def metadata(self,key,value,message):
        def change(root):
            p=root/'exact-script-metadata.json';d=json.loads(p.read_bytes());d[key]=value;p.write_text(json.dumps(d))
        self.check_mutation(change,message)
    def test_valid_probe_artifact(self):self.assertEqual(artifacts.audit(CI,pathlib.Path(__file__).parent/'source-publication.json',['exact-script'])['status'],'PASS')
    def test_wrong_id(self):self.metadata('id',11773442101,'publication artifact receipt')
    def test_wrong_digest(self):self.metadata('digest','sha256:'+'0'*64,'metadata digest')
    def test_wrong_size(self):self.metadata('size_in_bytes',0,'metadata size')
    def test_wrong_run(self):self.metadata('workflow_run',{'id':1,'head_sha':artifacts.HEAD},'metadata source/run')
    def test_wrong_head(self):self.metadata('workflow_run',{'id':int(artifacts.RUN),'head_sha':'0'*40},'metadata source/run')
    def test_wrong_name(self):self.metadata('name','wrong','artifact name')
    def test_extra_extraction(self):self.check_mutation(lambda root:(root/'exact-script/extra.log').write_text('extra'),'extraction inventory')
    def test_changed_extraction(self):self.check_mutation(lambda root:(root/'exact-script/01-clean.log').write_text('changed'),'extraction content')
    def test_archive_corruption(self):
        def change(root):
            p=root/'exact-script.zip';b=bytearray(p.read_bytes());b[-1]^=1;p.write_bytes(b)
        self.check_mutation(change,'artifact ZIP')
class BuildControls(unittest.TestCase):
    def log_marker(self,old,new,message='ordered build marker missing'):
        raw=(CI/'build-job.log').read_bytes();self.assertIn(old,raw);changed=raw.replace(old,new)
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t)/'log';p.write_bytes(changed)
            with patch.object(build,'LOG_SHA',build.sha(changed)):
                with self.assertRaisesRegex(ValueError,message):build.audit(p,json.loads((REPORT/'delivery-result.json').read_bytes()))
    def test_wrong_pr(self):self.log_marker(b'refs/remotes/pull/52/merge',b'refs/remotes/pull/55/merge')
    def test_wrong_base(self):self.log_marker(('into '+artifacts.BASE).encode(),b'into wrong')
    def test_missing_compile(self):self.log_marker(b'> Task :Paintroid:compileDebugKotlin',b'> Task :Paintroid:otherTask')
    def test_wrong_artifact(self):self.log_marker(b'Artifact ID 11778765976',b'Artifact ID 11773397420')
    def test_failed_build(self):self.log_marker(b'BUILD SUCCESSFUL',b'BUILD SUCCESSFUL\nBUILD FAILED','Gradle failure')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--ci-root',type=pathlib.Path,required=True);p.add_argument('--report',type=pathlib.Path,required=True)
    a,rest=p.parse_known_args();CI=a.ci_root;REPORT=a.report;unittest.main(argv=[__file__,*rest])
