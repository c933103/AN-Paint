"""Source/report data controls; synthetic changes never alter files or acceptance."""
import argparse,copy,json,tempfile
from pathlib import Path
from unittest.mock import patch
import recompute_delta as v
p=argparse.ArgumentParser()
for name in ('inputs','source-root','baseline-source-root','out'):p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();m=v.load_inputs(a.inputs);s=v.source_snapshot(a.source_root,a.baseline_source_root,m);positive=v.compute(m,s);controls=[]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def reject(label,fn,expected=None,scope='in-memory mutated actual report model'):
 try:fn()
 except (ValueError,KeyError,TypeError,IndexError,v.ET.ParseError) as e:
  if expected:need(expected in str(e),'wrong rejecting guard '+label+': '+str(e))
  controls.append({'case':label,'scope':scope,'result':'rejected','guard':str(e)});return
 raise ValueError('accepted negative '+label)
def model(label,fn,expected=None):
 c=copy.deepcopy(m);ss=copy.deepcopy(s);fn(c,ss);reject(label,lambda:v.compute(c,ss),expected)
for label,fn in [
 ('missing option',lambda c,s:c['rows'].pop()),
 ('duplicate option',lambda c,s:c['rows'].__setitem__(1,copy.deepcopy(c['rows'][0]))),
 ('wrong picker order',lambda c,s:c['rows'].reverse()),
 ('wrong inherited row number',lambda c,s:c['rows'][0].__setitem__('P0_present',999)),
 ('wrong baseline total',lambda c,s:c['baseline_delta']['presence_totals'].__setitem__('leaves_english_identical',0)),
 ('missing selected identity',lambda c,s:c['scope']['entries'].pop()),
 ('duplicate selected identity',lambda c,s:c['scope']['entries'].__setitem__(1,copy.deepcopy(c['scope']['entries'][0]))),
 ('cleared five-hold inventory',lambda c,s:c['approved']['preserved_holds'].pop()),
 ('missing approved value',lambda c,s:c['approved']['values'].pop()),
 ('duplicate approved value',lambda c,s:c['approved']['values'].__setitem__(1,copy.deepcopy(c['approved']['values'][0]))),
 ('false approved locale',lambda c,s:c['approved']['values'][0].__setitem__('locale','ca-ES-valencia')),
 ('false accepted verdict',lambda c,s:c['approved']['values'][0].__setitem__('verdict','hold')),
 ('wrong review source hash',lambda c,s:c['approved']['values'][0].__setitem__('source_value_sha256_utf8','0'*64)),
 ('wrong final XML value',lambda c,s:c['approved']['values'][0].__setitem__('final_xml_text','"changed"')),
 ('wrong independent receipt linkage',lambda c,s:c['approved']['values'][0].__setitem__('receipt','ro/other.json')),
 ('prior save scope removed',lambda c,s:c['prior_save']['new_review_scopes'].pop()),
 ('prior import scope removed',lambda c,s:c['prior_import']['new_review_scopes'].pop()),
 ('prior accepted hash silently altered',lambda c,s:c['prior_import']['new_review_scopes'][0].__setitem__('xml_text_sha256','0'*64)),
 ('false duplicate prior pair',lambda c,s:c['prior_import']['new_review_scopes'].__setitem__(0,copy.deepcopy(c['prior_save']['new_review_scopes'][0]))),
 ('English source substitution',lambda c,s:s['raw'].__setitem__(v.CANONICAL,s['raw'][v.CANONICAL].replace(b'Autosave failed',b'Unexpected failure',1))),
 ('inherited target value changed',lambda c,s:s['raw'].__setitem__(v.LOCALES['ca'],s['raw'][v.LOCALES['ca']].replace('Fitxer'.encode(),b'Changed',1))),
 ('new current target missing',lambda c,s:s['raw'].__setitem__(v.LOCALES['ca'],s['old'][v.LOCALES['ca']])),
]:model(label,fn)
for tag in ('ca','ro'):
 for suffix in [' %s',' %d',' %.2f',' %1$s',' %%',' %n',' %',' %q',' %1$',' %.',' %3$.',' %3$.f',' %t']:
  def edit(c,ss,tag=tag,suffix=suffix):
   x=next(e for e in c['approved']['values'] if e['locale']==tag and e['identity']=='string/ui_history_unavailable34');doc=c['receipts'][x['receipt']];verdict=next(e for e in doc['entries' if tag=='ca' else 'verdicts'] if e['identity']==x['identity'])
   display=x['final_display_text']+suffix;xml='"'+display+'"'
   for z in (x,verdict):z.update(final_display_text=display,final_value_sha256_utf8=v.sha(display.encode()),final_xml_text=xml,final_xml_text_sha256_utf8=v.sha(xml.encode()))
   root=v.ET.fromstring(ss['raw'][v.LOCALES[tag]]);node=next(n for n in root if n.get('name')=='ui_history_unavailable34');node.text=xml;ss['raw'][v.LOCALES[tag]]=v.ET.tostring(root,encoding='utf-8')
  model(tag+' actual formatted=false coherent refreshed final-token mutation '+repr(suffix),edit,'format')
# Freeze/hash checks cover metadata and qualification fields without changing real bytes.
raw_original=Path.read_bytes
for filename,edit,label in [
 ('source-head.json',lambda d:d.__setitem__('head',v.BASE_COMMIT),'wrong preview head'),
 ('source-head.json',lambda d:d.__setitem__('merged',True),'invented merge claim'),
 ('approved-manifest.json',lambda d:d.__setitem__('scope','native acceptance'),'promoted linguistic scope'),
 ('prior-save-scope-ledger.json',lambda d:d.__setitem__('global_accepted_count',99999),'invented prior global total'),
 ('packet/scope-and-source-context.json',lambda d:d['preserve'].pop(),'removed inherited pause'),
 ('review/ca/ca-group-02-recovery-independent-review.json',lambda d:d['entries'][0].__setitem__('independent_qualifications',[]),'dropped whole-value qualification'),
 ('review/ro/ro-group-02-recovery-independent-review.json',lambda d:d['verdicts'][0].__setitem__('qualifications',[]),'dropped Romanian qualification')]:
 target=a.inputs/filename;value=json.loads(target.read_bytes());edit(value);raw=(json.dumps(value,ensure_ascii=False)+'\n').encode()
 def altered(path,target=target,raw=raw):return raw if path==target else raw_original(path)
 # v.read uses read_text for semantic parse. Rebind its file-open to the same
 # patched bytes for this read-only probe; no files are overwritten.
 def check():
  with patch.object(Path,'read_bytes',altered),patch.object(v,'read',lambda path:json.loads(path.read_bytes(),object_pairs_hook=v.unique)):v.load_inputs(a.inputs)
 reject(label,check,scope='synthetic read substitution over exact input file')
for label,raw in [
 ('missing resource name',b'<resources><string>bad</string></resources>'),
 ('duplicate identity',b'<resources><string name="x">a</string><string name="x">b</string></resources>'),
 ('duplicate XML attribute',b'<resources><string name="x" name="y">a</string></resources>'),
 ('malformed XML',b'<resources><string>'),
 ('empty value',b'<resources><string name="x"/></resources>'),
 ('empty plurals',b'<resources><plurals name="x"/></resources>'),
 ('duplicate plural item',b'<resources><plurals name="x"><item quantity="one">a</item><item quantity="one">b</item></plurals></resources>'),
 ('unknown plural quantity',b'<resources><plurals name="x"><item quantity="unknown">a</item></plurals></resources>'),
 ('missing plural quantity',b'<resources><plurals name="x"><item>a</item></plurals></resources>'),
 ('entity declaration',b'<!DOCTYPE resources [<!ENTITY x "bad">]><resources><string name="x">&x;</string></resources>')]:reject(label,lambda raw=raw:v.parse(raw),scope='synthetic XML parser fixture')
reject('duplicate JSON metadata',lambda:json.loads('{"a":1,"a":2}',object_pairs_hook=v.unique),scope='synthetic JSON fixture')
for label,fn in [('truncated tree',lambda t:t.__setitem__('truncated',True)),('duplicate tree path',lambda t:t['tree'].append(copy.deepcopy(t['tree'][0]))),('wrong root',lambda t:t.__setitem__('sha','0'*40)),('forged leaf with unchanged root',lambda t:next(e for e in t['tree'] if e['type']=='blob').__setitem__('sha','0'*40)),('unsafe tree path',lambda t:t['tree'][0].__setitem__('path','../outside'))]:
 t=copy.deepcopy(m['head_tree']);fn(t);reject(label,lambda t=t:v.verify_tree(t,v.SOURCE_TREE),scope='synthetic tree metadata fixture')
need(len(controls)==len({x['case'] for x in controls})==71,'control inventory')
a.out.mkdir(parents=True,exist_ok=True);v.emit(a.out,'mutation-controls.json',{'source_commit':v.SOURCE_COMMIT,'source_tree':v.SOURCE_TREE,'source_status':v.STATUS,'positive_171_option_110_scope_preview':'passed','controls_rejected':len(controls),'actual_formatted_false_refreshed_final_pair_controls':26,'actual_formatted_false_values':2,'cases':controls,'source_files_modified':False,'limits':['All negative model, XML, tree and I/O substitutions are synthetic test mutations, not observed source defects.','The 26 refreshed final-pair probes start from two actual formatted=false locale values and are separately identified.','No acceptance, merge, CI, runtime or release gate is created by these data-integrity controls.']});print(len(controls))
