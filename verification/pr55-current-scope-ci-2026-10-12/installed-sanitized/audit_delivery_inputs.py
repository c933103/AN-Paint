#!/usr/bin/env python3
"""Read-only same-run APK/source and compiled Arabic resource audit; no Android execution."""
import argparse,hashlib,json,pathlib,re,subprocess,xml.etree.ElementTree as ET,zipfile
from audit_natural_artifacts import BINDING,HEAD,TREE,MERGE,RUN,require,sha

def audit(repo,artifacts,aapt2):
 info=json.loads((artifacts/'apk-and-source/build/delivery/build-info.json').read_bytes())
 require(info['commit']==MERGE and str(info['run_id'])==RUN,'delivery binding')
 apk=artifacts/'apk-and-source/app/build/outputs/apk/debug/app-debug.apk';source=artifacts/'apk-and-source/build/delivery/AN-Paint-source.zip';raw=source.read_bytes()
 require(sha(raw)==info['source_sha256'] and sha(apk.read_bytes())==info['apk_sha256'],'delivery payload digest mismatch')
 pins=json.loads((pathlib.Path(__file__).parent/'artifact-binding.json').read_bytes());outer=artifacts/'apk-and-source.zip';require(sha(outer.read_bytes())==pins['downloads']['apk-and-source']['sha256'],'official delivery artifact digest mismatch')
 with zipfile.ZipFile(apk) as z:require(z.read('assets/local-source/AN-Paint-source.zip')==raw,'embedded source differs')
 entries=subprocess.check_output(['git','ls-tree','-rz',TREE],cwd=repo).split(b'\0');tracked={}
 for entry in entries:
  if not entry:continue
  head,path=entry.split(b'\t');mode,kind,oid=head.decode().split();require(kind=='blob','unexpected tracked source kind');tracked[path.decode()]=(mode,oid)
 omitted=[];checked=[]
 with zipfile.ZipFile(source) as z:
  names=[n for n in z.namelist() if not n.endswith('/')];require(len(names)==len(set(names)),'duplicate source ZIP member')
  for name in names:
   q=pathlib.PurePosixPath(name);require(not q.is_absolute() and '..' not in q.parts and '\\' not in name,'unsafe source ZIP member')
  for path,(mode,oid) in tracked.items():
   if 'AN-Paint/'+path not in names:
    require(path.endswith('/.gitignore') or path=='.gitignore' or path.startswith('.idea/'),'unexpected source omission '+path);omitted.append(path);continue
   expected=subprocess.check_output(['git','cat-file','blob',oid],cwd=repo);require(z.read('AN-Paint/'+path)==expected,'source differs '+path);checked.append(path)
  extra=[n for n in names if n.removeprefix('AN-Paint/') not in tracked]
  require(all(any(n.startswith('AN-Paint/Paintroid/build/'+p+'/') for p in ('jxl-source','webp-source','heif-source','tiff-source')) for n in extra),'non-native extra source')
 dump=subprocess.check_output([str(aapt2),'dump','resources',str(apk)]);text=dump.decode();values={}
 for key in ('commons_metadata_query_failed','commons_credit_copy_failed_reason','ui_could_not_load_gallery_image'):
  section=re.search(r'^    resource [^\n]+ string/'+key+r'\n(.*?)(?=^    resource |\Z)',text,re.M|re.S);require(section is not None,'missing compiled resource '+key)
  matches=re.findall(r'^      \(ar\) (".*")$',section[1],re.M);require(len(matches)==1,'Arabic configuration mismatch '+key);values[key]=json.loads(matches[0])
 source_xml=(repo/'Paintroid/src/main/res/values-ar/strings.xml').read_bytes();src={n.get('name'):''.join(n.itertext()).replace("\\'", "'") for n in ET.fromstring(source_xml) if n.tag=='string'}
 require(all(values[k]==src[k] for k in values),'compiled Arabic resource/source mismatch')
 composed={r:values[k].replace('%1$s',values['commons_metadata_query_failed']) for r,k in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]};require(composed==BINDING['arabic_messages'],'compiled composed Arabic messages mismatch')
 common=dict(status='PASS',tree=TREE,head=HEAD,merge=MERGE,run_id=int(RUN),apk_sha256=info['apk_sha256'])
 payload=common|dict(official_artifact_sha256=sha(outer.read_bytes()),source_sha256=sha(raw),embedded_source_equals_delivered=True,tracked_source_files_compared=len(checked),excluded_tracked_files=omitted,native_extra_files=len(extra),limit='Tracked source bytes and embedded/delivered ZIP equality; native source extras restricted by directory. Native source provenance, signing/release and installed behavior are separate checks.')
 compiled=common|dict(aapt2_sha256=sha(aapt2.read_bytes()),dump_sha256=sha(dump),source_arabic_sha256=sha(source_xml),values=values,composed_route_text=composed,limit='Compiled source-equal Arabic strings and mechanical format composition only; no installed, rendering, helper or decoder acceptance claim.')
 return payload,compiled
if __name__=='__main__':
 p=argparse.ArgumentParser();[p.add_argument('--'+k,type=pathlib.Path,required=True) for k in ('repo','artifacts','aapt2','output')];a=p.parse_args();payload,compiled=audit(a.repo,a.artifacts,a.aapt2);a.output.mkdir(exist_ok=True)
 for n,d in [('payload-digest-result',payload),('delivery-compiled-arabic-input',compiled)]: (a.output/(n+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(payload,indent=2))
