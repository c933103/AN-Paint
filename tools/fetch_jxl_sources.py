"""Fetch the pinned JPEG XL reference codec sources. AN Paint: AGPL-3.0-or-later.

The fetched libraries retain their own licences. No generated binary is checked in.
"""
from pathlib import Path
import io, tarfile, urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'Paintroid/build/jxl-source'
SOURCES = [
    ('', 'libjxl/libjxl', 'a7a9c787341cf703dede03c2009fa460cae5e5df'),
    ('third_party/brotli', 'google/brotli', '028fb5a23661f123017c060daa546b55cf4bde29'),
    ('third_party/highway', 'google/highway', '457c891775a7397bdb0376bb1031e6e027af1c48'),
    ('third_party/skcms', 'google/skcms', '96d9171c94b937a1b5f0293de7309ac16311b722'),
]

for subdir, repo, sha in SOURCES:
    destination = DEST / subdir
    marker = destination / '.anpaint-revision'
    if marker.exists() and marker.read_text() == sha:
        continue
    url = f'https://codeload.github.com/{repo}/tar.gz/{sha}'
    print(f'Fetching {repo} at {sha}', flush=True)
    with urllib.request.urlopen(url, timeout=90) as response:
        archive = tarfile.open(fileobj=io.BytesIO(response.read()), mode='r:gz')
    destination.mkdir(parents=True, exist_ok=True)
    for member in archive.getmembers():
        relative = Path(*Path(member.name).parts[1:])
        if not relative.parts or '..' in relative.parts or member.issym() or member.islnk():
            continue
        target = destination / relative
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True)
        elif member.isfile():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    marker.write_text(sha)
