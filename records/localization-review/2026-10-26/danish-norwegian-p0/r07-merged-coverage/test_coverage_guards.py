"""Exercise real positive inputs and isolated malformed/corrupted copies, without changing source."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import xml.etree.ElementTree as ET
import recompute_delta as compute
import verify_independently as verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','report','baseline-report','baseline-source-root','review-dir','source-tree-file'):
        parser.add_argument('--' + name,type=Path,required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--source-tree', required=True)
    args = parser.parse_args()
    result = verify.run(args)
    cases = []
    def rejected(label, action):
        try:
            action()
        except (ValueError, KeyError, FileNotFoundError, ET.ParseError):
            cases.append({'case':label,'rejected':True})
        else:
            raise RuntimeError('Mutation accepted: ' + label)
    rejected('duplicate JSON key',lambda:json.loads('{"x":1,"x":2}',object_pairs_hook=compute.unique))
    for label,raw in [
        ('malformed XML',b'<resources>'),
        ('wrong XML root',b'<strings/>'),
        ('missing resource name',b'<resources><string>x</string></resources>'),
        ('duplicate resource name',b'<resources><string name="x">one</string><string name="x">two</string></resources>'),
        ('empty string',b'<resources><string name="x"/></resources>'),
        ('empty plural container',b'<resources><plurals name="x"/></resources>'),
        ('duplicate plural quantity',b'<resources><plurals name="x"><item quantity="one">one</item><item quantity="one">two</item></plurals></resources>')]:
        rejected(label,lambda raw=raw:compute.parse(raw))
    for text in ('bad %','bad %q','bad %1$','bad %3$.f'):
        rejected('malformed format token ' + text,lambda text=text:compute.tokens(text))
    tree = compute.read(args.source_tree_file)
    broken = deepcopy(tree);broken['truncated'] = True
    rejected('truncated source tree',lambda:compute.verify_tree(broken,args.source_tree))
    broken = deepcopy(tree);broken['tree'].append(broken['tree'][0])
    rejected('duplicate tree path',lambda:compute.verify_tree(broken,args.source_tree))
    broken = deepcopy(tree);broken['tree'][-1]['sha'] = '0'*40
    rejected('tree Merkle hash corruption',lambda:compute.verify_tree(broken,args.source_tree))
    mutations = [
        ('missing locale row','structural-per-locale.json',lambda d:d.pop()),
        ('duplicate locale row','structural-per-locale.json',lambda d:d.append(d[0])),
        ('wrong row presence','structural-per-locale.json',lambda d:d[0].__setitem__('P0_present',d[0]['P0_present']+1)),
        ('wrong aggregate','coverage-delta.json',lambda d:d['presence_totals'].__setitem__('all_present',0)),
        ('wrong delta','coverage-delta.json',lambda d:d['presence_delta'].__setitem__('P0_present',0)),
        ('unverified CI/production mislabel','coverage-delta.json',lambda d:d.__setitem__('source_status','merged production')),
        ('wrong explicit source commit','coverage-delta.json',lambda d:d.__setitem__('source_commit','0'*40)),
        ('wrong develop ref receipt','source-identity.json',lambda d:d.__setitem__('develop_at_check','0'*40)),
        ('wrong merge parent receipt','source-identity.json',lambda d:d.__setitem__('parents',[])),
        ('wrong signature receipt','source-identity.json',lambda d:d.__setitem__('signature_verified',False)),
        ('wrong merge commit receipt','source-identity.json',lambda d:d.__setitem__('merge_commit','0'*40)),
        ('unverified postmerge success','source-identity.json',lambda d:d.__setitem__('actual_postmerge_status','success')),
        ('wrong postmerge run','coverage-delta.json',lambda d:d['workflow_results'].__setitem__('postmerge_run_id',1)),
        ('duplicate coverage input','source-bindings.json',lambda d:d['files'].append(d['files'][0])),
        ('wrong coverage SHA256','source-bindings.json',lambda d:d['files'][0].__setitem__('sha256','0'*64)),
        ('duplicate review pair','review-scope-reconciliation.json',lambda d:d['new_review_scopes'].append(d['new_review_scopes'][0])),
        ('missing review pair','review-scope-reconciliation.json',lambda d:d['new_review_scopes'].pop()),
        ('changed accepted target','review-scope-reconciliation.json',lambda d:d['new_review_scopes'][0].__setitem__('accepted_display_text','changed')),
        ('omitted entry qualification','review-scope-reconciliation.json',lambda d:d['new_review_scopes'][0].__setitem__('receipt_qualifications',{})),
        ('omitted global qualification','review-scope-reconciliation.json',lambda d:d['new_review_scopes'][0].__setitem__('receipt_global_boundaries',{})),
        ('fabricated global acceptance','review-scope-reconciliation.json',lambda d:d.__setitem__('global_accepted_count',156))]
    for label,name,mutation in mutations:
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp)
            for path in args.report.glob('*'):
                if path.is_file():
                    shutil.copyfile(path,report/path.name)
            data = compute.read(report/name);mutation(data)
            (report/name).write_text(json.dumps(data),encoding='utf-8')
            changed = SimpleNamespace(**vars(args));changed.report=report
            rejected(label,lambda:verify.run(changed))
    with tempfile.TemporaryDirectory() as temp:
        report = Path(temp)
        for path in args.report.glob('*'):
            if path.is_file():shutil.copyfile(path,report/path.name)
        path = report/'structural-per-locale.csv';path.write_text(path.read_text().replace(',171,',',999,',1) + path.read_text().splitlines()[1]+'\n')
        changed = SimpleNamespace(**vars(args));changed.report=report
        rejected('CSV extra row',lambda:verify.run(changed))
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        for entry in compute.read(args.report/'source-bindings.json')['files']:
            path=root/entry['path'];path.parent.mkdir(parents=True,exist_ok=True);path.symlink_to(args.source_root/entry['path'])
        path=root/'Paintroid/src/main/res/values-da/strings.xml';raw=path.read_bytes();path.unlink();path.write_bytes(raw+b'\n')
        changed=SimpleNamespace(**vars(args));changed.source_root=root
        rejected('source byte corruption',lambda:verify.run(changed))
        path.unlink()
        rejected('missing source file',lambda:verify.run(changed))
    output={'source_commit':result['source_commit'],'source_status':result['source_status'],
            'positive_all_rows_and_scopes_validation_passed':True,'negative_controls':len(cases),'all_negative_controls_rejected':True,'cases':cases,
            'source_or_review_files_modified':False}
    (args.report/'mutation-controls.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'positive_validation':True,'negative_controls':len(cases),'all_rejected':True},indent=2))


if __name__ == '__main__':main()
