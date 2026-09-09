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

Paintroid and its colour picker: Copyright (C) 2010–2022 The Catrobat Team and
contributors. GNU AGPL version 3 or any later version. Original per-file notices
remain in the corresponding source, bundled in this APK. The full AGPL text is
available separately under Help. Local modifications are dated 7 September 2026.

The retained editor includes the original Catrobat tools and assets, including
JavaFillAlgorithm. The classic workspace uses a local scanline fill implementation. Android system typefaces and ten additional OFL-licensed bundled fonts are
used; the upstream Dubai and STC/GE SS font binaries are not redistributed.

Classic workspace tool/action/navigation and panel-arrow icons, including the
assembly attachment glyph, use KDE Breeze Icons. Copyright (C) 2014 Uri Herrera
and others; KDE Community contributors. Licence: LGPL-3.0-or-later. Original
SVG source, exact revision, hashes and conversion script are included in the
source archive. Full terms appear under Help > Icon licences and below.
Dynamic colour controls, honeycomb swatches and touch/selection boundaries
remain local application drawing code under AGPL-3.0-or-later.
Inherited launcher/tool artwork belongs to the Catrobat distribution, with
original file notices retained. Additional fonts are bundled under OFL-1.1,
with their complete notices included below and in Font licences. System fonts
are the device's system sans-serif, serif,
monospace and fallback faces, including bold/italic variants; their actual font
families and copyright holders depend on the Android vendor. See the device's
Open-source licences for its font notices. Help > Icons, fonts & artwork credits
contains a separate inventory of the included visual assets.

Resolved runtime components for this build follow. Their publisher metadata,
copyright notices and licence terms are retained below. Android platform APIs
and system fonts are supplied by the device, not bundled with this application.

AndroidX, Android support and Material Components: The Android Open Source
Project and Google contributors, Apache License 2.0.
Kotlin and kotlinx.coroutines: JetBrains s.r.o. and Kotlin contributors,
Apache License 2.0.

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
destination = ROOT / 'Paintroid/src/main/assets/legal/THIRD_PARTY_NOTICES.txt'
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(''.join(notice))
print(f'Wrote {destination}: {len(inventory)} resolved components, {len(embedded)} packaged notices.')
