#!/usr/bin/env python3
"""Verify CI artifact bytes/source, exact reviewed Serbian/SK/SL/CA/RO/DA/NO/NN resources and debug signature."""
from pathlib import Path
from prepare_source_expectations import tree_hash
import argparse,zipfile,json,hashlib,subprocess,re,shutil,xml.etree.ElementTree as E

def need(ok,message):
 if not ok:raise ValueError(message)
def h(b):return hashlib.sha256(b).hexdigest()
def filehash(path):
 with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def same_streams(left,right):
 while True:
  a,b=left.read(1024*1024),right.read(1024*1024)
  if a!=b:return False
  if not a:return True
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def dump(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def reviewed_expectations(source_root):
 fixtures=source_root/'tools/fixtures/current_localization'
 hrbs=json.loads((fixtures/'croatian_bosnian_p0_wording.json').read_bytes())
 need(hrbs.get('review_binding')=={'source_commit': '0ebd41d4d9b665213c776f5a0479a29ecabdd243', 'source_tree': 'bc5e10affc54ba2e0788c749b4b78968379596ba', 'accepted_pairs_sha256': 'ecf526badf05941ed1a11be43af7e6192fda51828861fce34b385c991e2011dc'},'Croatian/Bosnian immutable review binding')
 need(len(hrbs['values'])==78 and set(hrbs['preserved_values'])=={'hr','bs'},'Croatian/Bosnian fixture inventory')
 pairs=[{'locale':tag,'key':key,'source':hrbs['values'][key]['default'],'value':hrbs['values'][key][tag],'attributes':hrbs['constraints'][key][tag]['attributes']} for tag in ('hr','bs') for key in sorted(hrbs['values'])]
 need(h(json.dumps(pairs,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())=='ecf526badf05941ed1a11be43af7e6192fda51828861fce34b385c991e2011dc','complete156 Croatian/Bosnian reviewed pairs')
 serbian=json.loads((fixtures/'serbian_p0_wording.json').read_bytes())
 need(serbian.get('review_successors')=={'review_commit': '747437e11d94a88aeacc826cc8f2f7f227bc9a14', 'review_path': 'records/localization-review/2026-10-26/serbian-p0/r04-format-label-review/review.json', 'review_sha256': 'a2e91394fd6fcbbeaefafe4ee879df23fd4791a33dba565b0a31bfbc2f78b164', 'locale': 'sr-Cyrl', 'superseded_warning': 'ui_autosave_is_paused_to_protect_that_draft_use', 'newly_reviewed_label': 'save20_file_format', 'unchanged_inherited_values': 337, 'unchanged_prior_reviewed_values': 147, 'current_unique_reviewed_values': 149, 'accepted_pair_sha256': 'c84e7335b4bea3a9d2dc4d7857f8fdb9ea662d63d1c7368373dc7505df892511'},'successor immutable review receipt')
 label=serbian.get('format_label_successor');need(isinstance(label,dict) and set(label)=={'locale','key','value','attributes'} and label['locale']=='sr-Cyrl' and label['key']=='save20_file_format' and label['attributes']=={'name':'save20_file_format'},'successor label identity')
 warning='ui_autosave_is_paused_to_protect_that_draft_use'
 pair={label['key']:{'value':label['value'],'attributes':label['attributes']},warning:{'value':serbian['values'][warning]['sr-Cyrl'],'attributes':serbian['constraints'][warning]['sr-Cyrl']['attributes']}}
 need(h(json.dumps(pair,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())=='c84e7335b4bea3a9d2dc4d7857f8fdb9ea662d63d1c7368373dc7505df892511','successor complete pair review digest')
 need(len(serbian['values'])==74 and set(serbian['preserved_values'])=={'sr-Cyrl','sr-Latn'},'Serbian fixture inventory')
 sk_sl=json.loads((fixtures/'slovak_slovenian_p0_wording.json').read_bytes())
 need(len(sk_sl['values'])==78 and set(sk_sl['preserved_values'])=={'sk','sl'},'SK/SL fixture inventory')
 ca_ro_completion=json.loads((fixtures/'catalan_romanian_completion_wording.json').read_bytes())
 ca_ro_import=json.loads((fixtures/'catalan_romanian_import_wording.json').read_bytes())
 ca_ro=json.loads((fixtures/'catalan_romanian_save_wording.json').read_bytes())
 da_no=json.loads((fixtures/'danish_norwegian_p0_wording.json').read_bytes())
 nn72=json.loads((fixtures/'nynorsk_p0_remaining_wording.json').read_bytes())
 nn8=json.loads((fixtures/'nynorsk_save_wording.json').read_bytes())
 need(len(ca_ro_completion['values'])==55 and len(ca_ro_import['values'])==13 and len(ca_ro['values'])==10 and len(da_no['values'])==78 and len(nn72['values'])==72 and len(nn8['values'])==8,'reviewed fixture inventory')
 need(not(set(ca_ro_import['values']) & set(ca_ro['values'])),'overlapping CA/RO import and Save review scopes')
 need(not(set(ca_ro_completion['values']) & (set(ca_ro_import['values']) | set(ca_ro['values']))),'overlapping CA/RO completion and prior review scopes')
 need(not(set(nn72['values']) & set(nn8['values'])),'overlapping prior NN review scopes')
 def display(value):
  need(isinstance(value,str) and value.startswith('"') and value.endswith('"') and '\\' not in value,'unsupported Android fixture quoting/escape')
  return value[1:-1]
 result={tag:{key:display(value[tag]) for key,value in da_no['values'].items()} for tag in ('da','no')}
 result.update({tag:{key:display(value[tag]) for key,value in {**ca_ro['values'],**ca_ro_import['values'],**ca_ro_completion['values']}.items()} for tag in ('ca','ro')})
 result['nn']={key:display(value['nn']) for key,value in {**nn72['values'],**nn8['values']}.items()}
 need({tag:len(values) for tag,values in result.items()}=={'ca':78,'ro':78,'da':78,'no':78,'nn':80},'reviewed locale scope counts')
 for tag in ('sk','sl'):
  preserved=sk_sl['preserved_values'][tag]
  need(len(preserved)==127 and not(set(preserved)&set(sk_sl['values'])),'SK/SL prior/new overlap or inventory')
  result[tag]={key:display(value[tag]) for key,value in sk_sl['values'].items()}
  for key,value in preserved.items():
   text=value['value'];need(isinstance(text,str) and '\\' not in text and '\n' not in text,'unsupported inherited Android escaping')
   result[tag][key]=display(text) if text.startswith('"') else text
 for tag,count in [('sr-Cyrl',169),('sr-Latn',168)]:
  preserved=serbian['preserved_values'][tag]
  need(len(preserved)==count and not(set(preserved)&set(serbian['values'])),'Serbian prior/new overlap or inventory')
  result[tag]={key:display(value[tag]) for key,value in serbian['values'].items()}
  if tag=='sr-Cyrl':
   need(label['key'] not in result[tag] and label['key'] not in preserved,'successor reviewed/inherited overlap');result[tag][label['key']]=display(label['value'])
  for key,value in preserved.items():
   text=value['value'];need(isinstance(text,str) and '\\' not in text and '\n' not in text,'unsupported inherited Serbian Android escaping')
   result[tag][key]=display(text) if text.startswith('"') else text
 for tag,count in [('hr',98),('bs',117)]:
  preserved=hrbs['preserved_values'][tag];need(len(preserved)==count and not(set(preserved)&set(hrbs['values'])),'Croatian/Bosnian prior/new overlap or inventory')
  result[tag]={key:display(value[tag]) for key,value in hrbs['values'].items()}
  for key,value in preserved.items():
   text=value['value'];need(isinstance(text,str) and '\\' not in text and '\n' not in text,'unsupported inherited Croatian/Bosnian escaping');result[tag][key]=display(text) if text.startswith('"') else text
 need(sum(map(len,result.values()))==1659,'exact combined compiled inventory')
 return result

# Observed aapt2 forms of the actual explicit-script catalogues. Generic (sr)
# belongs to other resource configurations and must never stand in for sr-Cyrl.
COMPILED_CONFIG_TO_TAG={**{tag:tag for tag in ('ca','ro','da','no','nn','sk','sl','hr','bs')},
                        'b+sr+Cyrl':'sr-Cyrl','b+sr+Latn':'sr-Latn'}

def parse_compiled_resources(dump_text):
 result={tag:{} for tag in COMPILED_CONFIG_TO_TAG.values()};current=None
 for line in dump_text.splitlines():
  header=re.match(r'\s*resource 0x[0-9a-f]+ ([^ /]+)/([^ ]+)',line)
  if header:
   current=header.group(2) if header.group(1)=='string' else None
  elif current:
   entry=re.match(r'\s*\(([^()]*)\) (".*"|@string/[A-Za-z0-9_]+)$',line)
   if entry and entry.group(1) in COMPILED_CONFIG_TO_TAG:
    tag=COMPILED_CONFIG_TO_TAG[entry.group(1)];need(current not in result[tag],'duplicate compiled value '+tag+'/'+current)
    raw=entry.group(2)
    result[tag][current]={'reference':raw[len('@string/'):]} if raw.startswith('@string/') else json.loads(raw)
 return result

def verify_compiled_resources(parsed,expected,inherited=None):
 entries=[]
 def resolve(tag,key,seen=frozenset()):
  need(key not in seen,'compiled alias cycle '+tag+'/'+key)
  need(key in expected[tag] and key in parsed[tag],'compiled alias target outside exact scoped catalogue '+tag+'/'+key)
  wanted=expected[tag][key];actual=parsed[tag][key]
  match=re.fullmatch(r'@string/([A-Za-z0-9_]+)',wanted)
  if match:
   target=match.group(1)
   need(actual=={'reference':target},'compiled symbolic reference mismatch '+tag+'/'+key)
   return resolve(tag,target,seen|{key})
  need(isinstance(actual,str) and actual==wanted,'compiled reviewed text mismatch '+tag+'/'+key)
  return actual
 for tag,values in expected.items():
  for key,value in values.items():
   display=resolve(tag,key)
   reference=re.fullmatch(r'@string/([A-Za-z0-9_]+)',value)
   entries.append({'locale':tag,'identity':'string/'+key,'display_sha256':h(display.encode()),'exact_expected_display_match':True,'compiled_reference':reference.group(1) if reference else None,'source_value_sha256':h(value.encode()),'scope':('inherited preservation only' if inherited and key in inherited.get(tag,{}) else 'new bounded Croatian/Bosnian review' if tag in ('hr','bs') else 'current bounded Serbian review family' if tag in ('sr-Cyrl','sr-Latn') else 'prior bounded review')})
 return entries

a=argparse.ArgumentParser();a.add_argument('--directory',type=Path,required=True);a.add_argument('--source-root',type=Path,required=True);a.add_argument('--tree-file',type=Path,required=True);a.add_argument('--tools',type=Path,required=True);a.add_argument('--expected-commit',required=True);a.add_argument('--head',required=True);a.add_argument('--expected-tree',required=True);a.add_argument('--run-id',type=int,required=True);a.add_argument('--artifact-id',type=int,required=True);a.add_argument('--archive-sha256',required=True);args=a.parse_args();r=args.directory
archive=r/'apk-and-source.zip';need(filehash(archive)==args.archive_sha256,'artifact digest')
with zipfile.ZipFile(archive) as z:
 need(len(z.namelist())==len(set(z.namelist())),'duplicate artifact ZIP member')
 for source,destination in [('app/build/outputs/apk/debug/app-debug.apk','app-debug.apk'),('build/delivery/AN-Paint-source.zip','AN-Paint-source.zip'),('build/delivery/build-info.json','build-info.json')]:
  need(z.namelist().count(source)==1,'missing/duplicate artifact member '+source)
  with z.open(source) as src,(r/destination).open('wb') as dst:shutil.copyfileobj(src,dst)
info=json.loads((r/'build-info.json').read_bytes());need(info['commit']==args.expected_commit and str(info['run_id'])==str(args.run_id),'build-info identity');need(info['apk_sha256']==filehash(r/'app-debug.apk') and info['source_sha256']==filehash(r/'AN-Paint-source.zip'),'build-info digest')
with zipfile.ZipFile(r/'app-debug.apk') as apk:
 with apk.open('assets/local-source/AN-Paint-source.zip') as embedded,(r/'AN-Paint-source.zip').open('rb') as external:need(same_streams(embedded,external),'embedded source differs')
tree=json.loads(args.tree_file.read_bytes());need(tree['sha']==args.expected_tree and tree.get('truncated') is False,'tree binding');blob_entries=[x for x in tree['tree'] if x['type']=='blob'];blobs={x['path']:x for x in blob_entries};need(bool(blobs) and len(blobs)==len(blob_entries) and tree_hash(blob_entries)[0]==args.expected_tree,'tracked source inventory/tree reconstruction');need(all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in blobs),'unsafe tree path')
missing=[];checked=[]
with zipfile.ZipFile(r/'AN-Paint-source.zip') as z:
 names=z.namelist();need(len(names)==len(set(names)),'source ZIP duplicate names');need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names),'unsafe source ZIP path');extra_members=sorted(n for n in names if not n.endswith('/') and n not in {'AN-Paint/'+p for p in blobs})
 for p,v in blobs.items():
  local=(args.source_root/p).read_bytes();need(git(local)==v['sha'],'local source drift '+p)
  name='AN-Paint/'+p
  if name not in names:missing.append(p);continue
  need((z.getinfo(name).external_attr>>16 & 0o111)==(int(v['mode'],8)&0o111),'packaged executable mode mismatch '+p)
  raw=z.read(name);need(raw==local and git(raw)==v['sha'],'packaged source mismatch '+p);checked.append(p)
need(sorted(missing)==['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore'],'unexpected packager exclusions')
need(len(checked)==len(blobs)-len(missing),'packaged tracked source inventory')
dump(r/'artifact-source-binding.json',{'schema_version':1,'reviewed_head':args.head,'tested_commit':args.expected_commit,'source_tree':args.expected_tree,'run_id':args.run_id,'artifact_id':args.artifact_id,'archive_sha256':args.archive_sha256,'build_info':info,'tracked_files':len(blobs),'packaged_tracked_source_files_exact':len(checked),'packager_exclusions':sorted(missing),'embedded_source_matches_external':True,'tracked_executable_modes_match':True,'non_git_bound_extra_members':len(extra_members),'non_git_bound_extra_member_names_sha256':h(('\n'.join(extra_members)+'\n').encode()),'limits':'All tracked project source bytes and embedded/external archive identity checked. Extra vendored/generated members are counted, not authenticated by the project Git tree. Not tests passed, private upgrade signing or release.'})
aapt=args.tools/'aapt2';signer=args.tools/'apksigner.jar'
with (r/'apk-resources.txt').open('w') as out:subprocess.run([str(aapt),'dump','resources',str(r/'app-debug.apk')],stdout=out,check=True)
with (r/'apk-signature.txt').open('w') as out:subprocess.run(['java','-jar',str(signer),'verify','--verbose','--print-certs',str(r/'app-debug.apk')],stdout=out,stderr=subprocess.STDOUT,check=True)
expected=reviewed_expectations(args.source_root);parsed=parse_compiled_resources((r/'apk-resources.txt').read_text());inherited={}
for fixture_name in ('slovak_slovenian_p0_wording.json','serbian_p0_wording.json','croatian_bosnian_p0_wording.json'):
 inherited.update(json.loads((args.source_root/'tools/fixtures/current_localization'/fixture_name).read_bytes())['preserved_values'])
entries=verify_compiled_resources(parsed,expected,inherited)
sign=(r/'apk-signature.txt').read_text();need(sign.startswith('Verifies\n') and 'Verified using v1 scheme (JAR signing): true' in sign and 'Verified using v2 scheme (APK Signature Scheme v2): true' in sign,'signature schemes');cert=re.search(r'Signer #1 certificate SHA-256 digest: ([0-9a-f]+)',sign);need(cert is not None,'certificate fingerprint')
dump(r/'compiled-resource-verification.json',{'schema_version':1,'run_id':args.run_id,'reviewed_head':args.head,'tested_commit':args.expected_commit,'tree':args.expected_tree,'apk_sha256':info['apk_sha256'],'current_Serbian_reviewed_entries':149,'successor_changed_values':2,'unchanged_Serbian_reviewed_values':147,'total_reviewed_entries':853,'new_reviewed_entries':156,'new_reviewed_entries_by_locale':{'hr':78,'bs':78},'prior_reviewed_total':697,'prior_reviewed_entries':548,'inherited_entries':806,'current_Serbian_reviewed_entries_by_locale':{'sr-Cyrl':75,'sr-Latn':74},'prior_reviewed_entries_by_locale':{'ca':78,'ro':78,'da':78,'no':78,'nn':80,'sk':78,'sl':78},'inherited_entries_by_locale':{'hr':98,'bs':117,'sk':127,'sl':127,'sr-Cyrl':169,'sr-Latn':168},'SK_SL_new_inherited_keys_disjoint':True,'Serbian_new_inherited_keys_disjoint':True,'explicit_Serbian_configurations':{'sr-Cyrl':'b+sr+Cyrl','sr-Latn':'b+sr+Latn'},'reviewed_entries_by_locale':{'hr':78,'bs':78,'ca':78,'ro':78,'da':78,'no':78,'nn':80,'sk':78,'sl':78,'sr-Cyrl':75,'sr-Latn':74},'compiled_entries_by_locale':{tag:len(values) for tag,values in expected.items()},'scope':'156 new Croatian/Bosnian values plus149 current bounded Serbian review-family values (147 unchanged plus2 successor changes) plus548 prior bounded SK/SL/CA/RO/DA/NO/NN values;806 inherited Croatian/Bosnian/Serbian/SK/SL displays checked for preservation only, not new linguistic acceptance','entries':entries,'signature_exit':0,'v1_verified':True,'v2_verified':True,'CI_debug_certificate_sha256':cert.group(1),'aapt2_sha256':h(aapt.read_bytes()),'apksigner_jar_sha256':h(signer.read_bytes()),'signature_output_sha256':h((r/'apk-signature.txt').read_bytes()),'limits':'Compiled resource and CI debug certificate only; no physical-device, native-language, layout, whole-locale, private upgrade-signing or release claim.'})
print(json.dumps({'source_files_exact':len(checked),'apk_sha256':info['apk_sha256'],'source_sha256':info['source_sha256'],'compiled_checked_values':len(entries),'compiled_checked_values_by_locale':{tag:len(values) for tag,values in expected.items()},'certificate_sha256':cert.group(1)},indent=2))
