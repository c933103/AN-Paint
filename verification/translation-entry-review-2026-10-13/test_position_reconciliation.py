"""Negative controls for current source, full-value review, scope and history."""
import copy
import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import validate_position_reconciliation as v

class PositionGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory=v.HERE
        cls.receipts=v.read(v.HERE/'entry-review-receipts.json')
        cls.counts=v.read(v.HERE/'entry-review-counts.json')
        cls.ids=v.read(v.HERE/'source-identities.json')
        cls.fixture=v.read(v.HERE/v.FIXTURE)
        cls.index=v.read(v.HERE/v.INDEX)
        cls.evidence_root=v.evidence_location(cls.directory)
        cls.reports={n:v.read(cls.evidence_root/b['path']) for n,b in cls.index['reports'].items()}
        cls.source=Path(os.environ['AN_PAINT_SOURCE']) if os.environ.get('AN_PAINT_SOURCE') else None
        cls.english={p['key']:p['english'] for p in cls.index['complete_pairs']}
        cls.catalogues={}
        if cls.source:
            cls.english=v.values(cls.source/'Paintroid/src/main/res/values/strings.xml')
            cls.catalogues={r['tag']:v.values(cls.source/r['catalogue_path']) for r in cls.counts['languages']}
    def require_source(self):
        if self.source is None:self.skipTest('Supply AN_PAINT_SOURCE for actual source checks')
    def check_new(self,receipts=None,index=None):
        self.require_source()
        return v.check_new_receipts(receipts or self.receipts,index or self.index,self.counts,self.english,self.catalogues)
    def mutate_pair(self,field,value=None,remove=False,predicate=None):
        r=copy.deepcopy(self.receipts)
        x=next(x for x in r['receipts'] if x['cohort']==v.COHORT and (predicate is None or predicate(x)))
        if remove:x.pop(field,None)
        else:x[field]=value
        return r
    def test_full_current_source_validation(self):
        self.require_source()
        result=v.validate(self.source,evidence_root=self.evidence_root)
        self.assertEqual(result['new_complete_review_pairs'],354)
        self.assertEqual(result['summary']['reviewed_current'],3332)
    def test_old_entrypoint_dispatches_to_current_strict_validator(self):
        self.require_source()
        result=v.legacy.validate(self.source)
        self.assertEqual(result['active_english_hashes'],3356)
    def test_all_complete_reports_and_superseded_decisions(self):
        self.assertEqual(len(v.check_reports(self.evidence_root,self.index)),21)
        self.assertEqual(len(self.index['complete_pairs']),354)
        self.assertTrue(any(p['superseded_review_decisions'] for p in self.index['complete_pairs']))
    def test_all_current_pairs(self):
        self.assertEqual(len(self.check_new()),3356)
    def test_all_required_receipt_fields_missing_rejected(self):
        fields=['reviewed_source_revision','merged_revision','review_scope','disposition','review_kind','source','independent_review_source','complete_review_report_path','complete_review_report_sha256','review_pointer','complete_value_review','confidence','idiom_confidence','reviewed_english_utf8_sha256','reviewed_localized_utf8_sha256','native_speaker_certification','whole_language_certification','runtime_layout_acceptance_from_this_receipt']
        for field in fields:
            with self.subTest(field=field),self.assertRaises(ValueError):
                self.check_new(self.mutate_pair(field,remove=True))
    def test_partial_delta_and_open_dispositions_rejected(self):
        for field,value in [('review_scope','delta_only'),('review_scope','complete_delta_only'),('disposition','partial_review_not_counted'),('complete_value_review',False),('complete_value_review',1),('finding_status','open'),('state','needs_rereview')]:
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                self.check_new(self.mutate_pair(field,value))
    def test_unearned_runtime_native_whole_language_claims_rejected(self):
        for field in ('native_speaker_certification','whole_language_certification','runtime_layout_acceptance_from_this_receipt'):
            with self.subTest(field=field),self.assertRaises(ValueError):self.check_new(self.mutate_pair(field,True))
    def test_review_url_must_be_exact_published_receipt(self):
        for field in ('source','independent_review_source'):
            with self.subTest(field=field),self.assertRaises(ValueError):self.check_new(self.mutate_pair(field,'https://example.invalid/review'))
    def test_raw_utf8_and_json_hashes_are_not_interchangeable(self):
        for field in ('reviewed_english_sha256','reviewed_localized_sha256'):
            p=self.index['complete_pairs'][0];wrong=p['source_utf8_sha256' if 'english' in field else 'target_utf8_sha256']
            with self.subTest(field=field),self.assertRaises(ValueError):self.check_new(self.mutate_pair(field,wrong))
    def test_changed_current_english_or_target_rejected(self):
        for field in ('current_english_sha256','current_localized_sha256'):
            with self.subTest(field=field),self.assertRaises(ValueError):self.check_new(self.mutate_pair(field,'0'*64))
    def test_missing_duplicate_or_extra_new_pair_rejected(self):
        for mutation in ('missing','duplicate','outside'):
            r=copy.deepcopy(self.receipts)
            if mutation=='missing':r['receipts'].pop()
            elif mutation=='duplicate':r['receipts'][-1]=copy.deepcopy(r['receipts'][-2])
            else:r['receipts'][-1]['tag']='am'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):self.check_new(r)
    def test_test_convention_cannot_be_ordinary_language_acceptance(self):
        for field,val in [('disposition','accepted_static'),('review_scope','complete_value_bounded_semantic')]:
            with self.subTest(field=field),self.assertRaises(ValueError):self.check_new(self.mutate_pair(field,val,predicate=lambda r:r['tag']=='en-XV'))
    def test_report_held_partial_or_not_approved_rejected(self):
        p=next(p for p in self.index['complete_pairs'] if p['report']=='group-i-ainu-help-anchor-independent-review.json')
        for field,val in [('decision','hold'),('whole_value_reviewed',False),('approved_for_integration',False)]:
            d=copy.deepcopy(self.reports[p['report']]);row=v.resolve_pointer(d,p['pointer']);row[field]=val
            with self.subTest(field=field),self.assertRaises(ValueError):v.check_accepted_entry(p,d)
    def test_report_complete_value_and_pair_identity_required(self):
        p=next(p for p in self.index['complete_pairs'] if p['report']=='group-i-vi-hani-independent-review.json')
        for field,val in [('source','truncated'),('target','truncated'),('source_sha256','bad'),('target_sha256','bad'),('key','wrong'),('language','wrong')]:
            d=copy.deepcopy(self.reports[p['report']]);v.resolve_pointer(d,p['pointer'])[field]=val
            with self.subTest(field=field),self.assertRaises(ValueError):v.check_accepted_entry(p,d)
    def test_mongolian_revised_whole_paragraph_and_parent_reread_required(self):
        p=next(p for p in self.index['complete_pairs'] if p['tag']=='mn-Mong' and p['key'].endswith('_help'))
        bad=copy.deepcopy(p);bad.pop('additional_complete_acceptance')
        with self.assertRaises(ValueError):v.check_accepted_entry(bad,self.reports[p['report']])
        d=copy.deepcopy(self.reports[p['report']]);d['revisions'][0]['semantic_anchors'].pop()
        with self.assertRaises(ValueError):v.check_accepted_entry(p,d)
    def test_okinawan_author_candidate_is_not_accepted_without_full_successor(self):
        p=next(p for p in self.index['complete_pairs'] if p['report']=='group-h-okinawan-help-replacement-review.json')
        d=copy.deepcopy(self.reports[p['report']]);d['independent_complete_value_review']['verdict']='pending'
        with self.assertRaises(ValueError):v.check_accepted_entry(p,d)
    def test_new_index_cannot_omit_previous_hold_or_change_final_pointer(self):
        for mutation in ('history','pointer','receipt','unresolved'):
            x=copy.deepcopy(self.index)
            if mutation=='history':next(p for p in x['complete_pairs'] if p['superseded_review_decisions'])['superseded_review_decisions']=[]
            elif mutation=='pointer':x['complete_pairs'][0]['pointer']='/entries/1'
            elif mutation=='receipt':next(iter(x['reports'].values()))['durable_revision']='main'
            else:x['unresolved']=[{'tag':'ain-Latn','key':'string/ui_assembly_position_help'}]
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):v.check_reports(self.evidence_root,x)
    def test_review_file_bytes_must_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            shutil.copytree(self.evidence_root/'position-review-evidence',d/'position-review-evidence')
            first=next(iter(self.index['reports'].values()))
            p=d/first['path'];p.write_bytes(p.read_bytes()+b' ')
            with self.assertRaises(ValueError):v.check_reports(d,self.index)
    def test_prior_active_history_partial_and_cohorts_preserved(self):
        for field in ('receipts','superseded_receipts','partial_reviews','cohorts'):
            r=copy.deepcopy(self.receipts)
            if field=='cohorts':r[field][next(k for k in r[field] if k!=v.COHORT)]['scope']='changed'
            else:r[field][0]['source']='changed'
            with self.subTest(field=field),self.assertRaises(ValueError):v.check_preservation(r,self.ids,self.fixture)
    def test_four_processing_holds_not_cleared(self):
        for tag in ('ms','id','ja','zh-HK'):
            r=copy.deepcopy(self.receipts);x=next(x for x in r['receipts'] if x['tag']==tag and x['key']=='string/ui_rendering_images');x['state']='reviewed_current';x.pop('finding_status',None)
            with self.subTest(tag=tag),self.assertRaises(ValueError):v.check_preservation(r,self.ids,self.fixture)
    def test_source_identity_omission_substitution_and_duplicate_rejected(self):
        self.require_source()
        for mutation in ('omit','substitute','duplicate','hash'):
            ids=copy.deepcopy(self.ids)
            if mutation=='omit':ids['current_source_files'].pop()
            elif mutation=='substitute':ids['current_source_files'][0]['path']='other.xml'
            elif mutation=='duplicate':ids['current_source_files'][-1]=ids['current_source_files'][0]
            else:ids['current_source_files'][0]['sha256']='bad'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):v.check_source(self.source,ids,self.counts,self.fixture)
    def test_language_scope_and_denominator_cannot_drift(self):
        self.require_source()
        for mutation in ('identity','status','denominator','coverage'):
            counts=copy.deepcopy(self.counts)
            if mutation=='identity':counts['languages'][0]['tag']='tl'
            elif mutation=='status':counts['languages'][0]['language_status']='fully-reviewed'
            elif mutation=='denominator':counts['denominator']['total']=707
            else:counts['languages'][0]['present']-=1
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):v.check_source(self.source,self.ids,counts,self.fixture)
    def test_pr85_unmerged_key_and_context_promotion_rejected(self):
        self.require_source()
        for mutation in ('exclusion','context'):
            fixture=copy.deepcopy(self.fixture)
            if mutation=='exclusion':fixture['excluded_unmerged_prs']=[]
            else:fixture['source_context_files'][0]['git_blob_sha']='bad'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):v.check_source(self.source,self.ids,self.counts,fixture)
    def test_actual_source_byte_drift_rejected(self):
        self.require_source()
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            for item in self.ids['current_source_files']+self.fixture['source_context_files']:
                target=d/item['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(self.source/item['path'],target)
            p=d/'Paintroid/src/main/res/values/strings.xml';p.write_bytes(p.read_bytes()+b'\n')
            with self.assertRaises(ValueError):v.check_source(d,self.ids,self.counts,self.fixture)
    def test_end_to_end_rejects_inflated_native_scope(self):
        self.require_source()
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);shutil.copytree(self.directory,d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
            fixture=copy.deepcopy(self.fixture);fixture['native_evidence']['api']=30
            (d/v.FIXTURE).write_text(json.dumps(fixture))
            ids=copy.deepcopy(self.ids);ids['merged_position_rebinding']=fixture
            (d/'source-identities.json').write_text(json.dumps(ids))
            with self.assertRaises(ValueError):v.validate(self.source,directory=d,evidence_root=self.evidence_root)

    def test_required_table_documents_cannot_be_silently_skipped(self):
        self.require_source()
        for filename in ('TRANSLATION_PROGRESS.md','current-entry-review.md'):
            for mutation in ('remove_marker','rename_marker','remove_row','duplicate_row'):
                with self.subTest(filename=filename,mutation=mutation),tempfile.TemporaryDirectory() as tmp:
                    d=Path(tmp);shutil.copytree(self.directory,d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
                    p=d/filename
                    if not p.exists():shutil.copyfile(self.directory.parents[1]/filename,p)
                    text=p.read_text()
                    if mutation=='remove_marker':text=text.replace('### Current per-language entry counts','',1)
                    elif mutation=='rename_marker':text=text.replace('### Current per-language entry counts','### Current table',1)
                    else:
                        lines=text.splitlines(keepends=True)
                        first=next(i for i,line in enumerate(lines) if line.startswith('| `en-001`'))
                        if mutation=='remove_row':lines.pop(first)
                        else:lines.insert(first,lines[first])
                        text=''.join(lines)
                    p.write_text(text)
                    with self.assertRaises(ValueError):v.validate(self.source,directory=d,evidence_root=self.evidence_root)
                    previous=os.environ.get('AN_PAINT_PREVIOUS')
                    if previous:
                        with self.assertRaises(ValueError):v.validate(self.source,Path(previous),directory=d,evidence_root=self.evidence_root)
    def test_only_compact_pr_body_may_omit_current_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            for filename in ('current-entry-review.md','TRANSLATION_PROGRESS.md'):
                source=self.directory/filename
                if not source.exists():source=self.directory.parents[1]/filename
                shutil.copyfile(source,d/filename)
            (d/'new-body.md').write_text('Compact PR body links to the complete current table.')
            self.assertEqual(v.legacy.check_tables(d,self.counts),2)

    def test_external_evidence_root_is_required_and_not_tracker_local(self):
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(ValueError,'Explicit external evidence root required'):
                v.evidence_location(self.directory)
        with self.assertRaises(ValueError):v.evidence_location(self.directory,self.directory)
        with tempfile.TemporaryDirectory() as tmp:
            nested=Path(tmp)/'cache';nested.mkdir()
            with self.assertRaises(ValueError):v.evidence_location(Path(tmp),nested)
        with self.assertRaises(ValueError):v.evidence_location(self.directory,self.directory/'absent-evidence')
    def test_missing_external_report_fails_instead_of_trusting_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            shutil.copytree(self.evidence_root/'position-review-evidence',d/'position-review-evidence')
            first=next(iter(self.index['reports'].values()))
            (d/first['path']).unlink()
            with self.assertRaises(FileNotFoundError):v.check_reports(d,self.index)
    def test_materializer_validates_all_bytes_before_copying(self):
        from materialize_position_review_evidence import materialize
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);archive=d/'archive';out=d/'external';archive.mkdir()
            for binding in self.index['reports'].values():
                target=archive/binding['archive_path'];target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(self.evidence_root/binding['path'],target)
            result=materialize(archive,out,self.directory/v.INDEX)
            self.assertEqual(result['reports'],21)
            self.assertEqual(len(v.check_reports(out,self.index)),21)
            first=next(iter(self.index['reports'].values()))
            target=archive/first['archive_path'];target.write_bytes(target.read_bytes()+b' ')
            bad=d/'bad-output'
            with self.assertRaises(ValueError):materialize(archive,bad,self.directory/v.INDEX)
            self.assertFalse(bad.exists())

    def test_actual_publication_layout_with_previous_and_external_evidence(self):
        self.require_source()
        previous=os.environ.get('AN_PAINT_PREVIOUS')
        if not previous:self.skipTest('Supply AN_PAINT_PREVIOUS for both exact published snapshot layouts')
        previous=Path(previous)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);current_data=root/'current'/'verification'/'translation-entry-review-2026-10-13'
            previous_data=root/'previous'/'verification'/'translation-entry-review-2026-10-13'
            for source,destination in ((self.directory,current_data),(previous,previous_data)):
                shutil.copytree(source,destination,ignore=shutil.ignore_patterns('__pycache__','TRANSLATION_PROGRESS.md','new-body.md','position-validation-constants.json'))
                shutil.copyfile(v.document_path(source,'TRANSLATION_PROGRESS.md'),destination.parents[1]/'TRANSLATION_PROGRESS.md')
            result=v.validate(self.source,previous_data,directory=current_data,evidence_root=self.evidence_root)
            self.assertTrue(result['previous_checkpoint_compared'])
            self.assertEqual(result['table_files'],2)
            root_progress=current_data.parents[1]/'TRANSLATION_PROGRESS.md'
            original=root_progress.read_text()
            root_progress.write_text(original.replace('### Current per-language entry counts','### Renamed current table',1))
            with self.assertRaises(ValueError):v.validate(self.source,previous_data,directory=current_data,evidence_root=self.evidence_root)
            root_progress.write_text(original)
            old_progress=previous_data.parents[1]/'TRANSLATION_PROGRESS.md'
            old_progress.write_text(old_progress.read_text()+'\nAltered historical prose.\n')
            with self.assertRaises(ValueError):v.validate(self.source,previous_data,directory=current_data,evidence_root=self.evidence_root)

if __name__=='__main__':unittest.main()
