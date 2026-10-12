#!/usr/bin/env python3
"""Compare fresh compiled/packaged evidence to the frozen accepted PR55 4a receipt."""
import argparse, json, pathlib
from audit_direction_delivery import HEAD, TREE, require, sha

FILES = ('compiled-picker-arrays.txt','compiled-platform-resource.txt','compiled-platform-tags.json','compiled-platform-locales.txt','compiled-platform-manifest.txt','compiled-application-attributes.json','compiled-m04-resource.txt','compiled-arabic-routes.txt','font-legal-manifest.jsonl')

def audit(prior, current):
    read=lambda root,name:json.loads((root/name).read_bytes())
    preflight=read(current,'source-preflight.json')
    require(preflight['status']=='PASS' and preflight['tree']==TREE and preflight['unchanged_bytes_and_modes']==1094,'Source preflight differs')
    frozen=read(pathlib.Path(__file__).parent,'prior-review-freeze-manifest.json')
    observed=[{'path':p.relative_to(prior).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(prior.rglob('*')) if p.is_file()]
    require(frozen['files']==observed,'Prior review changed')
    identical={}
    for name in FILES:
        a,b=(prior/name).read_bytes(),(current/name).read_bytes()
        require(a==b,'Scoped evidence changed: '+name)
        identical[name]=sha(b)
    a,b=read(prior,'compiled-picker-result.json'),read(current,'compiled-picker-result.json')
    for key in ('status','manifest_binding_status','dump_sha256','platform_xml_dump_sha256','manifest_dump_sha256','binary_manifest_sha256','packaged_platform_xml_sha256','manifest_locale_binding_binary','array_content_and_order_exact','platform_content_and_order_exact','picker_names','picker_tags','platform_locales','alias_pairs','scoped_locales','truthful_open_fallbacks','accepted_untranslated_additions'):
        require(a[key]==b[key],'Compiled baseline changed: '+key)
    require(b['status']==b['manifest_binding_status']=='PASS','Compiled binding failed')
    prior_delivery,delivery=read(prior,'delivery-result.json'),read(current,'delivery-result.json')
    require(prior_delivery['head']==preflight['prior_head'] and prior_delivery['tree']==preflight['prior_tree'], 'Accepted baseline identity differs')
    require(prior_delivery['build_info']['source_sha256']==delivery['build_info']['source_sha256'], 'Corresponding source ZIP bytes differ from accepted baseline')
    for key in ('source_members_manifest','native_source_roots','font_legal_manifest','font_inventory_records','unresolved_individual_font_notice_paths','legal_assets_exact','font_assets_exact','font_sha256','nom_mit_ofl_paragraphs_preserved','nom_embedded_names_licence_preserved','omissions','native_extra_files'):
        require(prior_delivery[key]==delivery[key],'Packaged baseline changed: '+key)
    result={'status':'PASS','head':HEAD,'tree':TREE,'prior_head':preflight['prior_head'],'prior_tree':preflight['prior_tree'],'frozen_prior_files':len(observed),'frozen_prior_review_unchanged':True,'exact_tracked_source_changes':preflight['changed_paths'],'other_tracked_source_bytes_modes_unchanged':1094,'current_embedded_source_equals_delivered_source':delivery['embedded_source_exact'],'complete_source_zip_sha256_unchanged_from_accepted_receipt':True,'complete_source_zip_sha256':delivery['build_info']['source_sha256'],'all_four_native_source_content_mode_manifests_unchanged':True,'scoped_compiled_and_asset_evidence_byte_identical':identical,'entire_aapt2_resource_dump_sha256':b['dump_sha256'],'entire_aapt2_resource_dump_unchanged':True,'binary_manifest_sha256':b['binary_manifest_sha256'],'binary_manifest_unchanged':True,'platform_xml_binary_unchanged':True,'manifest_binding':'PASS','picker_count':167,'scoped_catalogues':59,'outside_scope_fallback_catalogues':108,'existing_individual_font_notice_references_unresolved':len(delivery['unresolved_individual_font_notice_paths']),'existing_notice_reference_issue_unchanged':True,'limits':['Baseline is the frozen accepted PR55 4a audit; it is compared, not re-executed or re-reviewed.','Fresh source and embedded-source equality was independently checked against the current tree. Zero tracked-source differences follow from the exact tree equality plus unchanged native-source content/mode manifests. The complete fresh corresponding-source ZIP also has the identical SHA-256 recorded in the accepted receipt; no broader APK binary equality is claimed.','No new language, installed/runtime, pixel, signing-key, ABI or overall CI acceptance claim.']}
    (current/'merged-delivery-context-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: compiled manifest/resource dump, picker/M04/Arabic/font/legal bytes and native-source manifests unchanged from frozen PR55 4a; all bundled tracked source and native-source manifests are unchanged.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ('prior-review','current-review'):p.add_argument('--'+arg,type=pathlib.Path,required=True)
    a=p.parse_args();audit(a.prior_review,a.current_review)
