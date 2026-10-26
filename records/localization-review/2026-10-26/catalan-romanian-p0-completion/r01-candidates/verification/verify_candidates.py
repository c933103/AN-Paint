#!/usr/bin/env python3
"""Fail-closed 110-value CA/RO source/candidate packet integrity; not acceptance."""
import argparse,collections,hashlib,json,re
from pathlib import Path
import xml.dom.minidom as D
PIN='ce796879f4568a27b9d905a8e8db639dd0a93a30'
TREE='f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c'
SCOPE_SHA256='8dd3dd99b633bbec8254639797ddc81000ce4d8bfa9c037503663123587399d5'
CORRECTION_SHA256='dde96f00968bc1009582f541524c8645b3e744dbb3c7076f2b29898be3a61225'
GROUPS={2: {'ui_autosave_pixels_are_missing', 'ui_draft_restored', 'ui_the_previous_draft_could_not_be_moved_to', 'ui_autosave_paused_use_save', 'ui_unexpected_data_in_the_undo_cache', 'ui_export_recovery_copy_144b8a', 'ui_cannot_create_the_undo_cache_free_some_device', 'ui_autosave_metadata_is_missing', 'ui_previous_draft_kept_for_recovery', 'ui_the_previous_draft_needs_more_memory_to_reopen', 'ui_could_not_export_the_recovery_copy', 'ui_autosave_failed_use_save', 'ui_draft_not_saved_yet', 'ui_a_separate_recovery_copy_has_been_kept_use', 'ui_autosave_image_encoding_failed', 'ui_draft_saved', 'ui_invalid_autosave_metadata', 'ui_autosave_selection_encoding_failed', 'ui_autosave_pixels_could_not_be_read', 'ui_the_previous_draft_could_not_be_preserved_separately', 'ui_autosave_is_paused_to_protect_that_draft_use', 'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_the_undo_cache_is_damaged', 'ui_history_unavailable34', 'ui_the_draft_is_saving_try_again_shortly', 'ui_the_previous_draft_could_not_be_restored', 'ui_export_recovery_copy', 'ui_recovered_image'}, 3: {'ui_the_saved_assembly_could_not_be_opened', 'ui_keeps_pixels_at_the_top_left_smaller_canvas', 'ui_could_not_save_the_assembly', 'ui_assembly_saved', 'ui_could_not_store_the_assembly', 'ui_d_d_pixels_2f_mp_exceeds_the_current', 'ui_not_enough_memory_for_this_operation_the_assembly', 'ui_clear_image', 'ui_sampled_resize_memory_explanation', 'ui_resize_large_image', 'ui_save_png', 'ui_the_trim_would_remove_the_entire_image', 'ui_clear_all', 'ui_assembly_source_memory_floor', 'ui_an_assembly_source_image_is_missing', 'ui_there_is_not_enough_memory_for_this_operation'}, 4: {'ui_not_enough_memory_to_save_in_this_format', 'ui_the_encoder_did_not_finish', 'save20_encoding_budget', 'legacy_credits_unreadable', 'ui_could_not_open_image', 'ui_this_location_is_not_writable', 'gallery_credit_too_large', 'gallery_credit_could_not_save', 'ui_the_selected_location_is_not_writable', 'save20_destination_error', 'ui_png_encoding_failed'}}
AUTHOR_SHA256={'author-proposals/ca-group-02-recovery.json': '24f47c7f55ba8c445ba93557d4e4b37f062db3aec9f85c0287fd17a9fc61b1f3', 'author-proposals/ca-group-03-assembly-memory.json': '77ec168499027b692cd62fa0f8aa96e5a833197bdf3059f2e22daaf386e30a45', 'author-proposals/ca-group-04-credit-destination-encoding.json': '493dfc2b1686e0d1a4efc389fd8e4ef770e5d9033dea0e38206c313d04e51beb', 'author-proposals/ro-group-02-recovery.json': 'd741ed285fce3973a57e2ced3d82662b28ab87b6d2e303fac32ba38f50409cb4', 'author-proposals/ro-group-03-assembly-memory.json': '6b52cd8919f46d68f5662625bd252de0d718b3eedc69e5f56075d3b8784c3639', 'author-proposals/ro-group-04-credit-destination-encoding.json': 'a5d0f35d4654948cdadafe2dc6bfdaa80d09ab7cdbfde9f3d4e436db304484a3'}
GROUP_NAMES={2:'recovery',3:'assembly-memory',4:'credit-destination-encoding'}
KEYS=set().union(*GROUPS.values())
HOLDS={'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png'}
TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')
LITERALS=('AN Paint','canvas.png','PNG','JPEG','ZIP','MP','×')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def git_blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def load(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def text(n):return ''.join(text(c) if c.nodeType==c.ELEMENT_NODE else c.data if c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE) else '' for c in n.childNodes)
def resources(raw):
 need(b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper(),'XML declaration boundary')
 root=D.parseString(raw).documentElement;need(root.tagName=='resources','XML root');rows={}
 for n in root.childNodes:
  if n.nodeType!=n.ELEMENT_NODE:continue
  k=n.tagName+'/'+n.getAttribute('name');need(n.getAttribute('name') and k not in rows,'XML identity grain');rows[k]={'value':text(n),'attributes':dict(n.attributes.items()),'child_elements':sum(c.nodeType==c.ELEMENT_NODE for c in n.childNodes)}
 return rows
def tokens(v):
 need(isinstance(v,str),'format text type');need('%' not in TOKEN.sub('',v),'malformed format token');return collections.Counter(TOKEN.findall(v))
def format_pair(source,candidate,attributes):
 # formatted=false never bypasses full indexed/unindexed/nonargument syntax checks.
 need(isinstance(attributes,dict),'attribute type');need(tokens(candidate)==tokens(source),'complete format inventory')
def safe_name(name):
 need(isinstance(name,str) and name and not Path(name).is_absolute() and '..' not in Path(name).parts and '\\' not in name,'unsafe relative path');return name
def safe_path(root,name):
 p=root/safe_name(name);need(p.resolve().is_relative_to(root.resolve()),'path escapes source');return p
def candidate_name(tag,group):return f'{tag}-group-{group:02d}-{GROUP_NAMES[group]}-candidates.json'
def calculate_tree(entries):
 """Derive Git root/tree identities from leaves; a forged advertised root is insufficient."""
 blobs={};declared={};directories={''}
 for e in entries:
  p=safe_name(e['path']);need(p not in blobs and p not in declared,'duplicate Git path');need(re.fullmatch('[0-9a-f]{40}',e['sha']) is not None,'Git identity syntax')
  if e['type']=='tree':need(e['mode']=='040000','tree mode');declared[p]=e['sha'];directories.add(p)
  else:
   need(e['type']=='blob' and e['mode'] in ('100644','100755'),'unsupported Git entry');blobs[p]=e
   parent=Path(p).parent
   while str(parent)!='.':directories.add(parent.as_posix());parent=parent.parent
 need(set(declared)==directories-{''},'directory inventory')
 def digest(path):
  prefix=path+'/' if path else '';children=[]
  for p,e in blobs.items():
   if p.startswith(prefix) and '/' not in p[len(prefix):]:children.append((p[len(prefix):],e['mode'],e['sha'],False))
  for p in directories:
   if p and p.startswith(prefix) and '/' not in p[len(prefix):]:children.append((p[len(prefix):],'40000',digest(p),True))
  children.sort(key=lambda x:(x[0]+('/' if x[3] else '')).encode())
  raw=b''.join(mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(identity) for name,mode,identity,_ in children)
  identity=hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  if path:need(identity==declared[path],'Git child tree identity')
  return identity
 return digest(''),blobs

def build_source(source,tree_file):
 tree=load(tree_file);need(tree['sha']==TREE and tree.get('truncated') is False,'source tree pin')
 root,blobs=calculate_tree(tree['tree']);need(root==TREE and len(blobs)==1376,'derived root/source inventory')
 raw={}
 for p,e in blobs.items():
  b=safe_path(source,p).read_bytes();need(git_blob(b)==e['sha'],'raw tracked source identity '+p);raw[p]=b
 prod={p for p in raw if '/src/main/' in p and Path(p).suffix in ('.kt','.java','.xml')}
 actual_prod={p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file() and '/src/main/' in p.relative_to(source).as_posix() and p.suffix in ('.kt','.java','.xml')}
 need(prod==actual_prod and len(prod)==322,'exact production input membership')
 refs={k:[] for k in KEYS|HOLDS}
 patterns={k:re.compile(r'(?:\bR\.string\.'+re.escape(k)+r'\b|@string/'+re.escape(k)+r'\b)') for k in refs}
 lines={p:raw[p].decode().splitlines() for p in prod}
 for p,ls in lines.items():
  for line_number,line in enumerate(ls,1):
   if 'R.string.' not in line and '@string/' not in line:continue
   for key,pat in patterns.items():
    if pat.search(line):refs[key].append({'path':p,'line':line_number,'line_text':line})
 need(all(refs[k] for k in KEYS) and all(not refs[k] for k in HOLDS),'live versus held references')
 base=resources(raw['Paintroid/src/main/res/values/strings.xml'])
 p0=set(next(t['keys'] for t in json.loads(raw['translations/string-importance.json'],object_pairs_hook=unique)['tiers'] if t['id']=='P0'));need(len(p0)==92,'P0 denominator')
 actual={tag:resources(raw[f'Paintroid/src/main/res/values-{tag}/strings.xml']) for tag in ('ca','ro')}
 need(all(len(v)==150 and len(set(v)&p0)==32 and p0-set(v)=={'string/'+k for k in KEYS|HOLDS} for v in actual.values()),'150 inherited /55 live /5 held partition')
 return {'raw':raw,'blobs':blobs,'prod':prod,'lines':lines,'refs':refs,'base':base,'p0':p0,'actual':actual,'tree_file_sha256':sha(tree_file.read_bytes())}

def validate_packet(packet,snapshot,groups=None):
 groups=tuple(GROUPS) if groups is None else tuple(groups);need(groups and len(groups)==len(set(groups)) and all(g in GROUPS for g in groups),'requested group inventory')
 scope=load(packet/'scope-and-source-context.json');terms=load(packet/'terminology-foundations.json');correction=load(packet/'source-context-correction.json')
 need(sha((packet/'source-context-correction.json').read_bytes())==CORRECTION_SHA256,'frozen correction ledger')
 need(correction['source_commit']==PIN and correction['original_scope_sha256']=='bd78a32332f1ebc00a6488a07a1bf4ab693cff78a85f9c68aed25fd4508af80f' and correction['corrected_scope_sha256']==SCOPE_SHA256 and correction['production_source_values_windows_and_bindings_unchanged'] is True,'correction lineage')
 need(sha((packet/'scope-and-source-context.json').read_bytes())==SCOPE_SHA256,'frozen corrected scope binding')
 need(scope['source_commit']==terms['source_commit']==PIN and scope['source_tree']==terms['source_tree']==TREE,'source pin')
 need(scope['full_source_blobs_verified']==1376 and scope['total_selected_locale_values']==110 and scope['unique_selected_identities']==55,'source scope counts')
 entries=scope['entries'];need(len(entries)==55 and {x['identity'] for x in entries}=={'string/'+k for k in KEYS},'source identity grain');source_entries={x['identity']:x for x in entries}
 bindings=scope['source_bindings'];need(len(bindings)==len({x['path'] for x in bindings})==22,'source binding grain')
 required={'translations/string-importance.json','Paintroid/src/main/res/values/strings.xml','Paintroid/src/main/res/values-ca/strings.xml','Paintroid/src/main/res/values-ro/strings.xml'}
 windows=0;formatted_false=[]
 for e in entries:
  key=e['identity'].split('/')[1];b=snapshot['base'][e['identity']];need(e['group'] in GROUPS and key in GROUPS[e['group']],'source semantic group')
  need(e['identity'] in snapshot['p0'] and e['source']==b['value'] and e['attributes']==b['attributes'] and b['child_elements']==0 and sha(e['source'].encode())==e['source_value_sha256_utf8'],'source complete value/attributes')
  need(e['placeholder_tokens']==TOKEN.findall(e['source']),'source token metadata');tokens(e['source'])
  if e['attributes'].get('formatted')=='false':formatted_false.append(e['identity'])
  contexts=e['consumer_contexts'];need(isinstance(contexts,list) and e['consumer_context_ids']==[c['id'] for c in contexts] and len(set(e['consumer_context_ids']))==len(contexts)==e['consumer_context_count']>0,'source context identity/count')
  need(e['absence_is_defect'] is False and e['independent_review_status']=='not reviewed for this batch','scope is not acceptance')
  need(sorted(e['all_current_direct_references'],key=lambda x:(x['path'],x['line']))==sorted(snapshot['refs'][key],key=lambda x:(x['path'],x['line'])),'full direct-reference inventory')
  for c in contexts:
   need(c['path'] in snapshot['prod'] and c['key']==e['identity'],'context path/key');required.add(c['path']);ls=snapshot['lines'][c['path']]
   need(all(type(c[k]) is int for k in ('line','start_line','end_line')) and 1<=c['start_line']<=c['line']<=c['end_line']<=len(ls),'context line/range')
   need(c['id']==c['path']+':'+str(c['line']) and any(x['path']==c['path'] and x['line']==c['line'] for x in snapshot['refs'][key]),'context ID/resource reference')
   need('\n'.join(ls[c['start_line']-1:c['end_line']])==c['text'],'consumer window');need(c['url']==f"https://github.com/c933103/AN-Paint/blob/{PIN}/{c['path']}#L{c['start_line']}-L{c['end_line']}",'consumer URL pin');windows+=1
  for ref in snapshot['refs'][key]:required.add(ref['path'])
 need(windows==98 and set(x['path'] for x in bindings)==required,'source binding membership/window inventory')
 for b in bindings:
  raw=snapshot['raw'][safe_name(b['path'])];need(b['bytes']==len(raw) and b['sha256']==sha(raw) and b['git_blob_sha1']==git_blob(raw),'source byte/Git binding');need(b['url']==f"https://github.com/c933103/AN-Paint/blob/{PIN}/{b['path']}",'source URL pin')
 need(formatted_false==['string/ui_history_unavailable34'],'actual formatted=false inventory')
 need(len(scope['held_entries'])==5 and {e['identity'] for e in scope['held_entries']}=={'string/'+k for k in HOLDS} and all(e['current_direct_reference_count']==0 for e in scope['held_entries']),'held ledger')
 need(set(terms['locales'])=={'ca','ro'} and set(scope['locale_counts'])=={'ca','ro'},'locale inventory')
 expected_files={candidate_name(tag,g) for tag in ('ca','ro') for g in GROUPS};actual_files={p.name for p in packet.glob('*-candidates.json')}
 need(actual_files<=expected_files and (actual_files==expected_files if set(groups)==set(GROUPS) else all(candidate_name(t,g) in actual_files for t in ('ca','ro') for g in groups)),'candidate file inventory')
 hashes={};candidate_total=0
 for tag in ('ca','ro'):
  counts=scope['locale_counts'][tag];need({k:counts[k] for k in ('containers_present','P0_present','P0_total','P0_missing','selected_live_consumer_missing','explicit_no_current_consumer_holds','values_to_preserve')}=={'containers_present':150,'P0_present':32,'P0_total':92,'P0_missing':60,'selected_live_consumer_missing':55,'explicit_no_current_consumer_holds':5,'values_to_preserve':150},'current structural partition')
  actual=snapshot['actual'][tag];foundation=terms['locales'][tag];preserved=foundation['values'];target_path=f'Paintroid/src/main/res/values-{tag}/strings.xml';raw=snapshot['raw'][target_path]
  need(foundation['path']==target_path and foundation['count']==150 and foundation['sha256']==sha(raw) and foundation['git_blob_sha1']==git_blob(raw),'foundation source identity')
  need(len(preserved)==150 and set(preserved)==set(actual),'foundation grain')
  for identity,x in preserved.items():need(actual[identity]['value']==x['value'] and actual[identity]['attributes']==x['attributes'] and x['value_sha256_utf8']==sha(x['value'].encode()),'inherited complete value/attributes')
  labels=foundation['composition_labels'];need(set(labels)=={'ui_menu_file','ui_save','save20_title','ui_undo','ui_resize_image','ui_resize_image_ab28be','ui_load_image','save20_file_format','ui_cancel'},'composition label inventory')
  for key,label in labels.items():
   identity='string/'+key;fallback=identity not in actual;value=(snapshot['base'] if fallback else actual)[identity];rawvalue=value['value']
   display=rawvalue[1:-1] if rawvalue.startswith('"') and rawvalue.endswith('"') else rawvalue
   need('\\' not in display,'unsupported inherited label escape')
   need(label['xml_value']==rawvalue and label['attributes']==value['attributes'] and label['display_context']==display and label['uses_default_fallback'] is fallback and label['source_path']==('Paintroid/src/main/res/values/strings.xml' if fallback else target_path) and label['value_sha256_utf8']==sha(rawvalue.encode()),'actual inherited/fallback composition label')
  for group in groups:
   keys=GROUPS[group]
   name=candidate_name(tag,group);d=load(packet/name);need(d['locale']==tag and d['source_commit']==PIN and d['source_tree']==TREE and d['group']==group and d['candidate_count']==len(keys),'candidate pin/group/count')
   need(d['target_path']==f'Paintroid/src/main/res/values-{tag}/strings.xml','target identity')
   for field,expected in [('shared_source_context','scope-and-source-context.json'),('existing_terminology','terminology-foundations.json'),('source_context_correction','source-context-correction.json')]:
    ref=d[field];need(ref['file']==expected and ref['sha256']==sha((packet/expected).read_bytes()),'candidate input binding')
   need(d.get('existing_values_preserved',150)==150 and d['existing_terminology']['values_to_preserve']==150,'candidate inherited count')
   author_ref=d['author_proposal'];author_file=f'author-proposals/{tag}-group-{group:02d}-{GROUP_NAMES[group]}.json';need(author_ref['file']==author_file and sha(safe_path(packet,author_file).read_bytes())==author_ref['sha256']==AUTHOR_SHA256[author_file],'author proposal binding');author=load(packet/author_file);authors={x['identity']:x for x in author['candidates']};need(len(authors)==len(author['candidates'])==len(keys) and set(authors)=={'string/'+k for k in keys},'author identity grain')
   need(d['record_kind']==author['record_kind'] and d.get('instructions_to_reviewer')==author.get('instructions_to_reviewer') and d['group_name']==GROUP_NAMES[group],'author review instructions/record kind/group preserved')
   cand=d['candidates'];need(len(cand)==len(keys) and {x['identity'] for x in cand}=={'string/'+k for k in keys},'candidate identity grain')
   for x in cand:
    e=source_entries[x['identity']];key=x['identity'].split('/')[1];need(x['identity'] not in actual and x['current_target'] is None and x['absence_is_defect'] is False,'missing-only boundary')
    need(x['priority']=='P0' and x['consumer_context_ids']==e['consumer_context_ids'],'candidate priority/context')
    need(x['source']==e['source'] and x['attributes']==e['attributes'] and x['source_value_sha256_utf8']==e['source_value_sha256_utf8'],'candidate source binding')
    need(x['source_semantic_notes']==e['semantic_notes'] and x['author_semantic_qualifications']==list(dict.fromkeys(e['semantic_notes']+authors[x['identity']]['author_semantic_qualifications'])),'complete semantic qualification carry')
    v=x['candidate_display_text'];need(isinstance(v,str) and v.strip() and not any(ord(c)<32 for c in v) and '\\' not in v and '"' not in v,'Android display encoding')
    need(sha(v.encode())==x['candidate_value_sha256_utf8'] and x['candidate_xml_text']=='"'+v+'"' and sha(x['candidate_xml_text'].encode())==x['candidate_xml_text_sha256_utf8'],'candidate XML/display hashes')
    node=D.parseString(('<string name="candidate">'+x['candidate_xml_text']+'</string>').encode()).documentElement;need(text(node)==x['candidate_xml_text'] and not any(c.nodeType==c.ELEMENT_NODE for c in node.childNodes),'candidate XML markup boundary')
    format_pair(e['source'],v,x['attributes']);need(x['placeholder_tokens']==e['placeholder_tokens'],'candidate token metadata')
    need(x['independent_review_status']=='pending' and isinstance(x['author_uncertainties'],list) and all(isinstance(z,str) and z.strip() for z in x['author_uncertainties']) and isinstance(x['author_semantic_qualifications'],list) and bool(x['author_semantic_qualifications']) and all(isinstance(z,str) and z.strip() for z in x['author_semantic_qualifications']),'proposal/qualification boundary')
    for literal in LITERALS:
     pat=re.compile(r'(?<!\w)'+re.escape(literal)+r'(?!\w)');need(len(pat.findall(v))==len(pat.findall(e['source'])),'product/unit syntax '+literal)
    need(all(x[field]==authors[x['identity']][field] for field in ('source','source_value_sha256_utf8','attributes','candidate_display_text','candidate_value_sha256_utf8','candidate_xml_text','candidate_xml_text_sha256_utf8','author_confidence','author_uncertainties')),'complete author target/attributes/confidence/uncertainty preserved')
    candidate_total+=1
   hashes[name]=sha((packet/name).read_bytes())
 expected_total=2*sum(len(GROUPS[g]) for g in groups);need(candidate_total==expected_total,'total selected-group candidate count')
 return {'schema_version':1,'source_commit':PIN,'source_tree':TREE,'derived_git_root_verified':True,'tracked_source_blobs_verified':1376,'source_tree_file_sha256':snapshot['tree_file_sha256'],'production_inventory_files':322,'source_bindings_verified':22,'consumer_windows_verified':98,'packet_complete':set(groups)==set(GROUPS),'groups_checked':list(groups),'expected_full_packet_count':110,'candidate_count':candidate_total,'unique_identities_checked':expected_total//2,'per_locale':{'ca':expected_total//2,'ro':expected_total//2},'per_locale_groups':{'recovery':28,'assembly_memory':16,'credit_destination_encoding':11},'inherited_values_preserved':{'ca':150,'ro':150},'held_absences_per_locale':5,'candidate_sha256':hashes,'full_indexed_unindexed_nonargument_format_inventory_checked':True,'actual_selected_formatted_false_unique_identities':formatted_false,'actual_selected_formatted_false_locale_values':2 if 2 in groups else 0,'formatted_false_policy':'No bypass; actual candidate controls and separately labelled synthetic helper controls are distinct.','scope':'Source/data integrity only; no independent linguistic/native/runtime acceptance or source edits. Full-value review remains required.'}

def validate(source,packet,tree_file,groups=None):return validate_packet(packet,build_source(source,tree_file),groups)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--tree-file',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--groups',type=int,nargs='+',choices=[2,3,4],help='Explicit partial groups; output cannot claim complete packet');a=p.parse_args();result=validate(a.source_root,a.packet,a.tree_file,a.groups);a.out.mkdir(parents=True,exist_ok=True);(a.out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
