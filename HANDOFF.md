# AN Paint 0.0.23

Updated 13 September 2026. Package `paint.anpaint.android`, version `0.0.23`,
version code `76`. The existing development signing certificate enables an update
from 0.0.22/local.20–local.22. Earlier package IDs still install separately.

## Changes

- Main, File, Edit, View and Color tabs in both orientations, with the panel
  collapse button on the tabs row. Navigate is first and initially selected.
  Drawing/Selection/Insert group tools; all tool buttons have visible labels.
- Cut/Copy/Paste beside Undo/Redo. Edit has selection, numeric canvas/image sizing,
  touch bounds, crop and image transformations. View contains grid, cursor drawing,
  magnifier, Languages and fullscreen. Drawing settings stay with relevant tools.
  File includes How to use and About / licences / credits.
- Save as offers pixel-preserving formats. Save reuses the successful Save as
  URI/name/format, including after draft recovery when provider permission remains.
  Export as offers lossy/reduced formats and does not change the Save destination,
  clear unsaved changes or complete a pending document replacement. Provider write
  failure leaves the drawing unsaved. Sharing offers all thirteen formats.
- Color contains the palette, Swap and Reset B/W. Choosing a color previews FG/BG
  immediately; Use color confirms and Cancel restores. Add to palette is optional,
  with the same saved colors visible in Color and every picker mode. Palette
  management supports explicit replacement/removal. Unconfirmed preview colors
  are excluded from autosave metadata.
- One scrollbar coordinate model governs drawing, clamping and dragging, including
  expanded canvas bounds and cursor mode. Rotation/panel resizing preserves the
  image-space centre or refits Fit mode. Legacy offscreen pan values refit safely.
- Reviewed clipboard/Cancel terminology from pinned AOSP sources plus
  editor-specific corrections across languages. Distinct Save / Discard changes /
  Keep editing outcomes; Traditional Chinese Cut is 剪下, Apply is 套用. Corrected
  Japanese horizontal/vertical flip labels remain intact.
- Literary Chinese (`lzh-Hant`) and traditional Mongolian (`mn-Mong`) translation
  foundations with vertical ribbon labels. Insert text offers horizontal, vertical
  right-to-left and vertical left-to-right columns, with mixed, sideways or upright
  characters. Preview/output share shaping. Noto Sans Mongolian and its original
  OFL are bundled. Native dialogs retain Android layout; these catalogues remain
  partial translations with English fallback, not fully reviewed translations.

## Retained previous work

All thirteen formats remain available: PNG, JPEG, JPEG XL, WebP, HEIC, AVIF, BMP,
GIF, DIB, TIFF, ICO, Base64 PNG text and ASCII export. PDF raster import and
PDF/TIFF page selection remain, as do animated GIF/APNG/WebP warnings, including
assembly and Base64 input. CODEC_SUPPORT.md records supported variants and limits.
The Catrobat gallery keeps direct insertion, localized page actions and copyable
credits; the paintbrush logo and `paint.anpaint.android` identity remain included.

## Verification

Production Kotlin and app instrumented tests compile locally. Host checks pass
(67 tests). Updated editor regression and current-platform device checks are in
progress; the signed delivery report will record their actual results. Source
implementation is not a claim of a completed runtime test. Prior 0.0.22 delivery
and evidence are recorded in verification/HANDOFF_0.0.22.md.

The document remains opaque 8-bit SDR sRGB, without layers or animation editing.
No physical phone is attached. ARM performance, manufacturer-specific document
providers and live gallery/sharing on a phone require device verification. Dubai
and STC remain excluded; see FONT-LICENCE-REVIEW.md. See REQUEST_COMPLETION.md for
an implementation mapping and CI.md for independent build/test delivery.
