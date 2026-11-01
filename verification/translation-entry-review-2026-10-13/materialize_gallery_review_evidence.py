#!/usr/bin/env python3
"""Verify the separate PR85 evidence checkout and add its exact files to an external cache.

Usage: python materialize_gallery_review_evidence.py EVIDENCE_CHECKOUT EXTERNAL_ROOT
Materialize the preserved position evidence separately into the same external root.
No network requests. All input bytes and full-statement decisions are checked before output.
"""
import argparse
import hashlib
import json
from pathlib import Path
import validate_gallery_reconciliation as v

def external_cache_boundary(archive,output):
    """Reject overlap with the evidence checkout or actual tracker repository."""
    archive=Path(archive).resolve();output=Path(output).resolve();tracker=Path(v.HERE).resolve()
    if tracker.name=='translation-entry-review-2026-10-13' and tracker.parent.name=='verification':
        tracker=tracker.parents[1]
    for root,label in ((archive,'evidence checkout'),(tracker,'tracker repository')):
        v.require(output!=root and root not in output.parents and output not in root.parents,
                  'Output must not overlap the '+label)
    return archive,output


def materialize(archive,output,index_path=v.HERE/v.INDEX):
    archive=Path(archive).resolve();output=Path(output).resolve()
    v.require(archive.is_dir(),'Separate evidence checkout unavailable')
    external_cache_boundary(archive,output)
    index=v.read(Path(index_path));v.require(v.value_hash(index)==v.EXPECTED['index'],'Pinned gallery evidence index changed')
    contents={};docs={}
    for name,b in index['reports'].items():
        data=v.safe_path(archive,b['archive_path']).read_bytes()
        v.require(len(data)==b['size'] and hashlib.sha256(data).hexdigest()==b['sha256'] and v.blob_hash(data)==b['git_blob_sha1'],'Archive bytes differ: '+name)
        v.safe_path(output,b['path']);contents[name]=data;docs[name]=json.loads(data)
    v.check_review_documents(docs,index)
    for name,b in index['reports'].items():
        target=v.safe_path(output,b['path']);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(contents[name])
    v.check_reports(output,index)
    return {'status':'PASS','artifacts':len(contents),'bytes':sum(map(len,contents.values())),'complete_statement_records':59,'reviewed_current':54,'open_idiom_reviews':5,'evidence_root':str(output),'network_requests':0,'new_linguistic_decisions':0}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('evidence_checkout',type=Path);p.add_argument('external_root',type=Path);p.add_argument('--index',type=Path,default=v.HERE/v.INDEX);a=p.parse_args();print(json.dumps(materialize(a.evidence_checkout,a.external_root,a.index),indent=2))
