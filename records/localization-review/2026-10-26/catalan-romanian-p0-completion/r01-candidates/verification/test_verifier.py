#!/usr/bin/env python3
"""Real packet negatives plus separately labelled synthetic source/tree/format probes."""
import argparse,copy,hashlib,json,tempfile
from pathlib import Path
from unittest.mock import patch
from xml.parsers.expat import ExpatError
import verify_candidates as v
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--tree-file',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def need(x,m):
 if not x:raise ValueError(m)
def h(b):return hashlib.sha256(b).hexdigest()
def encoded(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
snapshot=v.build_source(a.source_root,a.tree_file);positive=v.validate_packet(a.packet,snapshot);need(positive['packet_complete'] and positive['candidate_count']==110,'complete real packet')
base={p.relative_to(a.packet).as_posix():p.read_bytes() for p in a.packet.rglob('*.json')};controls=[];synthetic=[];tree_controls=[]
def change(root,name,fn):
 p=root/name;d=json.loads(p.read_bytes());fn(d);p.write_bytes(encoded(d))
def edit_text(x,value):x.update(candidate_display_text=value,candidate_value_sha256_utf8=h(value.encode()),candidate_xml_text='"'+value+'"',candidate_xml_text_sha256_utf8=h(('"'+value+'"').encode()))
def candidate(root,tag,group,fn,key=None):
 def edit(d):
  e=next(x for x in d['candidates'] if x['identity']=='string/'+key) if key else d['candidates'][0];fn(e)
 change(root,v.candidate_name(tag,group),edit)
def refresh(root,field,name):
 digest=h((root/name).read_bytes())
 for tag in ('ca','ro'):
  for group in v.GROUPS:change(root,v.candidate_name(tag,group),lambda d:d[field].__setitem__('sha256',digest))
def run(label,fn,refresh_terms=False,rebound_scope=False,expected=None):
 with tempfile.TemporaryDirectory() as td:
  root=Path(td)
  for name,b in base.items():p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  fn(root)
  if refresh_terms:refresh(root,'existing_terminology','terminology-foundations.json')
  scope_hash=v.SCOPE_SHA256;correction_hash=v.CORRECTION_SHA256
  if rebound_scope:
   scope_hash=h((root/'scope-and-source-context.json').read_bytes());change(root,'source-context-correction.json',lambda d:d.__setitem__('corrected_scope_sha256',scope_hash));correction_hash=h((root/'source-context-correction.json').read_bytes());refresh(root,'shared_source_context','scope-and-source-context.json');refresh(root,'source_context_correction','source-context-correction.json')
  try:
   # Only these explicit structural controls update trusted scope hashes, ensuring
   # actual context guards—not merely an obsolete checksum—reject the mutation.
   with patch.object(v,'SCOPE_SHA256',scope_hash),patch.object(v,'CORRECTION_SHA256',correction_hash):v.validate_packet(root,snapshot)
  except (ValueError,KeyError,TypeError,IndexError,OSError,ExpatError) as e:
   if expected:need(expected in str(e),'wrong rejecting guard for '+label+': '+str(e))
   controls.append({'case':label,'outcome':'rejected','guard':(type(e).__name__+' during required packet input read') if isinstance(e,OSError) else str(e),'refreshed_scope_bindings_for_structural_probe':rebound_scope});return
  raise ValueError('Accepted negative control: '+label)
suffixes=[' %s',' %d',' %.2f',' %1$s',' %%',' %n',' %',' %q',' %1$',' %.',' %3$.',' %3$.f',' %t']
for tag in ('ca','ro'):
 for group,key in [(2,'ui_history_unavailable34'),(3,'ui_clear_all'),(4,'ui_could_not_open_image')]:
  name=v.candidate_name(tag,group)
  for suffix in suffixes:
   run(f'{tag} group{group} actual'+(' formatted=false' if group==2 else '')+' refreshed-hash token '+repr(suffix),lambda r,tag=tag,group=group,key=key,suffix=suffix:candidate(r,tag,group,lambda x:edit_text(x,x['candidate_display_text']+suffix),key),expected='format')
  for label,fn in [
   ('missing value',lambda d:d['candidates'].pop()),
   ('duplicate value',lambda d:d['candidates'].__setitem__(1,copy.deepcopy(d['candidates'][0]))),
   ('wrong locale',lambda d:d.__setitem__('locale','nn')),
   ('wrong source pin',lambda d:d.__setitem__('source_commit','0'*40)),
   ('wrong tree',lambda d:d.__setitem__('source_tree','0'*40)),
   ('wrong group',lambda d:d.__setitem__('group',1)),
   ('wrong target',lambda d:d.__setitem__('target_path','Paintroid/src/main/res/values/strings.xml')),
   ('false record acceptance',lambda d:d.__setitem__('record_kind','native accepted')),
   ('changed reviewer instruction',lambda d:d['instructions_to_reviewer'].pop() if 'instructions_to_reviewer' in d else d.__setitem__('instructions_to_reviewer',['fabricated instruction'])),
   ('wrong preserved count',lambda d:d['existing_terminology'].__setitem__('values_to_preserve',0)),
   ('unsafe input ref',lambda d:d['shared_source_context'].__setitem__('file','../scope-and-source-context.json')),
   ('unsafe original proposal ref',lambda d:d['author_proposal'].__setitem__('file','../proposal.json'))]:
   run(f'{tag} group{group} '+label,lambda r,name=name,fn=fn:change(r,name,fn))
  for label,fn in [
   ('false missing-only',lambda x:x.__setitem__('current_target','existing')),
   ('absence implies defect',lambda x:x.__setitem__('absence_is_defect',True)),
   ('altered attribute',lambda x:x['attributes'].__setitem__('formatted','false' if x['attributes'].get('formatted')!='false' else 'true')),
   ('false priority',lambda x:x.__setitem__('priority','P1')),
   ('fabricated context',lambda x:x.__setitem__('consumer_context_ids',['invented:1'])),
   ('lost source notes',lambda x:x.__setitem__('source_semantic_notes',['wrong'])),
   ('empty qualifications',lambda x:x.__setitem__('author_semantic_qualifications',[])),
   ('added unsupported qualification',lambda x:x['author_semantic_qualifications'].append('Invented native acceptance')),
   ('duplicate qualification',lambda x:x['author_semantic_qualifications'].append(x['author_semantic_qualifications'][0])),
   ('false accepted status',lambda x:x.__setitem__('independent_review_status','accepted')),
   ('deleted uncertainty field',lambda x:x.pop('author_uncertainties')),
   ('altered uncertainty',lambda x:x.__setitem__('author_uncertainties',['invented author uncertainty'])),
   ('altered confidence',lambda x:x.__setitem__('author_confidence','native certified')),
   ('bad display hash',lambda x:x.__setitem__('candidate_value_sha256_utf8','0'*64)),
   ('bad XML hash',lambda x:x.__setitem__('candidate_xml_text_sha256_utf8','0'*64)),
   ('wrong source hash',lambda x:x.__setitem__('source_value_sha256_utf8','0'*64)),
   ('lost XML quote wrapper',lambda x:x.__setitem__('candidate_xml_text',x['candidate_display_text'])),
   ('empty target',lambda x:edit_text(x,'')),
   ('markup',lambda x:edit_text(x,'<b>'+x['candidate_display_text']+'</b>')),
   ('control character',lambda x:edit_text(x,x['candidate_display_text']+'\n')),
   ('Android escape',lambda x:edit_text(x,x['candidate_display_text']+'\\n')),
   ('ASCII quote',lambda x:edit_text(x,x['candidate_display_text']+'"'))]:
   run(f'{tag} group{group} '+label,lambda r,tag=tag,group=group,fn=fn:candidate(r,tag,group,fn))
  run(f'{tag} group{group} malformed JSON',lambda r,name=name:(r/name).write_text('{bad-json'))
  run(f'{tag} group{group} duplicate JSON key',lambda r,name=name:(r/name).write_bytes(b'{"locale":"duplicate",'+(r/name).read_bytes().lstrip()[1:]))
  run(f'{tag} group{group} missing file',lambda r,name=name:(r/name).unlink())
 for group in v.GROUPS:
  name=v.candidate_name(tag,group);d=json.loads(base[name])
  for x in d['candidates']:
   present=[z for z in v.LITERALS if z in x['source']]
   if present:
    key=x['identity'].split('/')[1];literal=present[0]
    run(f'{tag} literal {key}/{literal}',lambda r,tag=tag,group=group,key=key,literal=literal:candidate(r,tag,group,lambda e:edit_text(e,e['candidate_display_text'].replace(literal,'BROKEN')),key),expected='product/unit')
  nonempty=next((x for x in d['candidates'] if x['author_uncertainties']),None)
  if nonempty:
   key=nonempty['identity'].split('/')[1];run(f'{tag} group{group} deleted actual nonempty caveat',lambda r,tag=tag,group=group,key=key:candidate(r,tag,group,lambda x:x.__setitem__('author_uncertainties',[]),key),expected='author target/attributes/confidence/uncertainty')
 for token,replacement in [('%1$d','%1$s'),('%2$d',''),('%3$.2f','%3$.1f'),('%4$.2f','%4$f')]:
  run(tag+' indexed memory token '+token,lambda r,tag=tag,token=token,replacement=replacement:candidate(r,tag,3,lambda x:edit_text(x,x['candidate_display_text'].replace(token,replacement)),'ui_d_d_pixels_2f_mp_exceeds_the_current'),expected='format')

def scope_edit(root,fn):change(root,'scope-and-source-context.json',fn)
for label,fn,expected in [
 ('context key',lambda d:d['entries'][0]['consumer_contexts'][0].__setitem__('key','string/ui_save'),'context path/key'),
 ('context path',lambda d:d['entries'][0]['consumer_contexts'][0].__setitem__('path','translations/string-importance.json'),'context path/key'),
 ('context text',lambda d:d['entries'][0]['consumer_contexts'][0].__setitem__('text','wrong'),'consumer window'),
 ('context URL',lambda d:d['entries'][0]['consumer_contexts'][0].__setitem__('url','https://github.com/c933103/AN-Paint/blob/wrong/file'),'consumer URL'),
 ('context negative line',lambda d:d['entries'][0]['consumer_contexts'][0].__setitem__('line',-1),'context line/range'),
 ('context boolean range',lambda d:d['entries'][0]['consumer_contexts'][0].__setitem__('start_line',True),'context line/range'),
 ('context count',lambda d:d['entries'][0].__setitem__('consumer_context_count',999),'source context'),
 ('context IDs',lambda d:d['entries'][0].__setitem__('consumer_context_ids',[]),'source context'),
 ('source binding digest',lambda d:d['source_bindings'][0].__setitem__('sha256','0'*64),'source byte/Git'),
 ('source binding substitute',lambda d:d['source_bindings'][0].__setitem__('path','AGENTS.md'),'source binding membership'),
 ('source binding duplicate',lambda d:d['source_bindings'].__setitem__(1,copy.deepcopy(d['source_bindings'][0])),'source binding grain'),
 ('source value',lambda d:d['entries'][0].__setitem__('source','different'),'source complete value'),
 ('source attr',lambda d:d['entries'][0]['attributes'].__setitem__('formatted','false'),'source complete value'),
 ('source group',lambda d:d['entries'][0].__setitem__('group',1),'source semantic group'),
 ('source token metadata',lambda d:d['entries'][0].__setitem__('placeholder_tokens',['%s']),'source token metadata'),
 ('false source acceptance',lambda d:d['entries'][0].__setitem__('independent_review_status','accepted'),'scope is not acceptance'),
 ('direct consumer missing',lambda d:d['entries'][0]['all_current_direct_references'].pop(),'full direct-reference'),
 ('held entry cleared',lambda d:d['held_entries'].pop(),'held ledger'),
 ('bad locale count',lambda d:d['locale_counts']['ca'].__setitem__('P0_present',92),'current structural partition')]:
 run('rebound '+label,lambda r,fn=fn:scope_edit(r,fn),rebound_scope=True,expected=expected)
for label,fn in [('paused scope lost',lambda d:d['preserve'].pop()),('native qualification removed',lambda d:d['limits'].pop()),('forged semantic source note',lambda d:d['entries'][0]['semantic_notes'].append('Invented safety promise'))]:
 run('frozen '+label,lambda r,fn=fn:scope_edit(r,fn),expected='frozen corrected scope')
for tag in ('ca','ro'):
 for label,fn in [
  ('lost inherited value',lambda x:x['values'].pop(next(iter(x['values'])))),
  ('changed inherited value',lambda x:x['values'][next(iter(x['values']))].__setitem__('value','wrong')),
  ('changed inherited attrs',lambda x:x['values'][next(iter(x['values']))]['attributes'].__setitem__('formatted','false')),
  ('wrong foundation count',lambda x:x.__setitem__('count',0)),
  ('wrong label display',lambda x:x['composition_labels']['ui_save'].__setitem__('display_context','invented')),
  ('false inherited fallback',lambda x:x['composition_labels']['ui_load_image'].__setitem__('uses_default_fallback',False)),
  ('missing mixed label',lambda x:x['composition_labels'].pop('save20_file_format'))]:
  run(tag+' foundation '+label,lambda r,tag=tag,fn=fn:change(r,'terminology-foundations.json',lambda d:fn(d['locales'][tag])),refresh_terms=True)
run('extra locale candidate file',lambda r:(r/'nn-group-02-recovery-candidates.json').write_bytes(base[v.candidate_name('ca',2)]),expected='candidate file inventory')
run('missing correction ledger',lambda r:(r/'source-context-correction.json').unlink())
run('correction ledger silently altered',lambda r:change(r,'source-context-correction.json',lambda d:d.__setitem__('qualifications','changed')),expected='frozen correction ledger')
run('corrupted frozen author proposal',lambda r:change(r,'author-proposals/ca-group-02-recovery.json',lambda d:d['candidates'][0].__setitem__('candidate_display_text','wrong')),expected='author proposal binding')
for suffix in suffixes:
 try:v.format_pair('Safe %1$s','Safe %1$s'+suffix,{'name':'synthetic','formatted':'false'})
 except ValueError:synthetic.append({'case':'synthetic formatted=false '+repr(suffix),'outcome':'rejected'});continue
 raise ValueError('Synthetic formatted=false bypass')
v.format_pair('Safe %1$s','Traduit %1$s',{'name':'synthetic','formatted':'false'})
# These mutate only temporary tree descriptions, never production source bytes.
original_tree=v.load(a.tree_file)
def tree_negative(label,fn):
 with tempfile.TemporaryDirectory() as td:
  d=copy.deepcopy(original_tree);fn(d);p=Path(td)/'tree.json';p.write_bytes(encoded(d))
  try:v.build_source(a.source_root,p)
  except (ValueError,KeyError,TypeError,OSError) as e:tree_controls.append({'case':label,'outcome':'rejected','guard':str(e)});return
  raise ValueError('Accepted tree control '+label)
for label,fn in [
 ('advertised wrong root',lambda d:d.__setitem__('sha','0'*40)),
 ('truncated tree',lambda d:d.__setitem__('truncated',True)),
 ('missing tree member',lambda d:d['tree'].pop()),
 ('duplicate tree member',lambda d:d['tree'].append(copy.deepcopy(d['tree'][0]))),
 ('forged leaf with unchanged root',lambda d:next(x for x in d['tree'] if x['type']=='blob').__setitem__('sha','0'*40)),
 ('forged tree descendant',lambda d:next(x for x in d['tree'] if x['type']=='tree').__setitem__('sha','0'*40)),
 ('unsafe Git path',lambda d:d['tree'][0].__setitem__('path','../outside')),
 ('unsupported mode',lambda d:next(x for x in d['tree'] if x['type']=='blob').__setitem__('mode','120000'))]:tree_negative(label,fn)
# Explicitly synthetic I/O corruption verifies raw-byte binding without changing files.
original_read=Path.read_bytes;target=a.source_root/'Paintroid/src/main/res/values-ca/strings.xml'
def bad_read(path):return b'corrupted synthetic source bytes' if path==target else original_read(path)
try:
 with patch.object(Path,'read_bytes',bad_read):v.build_source(a.source_root,a.tree_file)
except ValueError as e:need('raw tracked source identity' in str(e),'raw corruption guard');tree_controls.append({'case':'synthetic source read corruption, no file changed','outcome':'rejected','guard':'raw tracked source identity'})
else:raise ValueError('Accepted corrupted raw source')
need(len({x['case'] for x in controls})==len(controls)==368,'complete packet negative inventory')
empty_uncertainty_rows=sum(not x['author_uncertainties'] for tag in ('ca','ro') for group in v.GROUPS for x in json.loads(base[v.candidate_name(tag,group)])['candidates']);need(empty_uncertainty_rows==85,'explicit empty uncertainty inventory')
a.out.mkdir(parents=True,exist_ok=True)
actual_false=[x for x in controls if 'actual formatted=false' in x['case']];need(len(actual_false)==26 and len(synthetic)==13 and len(tree_controls)==9,'format/source control inventories')
receipt={'schema_version':1,'source_commit':v.PIN,'source_tree':v.TREE,'positive_complete_packet':'passed','candidate_values':110,'packet_controls_rejected':len(controls),'packet_controls':controls,'actual_formatted_false_locale_values':2,'actual_formatted_false_refreshed_hash_negatives':len(actual_false),'synthetic_format_helper_positive':'passed','synthetic_format_helper_controls_rejected':len(synthetic),'synthetic_format_helper_controls':synthetic,'synthetic_tree_and_source_controls_rejected':len(tree_controls),'synthetic_tree_and_source_controls':tree_controls,'explicit_empty_author_uncertainty_rows_preserved':empty_uncertainty_rows,'source_files_mutated':False,'limits':['This is source/data integrity, not linguistic acceptance or Android/runtime execution.','Actual candidate format mutations use complete frozen source pairs and refreshed target hashes, including two real formatted=false locale values.','For explicitly labelled rebound structural scope probes, only expected metadata hashes are patched in the test process so actual source/context guards are exercised; no production verification flag bypass exists.','Synthetic formatted=false helper and tree/source-read corruption probes are separate from real candidate controls.','All original qualifications, explicit empty/nonempty author uncertainty lists and prior source/context correction lineage remain preserved.']}
(a.out/'mutation-controls.json').write_bytes(encoded(receipt));print(json.dumps({'packet_controls':len(controls),'actual_formatted_false_controls':len(actual_false),'synthetic_format_controls':len(synthetic),'synthetic_tree_source_controls':len(tree_controls),'receipt_sha256':h((a.out/'mutation-controls.json').read_bytes())},indent=2))
