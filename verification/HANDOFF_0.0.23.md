# AN Paint 0.0.23

Package **paint.anpaint.android**, version code **76**. Signed with the same
certificate as 0.0.22 for an in-place update. This is a development build.

[Corresponding source commit](https://github.com/c933103/AN-Paint/commit/a73521e4a254b921feb2a7bcf359553d38ef2ffd) ·
[Build and checks](https://github.com/c933103/AN-Paint/actions/runs/34743279040)

## Changes

- Main, File, Edit, View and Color tabs in both orientations, with a collapsible
  panel above the canvas. Navigate is first/default; Drawing replaces the Brush
  group label. Every tool is labelled. Cut/Copy/Paste sit beside Undo/Redo.
- Edit contains selection, canvas bounds/size and image transformations. View
  contains grid, cursor drawing, magnifier, Languages and fullscreen. Drawing
  settings stay with relevant tools. How to use and About/licences/credits are in File.
- Save as chooses a pixel-preserving format and destination. Save reuses that
  successful destination/name/format, including restored drafts when permission
  remains valid. Export as creates lossy/reduced output without changing the Save
  destination or clearing unsaved changes. All thirteen output formats remain.
- Color contains Swap, Reset B/W, standard/recent/saved colors. Pickers preview the
  active FG/BG immediately; Use color confirms and Cancel restores. Optional Add to
  palette updates the same saved palette in Color. Unconfirmed preview colors stay
  out of autosave metadata. Saved colors can be used, replaced or removed explicitly.
- Rotation and panel resizing preserve the viewed image centre or refit Fit mode.
  Scrollbar limits and thumb dragging agree, including cursor drawing and expanded
  canvas bounds. Legacy offscreen draft views recover safely.
- Reviewed action translations across languages, with pinned AOSP clipboard/Cancel
  terminology and editor-specific corrections. Save / Discard changes / Keep editing
  are distinct. Japanese flip labels retain the correction from the previous build.
- Literary Chinese (lzh-Hant) and traditional Mongolian (mn-Mong) foundations, with
  vertical ribbon labels and bundled Noto Sans Mongolian. Insert text supports
  horizontal and both vertical column orders, mixed/sideways/upright characters,
  joined-word shaping, shared preview/output and persistent settings.

Previous work remains included: DIB/TIFF/ICO/Base64 opening/saving, AVIF, ASCII
export, PDF raster import, PDF/TIFF page selection, animated GIF/APNG/WebP warnings,
Catrobat direct insertion/localized page actions/copyable credits, and the paintbrush
launcher. See REQUEST_COMPLETION.md and CODEC_SUPPORT.md in the matching source.

## Verification

| Check | Result |
|---|---|
| GitHub host checks | 65 passed; 2 skipped |
| GitHub editor regression tests | 232 passed |
| Lint | 0 errors / 0 warnings |
| API 35 device checks | 77 passed |
| Signing / install identity | Valid, certificate matches 0.0.22; version code increases from 75 to 76 |
| Source | 723 repository blobs match the frozen GitHub tree; embedded and downloadable source are identical |
| Native packaging | Four ABIs, expected codecs, 16 KB alignment checked |
| Fonts / launcher | Eleven bundled fonts with notices; source assets match the APK |

Locally, all 232 editor regressions and 67 host checks passed and lint was clean.
After the final locale-resource correction, the targeted language/vertical checks
also passed. Local logs and rendered previews are included in the private backup;
the table above records the exact GitHub build's separate checks.

The initial device run passed 76 of 77 checks; its only failure was an obsolete
font-count assertion after adding Noto Sans Mongolian. The final source updates
both catalogue counts, explicitly checks that font's asset, and retains loading
checks for every font. Historical logs are kept separately in the private backup.

The new language catalogues are partial translations with English fallback and
remain open to native-speaker review. Their ribbon labels support vertical text;
native Android dialogs/edit fields keep platform layout. The document remains
opaque 8-bit SDR sRGB, without layers or animation editing. No physical phone is
attached; ARM performance and manufacturer-specific picker/live-sharing behavior
are not established by emulator checks. SVG editing and layered PSD/OpenRaster
remain significant future format candidates, as described in CODEC_SUPPORT.md.

Keep the private build backup private: it includes the development signing key.

## SHA-256

```text
45b1b51796313dbd39f767326a353b26cbdd2ee2e7412a5fc84794cc19cac418  AN-Paint-0.0.23-development.apk
1cc70d8ce02b8771fc6270f609252e33f133d2e27fc43cc6afad1037d05e56ca  AN-Paint-source.zip
```
