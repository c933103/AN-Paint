"""One-time source/compiled-resource evidence audit, outside the app test tree."""
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

BASE=pathlib.Path('/workspace/scratch/bbca2890f602')
W=BASE/'priority-twentieth-20261102'
OUT=BASE/'priority147-ci-audit'
OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(W/'tools'))
from compose_device_reports import verify_source_bundle
from current_localization_contracts import require_string_root

meta=json.loads((OUT/'artifact-metadata.json').read_text())
archive=OUT/'build.zip'
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
assert meta['digest']=='sha256:'+digest
assert meta['workflow_run']['id']==41551141341
assert meta['workflow_run']['head_sha']=='db72d33ac3526cd6928c7f8a2d3de7a509006462'
z=zipfile.ZipFile(archive)
info=json.loads(z.read('build/delivery/build-info.json'))
assert info['commit']=='b3371af4594ffda11ad393668fa8797cb64ac6da'
assert info['run_id']=='41551141341' and info['build_variant']=='debug'
for name,key,out in [('app/build/outputs/apk/debug/app-debug.apk','apk_sha256','app.apk'),
                     ('build/delivery/AN-Paint-source.zip','source_sha256','source.zip')]:
    h=hashlib.sha256()
    with z.open(name) as src,(OUT/out).open('wb') as dest:
        for b in iter(lambda:src.read(1048576),b''):h.update(b);dest.write(b)
    assert h.hexdigest()==info[key],key
assert subprocess.check_output(['git','-C',str(W),'write-tree'],text=True).strip()=='6c17567438bdd321b8e04e151b7458ddc6244a69'
matched=verify_source_bundle(W,OUT/'source.zip')
assert matched==1273
tool=pathlib.Path('/tmp/anpaint287-audit/verification-tools/aapt2')
with (OUT/'compiled-resources.txt').open('w') as fp:
    subprocess.run([str(tool),'dump','resources',str(OUT/'app.apk')],stdout=fp,check=True)
values={};key=None
for line in (OUT/'compiled-resources.txt').read_text().splitlines():
    m=re.match(r'    resource \S+ string/(\S+)$',line)
    if m:key=m[1];continue
    if line.startswith('    resource '):key=None
    if key:
        m=re.match(r'      \(([^)]*)\) "(.*)"$',line)
        if m:
            ident=(key,m[1]);assert ident not in values,ident
            values[ident]=m[2]
rows=json.loads((BASE/'priority147-evidence/manifest.json').read_text())
sz=zipfile.ZipFile(OUT/'source.zip');details=[]
for r in rows:
    config='fa-rIR' if r['locale']=='fa-IR' else r['locale']
    ident=r['key'],config
    assert ident in values,('compiled configuration absent',ident)
    assert values[ident]==r['display'],('compiled mismatch',ident,values[ident],r['display'])
    root=ET.fromstring(sz.read('AN-Paint/'+r['path']))
    require_string_root(root,r['key'],r['raw'],{'attributes':r['attributes']})
    details.append(dict(locale=r['locale'],key=r['key'],compiled_configuration=config,
                        raw_source=r['raw'],source_attributes=r['attributes'],compiled_display=values[ident]))
receipt=dict(repository='c933103/AN-Paint',pr=288,head='db72d33ac3526cd6928c7f8a2d3de7a509006462',
             tested_checkout='b3371af4594ffda11ad393668fa8797cb64ac6da',
             tested_parents=['79bfae14b8138d2464756cfb13f508635ed25765','db72d33ac3526cd6928c7f8a2d3de7a509006462'],
             expected_tree='6c17567438bdd321b8e04e151b7458ddc6244a69',run=41551141341,
             artifact_id=meta['id'],artifact_sha256=digest,build_info=info,
             source_blobs_verified=matched,source_known_exclusions=['.gitignore','.idea/codeStyles/Project.xml','colorpicker/.gitignore'],
             source_and_compiled_displays_verified=len(details),mismatches=0,
             manifest_sha256=hashlib.sha256((BASE/'priority147-evidence/manifest.json').read_bytes()).hexdigest(),
             aapt2_sha256=hashlib.sha256(tool.read_bytes()).hexdigest(),
             limits='Source/compiled-resource verification, not native fluency or layout certification. CI status reported separately.')
(OUT/'compiled-value-details.json').write_text(json.dumps(details,ensure_ascii=False,indent=2)+'\n')
(OUT/'artifact-audit-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
