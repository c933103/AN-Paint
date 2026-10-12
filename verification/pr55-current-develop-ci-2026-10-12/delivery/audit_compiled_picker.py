#!/usr/bin/env python3
"""Compare actual compiled picker arrays and platform locales to exact current XML."""
import argparse, json, pathlib, re, struct, subprocess, zipfile, xml.etree.ElementTree as ET
from audit_direction_compiled_m04 import TREE, MERGE, RUN, AAPT_SHA, require, sha

def array_block(text,name):
    matches=re.findall(r'^    resource (0x[0-9a-f]+) array/'+re.escape(name)+r'\n(.*?)(?=^    resource |^  type |\Z)',text,re.S|re.M)
    require(len(matches)==1,'missing/duplicate array: '+name)
    rid,block=matches[0]
    require(len(re.findall(r'^      \(',block,re.M))==1,'unexpected array configuration or syntax: '+name)
    match=re.fullmatch(r'      \(\) \(array\) size=(\d+)\n\s*(\[.*\])\s*',block,re.S)
    require(match is not None,'unexpected array configuration or syntax: '+name)
    count,payload=match.groups();values=json.loads(payload)
    require(len(values)==int(count) and all(isinstance(x,str) for x in values),'array count/type differs: '+name)
    return rid,block,values

def binary_application_attributes(raw):
    """Decode the actual binary XML application attributes, including numeric IDs."""
    kind,header_size,total=struct.unpack_from('<HHI',raw,0)
    require(kind==3 and total==len(raw),'unexpected binary XML envelope')
    strings=None;resource_ids=[];attributes=[];application_count=0;offset=header_size
    def u16_length(start):
        value=struct.unpack_from('<H',raw,start)[0]
        if value&0x8000:return ((value&0x7fff)<<16)|struct.unpack_from('<H',raw,start+2)[0],start+4
        return value,start+2
    def u8_length(start):
        value=raw[start]
        if value&0x80:return ((value&0x7f)<<8)|raw[start+1],start+2
        return value,start+1
    def string(index):
        if index==0xffffffff:return None
        require(strings is not None and index<len(strings),'invalid binary XML string index')
        return strings[index]
    while offset<len(raw):
        kind,header,size=struct.unpack_from('<HHI',raw,offset)
        require(size>=header>=8 and offset+size<=len(raw),'invalid binary XML chunk')
        if kind==1:
            require(strings is None,'duplicate string pool')
            count,styles,flags,start,style_start=struct.unpack_from('<IIIII',raw,offset+8)
            strings=[]
            for index in range(count):
                pos=offset+start+struct.unpack_from('<I',raw,offset+header+4*index)[0]
                if flags&0x100:
                    chars,pos=u8_length(pos);length,pos=u8_length(pos)
                    value=raw[pos:pos+length].decode('utf-8');require(raw[pos+length]==0,'unterminated UTF-8 string')
                else:
                    chars,pos=u16_length(pos);length=2*chars
                    value=raw[pos:pos+length].decode('utf-16-le');require(raw[pos+length:pos+length+2]==b'\0\0','unterminated UTF-16 string')
                strings.append(value)
        elif kind==0x180:
            require((size-header)%4==0,'invalid XML resource map')
            resource_ids=list(struct.unpack_from('<'+'I'*((size-header)//4),raw,offset+header))
        elif kind==0x102:
            ns,name,attr_start,attr_size,attr_count,_,_,_=struct.unpack_from('<IIHHHHHH',raw,offset+header)
            require(attr_size==20,'unexpected XML attribute size')
            if string(name)=='application':
                application_count+=1
                for i in range(attr_count):
                    pos=offset+header+attr_start+i*attr_size
                    ans,aname,araw,value_size,zero,value_type,data=struct.unpack_from('<IIIHBBI',raw,pos)
                    require(value_size==8 and zero==0,'unexpected typed XML value')
                    attributes.append({'namespace':string(ans),'name':string(aname),'name_resource_id':f'0x{resource_ids[aname]:08x}' if aname<len(resource_ids) else None,'raw_value':string(araw),'value_type':f'0x{value_type:02x}','data':f'0x{data:08x}','string_value':string(data) if value_type==3 else None})
        offset+=size
    require(offset==len(raw) and application_count==1,'missing/duplicate application element')
    return attributes

def audit(repo,apk,aapt2,delivery,output):
    require(delivery['status']=='PASS' and delivery['tree']==TREE and delivery['merge']==MERGE and str(delivery['run_id'])==RUN,'delivery provenance mismatch')
    apk_sha=sha(apk.read_bytes());require(apk_sha==delivery['build_info']['apk_sha256'],'APK differs')
    require(sha(aapt2.read_bytes())==AAPT_SHA,'tool differs')
    def source(path):return subprocess.check_output(['git','show',TREE+':'+path],cwd=repo)
    raw=subprocess.check_output([str(aapt2),'dump','resources',str(apk)])
    text=raw.decode();source_bindings={};wanted={};compiled={};blocks=[];ids={}
    for filename in ('app_language_names.xml','app_language_tags.xml'):
        path='Paintroid/src/main/res/values/'+filename;data=source(path)
        source_bindings[path]=sha(data)
        for element in ET.fromstring(data).findall('string-array'):
            name=element.attrib['name'];values=[''.join(item.itertext()) for item in element.findall('item')]
            require(not any('\\' in x or '"' in x for x in values),'unsupported source Android quoting: '+name)
            wanted[name]=values
    require(set(wanted)=={'app_language_names','app_language_tags','app_language_aliases','app_language_alias_targets'},'unexpected source arrays')
    for name,values in wanted.items():
        rid,block,actual=array_block(text,name)
        require(actual==values,'compiled source array/order differs: '+name)
        compiled[name]=actual;ids[name]=rid;blocks.append('resource '+rid+' array/'+name+'\n'+block)
    names=compiled['app_language_names'];tags=compiled['app_language_tags']
    require(len(names)==len(tags)==167 and len(set(tags))==167,'picker count or duplicate tag')
    require(len(compiled['app_language_aliases'])==len(compiled['app_language_alias_targets'])==22,'alias inventory differs')
    locale_path='Paintroid/src/main/res/xml/app_locales.xml';locale_bytes=source(locale_path)
    source_bindings[locale_path]=sha(locale_bytes)
    locale_source=[x.attrib['{http://schemas.android.com/apk/res/android}name'] for x in ET.fromstring(locale_bytes).findall('locale')]
    resource=re.findall(r'^    resource (0x[0-9a-f]+) xml/app_locales\n(.*?)(?=^    resource |\Z)',text,re.S|re.M)
    require(len(resource)==1,'compiled locale resource missing/duplicate')
    locale_rid,locale_resource_block=resource[0]
    require(re.fullmatch(r'      \(\) \(file\) res/xml/app_locales.xml type=XML\s*',locale_resource_block) is not None,'unexpected locale file resource')
    xml_dump=subprocess.check_output([str(aapt2),'dump','xmltree','--file','res/xml/app_locales.xml',str(apk)])
    locale_actual=[json.loads(x) for x in re.findall(r'^\s*A: http://schemas.android.com/apk/res/android:name\(0x01010003\)=(".*?") \(Raw: ".*"\)$',xml_dump.decode(),re.M)]
    require(len(re.findall(r'^\s*E: locale \(',xml_dump.decode(),re.M))==167,'platform locale element count differs')
    require(locale_actual==locale_source==tags,'compiled platform locale order/content differs from current XML/picker')
    manifest=subprocess.check_output([str(aapt2),'dump','xmltree','--file','AndroidManifest.xml',str(apk)])
    bindings=re.findall(r'^\s*A: http://schemas.android.com/apk/res/android:localeConfig\(0x[0-9a-f]+\)=@(0x[0-9a-f]+)\s*$',manifest.decode(),re.M)
    with zipfile.ZipFile(apk) as z:
        binary_manifest=z.read('AndroidManifest.xml')
    attributes=binary_application_attributes(binary_manifest)
    binary_bindings=[row for row in attributes if row['name']=='localeConfig' and row['namespace']=='http://schemas.android.com/apk/res/android']
    source_manifest_path='Paintroid/src/main/AndroidManifest.xml';source_manifest=source(source_manifest_path)
    source_bindings[source_manifest_path]=sha(source_manifest)
    source_declaration=ET.fromstring(source_manifest).find('application').attrib['{http://schemas.android.com/apk/res/android}localeConfig']
    require(source_declaration=='@xml/app_locales','source manifest declaration differs')
    binding_pass=(bindings==[locale_rid] and len(binary_bindings)==1 and binary_bindings[0]['value_type']=='0x01' and binary_bindings[0]['data']==locale_rid)
    app_match=re.search(r'^      E: application[^\n]*\n(.*?)(?=^          E: |\Z)',manifest.decode(),re.S|re.M)
    require(app_match is not None,'aapt2 application excerpt absent')
    manifest_excerpt=app_match[0].splitlines()
    scope_path='tools/fixtures/current_localization/locale_contract_scope.json';scope_bytes=source(scope_path);source_bindings[scope_path]=sha(scope_bytes)
    scope=json.loads(scope_bytes);require(len(scope['scoped_tags'])==59 and len(scope['fallback_tags'])==108,'current 59/108 scope differs')
    require(set(tags)==set(scope['scoped_tags'])|set(scope['fallback_tags']) and not(set(scope['scoped_tags'])&set(scope['fallback_tags'])),'picker/scope partition differs')
    additions=[]
    for fixture in ('language_option_additions_20261012.json','language_option_additions_20261012_second.json'):
        path='tools/fixtures/'+fixture;data=source(path);source_bindings[path]=sha(data)
        additions.extend(json.loads(data)['languages'])
    require(len(additions)==len({row['tag'] for row in additions})==27,'accepted addition inventory differs')
    accepted=[]
    for row in additions:
        tag=row['tag'];position=tags.index(tag);require(names[position]==row['name'],'added name/tag pairing differs: '+tag)
        require(tag in scope['fallback_tags'],'new option incorrectly scoped: '+tag)
        catalogue=source(row['catalogue']);root=ET.fromstring(catalogue)
        require(root.tag=='resources' and len(root)==0,'new catalogue is not empty: '+tag)
        require(row['translation_status']=='not-started' and row['linguistic_review']=='not-started' and row['fallback']=='default-English','added fixture status changed: '+tag)
        accepted.append({'tag':tag,'name':names[position],'picker_index_zero_based':position,'platform_index_zero_based':locale_actual.index(tag),'catalogue':row['catalogue'],'catalogue_sha256':sha(catalogue),'catalogue_child_elements':0,'translation_status':row['translation_status'],'fallback':row['fallback']})
    (output.parent/'compiled-picker-arrays.txt').write_text('\n'.join(blocks))
    (output.parent/'compiled-platform-locales.txt').write_bytes(xml_dump)
    (output.parent/'compiled-platform-manifest.txt').write_text('\n'.join(manifest_excerpt)+'\n')
    (output.parent/'compiled-application-attributes.json').write_text(json.dumps(attributes,indent=2)+'\n')
    result={'status':'PASS' if binding_pass else 'FAIL','compiled_arrays_and_platform_xml_status':'PASS','manifest_binding_status':'PASS' if binding_pass else 'FAIL','tree':TREE,'merge':MERGE,'run_id':int(RUN),'apk_sha256':apk_sha,'aapt2_sha256':AAPT_SHA,'dump_sha256':sha(raw),'platform_xml_dump_sha256':sha(xml_dump),'manifest_dump_sha256':sha(manifest),'binary_manifest_sha256':sha(binary_manifest),'manifest_source_declaration':source_declaration,'manifest_locale_binding_aapt2':bindings,'manifest_locale_binding_binary':binary_bindings,'application_attribute_count':len(attributes),'locale_resource_id':locale_rid,'array_resource_ids':ids,'source_sha256':source_bindings,'picker_names':len(names),'picker_tags':len(tags),'platform_locales':len(locale_actual),'alias_pairs':len(compiled['app_language_aliases']),'array_content_and_order_exact':True,'platform_content_and_order_exact':True,'scoped_locales':59,'truthful_open_fallbacks':108,'accepted_untranslated_additions':accepted,'limits':['Actual compiled values/order and manifest resource binding inspection only; not installed system/app picker interaction, runtime locale resolution or rendering.','Accepted language identities and wording were not re-reviewed. All 27 added catalogues remain empty and untranslated.']}
    if not binding_pass:
        result['finding']='The APK contains the complete platform locale XML but the actual application manifest does not bind it with the source-declared android:localeConfig. Independent binary XML parsing checks all application attribute names, namespace and numeric resource IDs, in addition to aapt2 rendering. System-settings exposure is not established by the XML presence alone.'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('repo','apk','aapt2','delivery-result','output'):parser.add_argument('--'+key,type=pathlib.Path,required=True)
    a=parser.parse_args();result=audit(a.repo,a.apk,a.aapt2,json.loads(a.delivery_result.read_bytes()),a.output)
    print('PASS: actual compiled 167 picker names/tags, 22 aliases and 167 platform locales exactly match current XML; all 27 accepted additions remain empty catalogues in 108 open fallbacks.')
    if result['manifest_binding_status']!='PASS':
        print('FAIL: '+result['finding']);raise SystemExit(1)
    print('PASS: actual manifest localeConfig binding matches compiled platform locale XML.')

if __name__=='__main__':main()
