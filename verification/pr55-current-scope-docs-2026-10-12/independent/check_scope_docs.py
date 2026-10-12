#!/usr/bin/env python3
"""Bounded one-time documentation review, not a source-snapshot CI gate."""
import argparse,hashlib,json,pathlib,subprocess,xml.etree.ElementTree as ET,zipfile
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--source-zip',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
old='dc1ba97dacc573ead73729297eb739ecb244dcf5';new='b6bf7626c1d7c4aef669394970046ffc89a5c877'
def require(v,m):
 if not v:raise ValueError(m)
def git(*args):return subprocess.check_output(['git',*args],cwd=a.repo)
def contents(t,p):return git('show',t+':'+p)
def tree(t):return {r.split('\t',1)[1]:r.split('\t',1)[0] for r in git('ls-tree','-r',t).decode().splitlines()}
before,after=tree(old),tree(new);require(before.keys()==after.keys(),'path additions/deletions');changed=sorted(p for p in before if before[p]!=after[p]);require(changed==['AGENTS.md','README.md','TRANSLATING.md'],'scope changed');require(git('write-tree').decode().strip()==new and not git('diff'),'checkout changed')
original='Completing the other 81 locales is outside this task.'
replacement='The current picker scope (12 October 2026) is 167 locale options: 59 scoped catalogues and 108 outside-scope catalogues with explicit English fallback for this bounded work. Completing those 108 catalogues is outside this task. These counts do not claim translation completeness or linguistic acceptance. The 81-locale scope counts in withdrawn historical audits refer to the earlier 140-choice inventory, not the current 167-option scope.'
files=[]
with zipfile.ZipFile(a.source_zip) as z:
 for path in changed:
  b=contents(old,path);c=contents(new,path);require(b.decode().count(original)==1,'old sentence is not unique');require(b.decode().replace(original,replacement).encode()==c,'unexpected documentation edit '+path);require(z.read('AN-Paint/'+path)==b,'prior actual corresponding source bytes differ '+path);files.append({'path':path,'before_sha256':hashlib.sha256(b).hexdigest(),'after_sha256':hashlib.sha256(c).hexdigest(),'included_in_prior_matching_source_zip':True})
root=ET.fromstring(contents(new,'Paintroid/src/main/res/values/app_language_tags.xml'));tags=[n.text for n in root.find("string-array[@name='app_language_tags']")];scope=json.loads(contents(new,'tools/fixtures/current_localization/locale_contract_scope.json'));scoped=scope['scoped_tags'];fallback=scope['fallback_tags'];require(len(tags)==len(set(tags))==167,'picker cardinality/duplicates');require(len(scoped)==len(set(scoped))==59 and len(fallback)==len(set(fallback))==108,'scope cardinality/duplicates');require(set(scoped).isdisjoint(fallback) and set(scoped)|set(fallback)==set(tags),'scope partition')
r={'status':'PASS_THREE_CURRENT_SCOPE_DOCS','base_tree':old,'candidate_tree':new,'changed_paths':changed,'unchanged_other_leaves_and_modes':len(before)-len(changed),'all_leaves':len(after),'current_scope':{'offered':167,'bounded':59,'outside':108,'exact_disjoint_union':True},'file_bindings':files,'source_zip_sha256':hashlib.sha256(a.source_zip.read_bytes()).hexdigest(),'historical_records_untouched':True,'runtime_resources_tests_workflows_fonts_unchanged':True,'limits':['Documentation-only source review; no fresh APK/Android runtime/full-suite execution claimed.','The prior matching APK/source remain e19, including their old documentation. New bundled source bytes would differ for these three Markdown files.','Current count clarification does not certify completeness/fluency or remove partial translations outside scope.']};a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
