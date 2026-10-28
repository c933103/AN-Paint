"""Complete bounded KO-KP/en-AU resource contracts; no whole-source snapshots."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
from collections import Counter
import translation_catalogues as catalogues
FIXTURE=Path(__file__).resolve().parent/'fixtures/current_localization/north_korean_australian_priority_wording.json'
RAW_SHA256='94413c7d1952acdea6cbb26726ca845c16940d22d860fac14edab700bf1ca951'
def _unique(pairs):
 out={}
 for k,v in pairs:
  if k in out:raise ValueError('Duplicate JSON key')
  out[k]=v
 return out
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def _disk():
 raw=FIXTURE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=RAW_SHA256:raise ValueError('Reviewed fixture bytes differ')
 return json.loads(raw,object_pairs_hook=_unique)
_REFERENCE=_disk()
_CANONICAL_SHA256=hashlib.sha256(canonical(_REFERENCE)).hexdigest()
def bind_fixture(data=None):
 actual=_disk()if data is None else data
 try:same=hashlib.sha256(canonical(actual)).hexdigest()==_CANONICAL_SHA256
 except (ValueError,TypeError):same=False
 if not same:raise ValueError('Complete supplied fixture differs')
 return actual
# Immutable signatures bind standalone whole-value validation, not just suite setup.
_ROWS=frozenset((tag,ident,hashlib.sha256(canonical([_REFERENCE['sources'][ident],row])).hexdigest())for tag,loc in _REFERENCE['locales'].items()for ident,row in loc['accepted'].items())
del _REFERENCE
def require_complete(tag,ident,source,target):
 try:sig=hashlib.sha256(canonical([source,target])).hexdigest()
 except (ValueError,TypeError):raise ValueError('Invalid complete row')
 if (tag,ident,sig)not in _ROWS:raise ValueError('Unreviewed complete row')
 pairs=[(source['value'],target['value'])]if isinstance(target['value'],str)else[(source['value'].get(q,source['value']['other']),v)for q,v in target['value'].items()]
 for english,value in pairs:
  if catalogues.placeholders(value)!=catalogues.placeholders(english):raise ValueError('Complete format arguments differ')
  if catalogues.android_string_errors(value)+catalogues.format_string_errors(value,target['attributes'].get('formatted')!='false'):raise ValueError('Invalid Android raw grammar')
 return target

def require_resource(root,ident,row):
 typ,key=ident.split('/')
 nodes=[n for n in root if n.get('name')==key]
 if len(nodes)!=1:raise ValueError('Missing/duplicate/wrong-type resource')
 n=nodes[0]
 if n.tag!=typ or n.attrib!=row['attributes']or(n.tail or '').strip():raise ValueError('Resource type/attributes/tail differ')
 if typ=='string':
  if len(n)or n.text!=row['value']:raise ValueError('Complete string or markup differs')
 elif typ=='plurals':
  if(n.text or '').strip()or len(n)!=len(row['value']):raise ValueError('Plural shape differs')
  found={}
  for child in n:
   q=child.get('quantity')
   if child.tag!='item'or q in found or q not in row['value']or len(child)or(child.tail or '').strip()or child.attrib!=row['child_attributes'][q]:raise ValueError('Plural child differs')
   found[q]=child.text
  if found!=row['value']:raise ValueError('Complete plural differs')
 else:raise ValueError('Unsupported reviewed resource')
 return n

def validate_catalogue(tag,source_xml,target_xml,data=None):
 d=bind_fixture(data);loc=d['locales'][tag];source=ET.fromstring(source_xml);target=ET.fromstring(target_xml)
 for root in (source,target):
  if root.tag!='resources'or root.attrib or(root.text or '').strip()or(root.tail or '').strip():raise ValueError('Resources root differs')
  names=[n.get('name')for n in root]
  if len(names)!=len(set(names)):raise ValueError('Duplicate resource identity')
 for ident,row in loc['accepted'].items():
  require_resource(source,ident,d['sources'][ident]);require_complete(tag,ident,d['sources'][ident],row);require_resource(target,ident,row)
 for ident,row in loc['held'].items():require_resource(target,ident,row)
 return {'accepted':len(loc['accepted']),'existing_holds':len(loc['held'])}

# The original thirty-row fixture remains byte-for-byte historical. Only three
# complete North Korean metadata warnings have independently reviewed successors.
_KP_CREDIT_KEYS=frozenset(('gallery_credit_could_not_save','gallery_credit_too_large','legacy_credits_unreadable'))
_KP_HISTORY_ENTRIES_SHA256='03298cb10ef5bd0fe37d84e402fafa0c5ac26537e1efc0b6e10a0004b6f861cf'
def current_kp_attribution_entries(entries):
 try:actual=hashlib.sha256(canonical(entries)).hexdigest()
 except (TypeError,ValueError):raise ValueError('Invalid historical attribution rows')
 if actual!=_KP_HISTORY_ENTRIES_SHA256:raise ValueError('Historical attribution rows differ')
 current=bind_fixture();out=[]
 for original in entries:
  row=dict(original)
  if row['directory']=='values-b+ko+KP'and row['key']in _KP_CREDIT_KEYS:
   ident='string/'+row['key'];accepted=current['locales']['ko-KP']['accepted'][ident]
   require_complete('ko-KP',ident,current['sources'][ident],accepted)
   row['value']=accepted['value'];row['attributes']=dict(accepted['attributes'])
  out.append(row)
 return out
