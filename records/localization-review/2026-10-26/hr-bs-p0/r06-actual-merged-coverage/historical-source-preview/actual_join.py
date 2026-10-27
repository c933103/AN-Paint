"""Strict PR183 actual execution joins. Synthetic tests never count as runtime evidence."""
from coverage_common import *
from recompute_coverage import BASE,HEAD,TREE,safe
CHECKS={"Emulator API 35","Core emulator API 35","Position dialog API 35","Regression tests and lint","Build APK and corresponding source","Exact-script resource generation"}
def validate_actual(d,identity):
 """Validate explicit terminal join envelope. Underlying artifact validators remain mandatory."""
 require(d.get('schema_version')==1 and d.get('record_kind')=='actual-postmerge-terminal','actual terminal envelope required');merge=d['merge'];run=d['run'];pr=d['PR'];require(pr['number']==183 and pr['head']==HEAD and pr['tree']==TREE,'reviewed PR identity');require(re.fullmatch('[0-9a-f]{40}',merge['sha']) and merge['sha']!=HEAD and merge['tree']==TREE and merge['ordered_parents']==[BASE,HEAD] and merge['develop_at_verification']==merge['sha'],'actual merge tree/parents/develop');require(run['head']==merge['sha'] and run['event']=='push' and run['status']=='completed' and run['conclusion']=='success' and run['id']!=pr['run_id'] and run['attempt']>=1,'actual successful push not PR run');require(bool(run['updated_at']),'actual terminal timestamp')
 checks=d['checks'];require(len(checks)==len({x['id'] for x in checks})==6 and {x['name'] for x in checks}==CHECKS and all(x['head']==merge['sha'] and x['status']=='completed' and x['conclusion']=='success' for x in checks),'all exact actual checks')
 arts=d['artifacts'];require(len(arts)==len({x['id'] for x in arts}) and len(arts)>=4,'artifact grain');require({x['id'] for x in arts}.isdisjoint(pr['artifact_ids']),'PR artifacts cannot become postmerge');require(all(x['run_id']==run['id'] and x['head']==merge['sha'] and x['expired'] is False and re.fullmatch('[0-9a-f]{64}',x['sha256']) for x in arts),'fresh actual artifact identities')
 receipts=d['verified_receipts'];required={'apk-source','compiled-values','regression-lint','exact-script','api35'};require(set(receipts)==required,'all artifact verification receipt families');ids={x['id'] for x in arts}
 for kind,r in receipts.items():
  require(r['run_id']==run['id'] and r['tested_commit']==merge['sha'] and r['source_tree']==TREE and r['reviewed_pr_head']==HEAD and r['artifact_id'] in ids and r['result']=='pass' and re.fullmatch('[0-9a-f]{64}',r['receipt_sha256']),'actual verified receipt join '+kind)
 require(d['compiled_values']=={'new_hr':78,'new_bs':78,'new_reviewed':156,'preserved_hr_bs':215,'prior_reviewed':697,'combined_bounded_reviewed':853},'actual compiled new-value grain');require(d['new_linguistic_acceptances_due_to_CI']==0 and d['native_human_layout_whole_language_release_certifications']==0,'CI cannot expand linguistic scope')
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
   require(p['current_Serbian_reviewed_entries']==149 and p['current_Serbian_reviewed_entries_by_locale']=={'sr-Cyrl':75,'sr-Latn':74} and p['successor_changed_values']==2 and p['unchanged_Serbian_reviewed_values']==147 and p['prior_reviewed_entries']==548 and p['total_reviewed_entries']==853 and p['new_reviewed_entries']==156 and p['new_reviewed_entries_by_locale']=={'hr':78,'bs':78} and p['prior_reviewed_total']==697 and p['inherited_entries']==806 and p['inherited_entries_by_locale']=={'hr':98,'bs':117,'sk':127,'sl':127,'sr-Cyrl':169,'sr-Latn':168},'compiled receipt exact new Serbian scope')
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

