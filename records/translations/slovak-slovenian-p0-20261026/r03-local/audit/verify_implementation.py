#!/usr/bin/env python3
"""Independent read-only source/value inventory audit; no Android runtime claim."""
from pathlib import Path
import collections,hashlib,json,stat,xml.dom.minidom as DOM
R=Path(__file__).resolve().parents[1];S=R/'source';B=R/'base-source'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def parse(p,canonical=False):
 root=DOM.parse(str(p)).documentElement;out={}
 for n in root.childNodes:
  if n.nodeType!=n.ELEMENT_NODE:continue
  if canonical and n.tagName!='string':continue
  key=n.getAttribute('name');need(n.tagName=='string' and key not in out,'invalid target resource')
  need(all(c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE) for c in n.childNodes),'child markup')
  out[key]={'value':''.join(c.data for c in n.childNodes),'attributes':dict(n.attributes.items())}
 return out
T=load(R/'packet/source-tree.json');base={x['path']:x for x in T['tree'] if x['type']=='blob'}
need(len(base)==1379,'base count');changes=[]
for path,e in base.items():
 raw=(B/path).read_bytes();need(git(raw)==e['sha'],'baseline blob '+path)
 for parent in (B,S):need(('100755' if (parent/path).stat().st_mode&0o111 else '100644')==e['mode'],'mode '+path)
 new=(S/path).read_bytes()
 if new!=raw:changes.append({'path':path,'change':'modified','mode':e['mode'],'old_git_blob_sha1':e['sha'],'git_blob_sha1':git(new),'sha256':sha(new),'bytes':len(new)})
for p in S.rglob('*'):
 path=str(p.relative_to(S))
 if not p.is_file() or path in base or '__pycache__' in path:continue
 b=p.read_bytes();changes.append({'path':path,'change':'added','mode':'100755' if p.stat().st_mode&0o111 else '100644','git_blob_sha1':git(b),'sha256':sha(b),'bytes':len(b)})
need(len(changes)==15,'unexpected change count')
need({x['path'] for x in changes if '/src/main/' in x['path']}=={f'Paintroid/src/main/res/values-{t}/strings.xml' for t in ('sk','sl')},'production scope expanded')
A=load(R/'approved-manifest.json');F=load(S/'tools/fixtures/current_localization/slovak_slovenian_p0_wording.json');need(sha((S/'tools/fixtures/current_localization/slovak_slovenian_p0_wording.json').read_bytes())==A['fixture_sha256'],'fixture binding')
old_colour=load(B/'Paintroid/src/test/resources/tagged-colour/expected.json');colour=load(S/'Paintroid/src/test/resources/tagged-colour/expected.json');need(set(colour)-set(old_colour)=={'sk','sl'} and len(colour)==72,'colour grain');need(all(colour[k]==v for k,v in old_colour.items()),'old colours changed')
priority=load(S/'translations/string-importance.json');p0={x.split('/')[1] for x in next(t['keys'] for t in priority['tiers'] if t['id']=='P0')};need(len(p0)==92,'P0 total')
canonical=parse(S/'Paintroid/src/main/res/values/strings.xml',canonical=True);summaries={}
for tag in ('sk','sl'):
 path=f'Paintroid/src/main/res/values-{tag}/strings.xml';old=parse(B/path);new=parse(S/path);review_path=R/'review'/f'{tag}-review.json';review=load(review_path);receipt={e['identity'].split('/')[1]:e for e in review['entries']};need(sha(review_path.read_bytes())==A['review_bindings'][tag]['review_sha256'],'review binding')
 need(len(old)==127 and len(new)==205 and len(receipt)==78,'locale grain');need(set(new)-set(old)==set(receipt)==set(F['values'])==set(A['approved_values'][tag]),'exact identities')
 for k,v in old.items():need(new[k]==v==F['preserved_values'][tag][k],'inherited '+tag+'/'+k)
 for k,e in receipt.items():
  need(new[k]=={'value':e['accepted_xml_text'],'attributes':e['attributes']},'review match');need(new[k]['value']==A['approved_values'][tag][k]['accepted_xml_text']==F['values'][k][tag],'fixture final value');need(new[k]['attributes']==canonical[k]['attributes']==F['constraints'][k][tag]['attributes'],'source attributes');need(F['values'][k]['default']==canonical[k]['value'],'source full value')
  need(e['decision'] in ('accept','revise'),'not approved');need(sha(new[k]['value'].encode())==e['accepted_value_sha256_utf8'],'review value hash')
 for k in F['held_absent']+['ui_no_resize_fits_decoder_memory']:need(k not in new,'held/P1 present')
 need(len(p0&new.keys())==87,'P0 endpoint');need(colour[tag]==new['save20_unsupported_image_colour']['value'][1:-1],'colour full text');summaries[tag]={'added':78,'inherited_preserved':127,'total':205,'P0_present':87,'P0_total':92,'review_decisions':dict(collections.Counter(e['decision'] for e in receipt.values()))}
need('listOf("pt-BR","de","ro","sk","sl")' in (S/'Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt').read_text(),'zoom decimal correction missing')
# All other blobs/modes were checked above; only declared changes are allowed.
need(not any(x['path'].startswith('translations/') for x in changes),'historical/global source changed')
report={'schema_version':1,'source_commit':A['source_commit'],'source_tree':T['sha'],'base_source_blobs_and_modes_verified':1379,'changed_files':sorted(changes,key=lambda e:e['path']),'source_file_count_after':1382,'production_kotlin_java_changed':False,'default_English_changed':False,'P1_companion_added':False,'historical_source_review_changed':False,'locale_summary':summaries,'tagged_colour':{'direct':72,'structurally_absent':99,'parent_inherited':1,'runtime_English':98},'memory_boundary':{'separate_single_key_tags':['nn','da','no','ca','ro','sk','sl'],'paired_oracle_entries':120,'paired_oracle_tags':60,'paired_oracle_unchanged':True},'global_scope':{'scoped':59,'outside':112,'unchanged':True},'runtime_test_static_review':{'new_methods':8,'existing_numeric_suite_expanded':True,'real_paths':['ImageMemoryPolicy.check','recoverEditor','AutosaveStore','ImageExporter.encode','SaveOptionsDialog','PaintCanvas.zoomLabel'],'limitations':['Android/JVM compilation and runtime were not executed by this audit.','Full host suite was already running separately and was not duplicated.','No native-human linguistic, whole-locale or layout certification.']},'findings':[{'id':'numeric-zoom-comma','severity':'test oracle bug','path':'Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt','detail':'Expanded tag loop includes sk/sl, but low-zoom literal selector omitted both from comma-decimal locales. Add both to listOf(pt-BR,de,ro) in zoom test, preserving exact2,50% expected value.','status':'corrected by implementation owner before Android execution; auditor verified final selector contains pt-BR,de,ro,sk,sl' }]}
numeric=(S/'Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt').read_text()
for tag in ('sk','sl'):
 v=F['values']['ui_d_d_pixels_2f_mp_exceeds_the_current'][tag][1:-1]
 for a,b in [('%1$d','1500'),('%2$d','2000'),('%3$.2f','3,00'),('%4$.2f','2,25')]:v=v.replace(a,b)
 need(f'if(tag=="{tag}") assertEquals('+json.dumps(v,ensure_ascii=False)+', failure.message)' in numeric,'full numeric literal differs')
for e in F['values'].values():
 for tag in ('sk','sl'):
  v=e[tag];need(v.startswith('"') and v.endswith('"') and not any(c in v[1:-1] for c in ['"',chr(92),chr(10),chr(13),chr(9)]),'simple decoder precondition')
report['runtime_test_static_review']['numeric_warning_literals_exactly_rebound_to_final_reviewed_full_values']=True
report['runtime_test_static_review']['simple_outer_quote_decoder_precondition_checked_for_all_156']=True
report['runtime_test_static_review']['zoom_finding_source_trace']=['PaintCanvas.kt:217–218 uses ui_zoom_percent_fractional for low zoom.','UiText.kt:66–69 selects resource configuration locale, not mismatched process default.','NumericDisplayLocaleTest.kt final comma-decimal selector includes both sk/sl.']
report['audit_preparation_notes']=['First DOM audit reader rejected non-string canonical plural nodes. Restricted the string lookup reader to canonical string elements; target catalogues still require strings only. No production source change.','Optional Java decimal probe was not run: jshell is absent. Zoom finding is source-static, not a claimed executed Java/Android result.']
(R/'audit/implementation-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'verified':1379,'changed':len(changes),'locales':summaries,'findings':report['findings']},indent=2))
