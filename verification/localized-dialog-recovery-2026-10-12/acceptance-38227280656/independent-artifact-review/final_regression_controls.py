import pathlib,zipfile,json,hashlib,subprocess,sys,os,xml.etree.ElementTree as E
R=pathlib.Path(__file__).parent;mapping={'2131493276':'2131493277','2131493304':'2131493305','2131493378':'2131493379'};source=zipfile.ZipFile(R/'positive-schema-and-identical-visuals.zip')
base={}
for n in source.namelist():
 name=n
 if n.startswith('Paintroid/build/reports/hungarian-attribution-c05/'):
  for a,b in mapping.items():name=name.replace('-'+a,'-'+b)
 base[name]=source.read(n)
xmlpath=next(n for n in base if '/test-results/' in n);lintpath=next(n for n in base if n.endswith('lint-results-debug.xml'));png=next(n for n in base if n.endswith('.png'));rows=[]
for case in ['positive','wrong-lint-root','nested-lint-error','duplicate-visual-path','wrong-junit-root','mismatched-junit-count','stale-output-cleared','invalid-png-is-reported']:
 values=base.copy()
 if case in ('wrong-lint-root','stale-output-cleared'):values[lintpath]=b'<not-a-lint-report/>'
 if case=='nested-lint-error':values[lintpath]=b'<issues format="6" by="lint 8.13.0"><container><issue severity="Error"/></container></issues>'
 if case in ('wrong-junit-root','mismatched-junit-count'):
  root=E.fromstring(values[xmlpath]);
  if case=='wrong-junit-root':root.tag='not-a-junit-report'
  else:root.attrib['tests']='1'
  values[xmlpath]=E.tostring(root)
 if case=='invalid-png-is-reported':values[png]=b'INVALID PNG'
 artifact=R/'final-synthetic-regression-control.zip'
 with zipfile.ZipFile(artifact,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
  for n,b in values.items():z.writestr(n,b)
  if case=='duplicate-visual-path':z.writestr(png,values[png])
 out=R/('final-regression-control-'+case+'.json');out.write_text('{"stale_success":true}')
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';cmd=[sys.executable,str(R/'final-verify_regression.py'),str(artifact),'--output',str(out)]
 run=subprocess.run(cmd,capture_output=True,text=True,env=env);(R/('final-regression-control-'+case+'.stderr.log')).write_text(run.stderr)
 data=json.loads(out.read_text()) if out.exists() else {};row=dict(case=case,exit=run.returncode,output_exists=out.exists(),visual_differences=sum(len(v['differences']) for v in data.get('model_comparison',{}).values()));rows.append(row)
 if case in ['positive','invalid-png-is-reported']:assert run.returncode==0 and out.exists()
 else:assert run.returncode!=0 and not out.exists()
record=dict(helper_sha256=hashlib.sha256((R/'final-verify_regression.py').read_bytes()).hexdigest(),controls=rows);(R/'final-regression-control-results.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
