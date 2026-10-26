#!/usr/bin/env python3
"""Verify CI artifact bytes/source, exact reviewed NN resources and debug signature."""
from pathlib import Path
import argparse,zipfile,json,hashlib,subprocess,re,xml.etree.ElementTree as E

def need(ok,message):
 if not ok:raise ValueError(message)
def h(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def dump(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
a=argparse.ArgumentParser();a.add_argument('--directory',type=Path,required=True);a.add_argument('--source-root',type=Path,required=True);a.add_argument('--tree-file',type=Path,required=True);a.add_argument('--tools',type=Path,required=True);a.add_argument('--expected-commit',required=True);a.add_argument('--head',required=True);a.add_argument('--expected-tree',required=True);a.add_argument('--run-id',type=int,required=True);a.add_argument('--artifact-id',type=int,required=True);a.add_argument('--archive-sha256',required=True);args=a.parse_args();r=args.directory
archive=r/'apk-and-source.zip';need(h(archive.read_bytes())==args.archive_sha256,'artifact digest')
with zipfile.ZipFile(archive) as z:
 for source,destination in [('app/build/outputs/apk/debug/app-debug.apk','app-debug.apk'),('build/delivery/AN-Paint-source.zip','AN-Paint-source.zip'),('build/delivery/build-info.json','build-info.json')]:
  need(z.namelist().count(source)==1,'missing/duplicate artifact member '+source);(r/destination).write_bytes(z.read(source))
info=json.loads((r/'build-info.json').read_bytes());need(info['commit']==args.expected_commit and str(info['run_id'])==str(args.run_id),'build-info identity');need(info['apk_sha256']==h((r/'app-debug.apk').read_bytes()) and info['source_sha256']==h((r/'AN-Paint-source.zip').read_bytes()),'build-info digest')
with zipfile.ZipFile(r/'app-debug.apk') as apk:need(apk.read('assets/local-source/AN-Paint-source.zip')==(r/'AN-Paint-source.zip').read_bytes(),'embedded source differs')
tree=json.loads(args.tree_file.read_bytes());need(tree['sha']==args.expected_tree and not tree['truncated'],'tree binding');blobs={x['path']:x for x in tree['tree'] if x['type']=='blob'}
missing=[];checked=[]
with zipfile.ZipFile(r/'AN-Paint-source.zip') as z:
 names=z.namelist();need(len(names)==len(set(names)),'source ZIP duplicate names')
 for p,v in blobs.items():
  local=(args.source_root/p).read_bytes();need(git(local)==v['sha'],'local source drift '+p)
  name='AN-Paint/'+p
  if name not in names:missing.append(p);continue
  raw=z.read(name);need(raw==local and git(raw)==v['sha'],'packaged source mismatch '+p);checked.append(p)
need(sorted(missing)==['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore'],'unexpected packager exclusions')
dump(r/'artifact-source-binding.json',{'schema_version':1,'reviewed_head':args.head,'tested_commit':args.expected_commit,'source_tree':args.expected_tree,'run_id':args.run_id,'artifact_id':args.artifact_id,'archive_sha256':args.archive_sha256,'build_info':info,'tracked_files':len(blobs),'packaged_tracked_source_files_exact':len(checked),'packager_exclusions':sorted(missing),'embedded_source_matches_external':True,'limits':'Corresponding-source/CI debug artifact identity, not tests passed, private upgrade signing or release.'})
aapt=args.tools/'aapt2';signer=args.tools/'apksigner.jar'
with (r/'apk-resources.txt').open('w') as out:subprocess.run([str(aapt),'dump','resources',str(r/'app-debug.apk')],stdout=out,check=True)
with (r/'apk-signature.txt').open('w') as out:subprocess.run(['java','-jar',str(signer),'verify','--verbose','--print-certs',str(r/'app-debug.apk')],stdout=out,stderr=subprocess.STDOUT,check=True)
parsed={};current=None
for line in (r/'apk-resources.txt').read_text().splitlines():
 m=re.match(r'\s*resource 0x[0-9a-f]+ string/([^ ]+)',line)
 if m:current=m.group(1)
 elif current:
  m=re.match(r'\s*\(nn\) (".*")$',line)
  if m:need(current not in parsed,'duplicate nn compiled value');parsed[current]=json.loads(m.group(1))
fixture=json.loads((args.source_root/'tools/fixtures/current_localization/nynorsk_p0_remaining_wording.json').read_bytes());old=json.loads((args.source_root/'tools/fixtures/current_localization/nynorsk_save_wording.json').read_bytes());expected={k:v['nn'][1:-1] for k,v in {**fixture['values'],**old['values']}.items()};need(len(expected)==80,'reviewed scope count')
entries=[]
for k,v in expected.items():need(parsed.get(k)==v,'compiled NN text mismatch '+k);entries.append({'identity':'string/'+k,'display_sha256':h(v.encode()),'exact_approved_display_match':True})
sign=(r/'apk-signature.txt').read_text();need(sign.startswith('Verifies\n') and 'Verified using v1 scheme (JAR signing): true' in sign and 'Verified using v2 scheme (APK Signature Scheme v2): true' in sign,'signature schemes');cert=re.search(r'Signer #1 certificate SHA-256 digest: ([0-9a-f]+)',sign);need(cert is not None,'certificate fingerprint')
dump(r/'compiled-resource-verification.json',{'schema_version':1,'run_id':args.run_id,'reviewed_head':args.head,'tested_commit':args.expected_commit,'tree':args.expected_tree,'apk_sha256':info['apk_sha256'],'new_reviewed_entries':72,'prior_reviewed_entries':8,'entries':entries,'signature_exit':0,'v1_verified':True,'v2_verified':True,'CI_debug_certificate_sha256':cert.group(1),'aapt2_sha256':h(aapt.read_bytes()),'apksigner_jar_sha256':h(signer.read_bytes()),'signature_output_sha256':h((r/'apk-signature.txt').read_bytes()),'limits':'Compiled resource and CI debug certificate only; no physical-device, native-language, layout, whole-locale, private upgrade-signing or release claim.'})
print(json.dumps({'source_files_exact':len(checked),'apk_sha256':info['apk_sha256'],'source_sha256':info['source_sha256'],'compiled_reviewed_values':80,'certificate_sha256':cert.group(1)},indent=2))
