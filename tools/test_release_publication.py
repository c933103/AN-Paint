import copy
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from release_publication import publish_verified_release, tag_commit

COMMIT='a'*40
OTHER='b'*40
TAG='v0.0.38'
REPO='synthetic/audit'
TITLE='AN Paint 0.0.38'

class State:
    def __init__(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.assets=[]
        for name,data in [('app.apk',b'apk'),('source.zip',b'source'),('verification.json',b'{}'),('SHA256SUMS.txt',b'hashes')]:
            p=self.root/name;p.write_bytes(data);self.assets.append(p)
        self.notes=self.root/'notes.md';self.notes.write_text('Reviewed notes\n')
        self.release=None;self.tag=None;self.uploaded=[];self.commands=[];self.queries=[]
        self.fail=None;self.consume_failure=True;self.partial=1;self.tags={}
    def close(self):self.temp.cleanup()
    def create(self):
        self.release={'id':1,'tag_name':TAG,'target_commitish':COMMIT,'name':TITLE,
                      'body':self.notes.read_bytes().decode('utf-8'),'prerelease':False,'draft':True,
                      'html_url':'https://example.invalid/release'}
    def add(self,p):
        self.uploaded.append({'name':p.name,'size':p.stat().st_size,'state':'uploaded',
                              'digest':'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()})
    def api(self,path):
        self.queries.append(path)
        if '/git/matching-refs/' in path:return [] if self.tag is None else [{'ref':'refs/tags/'+TAG,'object':self.tag}]
        if '/git/tags/' in path:return {'object':self.tags[path.rsplit('/',1)[-1]]}
        if path.endswith('/releases?per_page=100&page=1'):return [] if self.release is None else [copy.deepcopy(self.release)]
        if '/assets?' in path:return copy.deepcopy(self.uploaded)
        raise AssertionError(path)
    def run(self,*args):
        self.commands.append(args)
        command=args[2]
        failure=self.fail
        if self.consume_failure:self.fail=None
        if command=='create':
            if failure=='create_before':raise subprocess.CalledProcessError(1,args)
            self.create()
            if failure=='create_after':raise subprocess.CalledProcessError(1,args)
        elif command=='upload':
            assets=args[6:]
            if failure=='upload_before':raise subprocess.CalledProcessError(1,args)
            for i,p in enumerate(assets):
                self.add(p)
                if failure=='upload_partial' and i+1==self.partial:raise subprocess.CalledProcessError(1,args)
            if failure=='upload_after':raise subprocess.CalledProcessError(1,args)
            if failure=='corrupt_upload':self.uploaded[-1]['digest']='sha256:'+'0'*64
        elif command=='edit':
            if failure=='publish_before':raise subprocess.CalledProcessError(1,args)
            self.release['draft']=False;self.tag={'type':'commit','sha':COMMIT}
            if failure=='publish_after':raise subprocess.CalledProcessError(1,args)
            if failure=='tag_after_publish':self.tag['sha']=OTHER
        else:raise AssertionError(args)
        return ''
    def invoke(self):
        return publish_verified_release(self.api,self.run,repo=REPO,tag=TAG,commit=COMMIT,
                                        title=TITLE,notes_path=self.notes,assets=self.assets)

class RecoveryTests(unittest.TestCase):
    def setUp(self):self.s=State()
    def tearDown(self):self.s.close()
    def test_fresh_success_and_published_rerun_is_read_only(self):
        self.assertEqual(self.s.invoke(),'https://example.invalid/release')
        self.assertFalse(self.s.release['draft']);self.assertEqual(len(self.s.uploaded),4)
        self.s.commands=[];self.s.invoke();self.assertEqual(self.s.commands,[])
    def test_uncertain_create_reconciles_created_draft(self):
        self.s.fail='create_after';self.s.invoke();self.assertFalse(self.s.release['draft'])
        self.assertEqual([c[2] for c in self.s.commands].count('create'),1)
    def test_failed_create_is_not_treated_as_success(self):
        self.s.fail='create_before'
        with self.assertRaises(subprocess.CalledProcessError):self.s.invoke()
        self.assertIsNone(self.s.release)
    def test_partial_upload_is_resumable_without_overwrite(self):
        self.s.create();self.s.fail='upload_partial'
        with self.assertRaises(subprocess.CalledProcessError):self.s.invoke()
        self.assertTrue(self.s.release['draft']);self.assertEqual(len(self.s.uploaded),1)
        self.s.commands=[];self.s.invoke()
        self.assertEqual([c[2] for c in self.s.commands],['upload','edit'])
        self.assertEqual(len(self.s.commands[0][6:]),3);self.assertEqual(len(self.s.uploaded),4)
    def test_uncertain_complete_upload_is_reconciled(self):
        self.s.create();self.s.fail='upload_after';self.s.invoke()
        self.assertFalse(self.s.release['draft']);self.assertEqual(len(self.s.uploaded),4)
    def test_failed_upload_leaves_draft(self):
        self.s.create();self.s.fail='upload_before'
        with self.assertRaises(subprocess.CalledProcessError):self.s.invoke()
        self.assertTrue(self.s.release['draft']);self.assertEqual(self.s.uploaded,[])
    def test_uncertain_successful_publish_is_reconciled(self):
        self.s.create()
        for p in self.s.assets:self.s.add(p)
        self.s.fail='publish_after';self.s.invoke();self.assertFalse(self.s.release['draft'])
    def test_failed_publish_is_resumable(self):
        self.s.create()
        for p in self.s.assets:self.s.add(p)
        self.s.fail='publish_before'
        with self.assertRaises(subprocess.CalledProcessError):self.s.invoke()
        self.assertTrue(self.s.release['draft'])
        self.s.commands=[];self.s.invoke();self.assertEqual([c[2] for c in self.s.commands],['edit'])
    def test_wrong_existing_tag_rejected_before_any_mutation(self):
        self.s.tag={'type':'commit','sha':OTHER}
        with self.assertRaisesRegex(ValueError,'tag'):self.s.invoke()
        self.assertEqual(self.s.commands,[])
    def test_correct_existing_lightweight_and_annotated_tags(self):
        self.s.tag={'type':'tag','sha':OTHER};self.s.tags[OTHER]={'type':'commit','sha':COMMIT}
        self.s.invoke();self.assertFalse(self.s.release['draft'])
    def test_wrong_annotated_target_rejected(self):
        self.s.tag={'type':'tag','sha':'c'*40};self.s.tags['c'*40]={'type':'commit','sha':OTHER}
        with self.assertRaisesRegex(ValueError,'tag'):self.s.invoke()
        self.assertEqual(self.s.commands,[])
    def test_cyclic_noncommit_and_malformed_tags_rejected(self):
        for typ,sha in [('tag',OTHER),('tree',OTHER),('commit','malformed')]:
            with self.subTest(typ=typ):
                self.s.tag={'type':typ,'sha':sha};self.s.tags[OTHER]={'type':'tag','sha':OTHER}
                with self.assertRaises(ValueError):self.s.invoke()
                self.assertEqual(self.s.commands,[])
    def test_changed_tag_after_upload_prevents_publish(self):
        self.s.create();normal=self.s.run
        def changed(*args):
            result=normal(*args)
            if args[2]=='upload':self.s.tag={'type':'commit','sha':OTHER}
            return result
        self.s.run=changed
        with self.assertRaisesRegex(ValueError,'tag'):self.s.invoke()
        self.assertTrue(self.s.release['draft'])
    def test_changed_tag_after_publish_is_not_reported_as_success(self):
        self.s.create()
        for p in self.s.assets:self.s.add(p)
        self.s.fail='tag_after_publish'
        with self.assertRaisesRegex(ValueError,'tag'):self.s.invoke()
    def test_conflicting_release_metadata_rejected_without_mutation(self):
        for key,value in [('target_commitish',OTHER),('name','Other release'),('body','Wrong notes'),('prerelease',True)]:
            self.s.create();self.s.release[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.s.invoke()
            self.assertEqual(self.s.commands,[])
    def test_partial_digest_size_state_or_name_mismatch_rejected(self):
        self.s.create()
        for key,value in [('digest',None),('digest','sha256:'+'0'*64),('size',99),('state','starter'),('name','unrelated')]:
            self.s.uploaded=[];self.s.add(self.s.assets[0]);self.s.uploaded[0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.s.invoke()
            self.assertEqual(self.s.commands,[])
    def test_duplicate_assets_rejected(self):
        self.s.create();self.s.add(self.s.assets[0]);self.s.add(self.s.assets[0])
        with self.assertRaisesRegex(ValueError,'Duplicate'):self.s.invoke()
        self.assertEqual(self.s.commands,[])
    def test_corrupt_upload_does_not_publish(self):
        self.s.create();self.s.fail='corrupt_upload'
        with self.assertRaisesRegex(ValueError,'mismatched'):self.s.invoke()
        self.assertTrue(self.s.release['draft'])
    def test_missing_published_asset_fails_read_only(self):
        self.s.invoke();self.s.commands=[];self.s.uploaded.pop()
        with self.assertRaisesRegex(ValueError,'missing'):self.s.invoke()
        self.assertEqual(self.s.commands,[])
    def test_api_error_is_not_absence(self):
        self.s.api=lambda path:(_ for _ in ()).throw(subprocess.CalledProcessError(1,['gh','api',path]))
        with self.assertRaises(subprocess.CalledProcessError):self.s.invoke()
        self.assertEqual(self.s.commands,[])

    def test_wrong_tag_object_types_fail_without_mutation(self):
        for object_type in ('blob', 'tree', 'unsupported'):
            with self.subTest(object_type=object_type):
                self.s.tag = {'type': object_type, 'sha': COMMIT}
                with self.assertRaises(ValueError):
                    self.s.invoke()
                self.assertEqual(self.s.commands, [])

    def test_api_failure_at_each_read_boundary_is_not_absence(self):
        self.s.create()
        normal = self.s.api
        for boundary in ('matching-refs', '/releases?', '/assets?'):
            def failing(path):
                if boundary in path:
                    raise subprocess.CalledProcessError(1, ['gh', 'api', path])
                return normal(path)
            self.s.api = failing
            with self.subTest(boundary=boundary), self.assertRaises(subprocess.CalledProcessError):
                self.s.invoke()
            self.assertEqual(self.s.commands, [])

    def test_missing_local_input_fails_before_api_or_mutation(self):
        self.s.notes.unlink()
        with self.assertRaises(FileNotFoundError):
            self.s.invoke()
        self.assertEqual(self.s.queries, [])
        self.assertEqual(self.s.commands, [])

    def test_missing_empty_and_partial_asset_receipts_fail_closed(self):
        self.s.create()
        for key, value, remove in [('digest', None, True), ('digest', '', False),
                                   ('state', 'starter', False), ('state', 'uploading', False)]:
            self.s.uploaded = []
            self.s.add(self.s.assets[0])
            if remove:
                del self.s.uploaded[0][key]
            else:
                self.s.uploaded[0][key] = value
            with self.subTest(key=key, value=value, remove=remove), self.assertRaises(ValueError):
                self.s.invoke()
            self.assertEqual(self.s.commands, [])
            self.assertTrue(self.s.release['draft'])

    def test_published_metadata_tag_and_asset_drift_remain_read_only(self):
        self.s.invoke()
        release, tag, uploaded = map(copy.deepcopy, (self.s.release, self.s.tag, self.s.uploaded))
        mutations = [lambda: self.s.release.update(name='Different'),
                     lambda: self.s.release.update(body='Different'),
                     lambda: self.s.release.update(target_commitish=OTHER),
                     lambda: self.s.tag.update(sha=OTHER),
                     lambda: self.s.uploaded[0].update(digest='sha256:' + '0' * 64),
                     lambda: self.s.uploaded[0].update(state='starter')]
        for index, mutate in enumerate(mutations):
            self.s.release, self.s.tag, self.s.uploaded = map(copy.deepcopy, (release, tag, uploaded))
            self.s.commands = []
            mutate()
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.s.invoke()
            self.assertEqual(self.s.commands, [])

    def test_unexpected_extra_asset_fails_without_deletion_or_upload(self):
        self.s.create()
        for path in self.s.assets:
            self.s.add(path)
        unexpected = self.s.root / 'unrelated.txt'
        unexpected.write_bytes(b'keep this unrelated file')
        self.s.add(unexpected)
        with self.assertRaisesRegex(ValueError, 'unexpected'):
            self.s.invoke()
        self.assertEqual(self.s.commands, [])
        self.assertEqual(self.s.uploaded[-1]['name'], 'unrelated.txt')

    def test_crlf_and_empty_notes_are_preserved(self):
        for data in (b'Notes\r\n', b''):
            with self.subTest(data=data):
                self.s.release = None
                self.s.uploaded = []
                self.s.tag = None
                self.s.notes.write_bytes(data)
                self.s.invoke()
                self.assertEqual(self.s.release['body'], data.decode())
                if not data:
                    self.s.release['body'] = None  # GitHub may omit an empty body.
                    self.s.commands = []
                    self.s.invoke()
                    self.assertEqual(self.s.commands, [])

    def test_paginated_release_lookup_finds_matching_draft_on_second_page(self):
        self.s.create()
        normal = self.s.api
        unrelated = [dict(self.s.release, id=i + 2, tag_name='unrelated-' + str(i))
                     for i in range(100)]
        def paginated(path):
            if path.endswith('/releases?per_page=100&page=1'):
                return unrelated
            if path.endswith('/releases?per_page=100&page=2'):
                return [copy.deepcopy(self.s.release)]
            return normal(path)
        self.s.api = paginated
        self.s.invoke()
        self.assertFalse(self.s.release['draft'])
        self.assertNotIn('create', [command[2] for command in self.s.commands])

    def test_prefix_only_tag_does_not_match_requested_tag(self):
        def api(path):
            return [{'ref': 'refs/tags/' + TAG + '-rc1',
                     'object': {'type': 'commit', 'sha': OTHER}}]
        self.assertIsNone(tag_commit(api, REPO, TAG))

    def test_duplicate_release_records_fail_without_mutation(self):
        self.s.create()
        normal = self.s.api
        def duplicate(path):
            if '/releases?' in path:
                return [copy.deepcopy(self.s.release), dict(self.s.release, id=2)]
            return normal(path)
        self.s.api = duplicate
        with self.assertRaisesRegex(ValueError, 'Multiple'):
            self.s.invoke()
        self.assertEqual(self.s.commands, [])

if __name__=='__main__':unittest.main(verbosity=2)
