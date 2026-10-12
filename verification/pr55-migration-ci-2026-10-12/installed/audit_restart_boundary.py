#!/usr/bin/env python3
"""Read-only live-seed/force-stop boundary audit; complete phase identities are separate."""
import argparse,json,pathlib,re
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,require,sha

def audit(artifacts):
 root=artifacts/'emulator-api-35/app/accepted-credit-restart';raw=(root/'boundary.log').read_bytes();log=raw.decode();seed=json.loads((root/'seed/summary.json').read_bytes());verify=json.loads((root/'verify/summary.json').read_bytes());pid=seed['target_pid_before_instrumentation']
 require(type(pid) is int and pid>0,'no seed live PID')
 require(seed['success'] is True and seed['leave_target_running'] is True and verify['success'] is True and verify['leave_target_running'] is False,'phase success/lifetime differs')
 require('FAILED:' not in log,'boundary failure')
 exits=re.findall(r'^exit=(\d+)$',log,re.M);require(exits==['0']*7,'boundary command count/status differs')
 markers=['Start ordinary launcher (maximum 30s)',f'alive:{pid}',f'Complete successful seed report verified; PID={pid}',f'alive:{pid}','Gallery must still be the resumed activity',f'alive:{pid}',f'Force-stop verified live PID {pid}', '\nabsent\n','Verified target PID absent before normal verify instrumentation']
 position=0
 for marker in markers:
  i=log.find(marker,position);require(i>=0,'missing or unordered boundary '+marker);position=i+len(marker)
 require(re.search(r'(topResumedActivity|mResumedActivity).*paint\.anpaint\.android/org\.catrobat\.paintroid\.classic\.MediaGalleryActivity',log),'Gallery resumed receipt missing')
 require((root/'verify-status.txt').read_text()=='COMPLETED: see strict verify summary\n','verification not completed')
 return {'status':'PASS_BOUNDED_RESTART_BOUNDARY','head':HEAD,'merge':MERGE,'tree':TREE,'run_id':int(RUN),'seed_pid':pid,'successful_commands':len(exits),'raw_sha256':sha(raw),'phase_scope':'Must be used with full source-bound seed/verify raw protocol/summary/XML matrix audit.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--artifacts',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.artifacts);a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
