from pathlib import Path
import subprocess,time,json,re,sys,hashlib
repo=Path('/workspace/shared/anpaint-pr55-reviewability-migration-20261012')
out=Path(__file__).parent
expected='592a60877524c5c118695cb45a4d0d5cd257b25a'
mode=sys.argv[1]
if mode not in ('ordinary','optimized'):raise SystemExit('unknown mode')
def clean():
 tree=subprocess.check_output(['git','write-tree'],cwd=repo,text=True).strip()
 if tree!=expected:raise RuntimeError('staged source tree changed')
 subprocess.run(['git','diff','--exit-code'],cwd=repo,check=True,stdout=subprocess.DEVNULL)
 if subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=repo,text=True).strip():raise RuntimeError('untracked source files')
 return tree
before=clean()
command=['timeout','--kill-after=5s','240s',sys.executable]+(['-O'] if mode=='optimized' else [])+['-m','unittest','discover','-s','tools','-p','test_*.py','-v']
start=time.monotonic();log=out/f'final-host-{mode}.log'
with log.open('w') as stream:
 process=subprocess.run(command,cwd=repo,stdout=stream,stderr=subprocess.STDOUT)
elapsed=time.monotonic()-start
after=clean();text=log.read_text();summaries=re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$',text,re.M)
receipt={'source_tree_before':before,'source_tree_after':after,'mode':mode,'command':command,'timeout_seconds':240,'exit_code':process.returncode,'elapsed_seconds':round(elapsed,3),'unittest_summaries':[{'tests':int(n),'seconds':float(s)} for n,s in summaries],'unittest_terminal_lines':re.findall(r'^(?:OK(?: \(.*\))?|FAILED \(.*\))$',text,re.M),'failure_status_lines':re.findall(r'^test_.*\.\.\. (?:FAIL|ERROR)$',text,re.M),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'log_bytes':log.stat().st_size,'android_local':'UNRUN: Android SDK unavailable'}
(out/f'final-host-{mode}.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2));raise SystemExit(process.returncode)
