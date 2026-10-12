#!/usr/bin/env python3
"""Compare aapt2's actual APK string table against the current compact M04 wording fixture on the PR55 current-develop integration delivery."""
import argparse,hashlib,json,pathlib,re,subprocess,xml.etree.ElementTree as ET
TREE='b5d8cbeac9bf6d613ed7c3be787aa984826daafd'
MERGE='e3dc717586539f8bbfe2ae3e3aae87e83db16d19'
RUN='38296205283'
AAPT_SHA='d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,s):
    if not v:raise ValueError(s)
def tag(config):
    if not config:return 'default'
    if config.startswith('b+'):return config[2:].replace('+','-')
    if config=='in':return 'id'
    return config.replace('-r','-')
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('repo','apk','aapt2','delivery-result','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
    a=p.parse_args(); delivery=json.loads(a.delivery_result.read_bytes())
    require(delivery['status']=='PASS' and delivery['merge']==MERGE and delivery['tree']==TREE and str(delivery['run_id'])==RUN,'delivery binding mismatch')
    apk_sha=delivery['build_info']['apk_sha256']
    require(sha(a.apk.read_bytes())==apk_sha,'APK differs');require(sha(a.aapt2.read_bytes())==AAPT_SHA,'tool differs')
    raw=subprocess.check_output([str(a.aapt2),'dump','resources',str(a.apk)])
    text=raw.decode(); blocks=re.findall(r'^    resource (0x[0-9a-f]+) string/commons_metadata_query_failed\n(.*?)(?=^    resource |\Z)',text,re.S|re.M)
    require(len(blocks)==1,'M04 resource missing/duplicate');rid,block=blocks[0]
    actual={};configurations={}
    for line in block.splitlines():
        m=re.fullmatch(r'      \(([^)]*)\) (".*")',line);require(m is not None,'unexpected resource entry '+line)
        cfg,val=m.groups();t=tag(cfg);require(t not in actual,'duplicate configuration');actual[t]=json.loads(val);configurations[t]=cfg
    fixture_path='tools/fixtures/current_localization/commons_metadata_current_wording.json'
    fixture_bytes=subprocess.check_output(['git','show',TREE+':'+fixture_path],cwd=a.repo)
    fixture=json.loads(fixture_bytes)
    scope_bytes=subprocess.check_output(['git','show',TREE+':tools/fixtures/current_localization/locale_contract_scope.json'],cwd=a.repo)
    scope=json.loads(scope_bytes)
    def android_value(value):
        # Current XML fixture values have only Android Unicode/apostrophe escapes.
        value=re.sub(r"\\u([0-9a-fA-F]{4})",lambda m:chr(int(m.group(1),16)),value)
        value=value.replace("\\'","'")
        require('\\' not in value and '"' not in value,'unsupported Android quoting')
        return value
    wanted={tag:android_value(value) for tag,value in fixture['values']['commons_metadata_query_failed'].items()}
    require(set(wanted)=={scope['default_tag'],*scope['scoped_tags']},'current fixture locale scope mismatch')
    require(len(wanted)==60 and len(scope['fallback_tags'])==108,'current scope changed')
    wanted['ko-Kore-KR-anpaint']=wanted['ko-Kore-KR']
    require(actual==wanted,'compiled catalogue values/configuration set mismatch: '+str({'missing':sorted(wanted.keys()-actual.keys()),'extra':sorted(actual.keys()-wanted.keys()),'changed':[t for t in actual.keys()&wanted.keys() if actual[t]!=wanted[t]]}))
    controls={t:{f'U+{cp:04X}':[i for i,c in enumerate(actual[t]) if ord(c)==cp] for cp in (0x180e,0x202f)} for t in ('mnc-Mong','mn-Mong')}
    require(controls['mnc-Mong']['U+180E']==[7,18,27] and controls['mn-Mong']['U+202F']==[7,17,30],'script controls moved/removed')
    (a.output.parent/'compiled-m04-resource.txt').write_text('resource '+rid+' string/commons_metadata_query_failed\n'+block)
    result={'status':'PASS','tree':TREE,'apk_sha256':apk_sha,'merge':MERGE,'run_id':int(RUN),'aapt2_sha256':AAPT_SHA,'aapt2_origin':'Executed the existing retained Android SDK Build Tools 35.0.0 aapt2. Its pinned digest also equals verification-tools/aapt2 in this fresh artifact, as recorded by artifact-bindings-result.json. No new SDK installed.','dump_sha256':sha(raw),'fixture_path':fixture_path,'fixture_sha256':sha(fixture_bytes),'scope_fixture_sha256':sha(scope_bytes),'resource_id':rid,'compiled_configurations':len(actual),'scope':'default + exact 59 + generated mixed-script Korean resource alias; no unexpected M04 entry for other locales','controls_zero_based':controls,'values':actual,'android_configurations':configurations,'limits':['Compiled table proves value/configuration/control retention, not runtime locale resolution, shaping, rendering or linguistic acceptance.','108 omitted locale keys retain fallback semantics; this dump alone does not execute all fallback choices.']}
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('status','compiled_configurations','controls_zero_based','limits')},indent=2))
if __name__=='__main__':main()
