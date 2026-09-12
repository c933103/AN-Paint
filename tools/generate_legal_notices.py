"""Pocket Paint Local, 2026-09-07, AGPL-3.0-or-later.
Run ./gradlew :app:writeDependencyInventory first, then this script.
Uses the resolved version inventory and cached publisher POMs, not guessed versions.
The checked-in legal/vendor files preserve upstream licence text for redistribution.
"""
from pathlib import Path
import io
import json
import os
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ.get('GRADLE_USER_HOME', str(Path.home() / '.gradle'))) / 'caches/modules-2/files-2.1'
inventory = json.loads((ROOT / 'app/build/runtime-dependencies.json').read_text())
notice = ["""AN Paint — third-party copyright and licence notices

Derived from Paintroid: Copyright (C) 2010–2022 The Catrobat Team and
contributors. GNU AGPL version 3 or any later version. Original per-file notices
remain in the corresponding source, bundled in this APK. Full AGPL text is under
Help. AN Paint modifications are dated 7–12 September 2026.

The consolidated editor uses a local scanline fill implementation. The original
editor, colour-picker module, project-file libraries and legacy artwork have
been removed. No Dubai or STC/GE SS font binaries are redistributed.

Tool/action/navigation and panel-arrow icons: KDE Breeze Icons. Copyright (C)
2014 Uri Herrera and others; KDE Community contributors. LGPL-3.0-or-later.
Original SVGs, revision, hashes and conversion script are included in the source.
Full terms appear under Icon licences and below. The AN monogram launcher,
dynamic colour controls, honeycomb swatches and selection/crop guides are
AN Paint application artwork/code, AGPL-3.0-or-later.

Material Design 3 baseline colour data: Copyright (C) 2022 The Android Open
Source Project, Apache-2.0. The exact upstream tokens and licence are preserved
in artwork/material3; complete notices follow below. AN Paint maps semantic
roles to its controls while retaining actual image and swatch colours.

Ten unmodified fonts are bundled under SIL OFL-1.1, with complete notices below.
System fonts and platform widget artwork are supplied by the Android device;
see its open-source licences for their exact files and authors.

The optional online Catrobat figures gallery is an external service. Its images
are not bundled. Catrobat's own non-software artwork uses CC BY-SA 4.0, except
project names and logos; inserted-image source links are kept under Image credits.
https://developer.catrobat.org/pages/legal/licenses/catrobat/

JPEG XL uses libjxl 0.12.0 plus Brotli, Highway and skcms. WebP uses libwebp 1.6.0
and SharpYUV, with Android NDK CPU-features support. HEIC and AVIF use libheif
1.23.4, libde265 1.1.2, Kvazaar 2.3.2 and libaom 3.15.0. Exact revisions,
copyrights, complete licence texts and patent grants follow below and under
Image codec licences. The scripts tools/fetch_jxl_sources.py,
tools/fetch_webp_sources.py and tools/fetch_heif_sources.py obtain the pinned
upstream sources for rebuilding the native libraries.

Native runtime support also includes LLVM libc++, libc++abi, libunwind and
compiler-rt built-ins supplied by Android NDK 27.2.12479018. Their complete
NDK-supplied LLVM licence text and exceptions are retained below and under
Image codec licences. tools/generate_native_runtime_notices.py preserves
the actual installed toolchain's NOTICE and records its source hash.

Resolved Android/JVM runtime components for this build follow. Their publisher
metadata and packaged notices are preserved below. Test and build tools are not
part of this inventory because they are not distributed in the application.
AndroidX: The Android Open Source Project and Google contributors, Apache-2.0.
Kotlin: JetBrains s.r.o. and Kotlin contributors, Apache-2.0.

COMPONENT INVENTORY
"""]

def pom_for(group, name, version):
    return next((CACHE / group / name / version).glob('*/*.pom'), None)

def metadata(group, name, version, seen=None):
    seen = seen or set()
    key = (group, name, version)
    if key in seen:
        return [], []
    seen.add(key)
    path = pom_for(*key)
    if not path:
        return [], []
    root = ET.parse(path).getroot()
    licenses = [(x.findtext('{*}name') or '', x.findtext('{*}url') or '') for x in root.findall('{*}licenses/{*}license')]
    owners = [x.text for x in root.findall('{*}developers/{*}developer/{*}name') if x.text]
    org = root.findtext('{*}organization/{*}name')
    if org:
        owners.append(org)
    if not licenses:
        parent = root.find('{*}parent')
        if parent is not None:
            inherited, parent_owners = metadata(*(parent.findtext('{*}' + k) for k in ['groupId', 'artifactId', 'version']), seen)
            licenses = inherited
            owners += parent_owners
    return licenses, list(dict.fromkeys(owners))

embedded = {}
for row in inventory:
    group, name, version = row['group'], row['name'], row['version']
    licenses, owners = metadata(group, name, version)
    assert licenses, f'Missing publisher licence metadata: {row}'
    notice.append(f'\n{group}:{name}:{version}\n')
    for title, url in licenses:
        notice.append(f'Licence: {title}\n{url}\n')
    if owners:
        notice.append('Publisher / contributors: ' + '; '.join(owners) + '\n')
    path = CACHE / group / name / version
    for archive in list(path.glob('*/*.jar')) + list(path.glob('*/*.aar')):
        with zipfile.ZipFile(archive) as z:
            archives = [z]
            if 'classes.jar' in z.namelist():
                archives.append(zipfile.ZipFile(io.BytesIO(z.read('classes.jar'))))
            for container in archives:
                for entry in container.namelist():
                    leaf = entry.rsplit('/', 1)[-1].upper()
                    if leaf.startswith(('LICENSE', 'NOTICE', 'COPYING', 'COPYRIGHT')) and not entry.endswith('/'):
                        text = container.read(entry).decode('utf-8', errors='replace')
                        embedded[(name, entry)] = text

notice.append('\n\nPRESERVED LICENCE TEXTS AND NOTICES\n')
for path in sorted((ROOT / 'legal/vendor').glob('*.txt')):
    notice.extend(['\n\n' + path.name + '\n\n', path.read_text()])
for (name, entry), text in sorted(embedded.items()):
    notice.extend([f'\n\n{name} — {entry}\n\n', text])
notice.append('\n\nBUNDLED FONT NOTICES\n\n' + (ROOT / 'Paintroid/src/main/assets/legal/FONT_NOTICES.txt').read_text())
notice.append('\n\nBREEZE ICON NOTICES\n\n' + (ROOT / 'Paintroid/src/main/assets/legal/ICON_NOTICES.txt').read_text())
for title, filename in [('JPEG XL', 'JPEG_XL_NOTICES.txt'), ('WEBP', 'WEBP_NOTICES.txt'),
                        ('HEIC AND AVIF', 'HEIF_AVIF_NOTICES.txt')]:
    notice.append(f'\n\n{title} CODEC NOTICES\n\n' + (ROOT / 'Paintroid/src/main/assets/legal' / filename).read_text())
notice.append('\n\nNATIVE RUNTIME NOTICES\n\n' + (ROOT / 'Paintroid/src/main/assets/legal/NATIVE_RUNTIME_NOTICES.txt').read_text())
notice.append('\n\nMATERIAL DESIGN 3 COLOUR NOTICES\n\n' + (ROOT / 'Paintroid/src/main/assets/legal/MATERIAL_COLOUR_NOTICES.txt').read_text())
destination = ROOT / 'Paintroid/src/main/assets/legal/THIRD_PARTY_NOTICES.txt'
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(''.join(notice))
print(f'Wrote {destination}: {len(inventory)} resolved components, {len(embedded)} packaged notices.')
