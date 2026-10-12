#!/usr/bin/env python3
"""Expiry-safe raw-evidence replay. Exact source checkout required; no CI artifact download.
Return 1 preserves the actual API30 gate failure. APK/outer-ZIP rehash is intentionally
not reproduced; original hash receipts remain available and explicitly distinguished.
"""
import argparse,json,os,pathlib,subprocess,sys,tarfile
from audit_natural_artifacts import HEAD,MERGE,TREE,RUN,require,sha

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();a.repo=a.repo.resolve();a.output=a.output.resolve();here=pathlib.Path(__file__).resolve().parent
 require(not a.output.exists(),'use a fresh output directory');a.output.mkdir(parents=True);rawroot=a.output/'inputs';rawroot.mkdir();results=a.output/'results';results.mkdir();manifest=json.loads((here/'replay-inputs/RAW-INPUTS.json').read_bytes());archive=here/'replay-inputs'/manifest['archive']['path'];data=archive.read_bytes()
 require(sha(data)==manifest['archive']['sha256'] and len(data)==manifest['archive']['bytes'],'raw archive binding differs');require(manifest['head']==HEAD and manifest['tree']==TREE and manifest['merge']==MERGE and manifest['run_id']==int(RUN),'raw source binding differs');expected={x['path']:x for x in manifest['files']};require(len(expected)==manifest['file_count'] and manifest['expanded_bytes']<=32*1024*1024,'raw inventory/budget differs')
 with tarfile.open(archive,'r:gz') as tar:
  members=tar.getmembers();require(len(members)==len(expected) and set(x.name for x in members)==set(expected),'tar member inventory differs')
  for member in members:
   q=pathlib.PurePosixPath(member.name);require(member.isfile() and not q.is_absolute() and '..' not in q.parts and '\\' not in member.name,'unsafe archive member');entry=expected[member.name];require(member.size==entry['bytes'],'member size differs');b=tar.extractfile(member).read();require(sha(b)==entry['sha256'],'member digest differs');dest=rawroot/member.name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'}
 def run(name,*args,script=None):
  result=subprocess.run([sys.executable,str(script or here/(name+'.py')),*map(str,args)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(results/(name+'.log')).write_bytes(result.stdout);require(result.returncode==0,name+' failed; inspect result log')
 run('audit_source_inputs','--repo',a.repo,'--output',results/'source-input-result.json')
 run('audit_installed_matrix','--repo',a.repo,'--artifact-root',rawroot,'--output',results/'installed-matrix-result.json')
 run('audit_prebuilt_provenance','--repo',a.repo,'--artifacts',rawroot,'--receipt-only','--output',results/'prebuilt-receipt-replay-result.json')
 run('audit_restart_boundary','--artifacts',rawroot,'--output',results/'restart-boundary-result.json')
 src='f8f8de6d967000411de5dc6a3e8a8309b6fd61f2eba9e4393556e3ad35fafe3e';root=rawroot/'emulator-api-35';records=results/'installed-observed'
 run('installed_strict_decoder','--raw-output',root/'app/androidTest-results/instrumentation.log','--expected-source-sha256',src,'--runner-summary',root/'app/androidTest-results/summary.json','--source-tests',a.repo/'app/src/androidTest','--output-dir',records,script=a.repo/'tools/installed_glyph_ink_evidence.py')
 for route in ('copy','insert'):
  for suffix in ('.json','-actual.png','-reference.png'):
   name=route+suffix;require((records/name).read_bytes()==(here/'installed-observed'/name).read_bytes(),'new decoding differs from preserved Arabic input '+name)
 run('audit_installed_pixels','--repo',a.repo,'--records',records,'--output',results/'installed-pixel-result.json')
 binding=dict(head=HEAD,merge=MERGE,tree=TREE,run_id=int(RUN),source_tests_sha256=src,logcat_sha256=sha((root/'logcat.txt').read_bytes()));bp=results/'natural-update-binding.json';bp.write_text(json.dumps(binding,indent=2)+'\n')
 run('audit_natural_update','--logcat',root/'logcat.txt','--records',records,'--binding',bp,'--output',results/'natural-update-result.json')
 m=json.loads((results/'installed-matrix-result.json').read_bytes());result={'receipt_replay_integrity_status':'PASS','installed_gate_status':m['installed_gate_status'],'head':HEAD,'tree':TREE,'run_id':int(RUN),'raw_inputs':len(expected),'expanded_bytes':manifest['expanded_bytes'],'matrices':{api:{k:x[k] for k in ('status','scheduled','completed','passed','failed','missing_phases')} for api,x in m['matrices'].items()},'not_repeated':['Outer original artifact ZIP hashing/extraction audit; original hashes and complete member manifests preserved.','APK and source payload hashing; original result preserved, payloads intentionally omitted.'],'scope':'Raw source-derived phase protocols/XML/summaries; exact strict decoded Arabic image records; independent raster recomputation; natural-update/full-log and prebuilt/restart receipts. No new Android run.'}
 (results/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return 0 if m['installed_gate_status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
