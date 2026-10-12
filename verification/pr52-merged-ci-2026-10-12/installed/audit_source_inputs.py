#!/usr/bin/env python3
"""Bind every read/imported input used in the installed audit to the frozen tree."""
import argparse,json,pathlib,stat,subprocess
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,sha,require,BINDING,messages
FILES=('app/src/main/AndroidManifest.xml','Paintroid/src/main/res/values/app_language_tags.xml','Paintroid/src/main/res/xml/app_locales.xml','.github/workflows/android.yml','tools/ci_emulator.sh','tools/run_android_instrumentation.py','tools/app_instrumentation_matrix.py','tools/vertical_locale_matrix.py','tools/installed_glyph_ink_evidence.py','tools/test_installed_glyph_ink_evidence.py','tools/vertical_control_reachability.py','tools/vertical_evidence_transport.py','Paintroid/src/main/res/values/strings.xml','Paintroid/src/main/res/values-ar/strings.xml')
ROOTS=('app/src/androidTest','Paintroid/src/androidTest')
def audit(repo):
 require(BINDING['merge_tree']==TREE and BINDING['merge_parents']==[BINDING['base'],HEAD],'supplied merge tree/ordered parents differ')
 require({r:v for (tag,r),v in messages(repo).items()}==BINDING['arabic_messages'],'current source messages differ')
 raw=subprocess.check_output(['git','ls-tree','-rz',TREE,'--',*FILES,*ROOTS],cwd=repo);rows=[];listed=set()
 for entry in raw.split(b'\0'):
  if not entry:continue
  head,name=entry.split(b'\t');mode,kind,oid=head.decode().split();name=name.decode();require(kind=='blob','unsupported source kind')
  p=repo/name;data=subprocess.check_output(['git','cat-file','blob',oid],cwd=repo)
  require(not p.is_symlink() and p.is_file() and data==p.read_bytes(),'frozen source byte mismatch '+name)
  require(bool(p.stat().st_mode&stat.S_IXUSR)==(mode=='100755'),'executable mode differs '+name)
  rows.append({'path':name,'mode':mode,'git_blob':oid,'sha256':sha(data)});listed.add(name)
 require(set(FILES)<=listed,'missing frozen helper or resource input')
 for root in ROOTS:
  expected={x for x in listed if x.startswith(root+'/')};found={x.relative_to(repo).as_posix() for x in (repo/root).rglob('*') if x.is_file()}
  require(found==expected,'test source file inventory mismatch '+root)
 return {'status':'PASS','head':HEAD,'merge':MERGE,'tree':TREE,'run_id':int(RUN),'checked_files':len(rows),'inputs':rows,'limit':'Exact bytes/modes of audit inputs and complete test-source trees; main production/APK audit is separate.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();r=audit(a.repo);a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r['checked_files'],'exact source inputs')
