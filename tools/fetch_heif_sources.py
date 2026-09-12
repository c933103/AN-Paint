"""Fetch exact HEIF/AVIF source revisions; AN Paint, AGPL-3.0-or-later.

The libraries retain their own licences in HEIF_AVIF_NOTICES.txt. Sources are
rebuilt by the Android NDK; no opaque prebuilt codec binary is downloaded.
"""
from pathlib import Path
import hashlib
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


def patch_kvazaar_mutex_lifetime(source: Path):
    """Fix optional RD logging cleanup when encoders are opened repeatedly.

    Upstream 2.3.2 destroys every global outfile mutex on encoder_close,
    including mutexes never initialized or already destroyed by a prior tile.
    Android's pthread FORTIFY correctly aborts on the second close. Track the
    actual initialization lifetime; encoding algorithms remain unchanged.
    """
    original_digest = '69e9902060b9d38a107cdea4b7d602b81c93dfd3faf63631226c22e39bad7c72'
    patched_digest = '0635fc6ddb808ad0b03126a3bc677e97d9f3bfa8cb871c244e89e3d5f9faccb1'
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest == patched_digest:
        return
    if digest != original_digest:
        raise RuntimeError('Unexpected Kvazaar rdo.c; review the pinned mutex lifetime patch')
    text = raw.decode('utf-8')
    replacements = [
        ('static pthread_mutex_t outfile_mutex[RD_SAMPLING_MAX_LAST_QP + 1];',
         'static pthread_mutex_t outfile_mutex[RD_SAMPLING_MAX_LAST_QP + 1];\n'
         '// AN Paint: track optional RD logging mutex lifetime.\n'
         'static unsigned char outfile_mutex_initialized[RD_SAMPLING_MAX_LAST_QP + 1];'),
        ('      goto out_destroy_mutexes;\n    }\n  }',
         '      goto out_destroy_mutexes;\n    }\n    outfile_mutex_initialized[qp] = 1;\n  }'),
        ('    pthread_mutex_destroy(outfile_mutex + qp);',
         '    if (outfile_mutex_initialized[qp]) {\n'
         '      pthread_mutex_destroy(outfile_mutex + qp);\n'
         '      outfile_mutex_initialized[qp] = 0;\n    }'),
        ('  for (i = 0; i < RD_SAMPLING_MAX_LAST_QP; i++) {',
         '  for (i = 0; i <= RD_SAMPLING_MAX_LAST_QP; i++) {'),
        ('      fclose(curr);\n    }\n    if (curr_mtx != NULL) {\n      pthread_mutex_destroy(curr_mtx);\n    }',
         '      fclose(curr);\n      fastrd_learning_outfile[i] = NULL;\n    }\n'
         '    if (outfile_mutex_initialized[i]) {\n'
         '      pthread_mutex_destroy(curr_mtx);\n      outfile_mutex_initialized[i] = 0;\n    }'),
    ]
    for old, new in replacements:
        if text.count(old) != 1:
            raise RuntimeError('Pinned Kvazaar source changed; review mutex lifetime patch')
        text = text.replace(old, new)
    patched = text.encode('utf-8')
    if hashlib.sha256(patched).hexdigest() != patched_digest:
        raise RuntimeError('Kvazaar mutex patch produced unexpected source')
    source.write_bytes(patched)


# Run after cache hits too, so an existing offline source archive is repairable.
patch_kvazaar_mutex_lifetime(DEST / 'kvazaar/src/rdo.c')
