#!/usr/bin/env python3
"""Independent successful AndroidJUnitRunner event-sequence check, without source parser."""
from audit_natural_artifacts import require

def verify_success_sequence(text, expected):
 fields={};events=[];terminals=[];seen=set();active=None
 for number,line in enumerate(text.splitlines(),1):
  if line.startswith('INSTRUMENTATION_STATUS: '):
   require(not terminals,'status appears after terminal')
   key,separator,value=line[len('INSTRUMENTATION_STATUS: '):].partition('=')
   require(separator and key not in fields,'malformed or duplicate status field');fields[key]=value
  elif line.startswith('INSTRUMENTATION_STATUS_CODE: '):
   require(not terminals,'event after terminal');code=int(line.split(': ',1)[1]);identity=(fields.get('class'),fields.get('test'))
   require(identity in expected,'event outside selected source identities');require(fields.get('numtests')==str(len(expected)),'event count differs from source')
   if code==1:
    require(active is None and identity not in seen,'duplicate/overlapping test start');active=identity
   else:
    require(code==0 and active==identity,'nonpassing/unstarted/misordered completion');active=None;seen.add(identity)
   require(fields.get('current')==str(len(seen)+(1 if code==1 else 0)),'nonsequential current counter')
   events.append({'line':number,'identity':list(identity),'code':code});fields={}
  elif line.startswith('INSTRUMENTATION_CODE: '):
   require(not fields and active is None,'terminal inside unfinished event');terminals.append(int(line.split(': ',1)[1]))
  elif line.startswith(('INSTRUMENTATION_FAILED:','INSTRUMENTATION_ABORTED:')):
   raise ValueError('runner abort/failure')
 require(terminals==[-1] and active is None and not fields,'missing/duplicate/unsuccessful/truncated terminal')
 require(seen==expected and len(events)==2*len(expected),'missing or extra identity/event')
 return {'status':'PASS_INDEPENDENT_SERIAL_PROTOCOL','terminal_codes':terminals,'start_events':len(expected),'successful_completion_events':len(expected),'event_count':len(events),'events':events}
