#!/usr/bin/env python3
"""Reproduce current regression evidence using only its compact delta and e19 replay ZIP."""
import argparse,hashlib,json,pathlib,sys,tempfile,zipfile
import audit_platform_artifacts as app
import audit_platform_ink as ink
import audit_retained_notice as notice
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--prior-replay-zip',type=pathlib.Path,required=True);p.add_argument('--evidence',type=pathlib.Path,default=pathlib.Path(__file__).parent);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();e=a.evidence
m=json.loads((e/'regression-delta-manifest.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
app.require(sha(a.prior_replay_zip.read_bytes())==m['prior_zip_sha256'],'prior replay digest')
app.require(sha((e/'regression-current-delta.zip').read_bytes())==m['delta_zip_sha256'],'delta digest')
with tempfile.TemporaryDirectory() as td,zipfile.ZipFile(a.prior_replay_zip) as old,zipfile.ZipFile(e/'regression-current-delta.zip') as new:
 root=pathlib.Path(td)
 for archive in (old,new):
  app.require(len(archive.namelist())==len(set(archive.namelist())),'duplicate archive member')
  for name in archive.namelist():
   pp=pathlib.PurePosixPath(name);app.require(not pp.is_absolute() and '..' not in pp.parts and '\\' not in name,'unsafe archive member')
 app.require(set(new.namelist())=={r['path'] for r in m['files'] if r['input']=='current_delta'},'delta member set')
 app.require(len(m['files'])==len({r['path'] for r in m['files']})==m['selected_members'],'selected member count/duplicates')
 for row in m['files']:
  name=row['path'];pp=pathlib.PurePosixPath(name);app.require(not pp.is_absolute() and '..' not in pp.parts and '\\' not in name,'unsafe selected path')
  app.require(row['input'] in ('current_delta','immutable_e19_replay'),'unknown member source')
  raw=(new if row['input']=='current_delta' else old).read(name)
  app.require(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'selected member integrity')
  f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
 sys.path.insert(0,str(a.repo/'tools'));inv=app.current_inventory(a.repo);messages=app.messages(a.repo);base=root/'Paintroid/build'
 r={'junit':app.junit_audit(base/'test-results/testDebugUnitTest',inv['expected']),'success_renders':app.render_audit(base/'reports/commons-metadata-m04',messages),'diagnostics':app.diagnostic_audit(base/'reports/commons-metadata-m04-diagnostic',messages),'painted_ink':ink.audit(base/'reports/commons-metadata-m04-painted-ink',messages)}
 expected=json.loads((e/'regression-audit.json').read_text())
 for key,value in r.items():app.require(value==expected[key],'current replay differs '+key)
 n=notice.audit(base/'reports/localized-dialog-layout');app.require(n==json.loads((e/'retained-notice-audit.json').read_text()),'notice replay differs')
 result={'status':'PASS_EXACT_CURRENT_EVIDENCE_REPLAY','run':m['run'],'tree':m['tree'],'source_jvm_executions':len(inv['expected']),'success_pairs':r['success_renders']['complete_pairs_checked'],'diagnostic_profiles':r['diagnostics']['checked_profiles'],'ink_frames':r['painted_ink']['checked_frames'],'native_mutations':sum(x.get('rejected_native_mutants',0) for x in r['painted_ink']['control_receipts']),'notice_pairs':n['checked_pairs'],'selected_members':m['selected_members'],'current_delta_members':m['current_delta_members'],'reused_exact_members':m['reused_exact_members'],'limits':['Per-member raw evidence replay. Does not reconstruct original outer Actions ZIP or APK/source delivery.','Fresh source/run attribution comes from separately verified receipts, not prior image equality.']}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
