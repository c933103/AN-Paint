#!/usr/bin/env python3
"""Read-only exact-commit comparisons; neither language certification nor Android execution."""
from pathlib import Path
import subprocess, hashlib, json, xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
REPO=HERE.parent.parent
CURRENT='7e8a0d2377693a35cd9392f2082ef88548a6f67f'
HEADS={7:'730319aea40eb205d18c894c496e500d6f660ac6',9:'a0afe1cfed363b65c3880c9875034b0460f811a2'}
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args],text=True)
def present(ref,path):return subprocess.run(['git','-C',str(REPO),'cat-file','-e',f'{ref}:{path}'],capture_output=True).returncode==0
def catalogue(ref,path):return {e.get('name'):ET.tostring(e,encoding='unicode').strip() for e in ET.fromstring(git('show',f'{ref}:{path}')) if e.get('name')}
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
out={'current':CURRENT,'resources':{},'pr16':{}}
for pr,head in HEADS.items():
 base=git('merge-base',CURRENT,head).strip();rows=[]
 for path in git('diff','--name-only',base,head).splitlines():
  if '/res/values' not in path or not path.endswith('/strings.xml'):continue
  old,new,current=catalogue(base,path),catalogue(head,path),catalogue(CURRENT,path)
  assert not old.keys()-new.keys(),(path,'removed keys')
  for key,value in new.items():
   if old.get(key)==value:continue
   assert current.get(key)==value,(pr,path,key)
   rows.append({'path':path,'key':key,'proposed_sha256':digest(value),'current_sha256':digest(current[key]),'equal':True})
 expected=json.loads((HERE/f'pr{pr}-resource-comparison.json').read_text())
 assert sorted(rows,key=lambda r:(r['path'],r['key']))==sorted(expected,key=lambda r:(r['path'],r['key']))
 assert not present(CURRENT,f'tools/test_normalization_scope_pr{pr}.py')
 out['resources'][str(pr)]={'head':head,'merge_base':base,'identical_changed_elements':len(rows),'normalization_guard_absent':True}
replacement='4e11cb42374f2aee0557cbdda1da938ff4902106'
subprocess.check_call(['git','-C',str(REPO),'merge-base','--is-ancestor',replacement,CURRENT])
path='Paintroid/src/test/java/org/catrobat/paintroid/local/GalleryImportTest.kt'
original=git('show','aa3412a45ca02526cabcc8358a697f60ec00adcc:'+path);current=git('show',CURRENT+':'+path)
def method(text,name):
 start=text.index('    @Test fun '+name);end=text.find('    @Test',start+1)
 return text[start:end if end>=0 else text.rfind('\n}')].strip()
methods=['unfinishedCreditDraftSurvivesRecreationWithoutBecomingASavedEdit','restoredCreditDraftKeepsSelectedSourceAndAnEmptyDraftWithoutSavingIt','dismissedCreditDraftIsNotSavedOrReopenedByActivityRecreation']
xml=ET.parse(HERE/'GalleryImportTest.xml').getroot()
assert xml.get('tests')=='11' and all(xml.get(k)=='0' for k in ['failures','errors','skipped'])
for name in methods:
 a,b=method(original,name),method(current,name);assert a==b
 cases=[e for e in xml.findall('testcase') if e.get('name')==name]
 assert len(cases)==1 and len(cases[0])==0
 out['pr16'][name]={'body_identical':True,'body_sha256':digest(b),'current_xml':'passed'}
subprocess.check_call(['git','-C',str(REPO),'merge-base','--is-ancestor','040d64f43a6cf938a0a0b3985942774fb6380fd4',CURRENT])
assert not present(CURRENT,'app/src/androidTest/java/paint/anpaint/android/VerticalLocaleDeviceTest.kt')
runner=git('show',CURRENT+':tools/ci_emulator.sh')
assert 'app-vertical' not in runner and 'run_credit_restart_regression' in runner
out['pr18']={'head_is_ancestor':True,'matrix_class_absent':True,'old_partition_absent':True,'accepted_credit_restart_retained':True}
receipt=json.loads((HERE/'ci-receipt.json').read_text())
for path,sha in receipt['files'].items():assert hashlib.sha256((HERE/path).read_bytes()).hexdigest()==sha
print(json.dumps(out,indent=2))
