"""Real published-layout cache boundaries: reject overlap before any write."""
import hashlib,json,os,shutil,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import materialize_position_review_evidence as position
import materialize_gallery_review_evidence as gallery

class ExternalCacheRoots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.here=Path(__file__).resolve().parent
        cls.evidence=Path(os.environ['AN_PAINT_POSITION_EVIDENCE']).resolve()
    def snapshot(self,root):
        result=[]
        for p in sorted(root.rglob('*')):
            rel=p.relative_to(root).as_posix()
            value=('symlink',os.readlink(p)) if p.is_symlink() else ('file',hashlib.sha256(p.read_bytes()).hexdigest()) if p.is_file() else ('dir',)
            result.append((rel,value))
        return result
    def setup(self,root,module):
        data=root/'workspace/repo/verification/translation-entry-review-2026-10-13';data.mkdir(parents=True)
        archive=root/'archive';archive.mkdir()
        index_path=self.here/module.v.INDEX;index=module.v.read(index_path)
        bindings=module.v.evidence_bindings(index) if module is position else index['reports']
        for b in bindings.values():
            p=archive/b['archive_path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(self.evidence/b['path'],p)
        return data,archive,index_path
    def rejects(self,module,kind):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);data,archive,index=self.setup(root,module);repo=data.parents[1]
            paths={'data':data,'data-child':data/'cache','verification':data.parent,'repository':repo,'ancestor':repo.parent,'sibling':repo/'sibling-cache','nested-sibling':repo/'other/subdir/cache','archive':archive,'archive-child':archive/'cache','archive-ancestor':root}
            if kind=='symlink-sibling':
                (repo/'sibling-cache').mkdir();link=root/'alias';link.symlink_to(repo/'sibling-cache',target_is_directory=True);out=link
            elif kind=='symlink-repository':
                link=root/'alias';link.symlink_to(repo,target_is_directory=True);out=link
            else:out=paths[kind]
            before=self.snapshot(root)
            with patch.object(module.v,'HERE',data),self.assertRaisesRegex(ValueError,'must not overlap'):
                # An absent index proves boundary rejection precedes evidence reads/writes.
                module.materialize(archive,out,index_path=root/'index-does-not-exist.json')
            self.assertEqual(self.snapshot(root),before,'Rejected cache path mutated the filesystem')
    def test_repository_root_and_every_ancestor_rejected_without_output(self):
        for module in (position,gallery):
            for kind in ('verification','repository','ancestor'):
                with self.subTest(module=module.__name__,kind=kind):self.rejects(module,kind)
    def test_data_root_and_descendants_rejected_without_output(self):
        for module in (position,gallery):
            for kind in ('data','data-child'):
                with self.subTest(module=module.__name__,kind=kind):self.rejects(module,kind)
    def test_repository_siblings_and_nested_siblings_rejected_without_output(self):
        for module in (position,gallery):
            for kind in ('sibling','nested-sibling'):
                with self.subTest(module=module.__name__,kind=kind):self.rejects(module,kind)
    def test_resolved_symlink_repository_paths_rejected_without_output(self):
        for module in (position,gallery):
            for kind in ('symlink-sibling','symlink-repository'):
                with self.subTest(module=module.__name__,kind=kind):self.rejects(module,kind)
    def test_evidence_checkout_overlap_rejected_without_output(self):
        for module in (position,gallery):
            for kind in ('archive','archive-child','archive-ancestor'):
                with self.subTest(module=module.__name__,kind=kind):self.rejects(module,kind)
    def test_actual_external_sibling_cache_accepts_all_complete_evidence(self):
        for module in (position,gallery):
            with self.subTest(module=module.__name__),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);data,archive,index=self.setup(root,module);out=root/'external-cache'
                with patch.object(module.v,'HERE',data):result=module.materialize(archive,out,index_path=index)
                self.assertEqual(result['status'],'PASS');self.assertTrue(out.is_dir())
                self.assertFalse((data.parents[1]/'position-review-evidence').exists());self.assertFalse((data.parents[1]/'gallery-review-evidence').exists())
    def test_position_materializer_exception_is_exact_not_blanket(self):
        import validate_gallery_reconciliation as v
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);shutil.copytree(self.here,d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','TRANSLATION_PROGRESS.md','new-body.md'))
            shutil.copyfile(v.position.document_path(self.here,'TRANSLATION_PROGRESS.md'),d/'TRANSLATION_PROGRESS.md')
            p=d/'materialize_position_review_evidence.py';p.write_bytes(p.read_bytes()+b'\n# unexpected edit\n')
            with self.assertRaisesRegex(ValueError,'differs beyond exact cache-boundary fix'):
                v.validate(Path(os.environ['AN_PAINT_SOURCE']),Path(os.environ['AN_PAINT_PREVIOUS']),d,self.evidence)

if __name__=='__main__':unittest.main()
