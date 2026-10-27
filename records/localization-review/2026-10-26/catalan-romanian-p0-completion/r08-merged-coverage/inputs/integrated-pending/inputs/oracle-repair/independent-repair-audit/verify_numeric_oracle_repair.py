#!/usr/bin/env python3
"""Read-only repair scope and static oracle controls; no JVM or Android execution."""
import argparse,hashlib,json,re,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
PATH='Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt'
KEY='ui_d_d_pixels_2f_mp_exceeds_the_current'
OLD='            if(tag=="ro") assertTrue(failure.message!!.startsWith("1500 × 2000 pixels (3,00 MP)"))'
NEW='''            // Romanian now has its own reviewed warning; keep literal decimal checks
            // independent of the resource formatter and the deliberately US process locale.
            if(tag=="ro") {
                assertTrue(failure.message!!.startsWith("Dimensiunea de 1500 × 2000 pixeli (3,00 MP)"))
                assertTrue(failure.message!!.contains("2,25 MP"))
            }'''
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def static_guard(text,reviewed):
 start=text.index('@Test fun oversizeWarningUsesResourceDigitsAndDecimalsWithoutChangingAdmission()');end=text.index('@Test',start+6);body=text[start:end]
 required=['assertEquals(2_250_000L,limit.maxPixels())','limit.check(1500,1500)','val failure=assertThrows(ImageSizeException::class.java) {limit.check(1500,2000)}','assertEquals(tag,expected(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current,1500,2000,3.0,2.25),failure.message)','assertEquals(2_249_999L,limit.maxPixels(3))','assertThrows(ImageSizeException::class.java) {limit.check(1500,1500,3)}','assertThrows(IllegalArgumentException::class.java) {limit.check(0,1)}']
 for literal in required:need(literal in body,'lost admission/full-resource assertion')
 need('Locale.setDefault(if(tag=="en-001") Locale.GERMANY else Locale.US)' in text,'lost deliberate locale mismatch')
 need('String.format(activity.resources.configuration.locales[0],activity.getString(id),*args)' in text,'expected formatter is not resource-localized')
 need('"ro" to ("Current safe editing budget: 25,7 MiB' in text and 'if(tag=="ro") assertTrue(texts(dialog.window!!.decorView).any {it.startsWith("Current safe budget:")})' in text,'P1 fallback caption guards changed')
 section=body.split('if(tag=="ro") {',1)[1].split('}',1)[0]
 prefix=re.search(r'startsWith\("([^"\n]+)"\)',section);budget=re.search(r'contains\("([^"\n]+)"\)',section);need(prefix is not None and budget is not None,'Romanian literal checks absent')
 need(prefix.group(1)=='Dimensiunea de 1500 × 2000 pixeli (3,00 MP)' and budget.group(1)=='2,25 MP','wrong independent numeric literals')
 # A deterministic static template substitution, not Java/Android formatting execution.
 example=reviewed.removeprefix('"').removesuffix('"')
 for token,value in [('%1$d','1500'),('%2$d','2000'),('%3$.2f','3,00'),('%4$.2f','2,25')]:example=example.replace(token,value)
 need(example.startswith(prefix.group(1)) and budget.group(1) in example,'literal checks not backed by reviewed full value')
 return example

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.root;before=(r/'implementation-original'/PATH).read_bytes();after=(r/'implementation'/PATH).read_bytes();change=json.loads((r/'repair/oracle-change.json').read_text())
 need(sha(before)==change['before_sha256']=='60f2eb1bc220abaa2a07b04a22a8c695b3fd519cf70a4d1b649d83176ee13df3','original hash');need(sha(after)==change['after_sha256']=='042fe46517f049806541809741f54829e4844529d44ccc85697650be94fb37cf','repair hash')
 need(before.decode().count(OLD)==1 and before.decode().replace(OLD,NEW)==after.decode(),'strict minimal patch differs')
 tree=json.loads((r/'head-tree.json').read_text());entries=[e for e in tree['tree'] if e['type']=='blob'];need(len(entries)==1379,'original tree source inventory');changed=[]
 for e in entries:
  old=(r/'implementation-original'/e['path']).read_bytes();new=(r/'implementation'/e['path']).read_bytes();g=hashlib.sha1(b'blob '+str(len(old)).encode()+b'\0'+old).hexdigest();need(g==e['sha'],'original frozen source drift')
  if old!=new:changed.append(e['path'])
 need(changed==[PATH],'only numeric test may change')
 fixture=json.loads((r/'implementation/tools/fixtures/current_localization/catalan_romanian_completion_wording.json').read_text());value=fixture['values'][KEY]['ro'];review=json.loads((r/'review/ro/ro-group-03-assembly-memory-independent-review.json').read_text());entry=next(v for v in review['verdicts'] if v['identity']=='string/'+KEY)
 need(entry['verdict']=='accept' and entry['final_xml_text']==value and sha(value.encode())==entry['final_xml_text_sha256_utf8'],'review complete-value binding');source=ET.parse(r/'implementation/Paintroid/src/main/res/values-ro/strings.xml').getroot().find(f"./string[@name='{KEY}']");need(source.text==value and source.attrib==entry['attributes'],'XML full-value binding')
 example=static_guard(after.decode(),value);controls=[]
 mutations=[('old English prefix',lambda t:t.replace('Dimensiunea de 1500 × 2000 pixeli (3,00 MP)','1500 × 2000 pixels (3,00 MP)')),('US decimal for image MP',lambda t:t.replace('Dimensiunea de 1500 × 2000 pixeli (3,00 MP)','Dimensiunea de 1500 × 2000 pixeli (3.00 MP)')),('US decimal for budget MP',lambda t:t.replace('assertTrue(failure.message!!.contains("2,25 MP"))\n            }','assertTrue(failure.message!!.contains("2.25 MP"))\n            }')),('missing independent budget literal',lambda t:t.replace('                assertTrue(failure.message!!.contains("2,25 MP"))\n','')),('missing complete-resource comparison',lambda t:t.replace('assertEquals(tag,expected(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current,1500,2000,3.0,2.25),failure.message)','')),('removed process/resource mismatch',lambda t:t.replace('Locale.setDefault(if(tag=="en-001") Locale.GERMANY else Locale.US)','')),('process formatter substituted',lambda t:t.replace('String.format(activity.resources.configuration.locales[0],activity.getString(id),*args)','String.format(activity.getString(id),*args)')),('changed admission maxPixels',lambda t:t.replace('assertEquals(2_250_000L,limit.maxPixels())','assertEquals(1L,limit.maxPixels())')),('removed successful boundary admission',lambda t:t.replace('limit.check(1500,1500)\n','')),('removed oversized rejection',lambda t:t.replace('val failure=assertThrows(ImageSizeException::class.java) {limit.check(1500,2000)}','val failure=ImageSizeException("fake")')),('removed resident-pixel guard',lambda t:t.replace('assertEquals(2_249_999L,limit.maxPixels(3))','')),('removed invalid-size rejection',lambda t:t.replace('assertThrows(IllegalArgumentException::class.java) {limit.check(0,1)}','')),('translated unrelated P1 fallback caption',lambda t:t.replace('"ro" to ("Current safe editing budget: 25,7 MiB','"ro" to ("changed: 25,7 MiB'))]
 for name,fn in mutations:
  mutated=fn(after.decode());need(mutated!=after.decode(),'ineffective negative mutation')
  try:static_guard(mutated,value)
  except (ValueError,IndexError):controls.append({'case':name,'outcome':'rejected static mutation'});continue
  raise ValueError('accepted static mutation '+name)
 z=zipfile.ZipFile(r/'ci/regression-and-lint.zip');names=z.namelist();need(len(names)==len(set(names)),'duplicate artifact member');xmls=[n for n in names if '/test-results/' in n and n.rsplit('/',1)[-1].startswith('TEST-') and n.endswith('.xml')];totals={k:0 for k in ('tests','failures','errors','skipped')};failed=[];identities=[]
 for n in xmls:
  doc=ET.fromstring(z.read(n));cases=doc.findall('testcase');need(len(cases)==int(doc.get('tests')),'JUnit count')
  for k in totals:totals[k]+=int(doc.get(k,0))
  for t in cases:
   identities.append((t.get('classname'),t.get('name')))
   if t.find('failure') is not None:failed.append({'classname':t.get('classname'),'name':t.get('name'),'failure_text':t.find('failure').text})
 need(len(identities)==len(set(identities))==1366 and totals=={'tests':1366,'failures':1,'errors':0,'skipped':0},'actual original aggregate')
 need(len(failed)==1 and failed[0]['name']=='oversizeWarningUsesResourceDigitsAndDecimalsWithoutChangingAdmission' and 'NumericDisplayLocaleTest.kt:99' in failed[0]['failure_text'],'original failure identity')
 focused={}
 for cls,count in [('NumericDisplayLocaleTest',6),('CatalanRomanianCompletionWordingTest',5)]:
  raw=(r/f'ci/TEST-org.catrobat.paintroid.local.{cls}.xml').read_bytes();member=next(n for n in xmls if n.endswith('.'+cls+'.xml'));need(raw==z.read(member),'individual XML archive binding');doc=ET.fromstring(raw);need(int(doc.get('tests'))==count,'focused count');focused[cls]={'tests':count,'failures':int(doc.get('failures')),'errors':int(doc.get('errors')),'skipped':int(doc.get('skipped')),'xml_sha256':sha(raw)}
 a.out.mkdir(exist_ok=True,parents=True);out={'schema_version':1,'record_kind':'Independent static audit of original-run numeric-oracle repair','original_head':'93f27ed172cc730c80ed7a2ffbcacc1b0c04383f','original_run_id':40340230583,'new_head':None,'result':'Minimal reviewed-value oracle repair accepted within static scope; fresh CI still required','changed_path':PATH,'before_sha256':sha(before),'after_sha256':sha(after),'frozen_original_source_blobs_verified':1379,'only_one_test_file_changed':True,'production_values_and_logic_unchanged':True,'original_actual_JVM_artifact':{'archive_sha256':sha((r/'ci/regression-and-lint.zip').read_bytes()),'XML_files':len(xmls),'unique_case_identities':len(identities),'totals':totals,'failed_case':{k:v for k,v in failed[0].items() if k!='failure_text'},'failure_line':99,'focused':focused},'reviewed_Romanian_full_value_sha256':entry['final_value_sha256_utf8'],'review_receipt_sha256':sha((r/'review/ro/ro-group-03-assembly-memory-independent-review.json').read_bytes()),'source_semantics':'The already-reviewed Romanian complete warning replaces English fallback text. Full resource-locale formatted equality remains, and the deliberately mismatched US process locale cannot satisfy either independent comma-decimal literal. Memory admission, resident-pixel and invalid-size checks remain identical. Unreviewed P1 English captions are unchanged.','static_composition_example':example,'static_controls':{'positive':'reviewed template/literal/source invariants agree','negative_mutations_rejected':len(controls),'cases':controls},'original_failure_limitation':'The original failure stack also carries Robolectric unexecuted-runnables suppression. The direct failing assertion is the stale prefix; suppression is preserved as original evidence and does not establish a separate runtime fix.','limits':['No Kotlin compilation or new JVM/Android execution performed by this auditor.','Static mutation controls are not executed production regressions.','Original CI result remains failed and is never relabelled as passing.','No translation, production behavior, P1, language routing or scoped hold changed.']};dump(a.out/'numeric-oracle-repair-audit.json',out);print(json.dumps({'result':'pass static audit','negative_controls':len(controls),'receipt_sha256':sha((a.out/'numeric-oracle-repair-audit.json').read_bytes())}))
if __name__=='__main__':main()
