#!/usr/bin/env python3
"""Fail-closed mechanical source/report reconciliation; no new linguistic review.

Usage: python validate_position_reconciliation.py SOURCE [PREVIOUS_TRACKER_DATA] --evidence-root EXTERNAL_ROOT
The original e53b2e6a historical gates are reused on the preserved historical view.
Their context hashes are not silently repinned to the new source.
"""
import argparse
import copy
import os
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import validate_merged_assembly_reconciliation as legacy
from validate_entry_review import validate as validate_internal
HERE=Path(__file__).resolve().parent
REV='0aa6c89c9d3a4d133a8b231e7002783b60ead46d'
TREE='36ee786caf7b728ee1dada5c4c971ff4830e965c'
OLDREV='e53b2e6aaaa9ac231cfdd38485e28ee9d638e870'
OLDHEAD='7c5c9779ab3ef70ddc5df35bfd62fa05fce87172'
COHORT='ASSEMBLY-POSITION-MERGED-20261015'
FIXTURE='position-merged-reconciliation-20261015.json'
INDEX='position-review-evidence-index.json'
NEW_KEYS={ 'string/'+x for x in ('ui_assembly_exact_position','ui_assembly_target_x','ui_assembly_target_y','ui_assembly_position_help','ui_assembly_position_nonnegative','ui_assembly_unknown_image') }
EARLY_REPORTS={'group-a-independent-review.json','group-b-independent-review.json','group-c-independent-review.json','group-d-independent-review.json','group-e-independent-review.json','group-english-fixtures-independent-review.json'}
EXPECTED={'current_resource_manifest_sha256': 'e38bb1105760edb14d768218c8664138f5a7266e82f8ca6a6d5ef53d0a46cc36', 'previous_resource_manifest_sha256': 'fda0471261e5871f8ff5d558f2a93549068ffa008d9d092860661d023d68af85', 'source_context_manifest_sha256': '6f84a99fc1fbd5e228a5d3d3bb0925940978f534f4cf0a24519974f3ba13dcf8', 'new_pairs_sha256': 'f6514eb8fbefb4a1952f4ae8ab5e0bd9c24d7562c880aa92a26c4237dabd5c84', 'review_bindings_sha256': '91a421c6e54f7969dad2359b4bbaabbdfdd6b471c799a1e3a5cac95f8e8843c3', 'complete_evidence_pairs_sha256': '2b21eb1401fd4a35d9b94fe71e736ebe287626e0c917417f1ae60e5bb4cf100a', 'index_sha256': '6ee8057a5b2a4b64f7eb0d085ff910eb1d0245d5faa4b161bff5eac79740232a', 'old_receipts_sha256': 'bcfa717be010cc15fb5d651837173065748cbdf0aeed1d5de751c36c48cfd557', 'old_cohorts_sha256': '6dce198081d223922c8a4ea83d3e533e363d646aba0ecadddbabc3708bc7cc3e', 'old_history_sha256': '65a914b4a8cf1889c7701f9a6b695f6c41f3d5f6db1cd151b8318bcc0d8960c4', 'old_partial_sha256': 'ed40cde25ca4466446799cf432a0a2989a5a1a2b23db0816e2e360e6feda35dd', 'language_identity_sha256': 'f147f620cb9f053b1cfe662eba80635ece98c6dc5063fbd1d3aa73f7b9a9c4e1', 'reconciliation_fixture_sha256': 'e29a676c19fb69ed44d766ede1ddbaa58f82ee39d76d8c565dceb2efe823dbb7'}
read=legacy.read
require=legacy.require
value_hash=legacy.value_hash
blob_hash=legacy.blob_hash
values=legacy.values

def historical_receipts(receipts):
    old=copy.deepcopy(receipts)
    old['source_revision']=OLDREV
    old['receipts']=[r for r in old['receipts'] if r['cohort']!=COHORT]
    old['cohorts'].pop(COHORT,None)
    return old

def check_preservation(receipts,identities,fixture,previous=None):
    old=historical_receipts(receipts)
    for field,key in [('receipts','old_receipts_sha256'),('cohorts','old_cohorts_sha256'),('superseded_receipts','old_history_sha256'),('partial_reviews','old_partial_sha256')]:
        require(value_hash(old[field])==EXPECTED[key],'Historical '+field+' changed')
    require((len(old['receipts']),len(old['superseded_receipts']),len(old['partial_reviews']))==(3002,59,56),'Historical counts changed')
    require(value_hash(identities['previous_resource_manifest_at_position_merge'])==EXPECTED['previous_resource_manifest_sha256'],'Previous resource scope changed')
    require(fixture['preserved_active_receipts_sha256']==EXPECTED['old_receipts_sha256'] and fixture['preserved_cohorts_sha256']==EXPECTED['old_cohorts_sha256'] and fixture['preserved_superseded_receipts_sha256']==EXPECTED['old_history_sha256'] and fixture['preserved_partial_reviews_sha256']==EXPECTED['old_partial_sha256'],'Preservation fixture differs')
    if previous:
        require(old==read(previous/'entry-review-receipts.json'),'Prior full receipt ledger differs')
        oldids=read(previous/'source-identities.json')
        changed={'source_revision','resource_keys','current_source_files','resource_identity_continuity'}
        require(all(identities[k]==v for k,v in oldids.items() if k not in changed),'Earlier source/context metadata changed')
        require(identities['previous_resource_manifest_at_position_merge']=={k:oldids[k] for k in changed},'Previous source manifest not exact')
    return old

def resolve_pointer(report,pointer):
    require(isinstance(pointer,str) and pointer.startswith('/'),'Review pointer absent')
    current=report
    for part in pointer[1:].split('/'):
        part=part.replace('~1','/').replace('~0','~')
        current=current[int(part)] if isinstance(current,list) else current[part]
    return current

def check_accepted_entry(pair,report):
    name=pair['report'];key=pair['key'].split('/',1)[1]
    r=resolve_pointer(report,pair['pointer'])
    target_hash=r.get('target_sha256',r.get('new_sha256'))
    require(target_hash==pair['target_utf8_sha256'],'Review target hash mismatch')
    if name in EARLY_REPORTS:
        require(report.get('source_commit')=='5d145e17b52200a6c132d847d0e12e892fa1c657' and bool(report.get('scope')),'Early full-value scope/source missing')
        require(r.get('verdict')=='accepted_source_semantics','Early full-value acceptance missing')
    elif name=='group-f-mn-mong-independent-review.json':
        if pair['pointer']=='/revisions/0':
            require(pair['tag']=='mn-Mong' and key=='ui_assembly_position_help','Mongolian replacement identity changed')
            require(r.get('verdict')=='complete revised value source-semantically acceptable to this reviewer; parent check required before publication','Complete Mongolian revised review missing')
            require(pair.get('additional_complete_acceptance')=='https://github.com/c933103/AN-Paint/pull/67#issuecomment-6191639077','Mongolian full-value reread receipt missing')
            require(r.get('new_target')==pair['localized'] and len(r.get('semantic_anchors',[]))==9,'Incomplete Mongolian full-value review')
        else:
            require(r.get('verdict')=='accepted_source_semantics','Mongolian original is held')
    elif name=='group-h-okinawan-help-replacement-review.json':
        require(pair['pointer']=='/independent_complete_value_review' and r.get('verdict')=='accepted_source_semantics','Okinawan independent complete successor missing')
        require(report.get('candidate')==pair['localized'] and len(r.get('clauses',{}))==7,'Okinawan candidate/complete clauses differ')
    else:
        require(r.get('decision')=='accept' and r.get('whole_value_reviewed') is True and r.get('approved_for_integration') is True,'Held, partial or unapproved review cannot count')
    require(r.get('key',key)==key and r.get('language',r.get('locale',pair['tag']))==pair['tag'],'Report pair identity mismatch')
    for field in ('source','source_value'):
        if field in r:require(r[field]==pair['english'],'Complete reviewed English differs')
    for field in ('target','complete_target_value'):
        if field in r:require(r[field]==pair['localized'],'Complete reviewed target differs')
    if 'source_sha256' in r:require(r['source_sha256']==pair['source_utf8_sha256'],'Reviewed English raw hash differs')
    return r

def check_reports(evidence_root,index):
    require(value_hash(index['reports'])==EXPECTED['review_bindings_sha256'],'Pinned report identity/receipt bindings changed')
    require(len(index['reports'])==21,'Report history omitted')
    reports={}
    for name,b in index['reports'].items():
        p=Path(b['path']);require(not p.is_absolute() and '..' not in p.parts and p.name==name,'Unsafe or mismatched report path')
        revision=b['durable_revision']
        require(re.fullmatch('[0-9a-f]{40}',revision) is not None,'Durable review revision not immutable')
        require(b['durable_receipt']=='https://github.com/c933103/AN-Paint/blob/'+revision+'/'+b['archive_path'],'Wrong durable receipt')
        data=(evidence_root/p).read_bytes()
        require(hashlib.sha256(data).hexdigest()==b['sha256'] and blob_hash(data)==b['git_blob_sha1'] and len(data)==b['size'],'Complete report bytes/identity mismatch: '+name)
        reports[name]=json.loads(data)
    require(value_hash(index['complete_pairs'])==EXPECTED['complete_evidence_pairs_sha256'],'Complete pair evidence or supersession changed')
    require(index['unresolved']==[] and index['complete_pair_count']==354,'Unresolved complete review evidence')
    for pair in index['complete_pairs']:
        require(pair.get('accepted') is True and pair['key'] in NEW_KEYS,'Pair is not fully accepted or key outside scope')
        require(hashlib.sha256(pair['english'].encode()).hexdigest()==pair['source_utf8_sha256'],'Full English raw hash mismatch')
        require(hashlib.sha256(pair['localized'].encode()).hexdigest()==pair['target_utf8_sha256'],'Full target raw hash mismatch')
        check_accepted_entry(pair,reports[pair['report']])
    return reports

def check_new_receipts(receipts,index,counts,english,catalogues):
    rows={r['tag']:r for r in counts['languages']}
    allpairs={(r['tag'],r['key']):r for r in receipts['receipts']}
    require(len(allpairs)==len(receipts['receipts'])==3356,'Duplicate or missing active pairs')
    expected={(p['tag'],p['key']) for p in index['complete_pairs']}
    new=[r for r in receipts['receipts'] if r['cohort']==COHORT]
    require(len(new)==354 and {(r['tag'],r['key']) for r in new}==expected,'New receipt identity set differs')
    require(len(expected)==354 and len({t for t,k in expected})==59,'Wrong new language scope')
    for r in receipts['receipts']:
        require(r['current_english_sha256']==value_hash(english[r['key']]),'Active English value mismatch')
        require(r['current_localized_sha256']==value_hash(catalogues[r['tag']][r['key']]),'Active localized value mismatch')
    for p in index['complete_pairs']:
        pair=(p['tag'],p['key']);r=allpairs[pair];b=index['reports'][p['report']];test=rows[p['tag']]['kind']=='test_mode'
        expected_fields={'cohort':COHORT,'state':'reviewed_current','reviewed_source_revision':'5d145e17b52200a6c132d847d0e12e892fa1c657','merged_revision':REV,'disposition':'accepted_test_convention' if test else 'accepted_static','review_scope':'complete_value_test_mode_convention' if test else 'complete_value_bounded_semantic','review_kind':'complete_position_value_source_binding','confidence':p['semantic_confidence'],'idiom_confidence':p['idiom_confidence'],'source':b['durable_receipt'],'independent_review_source':b['durable_receipt'],'complete_review_report_path':b['path'],'complete_review_report_sha256':b['sha256'],'review_pointer':p['pointer'],'reviewed_english_utf8_sha256':p['source_utf8_sha256'],'reviewed_localized_utf8_sha256':p['target_utf8_sha256'],'complete_value_review':True,'native_speaker_certification':False,'whole_language_certification':False,'runtime_layout_acceptance_from_this_receipt':False}
        for field,val in expected_fields.items():
            require(type(r.get(field)) is type(val) and r[field]==val,'New receipt metadata mismatch: '+str(pair)+' '+field)
        require(r.get('finding_status')!='open','Open finding counted current')
        require(english[p['key']]==p['english'] and catalogues[p['tag']][p['key']]==p['localized'],'Complete pair differs from actual source')
        for kind in ('english','localized'):
            require(r['reviewed_'+kind+'_sha256']==r['current_'+kind+'_sha256']==value_hash(p[kind]),'Canonical JSON review/source hash mismatch')
    return allpairs

def check_source(source,identities,counts,fixture):
    require(identities['source_revision']==fixture['source_revision']==REV and fixture['source_tree']==TREE,'Wrong current source identity')
    require(fixture['preceding_tracker_revision']==OLDHEAD and fixture['preceding_source_revision']==OLDREV and fixture['excluded_unmerged_prs']==[85],'Wrong predecessor/excluded scope')
    paths=[x['path'] for x in identities['current_source_files']]
    require(len(paths)==len(set(paths))==182,'Wrong resource path count')
    require(value_hash(identities['current_source_files'])==EXPECTED['current_resource_manifest_sha256'],'Current resource manifest changed')
    require(value_hash(fixture['source_context_files'])==EXPECTED['source_context_manifest_sha256'],'Current source context identities changed')
    for i in identities['current_source_files']+fixture['source_context_files']:
        p=Path(i['path']);require(not p.is_absolute() and '..' not in p.parts,'Unsafe source path')
        data=(source/p).read_bytes();require(blob_hash(data)==i['git_blob_sha'] and hashlib.sha256(data).hexdigest()==i['sha256'],'Exact current source identity mismatch: '+str(p))
    en=values(source/'Paintroid/src/main/res/values/strings.xml')
    require(set(en)==set(identities['resource_keys']) and len(en)==len(identities['resource_keys'])==706,'Source denominator or identity changed')
    require(set(en)-set(identities['previous_resource_manifest_at_position_merge']['resource_keys'])==NEW_KEYS,'New source-key scope changed')
    require(counts['denominator']=={'strings':705,'plural_resources':1,'total':706},'Typed denominator wrong')
    stable=[{k:v for k,v in row.items() if k not in ['total','present','reviewed_current','needs_rereview','unreviewed_or_unknown','missing','reviewed_current_keys','needs_rereview_keys']} for row in counts['languages']]
    require(value_hash(stable)==EXPECTED['language_identity_sha256'],'Language identity/path/status changed')
    cats={row['tag']:values(source/row['catalogue_path']) for row in counts['languages']}
    for row in counts['languages']:
        present=sum(bool(v) for k,v in cats[row['tag']].items() if k in en)
        require(row['present']==present and row['missing']==706-present,'Catalogue actual coverage mismatch')
    importance=read(source/'translations/string-importance.json')
    tier={k:t['id'] for t in importance['tiers'] for k in t['keys']}
    require(all(tier[k]=='P2' for k in NEW_KEYS),'Operational keys lost P2')
    require(tier[legacy.HELP_KEY]=='P3','General optional Help priority changed')
    return en,cats

def document_path(directory,name):
    direct=directory/name
    if direct.is_file():return direct
    if name=='TRANSLATION_PROGRESS.md':
        root=directory.parents[1]/name
        require(root.is_file(),'Required root progress document missing: '+str(root))
        return root
    require(False,'Required tracker document missing: '+str(direct))


def evidence_location(directory,evidence_root=None):
    selected=evidence_root if evidence_root is not None else os.environ.get('AN_PAINT_POSITION_EVIDENCE')
    require(bool(selected),'Explicit external evidence root required: --evidence-root or AN_PAINT_POSITION_EVIDENCE')
    root=Path(selected).resolve()
    require(root.is_dir(),'External evidence root is unavailable: '+str(root))
    require(root!=directory.resolve() and directory.resolve() not in root.parents,'Evidence must be separate from the tracker data directory')
    return root


def validate(source,previous=None,directory=HERE,evidence_root=None):
    evidence_root=evidence_location(directory,evidence_root)
    summary=validate_internal(directory)
    require(summary['source_revision']==REV,'Wrong source revision')
    receipts=read(directory/'entry-review-receipts.json');counts=read(directory/'entry-review-counts.json');ids=read(directory/'source-identities.json');fixture=read(directory/FIXTURE);index=read(directory/INDEX)
    require(value_hash(index)==EXPECTED['index_sha256'],'Pinned complete review index changed')
    require(value_hash(fixture)==EXPECTED['reconciliation_fixture_sha256'],'Current reconciliation scope/evidence changed')
    require(ids['merged_position_rebinding']==fixture,'Source identities/fixture disagree')
    require(value_hash(fixture['new_pairs'])==EXPECTED['new_pairs_sha256'] and fixture['new_keys']==sorted(NEW_KEYS),'New pair/key scope differs')
    old=check_preservation(receipts,ids,fixture,previous)
    english,cats=check_source(source,ids,counts,fixture)
    check_reports(evidence_root,index)
    check_new_receipts(receipts,index,counts,english,cats)
    # Original complete-review and history gates remain exact at their own source.
    oldfixture=read(directory/legacy.FIXTURE)
    legacy.check_history(old,oldfixture)
    legacy.check_review_artifacts(directory,oldfixture,source=None)
    historical=read(directory/'fr-assembly-merged-reconciliation-20261015.json')['complete_french_pairs']+read(directory/'four-crop-merged-reconciliation-20261015.json')['complete_crop_pairs']
    legacy.check_pairs(old,historical,oldfixture,english,cats)
    cohort=receipts['cohorts'][COHORT]
    require(cohort['source_revision']==REV and cohort['reports']==index['reports'] and cohort['complete_pair_count']==354 and cohort['requirements_closed']==[] and cohort['scope']==index['scope'],'Position cohort binding changed')
    require(cohort['counts']=={'complete_values':354,'catalogues':59,'operational_keys':6,'natural_regional_values':342,'test_mode_conventions':12},'Position scope counts differ')
    tables=legacy.check_tables(directory,counts)
    body=(directory/'new-body.md').read_text() if (directory/'new-body.md').exists() else ''
    if body:
        require(len(body)<4000 and all(x in body for x in ('3,332','44,198','73,172','120,726','706','PR85','Intentional draft')),'Compact body current facts missing')
    validation=read(directory/'validation.json')
    require(validation['summary']==counts['summary'] and validation['preceding_tracker_revision']==OLDHEAD,'Validation facts disagree')
    require(validation['new_unique_receipts']==354 and validation['unchanged_active_receipts']==3002 and validation['processing_holds']==4 and validation['source_stale_pairs_remaining']==0,'Validation receipt scope wrong')
    if previous:
        require(validation['prior_checkpoint_validation']==read(previous/'validation.json'),'Prior validation evidence lost')
        for n in ('TRANSLATION_PROGRESS.md','current-entry-review.md'):
            current=document_path(directory,n).read_text();prior=document_path(previous,n).read_text()
            require(current.split('### Preserved earlier review checkpoints',1)[1]==prior.split('### Preserved earlier review checkpoints',1)[1],'Historical prose edited')
            require(prior.split('### Current per-language entry counts',1)[0] in current,'Pre-position overview lost')
        for n in ('fr-assembly-merged-reconciliation-20261015.json','four-crop-merged-reconciliation-20261015.json',legacy.FIXTURE):
            require((directory/n).read_bytes()==(previous/n).read_bytes(),'Historical complete review fixture edited')
    return {'status':'PASS','source_revision':REV,'source_tree':TREE,'preceding_tracker_revision':OLDHEAD,'source_identity_files':182,'source_context_identity_files':8,'active_english_hashes':3356,'active_localized_hashes':3356,'catalogue_partitions':171,'new_complete_review_pairs':354,'bound_complete_reports':21,'preserved_active_pairs':3002,'superseded_history':59,'partial_records':56,'processing_holds':4,'previous_checkpoint_compared':bool(previous),'table_files':tables,'summary':counts['summary'],'scope':'Mechanical source/report validation only; original complete-review/history gates retained. No new application/native-speaker/full-language/runtime certification.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('previous',type=Path,nargs='?')
    parser.add_argument('--evidence-root',type=Path,help='External materialized review root; alternatively set AN_PAINT_POSITION_EVIDENCE')
    args=parser.parse_args()
    print(json.dumps(validate(args.source,args.previous,evidence_root=args.evidence_root),indent=2))
