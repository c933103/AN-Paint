#!/usr/bin/env python3
"""Read retained same-run phase logs without interpreting deliberate negative-control JSON as failures."""
import argparse,pathlib,re,json,hashlib

def require(v,m):
 if not v:raise ValueError(m)
def audit(p):
 rows=[]
 for phase in ('python','jvm','native','lint'):
  raw=(p/(phase+'.log')).read_bytes();log=raw.decode();timing=(p/(phase+'.time')).read_text()
  pairs=dict(re.findall(r'^([a-z_]+)=(\S+)$',timing,re.M));expected=1 if phase=='jvm' else 0
  require(int(pairs['exit_status'])==expected,phase+' exit differs')
  row={'phase':phase,'exit_status':expected,'timing':pairs,'files':{}}
  for s in ('log','time','started-at','ended-at'):
   b=(p/(phase+'.'+s)).read_bytes();row['files'][phase+'.'+s]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
  if phase=='python':
   m=re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$',log,re.M);require(len(m)==1 and int(m[0][0])==719,'host summary differs')
   require(re.findall(r'^OK \(skipped=(\d+)\)$',log,re.M)==['2'],'host outcome differs')
   require(not re.search(r'^(FAIL|ERROR):|^FAILED',log,re.M),'host actual failures')
   row.update(tests_discovered=719,passed=717,skipped=2,elapsed_seconds=float(m[0][1]),skip_identity_limit='Compact unittest output does not identify the two skips. They are not counted as executed passes.')
  elif phase=='jvm':require('BUILD FAILED' in log and 'paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtDoubleScale' in log,'missing known JVM failure')
  else:require('BUILD SUCCESSFUL' in log and 'BUILD FAILED' not in log,'unexpected native/lint outcome')
  rows.append(row)
 return {'status':'RECEIPTS_CONSISTENT_JVM_FAILS','rows':rows,'limits':'Source/run/ZIP provenance is supplied by the separate archive audit; no local Android execution.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--phases',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.phases);a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
