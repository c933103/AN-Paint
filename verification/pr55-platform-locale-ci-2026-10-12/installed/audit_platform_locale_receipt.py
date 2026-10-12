#!/usr/bin/env python3
"""Exact fresh installed framework receipt; source/run/install provenance is checked separately."""
import argparse,hashlib,json,pathlib,re,xml.etree.ElementTree as ET
MARKER='platformLocaleConfigStatus='
def require(v,message):
 if not v:raise ValueError(message)
def check(text,expected,sdk):
 require(type(sdk) is int and sdk>=33,'framework API is not selected on this SDK')
 require(expected and len(expected)==len(set(expected)),'invalid current expected inventory')
 lines=[(i+1,line) for i,line in enumerate(text.splitlines()) if MARKER in line]
 require(len(lines)==1,'missing or duplicate platform receipt')
 number,line=lines[0];m=re.search(r'platformLocaleConfigStatus=(-?\d+) expected=(\S*) actual=(\S*)\s*$',line)
 require(m is not None,'malformed platform receipt');status=int(m[1]);require(status==0,'framework status is not STATUS_SUCCESS')
 want=m[2].split(',');got=m[3].split(',');require(want==expected,'logged expected inventory differs from current source')
 require(got and all(got) and len(got)==len(set(got)),'empty or duplicate platform locales')
 require(len(got)==len(expected) and set(got)==set(expected),'platform exact current tag set differs')
 return {'status':'PASS_INSTALLED_FRAMEWORK_LOCALE_DISCOVERY','sdk':sdk,'framework_status':status,'expected_count':len(expected),'actual_count':len(got),'line':number,'expected_tags':expected,'actual_tags':got,'override_scope':'manifest/resource configuration, ignoring overrides' if sdk>=34 else 'API33 constructor; source reviewed fallback','limits':['This receipt requires separate exact source/run/prebuilt installation and complete method-protocol reconciliation.','Not a Settings UI visibility observation or translation-completeness claim.']}
def main():
 p=argparse.ArgumentParser();p.add_argument('--log',type=pathlib.Path,required=True);p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--sdk',type=int,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();source=a.repo/'Paintroid/src/main/res/values/app_language_tags.xml';raw=source.read_bytes();arr=ET.fromstring(raw).find("string-array[@name='app_language_tags']");require(arr is not None,'current tag array missing');expected=[e.text for e in arr];log=a.log.read_bytes();r=check(log.decode('utf-8-sig'),expected,a.sdk);r.update({'log_sha256':hashlib.sha256(log).hexdigest(),'source_tag_array_sha256':hashlib.sha256(raw).hexdigest()});a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('status','sdk','expected_count','actual_count')},indent=2))
if __name__=='__main__':main()
