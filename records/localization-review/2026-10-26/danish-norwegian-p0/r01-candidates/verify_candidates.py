#!/usr/bin/env python3
"""Fail-closed data/source checks only; never linguistic acceptance or source mutation."""
import argparse,collections,hashlib,json,re,subprocess,xml.dom.minidom as D
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--allow-partial',action='store_true');a=p.parse_args();P=a.packet;S=a.source_root

def need(ok,msg):
 if not ok:raise ValueError(msg)
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key: '+k);d[k]=v
 return d
def load(name):return json.loads((P/name).read_text(),object_pairs_hook=unique)
def h(b):return hashlib.sha256(b).hexdigest()
def text(n):return ''.join(text(c) if c.nodeType==c.ELEMENT_NODE else c.data if c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE) else '' for c in n.childNodes)
def resources(path):
 doc=D.parse(str(path));need(doc.documentElement.tagName=='resources','resource root');out={}
 for n in doc.documentElement.childNodes:
  if n.nodeType!=n.ELEMENT_NODE:continue
  key=n.tagName+'/'+n.getAttribute('name');need(n.getAttribute('name') and key not in out,'duplicate or missing resource name');out[key]={'text':text(n),'attributes':dict(n.attributes.items())}
 return out
def ph(s):return re.findall(r'%\d+\$(?:\.\d+)?[a-zA-Z]',s)
shared=load('shared-source-context.json');terms=load('terminology-foundations.json');scope=load('scope-and-holds.json');pin=shared['source_commit'];need(pin=='df9bc04b848ab5e99457bc67265d771bb839ec9d' and shared['source_tree']=='8ca5fc4f3989cf8c9307432d5e5c28ceef698251','source pin');need(terms['source_commit']==scope['source_commit']==pin,'mixed pins');bindings=shared['source_bindings'];need(len(bindings)==len({f['path'] for f in bindings})==323,'input inventory')
for f in bindings:
 raw=(S/f['path']).read_bytes();need(len(raw)==f['bytes'] and h(raw)==f['sha256'],'source bytes '+f['path']);actual=subprocess.check_output(['git','hash-object',str(S/f['path'])],text=True).strip();need(actual==f['git_blob_sha1'],'Git source identity '+f['path'])
base=resources(S/'Paintroid/src/main/res/values/strings.xml');priority=json.loads((S/'translations/string-importance.json').read_text(),object_pairs_hook=unique);p0=set(next(x['keys'] for x in priority['tiers'] if x['id']=='P0'));need(len(p0)==92,'P0 denominator');entries=shared['entries'];src={e['identity']:e for e in entries};need(len(src)==len(entries)==78,'source identity grain');windows=0
for e in entries:
 b=base[e['identity']];need(b['text']==e['source'] and b['attributes']==e['attributes'] and h(e['source'].encode())==e['source_value_sha256_utf8'],'canonical source/attrs');need(ph(e['source'])==e['placeholder_tokens'],'source placeholders')
 for c in e['consumer_contexts']:
  raw='\n'.join((S/c['path']).read_text().splitlines()[c['start_line']-1:c['end_line']]);need(raw==c['text'],'consumer context');windows+=1
prod=[f['path'] for f in bindings if '/src/main/' in f['path'] and f['path'].endswith(('.kt','.java','.xml'))];need(len(prod)==322,'production scan inventory');held=set(scope['locales']['da']['held_missing_identities']);need(len(held)==5 and held==set(scope['locales']['no']['held_missing_identities']),'hold inventory')
for path in prod:
 raw=(S/path).read_text()
 for identity in held:need(not re.search(r'(?:\bR\.string\.|@string/)'+re.escape(identity.split('/')[1])+r'\b',raw),'held identity now referenced')
counts={};groups={};candidate_hashes={}
for tag in ['da','no']:
 current=resources(S/terms['locales'][tag]['path']);preserved=terms['locales'][tag]['preserved_values'];need(len(current)==len(preserved)==({'da':127,'no':115}[tag]),'foundation count');need(set(current)=={e['identity'] for e in preserved},'foundation keys')
 for e in preserved:need(current[e['identity']]=={'text':e['xml_text'],'attributes':e['attributes']},'changed existing value')
 need(len(p0-current.keys())==83 and p0-current.keys()-held==set(src),'missing-only selection');seen={};groups[tag]={}
 for file in sorted(P.glob(tag+'-group-*-candidates.json')):
  d=load(file.name);need(d['locale']==tag and d['source_commit']==pin and d['source_tree']==shared['source_tree'],'candidate pin/locale');need(d['shared_source_context']['sha256']==h((P/'shared-source-context.json').read_bytes()) and d['existing_terminology']['sha256']==h((P/'terminology-foundations.json').read_bytes()),'candidate input binding');es=d['candidates'];need(len(es)==d['candidate_count'] and len({e['identity'] for e in es})==len(es),'candidate grain');expected={e['identity'] for e in entries if e['group']==d['group']};need({e['identity'] for e in es}==expected,'group scope')
  for e in es:
   key=e['identity'];need(key not in seen and key not in current and key in p0 and key not in held,'duplicate/existing/outside/held candidate');seen[key]=e;need(e['current_target'] is None and e['independent_review_status']=='pending','candidate falsely accepted/present');need(e['source']==src[key]['source'] and e['attributes']==src[key]['attributes'] and e['source_value_sha256_utf8']==src[key]['source_value_sha256_utf8'],'candidate source binding');v=e['candidate_display_text'];need(v and h(v.encode())==e['candidate_value_sha256_utf8'] and ph(v)==src[key]['placeholder_tokens'],'target hash/placeholder');need(e['candidate_xml_text']=='"'+v.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n').replace('\t','\\t')+'"' and h(e['candidate_xml_text'].encode())==e['candidate_xml_text_sha256_utf8'],'Android candidate encoding');need(e['consumer_context_ids']==src[key]['consumer_context_ids'],'context references');need(isinstance(e['author_uncertainties'],list) and isinstance(e['author_semantic_qualifications'],list),'missing uncertainty/qualification')
  groups[tag][str(d['group'])]=len(es);candidate_hashes[file.name]=h(file.read_bytes())
 counts[tag]=len(seen)
 if not a.allow_partial:need(len(seen)==78 and set(groups[tag])=={'1','2','3','4'},'incomplete candidates')
 if 'string/ui_autosave_is_paused_to_protect_that_draft_use' in seen:
  v=seen['string/ui_autosave_is_paused_to_protect_that_draft_use']['candidate_display_text'];need('Image format: PNG / JPEG' in v,'invented localized format label');need(('Filer' if tag=='da' else 'Fil') in v,'actual file menu');need(('Gem som…' if tag=='da' else 'Lagre som…') in v,'actual save-as command');need(seen['string/ui_export_recovery_copy']['candidate_display_text'] in v,'recovery command inconsistent')
 if 'string/ui_recovery_copy_exported_extract_canvas_png_from_the' in seen:
  v=seen['string/ui_recovery_copy_exported_extract_canvas_png_from_the']['candidate_display_text'];need('Load image…' in v and 'canvas.png' in v and 'ZIP' in v,'actual fallback/product syntax')
result={'schema_version':1,'source_commit':pin,'source_files_git_and_sha256_verified':len(bindings),'production_scan_files':len(prod),'source_identity_count':78,'consumer_windows_verified':windows,'candidate_counts':counts,'groups':groups,'candidate_sha256':candidate_hashes,'existing_values_preserved':{'da':127,'no':115},'held_missing_identities_per_locale':5,'all_qualifications_pending_independent_review':True,'limits':'Structural/source and composition-token checks only, not full linguistic/static semantic acceptance, runtime, native-human or layout certification.'};(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
