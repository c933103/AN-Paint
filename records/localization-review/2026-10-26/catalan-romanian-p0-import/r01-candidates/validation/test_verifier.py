#!/usr/bin/env python3
"""Refreshed-hash controls: actual packet mutations plus labelled synthetic formatted=false probes."""
import argparse,copy,hashlib,json,tempfile
from pathlib import Path
from xml.parsers.expat import ExpatError
from verify_candidates import validate,format_pair,PRODUCTS
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def need(x,msg):
 if not x:raise ValueError(msg)
def h(b):return hashlib.sha256(b).hexdigest()
base={f.name:f.read_bytes() for f in a.packet.glob('*.json')};controls=[];synthetic=[]
validate(a.source_root,a.packet)
def change(p,name,fn):
 d=json.loads((p/name).read_bytes());fn(d);(p/name).write_text(json.dumps(d,ensure_ascii=False))
def refresh_input(p,file,field):
 value=h((p/file).read_bytes())
 for tag in ('ca','ro'):change(p,tag+'-import-format-candidates.json',lambda d:d[field].__setitem__('sha256',value))
def run(label,fn,refresh_shared=False,refresh_terms=False):
 with tempfile.TemporaryDirectory() as td:
  target=Path(td)
  for n,b in base.items():(target/n).write_bytes(b)
  fn(target)
  if refresh_shared:refresh_input(target,'shared-source-context.json','shared_source_context')
  if refresh_terms:refresh_input(target,'terminology-foundations.json','existing_terminology')
  try:validate(a.source_root,target)
  except (ValueError,KeyError,TypeError,IndexError,OSError,ExpatError):controls.append({'case':label,'outcome':'rejected'});return
  raise ValueError('Incorrectly accepted negative control: '+label)
def edit_text(x,v):x.update(candidate_display_text=v,candidate_value_sha256_utf8=h(v.encode()),candidate_xml_text='"'+v+'"',candidate_xml_text_sha256_utf8=h(('"'+v+'"').encode()))
suffixes=[' %s',' %d',' %.2f',' %1$s',' %%',' %n',' %',' %q',' %1$',' %.',' %3$.',' %3$.f',' %t']
for tag in ('ca','ro'):
 n=tag+'-import-format-candidates.json'
 for suffix in suffixes:
  def mutate(p,n=n,suffix=suffix):
   def edit(d):
    x=next(x for x in d['candidates'] if x['identity']=='string/formats22_ascii_description');edit_text(x,x['candidate_display_text']+suffix)
   change(p,n,edit)
  run(tag+' refreshed-hash format '+repr(suffix),mutate)
 run(tag+' missing candidate',lambda p,n=n:change(p,n,lambda d:d['candidates'].pop()))
 run(tag+' duplicate candidate',lambda p,n=n:change(p,n,lambda d:d['candidates'].__setitem__(1,copy.deepcopy(d['candidates'][0]))))
 run(tag+' wrong source pin',lambda p,n=n:change(p,n,lambda d:d.__setitem__('source_commit','0'*40)))
 run(tag+' altered attribute',lambda p,n=n:change(p,n,lambda d:d['candidates'][0]['attributes'].__setitem__('formatted','false')))
 run(tag+' falsely accepted proposal',lambda p,n=n:change(p,n,lambda d:d['candidates'][0].__setitem__('independent_review_status','accepted')))
 run(tag+' altered candidate priority',lambda p,n=n:change(p,n,lambda d:d['candidates'][0].__setitem__('priority','P3')))
 run(tag+' fabricated candidate context',lambda p,n=n:change(p,n,lambda d:d['candidates'][0].__setitem__('consumer_context_ids',['nonexistent-context'])))
 run(tag+' empty uncertainty',lambda p,n=n:change(p,n,lambda d:d['candidates'][0].__setitem__('author_uncertainties',[])))
 run(tag+' false missing-only claim',lambda p,n=n:change(p,n,lambda d:d['candidates'][0].__setitem__('current_target','existing')))
 run(tag+' unsafe referenced input',lambda p,n=n:change(p,n,lambda d:d['shared_source_context'].__setitem__('file','../shared-source-context.json')))
 run(tag+' malformed JSON',lambda p,n=n:(p/n).write_text('{not-json'))
 run(tag+' duplicate JSON key',lambda p,n=n:(p/n).write_bytes(b'{"locale":"duplicate",'+(p/n).read_bytes().lstrip()[1:]))
 run(tag+' missing file',lambda p,n=n:(p/n).unlink())
 for key,products in PRODUCTS.items():
  def remove_product(p,n=n,key=key,product=products[-1]):
   def edit(d):
    x=next(x for x in d['candidates'] if x['identity']=='string/'+key);edit_text(x,x['candidate_display_text'].replace(product,'X'))
   change(p,n,edit)
  run(tag+' altered product '+key,remove_product)
for tag in ('ca','ro'):
 n=tag+'-import-format-candidates.json'
 run(tag+' lost source semantic note',lambda p,n=n:change(p,n,lambda d:d['candidates'][0]['source_semantic_notes'].pop()))
 run(tag+' lost nonempty full-value qualification',lambda p,n=n:change(p,n,lambda d:d['candidates'][0]['author_semantic_qualifications'].pop(0)))
for suffix in suffixes:
 try:format_pair('Safe %1$s','Safe %1$s'+suffix,{'name':'synthetic','formatted':'false'})
 except ValueError:synthetic.append({'case':'synthetic formatted=false '+repr(suffix),'outcome':'rejected'});continue
 raise ValueError('formatted=false bypassed token inventory')
format_pair('Safe %1$s','Traduit %1$s',{'name':'synthetic','formatted':'false'})
def forge_context_chain(p):
 d=json.loads((p/'shared-source-context.json').read_bytes());identity=d['entries'][0]['identity'];d['entries'][0]['consumer_context_ids']=['nonexistent-context'];(p/'shared-source-context.json').write_text(json.dumps(d,ensure_ascii=False))
 for tag in ('ca','ro'):
  def edit(c):next(x for x in c['candidates'] if x['identity']==identity)['consumer_context_ids']=['nonexistent-context']
  change(p,tag+'-import-format-candidates.json',edit)
run('forged source and candidate context chain with refreshed hashes',forge_context_chain,True)
for label,field,value in [('wrong source context count','consumer_context_count',999),('missing source context IDs','consumer_context_ids',[])]:
 run(label,lambda p,field=field,value=value:change(p,'shared-source-context.json',lambda d:d['entries'][0].__setitem__(field,value)),True)
for label,field,value in [('consumer window','text','wrong'),('context key','key','string/ui_save'),('context path','path','translations/string-importance.json'),('context URL','url','https://github.com/c933103/AN-Paint/blob/wrong/file'),('context line','line',91),('context negative range','start_line',-1),('context bool line','line',True)]:
 run(label+' with refreshed hashes',lambda p,field=field,value=value:change(p,'shared-source-context.json',lambda d:d['entries'][0]['consumer_contexts'][0].__setitem__(field,value)),True)
def forge_context_id_consistently(p):
 def edit(d):
  e=d['entries'][0];e['consumer_contexts'][0]['id']='invented:92';e['consumer_context_ids']=['invented:92']
 change(p,'shared-source-context.json',edit)
 for tag in ('ca','ro'):change(p,tag+'-import-format-candidates.json',lambda d:d['candidates'][0].__setitem__('consumer_context_ids',['invented:92']))
run('context ID forged across source and candidates',forge_context_id_consistently,True)
run('corrupt source binding',lambda p:change(p,'shared-source-context.json',lambda d:d['source_bindings'][0].__setitem__('sha256','0'*64)),True)
run('substituted source binding membership',lambda p:change(p,'shared-source-context.json',lambda d:d['source_bindings'][0].__setitem__('path','AGENTS.md')),True)
run('duplicate source binding',lambda p:change(p,'shared-source-context.json',lambda d:d['source_bindings'].__setitem__(1,copy.deepcopy(d['source_bindings'][0]))),True)
run('corrupt inherited count',lambda p:change(p,'scope-and-holds.json',lambda d:d['locales']['ca'].__setitem__('P0_present',92)))
run('cleared holds',lambda p:change(p,'scope-and-holds.json',lambda d:d['locales']['ca'].__setitem__('held_missing_identities',[])))
run('lost inherited term',lambda p:change(p,'terminology-foundations.json',lambda d:d['locales']['ca']['preserved_values'].pop()),refresh_terms=True)
run('altered inherited value',lambda p:change(p,'terminology-foundations.json',lambda d:d['locales']['ro']['preserved_values'][0].__setitem__('xml_text','wrong')),refresh_terms=True)
run('removed paused scope',lambda p:change(p,'scope-and-holds.json',lambda d:d['paused_scopes'].pop()))
run('invented equality defect inference',lambda p:change(p,'scope-and-holds.json',lambda d:d.__setitem__('English_identical_implies_defect',True)))
run('forged source semantic qualification',lambda p:change(p,'shared-source-context.json',lambda d:d['entries'][0]['semantic_notes'].pop()),True)
run('unselected missingness silently held',lambda p:change(p,'scope-and-holds.json',lambda d:d['locales']['ca'].__setitem__('other_missing_outside_batch_detail',{'held':60,'unselected_nonheld':0})))
need(len(controls)==90 and len(synthetic)==13 and len({x['case'] for x in controls})==len(controls),'control inventory')
a.out.mkdir(parents=True,exist_ok=True);receipt={'schema_version':1,'positive_packet':'passed','negative_controls':controls,'negative_controls_rejected':len(controls),'synthetic_formatted_false_positive':'passed','synthetic_formatted_false_negative_controls':synthetic,'synthetic_formatted_false_negative_controls_rejected':len(synthetic),'total_rejected_controls':len(controls)+len(synthetic),'actual_selected_formatted_false_values':0,'source_mutations_performed':False,'limits':'Packet mutations and labelled synthetic format helper checks only; not linguistic or Android/runtime acceptance.'};(a.out/'mutation-controls.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Positive packet passed;',len(controls),'packet and',len(synthetic),'synthetic formatted=false negative controls rejected')
