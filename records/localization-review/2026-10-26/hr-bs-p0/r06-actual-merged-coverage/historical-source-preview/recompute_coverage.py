#!/usr/bin/env python3
"""PR183 exact-source 171-option preview; no actual merge/runtime inference."""
from coverage_common import *
import csv
BASE='0ebd41d4d9b665213c776f5a0479a29ecabdd243';BASE_TREE='bc5e10affc54ba2e0788c749b4b78968379596ba'
HEAD='b97ba1e0b4abe31f9758242a82e8ff58f356ffe4';TREE='d41defc26ef6870aa35393c2f3fb909c5e803747'
BASE_MANIFEST='74c64ac05dba3f76ff4235169ee3a2adf1611415a5131d24b20d3a74db421e87';APPROVED='9c63fdda5531fe5d00ae0cb7dd876786c6a00dce8515cc7861311e3f54e5fdfb'
LOCALES=('hr','bs');HOLDS={'string/'+k for k in ('formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png')}
def safe(root,path):
 p=Path(path);require(not p.is_absolute() and '..' not in p.parts and '\\' not in path,'unsafe path');q=root/p;require(q.resolve().is_relative_to(root.resolve()),'escaped path');return q

def compute(inputs,source,baseline):
 br=inputs/'baseline';require(sha((br/'manifest.json').read_bytes())==BASE_MANIFEST,'R14 immutable baseline pin');m=read(br/'manifest.json');require((m['source_commit'],m['source_tree'])==(BASE,BASE_TREE),'actual immediate baseline');mi={e['path']:e for e in m['files']}
 for p in br.glob('*.json'):
  if p.name=='manifest.json':continue
  b=p.read_bytes();e=mi['ordinary/'+p.name];require(len(b)==e['bytes'] and sha(b)==e['sha256'] and git(b)==e['git_blob_sha1'],'baseline selected output hash')
 require(sha((inputs/'approved-manifest.json').read_bytes())==APPROVED,'accepted values pin');a=read(inputs/'approved-manifest.json');require((a['source_commit'],a['source_tree'],a['preserved_values'])==(BASE,BASE_TREE,215),'approval source and preserved scope')
 for filename,key in [('shared-source-context.json','scope_context_sha256'),('terminology-foundations.json','terminology_sha256')]:require(sha((inputs/'review'/filename).read_bytes())==a[key],'accepted context binding')
 old=verify_tree(read(inputs/'base-tree.json'),BASE_TREE);new=verify_tree(read(inputs/'source-head-tree.json'),TREE);require(len(old)==1385 and len(new)==1388 and len(new.keys()-old.keys())==3 and not old.keys()-new.keys(),'full inventory grain')
 raw=[]
 for root,tree in [(baseline,old),(source,new)]:
  d={}
  for path,e in tree.items():
   p=safe(root,path);b=p.read_bytes();require(git(b)==e['sha'],'source byte binding '+path);require(('100755' if p.stat().st_mode&0o111 else '100644')==e['mode'],'source mode binding '+path);d[path]=b
  raw.append(d)
 before,after=raw;changed={p for p in new if p not in old or (old[p]['sha'],old[p]['mode'])!=(new[p]['sha'],new[p]['mode'])};expected=read(inputs/'source-changed-files.json');require(len(changed)==18 and changed=={e['path'] for e in expected},'exact18-file delta');require({p for p in changed if '/src/main/' in p}=={f'Paintroid/src/main/res/values-{t}/strings.xml' for t in LOCALES},'only HR/BS production changes')
 for e in expected:require(new[e['path']]['sha']==e['sha'] and old.get(e['path'],{}).get('sha')==e.get('old_sha'),'declared exact source delta')
 canonical,english,_=parse(after['Paintroid/src/main/res/values/strings.xml']);require(len(canonical)==717 and len(english)==718,'English denominator');tiers={t['id']:set(t['keys']) for t in json.loads(after['translations/string-importance.json'])['tiers']};require({t:len(k) for t,k in tiers.items()}=={'P0':92,'P1':249,'P2':305,'P3':71},'tier denominator');prior=read(br/'structural-per-locale.json');tags=[n.text for n in ET.fromstring(after['Paintroid/src/main/res/values/app_language_tags.xml']).findall('./string-array/item')];require(len(prior)==len(set(tags))==171 and tags==[r['tag'] for r in prior],'171 picker grain/order')
 reviews={}
 for t in LOCALES:
  p=inputs/'review'/f'{t}-review.json';r=read(p);require(sha(p.read_bytes())==a['review_bindings'][t]['review_sha256'],'review hash');require((r['source_commit'],r['source_tree'],r['locale'])==(BASE,BASE_TREE,t),'review source locale');reviews[t]={e['identity']:e for e in r['entries']};require(len(reviews[t])==len(r['entries'])==78,'review grain')
 rows=[];scopes=[];decisions=collections.Counter()
 for prev in prior:
  t=prev['tag'];path=prev['path'];co,ll,nodes=parse(after[path]);oc,ol,on=parse(before[path]);r={k:prev[k] for k in ('order','tag','path')};r['blob']=new[path]['sha'];require(old[path]['sha']==prev['blob'],'baseline row blob')
  for tier,keys in {**tiers,'all':set(canonical)}.items():r[tier+'_present']=len(keys&co.keys());r[tier+'_missing']=len(keys-co.keys())
  overlap=english.keys()&ll.keys();r.update(leaves_present=len(overlap),leaves_missing=len(english.keys()-ll.keys()),leaves_english_identical=sum(ll[k]==english[k] for k in overlap),leaves_source_different=sum(ll[k]!=english[k] for k in overlap))
  if t not in LOCALES:require(r==prev,'other169 rows unchanged')
  else:
   selected={'string/'+k for k in a['approved_values'][t]};require(len(selected)==78 and set(nodes)-set(on)==selected and not set(on)-set(nodes),'missing-only78');require(len(on)=={'hr':98,'bs':117}[t] and len(nodes)=={'hr':176,'bs':195}[t] and all(fingerprint(nodes[k])==fingerprint(n) for k,n in on.items()),'all215 existing values/attributes preserved');holds=HOLDS|({'string/save20_title'} if t=='hr' else set());require(tiers['P0']-nodes.keys()==holds,'protected holds');require('string/ui_no_resize_fits_decoder_memory' not in nodes,'held P1 companion absent')
   for key,e in a['approved_values'][t].items():
    ident='string/'+key;v=reviews[t][ident];n=nodes[ident];require(n.text==e['accepted_xml_text']==v['accepted_xml_text'] and n.attrib==e['attributes']==v['attributes'],'exact accepted value attributes');require(sha(n.text.encode())==e['sha256']==v['accepted_value_sha256_utf8'] and sha(canonical[ident].encode())==v['source_value_sha256_utf8'],'accepted/source hashes');require(tokens(n.text)==tokens(canonical[ident]),'source token equivalence');require(e['decision']==v['decision'] and v['decision'] in ('accept','revise'),'review decision');decisions[v['decision']]+=1;scopes.append({'locale':t,'identity':ident,'source':canonical[ident],'xml_text':n.text,'attributes':n.attrib,'xml_text_sha256':e['sha256'],'decision':v['decision'],'review_sha256':a['review_bindings'][t]['review_sha256'],'qualifications':v['qualifications'],'acceptance':'Independent AI complete-value/source-static scope only'})
  rows.append(r)
 metrics=[k for k in rows[0] if k not in ('order','tag','path','blob')];totals={k:sum(r[k] for r in rows) for k in metrics};previous={k:sum(r[k] for r in prior) for k in metrics};require(previous==read(br/'coverage-delta.json')['presence_totals'],'baseline totals');delta={k:totals[k]-previous[k] for k in metrics};require({k:v for k,v in delta.items() if v}=={'P0_present':156,'P0_missing':-156,'all_present':156,'all_missing':-156,'leaves_present':156,'leaves_missing':-156,'leaves_source_different':156},'exact156 presence delta');require(len(scopes)==156 and decisions=={'accept':155,'revise':1},'bounded accepted/revised scope')
 ledger=read(br/'review-scope-reconciliation.json');serbian=ledger['current_serbian_review_scopes'];require(len(serbian)==149 and ledger['preserved_inherited_values']==337,'prior Serbian current149/337')
 for e in serbian:
  _,_,nodes=parse(after[f"Paintroid/src/main/res/values-b+{e['locale'].replace('-', '+')}/strings.xml"]);n=nodes[e['identity']];require(n.text==e['xml_text'] and n.attrib==e['attributes'],'prior current Serbian review preserved')
 return {'structural-per-locale.json':rows,'coverage-delta.json':{'source_commit':HEAD,'source_tree':TREE,'source_status':'PR183 source preview; actual merge/postmerge unknown','baseline_commit':BASE,'baseline_tree':BASE_TREE,'baseline_manifest_sha256':BASE_MANIFEST,'options':171,'canonical_containers':717,'canonical_leaves':718,'presence_totals':totals,'presence_delta':delta,'changed_options':['hr','bs'],'unchanged_options':169,'locales_before':[r for r in prior if r['tag'] in LOCALES],'locales_after':[r for r in rows if r['tag'] in LOCALES],'new_reviewed_pairs':156,'preserved_HR_BS_values':215,'current_production_replaced':False,'actual_postmerge_status':'not supplied; actual merge and fresh push evidence required','global_linguistic_accepted_count':None,'global_scope':{'scoped':59,'outside':112,'unchanged':True},'new_native_human_whole_language_layout_or_release_certifications':0},'review-scope-reconciliation.json':{'source_commit':HEAD,'source_tree':TREE,'new_review_scopes':scopes,'new_scope_verdict_counts':dict(decisions),'prior_values_preserved':{'hr':98,'bs':117},'holds_each':sorted(HOLDS),'additional_HR_hold':'string/save20_title','P1_companion_absent':True,'current_prior_Serbian_review_scopes':serbian,'prior_Serbian_current_reviewed':149,'prior_Serbian_preserved':337,'prior_PR180_historical_reviewed':148,'prior_PR180_historical_preserved':338,'prior_categories':ledger['prior_categories'],'prior_global_scope':ledger['prior_global_scope'],'compiled_family_count_qualification':{'new_HR_BS':156,'prior_current_Serbian':149,'earlier_prior_families':548,'combined_bounded_compiled_reviewed':853,'not_global_linguistic_acceptance':True},'global_linguistic_accepted_count':None,'no_prior_category_recount_upgrade_revocation':True,'new_linguistic_acceptances_due_to_CI':0},'full-source-delta.json':{'source_commit':HEAD,'source_tree':TREE,'base':BASE,'base_tree':BASE_TREE,'files':[{'path':p,'before':old.get(p,{}).get('sha'),'after':new[p]['sha'],'mode':new[p]['mode']} for p in sorted(changed)]}}
def main():
 p=argparse.ArgumentParser()
 for n in ('inputs','source-root','baseline-source-root','out'):p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();out=compute(a.inputs,a.source_root,a.baseline_source_root);a.out.mkdir(parents=True,exist_ok=True)
 for n,d in out.items():emit(a.out,n,d)
 with (a.out/'structural-per-locale.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(out['structural-per-locale.json'][0]));w.writeheader();w.writerows(out['structural-per-locale.json'])
 print(json.dumps({'source_commit':HEAD,'options':171,'new_reviewed_values':156,'preserved_values':215,'presence_totals':out['coverage-delta.json']['presence_totals'],'actual_postmerge_claim':False},indent=2))
if __name__=='__main__':main()
