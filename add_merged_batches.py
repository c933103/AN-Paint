import json,xml.etree.ElementTree as E,hashlib
H=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
b=json.load(open('/tmp/an-all-language-reviews/all-language-review-union.json'));d=json.load(open('/tmp/an-merged-review-delta/delta.json')); rows={x['tag']:x for x in b['languages']}; rows.update({x['tag']:x for x in d['languages']}); changed=set(x['tag'] for x in d['languages'])
def accept(tag,key,value,path,receipt):
 r=rows[tag];actual=E.parse(path).getroot().find(f"string[@name='{key.split('/',1)[1]}']").text;assert actual==value,(tag,key,actual,value)
 for field in ['needs_rereview_keys','present_review_unknown_keys','missing_keys']:
  if key in r[field]:r[field].remove(key)
 if key not in r['reviewed_current_keys']:r['reviewed_current_keys'].append(key)
 for field,target in [('reviewed_current_keys','reviewed_current'),('needs_rereview_keys','needs_rereview'),('present_review_unknown_keys','present_review_unknown'),('missing_keys','missing')]:r[field].sort();r[target]=len(r[field])
 r['present']=717-r['missing'];assert sum(r[k] for k in ['reviewed_current','needs_rereview','present_review_unknown','missing'])==717
 d['new_pair_receipts'].append({'tag':tag,'key':key,'state':'reviewed_current','localized_sha256':H(value),'source_receipt':receipt});changed.add(tag)
sv=json.load(open('/tmp/swedish-next-review/accepted-values.json'))
for key,val in sv.items():accept('sv','string/'+key,val,'/tmp/an-swedish-p1-integration/Paintroid/src/main/res/values-sv/strings.xml','independent-final-receipt.json, evidence57e4e46')
for r in json.load(open('/tmp/an-open-item-fixes/tools/fixtures/current_localization/open_review_recovery.json')):accept(r['tag'],'string/'+r['key'],r['value'],'/tmp/an-open-item-fixes/'+r['path'],'open-independent-review.json, evidence2b22c4f')
d['languages']=[rows[tag] for tag in sorted(changed)];d['source_commit']='1734d0c477fc42e097a0cb7ed115cc842306f851';d['summary']={k:sum(r[k] for r in rows.values()) for k in ['reviewed_current','needs_rereview','present_review_unknown','missing']}
assert sum(d['summary'].values())==171*717
json.dump(d,open('/tmp/an-merged-review-delta/delta-all-merged.json','w'),ensure_ascii=False,indent=2)
print(d['summary']);print([(r['tag'],r['reviewed_current'],r['needs_rereview'],r['present_review_unknown'],r['missing']) for r in d['languages']])
# Reconcile the completed unchanged-value re-review; most pairs already count.
for rec in json.load(open('/tmp/an-open-review-resolution/review.json'))['records']:
 if rec['disposition']=='accept_unchanged':
  assert rec['complete_message_read']
  accept(rec['tag'],rec['key'],rec['current'],'/tmp/an-open-item-fixes/'+rows[rec['tag']]['catalogue_path'],'open-review-resolution/review.json, evidence2b22c4f')
d['languages']=[rows[tag] for tag in sorted(changed)];d['summary']={k:sum(r[k] for r in rows.values()) for k in ['reviewed_current','needs_rereview','present_review_unknown','missing']}
assert sum(d['summary'].values())==171*717
json.dump(d,open('/tmp/an-merged-review-delta/delta-all-merged.json','w'),ensure_ascii=False,indent=2)
print('With unchanged-value re-review:',d['summary']);print([(r['tag'],r['reviewed_current'],r['needs_rereview']) for r in d['languages']])
