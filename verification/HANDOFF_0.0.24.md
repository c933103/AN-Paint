# AN Paint 0.0.24

Package `paint.anpaint.android`; version code `77`.

The development APK is compiled for arm64-v8a, armeabi-v7a, x86 and x86_64 and
signed with the existing development key, allowing an update over 0.0.23.

## Completed changes

- Restored square tool tiles, the original small bold panel captions and native
  horizontal command buttons. Top clipboard/undo shortcuts and zoom controls are
  compact again. Horizontal Save/Fit labels retain their previous presentation.
- Main/File/Edit/View/Color now share a tab strip with a selected edge rather than
  boxed command buttons. The collapse control stays on the same row.
- Vertical captions sit beside tool icons and retain their glyph size. Joined
  Mongolian words remain intact; long labels wrap into additional columns.
- Vertical languages have a status rail and separate dialog columns. Landscape
  places the ribbon beside the canvas to preserve its height. File dialogs start
  at the correct reading edge and show filename/format before optional settings.
  Format labels are measured without clipping; native keyboard fields remain
  editable and a vertical preview displays the filename.
- The colour picker keeps its spatial wheel/honeycomb/swatches while providing
  separate vertical captions. Live previews, Cancel restoration, accepted colours
  and saved-palette updates remain connected to the main colour panel.
- Removed generic zh-Hant from the offered language list. Existing preferences
  migrate to zh-TW. Regional zh-TW/zh-HK catalogues include terms such as
  橡皮擦/擦膠 and 色盤/調色板. Added horizontal mn-Cyrl-MN alongside mn-Mong.
  All 69 language entries are integrated into case-insensitive BCP-47 order.

## Verification

- The complete 732-file GitHub tree, including modes and the removed zh-Hant file,
  was verified before the build started.
- The APK's embedded corresponding-source archive matches its exported ZIP;
  729 repository file contents were verified (three Git/IDE files are excluded
  from source exports), together with the four bundled pinned native-source trees.
- Package/version, all four ABIs, APK integrity, 16 KB ZIP alignment and the original
  signing certificate were verified after signing under a temporary build directory.
- Five translation checks passed. Kotlin compilation passed. Local app lint
  reported zero issues.
- The full local regression run passed 235/236 tests and exposed one drawer-height
  defect. After fixing it, all 29 affected layout/workspace tests passed. The earlier
  42-test language/save/layout run passed. A separate colour-dialog and language-row
  review passed for both vertical scripts. Portrait and landscape previews were
  inspected for English, Literary Chinese and traditional Mongolian.
- The universal GitHub build passed. The fresh CI regression suite passed all
  236 tests with no failures, errors or skipped tests; CI lint reported zero issues.
  All 77 API 35 device tests also passed, with no failures, errors or skipped tests.
  Original CI reports are included in the private build backup.

Built source: [c5afc05a](https://github.com/c933103/AN-Paint/tree/c5afc05a3b7127d4e3c00be1fbb0688d506451db).
Workflow: [34758217415](https://github.com/c933103/AN-Paint/actions/runs/34758217415).

## Preserved work and limits

All 0.0.23 editing, Save/export, scroll bar and format work remains, including
BMP/DIB/TIFF, ICO/AVIF/Base64 text, ASCII export, PDF/TIFF page selection,
animation warnings and corrected Japanese flip labels. The preceding handoff
records the completed prior task.

The new catalogues remain partial foundations. Missing text uses English; locally
written Mongolian vocabulary still needs native-speaker review. Android's document
picker and keyboard are system-owned, and source legal texts retain their original
language. Private signing keys and backups are not published to GitHub.

## SHA-256

```
d75e7bf9bce4c9b5fcdaa6fd88b8439d236fa9a07fcf8598dc62de5f7ee775a4  AN-Paint-0.0.24-development.apk
1961e42cffcc3a6a2fdeaf0f83fe94ebb44f38ce839bc731be7f30ea7d8fb539  AN-Paint-source.zip
```

Signing certificate:
`f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`.
