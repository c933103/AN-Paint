#!/usr/bin/env python3
"""Bind a retained CI build log to the source-verified delivery; no job-state inference."""
import argparse,json,pathlib,re
from audit_direction_delivery import HEAD,TREE,MERGE,RUN,ZIP_SHA,ARTIFACT_ID,require,sha
LOG_SHA='4f72149d108c83491cfc07452a8109fae7598f6a580826e9b2d8fac60b31b1f4'

def audit(log,delivery):
    raw=log.read_bytes();require(sha(raw)==LOG_SHA,'retained build log differs')
    require(delivery['status']=='PASS' and delivery['tree']==TREE and delivery['merge']==MERGE and str(delivery['run_id'])==RUN,'delivery differs')
    lines=raw.decode().splitlines();clean=[re.sub(r'\x1b\[[0-9;]*m','',line) for line in lines]
    markers=[
        'fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +'+MERGE+':refs/remotes/pull/55/merge',
        'HEAD is now at '+MERGE[:7]+' Merge '+HEAD+' into 71f4d288669858e7975ec4c094b7f47a9a1ff145',
        '> Task :Paintroid:bundleCorrespondingSource',
        '> Task :Paintroid:generateExactScriptResources',
        '> Task :app:processDebugResources',
        '> Task :Paintroid:compileDebugKotlin',
        '> Task :app:packageDebug',
        '> Task :app:assembleDebug',
        'BUILD SUCCESSFUL',
        "source = z.read('assets/local-source/AN-Paint-source.zip')",
        "'commit': os.environ['GITHUB_SHA'], 'run_id': os.environ['GITHUB_RUN_ID']",
        'SHA256 digest of uploaded artifact is '+ZIP_SHA,
        'Artifact apk-and-source-'+MERGE+' successfully finalized. Artifact ID '+str(ARTIFACT_ID),
        'Artifact download URL: https://github.com/c933103/AN-Paint/actions/runs/'+RUN+'/artifacts/'+str(ARTIFACT_ID),
    ]
    hits=[];position=-1
    for marker in markers:
        matches=[i for i in range(position+1,len(clean)) if marker in clean[i]]
        require(matches,'ordered build marker missing: '+marker)
        position=matches[0];hits.append({'line':position+1,'text':clean[position]})
    require('BUILD FAILED' not in raw.decode(),'build log contains Gradle failure')
    return {'status':'PASS','head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'build_log_sha256':LOG_SHA,'build_log_bytes':len(raw),'artifact_id':ARTIFACT_ID,'artifact_sha256':ZIP_SHA,'ordered_build_and_upload_markers':hits,'limit':'Checks the parent-supplied log bytes, checkout/build/source-extraction/upload order and artifact binding. Job conclusion, remote authenticity, signing identity and installed execution are not inferred from log text.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('log','delivery-result','output'):parser.add_argument('--'+key,type=pathlib.Path,required=True)
    a=parser.parse_args();result=audit(a.log,json.loads(a.delivery_result.read_bytes()))
    a.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS: retained build checkout, producer/compile/package, source extraction and matching artifact upload are ordered and bound.')
if __name__=='__main__':main()
