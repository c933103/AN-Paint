#!/usr/bin/env python3
"""Fail-closed import/format packet integrity; no linguistic acceptance or source mutation."""
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path
import xml.dom.minidom as D
PIN='6a42948a3ac7bad241d502f3b6c18ebf1c0327d8';TREE='65afa7b96a83c08e0ae08365166dec0520694356'
KEYS={'formats22_animation_message','formats22_animation_poster','formats22_animation_still','formats22_animation_title','formats22_animation_unknown','formats22_ascii_description','formats22_open_still','formats22_pdf_raster_hint','save20_gif_description','save20_invalid_name','save20_lossy_quality_description','save20_unsupported_image_colour','ui_higher_quality_usually_makes_a_larger_file_lossless'}
HOLDS={'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png'}
TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')
PRODUCTS={'formats22_animation_message':['AN Paint'],'formats22_animation_poster':['PNG'],'formats22_animation_unknown':['AN Paint'],'formats22_pdf_raster_hint':['PDF','144'],'save20_gif_description':['GIF','256'],'save20_unsupported_image_colour':['AN Paint','sRGB','PNG']}
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
 raw=p.read_bytes();need(b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper(),'XML declaration boundary')
 root=D.parseString(raw).documentElement;need(root.tagName=='resources','XML root');rows={}
 for n in root.childNodes:
  if n.nodeType!=n.ELEMENT_NODE:continue
  k=n.tagName+'/'+n.getAttribute('name');need(n.getAttribute('name') and k not in rows,'XML identity grain');rows[k]={'value':text(n),'attributes':dict(n.attributes.items())}
 return rows
def tokens(v):
 need(isinstance(v,str),'format text type');need('%' not in TOKEN.sub('',v),'malformed format token');return collections.Counter(TOKEN.findall(v))
def format_pair(source,candidate,attributes):
 # Attributes never bypass structural token checking, including formatted=false.
 need(isinstance(attributes,dict),'attribute type');need(tokens(candidate)==tokens(source),'complete format inventory')
def safe_path(root,name):
 need(isinstance(name,str) and name and not Path(name).is_absolute() and '..' not in Path(name).parts and '\\' not in name,'unsafe relative path')
 p=root/name;need(p.resolve().is_relative_to(root.resolve()),'path escapes source');return p

def validate(source,packet):
 shared=load(packet/'shared-source-context.json');scope=load(packet/'scope-and-holds.json');terms=load(packet/'terminology-foundations.json')
 original_path=packet/'scope-and-source-context.json';need(sha(original_path.read_bytes())=='9edb77995bf225493bb6dde7de0e1206de202c2589d318bf6098f57c298be04a','frozen scope input');original=load(original_path);original_entries={e['identity']:e for e in original['selected_entries']}
 need(scope['scope_count']==26 and scope['absence_implies_defect'] is False and scope['English_identical_implies_defect'] is False,'scope interpretation')
 need(scope['paused_scopes']==['PR56 never-merge','PR159 freeze','PR113 hold/retarget','Help callback/archive identity','interrupted compressed archive retry','release'],'paused scopes')
 need(scope['limits']==shared['limits']==original['qualifications'],'full original scope qualifications')
 need(shared['source_commit']==scope['source_commit']==terms['source_commit']==PIN and shared['source_tree']==scope['source_tree']==TREE,'source pin')
 bindings=shared['source_bindings'];need(isinstance(bindings,list) and len(bindings)==len({x['path'] for x in bindings})==323,'source bindings inventory')
 prod={p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file() and '/src/main/' in p.relative_to(source).as_posix() and p.suffix in ('.kt','.java','.xml')}
 need(len(prod)==322 and {x['path'] for x in bindings}==prod|{'translations/string-importance.json'},'exact production binding membership')
 for x in bindings:
  p=safe_path(source,x['path']);b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'source byte identity');need(subprocess.check_output(['git','hash-object',str(p)],text=True).strip()==x['git_blob_sha1'],'source Git identity')
  if 'url' in x:need(x['url']==f"https://github.com/c933103/AN-Paint/blob/{PIN}/{x['path']}",'binding public URL pin')
 base=resources(source/'Paintroid/src/main/res/values/strings.xml');p0=set(next(t['keys'] for t in load(source/'translations/string-importance.json')['tiers'] if t['id']=='P0'));need(len(p0)==92,'P0 denominator')
 need(base['string/formats22_at_least_frames']['value']=='at least %1$d','inexact-count fallback source')
 entries=shared['entries'];need(len(entries)==13 and {x['identity'] for x in entries}=={'string/'+k for k in KEYS},'source scope');windows=0
 for x in entries:
  need(x['semantic_notes']==original_entries[x['identity']]['semantic_notes'],'original semantic notes');b=base[x['identity']];need(x['source']==b['value'] and x['attributes']==b['attributes'] and sha(x['source'].encode())==x['source_value_sha256_utf8'],'source value/attributes');need(x['identity'] in p0 and TOKEN.findall(x['source'])==x['placeholder_tokens'],'source tokens/priority');tokens(x['source'])
  need(isinstance(x['consumer_contexts'],list) and x['consumer_context_ids']==[c['id'] for c in x['consumer_contexts']] and len(set(x['consumer_context_ids']))==len(x['consumer_context_ids']) and x['consumer_context_count']==len(x['consumer_contexts'])>0,'source context identity/count')
  for c in x['consumer_contexts']:
   need(c['path'] in prod and c['key']==x['identity'],'context path/key');need(all(type(c[k]) is int for k in ('line','start_line','end_line')),'context line types');lines=safe_path(source,c['path']).read_text().splitlines();need(1<=c['start_line']<=c['line']<=c['end_line']<=len(lines),'context range')
   need(c['id']==c['path']+':'+str(c['line']),'context ID/line');need(re.search(r'\bR\.string\.'+re.escape(x['identity'].split('/')[1])+r'\b',lines[c['line']-1]) is not None,'actual resource reference line')
   need('\n'.join(lines[c['start_line']-1:c['end_line']])==c['text'],'consumer window');need(c['url']==f"https://github.com/c933103/AN-Paint/blob/{PIN}/{c['path']}#L{c['start_line']}-L{c['end_line']}",'context public URL pin');windows+=1
 need(windows==16,'window inventory');source_entries={x['identity']:x for x in entries};hashes={}
 for tag in ['ca','ro']:
  name=tag+'-import-format-candidates.json';d=load(packet/name);need(d['locale']==tag and d['source_commit']==PIN and d['source_tree']==TREE and d['candidate_count']==13,'candidate pin/count')
  need(d['target_path']==f'Paintroid/src/main/res/values-{tag}/strings.xml','target identity');actual=resources(source/d['target_path']);need(len(actual)==137,'inherited count')
  for field,expected in [('shared_source_context','shared-source-context.json'),('existing_terminology','terminology-foundations.json')]:
   ref=d[field];need(ref['file']==expected and sha((packet/expected).read_bytes())==ref['sha256'],'input file binding')
  cand=d['candidates'];need(len(cand)==13 and {x['identity'] for x in cand}=={'string/'+k for k in KEYS},'candidate identity grain')
  for x in cand:
   need(x['identity'] not in actual and x['current_target'] is None and x['absence_is_defect'] is False,'missing-only boundary');e=source_entries[x['identity']];need(x['priority']=='P0','candidate priority');need(x['consumer_context_ids']==e['consumer_context_ids'],'candidate context binding');need(x['source']==e['source'] and x['attributes']==e['attributes'] and x['source_value_sha256_utf8']==e['source_value_sha256_utf8'],'candidate source binding')
   need(x['source_semantic_notes']==e['semantic_notes'] and set(e['semantic_notes']).issubset(x['author_semantic_qualifications']),'complete source qualification carry')
   v=x['candidate_display_text'];need(isinstance(v,str) and bool(v.strip()) and '\\' not in v and '"' not in v and not any(ord(c)<32 for c in v),'candidate Android display encoding');need(sha(v.encode())==x['candidate_value_sha256_utf8'],'candidate display hash');need(x['candidate_xml_text']=='"'+v+'"' and sha(x['candidate_xml_text'].encode())==x['candidate_xml_text_sha256_utf8'],'candidate XML encoding/hash');format_pair(e['source'],v,x['attributes']);need(x['placeholder_tokens']==e['placeholder_tokens'],'candidate token metadata')
   need(x['independent_review_status']=='pending' and isinstance(x['author_uncertainties'],list) and bool(x['author_uncertainties']) and isinstance(x['author_semantic_qualifications'],list) and bool(x['author_semantic_qualifications']),'proposal/qualification boundary')
   for product in PRODUCTS.get(x['identity'].split('/')[1],[]):
    pattern=r'(?<!\w)'+re.escape(product)+(r's?' if product=='GIF' else '')+r'(?!\w)';need(len(re.findall(pattern,v))==1,'product syntax '+product)
  preserved=terms['locales'][tag]['preserved_values'];need(len(preserved)==137 and {x['identity'] for x in preserved}==set(actual),'foundation grain')
  for x in preserved:need(actual[x['identity']]=={'value':x['xml_text'],'attributes':x['attributes']},'inherited values/attributes')
  need(all('string/'+k not in actual for k in HOLDS),'held absence');need('string/formats22_at_least_frames' not in actual,'untouched English count fallback');need(set(scope['locales'][tag]['held_missing_identities'])=={'string/'+k for k in HOLDS},'held ledger')
  need({k:scope['locales'][tag][k] for k in ('existing_values_preserved','P0_present','P0_missing','missing_only_candidates','other_missing_outside_batch')}=={'existing_values_preserved':137,'P0_present':19,'P0_missing':73,'missing_only_candidates':13,'other_missing_outside_batch':60},'scope counts');need(len(set(actual)&p0)==19,'actual P0 count')
  need(scope['locales'][tag]['other_missing_outside_batch_detail']=={'held':5,'unselected_nonheld':55} and len(scope['locales'][tag]['proposed_identities'])==13 and set(scope['locales'][tag]['proposed_identities'])=={'string/'+k for k in KEYS},'held versus unselected missingness')
  labels={x['identity'].split('/')[1]:x['display_for_context'] for x in preserved};need(labels['save20_file_format']=='Image format','existing mixed label');hashes[name]=sha((packet/name).read_bytes())
 for name in prod:
  value=(source/name).read_text()
  for k in HOLDS:need(not re.search(r'(?:\bR\.string\.|@string/)'+k+r'\b',value),'held direct production consumer')
 return {'schema_version':1,'source_commit':PIN,'source_tree':TREE,'source_bindings_verified':323,'consumer_windows_verified':windows,'candidate_count':26,'per_locale':{'ca':13,'ro':13},'inherited_values_preserved':{'ca':137,'ro':137},'held_absences_per_locale':5,'production_scan_files':322,'candidate_sha256':hashes,'full_indexed_unindexed_nonargument_format_inventory_checked':True,'actual_selected_formatted_false_values':0,'formatted_false_policy':'Never bypass format checks; synthetic helper controls test this separately.','context_path_key_line_reference_and_input_membership_checked':True,'scope':'Source/data integrity only; no linguistic/native/runtime acceptance or source edits. Consult independent complete-value review receipts.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();result=validate(a.source_root,a.packet);a.out.mkdir(parents=True,exist_ok=True);(a.out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
