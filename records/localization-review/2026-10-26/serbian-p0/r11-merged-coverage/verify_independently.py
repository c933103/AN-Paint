#!/usr/bin/env python3
"""DOM-based independent171-option counts, not a second call to primary parser."""
import argparse,hashlib,json,xml.dom.minidom as D
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def catalogue(p):
 raw=p.read_bytes();need(b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper(),'entity boundary');r=D.parseString(raw).documentElement;containers=set();leaves={};names=set()
 for n in r.childNodes:
  if n.nodeType!=n.ELEMENT_NODE:continue
  name=n.getAttribute('name');need(name not in names,'duplicate');names.add(name)
  if n.getAttribute('translatable')=='false':continue
  ident=n.tagName+'/'+name;containers.add(ident)
  def text(node):return ''.join(c.data if c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE) else text(c) if c.nodeType==c.ELEMENT_NODE else '' for c in node.childNodes)
  if n.tagName=='string':leaves[ident]=text(n)
  else:
   for i,c in enumerate(x for x in n.childNodes if x.nodeType==x.ELEMENT_NODE):leaves[ident+'['+(c.getAttribute('quantity') if n.tagName=='plurals' else str(i))+']']=text(c)
 return containers,leaves

def run(a):
 rows=json.loads((a.outputs/'structural-per-locale.json').read_text());base,leaves=catalogue(a.source_root/'Paintroid/src/main/res/values/strings.xml');tier={x['id']:set(x['keys']) for x in json.loads((a.source_root/'translations/string-importance.json').read_text())['tiers']};need(len(rows)==len({r['tag'] for r in rows})==171,'171 grain');totals={k:0 for k in rows[0] if k not in ('order','tag','path','blob')}
 for r in rows:
  p=a.source_root/r['path'];c,ll=catalogue(p);metrics={}
  for t,keys in {**tier,'all':base}.items():metrics[t+'_present']=len(keys&c);metrics[t+'_missing']=len(keys-c)
  overlap=leaves.keys()&ll.keys();metrics.update(leaves_present=len(overlap),leaves_missing=len(leaves.keys()-ll.keys()),leaves_english_identical=sum(ll[k]==leaves[k] for k in overlap),leaves_source_different=sum(ll[k]!=leaves[k] for k in overlap));need(all(r[k]==v for k,v in metrics.items()),'independent row '+r['tag']);raw=p.read_bytes();need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==r['blob'],'row blob')
  for k,v in metrics.items():totals[k]+=v
 delta=json.loads((a.outputs/'coverage-delta.json').read_text());need(totals==delta['presence_totals'],'independent totals')
 if a.mode=='preview':need(delta['current_production_replaced'] is False and delta['actual_postmerge_status'].startswith('not supplied'),'preview cannot claim integration')
 else:
  need(a.expected_merge and a.expected_run,'explicit actual merge/run required')
  terminal=json.loads((a.outputs/'terminal-status-supplement.json').read_text())
  need(delta['source_commit']==a.expected_merge==terminal['actual_merge'] and terminal['actual_push_run']['id']==a.expected_run,'actual output identity')
  need(delta['current_production_replaced'] is True and delta['actual_postmerge_status']=='success; fresh actual push artifacts, not PR artifacts' and terminal['all_six_checks_successful'] is True,'actual output qualification')
 out={'options':171,'independent_DOM_rows_match':True,'totals_match':True,'preview_not_postmerge':a.mode=='preview','mode':a.mode,'new_native_human_acceptance':0};print(json.dumps(out,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--outputs',type=Path,required=True);p.add_argument('--mode',choices=['preview','actual-postmerge'],default='preview');p.add_argument('--expected-merge');p.add_argument('--expected-run',type=int);run(p.parse_args())
