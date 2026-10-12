#!/usr/bin/env python3
"""Compare unchanged scoped compiled/assets/native results to historical reference only."""
import argparse,json,pathlib
from audit_direction_delivery import require,sha,TREE,HEAD,MERGE,RUN
EVIDENCE=('compiled-m04-resource.txt','compiled-arabic-routes.txt','compiled-picker-arrays.txt','compiled-platform-resource.txt','compiled-platform-tags.json','compiled-platform-locales.txt','compiled-platform-manifest.txt','compiled-application-attributes.json','font-legal-manifest.jsonl')
def audit(prior,current):
    def get(root,name):return json.loads((root/(name+'-result.json')).read_bytes())
    old=get(prior,'delivery');new=get(current,'delivery')
    require(new['head']==HEAD and new['tree']==TREE and new['merge']==MERGE and str(new['run_id'])==RUN,'fresh delivery differs')
    fields=('native_source_roots','native_extra_files','font_inventory_records','font_assets_exact','legal_assets_exact','font_sha256','omissions','unresolved_individual_font_notice_paths')
    for k in fields:require(old[k]==new[k],'unchanged delivery field differs: '+k)
    rows=[]
    for name in EVIDENCE:
        data=(current/name).read_bytes();require(data==(prior/name).read_bytes(),'unchanged scoped evidence differs: '+name)
        rows.append({'path':name,'sha256':sha(data),'bytes':len(data),'equal_to_historical':True})
    hashes={}
    for group,keys in [('compiled-m04',['dump_sha256','fixture_sha256','scope_fixture_sha256','controls_zero_based']),('compiled-arabic',['dump_sha256','source_arabic_sha256']),('compiled-picker',['dump_sha256','platform_xml_dump_sha256','manifest_dump_sha256','binary_manifest_sha256','packaged_platform_xml_sha256','source_sha256'])]:
        a,b=get(prior,group),get(current,group)
        require(a['status']==b['status']=='PASS','compiled review status differs')
        for key in keys:require(a[key]==b[key],'historical resource evidence differs: '+group+'/'+key)
        hashes[group]=keys
    return {'status':'PASS','head':HEAD,'tree':TREE,'merge':MERGE,'run_id':int(RUN),'native_font_legal_and_omission_fields_equal':list(fields),'scoped_evidence_equal':rows,'compiled_result_fields_equal':hashes,'apk_sha256':new['build_info']['apk_sha256'],'source_sha256':new['build_info']['source_sha256'],'apk_differs_from_historical':new['build_info']['apk_sha256']!=old['build_info']['apk_sha256'],'source_zip_differs_from_historical':new['build_info']['source_sha256']!=old['build_info']['source_sha256'],'limits':['Equality is scoped to independently verified compiled resources, manifest, font/legal assets and four native-source manifests. APK, source ZIP and Kotlin behavior changed; no whole-APK equality or runtime/rendering reuse is inferred.','Historical review is only a reference, never fresh acceptance credit. Ten unresolved individual font-notice metadata references are unchanged; complete aggregate notices remain present.']}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('historical-review','current-review'):p.add_argument('--'+k,type=pathlib.Path,required=True)
    a=p.parse_args();r=audit(a.historical_review,a.current_review);(a.current_review/'historical-comparison-result.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS: exact unchanged scoped compiled, font/legal and native evidence; fresh APK/source hashes retained separately.')
