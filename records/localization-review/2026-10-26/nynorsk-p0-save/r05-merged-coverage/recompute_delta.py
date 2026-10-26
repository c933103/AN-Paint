"""Recompute structural coverage from a verified project checkout; no application code executes."""
import argparse,collections,csv,hashlib,json,pathlib,xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--source-root',type=pathlib.Path,required=True);p.add_argument('--source-tree',type=pathlib.Path,required=True);p.add_argument('--baseline-report',type=pathlib.Path,required=True);p.add_argument('--baseline-nn',type=pathlib.Path,required=True);p.add_argument('--review',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
def require(ok,message):
 if not ok:raise ValueError(message)
def read(path):return json.loads(path.read_text(encoding='utf8'))
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def sha(b):return hashlib.sha256(b).hexdigest()
def emit(name,obj):(a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def parse(b):
 root=ET.fromstring(b);require(root.tag=='resources','invalid resource root');c={};l={}
 for n in root:
  if n.tag not in ('string','plurals','string-array') or n.get('translatable')=='false':continue
  require(bool(n.get('name')),'missing name');k=n.tag+'/'+n.get('name');require(k not in c,'duplicate container')
  if n.tag=='string':c[k]=''.join(n.itertext());l[k]=c[k]
  else:
   values={}
   for i,item in enumerate(n):
    require(item.tag=='item','invalid resource child');q=item.get('quantity') if n.tag=='plurals' else str(i);require(q is not None and q not in values,'duplicate/missing item');values[q]=''.join(item.itertext());l[k+'['+q+']']=values[q]
   require(bool(values),'empty resource container');c[k]=values
 return c,l
baseline=read(a.baseline_report/'per-locale-final.json');summary=read(a.baseline_report/'summary.json');provenance=read(a.baseline_report/'source-provenance.json');tree=read(a.source_tree);require(not tree.get('truncated'),'truncated source tree');blobs={v['path']:v for v in tree['tree'] if v['type']=='blob'}
require(len(baseline)==171 and summary['source_commit']=='d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4','wrong baseline');require(tree['sha']=='857a20103285a77846e340b326667c15a402ff9e','wrong merged snapshot')
source={};changed=[];bindings=[]
for f in provenance['source_files']:
 path=f['path'];b=(a.source_root/path).read_bytes();require(git(b)==blobs[path]['sha'],'source bytes/tree mismatch: '+path);source[path]=b
 bindings.append({'path':path,'baseline_blob':f['git_blob'],'merged_blob':git(b),'sha256':sha(b),'bytes':len(b),'unchanged':f['git_blob']==git(b)})
 if f['git_blob']!=git(b):changed.append(path)
require(len(source)==176,'source inventory drift');nn='Paintroid/src/main/res/values-b+nn/strings.xml';require(changed==[nn],'unexpected changed coverage source')
base,leaves=parse(source['Paintroid/src/main/res/values/strings.xml']);require(len(base)==717 and len(leaves)==718,'canonical denominator changed')
arrays=ET.fromstring(source['Paintroid/src/main/res/values/app_language_tags.xml']).findall('string-array');require(len(arrays)==1,'invalid tag inventory');tags=[x.text for x in arrays[0]];require(len(tags)==len(set(tags))==171,'tag inventory changed');require(tags==[r['tag'] for r in baseline],'picker order changed')
tiers={x['id']:set(x['keys']) for x in json.loads(source['translations/string-importance.json'])['tiers']};require(sum(map(len,tiers.values()))==len(set.union(*tiers.values()))==len(base) and set.union(*tiers.values())==set(base),'invalid tier partition')
rows=[]
for old in baseline:
 path=old['path'];c,l=parse(source[path]);r={k:old[k] for k in ['order','tag','path']};r['blob']=blobs[path]['sha']
 for t,keys in {**tiers,'all':set(base)}.items():r[t+'_present']=len(keys&c.keys());r[t+'_missing']=len(keys-c.keys())
 r.update(leaves_present=len(leaves.keys()&l.keys()),leaves_missing=len(leaves.keys()-l.keys()),leaves_english_identical=sum(l[k]==leaves[k] for k in leaves.keys()&l.keys()),leaves_source_different=sum(l[k]!=leaves[k] for k in leaves.keys()&l.keys()))
 if old['tag']!='nn':require(all(r[k]==old[k] for k in r),'unexpected other-locale delta')
 rows.append(r)
metrics=[k for k in rows[0] if k not in ['order','tag','path','blob']];totals={k:sum(r[k] for r in rows) for k in metrics};delta={k:totals[k]-summary['presence_totals'][k] for k in metrics};require({k:v for k,v in delta.items() if v}=={'P0_present':8,'P0_missing':-8,'all_present':8,'all_missing':-8,'leaves_present':8,'leaves_missing':-8,'leaves_source_different':8},'unexpected aggregate delta')
oldnn=a.baseline_nn.read_bytes();f=next(x for x in bindings if x['path']==nn);require(git(oldnn)==f['baseline_blob'],'wrong baseline nn');oldroot=ET.fromstring(oldnn);newroot=ET.fromstring(source[nn]);oldnodes={n.get('name'):n for n in oldroot};newnodes={n.get('name'):n for n in newroot};require(len(oldnodes)==len(oldroot)==110 and len(newnodes)==len(newroot)==118,'nn inventory mismatch')
for k,n in oldnodes.items():require((n.tag,n.attrib,n.text,list(n))==(newnodes[k].tag,newnodes[k].attrib,newnodes[k].text,list(newnodes[k])),'changed inherited nn value')
review=read(a.review);require(review['input_candidates_sha256']=='deb1f64fdcba57228004ace4f402cffd5ae3269494e7a71ba1eeb7acc03903c2' and len(review['entries'])==8,'wrong review');newreceipts=[]
for e in review['entries']:
 key=e['identity'].split('/')[1];n=newnodes[key];require(key not in oldnodes and n.text==e['approved_xml_text'] and n.attrib==e['approved_attributes'],'reviewed value/attribute mismatch');require(sha(n.text.encode())==e['approved_xml_text_sha256'],'review target hash mismatch');require(base[e['identity']]==e['source'] and sha(e['source'].encode())==e['source_sha256'],'review source hash mismatch');newreceipts.append({k:e[k] for k in ['identity','source_sha256','approved_xml_text_sha256','verdict','confidence','approved_attributes','native_human_acceptance','runtime_or_device_acceptance']})
oldrow=next(r for r in baseline if r['tag']=='nn');require(oldrow['mixed_evidence_identity_union']==0,'new scopes overlap prior nn inventory')
a.out.mkdir(exist_ok=True,parents=True);emit('structural-per-locale.json',rows)
with (a.out/'structural-per-locale.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
emit('source-bindings.json',{'baseline_commit':summary['source_commit'],'merged_commit':tree['sha'],'merged_tree':'6bb4fa11534149df7f8f58cb3d21faf2b802089f','files':bindings,'unchanged_source_files':175,'changed_source_files':1})
emit('coverage-delta.json',{'schema':'nynorsk-merge-coverage-delta-v1','baseline_commit':summary['source_commit'],'merged_commit':tree['sha'],'merged_tree':'6bb4fa11534149df7f8f58cb3d21faf2b802089f','options':171,'canonical_containers':717,'canonical_leaves':718,'tiers':{k:len(v) for k,v in tiers.items()},'presence_totals':totals,'presence_delta':delta,'full_presence_options':sum(r['all_missing']==0 for r in rows),'zero_presence_options':sum(r['all_present']==0 for r in rows),'nn_before':{k:oldrow[k] for k in rows[0]},'nn_after':next(r for r in rows if r['tag']=='nn'),'new_review_scopes':newreceipts,'new_disjoint_bounded_AI_whole_value_scopes':8,'prior_review_scopes':'All previously present catalogue values remain unchanged. No inherited scope is revoked or upgraded; the new nn identities were absent from the prior mixed evidence inventory. Prior author-only, historical, qualified, clause-only and synthetic distinctions remain as documented in the immutable baseline report.','postmerge_ci':'pending separately at time of this structural delta; PR-head tests are not relabelled postmerge results','native_or_whole_language_certifications':0})
print(json.dumps({'options':171,'totals':totals,'delta':delta,'new_disjoint_review_scopes':8},indent=2))
