"""Independent DOM/CSV/Git executable checks for the structural delta outputs."""
import argparse,csv,json,pathlib,subprocess,xml.dom.minidom as DOM
p=argparse.ArgumentParser();p.add_argument('--source-root',type=pathlib.Path,required=True);p.add_argument('--report',type=pathlib.Path,required=True);a=p.parse_args()
def check(ok,msg):
 if not ok:raise ValueError(msg)
def load(name):return json.loads((a.report/name).read_text())
def text(n):return ''.join(text(c) if c.nodeType==c.ELEMENT_NODE else c.data if c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE) else '' for c in n.childNodes)
def parse(path):
 doc=DOM.parse(str(path));containers={};leaves={}
 for n in doc.documentElement.childNodes:
  if n.nodeType!=n.ELEMENT_NODE or n.tagName not in ['string','plurals','string-array'] or n.getAttribute('translatable')=='false':continue
  key=n.tagName+'/'+n.getAttribute('name');check(key not in containers,'duplicate container');containers[key]=True
  if n.tagName=='string':leaves[key]=text(n)
  else:
   children=[x for x in n.childNodes if x.nodeType==x.ELEMENT_NODE]
   for i,c in enumerate(children):
    check(c.tagName=='item','invalid child');q=c.getAttribute('quantity') if n.tagName=='plurals' else str(i);leaf=key+'['+q+']';check(leaf not in leaves,'duplicate leaf');leaves[leaf]=text(c)
 return containers,leaves
rows=load('structural-per-locale.json');coverage=load('coverage-delta.json');bindings=load('source-bindings.json');check(len(rows)==len({x['tag'] for x in rows})==171,'locale inventory')
for f in bindings['files']:
 actual=subprocess.check_output(['git','hash-object',str(a.source_root/f['path'])],text=True).strip();check(actual==f['merged_blob'],'Git executable hash differs')
canonical,baseleaves=parse(a.source_root/'Paintroid/src/main/res/values/strings.xml');tiers=json.loads((a.source_root/'translations/string-importance.json').read_text())['tiers'];fields=[];sums={}
for row in rows:
 c,l=parse(a.source_root/row['path']);calc={}
 for tier in tiers+[{'id':'all','keys':list(canonical)}]:
  keys=tier['keys'];calc[tier['id']+'_present']=sum(k in c for k in keys);calc[tier['id']+'_missing']=sum(k not in c for k in keys)
 calc['leaves_present']=sum(k in l for k in baseleaves);calc['leaves_missing']=sum(k not in l for k in baseleaves);calc['leaves_english_identical']=sum(k in l and l[k]==v for k,v in baseleaves.items());calc['leaves_source_different']=sum(k in l and l[k]!=v for k,v in baseleaves.items())
 check(all(row[k]==v for k,v in calc.items()),'DOM recomputation mismatch');fields=list(calc)
 for k,v in calc.items():sums[k]=sums.get(k,0)+v
check(sums==coverage['presence_totals'],'aggregate mismatch');check(sums['all_present']+sums['all_missing']==171*717,'container denominator');check(sums['leaves_present']+sums['leaves_missing']==171*718,'leaf denominator')
with (a.report/'structural-per-locale.csv').open(newline='') as f:csvrows=list(csv.DictReader(f))
for r in csvrows:
 for k in fields+['order']:r[k]=int(r[k])
check(csvrows==rows,'CSV/JSON mismatch');check(coverage['full_presence_options']==59 and coverage['zero_presence_options']==31,'full/zero groups')
result={'schema':'nynorsk-coverage-independent-validation-v1','source_commit':'df9bc04b848ab5e99457bc67265d771bb839ec9d','rows':171,'source_files_Git_executable_verified':len(bindings['files']),'separate_DOM_calculation_matches_all_presence_and_English_identity_fields':True,'CSV_JSON_equal':True,'aggregate_denominators_verified':True,'native_linguistic_or_layout_judgment_added':False}
(a.report/'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
