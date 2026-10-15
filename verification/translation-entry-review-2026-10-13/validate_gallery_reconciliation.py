#!/usr/bin/env python3
"""Current PR85 source/evidence gates, retaining every prior acceptance/history gate.

Usage: python validate_gallery_reconciliation.py SOURCE [PREVIOUS_TRACKER_DATA]
       --evidence-root EXTERNAL_ROOT
No network requests, application tests or new linguistic decisions are made.
"""
import argparse
import copy
import hashlib
import json
import re
import posixpath
from urllib.parse import urlsplit
from pathlib import Path
import validate_position_reconciliation as position
from validate_entry_review import validate as validate_internal
HERE=Path(__file__).resolve().parent
REV='5ece04b6c604b98fc0e59db600c728e541d08261'
TREE='7b5641d6b4b041e49fa7442d894353b4f65275f6'
OLDHEAD='2499c5e32e75d5bd1de916174b9992ea001af6b6'
EREV='97c91f05bb2192f13db309d1ce2927cc3f328024'
COHORT='GALLERY-LINK-MERGED-20261015'
KEY='string/gallery_external_link_no_handler'
INDEX='gallery-review-evidence-index.json'
FIXTURE='gallery-merged-reconciliation-20261015.json'
OPEN={'ain-Kana','ain-Latn','hak-Latn-TW','mnc-Mong','ryu'}
ALLOWED={'accept-for-bounded-error-message','accept-with-disclosed-idiom-limit','bounded_semantic_review_no_correction','bounded_semantic_review_with_idiom_limit','limited_full_statement_review_unresolved_idiom'}
EXPECTED={'old_receipts': 'be74babbbf26bdf5476e520d20652dcd85d42108d198843950ea16f590524474', 'old_ids': '01c68530db5b5393a3bedf0c744ac31438022a258ca46d5f9931999115d7cf2b', 'index': '2234d10bb15f829e8946be5c24329343317508567de327cde3a5ad599900a7ae', 'fixture': '4e4a0a6e6ffa1eec2b131654611cbb5aa3668c9d8fe8b2015317af7db1e35b83', 'source_manifest': '0225fa69ca7c33b50798cee45480378af32162a0235af52612fe5f6dec541cf2', 'language_identity': 'f147f620cb9f053b1cfe662eba80635ece98c6dc5063fbd1d3aa73f7b9a9c4e1', 'new_receipts': 'eded079031c940947457c7f19d025c17e8e17854387e2cda15b1c485fbb9f5c9', 'counts': '1c0cc63db13f925a19589af743eec862915fcf2e3f0b7c8488abefba884a1777', 'source_ids': '29fcc70503eb8ee38869f301020fd4aeff6f591c6a56d2f4fd0feeccc835a248'}
read=position.read
require=position.require
value_hash=position.value_hash
blob_hash=position.blob_hash
values=position.values

def prior_ledger(receipts):
    old=copy.deepcopy(receipts)
    old['source_revision']=position.REV
    old['receipts']=[r for r in old['receipts'] if r['cohort']!=COHORT]
    old['cohorts'].pop(COHORT,None)
    return old

def check_preservation(receipts,identities,previous=None):
    old=prior_ledger(receipts)
    require(value_hash(old)==EXPECTED['old_receipts'],'Earlier full ledger/cohorts/history/partial records changed')
    earlier={k:v for k,v in identities.items() if k not in ('previous_resource_manifest_at_gallery_merge','merged_gallery_rebinding')}
    earlier.update(identities['previous_resource_manifest_at_gallery_merge'])
    require(value_hash(earlier)==EXPECTED['old_ids'],'Earlier complete source/context identities changed')
    require((len(old['receipts']),len(old['superseded_receipts']),len(old['partial_reviews']))==(3356,59,56),'Prior record counts changed')
    if previous:
        require(old==read(previous/'entry-review-receipts.json'),'Previous published ledger differs')
        require(earlier==read(previous/'source-identities.json'),'Previous published identities differ')
    return old

def safe_path(root,relative):
    p=Path(relative)
    require(not p.is_absolute() and '..' not in p.parts,'Unsafe external evidence path')
    path=(root/p).resolve()
    require(root.resolve() in path.parents,'External evidence path escapes root')
    return path

def check_statement(pair,entry,report):
    require(pair['key']==KEY and entry['tag']==pair['tag'] and entry['catalogue']==pair['catalogue_path'],'Complete statement identity differs')
    require(report['key']==KEY.split('/',1)[1] and report['source']=='Android could not find an app to open this link.','Complete source statement differs')
    require(hashlib.sha256(report['source'].encode()).hexdigest()==pair['source_utf8_sha256'],'Reviewed source hash differs')
    require(hashlib.sha256(entry['text'].encode()).hexdigest()==entry['text_sha256']==pair['target_utf8_sha256'],'Complete target/hash differs')
    require(isinstance(entry.get('full_statement_review'),str) and bool(entry['full_statement_review'].strip()),'Full-statement review absent')
    require(hashlib.sha256(entry['full_statement_review'].encode()).hexdigest()==pair['review_conclusion_sha256'],'Original review conclusion/limit changed')
    disposition=entry['disposition']
    require(disposition in ALLOWED and disposition==pair['review_disposition'],'Original full-review disposition changed')
    require(entry.get('reviewer_confidence')==pair['reviewer_confidence'],'Original confidence changed')
    require(entry.get('native_speaker_certification') is False and entry.get('runtime_ui_verification') is False,'Review falsely promoted to native/runtime certification')
    isopen=pair['tag'] in OPEN
    require(isopen==(disposition=='limited_full_statement_review_unresolved_idiom'),'Unresolved idiom incorrectly classified')
    require(pair['state']==('needs_rereview' if isopen else 'reviewed_current'),'Open/full-current classification differs')
    require(type(pair['test_convention']) is bool and pair['test_convention']==(pair['tag'] in {'en-XV','qaa-Zsye-XV'}),'Layout convention promoted to language review')
    return entry

def check_review_documents(docs,index):
    require(value_hash(index)==EXPECTED['index'],'Pinned gallery evidence index changed')
    report=docs['complete-statement-review.json'];binding=docs['source-binding.json'];correction=docs['sdk-fixture-correction.json'];hosted=docs['hosted-verification.json']
    require(len(report['entries'])==59 and len({e['tag'] for e in report['entries']})==59,'Incomplete/duplicate statement scope')
    require(set(report['unresolved_low_idiom_confidence_tags'])==OPEN and report['limits']==index['original_limits'],'Original idiom limits lost')
    require(len(index['complete_pairs'])==59 and len({(p['tag'],p['key']) for p in index['complete_pairs']})==59,'Wrong complete pair scope')
    for pair in index['complete_pairs']:check_statement(pair,position.resolve_pointer(report,pair['pointer']),report)
    require(sum(p['state']=='reviewed_current' for p in index['complete_pairs'])==54 and sum(p['state']=='needs_rereview' for p in index['complete_pairs'])==5,'Bounded/current/open totals differ')
    require(binding['complete_statement_review_sha256']==index['reports']['complete-statement-review.json']['sha256'],'Original complete-report binding differs')
    require(binding['default_text']==report['source'] and binding['default_text_sha256']==hashlib.sha256(report['source'].encode()).hexdigest(),'Default English not bound')
    require(binding['all_59_statements_match_review_and_fixture'] is True,'Original canonical binding absent')
    require(binding['all_59_bindings']==[{'tag':e['tag'],'text_sha256':e['text_sha256']} for e in report['entries']],'Original all-59 binding differs')
    require(binding['expected_application_tree']==correction['failed_application_tree']=='faa0cf1d9976061ca970c92a8625e11febbc3929' and correction['expected_corrected_tree']==TREE,'Earlier/current source transition lost')
    require({f['path'] for f in correction['files']}=={'Paintroid/build.gradle','Paintroid/src/test/java/org/catrobat/paintroid/local/GalleryExternalLinkTest.kt'},'Test-only correction scope changed')
    require(hosted['tested_tree']==TREE and hosted['tested_merge_commit']=='515078d1c4d11323bb88347df0d5e413a25ee343','Hosted test source identity changed')
    require(hosted['junit']['passed_by_sdk']=={'30':6,'35':6} and hosted['junit']['expected_unique_methods']==6 and hosted['junit']['testcase_elements']==12,'Bounded JVM result count differs')
    require(all(hosted['junit'][k]==[] for k in ('missing','unexpected','duplicate')) and all(hosted['junit']['suite'][k]=='0' for k in ('skipped','failures','errors')),'Hosted failures/skips omitted')
    require(len(hosted['cases'])==12 and len({(x['method'],x['sdk']) for x in hosted['cases']})==12 and all(x['result']=='passed' for x in hosted['cases']),'Incomplete JVM test identities')
    return report

def check_reports(evidence_root,index):
    require(value_hash(index)==EXPECTED['index'],'Pinned gallery evidence index changed')
    docs={}
    for name,b in index['reports'].items():
        require(b['durable_revision']==EREV and b['durable_receipt']=='https://github.com/c933103/AN-Paint/blob/'+EREV+'/'+b['archive_path'],'Gallery evidence is not exact immutable binding')
        data=safe_path(evidence_root,b['path']).read_bytes()
        require(len(data)==b['size'] and hashlib.sha256(data).hexdigest()==b['sha256'] and blob_hash(data)==b['git_blob_sha1'],'Gallery complete evidence bytes differ: '+name)
        docs[name]=json.loads(data)
    check_review_documents(docs,index)
    return docs

def check_source(source,ids,counts,fixture,index,report):
    require(ids['source_revision']==counts['source_revision']==fixture['source_revision']==REV and fixture['source_tree']==TREE,'Wrong merged source')
    require(value_hash(fixture)==EXPECTED['fixture'] and ids['merged_gallery_rebinding']==fixture,'Current source/context fixture changed')
    require(value_hash(ids)==EXPECTED['source_ids'],'Exact source identities changed')
    require(value_hash(counts)==EXPECTED['counts'],'Current counts/policy/language limits changed')
    require(len(ids['current_source_files'])==182 and len({x['path'] for x in ids['current_source_files']})==182,'Incomplete resource identity scope')
    for x in ids['current_source_files']+fixture['source_context_files']:
        data=safe_path(source,x['path']).read_bytes()
        require(blob_hash(data)==x['git_blob_sha'] and hashlib.sha256(data).hexdigest()==x['sha256'],'Merged source/context bytes changed: '+x['path'])
    english=values(source/'Paintroid/src/main/res/values/strings.xml')
    require(len(english)==707 and set(english)==set(ids['resource_keys']) and set(english)-set(ids['previous_resource_manifest_at_gallery_merge']['resource_keys'])=={KEY},'New denominator/key identity differs')
    require(counts['denominator']=={'strings':706,'plural_resources':1,'total':707},'Typed denominator differs')
    cats={r['tag']:values(source/r['catalogue_path']) for r in counts['languages']}
    require({p['tag'] for p in index['complete_pairs']}=={r['tag'] for r in counts['languages'] if r['present']==707},'Reviewed scope/catalogue identities differ')
    for row in counts['languages']:
        present=sum(bool(x) for k,x in cats[row['tag']].items() if k in english)
        require(row['present']==present and row['missing']==707-present,'Actual catalogue partition differs')
    for p in index['complete_pairs']:
        entry=position.resolve_pointer(report,p['pointer'])
        require(english[KEY]==report['source'] and cats[p['tag']][KEY]==entry['text'],'Complete report differs from merged source')
    importance=read(source/'translations/string-importance.json');tier={k:t['id'] for t in importance['tiers'] for k in t['keys']}
    require(tier[KEY]=='P2' and all(tier[k]=='P2' for k in position.NEW_KEYS) and tier[position.legacy.HELP_KEY]=='P3','Operational/general Help priority changed')
    return english,cats

def check_new_receipts(receipts,index,english,cats,report):
    new=[r for r in receipts['receipts'] if r['cohort']==COHORT]
    require(value_hash(new)==EXPECTED['new_receipts'],'Exact new receipt dispositions, confidence, holds or evidence changed')
    require(len(new)==59 and len(receipts['receipts'])==3415,'New or prior active records omitted')
    allpairs={(r['tag'],r['key']):r for r in receipts['receipts']}
    require(len(allpairs)==3415,'Duplicate active pair')
    require({(r['tag'],r['key']) for r in new}=={(p['tag'],p['key']) for p in index['complete_pairs']},'New pair identities differ')
    for r in receipts['receipts']:
        require(r['current_english_sha256']==value_hash(english[r['key']]) and r['current_localized_sha256']==value_hash(cats[r['tag']][r['key']]),'Active full source hash differs')
    for p in index['complete_pairs']:
        r=allpairs[p['tag'],p['key']];e=position.resolve_pointer(report,p['pointer'])
        require(r['state']==p['state'] and r['original_review_disposition']==e['disposition'] and r['reviewer_confidence']==e.get('reviewer_confidence'),'Receipt changed original review decision/confidence')
        require((r.get('finding_status')=='open')==(p['tag'] in OPEN),'Unresolved idiom hidden or invented')
        require(r['reviewed_english_sha256']==r['current_english_sha256'] and r['reviewed_localized_sha256']==r['current_localized_sha256'],'Review/current source mismatch')
    return new

def check_document_links(directory):
    """Resolve only newly authored links using the actual repository layout.

    Flat preparation fixtures map to the same logical published locations;
    preceding overviews/history are deliberately outside this new-link gate.
    """
    prefix='verification/translation-entry-review-2026-10-13/'
    documents=('TRANSLATION_PROGRESS.md','current-entry-review.md','README.md','gallery-reconciliation-report-20261015.md')
    checked=0
    for name in documents:
        text=position.document_path(directory,name).read_text()
        if name in ('TRANSLATION_PROGRESS.md','current-entry-review.md'):
            text=text.split('### Current per-language entry counts',1)[0]
        logical=name if name=='TRANSLATION_PROGRESS.md' else prefix+name
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
            parsed=urlsplit(target)
            if parsed.scheme or parsed.netloc:continue
            require(bool(parsed.path) and not parsed.path.startswith('/'),'New relative link has no repository file target')
            resolved=posixpath.normpath(posixpath.join(posixpath.dirname(logical),parsed.path))
            require(resolved.startswith(prefix) and '..' not in Path(resolved).parts,'New relative link resolves outside tracker data: '+logical+' -> '+target)
            path=directory/resolved[len(prefix):]
            require(path.is_file(),'New relative link target missing: '+logical+' -> '+target)
            checked+=1
    require(checked==4,'New overview/README evidence links missing or changed')
    return checked


def validate(source,previous=None,directory=HERE,evidence_root=None):
    evidence_root=position.evidence_location(directory,evidence_root)
    summary=validate_internal(directory)
    receipts=read(directory/'entry-review-receipts.json');counts=read(directory/'entry-review-counts.json');ids=read(directory/'source-identities.json');fixture=read(directory/FIXTURE);index=read(directory/INDEX)
    require(summary['source_revision']==REV,'Wrong current revision')
    old=check_preservation(receipts,ids,previous)
    docs=check_reports(evidence_root,index)
    english,cats=check_source(source,ids,counts,fixture,index,docs['complete-statement-review.json'])
    check_new_receipts(receipts,index,english,cats,docs['complete-statement-review.json'])
    require(receipts['cohorts'][COHORT]=={'source_revision':REV,'complete_review_index':INDEX,'reports':index['reports'],'scope':index['scope'],'counts':{'full_statement_reviews':59,'reviewed_current':54,'needs_rereview':5,'accepted_natural_or_regional':52,'accepted_test_conventions':2},'requirements_closed':[]},'Gallery cohort acceptance scope changed')
    # Directly reuse strict existing semantic/history gates on unchanged receipts.
    oldindex=read(directory/position.INDEX);oldfixture=read(directory/position.FIXTURE)
    require(value_hash(oldindex)==position.EXPECTED['index_sha256'] and value_hash(oldfixture)==position.EXPECTED['reconciliation_fixture_sha256'],'Position evidence/acceptance checkpoint changed')
    position.check_reports(evidence_root,oldindex)
    position.check_new_receipts(old,oldindex,counts,english,cats)
    historical=position.check_preservation(old,ids,oldfixture)
    legacy=position.legacy;legacyfixture=read(directory/legacy.FIXTURE)
    legacy.check_history(historical,legacyfixture);legacy.check_review_artifacts(directory,legacyfixture,source=None)
    historicalpairs=read(directory/'fr-assembly-merged-reconciliation-20261015.json')['complete_french_pairs']+read(directory/'four-crop-merged-reconciliation-20261015.json')['complete_crop_pairs']
    legacy.check_pairs(historical,historicalpairs,legacyfixture,english,cats)
    position.document_path(directory,'TRANSLATION_PROGRESS.md')
    tables=legacy.check_tables(directory,counts)
    link_count=check_document_links(directory)
    body_path=directory/'new-body.md'
    if body_path.exists():
        body=body_path.read_text()
        require(len(body)<4000 and all(x in body for x in ('Intentional draft','5ece04b6','707','120,897','3,386','29 open','44,198','73,284','54 bounded','five open')),'Compact current PR body facts missing')
    validation=read(directory/'validation.json')
    require(validation['preceding_tracker_revision']==OLDHEAD and validation['summary']==counts['summary'] and validation['new_unique_records']==59 and validation['new_reviewed_current']==54 and validation['new_open_idiom_reviews']==5,'Validation scope/counts changed')
    if previous:
        require(validation['prior_checkpoint_validation']==read(previous/'validation.json'),'Prior validation history changed')
        for name in ('TRANSLATION_PROGRESS.md','current-entry-review.md'):
            current=position.document_path(directory,name).read_text();prior=position.document_path(previous,name).read_text()
            require(current.split('### Preserved earlier review checkpoints',1)[1]==prior.split('### Preserved earlier review checkpoints',1)[1],'Historical checkpoint prose changed')
            require(prior.split('### Current per-language entry counts',1)[0] in current,'Pre-gallery overview omitted')
        for name in (position.INDEX,position.FIXTURE,'materialize_position_review_evidence.py','validate_position_reconciliation.py','test_position_reconciliation.py','position-reconciliation-report-20261015.md'):
            require((directory/name).read_bytes()==(previous/name).read_bytes(),'Prior strict acceptance/report/test artifact changed: '+name)
    return {'status':'PASS','source_revision':REV,'source_tree':TREE,'preceding_tracker_revision':OLDHEAD,'active_pairs':3415,'new_full_statement_records':59,'new_reviewed_current':54,'new_open_idiom_reviews':5,'preserved_active_pairs':3356,'processing_holds':4,'source_identity_files':182,'source_context_files':len(fixture['source_context_files']),'table_files':tables,'new_relative_links':link_count,'previous_checkpoint_compared':bool(previous),'summary':counts['summary'],'scope':'Mechanical source/evidence binding with all earlier strict acceptance/history gates. No new linguistic decision or app/native execution.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('previous',type=Path,nargs='?');p.add_argument('--evidence-root',type=Path);a=p.parse_args();print(json.dumps(validate(a.source,a.previous,evidence_root=a.evidence_root),indent=2))
