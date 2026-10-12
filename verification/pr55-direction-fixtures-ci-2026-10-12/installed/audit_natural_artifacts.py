"""One-time current-source review binding and direct resource lookup; no historical fixture dependency."""
import hashlib,subprocess,xml.etree.ElementTree as ET
import json,pathlib
BINDING=json.loads((pathlib.Path(__file__).resolve().parent/'binding.json').read_bytes())
TREE=BINDING['tree'];HEAD=BINDING['head'];BASE=BINDING['base'];MERGE=BINDING['merge'];RUN=str(BINDING['run_id'])
SOURCE_SHA=BINDING['source_digests']['app'];LIBRARY_SHA=BINDING['source_digests']['library']
def require(v,message):
 if not v:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def read_source(repo,path):return subprocess.check_output(['git','show',TREE+':'+path],cwd=repo)
def messages(repo):
 def values(path):return {n.get('name'):''.join(n.itertext()) for n in ET.fromstring(read_source(repo,path)) if n.tag=='string'}
 d=values('Paintroid/src/main/res/values/strings.xml')|values('Paintroid/src/main/res/values-ar/strings.xml')
 out={}
 for route,key in [('copy','commons_credit_copy_failed_reason'),('insert','ui_could_not_load_gallery_image')]:
  raw=d[key].replace('%1$s',d['commons_metadata_query_failed']).replace("\\'", "'")
  require('\\' not in raw and '"' not in raw,'unsupported Android resource quotation')
  out[('ar',route)]=raw
 return out
