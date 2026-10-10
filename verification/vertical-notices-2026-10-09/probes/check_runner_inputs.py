#!/usr/bin/env python3
"""Exercise the runner's fail-closed input checks without compiling/executing JARs."""
from pathlib import Path
import argparse,json,os,subprocess,sys,tempfile
p=argparse.ArgumentParser(description=__doc__)
for name in ['repo','compiler-classpath','runtime-classpath','android-jars']:p.add_argument('--'+name,required=True)
a=p.parse_args();runner=Path(__file__).with_name('run.py');results=[]
with tempfile.TemporaryDirectory(prefix='vertical-notice-input-check-') as directory:
 root=Path(directory)
 def check(name,out,compiler=a.compiler_classpath,runtime=a.runtime_classpath,expected=''):
  command=[sys.executable,str(runner),'--repo',a.repo,'--out',str(out),'--compiler-classpath',compiler,'--runtime-classpath',runtime,'--android-jars',a.android_jars]
  result=subprocess.run(command,capture_output=True,text=True,timeout=20)
  assert result.returncode==2 and expected in result.stderr,(name,result.returncode,result.stderr)
  assert not (out/'logs/compile.log').exists(),'Invalid inputs must never reach compiler execution'
  results.append({'check':name,'expected_rejection':expected,'exit_code':result.returncode,'passed':True})
 occupied=root/'occupied';occupied.mkdir();(occupied/'retained.txt').write_text('must remain untouched')
 check('nonempty-output',occupied,expected='--out must be a new or empty directory')
 assert (occupied/'retained.txt').read_text()=='must remain untouched'
 check('empty-classpath-entry',root/'empty-entry',compiler=a.compiler_classpath+os.pathsep,expected='Empty classpath components are forbidden')
 paths=a.runtime_classpath.split(os.pathsep);original=Path(paths[0]);changed=root/'changed-dependency';changed.mkdir();copy=changed/original.name;copy.write_bytes(original.read_bytes()+b'\nnot the pinned dependency\n');paths[0]=str(copy)
 check('dependency-digest-mismatch',root/'wrong-digest',runtime=os.pathsep.join(paths),expected='Dependency digest mismatch')
print(json.dumps(results,indent=2))
