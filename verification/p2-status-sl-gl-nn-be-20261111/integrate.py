import copy, hashlib, json, pathlib, re, sys, unicodedata, difflib
import xml.etree.ElementTree as E
w=pathlib.Path(__file__).resolve().parent
root=w/'source'; sys.path.insert(0,str(root/'tools')); import translation_catalogues as c
p=json.loads((w/'inputs.json').read_text()); review=json.loads((w/'review.json').read_text()); values=review['final_accepted_map']
tree=json.loads((w/'base-tree.json').read_text()); entries={x['path']:x for x in tree['tree'] if x['type']=='blob'}
def gitblob(b): return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
source={n.get('name'):n for n in E.parse(c.RES/'values/strings.xml').getroot()}
tiers={k:t['id'] for t in json.loads((root/'translations/string-importance.json').read_text())['tiers'] for k in t['keys']}
plan=json.loads((w/'held-blob-plan.json').read_text());blobs=json.loads((w/'held-blobs.json').read_text())
for sha,txt in blobs.items():
 assert gitblob(txt.encode())==sha
 keys={n.get('name') for n in E.fromstring(txt)}
 for pair in plan[sha]: assert not keys&set(values[pair['tag']])
def node(n):
 n=copy.deepcopy(n);n.tail=None;return E.tostring(n,encoding='unicode')
summary={};patch=[]
for tag,accepted in values.items():
 path=root/p['paths'][tag];assert path==c.catalogue_paths()[tag]
 old=path.read_text(); assert gitblob(old.encode())==entries[p['paths'][tag]]['sha']
 before=E.fromstring(old);oldnodes={n.get('name'):node(n) for n in before};additions=[]
 for k,v in accepted.items():
  assert k not in oldnodes and k in p['missing_keys'][tag] and tiers['string/'+k]=='P2'
  assert p['source'][k]=={'text':source[k].text,'attributes':source[k].attrib}
  assert v and v==unicodedata.normalize('NFC',v) and not any(unicodedata.category(x).startswith('C') for x in v)
  assert c.placeholders(v)==c.placeholders(source[k].text)
  assert not c.android_string_errors(v) and not c.format_string_errors(v,source[k].get('formatted')!='false')
  assert any(re.search(r'R\.string\.'+re.escape(k)+r'\b',f.read_text()) for f in (root/'Paintroid/src/main/java').rglob('*.kt'))
  n=E.Element('string',source[k].attrib);n.text=v;additions.append('    '+E.tostring(n,encoding='unicode')+'\n')
 final=old.replace('</resources>',''.join(additions)+'</resources>');after=E.fromstring(final);nodes={n.get('name'):n for n in after}
 assert len(nodes)==len(after)==len(before)+len(accepted)
 assert all(node(nodes[k])==v for k,v in oldnodes.items())
 assert all(nodes[k].text==v and nodes[k].attrib==source[k].attrib for k,v in accepted.items())
 patch.extend(difflib.unified_diff(old.splitlines(True),final.splitlines(True),fromfile='a/'+p['paths'][tag],tofile='b/'+p['paths'][tag]))
 path.write_text(final);summary[tag]={'path':p['paths'][tag],'old_nodes_preserved':len(before),'new_values':len(accepted),'blob':gitblob(final.encode())}
summary['accepted_map_sha256']=hashlib.sha256(json.dumps(values,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();summary['total_new_values']=sum(map(len,values.values()))
(w/'integration.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');(w/'source.patch').write_text(''.join(patch));print(json.dumps(summary,ensure_ascii=False,indent=2))
