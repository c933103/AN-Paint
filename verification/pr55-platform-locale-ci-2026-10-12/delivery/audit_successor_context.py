#!/usr/bin/env python3
"""Compare bounded successor outputs with the read-only frozen predecessor."""
import argparse,hashlib,json,pathlib
from audit_direction_delivery import require,sha,TREE,HEAD

def audit(prior,current):
    frozen=json.loads((current/'prior-review-freeze-manifest.json').read_bytes())
    observed=[{'path':p.relative_to(prior).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(prior.rglob('*')) if p.is_file()]
    require(frozen['files']==observed,'frozen predecessor file set/size/bytes changed')
    def read(root,name):return json.loads((root/name).read_bytes())
    a=read(prior,'compiled-picker-result.json');b=read(current,'compiled-picker-result.json')
    require(a['manifest_binding_status']=='FAIL' and b['manifest_binding_status']=='PASS','predecessor/successor manifest statuses differ')
    for key in ('picker_names','picker_tags','platform_locales','alias_pairs','array_content_and_order_exact','platform_content_and_order_exact','scoped_locales','truthful_open_fallbacks','accepted_untranslated_additions'):
        require(a[key]==b[key],'picker inventory/content/status changed: '+key)
    exact_files=['compiled-picker-arrays.txt','compiled-platform-locales.txt','compiled-m04-resource.txt','compiled-arabic-routes.txt','font-legal-manifest.jsonl']
    for name in exact_files:require((prior/name).read_bytes()==(current/name).read_bytes(),'compiled/assets changed: '+name)
    attrs_a=read(prior,'compiled-application-attributes.json');attrs_b=read(current,'compiled-application-attributes.json')
    def semantic(row):
        return {key:value for key,value in row.items() if key!='data' or row['value_type']!='0x03'}
    require([semantic(row) for row in attrs_b if row['name']!='localeConfig']==[semantic(row) for row in attrs_a],'other compiled application attribute semantics changed')
    index_changes=[{'attribute':a['name'],'old_string_pool_index':a['data'],'new_string_pool_index':b['data'],'decoded_string':a['string_value']} for a,b in zip(attrs_a,[row for row in attrs_b if row['name']!='localeConfig']) if a['data']!=b['data']]
    require(all(a['value_type']==b['value_type']=='0x03' and a['string_value']==b['string_value'] for a,b in zip(attrs_a,[row for row in attrs_b if row['name']!='localeConfig']) if a['data']!=b['data']),'non-string reference changed')
    added=[row for row in attrs_b if row['name']=='localeConfig']
    require(len(attrs_a)==12 and len(attrs_b)==13 and added==b['manifest_locale_binding_binary'],'compiled manifest change inventory differs')
    result={'status':'PASS','tree':TREE,'head':HEAD,'prior_tree':a['tree'],'frozen_prior_review_files':len(observed),'frozen_prior_review_unchanged':True,'prior_manifest_binding':'FAIL','current_manifest_binding':'PASS','prior_binary_manifest_sha256':a['binary_manifest_sha256'],'current_binary_manifest_sha256':b['binary_manifest_sha256'],'prior_application_attributes':len(attrs_a),'current_application_attributes':len(attrs_b),'only_added_application_attribute':added,'all_other_application_attribute_semantics_unchanged':True,'string_pool_index_relocations':index_changes,'byte_identical_compiled_and_asset_evidence':{name:sha((current/name).read_bytes()) for name in exact_files},'picker_inventory_catalogue_statuses_unchanged':True,'limits':['Bounded compiled/resource/asset comparison only. No installed LocaleConfig, Settings UI, rendering, upgrade-signing or overall CI claim.','The frozen earlier finding remains intact; this separate successor records the repaired compiled binding.']}
    (current/'successor-context-result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior-review',type=pathlib.Path,required=True);p.add_argument('--current-review',type=pathlib.Path,required=True);a=p.parse_args()
    result=audit(a.prior_review,a.current_review)
    print('PASS: predecessor frozen; new localeConfig is the sole semantic compiled application attribute addition; picker/M04/Arabic/font/legal scoped evidence is byte-identical.')
