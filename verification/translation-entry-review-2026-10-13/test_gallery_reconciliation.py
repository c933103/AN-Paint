"""Current merged-gallery source, exact full-review and immutable-history negative controls."""
import copy
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
import validate_gallery_reconciliation as v

class GalleryGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory=v.HERE;cls.source=Path(os.environ['AN_PAINT_SOURCE']);cls.previous=Path(os.environ['AN_PAINT_PREVIOUS']);cls.evidence=v.position.evidence_location(cls.directory)
        cls.index=v.read(cls.directory/v.INDEX);cls.receipts=v.read(cls.directory/'entry-review-receipts.json');cls.ids=v.read(cls.directory/'source-identities.json');cls.counts=v.read(cls.directory/'entry-review-counts.json');cls.fixture=v.read(cls.directory/v.FIXTURE)
        cls.docs=v.check_reports(cls.evidence,cls.index);cls.report=cls.docs['complete-statement-review.json'];cls.en=v.values(cls.source/'Paintroid/src/main/res/values/strings.xml');cls.cats={r['tag']:v.values(cls.source/r['catalogue_path']) for r in cls.counts['languages']}
    def copied(self,d):
        shutil.copytree(self.directory,d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','TRANSLATION_PROGRESS.md','new-body.md'))
        # The checkout publishes progress at its root, not beside the data JSON.
        # Flat mutation fixtures are normalized explicitly; repository fixtures
        # retain the real root placement. A PR draft body is never a checkout input.
        root_layout=d.name=='translation-entry-review-2026-10-13' and d.parent.name=='verification'
        progress=(d.parents[1] if root_layout else d)/'TRANSLATION_PROGRESS.md'
        progress.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(v.position.document_path(self.directory,'TRANSLATION_PROGRESS.md'),progress)
    def new_receipts(self,r):return v.check_new_receipts(r,self.index,self.en,self.cats,self.report)
    def test_current_source_and_exact_previous_checkpoint(self):
        for previous in (None,self.previous):
            result=v.validate(self.source,previous,evidence_root=self.evidence)
            self.assertEqual((result['new_reviewed_current'],result['new_open_idiom_reviews']),(54,5));self.assertEqual(result['summary']['reviewed_current'],3386)
    def test_original_entrypoint_dispatches_to_new_current_gates(self):
        self.assertEqual(v.position.legacy.validate(self.source,self.previous)['new_open_idiom_reviews'],5)
    def test_historical_strict_functions_are_unchanged(self):
        import ast
        name='validate_merged_assembly_reconciliation.py'
        functions=lambda p:{x.name:ast.dump(x) for x in ast.parse(p.read_text()).body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name!='validate'}
        self.assertEqual(functions(self.directory/name),functions(self.previous/name))
    def test_exact_all_59_full_statements_and_limits(self):
        v.check_review_documents(self.docs,self.index)
        self.assertEqual({p['tag'] for p in self.index['complete_pairs'] if p['state']=='needs_rereview'},v.OPEN)
        self.assertEqual(self.index['original_limits'],self.report['limits'])
    def test_full_statement_identity_value_conclusion_and_confidence_required(self):
        p=self.index['complete_pairs'][0];entry=v.position.resolve_pointer(self.report,p['pointer'])
        for field in ('tag','catalogue','text','text_sha256','full_statement_review','disposition','reviewer_confidence'):
            e=copy.deepcopy(entry);e[field]='changed'
            with self.subTest(field=field),self.assertRaises(ValueError):v.check_statement(p,e,self.report)
        source=copy.deepcopy(self.report);source['source']='A browser is missing.'
        with self.assertRaises(ValueError):v.check_statement(p,entry,source)
    def test_native_or_runtime_claims_cannot_be_promoted(self):
        p=self.index['complete_pairs'][0];e=v.position.resolve_pointer(self.report,p['pointer'])
        for field in ('native_speaker_certification','runtime_ui_verification'):
            bad=copy.deepcopy(e);bad[field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):v.check_statement(p,bad,self.report)
    def test_five_equal_hash_idiom_holds_cannot_gain_current_credit(self):
        for tag in v.OPEN:
            r=copy.deepcopy(self.receipts);entry=next(x for x in r['receipts'] if x['cohort']==v.COHORT and x['tag']==tag)
            self.assertEqual(entry['reviewed_localized_sha256'],entry['current_localized_sha256'])
            entry['state']='reviewed_current';entry.pop('finding_status')
            with self.subTest(tag=tag),self.assertRaises(ValueError):self.new_receipts(r)
    def test_other_disclosed_limits_and_confidence_are_preserved(self):
        for tag in ('ceb','bo','mn-Mong'):
            for field in ('original_review_disposition','idiom_limits_preserved','reviewer_confidence','review_conclusion_sha256'):
                r=copy.deepcopy(self.receipts);entry=next(x for x in r['receipts'] if x['cohort']==v.COHORT and x['tag']==tag);entry.pop(field)
                with self.subTest(tag=tag,field=field),self.assertRaises(ValueError):self.new_receipts(r)
    def test_layout_conventions_stay_separate(self):
        for tag in ('en-XV','qaa-Zsye-XV'):
            p=copy.deepcopy(next(p for p in self.index['complete_pairs'] if p['tag']==tag));p['test_convention']=False
            with self.subTest(tag=tag),self.assertRaises(ValueError):v.check_statement(p,v.position.resolve_pointer(self.report,p['pointer']),self.report)
    def test_new_receipt_missing_duplicate_or_fallback_identity_rejected(self):
        for mutation in ('missing','duplicate','fallback'):
            r=copy.deepcopy(self.receipts)
            if mutation=='missing':r['receipts'].pop()
            elif mutation=='duplicate':r['receipts'][-1]=copy.deepcopy(r['receipts'][-2])
            else:r['receipts'][-1]['tag']='am'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):self.new_receipts(r)
    def test_new_receipt_scope_hashes_and_urls_required(self):
        for field in ('source','independent_review_source','review_scope','complete_value_review','reviewed_english_utf8_sha256','current_localized_sha256','review_pointer','complete_review_report_sha256','whole_language_certification'):
            r=copy.deepcopy(self.receipts);r['receipts'][-1][field]='changed'
            with self.subTest(field=field),self.assertRaises(ValueError):self.new_receipts(r)
    def test_every_prior_receipt_cohort_history_and_partial_record_preserved(self):
        for field in ('receipts','cohorts','superseded_receipts','partial_reviews'):
            r=copy.deepcopy(self.receipts)
            if field=='cohorts':r[field][next(k for k in r[field] if k!=v.COHORT)]['scope']='changed'
            else:r[field][0]['source']='changed'
            with self.subTest(field=field),self.assertRaises(ValueError):v.check_preservation(r,self.ids,self.previous)
    def test_four_processing_holds_stay_open(self):
        for tag in ('ms','id','ja','zh-HK'):
            r=copy.deepcopy(self.receipts);e=next(x for x in r['receipts'] if x['tag']==tag and x['key']=='string/ui_rendering_images');e['state']='reviewed_current';e.pop('finding_status',None)
            with self.subTest(tag=tag),self.assertRaises(ValueError):v.check_preservation(r,self.ids)
    def test_prior_source_context_metadata_cannot_be_promoted(self):
        ids=copy.deepcopy(self.ids);ids['previous_resource_manifest_at_gallery_merge']['source_revision']=v.REV
        with self.assertRaises(ValueError):v.check_preservation(self.receipts,ids)
    def test_index_missing_pointer_limit_or_mutable_ref_rejected(self):
        for mutation in ('missing','duplicate','pointer','limit','revision'):
            index=copy.deepcopy(self.index)
            if mutation=='missing':index['complete_pairs'].pop()
            elif mutation=='duplicate':index['complete_pairs'][-1]=index['complete_pairs'][0]
            elif mutation=='pointer':index['complete_pairs'][0]['pointer']='/entries/1'
            elif mutation=='limit':index['original_limits']=[]
            else:index['reports']['complete-statement-review.json']['durable_revision']='main'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):v.check_reports(self.evidence,index)
    def test_missing_or_corrupt_external_gallery_artifacts_fail(self):
        for name,b in self.index['reports'].items():
            for mutation in ('missing','bytes'):
                with self.subTest(name=name,mutation=mutation),tempfile.TemporaryDirectory() as tmp:
                    d=Path(tmp);shutil.copytree(self.evidence/'gallery-review-evidence',d/'gallery-review-evidence');p=d/b['path']
                    if mutation=='missing':
                        p.unlink()
                        with self.assertRaises(FileNotFoundError):v.check_reports(d,self.index)
                    else:
                        p.write_bytes(p.read_bytes()+b' ')
                        with self.assertRaises(ValueError):v.check_reports(d,self.index)
    def test_original_source_binding_and_test_scope_are_not_rewritten(self):
        for name,field,value in [('source-binding.json','default_text','wrong'),('source-binding.json','all_59_bindings',[]),('sdk-fixture-correction.json','expected_corrected_tree','bad'),('hosted-verification.json','tested_tree','bad')]:
            docs=copy.deepcopy(self.docs);docs[name][field]=value
            with self.subTest(name=name,field=field),self.assertRaises(ValueError):v.check_review_documents(docs,self.index)
        docs=copy.deepcopy(self.docs);docs['hosted-verification.json']['junit']['passed_by_sdk']={'30':6,'35':5}
        with self.assertRaises(ValueError):v.check_review_documents(docs,self.index)
    def test_exact_current_denominator_and_partitions_required(self):
        for mutation in ('denominator','missing','status'):
            counts=copy.deepcopy(self.counts)
            if mutation=='denominator':counts['denominator']['total']=706
            elif mutation=='missing':counts['languages'][0]['missing']+=1
            else:counts['languages'][0]['language_status']='fully-reviewed'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):v.check_source(self.source,self.ids,counts,self.fixture,self.index,self.report)
    def test_exact_source_identity_scope_and_context_required(self):
        for mutation in ('missing','duplicate','hash'):
            ids=copy.deepcopy(self.ids)
            if mutation=='missing':ids['current_source_files'].pop()
            elif mutation=='duplicate':ids['current_source_files'][-1]=ids['current_source_files'][0]
            else:ids['current_source_files'][0]['sha256']='bad'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):v.check_source(self.source,ids,self.counts,self.fixture,self.index,self.report)
    def test_actual_source_byte_drift_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            for item in self.ids['current_source_files']+self.fixture['source_context_files']:
                p=d/item['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(self.source/item['path'],p)
            p=d/'Paintroid/src/main/res/values/strings.xml';p.write_bytes(p.read_bytes()+b'\n')
            with self.assertRaises(ValueError):v.check_source(d,self.ids,self.counts,self.fixture,self.index,self.report)
    def test_previous_immutable_mongolian_acceptance_is_still_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);shutil.copytree(self.evidence,d,dirs_exist_ok=True)
            (d/'position-review-evidence'/v.position.ACCEPTANCE_RECORD).unlink()
            with self.assertRaises(FileNotFoundError):v.validate(self.source,self.previous,evidence_root=d)
    def test_position_index_and_conditional_report_cannot_be_weakened(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);self.copied(d);index=v.read(d/v.position.INDEX);index.pop('additional_acceptance_records');(d/v.position.INDEX).write_text(json.dumps(index))
            with self.assertRaises(ValueError):v.validate(self.source,self.previous,d,self.evidence)
    def test_existing_table_markers_and_rows_always_required(self):
        for name in ('TRANSLATION_PROGRESS.md','current-entry-review.md'):
            for mutation in ('rename','remove_row','duplicate'):
                with self.subTest(name=name,mutation=mutation),tempfile.TemporaryDirectory() as tmp:
                    d=Path(tmp);self.copied(d);p=v.position.document_path(d,name);text=p.read_text()
                    if mutation=='rename':text=text.replace('### Current per-language entry counts','### renamed',1)
                    else:
                        lines=text.splitlines(keepends=True);i=next(i for i,s in enumerate(lines) if s.startswith('| `en-001`'))
                        if mutation=='remove_row':lines.pop(i)
                        else:lines.insert(i,lines[i])
                        text=''.join(lines)
                    p.write_text(text)
                    for previous in (None,self.previous):
                        with self.assertRaises(ValueError):v.validate(self.source,previous,d,self.evidence)
    def test_actual_publication_layout_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);current=root/'current/verification/translation-entry-review-2026-10-13';previous=root/'previous/verification/translation-entry-review-2026-10-13'
            for source,dest in ((self.directory,current),(self.previous,previous)):
                shutil.copytree(source,dest,ignore=shutil.ignore_patterns('__pycache__','TRANSLATION_PROGRESS.md','new-body.md'));shutil.copyfile(v.position.document_path(source,'TRANSLATION_PROGRESS.md'),dest.parents[1]/'TRANSLATION_PROGRESS.md')
            self.assertEqual(v.validate(self.source,previous,current,self.evidence)['table_files'],2)
            p=previous.parents[1]/'TRANSLATION_PROGRESS.md';p.write_text(p.read_text()+'\nChanged previous checkpoint.\n')
            with self.assertRaises(ValueError):v.validate(self.source,previous,current,self.evidence)
    def test_compact_body_must_keep_current_counts_and_draft_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);self.copied(d);p=d/'new-body.md'
            self.assertFalse(p.exists())
            body='Intentional draft. Source5ece04b6:707 entries,120,897 slots;3,386 current,29 open,44,198 unknown,73,284 missing.54 bounded current records and five open idiom reviews.'
            p.write_text(body)
            v.validate(self.source,self.previous,d,self.evidence)
            p.write_text(body.replace('3,386','3,391',1))
            with self.assertRaises(ValueError):v.validate(self.source,self.previous,d,self.evidence)
    def test_required_root_progress_document_cannot_disappear(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);d=root/'repo/verification/translation-entry-review-2026-10-13';self.copied(d)
            self.assertFalse((d/'TRANSLATION_PROGRESS.md').exists())
            progress=v.position.document_path(d,'TRANSLATION_PROGRESS.md')
            self.assertEqual(progress,d.parents[1]/'TRANSLATION_PROGRESS.md')
            progress.unlink()
            with self.assertRaises(ValueError):v.validate(self.source,self.previous,d,self.evidence)
    def test_materializer_checks_all_inputs_before_output(self):
        from materialize_gallery_review_evidence import materialize
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);archive=root/'archive';out=root/'out';archive.mkdir()
            for b in self.index['reports'].values():
                p=archive/b['archive_path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(self.evidence/b['path'],p)
            self.assertEqual(materialize(archive,out)['open_idiom_reviews'],5)
            b=self.index['reports']['complete-statement-review.json'];p=archive/b['archive_path'];p.write_bytes(p.read_bytes()+b' ')
            with self.assertRaises(ValueError):materialize(archive,root/'bad')
            self.assertFalse((root/'bad').exists())

    def test_new_relative_links_resolve_at_each_published_document_location(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)/'repo/verification/translation-entry-review-2026-10-13';self.copied(d)
            self.assertEqual(v.check_document_links(d),4)
            mutations=[('TRANSLATION_PROGRESS.md','verification/translation-entry-review-2026-10-13/gallery-review-evidence-index.json','gallery-review-evidence-index.json'),('current-entry-review.md','gallery-review-evidence-index.json','../gallery-review-evidence-index.json'),('README.md','current-entry-review.md','missing-overview.md')]
            for name,good,bad in mutations:
                p=v.position.document_path(d,name);original=p.read_text();p.write_text(original.replace('('+good+')','('+bad+')',1))
                with self.subTest(name=name),self.assertRaises(ValueError):v.check_document_links(d)
                p.write_text(original)

if __name__=='__main__':unittest.main()
