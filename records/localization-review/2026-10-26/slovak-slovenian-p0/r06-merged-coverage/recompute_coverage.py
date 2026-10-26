#!/usr/bin/env python3
"""PR179 source preview and explicit later actual-postmerge evidence join; no inferred success."""
from coverage_common import *
import stat
BASE='e5f2d4e2d07e678076f022aa7b3ef923e13c3721';BASE_TREE='806d9577409c4044212d1c12e6e38da46417bae6'
HEAD='0824180c14ae979dc253f03d0fe628fbe9cf9b34';TREE='98b89d126533df3c0dbaeb729c74e4bcb44a3a8a'
APPROVED='5bf7ef0107eaa48f46ecfbf265afa5cd06a1680414b28c876dcd0f391a3f6bd0';BASE_MANIFEST='5e5d841b161021f3f7247a0f36348ae6ff9919105cf1fd793811518bb146aad4'
CANONICAL='Paintroid/src/main/res/values/strings.xml';TAGS='Paintroid/src/main/res/values/app_language_tags.xml';IMPORTANCE='translations/string-importance.json'
LOCALES=('sk','sl');HOLDS={'string/'+k for k in ('formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png')}
FORMAT_TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')
CHECKS={'Emulator API 35','Core emulator API 35','Position dialog API 35','Regression tests and lint','Build APK and corresponding source','Exact-script resource generation'}

def safe(root,name):
 p=Path(name);require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,'unsafe path');out=root/p;require(out.resolve().is_relative_to(root.resolve()),'escaped path');return out

def baseline(inputs):
 root=inputs/'baseline';require(sha((root/'manifest.json').read_bytes())==BASE_MANIFEST,'baseline immutable manifest');m=read(root/'manifest.json');require(m['source_commit']==BASE and m['source_tree']==BASE_TREE,'baseline source identity');entries={x['path']:x for x in m['files']};require(len(entries)==len(m['files'])==201,'baseline manifest grain')
 for p in root.iterdir():
  if p.name=='manifest.json':continue
  b=p.read_bytes();e=entries[p.name];require(len(b)==e['bytes'] and sha(b)==e['sha256'] and git(b)==e['git_blob_sha1'],'baseline selected payload hash')
 return {p.stem:read(p) for p in root.iterdir() if p.suffix=='.json'}

def source_snapshot(inputs,source,oldsource):
 head=verify_tree(read(inputs/'source-head-tree.json'),TREE);old=verify_tree(read(inputs/'base-source-tree.json'),BASE_TREE);require(len(head)==1382 and len(old)==1379,'full source counts');raw={};oldraw={}
 for root,tree,out in [(source,head,raw),(oldsource,old,oldraw)]:
  for path,e in tree.items():
   p=safe(root,path);b=p.read_bytes();require(git(b)==e['sha'],'raw Git source '+path);require(('100755' if p.stat().st_mode&0o111 else '100644')==e['mode'],'source mode '+path);out[path]=b
 changes=[{'path':p,'before':old.get(p,{}).get('sha'),'after':head.get(p,{}).get('sha'),'mode':head.get(p,old.get(p))['mode']} for p in sorted(head.keys()|old.keys()) if head.get(p,{}).get('sha')!=old.get(p,{}).get('sha')]
 require(len(changes)==15 and len(set(head)-set(old))==3 and not set(old)-set(head),'full bounded source delta')
 production={e['path'] for e in changes if '/src/main/' in e['path']};require(production=={f'Paintroid/src/main/res/values-{t}/strings.xml' for t in LOCALES},'production boundary')
 return head,old,raw,oldraw,changes

def compute(inputs,source,oldsource):
 require(sha((inputs/'approved-manifest.json').read_bytes())==APPROVED,'approved immutable identity');a=read(inputs/'approved-manifest.json');identity=read(inputs/'identity.json');require((identity['base'],identity['base_tree'],identity['reviewed_head'],identity['reviewed_tree'],identity['PR'])==(BASE,BASE_TREE,HEAD,TREE,179),'preview identity')
 b=baseline(inputs);head,old,raw,oldraw,changes=source_snapshot(inputs,source,oldsource);base,leaves,_=parse(raw[CANONICAL]);require(len(base)==717 and len(leaves)==718,'canonical denominator')
 before=b['structural-per-locale'];require(len(before)==len({r['tag'] for r in before})==171,'baseline option grain');tagroot=ET.fromstring(raw[TAGS]);tags=[n.text for n in tagroot.findall('./string-array/item')];require(tags==[r['tag'] for r in before] and len(set(tags))==171,'picker order/grain')
 tierlist=json.loads(raw[IMPORTANCE],object_pairs_hook=unique)['tiers'];tiers={x['id']:set(x['keys']) for x in tierlist};require({k:len(v) for k,v in tiers.items()}=={'P0':92,'P1':249,'P2':305,'P3':71} and sum(map(len,tiers.values()))==len(set.union(*tiers.values()))==len(base),'tier partition')
 rows=[];newscopes=[];decisions=collections.Counter();review_records={};selected=set(a['approved_values']['sk']);require(len(selected)==78 and selected==set(a['approved_values']['sl']),'selected78')
 for tag in LOCALES:
  path=inputs/'review'/f'{tag}-review.json';r=read(path);require(sha(path.read_bytes())==a['review_bindings'][tag]['review_sha256'],'independent receipt hash');require(r['source_commit']==BASE and r['source_tree']==BASE_TREE and r['locale']==tag,'receipt source');review_records[tag]={e['identity']:e for e in r['entries']};require(len(r['entries'])==len(review_records[tag])==78,'receipt pair grain')
 for prior in before:
  path=prior['path'];containers,ll,nodes=parse(raw[path]);oldcontainers,oldleaves,oldnodes=parse(oldraw[path]);require(old[path]['sha']==prior['blob'],'baseline row Git binding')
  row={k:prior[k] for k in ('order','tag','path')};row['blob']=head[path]['sha']
  for tier,keys in {**tiers,'all':set(base)}.items():row[tier+'_present']=len(keys&containers.keys());row[tier+'_missing']=len(keys-containers.keys())
  overlap=leaves.keys()&ll.keys();row.update(leaves_present=len(overlap),leaves_missing=len(leaves.keys()-ll.keys()),leaves_english_identical=sum(ll[k]==leaves[k] for k in overlap),leaves_source_different=sum(ll[k]!=leaves[k] for k in overlap))
  tag=row['tag']
  if tag not in LOCALES:require(row==prior,'other option row changed')
  else:
   require(len(oldnodes)==127 and len(nodes)==205 and set(nodes)-set(oldnodes)=={'string/'+x for x in selected},'missing-only78');require(all(fingerprint(nodes[k])==fingerprint(n) for k,n in oldnodes.items()),'inherited value/attributes changed');require(tiers['P0']-nodes.keys()==HOLDS and row['P1_present']==prior['P1_present']==94 and row['P1_missing']==155,'P0 holds/P1 boundary');require('string/ui_no_resize_fits_decoder_memory' not in nodes,'P1 companion added')
   for key,e in a['approved_values'][tag].items():
    ident='string/'+key;v=review_records[tag][ident];node=nodes[ident];require(v['decision'] in ('accept','revise') and e['decision']==v['decision'],'independent decision');require(node.text==e['accepted_xml_text']==v['accepted_xml_text'] and node.attrib==e['attributes']==v['attributes'],'exact reviewed value/attrs');require(sha(node.text.encode())==v['accepted_value_sha256_utf8']==e['sha256'],'reviewed hash');require(sha(base[ident].encode())==v['source_value_sha256_utf8'],'current English binding');require(tokens(node.text)==tokens(base[ident]),'source format token equality');decisions[v['decision']]+=1
    newscopes.append({'locale':tag,'identity':ident,'decision':v['decision'],'source':base[ident],'source_sha256':sha(base[ident].encode()),'xml_text':node.text,'xml_text_sha256':sha(node.text.encode()),'attributes':node.attrib,'review_receipt_sha256':a['review_bindings'][tag]['review_sha256'],'qualifications':v['qualifications'],'acceptance':'bounded independent AI complete-value/source-static only'})
  rows.append(row)
 metrics=[k for k in rows[0] if k not in ('order','tag','path','blob')];previous={k:sum(r[k] for r in before) for k in metrics};require(previous==b['coverage-delta']['presence_totals'],'baseline totals');totals={k:sum(r[k] for r in rows) for k in metrics};delta={k:totals[k]-previous[k] for k in metrics};require({k:v for k,v in delta.items() if v}=={'P0_present':156,'P0_missing':-156,'all_present':156,'all_missing':-156,'leaves_present':156,'leaves_missing':-156,'leaves_source_different':156},'exact source presence delta')
 # Preserve prior review scopes as independent immutable history, not newly accepted pairs.
 priorledger=b['review-scope-reconciliation'];require(len(priorledger['new_review_scopes'])==110,'prior CA/RO scope grain')
 for e in priorledger['new_review_scopes']:
  path=f'Paintroid/src/main/res/values-{e["locale"]}/strings.xml';_,_,nodes=parse(raw[path]);n=nodes[e['identity']];require(n.text==e['final_xml_text'] and n.attrib==e['attributes'],'prior full value changed')
 require(len(newscopes)==len({(e['locale'],e['identity']) for e in newscopes})==156 and decisions=={'accept':148,'revise':8},'new exact scope grain')
 outputs={'structural-per-locale.json':rows,'coverage-delta.json':{'schema_version':1,'source_commit':HEAD,'source_tree':TREE,'source_status':'PR179 preview; not integrated; no PR or actual-postmerge CI result claimed','baseline_commit':BASE,'baseline_tree':BASE_TREE,'current_production_replaced':False,'options':171,'canonical_containers':717,'canonical_leaves':718,'tiers':{k:len(v) for k,v in tiers.items()},'presence_totals':totals,'presence_delta':delta,'changed_options':list(LOCALES),'unchanged_options':169,'locales_before':[r for r in before if r['tag'] in LOCALES],'locales_after':[r for r in rows if r['tag'] in LOCALES],'absent_implies_defect':False,'English_identical_implies_defect':False,'new_reviewed_pairs':156,'global_linguistic_accepted_count':None,'global_scope':{'scoped':59,'outside':112,'unchanged':True},'new_native_human_whole_language_layout_or_release_certifications':0,'actual_postmerge_status':'not supplied; required before terminal claim'},'review-scope-reconciliation.json':{'source_commit':HEAD,'source_tree':TREE,'new_review_scopes':newscopes,'new_scope_verdict_counts':dict(decisions),'prior_values_preserved':{'sk':127,'sl':127},'holds_each':sorted(HOLDS),'P0_warning_only':True,'P1_companion_absent':True,'paired120_entry60_tag_oracle_and_frozen_history_unchanged':True,'global_linguistic_accepted_count':None,'prior_categories':priorledger['prior_categories'],'prior_coverage_manifest_sha256':BASE_MANIFEST,'prior_coverage_publication':identity['prior_coverage_publication'],'prior_review_ledgers':'Unmodified baseline indexes carry prior scopes; complete202-file baseline package was independently hash-verified before selecting indexes. Its separate pending publication is not duplicated. No prior category is recounted, upgraded, revoked or guessed.','new_Valencian_direct_acceptance':0},'full-source-delta.json':{'source_commit':HEAD,'source_tree':TREE,'base':BASE,'base_tree':BASE_TREE,'files':changes}}
 return outputs,identity

def validate_actual(d,identity):
 """Validate explicit terminal join envelope. Underlying artifact validators remain mandatory."""
 require(d.get('schema_version')==1 and d.get('record_kind')=='actual-postmerge-terminal','actual terminal envelope required');merge=d['merge'];run=d['run'];pr=d['PR'];require(pr['number']==179 and pr['head']==HEAD and pr['tree']==TREE,'reviewed PR identity');require(merge['sha']!=HEAD and merge['tree']==TREE and merge['ordered_parents']==[BASE,HEAD] and merge['develop_at_verification']==merge['sha'],'actual merge tree/parents/develop');require(run['head']==merge['sha'] and run['event']=='push' and run['status']=='completed' and run['conclusion']=='success' and run['id']!=pr['run_id'] and run['attempt']>=1,'actual successful push not PR run');require(bool(run['updated_at']),'actual terminal timestamp')
 checks=d['checks'];require(len(checks)==len({x['id'] for x in checks})==6 and {x['name'] for x in checks}==CHECKS and all(x['head']==merge['sha'] and x['status']=='completed' and x['conclusion']=='success' for x in checks),'all exact actual checks')
 arts=d['artifacts'];require(len(arts)==len({x['id'] for x in arts}) and len(arts)>=4,'artifact grain');require({x['id'] for x in arts}.isdisjoint(pr['artifact_ids']),'PR artifacts cannot become postmerge');require(all(x['run_id']==run['id'] and x['head']==merge['sha'] and x['expired'] is False and re.fullmatch('[0-9a-f]{64}',x['sha256']) for x in arts),'fresh actual artifact identities')
 receipts=d['verified_receipts'];required={'apk-source','compiled-values','regression-lint','exact-script','api35'};require(set(receipts)==required,'all artifact verification receipt families');ids={x['id'] for x in arts}
 for kind,r in receipts.items():
  require(r['run_id']==run['id'] and r['tested_commit']==merge['sha'] and r['source_tree']==TREE and r['reviewed_pr_head']==HEAD and r['artifact_id'] in ids and r['result']=='pass' and re.fullmatch('[0-9a-f]{64}',r['receipt_sha256']),'actual verified receipt join '+kind)
 require(d['compiled_values']=={'new_reviewed_sk':78,'new_reviewed_sl':78,'exact_new_reviewed':156},'actual compiled new-value grain');require(d['new_linguistic_acceptances_due_to_CI']==0 and d['native_human_layout_whole_language_release_certifications']==0,'CI cannot expand linguistic scope')
 return {'actual_merge':merge['sha'],'actual_tree':TREE,'actual_push_run':run,'reviewed_PR':pr,'all_six_checks_successful':True,'fresh_artifact_ids':[x['id'] for x in arts],'underlying_receipts_must_be_supplied_and_hash_checked':True,'no_linguistic_scope_expansion':True}

def bind_receipt_payloads(envelope,payloads):
 """Join exact producer schemas without inventing absent receipt fields."""
 required={'apk-source','compiled-values','regression-lint','exact-script','api35'}
 require(set(payloads)==required,'complete receipt payload families')
 apk=payloads['apk-source']
 for kind,r in envelope['verified_receipts'].items():
  p=payloads[kind]
  require(p['run_id']==r['run_id'],'receipt payload run identity '+kind)
  commit=p['source_commit'] if kind=='exact-script' else p['tested_commit']
  require(commit==r['tested_commit'],'receipt payload actual commit '+kind)
  head=p['reviewed_pr_head'] if kind in ('exact-script','api35') else p['reviewed_head']
  require(head==r['reviewed_pr_head'],'receipt payload reviewed head '+kind)
  if kind=='regression-lint':
   # Regression has no tree field. Same exact tested commit is independently
   # joined to the actual merge and APK source tree, never added to its receipt.
   require(commit==apk['tested_commit'] and apk['source_tree']==r['source_tree'],'regression source-tree join')
  else:
   tree=p['tree'] if kind in ('compiled-values','exact-script') else p['source_tree']
   require(tree==r['source_tree'],'receipt payload actual tree '+kind)
  if kind=='compiled-values':
   # Compiled receipt has no artifact ID. Bind actual APK bytes and source/run.
   require(p['apk_sha256']==apk['build_info']['apk_sha256'] and p['run_id']==apk['run_id'] and commit==apk['tested_commit'],'compiled APK-byte/source join')
   require(apk['artifact_id']==r['artifact_id'],'compiled artifact join')
  else:require(p['artifact_id']==r['artifact_id'],'receipt payload artifact identity '+kind)
  digest_key={'apk-source':'archive_sha256','regression-lint':'artifact_sha256','exact-script':'archive_sha256','api35':'artifact_sha256'}.get(kind)
  if digest_key:
   matches=[a for a in envelope['artifacts'] if a['id']==r['artifact_id']]
   require(len(matches)==1 and p[digest_key]==matches[0]['sha256'],'receipt artifact digest '+kind)
 return validate_actual(envelope,None)

def join_actual(envelope,root,expected_manifest):
 manifest=read(root/'manifest.json');require(sha((root/'manifest.json').read_bytes())==expected_manifest,'terminal manifest pinned by caller');files=manifest['files'];require(len(files)==len({x['path'] for x in files}),'terminal manifest grain')
 for e in files:
  b=safe(root,e['path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'] and git(b)==e['git_blob_sha1'],'terminal manifest payload')
 entries={e['path']:e for e in files};payloads={}
 for kind,r in envelope['verified_receipts'].items():
  require(r['receipt_path'] in entries,'receipt absent from pinned manifest')
  b=safe(root,r['receipt_path']).read_bytes();require(sha(b)==r['receipt_sha256'],'receipt hash');payloads[kind]=json.loads(b,object_pairs_hook=unique)
 return bind_receipt_payloads(envelope,payloads)

def run(a):
 out,identity=compute(a.inputs,a.source_root,a.baseline_source_root)
 if a.mode=='actual-postmerge':
  require(a.actual_evidence is not None and a.actual_manifest_sha256 is not None,'actual evidence and immutable manifest hash required; preview cannot be promoted')
  envelope=read(a.actual_evidence/'coverage-terminal-envelope.json');terminal=join_actual(envelope,a.actual_evidence,a.actual_manifest_sha256);out['terminal-status-supplement.json']=terminal
  for n in ('coverage-delta.json','review-scope-reconciliation.json','full-source-delta.json'):out[n]['source_commit']=terminal['actual_merge'];out[n]['source_status']='actual merge; supplied fresh actual-postmerge terminal evidence verified'
  out['coverage-delta.json']['current_production_replaced']=True;out['coverage-delta.json']['actual_postmerge_status']='success; fresh actual push artifacts, not PR artifacts'
 else:require(a.actual_evidence is None and a.actual_manifest_sha256 is None,'preview must not imply actual evidence')
 a.out.mkdir(parents=True,exist_ok=True)
 for n,d in out.items():emit(a.out,n,d)
 with (a.out/'structural-per-locale.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(out['structural-per-locale.json'][0]));w.writeheader();w.writerows(out['structural-per-locale.json'])
 print(json.dumps({'mode':a.mode,'source_commit':out['coverage-delta.json']['source_commit'],'options':171,'new_scope_pairs':156,'structural_P0_delta':156,'actual_postmerge_claim':a.mode=='actual-postmerge'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ('inputs','source-root','baseline-source-root','out'):p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--mode',choices=['preview','actual-postmerge'],default='preview');p.add_argument('--actual-evidence',type=Path);p.add_argument('--actual-manifest-sha256');run(p.parse_args())
