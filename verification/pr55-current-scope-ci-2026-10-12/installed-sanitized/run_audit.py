#!/usr/bin/env python3
"""Reproduce this read-only frozen-tree audit into a fresh output directory.
Exit 0: all reviewed installed gates pass. Exit 1: integrity verified but a device
gate failed. Other failures propagate as audit errors. No Android device is run.
"""
from audit_natural_artifacts import SOURCE_SHA,LIBRARY_SHA
import argparse,hashlib,json,os,pathlib,subprocess,sys
from audit_natural_artifacts import HEAD,MERGE,TREE,RUN

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for k in ('repo','artifacts','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 a=p.parse_args();a.repo=a.repo.resolve();a.artifacts=a.artifacts.resolve();a.output=a.output.resolve()
 if a.output.exists():raise ValueError('Use a fresh output directory; preserved results are never overwritten')
 a.output.mkdir(parents=True); here=pathlib.Path(__file__).resolve().parent;env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'}
 def run(name,*args,script=None):
  command=[sys.executable,str(script or here/(name+'.py')),*map(str,args)]
  r=subprocess.run(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (a.output/(name+'.log')).write_bytes(r.stdout)
  if r.returncode:raise RuntimeError(name+' failed; see '+str(a.output/(name+'.log')))
 run('audit_source_inputs','--repo',a.repo,'--output',a.output/'source-input-result.json')
 run('audit_deadlines','--repo',a.repo,'--output',a.output/'deadline-result.json')
 run('audit_installed_archives','--artifacts',a.artifacts,'--output',a.output/'installed-archive-result.json')
 run('audit_installed_matrix','--repo',a.repo,'--artifact-root',a.artifacts,'--output',a.output/'installed-matrix-result.json')
 run('audit_prebuilt_provenance','--repo',a.repo,'--artifacts',a.artifacts,'--output',a.output/'prebuilt-provenance-result.json')
 run('audit_platform_locale_binding','--repo',a.repo,'--artifacts',a.artifacts,'--matrix',a.output/'installed-matrix-result.json','--provenance',a.output/'prebuilt-provenance-result.json','--output',a.output/'platform-locale-binding-result.json')
 run('audit_restart_boundary','--artifacts',a.artifacts,'--output',a.output/'restart-boundary-result.json')
 src=SOURCE_SHA;root=a.artifacts/'api35';records=a.output/'installed-observed'
 run('installed_strict_decoder','--raw-output',root/'app/androidTest-results/instrumentation.log','--expected-source-sha256',src,'--runner-summary',root/'app/androidTest-results/summary.json','--source-tests',a.repo/'app/src/androidTest','--output-dir',records,script=a.repo/'tools/installed_glyph_ink_evidence.py')
 run('audit_installed_pixels','--repo',a.repo,'--records',records,'--output',a.output/'installed-pixel-result.json')
 raw=(root/'logcat.txt').read_bytes();binding=dict(head=HEAD,merge=MERGE,tree=TREE,run_id=int(RUN),source_tests_sha256=src,logcat_sha256=hashlib.sha256(raw).hexdigest());bp=a.output/'natural-update-binding.json';bp.write_text(json.dumps(binding,indent=2)+'\n')
 run('audit_natural_update','--logcat',root/'logcat.txt','--records',records,'--binding',bp,'--output',a.output/'natural-update-result.json')
 run('audit_native_vertical','--repo',a.repo,'--artifacts',a.artifacts,'--output',a.output/'native-vertical')
 m=json.loads((a.output/'installed-matrix-result.json').read_bytes());result={'audit_integrity_status':'PASS','installed_gate_status':m['installed_gate_status'],'native_vertical_status':'PASS_BOUNDED_NATIVE_VERTICAL','platform_locale_discovery_status':'PASS_BOUND_INSTALLED_PLATFORM_LOCALE_DISCOVERY','matrices':{api:{k:x[k] for k in ('status','scheduled','completed','passed','failed','missing_phases')} for api,x in m['matrices'].items()},'scope':'Exact installed artifacts, raw protocols/XML, source inputs, strict native software rasters and natural-update/prebuilt/restart receipt consistency. Hardware/network/release/linguistic claims excluded.'}
 (a.output/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return 0 if result['installed_gate_status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
