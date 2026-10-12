#!/usr/bin/env python3
"""Reproduce raw evidence checks after artifact expiry, without claiming outer ZIP rehash."""
import argparse,hashlib,json,pathlib,sys,tempfile,zipfile
import audit_platform_artifacts as app
import audit_platform_ink as ink
import audit_retained_notice as notice
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--evidence',type=pathlib.Path,default=pathlib.Path(__file__).parent);a=p.parse_args();e=a.evidence
manifest=json.loads((e/'regression-replay-manifest.json').read_text());raw=(e/'regression-replay-inputs.zip').read_bytes();app.require(hashlib.sha256(raw).hexdigest()==manifest['zip_sha256'],'replay ZIP hash')
with tempfile.TemporaryDirectory() as td:
 root=pathlib.Path(td)
 with zipfile.ZipFile(e/'regression-replay-inputs.zip') as z:
  app.require(len(z.namelist())==len(set(z.namelist()))==manifest['file_count'],'replay duplicate/count')
  app.require(set(z.namelist())=={r['path'] for r in manifest['files']},'replay member set')
  for row in manifest['files']:
   path=pathlib.PurePosixPath(row['path']);app.require(not path.is_absolute() and '..' not in path.parts and '\\' not in row['path'],'unsafe replay path')
   data=z.read(row['path']);app.require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'replay member digest')
   target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 sys.path.insert(0,str(a.repo/'tools'));inventory=app.current_inventory(a.repo);messages=app.messages(a.repo);base=root/'Paintroid/build'
 result={'junit':app.junit_audit(base/'test-results/testDebugUnitTest',inventory['expected']),'success_renders':app.render_audit(base/'reports/commons-metadata-m04',messages),'diagnostics':app.diagnostic_audit(base/'reports/commons-metadata-m04-diagnostic',messages),'painted_ink':ink.audit(base/'reports/commons-metadata-m04-painted-ink',messages)}
 notice_result=notice.audit(base/'reports/localized-dialog-layout')
 app.require(notice_result==json.loads((e/'retained-notice-audit.json').read_text()),'retained notice replay differs')
 expected=json.loads((e/'regression-audit.json').read_text())
 for key,value in result.items():app.require(value==expected[key],'replayed section differs '+key)
 outcome={'status':'PASS_EXACT_REPLAY','sections_equal':list(result)+['retained_notice'], 'retained_notice_pairs':notice_result['checked_pairs'],'current_source_jvm_identities':len(inventory['expected']),'original_success_pairs':result['success_renders']['complete_pairs_checked'],'ink_frames':result['painted_ink']['checked_frames'],'native_mutations':sum(r.get('rejected_native_mutants',0) for r in result['painted_ink']['control_receipts']),'review_required_positives':result['painted_ink']['positive_review_required'],'replay_zip_sha256':manifest['zip_sha256'],'scope':'Per-member authenticated raw evidence subset. Original outer-artifact ZIP/APK/source rehash is not replayed; original audit records those results separately.'}
 a.output.write_text(json.dumps(outcome,indent=2)+'\n');print(json.dumps(outcome,indent=2))
