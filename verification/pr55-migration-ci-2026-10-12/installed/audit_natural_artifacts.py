"""Exact migration source constants and direct resource lookup; no historical fixture dependency."""
import hashlib,subprocess,xml.etree.ElementTree as ET
TREE='592a60877524c5c118695cb45a4d0d5cd257b25a'
HEAD='43ab6622cdf6aac957a8d31cf2c5c20009e71d6e'
MERGE='e191c4660ef8709450df213cb75bd4bcf0810cb2'
RUN='38279470164'
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
