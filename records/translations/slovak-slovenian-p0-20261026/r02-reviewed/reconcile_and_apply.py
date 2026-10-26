#!/usr/bin/env python3
"""Reconcile independent full-value receipts and apply only approved missing values."""
from pathlib import Path
import argparse,collections,hashlib,json,sys,xml.etree.ElementTree as E
from xml.sax.saxutils import escape,quoteattr

def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def main(R):
 sys.path.insert(0,str(R/'validation'));from verify_candidates import verify,verify_entry,tokens
 verify(R,R/'base-source');source=load(R/'packet/shared-source-context.json');src={e['identity']:e for e in source['entries']};terms=load(R/'packet/terminology-foundations.json');approved={};counts={};bindings={}
 for tag in ('sk','sl'):
  draft_path=R/'drafts'/f'{tag}-candidates.json';draft={e['identity']:e for e in load(draft_path)['candidates']};review_path=R/'review'/f'{tag}-review.json';review=load(review_path)
  need(review['locale']==tag and review['source_commit']==source['source_commit'] and review['source_tree']==source['source_tree'],'review identity')
  for field,path in [('candidate_sha256',draft_path),('source_context_sha256',R/'packet/shared-source-context.json'),('terminology_sha256',R/'packet/terminology-foundations.json')]:need(review[field]==sha(path.read_bytes()),'review input binding '+field)
  es=review['entries'];need(len(es)==len({e['identity'] for e in es})==78 and {e['identity'] for e in es}==set(src),'review grain')
  approved[tag]={};counts[tag]=dict(collections.Counter(e['decision'] for e in es));bindings[tag]={'candidate_sha256':sha(draft_path.read_bytes()),'review_sha256':sha(review_path.read_bytes())}
  for e in es:
   key=e['identity'];old=draft[key];need(e['original_xml_text']==old['proposed_xml_text'] and e['attributes']==src[key]['attributes'],'review exact original/attribute join')
   need(e['decision'] in ('accept','revise'),'held/unapproved value; stop rather than expand');v=e['accepted_xml_text'];need(e['reason'].strip(),'missing rationale')
   need((v==e['original_xml_text'])==(e['decision']=='accept'),'decision mismatch');need(sha(v.encode())==e['accepted_value_sha256_utf8'],'final hash')
   verify_entry(dict(old,proposed_xml_text=v),src[key]);need(tokens(v)==tokens(src[key]['source']),'final tokens')
   approved[tag][key.split('/')[1]]={'accepted_xml_text':v,'attributes':e['attributes'],'decision':e['decision'],'reason':e['reason'],'qualifications':e['qualifications'],'sha256':sha(v.encode())}
 I=R/'source';preserved={};keys=set(approved['sk']);need(keys==set(approved['sl']) and len(keys)==78,'exact paired inventory')
 for tag in ('sk','sl'):
  path=f'Paintroid/src/main/res/values-{tag}/strings.xml';old=(R/'base-source'/path).read_bytes();need((I/path).read_bytes()==old,'working target changed before apply');preserved[tag]=terms['locales'][tag]['preserved_values'];need(not keys&preserved[tag].keys(),'overwrites inherited value')
  addition='\n    <!-- 78 independently reviewed missing P0 values; bounded static scope. -->\n'
  for key in sorted(keys):
   e=approved[tag][key];addition+='    <string '+' '.join(k+'='+quoteattr(v) for k,v in e['attributes'].items())+'>'+escape(e['accepted_xml_text'])+'</string>\n'
  text=old.decode();need(text.count('</resources>')==1,'resource closing element');(I/path).write_text(text.replace('</resources>',addition+'</resources>'))
  actual={n.get('name'):{'value':''.join(n.itertext()),'attributes':n.attrib} for n in E.parse(I/path).getroot()};need(len(actual)==205,'final count')
  for k,v in preserved[tag].items():need(actual[k]==v,'inherited changed '+k)
 sys.path.insert(0,str(I/'tools'));from translation_catalogues import placeholders
 values={};constraints={}
 for key in sorted(keys):
  se=src['string/'+key];values[key]={'default':se['source'],**{t:approved[t][key]['accepted_xml_text'] for t in approved}};constraints[key]={}
  for t,v in values[key].items():
   attrs=se['attributes'];constraints[key][t]={'attributes':attrs,'placeholders':dict(placeholders(v)),'child_elements':0,'formatted':attrs.get('formatted')!='false','escaped_newline_count':v.count('\\n')}
 holds=['formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png']
 fixture={'schema_version':1,'note':'Exactly78 independently reviewed missing live-consumer P0 values each in sk/sl.148 accepted unchanged;8 exact revisions. Bounded independent AI full-value/source-static review, not whole-language/native-human/runtime/layout certification. All254 inherited values unchanged.','values':values,'constraints':constraints,'preserved_values':preserved,'held_absent':holds,'single_warning_scope':{'tags':['sk','sl'],'key':'ui_assembly_source_memory_floor','historical_value':None,'unreviewed_companion':'ui_no_resize_fits_decoder_memory'}}
 f=I/'tools/fixtures/current_localization/slovak_slovenian_p0_wording.json';f.write_text(json.dumps(fixture,ensure_ascii=False,indent=2)+'\n')
 colour=I/'Paintroid/src/test/resources/tagged-colour/expected.json';d=load(colour)
 for t in approved:need(t not in d,'existing colour tag');d[t]=values['save20_unsupported_image_colour'][t][1:-1]
 colour.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 manifest={'schema_version':1,'source_commit':source['source_commit'],'source_tree':source['source_tree'],'scope_context_sha256':sha((R/'packet/shared-source-context.json').read_bytes()),'terminology_sha256':sha((R/'packet/terminology-foundations.json').read_bytes()),'review_bindings':bindings,'counts':counts,'approved_values':approved,'preserved_values':254,'held_absent_per_locale':holds,'result_per_locale':{'total':205,'P0_present':87,'P0_total':92},'fixture_sha256':sha(f.read_bytes()),'qualification':'Bounded independent AI complete-value/source-static acceptance only; no inherited/whole-language/native-human/runtime/layout acceptance.'}
 (R/'approved-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'counts':counts,'added':156,'preserved':254,'fixture_sha256':manifest['fixture_sha256']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();main(a.root)
