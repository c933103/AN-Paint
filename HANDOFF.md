# AN Paint 0.0.24

Package `paint.anpaint.android`; version code `77`.

## Requested interface corrections

- Restored the original square tool tiles and bold panel captions, and native text
  buttons for ordinary horizontal commands. Undo/redo, clipboard, zoom and collapse
  shortcuts use compact icon controls. Original horizontal Save/Fit labels remain.
- Main/File/Edit/View/Color use an attached tab strip with a shared selected edge.
- Vertical captions sit beside tool icons. Glyph sizes stay unchanged; captions
  wrap into columns at cluster/word boundaries, preserving joined Mongolian words.
- Vertical scripts use a separate status rail and column-based dialogs. Landscape
  places the ribbon beside the canvas. Save as shows filename and format first,
  with optional settings and explanations in scrolling columns. Native keyboard
  fields remain editable and the filename has a vertical preview.
- The colour picker keeps its spatial wheel, honeycomb and swatches while giving
  vertical captions their own columns. Cancel restores the previous colour;
  accepted colours and saved palette entries still update the main colour panel.
- Chinese is offered as zh-TW and zh-HK, with regional vocabulary. Existing
  zh-Hant preferences migrate to zh-TW. Mongolian Cyrillic is mn-Cyrl-MN; the
  vertical Mongolian foundation remains mn-Mong. All 69 entries are generated in
  the same case-insensitive BCP-47 order; device default is first in the picker.

## Verification status

Local Kotlin compilation, the five translation catalogue checks and app lint
complete successfully (zero lint issues). Rendered English, Literary Chinese and
Mongolian screens were inspected in portrait and landscape, including Save as.

The full local regression run passed 235 of 236 tests and exposed one tool-drawer
height regression. That defect was corrected; all 29 affected responsive-toolbox,
workspace and vertical-layout tests then passed. The earlier 42-test language,
save-format and layout run also passed. Vertical checks verify that format captions
are not clipped and Literary Chinese opens dialogs at the first reading column.

The published change now needs its fresh GitHub regression/lint run, universal APK
build and API 35 device checks. No installable artifact or final all-checks-passed
claim is made here yet. Final results and signed APK/source hashes will be recorded
after packaging. Previous failed attempts remain failures in the private logs.

## Preserved work and limitations

All 0.0.23 editing, Save/export, scroll bar and format support remains. This includes
BMP/DIB/TIFF, ICO/AVIF/Base64 text, ASCII export, PDF/TIFF page selection, animation
warnings and corrected Japanese flip labels. See
[the previous handoff](verification/HANDOFF_0.0.23.md) for the completed prior task.

The new language catalogues are partial foundations. Missing strings use English;
local Mongolian editor vocabulary still needs native-speaker review. Android's
system document picker and keyboard are system-owned UI. Legal source texts remain
in their original language. Private signing keys and backups are never published.
