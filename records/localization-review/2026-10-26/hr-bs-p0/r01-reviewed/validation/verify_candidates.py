#!/usr/bin/env python3
"""Bounded candidate/source integrity; not linguistic acceptance. Run from evidence root."""
import argparse,collections,hashlib,json,re,sys,xml.etree.ElementTree as E
from pathlib import Path
PIN='0ebd41d4d9b665213c776f5a0479a29ecabdd243';TREE='bc5e10affc54ba2e0788c749b4b78968379596ba'
HOLDS={'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png'}
TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key '+k);d[k]=v
 return d
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def tokens(v):
 need('%' not in TOKEN.sub('',v),'malformed percent');return collections.Counter(TOKEN.findall(v))
def resources(p):
 r=E.parse(p).getroot();out={}
 for n in r:
  key=n.tag+'/'+n.get('name');need(key not in out,'duplicate resource');out[key]={'value':''.join(n.itertext()),'attributes':dict(n.attrib)}
 return out
def verify_entry(e,src):
 need(e['identity']==src['identity'] and e['source']==src['source'] and e['attributes']==src['attributes'],'canonical binding')
 v=e['proposed_xml_text'];need(isinstance(v,str) and len(v)>2 and v[0]==v[-1]=='"','empty/unwrapped Android string')
 need(not any(x in v[1:-1] for x in ['"','\\','\n','\r','\t']),'non-simple Android encoding')
 need(tokens(v)==tokens(src['source']),'complete format-token mismatch')
 need(isinstance(e['semantic_rationale'],str) and e['semantic_rationale'].strip(),'missing semantic rationale')
 need(isinstance(e['uncertainties'],list),'missing uncertainty ledger')
 return v

def verify(R,S):
 packet=R/'packet';shared=load(packet/'shared-source-context.json');terms=load(packet/'terminology-foundations.json');tree=load(R/'base-tree.json')
 need(shared['source_commit']==PIN and shared['source_tree']==tree['sha']==TREE,'source identity')
 blobs=[x for x in tree['tree'] if x['type']=='blob'];need(len(blobs)==1385 and not tree['truncated'],'full tree')
 for x in blobs:need(git((S/x['path']).read_bytes())==x['sha'],'source blob '+x['path'])
 base=resources(S/'Paintroid/src/main/res/values/strings.xml');p0=set(next(x['keys'] for x in load(S/'translations/string-importance.json')['tiers'] if x['id']=='P0'));need(len(p0)==92,'P0 denominator')
 entries=shared['entries'];source={e['identity']:e for e in entries};need(len(entries)==len(source)==78,'candidate inventory')
 windows=0
 for e in entries:
  need(base[e['identity']]=={'value':e['source'],'attributes':e['attributes']},'source entry');need(sha(e['source'].encode())==e['source_value_sha256_utf8'],'source value hash')
  for c in e['consumer_contexts']:
   need(c['text'] in (S/c['path']).read_text(),'consumer window');windows+=1
 production=[x['path'] for x in blobs if '/src/main/' in x['path'] and x['path'].endswith(('.kt','.java','.xml'))];need(len(production)==322,'production inventory')
 hits={k:[] for k in sorted(HOLDS)}
 for path in production:
  raw=(S/path).read_text()
  for k in HOLDS:
   if re.search(r'(?:\bR\.string\.|@string/)'+re.escape(k)+r'\b',raw):hits[k].append(path)
 need(not any(hits.values()),'held resource has current direct consumer')
 counts={};hashes={};groups={}
 for tag in ('hr','bs'):
  f=terms[tag];raw=(S/f['path']).read_bytes();current=resources(S/f['path']);need(raw==(R/'base-source'/f['path']).read_bytes(),'foundation file identity')
  need(len(current)==len(f['all_existing_values'])=={'hr':98,'bs':117}[tag],'inherited count');need(current=={'string/'+k:v for k,v in f['all_existing_values'].items()},'inherited values/attributes')
  need(set(source)<=p0 and not(set(source)&current.keys()),'missing-only selection');need(p0-current.keys()-set(source)=={'string/'+k for k in HOLDS}|({'string/save20_title'} if tag=='hr' else set()),'exact remaining absences')
  path=R/'drafts'/f'{tag}-candidates.json';data=load(path);need(data['locale']==tag and data['source_commit']==PIN and data['source_tree']==TREE,'candidate pin');need(data['source_context_sha256']==sha((packet/'shared-source-context.json').read_bytes()),'candidate context hash');es=data['candidates'];need(len(es)==78 and {e['identity'] for e in es}==set(source),'candidate identity grain')
  for e in es:verify_entry(e,source[e['identity']])
  counts[tag]=len(es);hashes[path.name]=sha(path.read_bytes());groups[tag]=dict(collections.Counter(source[e['identity']]['group'] for e in es))
 return {'source_commit':PIN,'source_tree':TREE,'verified_source_blobs':1385,'canonical_identities':78,'consumer_windows':windows,'production_files':len(production),'candidate_counts':counts,'candidate_sha256':hashes,'groups':groups,'preserved_values':215,'holds_per_locale':5,'held_direct_consumer_hits':hits,'qualification':'Structural/source checks only; no linguistic acceptance. Ordinary and optimized checks use explicit exceptions, not removable asserts.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--source',type=Path,required=True);a=p.parse_args();print(json.dumps(verify(a.root,a.source),ensure_ascii=False,indent=2))
