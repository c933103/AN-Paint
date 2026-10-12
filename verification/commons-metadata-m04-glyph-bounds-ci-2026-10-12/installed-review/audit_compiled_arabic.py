#!/usr/bin/env python3
"""Compare actual compiled Arabic route strings with the forensic image records."""
import argparse,pathlib,subprocess,re,json,hashlib
from forensic_installed_ink import require,sha

def main():
 p=argparse.ArgumentParser()
 for k in ('apk','aapt2','records','output'):p.add_argument('--'+k,type=pathlib.Path,required=True)
 a=p.parse_args();require(sha(a.aapt2.read_bytes())=='d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de','tool changed')
 require(sha(a.apk.read_bytes())=='b1528f3f58c5f5412b177a881686af6b2aa99b2b0a7ddeeeb094a329f1f99820','source-bound APK changed')
 raw=subprocess.check_output([str(a.aapt2),'dump','resources',str(a.apk)]);s=raw.decode();values={};blocks=[]
 for key in ('commons_metadata_query_failed','commons_credit_copy_failed_reason','ui_could_not_load_gallery_image'):
  block=re.findall(r'^    resource (0x[0-9a-f]+) string/'+key+r'\n(.*?)(?=^    resource |\Z)',s,re.S|re.M);require(len(block)==1,'resource absent');rid,b=block[0]
  line=re.findall(r'^      \(ar\) (".*")$',b,re.M);require(len(line)==1,'Arabic absent');values[key]=json.loads(line[0]);blocks.append('resource '+rid+' string/'+key+'\n      (ar) '+line[0])
 for route,key in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]:
  d=json.loads((a.records/(route+'.json')).read_bytes());require(values[key].replace('%1$s',values['commons_metadata_query_failed'])==d['message'],'compiled Arabic differs')
 (a.output.parent/'compiled-arabic-routes.txt').write_text('\n'.join(blocks)+'\n')
 a.output.write_text(json.dumps({'status':'PASS','scope':'Exact installed-record text matches Arabic strings from the independently source-bound APK; not a rendering pass','apk_sha256':sha(a.apk.read_bytes()),'aapt2_sha256':sha(a.aapt2.read_bytes()),'dump_sha256':sha(raw),'values':values},ensure_ascii=False,indent=2)+'\n');print('PASS compiled Arabic route strings match both failed image records')
if __name__=='__main__':main()
