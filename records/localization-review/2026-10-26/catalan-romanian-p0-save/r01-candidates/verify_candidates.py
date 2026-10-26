#!/usr/bin/env python3
"""Fail-closed packet/source check; not a linguistic review or source mutation."""
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path
import xml.dom.minidom as D
PIN='05607f0d60131cc9148461ce595155d820748e4e';TREE='16ff3d877650ad4ad3198ce19007e8606fcd080a'
KEYS={'ui_your_current_image_has_unsaved_changes','ui_could_not_save_image','ui_saved','ui_export_did_not_save23','ui_save_explanation23','ui_export_explanation23','ui_share_explanation34','ui_save_and_share','ui_save_and_share_41edb4','ui_the_image_was_saved_but_android_could_not'}
HOLDS={'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png'}
TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def text(n):return ''.join(text(c) if c.nodeType==c.ELEMENT_NODE else c.data if c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE) else '' for c in n.childNodes)
def resources(p):
 root=D.parse(str(p)).documentElement;need(root.tagName=='resources','XML root');rows={}
 for n in root.childNodes:
  if n.nodeType!=n.ELEMENT_NODE:continue
  k=n.tagName+'/'+n.getAttribute('name');need(n.getAttribute('name') and k not in rows,'XML identity grain');rows[k]={'value':text(n),'attributes':dict(n.attributes.items())}
 return rows
def tokens(v):
 need('%' not in TOKEN.sub('',v),'malformed format token');return collections.Counter(TOKEN.findall(v))
def validate(source,packet):
 shared=load(packet/'shared-source-context.json');scope=load(packet/'scope-and-holds.json');terms=load(packet/'terminology-foundations.json')
 need(shared['source_commit']==scope['source_commit']==terms['source_commit']==PIN and shared['source_tree']==scope['source_tree']==TREE,'source pin')
 bindings=shared['source_bindings'];need(len(bindings)==len({x['path'] for x in bindings})==323,'source bindings inventory')
 for x in bindings:
  p=source/x['path'];b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'source byte identity');need(subprocess.check_output(['git','hash-object',str(p)],text=True).strip()==x['git_blob_sha1'],'source Git identity')
 base=resources(source/'Paintroid/src/main/res/values/strings.xml');p0=set(next(t['keys'] for t in load(source/'translations/string-importance.json')['tiers'] if t['id']=='P0'));need(len(p0)==92,'P0 denominator')
 entries=shared['entries'];need(len(entries)==10 and {x['identity'] for x in entries}=={'string/'+k for k in KEYS},'source scope');windows=0
 for x in entries:
  b=base[x['identity']];need(x['source']==b['value'] and x['attributes']==b['attributes'] and sha(x['source'].encode())==x['source_value_sha256_utf8'],'source value/attributes');need(x['identity'] in p0 and tokens(x['source'])==collections.Counter(x['placeholder_tokens']),'source tokens/priority')
  for c in x['consumer_contexts']:
   need('\n'.join((source/c['path']).read_text().splitlines()[c['start_line']-1:c['end_line']])==c['text'],'consumer window');windows+=1
 need(windows==26,'window inventory');source_entries={x['identity']:x for x in entries};hashes={}
 for tag in ['ca','ro']:
  name=tag+'-save-export-share-candidates.json';d=load(packet/name);need(d['locale']==tag and d['source_commit']==PIN and d['source_tree']==TREE and d['candidate_count']==10,'candidate pin/count')
  need(d['target_path']==f'Paintroid/src/main/res/values-{tag}/strings.xml','target identity');actual=resources(source/d['target_path']);need(len(actual)==127,'inherited count')
  for field in ['shared_source_context','existing_terminology']:
   ref=d[field];need(sha((packet/ref['file']).read_bytes())==ref['sha256'],'input file binding')
  cand=d['candidates'];need(len(cand)==10 and {x['identity'] for x in cand}=={'string/'+k for k in KEYS},'candidate identity grain');vals={}
  for x in cand:
   need(x['identity'] not in actual and x['current_target'] is None and x['absence_is_defect'] is False,'missing-only boundary');e=source_entries[x['identity']];need(x['source']==e['source'] and x['attributes']==e['attributes'] and x['source_value_sha256_utf8']==e['source_value_sha256_utf8'],'candidate source binding')
   v=x['candidate_display_text'];need(isinstance(v,str) and bool(v.strip()),'empty candidate');need(sha(v.encode())==x['candidate_value_sha256_utf8'],'candidate display hash');need(x['candidate_xml_text']=='"'+v+'"' and sha(x['candidate_xml_text'].encode())==x['candidate_xml_text_sha256_utf8'],'candidate XML encoding/hash');need(tokens(v)==tokens(e['source'])==collections.Counter(x['placeholder_tokens']),'complete format inventory')
   need(x['independent_review_status']=='pending' and x['author_uncertainties'] and x['author_semantic_qualifications'],'proposal/qualification boundary');vals[x['identity'].split('/')[1]]=v
  preserved=terms['locales'][tag]['preserved_values'];need(len(preserved)==127 and len({x['identity'] for x in preserved})==127,'foundation grain')
  for x in preserved:need(actual[x['identity']]=={'value':x['xml_text'],'attributes':x['attributes']},'inherited values/attributes')
  need(all('string/'+k not in actual for k in HOLDS),'held absence');need(set(scope['locales'][tag]['held_missing_identities'])=={'string/'+k for k in HOLDS},'held ledger');need({k:scope['locales'][tag][k] for k in ('existing_values_preserved','P0_present','P0_missing','missing_only_candidates','other_missing_outside_batch')}=={'existing_values_preserved':127,'P0_present':9,'P0_missing':83,'missing_only_candidates':10,'other_missing_outside_batch':73},'scope counts')
  labels={x['identity'].split('/')[1]:x['display_for_context'] for x in preserved}
  need(labels['save20_file_format']=='Image format','existing mixed label');need(labels['ui_save'] in vals['ui_save_explanation23'] and labels['ui_save'] in vals['ui_export_did_not_save23'] and labels['save20_title'] in vals['ui_export_did_not_save23'],'actual action labels');need(vals['ui_save_and_share']==vals['ui_save_and_share_41edb4']+'…','paired share labels');need('Base64' in vals['ui_export_explanation23'] and 'ASCII' in vals['ui_export_explanation23'] and 'Android' in vals['ui_the_image_was_saved_but_android_could_not'],'product syntax')
  hashes[name]=sha((packet/name).read_bytes())
 prod=[x for x in bindings if '/src/main/' in x['path'] and x['path'].endswith(('.kt','.java','.xml'))];need(len(prod)==322,'production scan count')
 for x in prod:
  value=(source/x['path']).read_text()
  for k in HOLDS:need(not re.search(r'(?:\bR\.string\.|@string/)'+k+r'\b',value),'held direct production consumer')
 return {'schema_version':1,'source_commit':PIN,'source_tree':TREE,'source_bindings_verified':323,'consumer_windows_verified':windows,'candidate_count':20,'per_locale':{'ca':10,'ro':10},'inherited_values_preserved':{'ca':127,'ro':127},'held_absences_per_locale':5,'production_scan_files':322,'candidate_sha256':hashes,'full_indexed_unindexed_nonargument_format_inventory_checked':True,'scope':'Data/source integrity only; this validator does not confer linguistic acceptance; consult separate review receipts. No source edits.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();result=validate(a.source_root,a.packet);a.out.mkdir(parents=True,exist_ok=True);(a.out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
