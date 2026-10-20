import json,hashlib,xml.etree.ElementTree as E,pathlib
base=json.load(open('/tmp/an-all-language-reviews/all-language-review-union.json'))
values=json.load(open('/tmp/an-all-language-coverage/source-values.json'))
H=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
out={'source_commit':'26cb10b1a0fddadfb4ca282431879ab6e0a82bde','baseline_evidence_commit':'2fff195596e7a792185b3b29eb756b7df9081a92','review_packet_commit':'2b22c4f9efc2174854a247901f5c191a299d69df','languages':[],'new_pair_receipts':[],'limits':['Original source-only, no-device and context limitations remain.','No whole-language acceptance.','Taiwan GIF follow-up wording is withheld from new linguistic credit pending an independent full-string re-review.']}
for tag,file,root,rel in [('ko-KR','/tmp/an-korean-priority-review/review.json','/tmp/an-korean-priority-fixes','values-b+ko+KR'),('zh-TW','/tmp/an-taiwan-priority-review/review.json','/tmp/an-taiwan-priority-fixes','values-zh-rTW')]:
 r=next(x for x in base['languages'] if x['tag']==tag)
 current={ 'string/'+e.attrib['name']:e.text or '' for e in E.parse(root+'/Paintroid/src/main/res/'+rel+'/strings.xml').getroot() if e.tag=='string'}
 accepted=set(r['reviewed_current_keys']);held=set(r['needs_rereview_keys']);present=accepted|held|set(r['present_review_unknown_keys'])
 for i,e in enumerate(json.load(open(file))['entries']):
  key=e['key'];status=e.get('status',e.get('disposition')); english=e['english'];assert english==values['default'][key],key
  target=(e.get('proposed_korean') if status=='corrected' else e.get('current_korean')) if tag=='ko-KR' else (e['proposed'] if status=='corrected' else e['current'])
  state='needs_rereview' if status=='uncertain' or target!=current[key] else 'reviewed_current'
  # Existing explicit assembly-help semantic reference hold is not cleared by a narrower review.
  if key in r['needs_rereview_keys']: state='needs_rereview'
  if state=='reviewed_current':accepted.add(key);held.discard(key)
  else:held.add(key);accepted.discard(key)
  out['new_pair_receipts'].append({'tag':tag,'key':key,'state':state,'original_decision':status,'review_entry_index':i,'english_sha256':H(english),'localized_sha256':H(current[key]),'context_scope':e.get('context_scope',e.get('review_scope')),'target_matches_full_review':target==current[key]})
 unknown=present-accepted-held
 n=dict(r,reviewed_current=len(accepted),needs_rereview=len(held),present_review_unknown=len(unknown),reviewed_current_keys=sorted(accepted),needs_rereview_keys=sorted(held),present_review_unknown_keys=sorted(unknown))
 assert len(accepted)+len(held)+len(unknown)+n['missing']==717
 out['languages'].append(n)
 print(tag,n['reviewed_current'],n['needs_rereview'],n['present_review_unknown'],n['needs_rereview_keys'])
json.dump(out,open('/tmp/an-merged-review-delta/delta.json','w'),ensure_ascii=False,indent=2)
