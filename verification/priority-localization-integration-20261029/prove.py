import subprocess,json,hashlib
from pathlib import Path
R=Path('/tmp/combined-localization-20261029/repo')
def git(*args):return subprocess.check_output(['git','-C',str(R),*args]).decode().strip()
changes=json.loads(Path('/tmp/combined-localization-20261029/changed-sources.json').read_text())
proof=[];composed=[]
for p,refs in changes.items():
    actual=git('hash-object',p);src={r:git('rev-parse',r+':'+p)for r in refs};same=[r for r,h in src.items()if h==actual]
    (proof if same else composed).append({'path':p,'blob':actual,'exact_sources':same,'sources':src})
assert len(composed)==6,(len(composed),composed)
base='72f987b2b02b4a9a421a0c0874cce6a0d0b53934'
protected=git('diff','--name-only','0070c5816ad31911d227fab50ea193e2a39b13ab',base).splitlines()
for p in protected:assert git('hash-object',p)==git('rev-parse',base+':'+p),p
assert len(protected)==6
resources=[p for p in changes if '/src/main/res/'in p];assert len(resources)==12
assert all(any(d['path']==p for d in proof)for p in resources)
heads={n:{'head':git('rev-parse',f'source/pr{n}'),'tree':git('rev-parse',f'source/pr{n}^{{tree}}')}for n in(215,216,217,218,220)}
data={'base':base,'base_tree':git('rev-parse',base+'^{tree}'),'source_heads':heads,'inherited_paths':len(changes),'exact_source_paths':proof,'composed_paths':composed,'protected_113_219_paths':protected,'scope':'12 locale resource files; exact retained fixtures and consumer tests. No release/version/signing or workflow changes.'}
Path('/tmp/combined-localization-20261029/preservation.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('PASS',len(proof),'exact incoming paths;',len(composed),'composed;',len(protected),'protected merged-fix paths')
