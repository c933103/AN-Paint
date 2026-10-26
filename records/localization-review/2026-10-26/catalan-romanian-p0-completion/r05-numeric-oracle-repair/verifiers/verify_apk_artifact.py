#!/usr/bin/env python3
"""Verify CI artifact bytes/source, exact reviewed CA/RO/DA/NO/NN resources and debug signature."""
from pathlib import Path
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
 return result

def parse_compiled_resources(dump_text):
 result={tag:{} for tag in ('ca','ro','da','no','nn')};current=None
 for line in dump_text.splitlines():
  header=re.match(r'\s*resource 0x[0-9a-f]+ ([^ /]+)/([^ ]+)',line)
  if header:
   current=header.group(2) if header.group(1)=='string' else None
  elif current:
   entry=re.match(r'\s*\((ca|ro|da|no|nn)\) (".*")$',line)
   if entry:
    tag=entry.group(1);need(current not in result[tag],'duplicate compiled value '+tag+'/'+current)
    result[tag][current]=json.loads(entry.group(2))
 return result

def verify_compiled_resources(parsed,expected):
 entries=[]
 for tag,values in expected.items():
  for key,value in values.items():
   need(parsed[tag].get(key)==value,'compiled reviewed text mismatch '+tag+'/'+key)
   entries.append({'locale':tag,'identity':'string/'+key,'display_sha256':h(value.encode()),'exact_approved_display_match':True})
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
tree=json.loads(args.tree_file.read_bytes());need(tree['sha']==args.expected_tree and tree.get('truncated') is False,'tree binding');blob_entries=[x for x in tree['tree'] if x['type']=='blob'];blobs={x['path']:x for x in blob_entries};need(len(blobs)==len(blob_entries)==1379,'tracked source inventory');need(all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in blobs),'unsafe tree path')
missing=[];checked=[]
with zipfile.ZipFile(r/'AN-Paint-source.zip') as z:
 names=z.namelist();need(len(names)==len(set(names)),'source ZIP duplicate names');need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names),'unsafe source ZIP path');extra_members=sorted(n for n in names if not n.endswith('/') and n not in {'AN-Paint/'+p for p in blobs})
 for p,v in blobs.items():
  local=(args.source_root/p).read_bytes();need(git(local)==v['sha'],'local source drift '+p)
  name='AN-Paint/'+p
  if name not in names:missing.append(p);continue
  raw=z.read(name);need(raw==local and git(raw)==v['sha'],'packaged source mismatch '+p);checked.append(p)
need(sorted(missing)==['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore'],'unexpected packager exclusions')
need(len(checked)==len(blobs)-len(missing)==1376,'packaged tracked source inventory')
dump(r/'artifact-source-binding.json',{'schema_version':1,'reviewed_head':args.head,'tested_commit':args.expected_commit,'source_tree':args.expected_tree,'run_id':args.run_id,'artifact_id':args.artifact_id,'archive_sha256':args.archive_sha256,'build_info':info,'tracked_files':len(blobs),'packaged_tracked_source_files_exact':len(checked),'packager_exclusions':sorted(missing),'embedded_source_matches_external':True,'non_git_bound_extra_members':len(extra_members),'non_git_bound_extra_member_names_sha256':h(('\n'.join(extra_members)+'\n').encode()),'limits':'All tracked project source bytes and embedded/external archive identity checked. Extra vendored/generated members are counted, not authenticated by the project Git tree. Not tests passed, private upgrade signing or release.'})
aapt=args.tools/'aapt2';signer=args.tools/'apksigner.jar'
with (r/'apk-resources.txt').open('w') as out:subprocess.run([str(aapt),'dump','resources',str(r/'app-debug.apk')],stdout=out,check=True)
with (r/'apk-signature.txt').open('w') as out:subprocess.run(['java','-jar',str(signer),'verify','--verbose','--print-certs',str(r/'app-debug.apk')],stdout=out,stderr=subprocess.STDOUT,check=True)
expected=reviewed_expectations(args.source_root);parsed=parse_compiled_resources((r/'apk-resources.txt').read_text());entries=verify_compiled_resources(parsed,expected)
sign=(r/'apk-signature.txt').read_text();need(sign.startswith('Verifies\n') and 'Verified using v1 scheme (JAR signing): true' in sign and 'Verified using v2 scheme (APK Signature Scheme v2): true' in sign,'signature schemes');cert=re.search(r'Signer #1 certificate SHA-256 digest: ([0-9a-f]+)',sign);need(cert is not None,'certificate fingerprint')
dump(r/'compiled-resource-verification.json',{'schema_version':1,'run_id':args.run_id,'reviewed_head':args.head,'tested_commit':args.expected_commit,'tree':args.expected_tree,'apk_sha256':info['apk_sha256'],'new_reviewed_entries':110,'prior_reviewed_entries':282,'new_reviewed_entries_by_locale':{'ca':55,'ro':55},'prior_reviewed_entries_by_locale':{'ca':23,'ro':23,'da':78,'no':78,'nn':80},'CA_RO_new_prior_keys_disjoint':True,'reviewed_entries_by_locale':{'ca':78,'ro':78,'da':78,'no':78,'nn':80},'scope':'110 new bounded CA/RO completion values plus 282 prior bounded CA/RO import/Save and DA/NO/NN values; no whole-locale certification','entries':entries,'signature_exit':0,'v1_verified':True,'v2_verified':True,'CI_debug_certificate_sha256':cert.group(1),'aapt2_sha256':h(aapt.read_bytes()),'apksigner_jar_sha256':h(signer.read_bytes()),'signature_output_sha256':h((r/'apk-signature.txt').read_bytes()),'limits':'Compiled resource and CI debug certificate only; no physical-device, native-language, layout, whole-locale, private upgrade-signing or release claim.'})
print(json.dumps({'source_files_exact':len(checked),'apk_sha256':info['apk_sha256'],'source_sha256':info['source_sha256'],'compiled_reviewed_values':len(entries),'compiled_reviewed_values_by_locale':{'ca':78,'ro':78,'da':78,'no':78,'nn':80},'certificate_sha256':cert.group(1)},indent=2))
