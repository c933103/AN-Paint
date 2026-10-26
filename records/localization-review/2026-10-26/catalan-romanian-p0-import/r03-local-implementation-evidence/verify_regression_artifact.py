#!/usr/bin/env python3
"""Check terminal regression artifact identities/results without inferring skipped tests."""
from pathlib import Path
import argparse,zipfile,xml.etree.ElementTree as E,json,hashlib,re
p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--head',required=True);p.add_argument('--tested-commit',required=True);p.add_argument('--run-id',type=int,required=True);p.add_argument('--artifact-id',type=int,required=True);p.add_argument('--sha256',required=True);a=p.parse_args()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def h(b):return hashlib.sha256(b).hexdigest()
r=a.directory;archive=r/'regression-and-lint.zip';need(h(archive.read_bytes())==a.sha256,'artifact digest');z=zipfile.ZipFile(archive);names=z.namelist();need(len(names)==len(set(names)),'duplicate ZIP members');files=[n for n in names if '/test-results/' in n and n.split('/')[-1].startswith('TEST-') and n.endswith('.xml')];need(bool(files),'no JUnit XML')
totals={k:0 for k in ['tests','failures','errors','skipped']};cases=[];focused=[]
classes=['CatalanRomanianImportWordingTest','CatalanRomanianSaveWordingTest','DanishNorwegianP0Test','NynorskRemainingP0Test','NynorskSaveWordingTest','DerivedExportStateTest','ImportSelectionTitleTest','TaggedColourImportTest']
for n in files:
 doc=E.fromstring(z.read(n));need(doc.tag=='testsuite','JUnit root')
 for k in totals:
  declared_count=int(doc.get(k,0));need(declared_count>=0,'negative JUnit count');totals[k]+=declared_count
 tests=doc.findall('testcase');need(len(tests)==int(doc.get('tests')),'JUnit declared tests');need(all(t.get('classname') and t.get('name') for t in tests),'missing JUnit case identity');cases.extend((t.get('classname'),t.get('name')) for t in tests)
 for category,child in [('failures','failure'),('errors','error'),('skipped','skipped')]:need(sum(t.find(child) is not None for t in tests)==int(doc.get(category,0)),'JUnit declared/status mismatch '+category)
 matched=[cls for cls in classes if n.endswith('.'+cls+'.xml')]
 if matched:
  cls=matched[0];source=a.source_root/f'Paintroid/src/test/java/org/catrobat/paintroid/local/{cls}.kt';source_text=source.read_text();declared=set(re.findall(r'@Test\s+(?:@[\w.]+(?:\([^()]*\))?\s+)*fun\s+([A-Za-z0-9_]+)\s*\(',source_text));need(len(declared)==len(re.findall(r'@Test\b',source_text)),'unparsed focused source test '+cls);actual={t.get('name') for t in tests}
  need(declared and declared==actual,'focused source/method inventory differs '+cls)
  need(all(not list(t) for t in tests),'focused skipped/failed method '+cls)
  focused.append({'class':cls,'source_test_methods':len(declared),'artifact_path':n,'xml_sha256':h(z.read(n)),'cases':[{'classname':t.get('classname'),'name':t.get('name'),'seconds':t.get('time'),'passed':not list(t)} for t in tests]})
need(totals['failures']==totals['errors']==totals['skipped']==0,'JUnit failure/error/skip');need(len(cases)==len(set(cases)),'duplicate JUnit identity');need(len(focused)==len(classes),'missing focused suite')
lint=E.fromstring(z.read('app/build/reports/lint-results-debug.xml'));issues=lint.findall('issue');python=z.read('build/reports/ci-phases/python.log').decode();matches=re.findall(r'\nRan (\d+) tests in ([0-9.]+)s\n\nOK(?: \(skipped=(\d+)\))?\n',python);need(len(matches)==1,'ambiguous/missing Python terminal success');count,seconds,skipped=matches[0];count=int(count);skipped=int(skipped or 0);need(0<=skipped<=count and count>0,'invalid Python counts')
phases={}
for phase in ['python','jvm','native','lint']:
 raw=z.read('build/reports/ci-phases/'+phase+'.time');matches=re.findall(r'^exit_status=(\d+)$',raw.decode(),re.M);need(matches==['0'],'phase failure/ambiguous receipt '+phase);phases[phase]={'exit_code':0,'receipt_sha256':h(raw)}
out={'schema_version':1,'run_id':a.run_id,'artifact_id':a.artifact_id,'artifact_sha256':a.sha256,'reviewed_head':a.head,'tested_commit':a.tested_commit,'junit_files':len(files),'junit_totals':totals,'unique_junit_identities':len(cases),'focused_suites':focused,'hosted_python':{'run':count,'passed':count-skipped,'skipped':skipped,'seconds':float(seconds),'raw_log_sha256':h(z.read('build/reports/ci-phases/python.log')),'skipped_identities':'Not named in non-verbose hosted terminal summary; not guessed from source or local results.' if skipped else 'none'},'lint_issues':len(issues),'lint_severities':sorted({x.get('severity') for x in issues}),'phase_receipts':phases,'limits':'Hosted JVM/resources/lint results; not native-human, physical-device, whole-language or release acceptance. API35 is a separate artifact.'}
(r/'hosted-regression-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'junit_files':len(files),'junit':totals,'focused_suites':[(f['class'],f['source_test_methods']) for f in focused],'hosted_python':out['hosted_python'],'lint_issues':len(issues)},indent=2))
