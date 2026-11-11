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
import urllib.error
import urllib.request
import time

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'Paintroid/build/tiff-source'
SOURCES = [
    ('libtiff', '4.7.2', 'https://download.osgeo.org/libtiff/tiff-4.7.2.tar.gz',
     '672bd7d10aee4606171afb864f3570b83340f6a33e2c186dc0512f7145ffdf6a'),
    ('libjpeg-turbo', '3.2.0',
     'https://github.com/libjpeg-turbo/libjpeg-turbo/releases/download/3.2.0/libjpeg-turbo-3.2.0.tar.gz',
     '6f30092cef9fb839779646608f4ee14ae3cbac989c47fa05e841b0841f09878e'),
]


# This immutable asset ID belongs to the same official 3.2.0 release archive,
# not GitHub's generated tag tarball. Both routes must pass SOURCES' one digest.
# Verified archive: 2,537,858 bytes, SHA-256 6f30092c...f09878e.
JPEG_RELEASE_URL = SOURCES[1][2]
JPEG_ASSET_URL = ('https://api.github.com/repos/libjpeg-turbo/libjpeg-turbo/'
                  'releases/assets/462450397')


def download_source(url):
    """At most three requests; switch JPEG transport after transient failure.

    Keep the existing 120-second per-request socket timeout and 2/4-second
    backoff, inside the workflow's unchanged preparation cap. This is not a
    wall-clock guarantee against a slowly streaming server. Only the pinned
    official JPEG URL gets an alternative; certificates/permanent HTTP errors
    and subsequent checksum failures never select another source.
    """
    for attempt in range(3):
        route = JPEG_ASSET_URL if url == JPEG_RELEASE_URL and attempt else url
        request = (urllib.request.Request(route, headers={'Accept': 'application/octet-stream'})
                   if route == JPEG_ASSET_URL else route)
        # Log stable public routes only, never signed redirect query strings.
        print(f'Source download attempt {attempt + 1}/3: {route}', flush=True)
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.read()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            if isinstance(error, urllib.error.HTTPError):
                error.close()
                transient = error.code in (502, 503, 504)
                reason = f'HTTP {error.code}'
            else:
                transient = (isinstance(error, TimeoutError) or
                             isinstance(getattr(error, 'reason', None), TimeoutError))
                reason = 'socket timeout'
            if not transient or attempt == 2:
                raise
            delay = 2 ** (attempt + 1)
            print(f'Transient {reason}; retrying source download in {delay}s', flush=True)
            time.sleep(delay)


def fetch_sources():
    DEST.mkdir(parents=True, exist_ok=True)
    for name, version, url, digest in SOURCES:
        destination = DEST / name
        marker = destination / '.anpaint-revision'
        identity = f'{name}-{version} sha256:{digest}\n'
        if marker.exists() and marker.read_text() == identity:
            continue
        print(f'Fetching {name} {version}', flush=True)
        data = download_source(url)
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
        dict(name=name, version=version, url=url, sha256=digest,
             download_urls=[url, JPEG_ASSET_URL] if url == JPEG_RELEASE_URL else [url])
        for name, version, url, digest in SOURCES
    ], indent=2) + '\n')


if __name__ == '__main__':
    fetch_sources()
