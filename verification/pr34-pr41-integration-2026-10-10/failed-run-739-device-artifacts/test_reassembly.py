#!/usr/bin/env python3
"""Positive and negative verification controls for the exact retained artifacts."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def main():
    checks = []
    for mode in ('normal', 'flag', 'environment'):
        with tempfile.TemporaryDirectory() as temporary:
            p = Path(temporary); source=p/'archive'; source.mkdir()
            for path in ROOT.iterdir():
                if path.name in ('manifest.json', 'reassemble.py', 'device30.zip') or path.name.startswith('device35.zip.part-'):
                    shutil.copyfile(path, source/path.name)
            env = dict(os.environ);env.pop('PYTHONOPTIMIZE', None)
            if mode == 'environment': env['PYTHONOPTIMIZE']='1'
            command=[sys.executable]+(['-O'] if mode=='flag' else [])+[str(source/'reassemble.py')]
            def run(name, expected=0, extra=()):
                r=subprocess.run(command+list(extra),env=env,capture_output=True,text=True,timeout=15)
                if (r.returncode==0)!=(expected==0):raise RuntimeError((mode,name,r.returncode,r.stdout,r.stderr))
                checks.append(dict(mode=mode,case=name,passed=True))
            run('positive checksum verification')
            out=p/'reconstructed';run('positive fresh reconstruction',extra=('--output',str(out)))
            b=(out/'device35.zip').read_bytes()
            if hashlib.sha256(b).hexdigest()!='a813678e7a67623567a5b7e890449be7c822c8af38463db22c2a3db9f1463ca6':raise RuntimeError('reconstruction differs')
            run('existing destination rejected',1,('--output',str(out)))
            part=source/'device35.zip.part-000';original=part.read_bytes();part.unlink()
            run('missing part rejected',1);part.write_bytes(original)
            part.write_bytes(bytes([original[0]^1])+original[1:]);run('same-size tamper rejected',1);part.write_bytes(original)
            part.write_bytes(original[:-1]);run('truncated part rejected',1);part.write_bytes(original)
            extra=source/'device35.zip.part-999';extra.write_bytes(b'extra');run('extra part rejected',1);extra.unlink()
            part.unlink();part.symlink_to(source/'device35.zip.part-001');run('symlink part rejected',1);part.unlink();part.write_bytes(original)
            manifest=source/'manifest.json';before=manifest.read_bytes();obj=json.loads(before);obj['device35']['parts'][0],obj['device35']['parts'][1]=obj['device35']['parts'][1],obj['device35']['parts'][0];manifest.write_text(json.dumps(obj));run('swapped manifest order rejected',1);manifest.write_bytes(before)
            a=source/'device30.zip';before=a.read_bytes();a.write_bytes(before[:-1]);run('API30 truncation rejected',1);a.write_bytes(before)
    print(json.dumps(dict(success=True,checks=len(checks),results=checks),indent=2))

if __name__=='__main__':main()
