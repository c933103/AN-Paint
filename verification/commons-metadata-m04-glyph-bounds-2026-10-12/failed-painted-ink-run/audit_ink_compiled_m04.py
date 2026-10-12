#!/usr/bin/env python3
"""Compare aapt2's actual APK string table against the unchanged frozen M04 fixture on the PR55 painted-ink successor."""
import argparse,hashlib,json,pathlib,re,subprocess,xml.etree.ElementTree as ET
TREE='8752ed99c9350235da46fac1b4a188ca89296889'
MERGE='9af58e46c6a7196ef90c60e345bcd7a5194ffacf'
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
    require(delivery['status']=='PASS' and delivery['merge']==MERGE and delivery['tree']==TREE and str(delivery['run_id'])=='38250189049','delivery binding mismatch')
    apk_sha=delivery['build_info']['apk_sha256']
    require(sha(a.apk.read_bytes())==apk_sha,'APK differs');require(sha(a.aapt2.read_bytes())==AAPT_SHA,'tool differs')
    raw=subprocess.check_output([str(a.aapt2),'dump','resources',str(a.apk)])
    text=raw.decode(); blocks=re.findall(r'^    resource (0x[0-9a-f]+) string/commons_metadata_query_failed\n(.*?)(?=^    resource |\Z)',text,re.S|re.M)
    require(len(blocks)==1,'M04 resource missing/duplicate');rid,block=blocks[0]
    actual={};configurations={}
    for line in block.splitlines():
        m=re.fullmatch(r'      \(([^)]*)\) (".*")',line);require(m is not None,'unexpected resource entry '+line)
        cfg,val=m.groups();t=tag(cfg);require(t not in actual,'duplicate configuration');actual[t]=json.loads(val);configurations[t]=cfg
    fixture_bytes=subprocess.check_output(['git','show',TREE+':tools/fixtures/commons_metadata_query_failure_scope.json'],cwd=a.repo)
    fixture=json.loads(fixture_bytes);wanted={}
    for e in fixture['entries']:
        node=ET.fromstring('<resources>'+e['line']+'</resources>').find('string')
        require(node is not None,'missing fixture string');s=''.join(node.itertext()).replace("\\'","'")
        require('\\' not in s and '"' not in s,'unexpected Android quoting');wanted[e['tag']]=s
    require(len(wanted)==60,'source scope differs');wanted['ko-Kore-KR-anpaint']=wanted['ko-Kore-KR']
    require(actual==wanted,'compiled catalogue values/configuration set mismatch: '+str({'missing':sorted(wanted.keys()-actual.keys()),'extra':sorted(actual.keys()-wanted.keys()),'changed':[t for t in actual.keys()&wanted.keys() if actual[t]!=wanted[t]]}))
    controls={t:{f'U+{cp:04X}':[i for i,c in enumerate(actual[t]) if ord(c)==cp] for cp in (0x180e,0x202f)} for t in ('mnc-Mong','mn-Mong')}
    require(controls['mnc-Mong']['U+180E']==[7,18,27] and controls['mn-Mong']['U+202F']==[7,17,30],'script controls moved/removed')
    (a.output.parent/'compiled-m04-resource.txt').write_text('resource '+rid+' string/commons_metadata_query_failed\n'+block)
    result={'status':'PASS','tree':TREE,'apk_sha256':apk_sha,'merge':MERGE,'run_id':38250189049,'aapt2_sha256':AAPT_SHA,'aapt2_origin':'Existing CI tools/ci_prepare_build.sh copies Android SDK build-tools/35.0.0/aapt2 into source-bound artifact. No new SDK installed.','dump_sha256':sha(raw),'fixture_sha256':sha(fixture_bytes),'resource_id':rid,'compiled_configurations':len(actual),'scope':'default + exact 59 + generated mixed-script Korean resource alias; no unexpected M04 entry for other locales','controls_zero_based':controls,'values':actual,'android_configurations':configurations,'limits':['Compiled table proves value/configuration/control retention, not runtime locale resolution, shaping, rendering or linguistic acceptance.','81 omitted locale keys retain fallback semantics; this dump alone does not execute all fallback choices.']}
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('status','compiled_configurations','controls_zero_based','limits')},indent=2))
if __name__=='__main__':main()
