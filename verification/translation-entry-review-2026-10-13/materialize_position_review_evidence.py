#!/usr/bin/env python3
"""Verify and materialize position reports from a separately obtained evidence checkout.

Usage: python materialize_position_review_evidence.py EVIDENCE_CHECKOUT EXTERNAL_OUTPUT_ROOT
The input checkout contains verification/assembly-position-review-20261015/.
No network request is made. Every report must match the immutable index's exact
Git blob SHA1, SHA256 and byte count before any output is created. Full-value
acceptance/pointer checks also run. A URL or checkout name alone proves nothing.
"""
import argparse
import hashlib
import json
from pathlib import Path
import validate_position_reconciliation as v


def safe_path(root,relative):
    path=Path(relative)
    v.require(not path.is_absolute() and '..' not in path.parts,'Unsafe evidence relative path')
    resolved=(root/path).resolve()
    v.require(root==resolved or root in resolved.parents,'Evidence path escapes its explicit root')
    return resolved


def materialize(archive_root,output_root,index_path=v.HERE/v.INDEX):
    archive_root=Path(archive_root).resolve()
    output_root=Path(output_root).resolve()
    v.require(archive_root.is_dir(),'Evidence checkout is unavailable')
    v.require(output_root!=archive_root and archive_root not in output_root.parents,'Output must be external to the evidence checkout')
    v.require(output_root!=v.HERE.resolve() and v.HERE.resolve() not in output_root.parents,'Output must be external to the tracker directory')
    index=v.read(Path(index_path))
    v.require(v.value_hash(index)==v.EXPECTED['index_sha256'],'Evidence index differs from pinned complete reviews')
    contents={};reports={}
    for name,binding in index['reports'].items():
        data=safe_path(archive_root,binding['archive_path']).read_bytes()
        v.require(len(data)==binding['size'] and hashlib.sha256(data).hexdigest()==binding['sha256'] and v.blob_hash(data)==binding['git_blob_sha1'],'Evidence checkout bytes differ: '+name)
        safe_path(output_root,binding['path'])
        contents[name]=data
        reports[name]=json.loads(data)
    for pair in index['complete_pairs']:
        v.check_accepted_entry(pair,reports[pair['report']])
    # No output/cache mutation until every input and every complete acceptance passes.
    for name,binding in index['reports'].items():
        target=safe_path(output_root,binding['path'])
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(contents[name])
    v.check_reports(output_root,index)
    return {'status':'PASS','reports':len(reports),'bytes':sum(map(len,contents.values())),'complete_pairs':len(index['complete_pairs']),'evidence_root':str(output_root),'immutable_evidence_revisions':sorted({b['durable_revision'] for b in index['reports'].values()}),'network_requests':0,'scope':'Exact report content and full-value acceptance materialization only; no new language or runtime review.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence_checkout',type=Path)
    parser.add_argument('external_output_root',type=Path)
    parser.add_argument('--index',type=Path,default=v.HERE/v.INDEX)
    args=parser.parse_args()
    print(json.dumps(materialize(args.evidence_checkout,args.external_output_root,args.index),indent=2))
