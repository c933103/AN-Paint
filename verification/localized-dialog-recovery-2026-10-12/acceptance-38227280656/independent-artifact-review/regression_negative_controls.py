import hashlib,json,os,pathlib,subprocess,sys,zipfile,xml.etree.ElementTree as E
R=pathlib.Path(__file__).parent
expected=json.loads((R/'checkout/verification/localized-dialog-develop-integration-2026-10-12/expected-jvm-identities.json').read_text())['expected']
root=E.Element('testsuite',tests=str(len(expected)),errors='0',failures='0',skipped='0')
for cls,name in expected:E.SubElement(root,'testcase',classname=cls,name=name)
xml=E.tostring(root)
visuals={}
for zipname,prefixes in [('accepted-regression.zip',['localized-dialog-layout','commons-metadata-m02','hungarian-attribution-c05']),('develop-regression.zip',['commons-metadata-m03'])]:
 with zipfile.ZipFile(R/zipname) as z:
  for n in z.namelist():
   if any(n.startswith('Paintroid/build/reports/'+p+'/') for p in prefixes) and not n.endswith('/'):visuals[n]=z.read(n)
firstpng=next(n for n in visuals if n.endswith('.png'))
results=[]
for case in ['positive-schema-and-identical-visuals','malformed-lint-root','negative-root-lint-issues-hidden','duplicate-visual-path','invalid-png','optimized-zero-jvm']:
 path=R/(case+'.zip')
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
  if case!='optimized-zero-jvm':z.writestr('Paintroid/build/test-results/testDebugUnitTest/TEST-synthetic.xml',xml)
  lint=b'<issues format="6" by="lint 8.13.0"/>'
  if case=='malformed-lint-root':lint=b'<not-a-lint-report/>'
  if case=='negative-root-lint-issues-hidden':lint=b'<not-a-lint-report><issues><issue severity="Error"/></issues></not-a-lint-report>'
  z.writestr('app/build/reports/lint-results-debug.xml',lint)
  for name,b in visuals.items():z.writestr(name,b'NOT A PNG' if case=='invalid-png' and name==firstpng else b)
  if case=='duplicate-visual-path':z.writestr(firstpng,visuals[firstpng])
 out=R/(case+'.json');env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 cmd=[sys.executable,*(['-O'] if case.startswith('optimized') else []),str(R/'original-verify_regression.py'),str(path),'--output',str(out)]
 run=subprocess.run(cmd,env=env,capture_output=True,text=True)
 (R/(case+'.stdout.log')).write_text(run.stdout);(R/(case+'.stderr.log')).write_text(run.stderr)
 data=json.loads(out.read_text()) if out.exists() else None
 results.append(dict(case=case,command=cmd,returncode=run.returncode,output_created=out.exists(),artifact_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),lint_issues=None if data is None else data['lint_issues'],unique_identities=None if data is None else data['unique_identities'],visual_difference_count=None if data is None else sum(len(x['differences']) for x in data['model_comparison'].values())))
print(json.dumps(results,indent=2));(R/'regression-negative-control-results.json').write_text(json.dumps(results,indent=2)+'\n')
