#!/usr/bin/env python3
"""Mutation controls for the candidate-data verifier; no application edits."""
import argparse,hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--verifier',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def h(b):return hashlib.sha256(b).hexdigest()
filename='da-group-01-import-format-candidates.json';outcomes=[]
for case in ['positive','extra-unindexed-s','extra-indexed-d','invalid-q','stray-percent','missing-argument','duplicate-identity','duplicate-JSON-key','missing-group-file']:
 with tempfile.TemporaryDirectory() as temp:
  root=Path(temp);packet=root/'packet';shutil.copytree(a.packet,packet);f=packet/filename;data=json.loads(f.read_text());e=data['candidates'][0]
  if case in ['extra-unindexed-s','extra-indexed-d','invalid-q','stray-percent','missing-argument']:
   if case=='missing-argument':e['candidate_display_text']=e['candidate_display_text'].replace('%1$s','format')
   else:e['candidate_display_text']+=' '+{'extra-unindexed-s':'%s','extra-indexed-d':'%9$d','invalid-q':'%q','stray-percent':'%'}[case]
   value=e['candidate_display_text'];e['candidate_value_sha256_utf8']=h(value.encode());e['candidate_xml_text']='"'+value.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n').replace('\t','\\t')+'"';e['candidate_xml_text_sha256_utf8']=h(e['candidate_xml_text'].encode());f.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
  elif case=='duplicate-identity':data['candidates'][1]=data['candidates'][0];f.write_text(json.dumps(data,ensure_ascii=False)+'\n')
  elif case=='duplicate-JSON-key':f.write_text('{"schema_version":1,'+f.read_text().lstrip()[1:])
  elif case=='missing-group-file':f.unlink()
  result=subprocess.run(['python',str(a.verifier),'--source-root',str(a.source_root),'--packet',str(packet),'--out',str(root/'out')],capture_output=True,text=True)
  expected=0 if case=='positive' else 1
  if (result.returncode==0)!=(expected==0):raise ValueError('Mutation expectation failed: '+case)
  reason=next((line.split('ValueError: ',1)[1] for line in reversed(result.stderr.splitlines()) if 'ValueError: ' in line),'passed')
  outcomes.append({'case':case,'exit_code':result.returncode,'expected_success':case=='positive','outcome':reason})
a.out.mkdir(parents=True,exist_ok=True);(a.out/'mutation-controls.json').write_text(json.dumps({'schema_version':1,'verifier_sha256':h(a.verifier.read_bytes()),'positive_cases':1,'negative_cases':8,'all_expected_outcomes_observed':True,'controls':outcomes,'limits':'Data-only synthetic mutations in temporary copies; actual candidate/source files unchanged.'},indent=2)+'\n');print(json.dumps(outcomes,indent=2))
