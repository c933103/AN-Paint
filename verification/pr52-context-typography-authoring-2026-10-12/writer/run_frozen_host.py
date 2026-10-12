"""Temporary bounded host receipt runner; not part of application CI."""
from pathlib import Path
import subprocess, sys, time, json, datetime, hashlib, re
repo=Path('/workspace/shared/anpaint-pr52-context-typography-20261012')
out=Path(__file__).parent
mode=sys.argv[1]
assert mode in ('ordinary','optimized')
tree=subprocess.check_output(['git','write-tree'],cwd=repo,text=True).strip()
assert not subprocess.check_output(['git','diff','--name-only'],cwd=repo,text=True).strip()
command=['timeout','--signal=TERM','240s','python3']+(['-O'] if mode=='optimized' else [])+['-m','unittest','discover','-s','tools','-p','test_*.py','-v']
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
log=out/(mode+'.log')
with log.open('wb') as f: result=subprocess.run(command,cwd=repo,stdout=f,stderr=subprocess.STDOUT)
seconds=time.monotonic()-t
end_tree=subprocess.check_output(['git','write-tree'],cwd=repo,text=True).strip()
assert tree==end_tree and not subprocess.check_output(['git','diff','--name-only'],cwd=repo,text=True).strip()
text=log.read_text();counts=re.findall(r'^Ran (\d+) tests? in ([0-9.]+)s$',text,re.M)
receipt=dict(mode=mode,source_tree=tree,command=command,started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=seconds,exit_code=result.returncode,declared_timeout_seconds=240,reported_summary=counts[-1] if counts else None,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),source_unchanged=True)
(out/(mode+'-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt));sys.exit(result.returncode)
