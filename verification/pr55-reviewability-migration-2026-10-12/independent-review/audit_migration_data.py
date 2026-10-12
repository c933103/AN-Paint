#!/usr/bin/env python3
"""One-time migration evidence only. This is deliberately outside normal CI."""
import argparse,hashlib,json,pathlib,subprocess,sys,xml.etree.ElementTree as ET
BASE='04b128889a4ff9159f199d1737bd07d41e22162d'
BASE_TREE='3dcc1a82f878ad7e0e708cff25ec8d493b88bbc6'
FAMILIES=['commons_metadata_current_wording.json','commons_copy_credit_current_wording.json','commons_svg_current_wording.json','hungarian_attribution_current_wording.json','help_commons_provider_current_contract.json']
def require(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def audit(repo):
 sys.path.insert(0,str(repo/'tools'));import translation_catalogues as cat
 require(subprocess.check_output(['git','show',BASE_TREE+':tools/translation_catalogues.py'],cwd=repo)==(repo/'tools/translation_catalogues.py').read_bytes(),'catalogue discovery changed; separately review')
 paths={'default':cat.RES/'values/strings.xml',**cat.catalogue_paths()};roots={};pins={};rows=[]
 def original(path):return subprocess.check_output(['git','show',BASE_TREE+':'+path],cwd=repo)
 for name in FAMILIES:
  f=repo/'tools/fixtures/current_localization'/name;raw=f.read_bytes();d=json.loads(raw);checked=0
  for key,values in d['values'].items():
   for tag,expected in values.items():
    p=paths[tag];rel=p.relative_to(repo).as_posix()
    if tag not in roots:
     old=original(rel);new=p.read_bytes();require(old==new,'production catalogue bytes changed '+rel)
     roots[tag]=ET.fromstring(old);pins[rel]=sha(old)
    nodes=roots[tag].findall(f"./string[@name='{key}']");require(len(nodes)==1,'old parsed resource missing/duplicate')
    require(''.join(nodes[0].itertext())==expected,'compact fixture changed existing wording '+name+' '+key+' '+tag)
    checked+=1
  require(checked>0,'empty migrated family')
  rows.append({'fixture':name,'sha256':sha(raw),'keys':sorted(d['values']),'parsed_values_checked':checked})
 # The import fixture retains its existing compact record shape.
 old_import=json.loads(original('verification/commons-import-changes-2026-10-09/translations.json'))
 new_import=json.loads((repo/'tools/fixtures/current_localization/commons_import_current_wording.json').read_text())
 require(all(old_import[k]==v for k,v in new_import.items()),'import fixture changed parsed record')
 import_count=len(new_import['source_messages'])+sum(len(v) for v in new_import['translations'].values())
 # Intended production/build/workflow scope stays empty. The separately reviewed
 # Flow test policy change is deliberately not included in this production check.
 production=['Paintroid/src/main','app/src/main','colorpicker','.github','gradle','build.gradle','settings.gradle']
 diff=subprocess.check_output(['git','diff','--name-status',BASE_TREE,'--',*production],cwd=repo).decode();require(not diff,'production/build/workflow changed: '+diff)
 untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=repo).decode().splitlines()
 require(not any(any(p==q or p.startswith(q+'/') for q in production) for p in untracked),'new production/build/workflow path')
 required=['verification/legacy-font-metadata.json','verification/releases/request.json']
 request=json.loads((repo/required[-1]).read_bytes())
 # The actual publisher-selected dependencies are checked by their retained
 # names; publication/release authorization is outside this reviewer audit.
 required+=['verification/releases/0.0.38-signing.json','verification/releases/0.0.38-notes.md']
 operational=[]
 for rel in required:
  raw=(repo/rel).read_bytes();require(raw==original(rel),'operational/licence input changed '+rel);operational.append({'path':rel,'sha256':sha(raw)})
 return {'status':'PASS_ONE_TIME_MIGRATION_DATA','base':BASE,'base_tree':BASE_TREE,'scope':'Current parsed wording/default/script controls preserved in compact fixtures; production/resources/fonts/build/workflow and selected operational/licence inputs unchanged. Historical reconstruction is not a future CI requirement.','families':rows,'total_parsed_values':sum(r['parsed_values_checked'] for r in rows),'additional_import_values':import_count,'catalogue_paths':pins,'operational_inputs':operational,'untracked_production_paths':[],'limits':['Draft checked at execution time; bind final source separately.','No linguistic re-review, Android compilation or runtime execution.','Other modified host-test semantics need the separate source review and focused/full execution.']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.repo);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(r['status'],r['total_parsed_values'],'parsed values')
