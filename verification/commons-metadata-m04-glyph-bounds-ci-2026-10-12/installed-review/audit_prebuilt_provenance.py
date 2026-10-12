#!/usr/bin/env python3
"""Verify the writer's bounded prebuilt receipt against actual retained job logs."""
import argparse,json,pathlib
from forensic_installed_ink import TREE,HEAD,MERGE,RUN,sha,require

def main():
 p=argparse.ArgumentParser();p.add_argument('--artifact-root',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
 path=a.artifact_root/'installed-prebuilt-provenance.json';raw=path.read_bytes();require(sha(raw)=='85ce907951158fdcd3e44b3844a2711f72a86e8228c7c21a3103c2205bbb70e9','writer provenance changed');d=json.loads(raw)
 require((d['source_head'],d['source_merge'],d['tree'],d['run_id'])==(HEAD,MERGE,TREE,RUN),'source binding differs')
 info=json.loads((a.artifact_root/'apk-and-source/build/delivery/build-info.json').read_bytes());require(info==d['build_info'],'build-info differs')
 require(info['apk_sha256']==sha((a.artifact_root/'apk-and-source/app/build/outputs/apk/debug/app-debug.apk').read_bytes()),'actual main APK differs')
 require(info['source_sha256']==sha((a.artifact_root/'apk-and-source/build/delivery/AN-Paint-source.zip').read_bytes()),'actual source ZIP differs')
 for j in d['jobs']:
  log=(a.artifact_root/f"api{j['api']}-job.log").read_bytes();require(sha(log)==j['log_sha256'],'job log differs');lines=log.decode('utf-8-sig').splitlines();s='\n'.join(lines)
  for e in j['evidence']:require(lines[e['line']-1]==e['text'],'job receipt excerpt differs')
  require('HEAD is now at b750c54 Merge '+HEAD+' into 71f4d288669858e7975ec4c094b7f47a9a1ff145' in s,'job checkout binding')
  require(s.count('digest-mismatch: error')==2,'download digest enforcement count')
  require(s.count('run-id: '+str(RUN))==2,'same-run download binding')
  for name,digest in [('apk-and-source','7f625c5b6f8b78c58fb5d265ad92320d6c176e771f13cc8e5cdc63ff7304217f'),('instrumentation-apks','a13817358657049b265c17aed0b630c6df4829a4c00f29c74e352ea25d6ff7d2')]:
   require('name: '+name+'-'+MERGE in s and 'Expected Digest: sha256:'+digest in s and 'SHA256 digest of downloaded artifact is '+digest in s,'prebuilt download digest receipt')
 result={'status':'PASS_BOUNDED_PROVENANCE','writer_receipt_sha256':sha(raw),'head':HEAD,'merge':MERGE,'tree':TREE,'run_id':RUN,'job_log_hashes':{str(j['api']):j['log_sha256'] for j in d['jobs']},'limitation':'Same-run exact-name digest-enforced prebuilt download and successful install receipts; no independent extraction/on-device hash of instrumentation test APKs. Source test digests/raw identities and actual main-APK source binding checked separately. API35 outcome remains failed.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
