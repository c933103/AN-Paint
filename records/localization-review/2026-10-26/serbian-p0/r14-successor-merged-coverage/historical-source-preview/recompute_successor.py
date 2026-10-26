#!/usr/bin/env python3
"""PR182 bounded source reconciliation; does not infer actual-postmerge execution."""
from coverage_common import *
import csv
BASE='3160b02e939cd732536f4f3c896e082b19325eee'; BASE_TREE='385bd19a6cd68c7b8ce9644f157e4acb4e4cf93e'
HEAD='a17194b2402fbcea85ee526964b4adc497295ebf'; MERGE='0ebd41d4d9b665213c776f5a0479a29ecabdd243'; TREE='bc5e10affc54ba2e0788c749b4b78968379596ba'
BASE_MANIFEST='7eaeba5758fe3e19469fd2e9db2977ed35ff9a2c0e0dd3c8c07deadf8e892da1'; REVIEW='a2e91394fd6fcbbeaefafe4ee879df23fd4791a33dba565b0a31bfbc2f78b164'
PAIR={'string/save20_file_format','string/ui_autosave_is_paused_to_protect_that_draft_use'}
CHANGED={'Paintroid/src/main/res/values-b+sr+Cyrl/strings.xml','Paintroid/src/test/java/org/catrobat/paintroid/local/ProtectedDraftWarningTest.kt','Paintroid/src/test/java/org/catrobat/paintroid/local/SerbianP0WordingTest.kt','tools/fixtures/current_localization/serbian_p0_wording.json','tools/test_serbian_p0_wording.py'}
def safe(root,path):
 p=Path(path); require(not p.is_absolute() and '..' not in p.parts and '\\' not in path,'unsafe path');q=root/p;require(q.resolve().is_relative_to(root.resolve()),'escaped path');return q

def compute(inputs,source,baseline):
 br=inputs/'baseline';require(sha((br/'manifest.json').read_bytes())==BASE_MANIFEST,'immutable immediate R11 baseline');manifest=read(br/'manifest.json');require(manifest['source_commit']==BASE and manifest['source_tree']==BASE_TREE,'baseline actual source');entries={e['path']:e for e in manifest['files']}
 for p in br.glob('*.json'):
  if p.name=='manifest.json':continue
  e=entries['ordinary/'+p.name];b=p.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'] and git(b)==e['git_blob_sha1'],'baseline output hash')
 trees=[verify_tree(read(inputs/name),expected) for name,expected in [('base-source-tree.json',BASE_TREE),('source-head-tree.json',TREE)]];old,new=trees;require(len(old)==len(new)==1385 and old.keys()==new.keys(),'same source inventory')
 raw=[]
 for root,tree in [(baseline,old),(source,new)]:
  data={}
  for path,e in tree.items():
   p=safe(root,path);b=p.read_bytes();require(git(b)==e['sha'],'source bytes '+path);require(('100755' if p.stat().st_mode&0o111 else '100644')==e['mode'],'source mode '+path);data[path]=b
  raw.append(data)
 before,after=raw;changed={p for p in new if (new[p]['sha'],new[p]['mode'])!=(old[p]['sha'],old[p]['mode'])};require(changed==CHANGED,'exact five-file source delta')
 merge=read(inputs/'actual-merge-readback.json');require((merge['sha'],merge['tree'],merge['ordered_parents'])==(MERGE,TREE,[BASE,HEAD]),'actual merge binding')
 review=read(inputs/'review/review.json');require(sha((inputs/'review/review.json').read_bytes())==REVIEW,'accepted pair review pin');require(review['overall_decision']=='accept' and review['atomic_pair_required'] is True,'atomic accepted pair')
 for n,k in [('context.json','context_sha256'),('candidates.json','candidate_sha256')]:require(sha((inputs/'review'/n).read_bytes())==review[k],'linguistic context binding')
 accepted={e['identity']:e for e in review['entries']};require(set(accepted)==PAIR and all(e['decision']=='accept' for e in accepted.values()),'two accepted identities')
 rows0=read(br/'structural-per-locale.json');require(len(rows0)==171 and len({r['tag'] for r in rows0})==171,'171 baseline grain')
 canonical,english,_=parse(after['Paintroid/src/main/res/values/strings.xml']);tiers={x['id']:set(x['keys']) for x in json.loads(after['translations/string-importance.json'])['tiers']};tags=[n.text for n in ET.fromstring(after['Paintroid/src/main/res/values/app_language_tags.xml']).findall('./string-array/item')];require(tags==[r['tag'] for r in rows0],'picker grain/order')
 rows=[];pair=[]
 for prior in rows0:
  path=prior['path'];containers,leaves,nodes=parse(after[path]);oc,ol,on=parse(before[path]);require(nodes.keys()==on.keys(),'no structural additions/removals');changes={k for k in nodes if fingerprint(nodes[k])!=fingerprint(on[k])};require(changes==(PAIR if prior['tag']=='sr-Cyrl' else set()),'bounded wording-only correction')
  r={k:prior[k] for k in ('order','tag','path')};r['blob']=new[path]['sha']
  for t,keys in {**tiers,'all':set(canonical)}.items():r[t+'_present']=len(keys&containers.keys());r[t+'_missing']=len(keys-containers.keys())
  overlap=english.keys()&leaves.keys();r.update(leaves_present=len(overlap),leaves_missing=len(english.keys()-leaves.keys()),leaves_english_identical=sum(leaves[k]==english[k] for k in overlap),leaves_source_different=sum(leaves[k]!=english[k] for k in overlap));require(all(r[k]==prior[k] for k in r if k!='blob'),'all171 presence metrics unchanged');rows.append(r)
  for k in sorted(changes):
   a=accepted[k];n=nodes[k];require(n.text==a['accepted_xml_text'] and n.attrib==a['accepted_attributes'] and on[k].text==a['original_xml_text'],'reviewed current/baseline pair');pair.append({'locale':'sr-Cyrl','identity':k,'source':canonical[k],'before':on[k].text,'after':n.text,'attributes':n.attrib,'review_sha256':REVIEW,'decision':'accept','qualification':'Independent AI full-value/source-context review; not native-human/device/layout/whole-language certification'})
 metrics=[k for k in rows[0] if k not in ('order','tag','path','blob')];totals={k:sum(r[k] for r in rows) for k in metrics};require(totals==read(br/'coverage-delta.json')['presence_totals'],'all global metrics unchanged')
 prior=read(br/'review-scope-reconciliation.json');prior_scopes=prior['new_review_scopes'];require(len(prior_scopes)==148 and prior['prior_values_preserved']=={'sr-Cyrl':170,'sr-Latn':168},'historical148/338 retained')
 current=[]
 for e in prior_scopes:
  path=f"Paintroid/src/main/res/values-b+{e['locale'].replace('-', '+')}/strings.xml";_,_,nodes=parse(after[path]);n=nodes[e['identity']]
  if e['locale']=='sr-Cyrl' and e['identity'] in PAIR:continue
  require(n.text==e['xml_text'] and n.attrib==e['attributes'],'147 unchanged previously reviewed values');current.append(e)
 require(len(current)==147,'current unchanged147')
 for e in pair:current.append({'locale':e['locale'],'identity':e['identity'],'xml_text':e['after'],'attributes':e['attributes'],'review_receipt_sha256':REVIEW,'decision':'accept','qualification':e['qualification']})
 require(len(current)==len({(e['locale'],e['identity']) for e in current})==149,'current unique149')
 require(sum(r['all_present'] for r in rows if r['tag'] in ('sr-Cyrl','sr-Latn'))==486 and 486-len(current)==337,'current reviewed/preserved partition')
 out={'structural-per-locale.json':rows,'coverage-delta.json':{'source_commit':MERGE,'source_tree':TREE,'source_status':'Actual merged source recomputed; actual-postmerge execution evidence pending','baseline_commit':BASE,'baseline_tree':BASE_TREE,'baseline_manifest_sha256':BASE_MANIFEST,'options':171,'presence_totals':totals,'presence_delta':{k:0 for k in metrics},'new_structural_values':0,'wording_values_corrected':2,'current_serbian_unique_reviewed_values':149,'current_serbian_preserved_inherited_values':337,'historical_PR180_new_reviewed_values':148,'historical_PR180_preserved_inherited_values':338,'current_production_replaced':False,'actual_postmerge_status':'not supplied; source-only reconciliation, no terminal runtime claim','global_linguistic_accepted_count':None,'new_native_human_whole_language_layout_or_release_certifications':0},'review-scope-reconciliation.json':{'source_commit':MERGE,'source_tree':TREE,'atomic_corrected_pair':sorted(pair,key=lambda e:e['identity']),'current_serbian_review_scopes':current,'unchanged_prior_reviewed_values':147,'current_unique_reviewed_values':149,'preserved_inherited_values':337,'current_total_serbian_values':486,'historical_baseline_new_review_scopes':prior_scopes,'historical_baseline_preserved_inherited_values':338,'inherited_Cyrillic_label_defect_corrected_in_this_successor':True,'other169_rows_unchanged':True,'holds_and_all_frozen_prior_categories_preserved':True,'prior_categories':prior['prior_categories'],'prior_global_scope':{'scoped':59,'outside':112},'new_linguistic_acceptances_due_to_CI':0,'newly_reviewed_unique_identity_count':1,'previously_reviewed_identity_reworded_count':1,'independent_pair_review_count':2,'global_linguistic_accepted_count':None},'full-source-delta.json':{'source_commit':MERGE,'source_tree':TREE,'base':BASE,'base_tree':BASE_TREE,'files':[{'path':p,'before':old[p]['sha'],'after':new[p]['sha'],'mode':new[p]['mode']} for p in sorted(changed)]}}
 return out

def main():
 p=argparse.ArgumentParser()
 for n in ('inputs','source-root','baseline-source-root','out'):p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();out=compute(a.inputs,a.source_root,a.baseline_source_root);a.out.mkdir(parents=True,exist_ok=True)
 for n,d in out.items():emit(a.out,n,d)
 with (a.out/'structural-per-locale.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(out['structural-per-locale.json'][0]));w.writeheader();w.writerows(out['structural-per-locale.json'])
 print(json.dumps({'source_commit':MERGE,'options':171,'all_presence_metrics_unchanged':True,'reviewed149_preserved337':True,'actual_postmerge_execution':'pending'},indent=2))
if __name__=='__main__':main()
