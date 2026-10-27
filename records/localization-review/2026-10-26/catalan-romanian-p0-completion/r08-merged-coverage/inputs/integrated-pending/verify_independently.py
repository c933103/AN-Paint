"""Independent DOM/Git CLI coverage calculation; no recomputation-module import."""
import argparse,collections,csv,hashlib,json,subprocess
from pathlib import Path
from xml.dom import minidom as D
p=argparse.ArgumentParser()
for name in ('inputs','actual-inputs','source-root','baseline-source-root','result','out'):p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args()
def require(ok,m):
 if not ok:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def text(n):return ''.join(text(c) if c.nodeType==c.ELEMENT_NODE else c.data if c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE) else '' for c in n.childNodes)
def catalogue(raw):
 root=D.parseString(raw).documentElement;c={};l={};attrs={}
 for n in root.childNodes:
  if n.nodeType!=n.ELEMENT_NODE:continue
  key=n.tagName+'/'+n.getAttribute('name');require(key not in attrs,'independent duplicate identity');attrs[key]=dict(n.attributes.items())
  if n.getAttribute('translatable')=='false':continue
  if n.tagName=='string':c[key]=text(n);l[key]=text(n)
  else:
   c[key]={};items=[x for x in n.childNodes if x.nodeType==x.ELEMENT_NODE]
   for i,x in enumerate(items):q=x.getAttribute('quantity') if n.tagName=='plurals' else str(i);c[key][q]=text(x);l[key+'['+q+']']=text(x)
 return c,l,attrs
head='e5f2d4e2d07e678076f022aa7b3ef923e13c3721';tree='806d9577409c4044212d1c12e6e38da46417bae6'
proof=read(a.actual_inputs/'actual-merge-identity.json');require(sha((a.actual_inputs/'actual-merge-identity.json').read_bytes())=='0abf768af2344a93fa403e1730a11f049c92d1e9cb1d4fc314baaacf784c3d4e','independent actual receipt hash');require(proof['merge']==head and proof['tree']==tree and proof['parents']==['ce796879f4568a27b9d905a8e8db639dd0a93a30','82995ec1f030d23cb4e2b1426b511abe802890eb'] and proof['develop_at_verification']==head and proof['postmerge_runs'][0]['id']==40350966050 and proof['postmerge_runs'][0]['head']==head and proof['postmerge_runs'][0]['event']=='push' and proof['postmerge_runs'][0]['status']=='in_progress','independent actual merge/pending push proof')
t=read(a.actual_inputs/'fixed-head-tree.json');blobs=[x for x in t['tree'] if x['type']=='blob'];require(len(blobs)==1379 and t['sha']==tree and t['truncated'] is False,'independent tree inventory')
paths=''.join(str((a.source_root/x['path']).resolve())+'\n' for x in blobs);run=subprocess.run(['git','hash-object','--stdin-paths'],input=paths,text=True,capture_output=True,check=True);require(run.stdout.splitlines()==[x['sha'] for x in blobs],'independent git CLI source identities')
by_path={x['path']:x for x in blobs};base,bl,_=catalogue((a.source_root/'Paintroid/src/main/res/values/strings.xml').read_bytes());require(len(base)==717 and len(bl)==718,'independent canonical grain')
importance=read(a.source_root/'translations/string-importance.json');tiers={x['id']:set(x['keys']) for x in importance['tiers']};tagsdoc=D.parseString((a.source_root/'Paintroid/src/main/res/values/app_language_tags.xml').read_bytes());tags=[text(n) for n in tagsdoc.getElementsByTagName('item')];require(len(tags)==len(set(tags))==171,'independent picker grain')
previous=read(a.inputs/'baseline/structural-per-locale.json');previousby={x['tag']:x for x in previous};rows=[];rawpairs={}
for order,tag in enumerate(tags,1):
 old=previousby[tag];path=old['path'];c,l,attrs=catalogue((a.source_root/path).read_bytes());r={'order':old['order'],'tag':tag,'path':path,'blob':by_path[path]['sha']}
 for tier,keys in dict(tiers,all=set(base)).items():r[tier+'_present']=sum(k in c for k in keys);r[tier+'_missing']=sum(k not in c for k in keys)
 common=[k for k in bl if k in l];r.update(leaves_present=len(common),leaves_missing=sum(k not in l for k in bl),leaves_english_identical=sum(l[k]==bl[k] for k in common),leaves_source_different=sum(l[k]!=bl[k] for k in common));rows.append(r)
 if tag in ('ca','ro'):
  before,_,beforeattrs=catalogue((a.baseline_source_root/path).read_bytes());require(len(before)==150 and len(c)==205 and all(c[k]==before[k] and attrs[k]==beforeattrs[k] for k in before),'independent inherited complete pairs');rawpairs[tag]=(c,attrs)
require(rows==read(a.result/'structural-per-locale.json'),'independent all 171 rows')
with (a.result/'structural-per-locale.csv').open(newline='') as stream:
 csvrows=list(csv.DictReader(stream));require(len(csvrows)==171,'CSV rows')
 for expected,actual in zip(rows,csvrows):require(all(str(v)==actual[k] for k,v in expected.items()),'CSV typed values')
metrics=[k for k in rows[0] if k not in ('order','tag','path','blob')];totals={k:sum(r[k] for r in rows) for k in metrics};delta={k:totals[k]-sum(r[k] for r in previous) for k in metrics};report=read(a.result/'coverage-delta.json');require(totals==report['presence_totals'] and delta==report['presence_delta'],'independent totals/delta')
approved=read(a.inputs/'approved-manifest.json');pairs=set();verdicts=collections.Counter()
for e in approved['values']:
 tag,key=e['locale'],e['identity'];require((tag,key) not in pairs,'independent reviewed grain');pairs.add((tag,key));c,attrs=rawpairs[tag];require(c[key]==e['final_xml_text'] and attrs[key]==e['attributes'] and base[key]==e['source'],'independent current/source full review pair');require(sha(c[key].encode())==e['final_xml_text_sha256_utf8'] and sha(e['source'].encode())==e['source_value_sha256_utf8'],'independent pair hashes');verdicts[e['verdict']]+=1
require(len(pairs)==110 and verdicts=={'accept':107,'revise':3},'independent review counts')
priorpairs=set()
for file in ('prior-save-scope-ledger.json','baseline/integrated-pending/review-scope-reconciliation.json'):
 for e in read(a.inputs/file)['new_review_scopes']:
  t,k=e['locale'],e['identity'];require((t,k) not in priorpairs and (t,k) not in pairs,'independent prior/new disjointness');priorpairs.add((t,k));c,attrs=rawpairs[t];require(c[k]==e['xml_text'] and attrs[k]==e['attributes'] and base[k]==e['source'],'independent prior current scope')
require(collections.Counter(t for t,k in priorpairs)=={'ca':23,'ro':23},'independent prior23 count')
require(report['source_commit']==head and report['source_tree']==tree and report['current_production_replaced'] is True and report['production_baseline_commit']=='ce796879f4568a27b9d905a8e8db639dd0a93a30' and report['global_accepted_count'] is None and report['new_Valencian_direct_acceptance']==0,'integrated/pending nonacceptance state')
require(report['workflow_results']['actual_postmerge_run']==40350966050 and report['workflow_results']['actual_postmerge_event']=='push' and report['workflow_results']['actual_postmerge_terminal_result'] is None and report['workflow_results']['PR_artifacts_are_not_postmerge_artifacts'] is True,'independent pending/not relabelled gate')
receipt={'schema_version':1,'source_commit':head,'source_tree':tree,'status':'actual merged source independently verified; actual postmerge CI remains pending in supplied receipt','method':'Independent DOM parser, separately computed rows/totals and read-only Git hash-object CLI; no import from recompute_delta.py or its tests.','raw_tracked_Git_blobs_verified':1379,'offered_option_rows_recomputed':171,'CSV_and_JSON_agree':True,'all_totals_and_deltas_agree':True,'new_reviewed_complete_pairs_hash_matched':110,'new_verdicts':dict(verdicts),'inherited_complete_values_preserved':300,'prior_reviewed_pairs_preserved_separately':46,'prior_reviewed_pairs_per_locale':23,'new_Valencian_direct_acceptance':0,'totals':totals,'delta':delta,'limits':['Structural/raw complete-value identity checks only; review qualifications are retained by exact source-bound original receipts.','Actual merge identity is supplied and byte-bound. No actual postmerge success, native-human, device, layout or release outcome inferred.']}
a.out.mkdir(parents=True,exist_ok=True);out=a.out/'independent-verification.json';out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(sha(out.read_bytes()))
