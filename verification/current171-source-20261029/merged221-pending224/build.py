import json,hashlib,subprocess,xml.etree.ElementTree as E
from pathlib import Path
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--previous',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
def git(*args):return subprocess.check_output(['git','-C',str(a.repo),*args])
source='ae7d25ca60f9852a9d936743a3c4a1833e9e24ba';candidate='6fd72e8d31f13676e92c16c40506e4c1bdd4c221'
for ref,tree in [(source,'de438227d759a2def5fc987600c3c1591f452f9f'),(candidate,'8f4874a6daffab624fb65501cf1d370017714c99')]:
 if git('rev-parse',ref+'^{tree}').decode().strip()!=tree:raise ValueError('Wrong immutable tree')
def blob(ref,path):return git('show',ref+':'+path)
old=json.loads(a.previous.read_text());tiers=json.loads(blob(source,'translations/string-importance.json'))['tiers']; keys={t['id']:set(t['keys']) for t in tiers if t['id'] in ['P0','P1']}
if blob(source,'translations/string-importance.json')!=blob(candidate,'translations/string-importance.json'):raise ValueError('Tier drift')
if len(old['rows'])!=171 or len({r['tag'] for r in old['rows']})!=171:raise ValueError('Inventory mismatch')
for filename, field in [('app_language_tags.xml','tag'),('app_language_names.xml','picker_label')]:
 path='Paintroid/src/main/res/values/'+filename
 current=blob(source,path)
 if current!=blob(candidate,path):raise ValueError('Picker changed')
 values=[x.text for x in E.fromstring(current).findall(".//string-array[@name='"+filename.removesuffix('.xml')+"']/item")]
 if values!=[r[field] for r in old['rows']]:raise ValueError('Picker inventory drift')
pending={'fa':222,'he':222,'ur':222,'sr-Cyrl':223,'sr-Latn':223};rows=[]
def presence(data):
 entries={x.tag+'/'+x.attrib['name'] for x in E.fromstring(data) if x.tag in ('string','plurals') and 'name' in x.attrib}
 return {t:dict(present=len(ks&entries),missing=len(ks-entries),total=len(ks)) for t,ks in keys.items()}
for r in old['rows']:
 p=r['catalogue_path'];s=blob(source,p);c=blob(candidate,p);tag=r['tag']
 if tag not in pending and s!=c:raise ValueError('Unexpected locale delta '+tag)
 rows.append(dict(order=r['order'],tag=tag,picker_label=r['picker_label'],catalogue_path=p,current_catalogue_sha256=hashlib.sha256(s).hexdigest(),current_explicit_priority_presence=presence(s),current_review_acceptance_total=None,pending_pr=pending.get(tag),pending_integration_pr=224 if tag in pending else None,pending_catalogue_sha256=hashlib.sha256(c).hexdigest() if tag in pending else None,pending_explicit_priority_presence=presence(c) if tag in pending else None))
o=dict(source_commit=source,source_tree=git('rev-parse',source+'^{tree}').decode().strip(),pending_integration_head=candidate,pending_integration_tree=git('rev-parse',candidate+'^{tree}').decode().strip(),scope='All 171 explicit source catalogues. Presence only, not runtime resolution or linguistic acceptance. PR221 is merged; PR224 remains pending. Prior historical acceptance totals are not relabelled current. No stopped bulk archive resumed.',rows=rows)
o['totals']={t:dict(current_present=sum(r['current_explicit_priority_presence'][t]['present'] for r in rows),current_missing=sum(r['current_explicit_priority_presence'][t]['missing'] for r in rows),denominator=len(rows)*len(keys[t])) for t in keys};o['pending_rows']=len(pending)
a.output.mkdir(parents=True,exist_ok=True);(a.output/'current171-source-and-pending.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
lines=['# All 171 source catalogues after PR221','',o['scope'],'','Source: '+source+'. Pending PR224: '+candidate+'.','', '| # | Tag | P0 present | P1 present | Pending source PR |','|---:|---|---:|---:|---:|']
for r in rows:lines.append(f"| {r['order']} | {r['tag']} | {r['current_explicit_priority_presence']['P0']['present']} | {r['current_explicit_priority_presence']['P1']['present']} | {r['pending_pr'] or '—'} |")
(a.output/'CURRENT-171.md').write_text('\n'.join(lines)+'\n');print(json.dumps({k:v for k,v in o.items() if k!='rows'},indent=2))
