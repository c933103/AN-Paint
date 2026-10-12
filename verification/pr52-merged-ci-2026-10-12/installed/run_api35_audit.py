#!/usr/bin/env python3
"""Reproduce all current selected API35 installed gates. No Android execution.
API30 is explicitly unselected and never copied into a fresh-run matrix.
"""
import argparse,hashlib,json,os,pathlib,subprocess,sys
from audit_natural_artifacts import HEAD,MERGE,TREE,RUN,SOURCE_SHA
p=argparse.ArgumentParser(description=__doc__)
for k in ('repo','artifacts','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
p.add_argument('--receipt-only',action='store_true');a=p.parse_args();a.repo=a.repo.resolve();a.artifacts=a.artifacts.resolve();a.output=a.output.resolve()
if a.output.exists():raise ValueError('use a fresh output directory')
a.output.mkdir(parents=True);here=pathlib.Path(__file__).resolve().parent;env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'}
def run(name,*args,script=None):
 r=subprocess.run([sys.executable,str(script or here/(name+'.py')),*map(str,args)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (a.output/(name+'.log')).write_bytes(r.stdout)
 if r.returncode:raise RuntimeError(name+' failed; inspect local audit log')
 print(name+' PASS',flush=True)
run('audit_source_inputs','--repo',a.repo,'--output',a.output/'source-input-result.json')
run('audit_deadlines','--repo',a.repo,'--output',a.output/'deadline-result.json')
if not a.receipt_only:run('audit_installed_archives','--artifacts',a.artifacts,'--apis',35,'--output',a.output/'installed-archive-result.json')
run('audit_installed_matrix','--repo',a.repo,'--artifact-root',a.artifacts,'--apis',35,'--output',a.output/'installed-matrix-result.json')
args=['--repo',a.repo,'--artifacts',a.artifacts,'--apis',35,'--output',a.output/'prebuilt-provenance-result.json']
if a.receipt_only:args.append('--receipt-only')
run('audit_prebuilt_provenance',*args)
run('audit_platform_locale_binding','--repo',a.repo,'--artifacts',a.artifacts,'--matrix',a.output/'installed-matrix-result.json','--provenance',a.output/'prebuilt-provenance-result.json','--output',a.output/'platform-locale-binding-result.json')
run('audit_restart_boundary','--artifacts',a.artifacts,'--output',a.output/'restart-boundary-result.json')
root=a.artifacts/'api35';records=a.output/'installed-observed'
run('installed_strict_decoder','--raw-output',root/'app/androidTest-results/instrumentation.log','--expected-source-sha256',SOURCE_SHA,'--runner-summary',root/'app/androidTest-results/summary.json','--source-tests',a.repo/'app/src/androidTest','--output-dir',records,script=a.repo/'tools/installed_glyph_ink_evidence.py')
run('audit_installed_pixels','--repo',a.repo,'--records',records,'--output',a.output/'installed-pixel-result.json')
raw=(root/'logcat.txt').read_bytes();bp=a.output/'natural-update-binding.json';bp.write_text(json.dumps(dict(head=HEAD,merge=MERGE,tree=TREE,run_id=int(RUN),source_tests_sha256=SOURCE_SHA,logcat_sha256=hashlib.sha256(raw).hexdigest()),indent=2)+'\n')
run('audit_natural_update','--logcat',root/'logcat.txt','--records',records,'--binding',bp,'--output',a.output/'natural-update-result.json')
run('audit_native_vertical','--repo',a.repo,'--artifacts',a.artifacts,'--apis',35,'--output',a.output/'native-vertical')
m=json.loads((a.output/'installed-matrix-result.json').read_bytes())
if set(m['matrices'])!={'35'}:raise ValueError('current matrix must be API35 only')
r=dict(head=HEAD,tree=TREE,merge=MERGE,run_id=int(RUN),audit_integrity_status='PASS',installed_gate_status=m['installed_gate_status'],selected_apis=[35],api30_status='NOT_SELECTED_IN_CURRENT_RUN',platform_locale_discovery_status='PASS_BOUND_INSTALLED_PLATFORM_LOCALE_DISCOVERY',native_vertical_status='PASS_BOUNDED_NATIVE_VERTICAL',matrices={api:{k:x[k] for k in ('status','scheduled','completed','passed','failed','missing_phases')} for api,x in m['matrices'].items()},input_mode='RECEIPT_ONLY_COMPACT_SUPPORT' if a.receipt_only else 'ORIGINAL_CURRENT_CI_ARTIFACTS',scope='Fresh source-bound phase identities/protocol/terminal/raw XML, same-run prebuilt install receipts, LocaleConfig167, strict Arabic full rasters and natural-update, restart and native input/geometry. Actual screenshot inspection remains separate. No API30 current execution, new Android execution, hardware/network/release/linguistic claim.')
(a.output/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if r['installed_gate_status']!='PASS':sys.exit(1)
