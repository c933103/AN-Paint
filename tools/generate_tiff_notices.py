"""Preserve full notices from the exact TIFF dependency sources. AGPL-3.0-or-later."""
from pathlib import Path
import hashlib
import json
from fetch_tiff_sources import DEST, ROOT, SOURCES, fetch_sources

fetch_sources()
notice = ["""TIFF CODEC NOTICES

AN Paint TIFF integration: Copyright (C) 2026 AN Paint contributors,
GNU AGPL version 3 or any later version. Codec authors retain their own terms.

TIFF uses LibTIFF 4.7.2 by Sam Leffler, Silicon Graphics and contributors,
with libjpeg-turbo 3.2.0 for JPEG compression. This software is based in part
on the work of the Independent JPEG Group. The LZW compression software was
developed by the University of California, Berkeley.

The build enables uncompressed, LZW, PackBits, CCITT Group 3/4, JPEG/old-JPEG
and Deflate TIFF support. Android supplies the system zlib library used for
Deflate. Its runtime implementation belongs to the device; see the device's
open-source notices for its exact version and authors. LibTIFF's zlib callbacks
route Deflate allocations through the same application memory budget.

The unmodified official release sources and these exact licence files are
bundled in the corresponding-source ZIP. tools/fetch_tiff_sources.py checks
release archives against the SHA-256 hashes below. The application CMake file
builds LibTIFF statically and uses libjpeg-turbo's supported ExternalProject
build, disables optional tools/tests/codecs, and routes allocation symbols
through the AN Paint TIFF budget. The JPEG XL/skcms colour pipeline is covered
by JPEG_XL_NOTICES.txt. TIFF bridge and build integration are application code.

SOURCE ARCHIVE INVENTORY
"""]
for name, version, url, digest in SOURCES:
    notice.append(f'\n{name} {version}\n{url}\nArchive SHA-256: {digest}\n')
files = [('libtiff', 'LICENSE.md'), ('libjpeg-turbo', 'LICENSE.md'), ('libjpeg-turbo', 'README.ijg')]
manifest = []
for name, relative in files:
    data = (DEST / name / relative).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    manifest.append(dict(component=name, path=relative, sha256=digest))
    notice.append(f'\n\n--- {name}/{relative} (verbatim; SHA-256 {digest}) ---\n\n')
    notice.append(data.decode('utf-8'))
    notice.append('\n')
(ROOT / 'Paintroid/src/main/assets/legal/TIFF_NOTICES.txt').write_text(''.join(notice))
manifest_path = ROOT / 'legal/tiff-sources.json'
manifest_path.write_text(json.dumps(dict(
    sources=[dict(name=n, version=v, url=u, sha256=h) for n, v, u, h in SOURCES],
    licence_files=manifest), indent=2) + '\n')
print('Preserved TIFF codec notices and source hashes.')
