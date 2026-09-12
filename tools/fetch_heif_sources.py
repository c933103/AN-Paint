"""Fetch exact HEIF/AVIF source revisions; AN Paint, AGPL-3.0-or-later.

The libraries retain their own licences in HEIF_AVIF_NOTICES.txt. Sources are
rebuilt by the Android NDK; no opaque prebuilt codec binary is downloaded.
"""
from pathlib import Path
import io
import shutil
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'Paintroid/build/heif-source'
SOURCES = [
    ('libheif', 'strukturag/libheif', '4e14f5942c1732ace9611b9522cc991501445463'),  # 1.23.4
    ('libde265', 'strukturag/libde265', 'd0bcab76380c079358a3156b3e3b37d17c00a078'),  # 1.1.2
    ('kvazaar', 'ultravideo/kvazaar', '6040962bed5cc68c5ad01234c38c08b8b2822068'),  # 2.3.2
    # SDL's mirror retains the upstream AOM release commit unchanged.
    ('aom', 'libsdl-org/aom', 'de4c1d1edc49723a78954d30a83690aa1937422f'),  # 3.15.0
]

for name, repo, revision in SOURCES:
    destination = DEST / name
    marker = destination / '.anpaint-revision'
    if marker.exists() and marker.read_text() == revision:
        continue
    if destination.exists():
        shutil.rmtree(destination)
    url = f'https://codeload.github.com/{repo}/tar.gz/{revision}'
    print(f'Fetching {repo} at {revision}', flush=True)
    with urllib.request.urlopen(url, timeout=120) as response:
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
    # Both independent upstream projects call their packaging target "dist".
    # Namespace only those unused packaging targets for this combined build.
    if name in ('libde265', 'aom'):
        cmake = destination / 'CMakeLists.txt'
        text = cmake.read_text().replace('add_custom_target(dist', f'add_custom_target({name}-dist')
        text = text.replace('add_dependencies(dist ', f'add_dependencies({name}-dist ')
        cmake.write_text(text)
    marker.write_text(revision)
