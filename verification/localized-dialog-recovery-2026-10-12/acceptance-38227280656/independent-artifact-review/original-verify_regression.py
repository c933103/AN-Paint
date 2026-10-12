if not __debug__:
 raise RuntimeError('Acceptance verification requires ordinary Python; optimized mode is rejected')
import argparse,collections,hashlib,json,zipfile
from pathlib import Path
import xml.etree.ElementTree as E
p=argparse.ArgumentParser();p.add_argument('artifact',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();R=Path(__file__).parent
expected_doc=json.loads((R/'checkout/verification/localized-dialog-develop-integration-2026-10-12/expected-jvm-identities.json').read_text());expected=set(map(tuple,expected_doc['expected']))
old=zipfile.ZipFile(R/'accepted-regression.zip');base=zipfile.ZipFile(R/'develop-regression.zip')
with zipfile.ZipFile(a.artifact) as z:
 xmls=[n for n in z.namelist() if '/test-results/' in n and n.endswith('.xml')];actual=[];counts=collections.Counter()
 for n in xmls:
  root=E.fromstring(z.read(n))
  for key in ['tests','errors','failures','skipped']:counts[key]+=int(root.attrib.get(key,0))
  for case in root.iter('testcase'):
   assert all(case.find(k) is None for k in ['failure','error','skipped']),(n,case.attrib)
   actual.append((case.attrib['classname'],case.attrib['name']))
 assert len(actual)==len(set(actual));assert set(actual)==expected,dict(missing=sorted(expected-set(actual)),extra=sorted(set(actual)-expected));assert counts==dict(tests=869,errors=0,failures=0,skipped=0),counts
 lint=[n for n in z.namelist() if n.endswith('lint-results-debug.xml')];assert len(lint)==1;issues=len(E.fromstring(z.read(lint[0])).findall('issue'));assert issues==0
 visuals={}
 for prefix,reference in [('localized-dialog-layout',old),('commons-metadata-m02',old),('hungarian-attribution-c05',old),('commons-metadata-m03',base)]:
  path='Paintroid/build/reports/'+prefix+'/';original={n:reference.read(n) for n in reference.namelist() if n.startswith(path) and not n.endswith('/')};current={n:z.read(n) for n in z.namelist() if n.startswith(path) and not n.endswith('/')};assert original.keys()==current.keys(),prefix
  differences=[n for n in original if original[n]!=current[n]];visuals[prefix]=dict(members=len(original),pngs=sum(n.endswith('.png') for n in original),identical_bytes=len(original)-len(differences),differences=differences)
 result=dict(artifact_sha256=hashlib.sha256(a.artifact.read_bytes()).hexdigest(),jvm=dict(counts),suites=len(xmls),unique_identities=len(actual),missing=[],extra=[],lint_issues=issues,historical_oracle_rename=expected_doc['historical_oracle_rename'],model_comparison=visuals)
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
