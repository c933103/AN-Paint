#!/usr/bin/env python3
"""One-time integration audit; no historical-source gate is added to normal CI."""
import hashlib, importlib.util, json, pathlib, subprocess, sys
R=pathlib.Path('/workspace/shared/anpaint-pr55-current-develop-20261012')
O=pathlib.Path('/workspace/shared/anpaint-pr55-direction-fixtures-20261012')
D=pathlib.Path('/workspace/shared/anpaint-sixteen-language-options-20261012')
B=pathlib.Path('/workspace/shared/anpaint-six-language-options-20261012')
OUT=pathlib.Path(__file__).parent
OLD='d2379b932cc976bb5347515887ecdfc4729ee70d'; DEV='8d4e32c937cf9ab2d1efa7ca378d20341166f492'; BASE='c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1'
def git(repo,*a):return subprocess.check_output(['git','-C',str(repo),*a])
def inv(repo,t):return {p:(m,s) for m,_,s,p in (x.split(None,3) for x in git(repo,'ls-tree','-r',t).decode().splitlines())}
def raw(repo,t,p):return git(repo,'show',t+':'+p)
def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
TREE=git(R,'write-tree').decode().strip(); require(not git(R,'diff','--name-only'),'unstaged source')
o,d,b,n=inv(O,OLD),inv(D,DEV),inv(B,BASE),inv(R,TREE)
changes=sorted(p for p in o.keys()|n.keys() if o.get(p)!=n.get(p)); incoming={p for p in b.keys()|d.keys() if b.get(p)!=d.get(p)}
extra={'CI.md','Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataHttpTranslationTest.kt','Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureTranslationTest.kt','tools/current_localization_contracts.py','tools/test_current_localization_contracts.py','tools/fixtures/current_localization/commons_copy_credit_current_wording.json','tools/fixtures/current_localization/commons_import_current_wording.json','tools/fixtures/current_localization/commons_metadata_current_wording.json','tools/fixtures/current_localization/commons_svg_current_wording.json','tools/fixtures/current_localization/help_commons_provider_current_contract.json','tools/fixtures/current_localization/locale_contract_scope.json','tools/fixtures/current_localization/wording-provenance.json','verification/README.md'}
require(set(changes)<=incoming|extra,'unrelated source change')
retired={'tools/test_commons_copy_credit_errors.py','tools/test_commons_metadata_m03.py','tools/fixtures/language_option_historical_evidence.json'}
require(not retired & n.keys(),'retired source restored')
evidence={p for p in incoming if p.startswith('verification/')}; require(len(evidence)==30 and not evidence & n.keys(),'incoming generated evidence restored')
registration={'Paintroid/src/main/res/values/app_language_names.xml','Paintroid/src/main/res/values/app_language_tags.xml','Paintroid/src/main/res/xml/app_locales.xml'}
newcat={p for p in incoming if p.startswith('Paintroid/src/main/res/values-b+')};require(len(newcat)==27,'wrong catalogue addition scope')
for p in registration|newcat|{'translations/language-options.json'}:require(n.get(p)==d[p],'accepted develop identity bytes or mode changed: '+p)
production={p for p in o if '/src/main/' in p}
for p in production-registration:require(n.get(p)==o[p],'accepted production/resource/font changed: '+p)
for p in o:
 if p in n:require(n[p][0]==o[p][0],'existing executable mode changed: '+p)
for p in n.keys()-o.keys():require(n[p][0]==d[p][0],'incoming executable mode changed: '+p)
protected=[p for p in o if p.startswith(('.github/','app/src/androidTest/','Paintroid/src/androidTest/')) or p.endswith(('.gradle','.ttf','.otf','.woff','.woff2')) or p in ['AGENTS.md','LICENSE']]
for p in protected:require(n.get(p)==o[p],'protected workflow/installed/font/licence/build changed: '+p)
for p in ('tools/run_android_instrumentation.py','tools/app_instrumentation_matrix.py','tools/installed_glyph_ink_evidence.py','tools/ci_run_timed.sh'):
 require(n.get(p)==o[p],'hard guard/deadline changed: '+p)
for p in o:
 if p.startswith('Paintroid/src/test/') and p not in incoming|extra:require(n.get(p)==o[p],'unrelated JVM rendering/lifecycle test changed: '+p)
for name in ('commons_metadata_current_wording.json','commons_copy_credit_current_wording.json','commons_svg_current_wording.json','help_commons_provider_current_contract.json'):
 p='tools/fixtures/current_localization/'+name
 require(raw(O,OLD,p).replace(b'default-plus-59-with-81-open-fallbacks',b'default-plus-59-with-108-open-fallbacks')==raw(R,TREE,p),'wording/constraint/control fixture changed: '+p)
oldscope=json.loads(raw(O,OLD,'tools/fixtures/current_localization/locale_contract_scope.json')); scope=json.loads(raw(R,TREE,'tools/fixtures/current_localization/locale_contract_scope.json'))
require(oldscope['scoped_tags']==scope['scoped_tags'],'scoped tags changed')
added=set(scope['fallback_tags'])-set(oldscope['fallback_tags']);require(len(added)==27 and len(scope['fallback_tags'])==108,'fallback scope differs')
require({p.split('values-b+')[1].split('/')[0] for p in newcat}==added,'fallback identities differ')
p='tools/fixtures/current_localization/commons_import_current_wording.json'; a=json.loads(raw(O,OLD,p));c=json.loads(raw(R,TREE,p));a['remaining_other_offered_locales']=scope['fallback_tags'];require(a==c,'import wording changed')
sys.path.insert(0,str(R/'tools'))
import translation_catalogues as cat
from run_android_instrumentation import declared_tests,source_tests_sha256
from app_instrumentation_matrix import app_partition
review=pathlib.Path('/workspace/shared/anpaint-pr55-direction-fixture-artifact-review-20261012/audit_fixture_artifacts.py')
spec=importlib.util.spec_from_file_location('discovery',review);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
mod.TREE=TREE;fresh=mod.current_inventory(R); mod.TREE=OLD;previous=mod.current_inventory(O)
(OUT/'current-jvm-inventory.json').write_text(json.dumps(fresh,indent=2)+'\n')
a=set(map(tuple,previous['expected']));c=set(map(tuple,fresh['expected'])); removed=sorted(a-c);new=sorted(c-a)
rename_prefixes={'CommonsMetadataHttpTranslationTest':('all140TagsResolve','allOfferedTagsResolve'),'CommonsMetadataResponseLimitTranslationTest':('all140TagsResolve','allOfferedTagsResolve'),'CommonsMetadataQueryFailureTranslationTest':('all140TagsResolve','allOfferedTagsResolve'),'CommonsCopyCreditTranslationTest':('remaining81OfferedTags','remainingOfferedTags'),'CommonsHelpProviderTranslationTest':('other81OfferedTags','otherOfferedTags')}
for owner,name in removed:
 before,after=rename_prefixes[owner.rsplit('.',1)[1]]
 require(name.startswith(before) and (owner,name.replace(before,after,1)) in c,'unexpected dropped JVM identity')
require(len(c)==len(a)+4,'unexpected JVM execution count delta')
installed={}
for sdk in [30,35]:
 native=declared_tests(R/'Paintroid/src/androidTest',sdk_level=sdk);app=declared_tests(R/'app/src/androidTest',sdk_level=sdk);parts=app_partition(app,sdk);selected=set().union(*parts.values());declared=declared_tests(R/'app/src/androidTest')
 installed[str(sdk)]={'native':sorted(native),'app_phases':{k:sorted(v) for k,v in parts.items()},'selected_total':len(native)+len(selected),'native_count':len(native),'app_selected_count':len(selected),'app_sdk_suppressed':sorted(declared-app),'app_explicitly_excluded':sorted(app-selected),'native_source_sha256':source_tests_sha256(R/'Paintroid/src/androidTest'),'app_source_sha256':source_tests_sha256(R/'app/src/androidTest')}
(OUT/'current-installed-inventory.json').write_text(json.dumps(installed,indent=2)+'\n')
result={'status':'PASS_SOURCE_SCOPE','tree':TREE,'ordered_publication_parents':['6d603af92ee26d852af62cd1006468ef8472bfcf','484d1b31cb113c88351e6d0dbdaa0d503e5dd834'],'published_input_trees':{'accepted_pr55':OLD,'develop':DEV},'files_changed':len(changes),'changed_files':changes,'production_files_preserved':len(production-registration),'protected_build_font_licence_workflow_installed_files':len(protected),'retired_files_not_restored':sorted(retired),'generated_evidence_not_restored':len(evidence),'scoped_count':len(scope['scoped_tags']),'fallback_count':len(scope['fallback_tags']),'added_fallback_tags':sorted(added),'current_translatable_strings':len(cat.default_resources()[2]),'current_translatable_plurals':len(cat.default_resources()[3]),'jvm_expected_previous':len(a),'jvm_expected_current':len(c),'jvm_old_identities_renamed':removed,'jvm_new_or_renamed_identities':new,'installed_expected_totals':{k:v['selected_total'] for k,v in installed.items()},'full_patch_sha256':digest((OUT/'candidate.patch').read_bytes()),'jvm_discovery_source_sha256':digest(review.read_bytes()),'limits':['Source discovery only, not Android/JVM execution.','Compilation, native/lint/APK and corresponding-source delivery binding, and installed gates remain locally unrun; no SDK is available.','Parent publishes with actual ordered parents; local HEAD is only an exact-tree review baseline.']}
(OUT/'source-scope.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
