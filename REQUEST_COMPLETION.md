# Request completion audit — local.20

This audit rechecks the actual source and regression coverage against the user's
requests, rather than treating the prior release notes as proof of completion.
The detailed original-editor mapping remains in EDITOR_PARITY.md. The signed
build's actual verification status belongs in HANDOFF.md and its verification
report; implementation coverage does not imply physical-phone verification.

| Requested area | Completion / location |
|---|---|
| Copyleft icons; distinct app identity | KDE Breeze LGPL icons with original SVGs and generated hashes. Local.20 replaces the old monogram with an original AGPL paintbrush/stroke launcher. Package `paint.anpaint.android` installs separately from prior builds; copyright and source remain in Help. |
| Material Design 3 colour scheme | Local.19 replaces the remaining old cream/blue UI chrome with shared Material 3 colour roles. Image pixels, brush colours and palette swatches keep their actual values. |
| Pencil and brush widths | Pencil has independent 1–100 px width. Brush, Watercolor, Airbrush and Eraser have adjustable sizes and exact numeric entry. |
| Tool grouping and orientation | Brush, Selection and Insert categories remember their chosen tool. Landscape keeps tools left and opens options right; portrait places tools below the toolbar and opens options downward. |
| Requested drawing/selection additions | Watercolor; Heart/Star/Arrow; polygon double-tap completion; rounded-corner radius; corner/edge resize and rotation for rectangle and free-form masks; Select all and two-column clipboard controls. |
| Navigation | Pinch/pan, cursor drawing, magnified preview, 100% zoom tick/step stop and centred Fit. Local.19 also autosaves a magnification-only setting change while the editor stays open. |
| Canvas size and assembly | Pixel/percent controls and aspect locks; touch trim/expand on all sides; up to 20 assembly inputs, name/time sorting, individual/batch crop, normalization, single-image Unplace with gap closing, drag/snap preview and PNG/save-to-Paint transfer. |
| Colours | FG/BG appear once in the pinned indicator, with separate picker targets and expansion arrow. Expanded swatches retain four recent cells. Palette/Honeycomb/Advanced share visible custom slots with explicit Select, Save and Replace behavior; empty slots show “+”. Presets remain available. RGB/HSV/HSL numeric entry uses the selected locale. |
| Import and memory | File picker opens without broad photo permission; explicit oversized-image choice with dimensions, pixel count and memory estimates; source files unchanged. Supported ICC/high-bit-depth/HDR input converts to SDR sRGB before compositing alpha. |
| Formats and export | One Save as panel contains filename, eight formats and applicable encoding options. PNG, JPEG, JPEG XL, WebP, HEIC and AVIF are joined by 24-bit BMP and single-frame GIF with at most 256 colours and optional dithering. Save and share uses that panel and saves before opening the share chooser. Filename extensions follow format changes. See CODEC_SUPPORT.md for limits. |
| Existing-image insertion and gallery | File > Insert image into canvas; Catrobat gallery directly below. Image use inserts directly without recurring confirmation. Local page actions use the selected app language. Header guidance explains attribution and ShareAlike; each image offers Copy credit, with Copy all and Edit credits for distribution. Download cancellation, transparent-pixel insertion and credits retain regression coverage. |
| Recovery and editing history | Atomic autosave/recovery, recoverable pending geometry, disk-backed undo/redo and unavailable-action states. |
| Font and licence UI | Actual-font previews, 19 named choices, ten bundled OFL fonts, complete credits and fixed licence footer with Copy all. Dubai/STC review examines exact binaries, public terms and upstream introduction history; their redistribution rights for AN Paint remain unestablished. |
| App language and inherited translations | View > Settings > App language offers 64 locale variants (including English), plus Use device language. All 73 upstream translation source files are verified against pinned Git blobs; 42 equivalent common terms are mapped into new controls. Variants with no mapped translations are excluded. Android 13+ uses the same app-language setting as Android; older versions retain the preference internally. Partial translations fall back to English. |
| Original editor removal | Original activity, layers, document transparency controls, Smudge, automatic crop and public project formats removed. Retained editing commands are mapped to the new view in EDITOR_PARITY.md. Internal selection masks and transparent input compositing remain necessary image operations. |

## Boundaries that cannot be labelled complete by a source change

- The working document and exports are opaque 8-bit SDR sRGB, as requested.
  HDR import produces an SDR rendition, not HDR editing/output. Unsupported
  colour models are rejected visibly; they are listed in CODEC_SUPPORT.md.
- Physical-phone installation, manufacturer-specific picker behaviour and ARM
  runtime performance require an attached device. No such device is available.
- The live Catrobat gallery is an external service. The source page and an image
  URL can be checked independently; this is distinct from a physical-phone live
  download. Deterministic end-to-end download/insertion tests are identified as
  such, not presented as a physical-device/network test.
- The language picker is partial translation coverage. It does not claim a new
  complete translation of all AN Paint controls; unmapped terms remain English.
- GIF output is still-image, indexed colour. Animation editing and HDR output
  are not added by supporting additional formats.
- Public history does not establish what font permissions Catrobat relied on.
  No rights holder was contacted or additional font licence obtained. Excluding
  the two files is a decision about rights established for AN Paint; it is not
  an accusation about the upstream distributor.

Long device testing is asynchronous under CI.md. Pending/failed checks remain
visible in the release report and do not disappear merely because an APK exists.
