#!/usr/bin/env python3
"""Explicit refreshed-hash negative controls; no linguistic or source judgment."""
import argparse,copy,hashlib,json,tempfile
from pathlib import Path
from verify_candidates import validate,tokens
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def need(x,msg):
 if not x:raise ValueError(msg)
def h(b):return hashlib.sha256(b).hexdigest()
base={f.name:f.read_bytes() for f in a.packet.glob('*.json')};controls=[]
validate(a.source_root,a.packet)
def run(label,fn,refresh_shared=False):
 with tempfile.TemporaryDirectory() as td:
  target=Path(td)
  for n,b in base.items():(target/n).write_bytes(b)
  fn(target)
  if refresh_shared:
   value=h((target/'shared-source-context.json').read_bytes())
   for tag in ('ca','ro'):
    n=tag+'-save-export-share-candidates.json';d=json.loads((target/n).read_bytes());d['shared_source_context']['sha256']=value;(target/n).write_text(json.dumps(d,ensure_ascii=False))
  try:validate(a.source_root,target)
  except (ValueError,KeyError,TypeError):controls.append({'case':label,'outcome':'rejected'});return
  raise ValueError('Incorrectly accepted negative control: '+label)
def change(p,name,fn):
 d=json.loads((p/name).read_bytes());fn(d);(p/name).write_text(json.dumps(d,ensure_ascii=False))
for tag in ('ca','ro'):
 n=tag+'-save-export-share-candidates.json'
 for suffix in [' %s',' %d',' %.2f',' %1$s',' %%',' %n',' %',' %q',' %1$',' %.',' %3$.',' %3$.f',' %t']:
  def mutate(p,n=n,suffix=suffix):
   def edit(d):
    x=next(x for x in d['candidates'] if x['identity']=='string/ui_share_explanation34');need(x['attributes']['formatted']=='false','wrong negative target');v=x['candidate_display_text']+suffix;x.update(candidate_display_text=v,candidate_value_sha256_utf8=h(v.encode()),candidate_xml_text='"'+v+'"',candidate_xml_text_sha256_utf8=h(('"'+v+'"').encode()))
   change(p,n,edit)
  run(tag+' formatted=false refreshed-hash '+repr(suffix),mutate)
 run(tag+' missing candidate',lambda p,n=n:change(p,n,lambda d:d['candidates'].pop()))
 run(tag+' duplicate candidate',lambda p,n=n:change(p,n,lambda d:d['candidates'].__setitem__(1,copy.deepcopy(d['candidates'][0]))))
 run(tag+' wrong source pin',lambda p,n=n:change(p,n,lambda d:d.__setitem__('source_commit','0'*40)))
 run(tag+' altered attribute',lambda p,n=n:change(p,n,lambda d:d['candidates'][0]['attributes'].__setitem__('formatted','false')))
 run(tag+' falsely accepted proposal',lambda p,n=n:change(p,n,lambda d:d['candidates'][0].__setitem__('independent_review_status','accepted')))
run('consumer window with refreshed input hashes',lambda p:change(p,'shared-source-context.json',lambda d:d['entries'][0]['consumer_contexts'][0].__setitem__('text','wrong')),True)
run('corrupt source binding',lambda p:change(p,'shared-source-context.json',lambda d:d['source_bindings'][0].__setitem__('sha256','0'*64)),True)
run('corrupt inherited count',lambda p:change(p,'scope-and-holds.json',lambda d:d['locales']['ca'].__setitem__('P0_present',92)))
need(len(controls)==39,'control inventory')
a.out.mkdir(parents=True,exist_ok=True);receipt={'schema_version':1,'positive_packet':'passed','negative_controls':controls,'negative_controls_rejected':len(controls),'source_mutations_performed':False,'limits':'Synthetic packet validation only; not linguistic or runtime acceptance.'};(a.out/'mutation-controls.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Positive packet passed;',len(controls),'negative controls rejected')
