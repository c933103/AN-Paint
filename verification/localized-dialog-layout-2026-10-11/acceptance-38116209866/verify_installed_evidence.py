#!/usr/bin/env python3
"""Verify and reconstruct only current run38116209866 installed evidence.

python3 verify_installed_evidence.py --output /tmp/current-installed-evidence.zip \
  --extract /tmp/current-installed-evidence

Requires Python standard library only. No predecessor archive or network access.
Parts, companions, exact ZIP inventory, nested original producer manifests,
source bindings, all eight phase summaries, and all ten PNG hashes are checked.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,zipfile

def check(condition, message):
    if not condition: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def gitsha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def safe(path):
    p=PurePosixPath(path)
    check(not p.is_absolute() and '..' not in p.parts and '\\' not in path and path!='', 'Unsafe member path')
    return path
def validate(b,row):
    check(len(b)==row['bytes'] and sha(b)==row['sha256'],'Byte/hash mismatch: '+row['path'])
    if 'git_blob_sha' in row:check(gitsha(b)==row['git_blob_sha'],'Git SHA mismatch: '+row['path'])
def verify(directory,output=None,extract=None):
    directory=Path(directory);m=json.loads((directory/'installed-evidence-manifest.json').read_text());parts=[]
    check(m['independence']['prior_archive_required'] is False,'Not standalone')
    protected={(directory/safe(x['path'])).resolve() for x in m['parts']+m['companion_files']}
    protected.add((directory/'installed-evidence-manifest.json').resolve())
    if output:check(Path(output).resolve() not in protected,'Refusing to overwrite verification input')
    for r in m['companion_files']:validate((directory/safe(r['path'])).read_bytes(),r)
    for r in m['parts']:
        b=(directory/safe(r['path'])).read_bytes();validate(b,r);check(len(b)<=50000,'Oversized part');parts.append(b)
    archive=b''.join(parts);validate(archive,m['archive']);z=zipfile.ZipFile(io.BytesIO(archive))
    check(len(z.namelist())==len(set(z.namelist())),'Duplicate ZIP members')
    check(set(z.namelist())=={r['path'] for r in m['members']},'Exact member inventory mismatch')
    for r in m['members']:safe(r['path']);validate(z.read(r['path']),r)
    pngs=0
    for n in m['nested_original_exports']:
        b=z.read(n['path']);validate(b,n);zz=zipfile.ZipFile(io.BytesIO(b))
        check(len(zz.namelist())==len(set(zz.namelist())),'Duplicate nested ZIP members')
        check(set(zz.namelist())=={r['path'] for r in n['members']},'Nested inventory mismatch')
        for r in n['members']:safe(r['path']);validate(zz.read(r['path']),r);pngs+=r['path'].endswith('.png')
        pm=json.loads(zz.read('manifest.json'))
        for r in pm['files']:validate(zz.read(safe(r['path'])),r)
        receipt=json.loads(zz.read('receipt.json'))
        check(receipt['outcome']=='passed' and receipt['source_tests_sha256']==m['source_tests_sha256'],'Receipt outcome/source mismatch')
        if 'unchangedAdvancedColour' in n['path']:check(receipt['positive_viewport_accepted'] is False,'Colour limitation misclassified')
    check(len(m['nested_original_exports'])==5 and pngs==10,'Wrong installed export/PNG count')
    cases=0
    for r in m['phases']:
        p=json.loads(z.read(r['path']));check(p['success'] and p['completed_tests']==p['expected_tests']==r['completed_tests'],'Phase mismatch')
        check(all(c['status']=='passed' for c in p['cases']),'Non-passing phase');cases+=p['completed_tests']
    check(len(m['phases'])==8 and cases==104,'Wrong phase/case count')
    if output:Path(output).write_bytes(archive)
    if extract:
        dest=Path(extract);dest.mkdir(parents=True,exist_ok=True)
        for name in z.namelist():
            path=dest/safe(name);check(path.resolve() not in protected,'Extraction would overwrite verification input');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(z.read(name))
        for n in m['nested_original_exports']:
            zz=zipfile.ZipFile(io.BytesIO(z.read(n['path'])))
            for name in zz.namelist():
                path=dest/'producer-dialog'/Path(n['path']).stem/safe(name);check(path.resolve() not in protected,'Extraction would overwrite verification input');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(zz.read(name))
    return {'verified':True,'prior_archive_required':False,'archive_sha256':sha(archive),'archive_bytes':len(archive),'members':len(m['members']),'parts':len(parts),'original_exports':5,'original_pngs':pngs,'phases':8,'passed_cases':cases,'positive_colour_viewport_accepted':False}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path);p.add_argument('--extract',type=Path);a=p.parse_args();print(json.dumps(verify(a.directory,a.output,a.extract),indent=2))
