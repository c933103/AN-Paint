#!/usr/bin/env python3
"""Bound current same-run prebuilt download/install receipt audit; no on-device APK hash claim."""
import argparse,json,pathlib,subprocess,re,hashlib
from audit_natural_artifacts import HEAD,TREE,MERGE,RUN,require,sha
DOWNLOADS={'apk-and-source':(11760314237,'a9134a6575b8e61a1b90cf63309b455da1dabeaaa68f6b55faa7bcec63cdf1a8'),'instrumentation-apks':(11760663150,'5fe573e500a307cb636a62a830d0ef4e73ec4335c02a91a781f720bf8186cef6')}
def audit(repo,p,receipt_only=False):
 info=json.loads((p/'apk-and-source/build/delivery/build-info.json').read_bytes())
 require(info['commit']==MERGE and str(info['run_id'])==RUN and info['build_variant']=='debug','build-info binding')
 for k,path in [('apk_sha256','apk-and-source/app/build/outputs/apk/debug/app-debug.apk'),('source_sha256','apk-and-source/build/delivery/AN-Paint-source.zip')]:
  require(isinstance(info[k],str) and re.fullmatch('[0-9a-f]{64}',info[k]),'invalid payload digest')
  if not receipt_only:require(info[k]==sha((p/path).read_bytes()),'actual delivery digest differs')
 source=subprocess.check_output(['git','show',TREE+':tools/ci_emulator.sh'],cwd=repo).decode();require(source==(repo/'tools/ci_emulator.sh').read_text(),'local install driver differs from tree')
 for token in ['"$adb" install -r -t "build/prebuilt/app/build/outputs/apk/$variant/app-$variant.apk"','--apk "build/prebuilt/app/build/outputs/apk/androidTest/$variant/app-$variant-androidTest.apk"','--apk "build/prebuilt/Paintroid/build/outputs/apk/androidTest/$variant/Paintroid-$variant-androidTest.apk"']:require(token in source,'prebuilt install source differs')
 rows=[]
 for api in (30,35):
  path=p/f'emulator-api-{api}-job.log';raw=path.read_bytes();s=raw.decode('utf-8-sig');lines=s.splitlines()
  require('HEAD is now at e191c46 Merge '+HEAD+' into 71f4d288669858e7975ec4c094b7f47a9a1ff145' in s,'job checkout differs')
  require(s.count('digest-mismatch: error')==2 and s.count('run-id: '+RUN)==2,'digest enforcement/same-run receipt differs')
  for name,(aid,digest) in DOWNLOADS.items():
   require(f'name: {name}-{MERGE}' in s and f'(ID: {aid}, Size:' in s and 'Expected Digest: sha256:'+digest in s and 'SHA256 digest of downloaded artifact is '+digest in s,'artifact receipt differs')
  require('Run bash tools/ci_emulator.sh' in s and 'BUILD_VARIANT: debug' in s and f'TEST_API: {api}' in s,'driver/variant/API binding')
  require(re.search(r'Install main APK \(60s maximum\).*?Performing Streamed Install\n[^\n]*Success',s,re.S),'main install success absent')
  installs=sorted((p/f'emulator-api-{api}').rglob('install.log'));require(installs,'test install receipts absent')
  for log in installs:require(log.read_text().strip()=='Performing Streamed Install\nSuccess','test install did not report success '+str(log))
  terms=('HEAD is now at','name: apk-and-source','name: instrumentation-apks','run-id:','digest-mismatch:','Expected Digest:','SHA256 digest of downloaded artifact','Run bash tools/ci_emulator.sh','BUILD_VARIANT:','TEST_API:','Install main APK')
  excerpts=[{'line':i+1,'text':line} for i,line in enumerate(lines) if any(t in line for t in terms)]
  rows.append({'api':api,'job_log_sha256':sha(raw),'job_log_bytes':len(raw),'test_install_receipts':[{'path':str(x.relative_to(p)),'sha256':sha(x.read_bytes())} for x in installs],'evidence':excerpts})
 return {'status':'PASS_RECEIPT_ONLY_PREBUILT_PROVENANCE' if receipt_only else 'PASS_BOUNDED_PREBUILT_PROVENANCE','payload_hash_recomputed':not receipt_only,'head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'build_info':info,'install_driver_sha256':sha(source.encode()),'downloads':{k:{'artifact_id':v[0],'sha256':v[1]} for k,v in DOWNLOADS.items()},'jobs':rows,'limitations':['Same-run digest-enforced main/test artifact download and install receipts verified. Payload equality independently rehashed only when payload_hash_recomputed is true; expiry-safe receipt replay intentionally omits APK/source payloads.','Instrumentation APK archive not independently extracted or hashed on the emulator; install success/source-test fingerprints/raw identities provide the bounded test-APK provenance.','CI debug signing; no release signing or upgrade-key claim.']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--artifacts',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--receipt-only',action='store_true');a=p.parse_args();r=audit(a.repo,a.artifacts,a.receipt_only);a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
