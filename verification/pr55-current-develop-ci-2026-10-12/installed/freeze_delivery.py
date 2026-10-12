#!/usr/bin/env python3
"""Hash only the bounded installed-review deliverable; preserve temporary working files."""
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
paths=set(p.glob('*.py'))
paths.update(p/n for n in ['README.md','ACCEPTANCE.json','INSTALLED-VERDICT.json','deadline-result.json','source-continuity-result.json','source-matrix-deadline-selftests.log','privacy-scan-result.json','frozen-selection-check.json','frozen-selection-replay.log','binding.json','artifact-binding.json','source-input-result.json','payload-digest-result.json','build-provenance-result.json','delivery-compiled-arabic-input.json','api30-visual-inspection.json','api35-visual-inspection.json','visual-inspection.json','arabic-visual-inputs.json','arabic-visual-white.png','checker-selftests.log','checker-selftests-optimized.log','source-decoder-selftests.log','source-decoder-selftests-optimized.log','reproduction.log','bundle-build.log','replay-check.log'])
for directory in ['installed-observed','replay-inputs']:
 paths.update(q for q in (p/directory).iterdir() if q.is_file())
for directory in ['reproduced','replayed-verified/results']:
 paths.update(q for q in (p/directory).iterdir() if q.is_file() and q.suffix in ('.json','.log'))
 paths.add(p/directory/'native-vertical/result.json.gz')
paths.update(p/('visual-api'+api)/'sheets.json' for api in ['30','35'])
files=[]
for f in sorted(paths):
 if not f.is_file():raise ValueError('Missing delivery file '+str(f))
 data=f.read_bytes();files.append({'path':f.relative_to(p).as_posix(),'bytes':len(data),'sha256':sha(data)})
b=json.loads((p/'binding.json').read_bytes());out={'schema':1,'head':b['head'],'tree':b['tree'],'merge':b['merge'],'run_id':b['run_id'],'file_count':len(files),'total_bytes':sum(x['bytes'] for x in files),'files':files,'scope':'Copy exactly these bounded files plus this manifest. APK/source ZIPs/whole-tree dumps and duplicate extracted raw files are intentionally excluded. All original bounded protocol/log/native PNG replay inputs remain in replay-inputs/raw-inputs.tar.gz.'}
(p/'DELIVERY-FILES.json').write_text(json.dumps(out,indent=2)+'\n')
for r in files:
 data=(p/r['path']).read_bytes()
 if len(data)!=r['bytes'] or sha(data)!=r['sha256']:raise ValueError('Frozen delivery differs '+r['path'])
print(json.dumps({k:v for k,v in out.items() if k not in ('files','scope')},indent=2));print('manifest_sha256',sha((p/'DELIVERY-FILES.json').read_bytes()))
