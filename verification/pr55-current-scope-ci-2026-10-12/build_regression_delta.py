#!/usr/bin/env python3
"""Evidence-only delta against the immutable e19 replay inputs; no source gate."""
import argparse,hashlib,json,pathlib,zipfile
p=argparse.ArgumentParser();p.add_argument('--artifact-root',type=pathlib.Path,required=True);p.add_argument('--prior-review',type=pathlib.Path,required=True);p.add_argument('--binding',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
b=json.loads(a.binding.read_text());prior=json.loads((a.prior_review/'regression-replay-manifest.json').read_text());old_zip=a.prior_review/'regression-replay-inputs.zip'
if sha(old_zip.read_bytes())!=prior['zip_sha256']:raise ValueError('prior replay archive digest changed')
roots=['Paintroid/build/test-results/testDebugUnitTest','Paintroid/build/reports/commons-metadata-m04','Paintroid/build/reports/commons-metadata-m04-diagnostic','Paintroid/build/reports/commons-metadata-m04-painted-ink','build/reports/ci-phases'];files=[]
for directory in roots:
 files.extend(f for f in (a.artifact_root/directory).rglob('*') if f.is_file() and (directory!='Paintroid/build/test-results/testDebugUnitTest' or f.suffix=='.xml'))
files.extend(f for f in (a.artifact_root/'Paintroid/build/reports/localized-dialog-layout').glob('*retained-vertical*') if f.is_file())
files=sorted(set(files));old={x['path']:x for x in prior['files']};rows=[];target=a.out/'regression-current-delta.zip'
with zipfile.ZipFile(old_zip) as origin,zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as delta:
 for f in files:
  name=str(f.relative_to(a.artifact_root));raw=f.read_bytes();row={'path':name,'bytes':len(raw),'sha256':sha(raw)}
  same=name in old and origin.read(name)==raw
  row['input']='immutable_e19_replay' if same else 'current_delta'
  if not same:
   info=zipfile.ZipInfo(name,(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;delta.writestr(info,raw)
  rows.append(row)
r={'purpose':'Preserve fresh raw XML/JSON/phase logs while reusing only exact-matching immutable e19 members; evidence replay only, no permanent CI snapshot requirement.','run':b['run_id'],'head':b['head'],'tree':b['tree'],'original_artifact_id':b['regression_artifact_id'],'original_artifact_sha256':b['regression_artifact_sha256'],'prior_evidence_commit':'f066e90b8fc7682023e0bf260da55959e6ebf9e5','prior_replay_path':'verification/pr55-platform-locale-ci-2026-10-12/regression-replay-inputs.zip (transport parts may require reconstruction)','prior_zip_sha256':prior['zip_sha256'],'prior_manifest_sha256':sha((a.prior_review/'regression-replay-manifest.json').read_bytes()),'delta_zip_sha256':sha(target.read_bytes()),'delta_zip_bytes':target.stat().st_size,'files':rows,'current_delta_members':sum(x['input']=='current_delta' for x in rows),'reused_exact_members':sum(x['input']=='immutable_e19_replay' for x in rows),'selected_members':len(rows),'removed_prior_members':sorted(old.keys()-{r['path'] for r in rows})}
(a.out/'regression-delta-manifest.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('current_delta_members','reused_exact_members','selected_members','delta_zip_bytes')},indent=2))
