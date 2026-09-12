# AN Paint launcher artwork

Copyright (C) 2026 AN Paint contributors. GNU AGPL-3.0-or-later; see the
repository's LICENSE for the full terms.

The launcher is an original rounded paintbrush making a broad coral and blue
stroke, on a pale lavender background. The simple silhouette communicates
painting without lettering, age-specific characters or copied reference art.
No font glyph, upstream logo or third-party icon was used. `launcher.svg` is
the editable source, including a separate monochrome silhouette.

`tools/generate_launcher_icons.py` generates Android legacy square/round PNGs,
adaptive foreground/background resources and Android 13 monochrome artwork.
The foreground lies within the adaptive icon's central 66 dp safe circle on a
108 dp layer. Legacy icons crop the central 72 dp visible area, keeping the
symbol at the same scale as adaptive icons. The monochrome artwork separates
the handle, bristles and paint stroke so the brush stays legible with a single
system-supplied colour. All paths are ordinary filled curves, without raster
layers, effects or API-specific fill rules.

Reproduce the checked-in assets with Python and CairoSVG 2.8.2:

```sh
python3 -m pip install CairoSVG==2.8.2
python3 tools/generate_launcher_icons.py
```

For review images at 48, 96 and 512 pixels, add `--preview-directory` with an
output directory outside the repository. This also renders the foreground and
a safe-zone guide. Preview images are not needed to build the app.

`generated.json` records the source and every generated resource's SHA-256.
The source, script, resources and hashes are included in the corresponding
source distributed with the APK. The toolbar glyphs separately retain KDE
Breeze's LGPL-3.0-or-later terms. Launcher colour choices are individual values;
they do not copy any Material icon artwork.
