#!/usr/bin/env python3
"""Derive staged source tree and artifact identity expectations without executing Android tests."""
import argparse,hashlib,json,re,sys
from pathlib import Path

def need(ok,message):
 if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def object_hash(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def tree_hash(blobs):
 root={}
 for e in blobs:
  d=root;parts=e['path'].split('/')
  for name in parts[:-1]:d=d.setdefault(name,{})
  need(parts[-1] not in d,'duplicate tree path');d[parts[-1]]=e
 entries=[]
 def recurse(d,prefix=''):
  rows=[]
  for name,v in d.items():
   if 'sha' in v and 'mode' in v:
    mode=v['mode'];identity=v['sha'];kind='blob'
   else:
    mode='040000';identity=recurse(v,prefix+name+'/');kind='tree';entries.append({'path':prefix+name,'mode':mode,'type':'tree','sha':identity})
   rows.append((name+('/' if kind=='tree' else ''),mode.lstrip('0')+' '+name,identity))
  body=b''.join(label.encode()+b'\0'+bytes.fromhex(identity) for _,label,identity in sorted(rows,key=lambda r:r[0].encode()))
  return object_hash('tree',body)
 digest=recurse(root);return digest,sorted(blobs+entries,key=lambda e:e['path'])
def numeric_caption_inventory(text):
 tags=re.findall(r'"([^"\n]+)"',re.search(r'private val tags=listOf\(([^\n]+)\)',text).group(1))
 captions=re.findall(r'^\s*"([^"\n]+)" to \(',text.split('val captions=mapOf(',1)[1].split('assertEquals(tags.toSet(), captions.keys)',1)[0],re.M)
 need(len(tags)==len(set(tags))==len(captions)==len(set(captions))==11 and set(tags)==set(captions) and {'hr','bs'}<=set(tags),'exact11 numeric caption maps')
 return {'locale_tags':tags,'caption_tags':captions,'count':len(tags),'exact_inventory_match':True}
def main():
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--base-tree',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--source-head');p.add_argument('--source-head-status',default='explicit commit argument; branch publication not established');a=p.parse_args();a.out.mkdir(exist_ok=True,parents=True)
 base=json.loads(a.base_tree.read_bytes());old=[e for e in base['tree'] if e['type']=='blob'];need(bool(old) and len({e['path'] for e in old})==len(old) and tree_hash(old)[0]==base['sha'],'base raw Git tree reconstruction')
 newpaths=['tools/test_croatian_bosnian_p0_wording.py','tools/fixtures/current_localization/croatian_bosnian_p0_wording.json','Paintroid/src/test/java/org/catrobat/paintroid/local/CroatianBosnianP0WordingTest.kt']
 newpaths=[p for p in newpaths if p not in {e['path'] for e in old}]
 entries=[]
 for e in old+[{'path':p,'mode':'100644'} for p in newpaths]:
  raw=(a.source_root/e['path']).read_bytes();need(('100755' if (a.source_root/e['path']).stat().st_mode & 0o111 else '100644')==e['mode'],'local executable mode '+e['path']);entries.append({'path':e['path'],'mode':e['mode'],'type':'blob','sha':object_hash('blob',raw),'size':len(raw)})
 need(len({e['path'] for e in entries})==len(entries)==len(old)+len(newpaths),'new tracked source inventory')
 digest,full=tree_hash(entries);dump(a.out/'staged-source-tree.json',{'sha':digest,'tree':full,'truncated':False,'record_kind':'Locally reconstructed staged Git tree; not a published ref or commit'})
 sys.path.insert(0,str(a.source_root/'tools'));from run_android_instrumentation import declared_tests,source_tests_sha256
 app=declared_tests(a.source_root/'app/src/androidTest',sdk_level=35);native=declared_tests(a.source_root/'Paintroid/src/androidTest',sdk_level=35)
 classes=['CroatianBosnianP0WordingTest','ProtectedDraftWarningTest','SerbianP0WordingTest','SlovakSlovenianP0WordingTest','NumericDisplayLocaleTest','CatalanRomanianCompletionWordingTest','CatalanRomanianImportWordingTest','CatalanRomanianSaveWordingTest','DanishNorwegianP0Test','NynorskRemainingP0Test','NynorskSaveWordingTest','DerivedExportStateTest','ImportSelectionTitleTest','TaggedColourImportTest'];focused={}
 for cls in classes:
  rel=f'Paintroid/src/test/java/org/catrobat/paintroid/local/{cls}.kt';raw=(a.source_root/rel).read_bytes();methods=re.findall(r'@Test\s+(?:@[\w.]+(?:\([^()]*\))?\s+)*fun\s+([A-Za-z0-9_]+)\s*\(',raw.decode());need(len(set(methods))==len(methods)==len(re.findall(r'@Test\b',raw.decode())),'focused method parsing')
  focused[cls]={'path':rel,'sha256':sha(raw),'methods':methods,'count':len(methods)}
 numeric=numeric_caption_inventory((a.source_root/'Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt').read_text())
 bindings=['tools/verify_exact_script_generation.py','tools/app_instrumentation_matrix.py','tools/run_android_instrumentation.py']
 receipt={'schema_version':1,'record_kind':'Source-derived artifact expectations; no artifact execution','source_tree':digest,'source_head':a.source_head,'source_head_binding_status':a.source_head_status,'tracked_source_files':len(entries),'expected_packaged_tracked_source_files':len(entries)-3,'packager_exclusions':['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore'],'focused_JVM_classes':focused,'numeric_caption_inventory':numeric,'API35':{'app':{'selected_count':len(app),'source_tests_sha256':source_tests_sha256(a.source_root/'app/src/androidTest'),'identities':[{'classname':c,'name':n} for c,n in sorted(app)]},'native':{'selected_count':len(native),'source_tests_sha256':source_tests_sha256(a.source_root/'Paintroid/src/androidTest'),'identities':[{'classname':c,'name':n} for c,n in sorted(native)]}},'source_verifier_bindings':[{'path':p,'sha256':sha((a.source_root/p).read_bytes())} for p in bindings],'limits':['All counts and identities are source expectations, not executed tests.','Full JVM aggregate count must come from actual artifact XML; no total is inferred from these focused classes.','Future runtime verification must bind actual workflow head, tested commit, source tree, run/artifact IDs and downloaded artifact digests.']}
 dump(a.out/'source-expectations.json',receipt);print(json.dumps({'staged_tree':digest,'tracked':len(entries),'packaged_expected':len(entries)-3,'focused_methods':{c:v['count'] for c,v in focused.items()},'API35_app':len(app),'API35_native':len(native)}))
if __name__=='__main__':main()
