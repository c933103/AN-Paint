"""Fetch verified official TIFF/JPEG release sources. AN Paint: AGPL-3.0-or-later.

Codec source licences are preserved in TIFF_NOTICES.txt and corresponding source.
Only integration CMake options and allocation symbol routing alter the build.
"""
from pathlib import Path
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'Paintroid/build/tiff-source'
SOURCES = [
    ('libtiff', '4.7.2', 'https://download.osgeo.org/libtiff/tiff-4.7.2.tar.gz',
     '672bd7d10aee4606171afb864f3570b83340f6a33e2c186dc0512f7145ffdf6a'),
    ('libjpeg-turbo', '3.2.0',
     'https://github.com/libjpeg-turbo/libjpeg-turbo/releases/download/3.2.0/libjpeg-turbo-3.2.0.tar.gz',
     '6f30092cef9fb839779646608f4ee14ae3cbac989c47fa05e841b0841f09878e'),
]


def fetch_sources():
    DEST.mkdir(parents=True, exist_ok=True)
    for name, version, url, digest in SOURCES:
        destination = DEST / name
        marker = destination / '.anpaint-revision'
        identity = f'{name}-{version} sha256:{digest}\n'
        if marker.exists() and marker.read_text() == identity:
            continue
        print(f'Fetching {name} {version}', flush=True)
        with urllib.request.urlopen(url, timeout=120) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != digest:
            raise RuntimeError(f'{name} {version}: official source archive hash mismatch')
        with tempfile.TemporaryDirectory(prefix=f'{name}-', dir=DEST) as temporary:
            staged = Path(temporary) / 'source'
            staged.mkdir()
            with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
                for member in archive.getmembers():
                    relative = Path(*Path(member.name).parts[1:])
                    if not relative.parts or relative.is_absolute() or '..' in relative.parts:
                        continue
                    target = staged / relative
                    if member.isdir():
                        target.mkdir(parents=True, exist_ok=True)
                    elif member.isfile():
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(archive.extractfile(member).read())
            (staged / '.anpaint-revision').write_text(identity)
            if destination.exists():
                shutil.rmtree(destination)
            staged.rename(destination)
    (DEST / 'sources.json').write_text(json.dumps([
        dict(name=name, version=version, url=url, sha256=digest)
        for name, version, url, digest in SOURCES
    ], indent=2) + '\n')


if __name__ == '__main__':
    fetch_sources()
