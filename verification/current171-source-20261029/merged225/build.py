import argparse,hashlib,json,subprocess,xml.etree.ElementTree as E
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
source='b05a4463e03683f92c2b3ebe21905e0420362a42';tree='0f5961b48f686b0c04748517e095eaa349cfa0a0'
def blob(path):return subprocess.check_output(['git','-C',str(a.repo),'show',tree+':'+path])
old=json.loads(a.previous.read_text());tiers=json.loads(blob('translations/string-importance.json'))['tiers'];keys={t['id']:set(t['keys']) for t in tiers if t['id'] in ('P0','P1')}
if len(old['rows'])!=171 or len({r['tag'] for r in old['rows']})!=171:raise ValueError('Bad inventory')
for file,field in [('app_language_tags.xml','tag'),('app_language_names.xml','picker_label')]:
 root=E.fromstring(blob('Paintroid/src/main/res/values/'+file));values=[e.text for e in root.find("string-array[@name='"+file[:-4]+"']")]
 if values!=[r[field] for r in old['rows']]:raise ValueError('Picker drift')
rows=[];changed=[]
for prior in old['rows']:
 data=blob(prior['catalogue_path']);sha=hashlib.sha256(data).hexdigest();entries={e.tag+'/'+e.attrib['name'] for e in E.fromstring(data) if e.tag in ('string','plurals') and 'name' in e.attrib}
 if sha!=prior['current_catalogue_sha256']:changed.append(prior['tag'])
 if prior['pending_catalogue_sha256'] and sha!=prior['pending_catalogue_sha256']:raise ValueError('Pending content mismatch')
 row={k:prior[k] for k in ('order','tag','picker_label','catalogue_path')};row.update(current_catalogue_sha256=sha,current_explicit_priority_presence={t:dict(present=len(ks&entries),missing=len(ks-entries),total=len(ks)) for t,ks in keys.items()},current_review_acceptance_total=None);rows.append(row)
if set(changed)!={'en-001','eo','es-419'}:raise ValueError('Unexpected locale delta')
d=dict(source_commit=source,source_tree=tree,scope='All171 explicit source catalogues after PR225. Presence only, not linguistic acceptance or runtime fallback. Actual merge tree verified through GitHub; local reads use that exact tree object without claiming the local anchor is the merge commit. Unpublished independent candidates remain separately tracked. No stopped bulk archive resumed.',changed_catalogues_since_224=changed,rows=rows)
d['totals']={t:dict(current_present=sum(r['current_explicit_priority_presence'][t]['present'] for r in rows),current_missing=sum(r['current_explicit_priority_presence'][t]['missing'] for r in rows),denominator=len(rows)*len(keys[t])) for t in keys}
a.output.mkdir(parents=True,exist_ok=True);(a.output/'current171-source.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(d['totals']))
