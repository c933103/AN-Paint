#!/usr/bin/env python3
"""Fresh source-derived XML priority audit; no prior runtime credit or visual claim."""
import argparse,json,pathlib,hashlib,collections,sys,xml.etree.ElementTree as ET
from audit_platform_artifacts import current_inventory,junit_audit,TREE,HEAD,MERGE,RUN
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--artifact-root',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
sys.path.insert(0,str(a.repo/'tools'));inv=current_inventory(a.repo)
root=a.artifact_root/'Paintroid/build/test-results/testDebugUnitTest';whole=junit_audit(root,inv['expected'])
priority=[tuple(x) for x in inv['expected'] if x[0].endswith('.UiTypographyContextTest') or x[0].endswith('.LocaleNotificationTest') and x[1].startswith('notificationRouteUsesResourcesDespiteAnOppositeProcessDefault')]
lifecycle=[tuple(x) for x in inv['expected'] if x[0].endswith('.UiDirectionContextTest') and x[1].startswith('rotationAndRecreationPreserveSelectedDirectionDespiteLaterDefaultReset')]
rows=[];xml=[]
for path in sorted(root.glob('TEST-*.xml')):
 selected=[]
 for c in ET.parse(path).getroot().iter('testcase'):
  identity=(c.get('classname'),c.get('name'))
  if identity not in priority+lifecycle:continue
  states=[n.tag for n in c if n.tag in ['failure','error','skipped']]
  row={'classname':identity[0],'name':identity[1],'status':'PASS' if not states else '/'.join(states).upper(),'seconds':float(c.get('time')),'scope':'Legacy font binding only' if identity[1].endswith(('[21]','[24]')) else 'Robolectric native behavior; installed proof is separate','extended_existing_lifecycle':identity in lifecycle}
  selected.append(row);rows.append(row)
 if selected:xml.append({'path':str(path.relative_to(a.artifact_root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
actual=collections.Counter((r['classname'],r['name']) for r in rows);expected=collections.Counter(priority+lifecycle)
status='PASS' if whole['status']=='PASS' and actual==expected and all(r['status']=='PASS' for r in rows) else 'FAIL'
r={'status':status,'head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'complete_junit':whole,'priority_font_execution_count':len(priority),'extended_lifecycle_execution_count':len(lifecycle),'priority_executions':rows,'priority_xml':xml,'limits':['Every expected identity is derived from current source.','Legacy API21/24 font binding is not real glyph geometry or installed-device coverage.','No image readability/fluency verdict is supplied by XML pass.']}
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':status,'jvm':whole['actual_count'],'new_font_controls':len(priority),'extended_lifecycle':len(lifecycle),'failed_or_missing':whole['failures_and_errors']+whole['missing']},indent=2));sys.exit(0 if status=='PASS' else 1)
