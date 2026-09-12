"""Fetch the pinned official WebP codec. AN Paint: AGPL-3.0-or-later.

The fetched sources retain Google's BSD-3-Clause licence and patent grant.
Source files are unmodified; CMake routes allocations through AN Paint's budget.
"""
from pathlib import Path
import io
import shutil
import tarfile
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'Paintroid/build/webp-source'
REPOSITORY = 'webmproject/libwebp'
REVISION = '4fa21912338357f89e4fd51cf2368325b59e9bd9'  # v1.6.0
marker = DEST / '.anpaint-revision'
if not marker.exists() or marker.read_text() != REVISION:
    print(f'Fetching {REPOSITORY} at {REVISION}', flush=True)
    url = f'https://codeload.github.com/{REPOSITORY}/tar.gz/{REVISION}'
    with urllib.request.urlopen(url, timeout=90) as response:
        archive_bytes = response.read()
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='webp-source-', dir=DEST.parent) as temporary:
        staged = Path(temporary) / 'source'
        staged.mkdir()
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode='r:gz') as archive:
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
        (staged / '.anpaint-revision').write_text(REVISION)
        if DEST.exists():
            shutil.rmtree(DEST)
        staged.rename(DEST)
