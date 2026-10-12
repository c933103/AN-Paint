#!/usr/bin/env python3
"""Bind compiled Arabic M04/wrapper strings to the exact current source; no installed claim."""
import argparse, hashlib, json, pathlib, re, subprocess, xml.etree.ElementTree as ET
from audit_migration_compiled_m04 import TREE, MERGE, RUN, AAPT_SHA, require, sha


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('repo','apk','aapt2','delivery-result','output'):
        parser.add_argument('--'+key,type=pathlib.Path,required=True)
    a=parser.parse_args();delivery=json.loads(a.delivery_result.read_bytes())
    require(delivery['status']=='PASS' and delivery['tree']==TREE and delivery['merge']==MERGE and str(delivery['run_id'])==RUN,'delivery provenance mismatch')
    apk_sha=sha(a.apk.read_bytes())
    require(apk_sha==delivery['build_info']['apk_sha256'],'source-bound APK differs')
    require(sha(a.aapt2.read_bytes())==AAPT_SHA,'tool differs')
    raw=subprocess.check_output([str(a.aapt2),'dump','resources',str(a.apk)])
    xml=subprocess.check_output(['git','show',TREE+':Paintroid/src/main/res/values-ar/strings.xml'],cwd=a.repo)
    root=ET.fromstring(xml);values={};blocks=[]
    for key in ('commons_metadata_query_failed','commons_credit_copy_failed_reason','ui_could_not_load_gallery_image'):
        matching=re.findall(r'^    resource (0x[0-9a-f]+) string/'+key+r'\n(.*?)(?=^    resource |\Z)',raw.decode(),re.S|re.M)
        require(len(matching)==1,'compiled resource absent/duplicate: '+key)
        rid,block=matching[0]
        line=re.findall(r'^      \(ar\) (".*")$',block,re.M)
        require(len(line)==1,'compiled Arabic absent/duplicate: '+key)
        values[key]=json.loads(line[0]);nodes=root.findall("./string[@name='"+key+"']")
        require(len(nodes)==1,'source Arabic absent/duplicate: '+key)
        expected=''.join(nodes[0].itertext()).replace("\\'","'")
        require('\\' not in expected,'unsupported source escape')
        require(values[key]==expected,'compiled Arabic differs from source: '+key)
        blocks.append('resource '+rid+' string/'+key+'\n      (ar) '+line[0])
    routes={route:values[key].replace('%1$s',values['commons_metadata_query_failed']) for route,key in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]}
    result={'status':'PASS','tree':TREE,'merge':MERGE,'run_id':int(RUN),'apk_sha256':apk_sha,'aapt2_sha256':AAPT_SHA,'dump_sha256':sha(raw),'source_arabic_sha256':sha(xml),'values':values,'composed_route_text':routes,'limit':'Compiled source-equal Arabic strings and mechanical format composition only; no installed, rendering, helper or decoder acceptance claim.'}
    (a.output.parent/'compiled-arabic-routes.txt').write_text('\n'.join(blocks)+'\n')
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS: all three compiled Arabic values match current source; two composed route strings retained for independent installed comparison.')

if __name__=='__main__':main()
