#!/usr/bin/env python3
"""One-time prior/current APK manifest comparison; no source or old evidence writes."""
import argparse,json,pathlib,subprocess,zipfile
from audit_direction_delivery import TREE,HEAD,require,sha
from audit_compiled_picker import binary_application_attributes

PRIOR_TREE='d2379b932cc976bb5347515887ecdfc4729ee70d'
PRIOR_APK_SHA='1a51061a64cb628b239cf3b442a4e6d372563cc5d7be789a4a41489d6aa054b2'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('repo','prior-apk','current-apk','delivery-result','output'):p.add_argument('--'+key,type=pathlib.Path,required=True)
    a=p.parse_args();delivery=json.loads(a.delivery_result.read_bytes())
    require(delivery['status']=='PASS' and delivery['tree']==TREE and delivery['head']==HEAD,'delivery provenance differs')
    require(sha(a.prior_apk.read_bytes())==PRIOR_APK_SHA,'prior APK differs')
    require(sha(a.current_apk.read_bytes())==delivery['build_info']['apk_sha256'],'current APK differs')
    manifests=[];rows=[]
    for label,path in [('prior',a.prior_apk),('current',a.current_apk)]:
        with zipfile.ZipFile(path) as z:raw=z.read('AndroidManifest.xml')
        attributes=binary_application_attributes(raw);bindings=[r for r in attributes if r['name']=='localeConfig']
        manifests.append(raw);rows.append({'label':label,'apk_sha256':sha(path.read_bytes()),'binary_manifest_sha256':sha(raw),'binary_manifest_bytes':len(raw),'application_attributes':len(attributes),'localeConfig_bindings':bindings})
    require(manifests[0]==manifests[1],'prior/current manifest bytes differ')
    require(all(not r['localeConfig_bindings'] for r in rows),'prior/current observation differs')
    sources={}
    for path in ('Paintroid/src/main/AndroidManifest.xml','app/src/main/AndroidManifest.xml'):
        prior=subprocess.check_output(['git','show',PRIOR_TREE+':'+path],cwd=a.repo)
        current=subprocess.check_output(['git','show',TREE+':'+path],cwd=a.repo)
        require(prior==current,'source manifest changed: '+path)
        sources[path]={'sha256':sha(current),'bytes':len(current),'unchanged':True}
    result={'status':'PASS','observation':'The fresh and preceding direction-fixture APK AndroidManifest.xml files are byte-identical; both omit localeConfig from their 12 application attributes. Both source manifests are also unchanged between source trees. This is a pre-existing delivery/platform binding issue, not a regression introduced by current develop integration.','prior_tree':PRIOR_TREE,'current_tree':TREE,'apk_observations':rows,'source_manifests':sources,'limits':['One-time context comparison with hash-pinned prior artifact; previous review conclusions are not restored.','Cause within merging/packaging and installed system-settings behavior are not established by this comparison.']}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: prior/current APK manifests are byte-identical and both lack localeConfig; both source manifest files are unchanged.')

if __name__=='__main__':main()
