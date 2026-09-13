# AN Paint local.22

Updated 13 September 2026. Package `paint.anpaint.android`, version
`2.14.1-local.22`, version code `75`.

Local.22 completes DIB/TIFF support and adds ICO and Base64 text opening/saving,
ASCII text export, PDF raster import, PDF/TIFF page selection and animated-image
warnings. AVIF opening/saving, including lossless mode, remains supported.
See CODEC_SUPPORT.md for variants and limits. This build updates local.20–local.21
in place with the same signing key.

Local.21 corrects the Japanese horizontal-flip label to 左右反転 and vertical-flip
label to 上下反転. The translation generator preserves this reviewed correction
while retaining the exact upstream source files for provenance. It updates
local.20 in place when signed with the existing key. All local.20 feature changes
listed below remain included.

## Installation identity

This package installs separately from local.15–local.19
(`io.github.c933103.anpaint`). The same signing key is retained, but changing the
package name prevents an in-place update. Earlier private autosaves, undo history,
clipboard and preferences are not migrated. Save needed images as PNG in the old
app and open them in the new app; keep the old installation until that is done.

## Changes in this build

- The pinned colour indicator is the only FG/BG display. Its two colour targets
  open the corresponding picker; its separate arrow expands or collapses the
  swatch panel without duplicating FG/BG controls.
- Custom-colour slots stay visible in Palette, Honeycomb and Advanced. Select a
  labelled slot, edit the colour and use Save/Replace explicitly. Empty slots
  show “+”; hidden cycling and long-press replacement are removed. The four
  preset colours and saved custom colours are preserved within an installation.
- File has one Save as panel with filename, format and relevant encoding options:
  PNG, JPEG, JPEG XL, WebP, HEIC, AVIF, BMP, GIF, DIB, TIFF, ICO, Base64 text and ASCII art. Quality controls appear for
  lossy formats, lossless options where supported, dithering for GIF and a lossless
  compression switch for TIFF. ICO offers size; ASCII offers width/inversion. Android's
  destination picker follows the panel. Save and share uses the same options.
- PDF and TIFF show a preview/page selector; the selected page persists through
  assembly and crop. PDF rasterizes at 144 dpi and saving uses an image format.
- GIF/APNG/WebP imports warn before reducing animation to a still/default image,
  including separate APNG posters and Base64-wrapped or assembly imports.
- ICO and ASCII exports keep the full drawing unsaved and block a pending
  destructive replacement until a full image copy is saved.
- BMP output uses uncompressed 24-bit RGB. GIF output is a single indexed frame,
  limited to 256 colours with optional dithering; it does not add animation.
- Catrobat gallery image use inserts directly. The page header explains credit
  and licence requirements, and each image has local Use image and Copy credit
  actions. Copy all and Edit credits support credits for later distribution;
  saved image credits are also available under Help.
- View > Settings > App language chooses a language independently of the device,
  or restores Use device language. Common terms reuse the original Paintroid
  translations: 73 source files were verified, 42 common terms mapped and 64
  language variants (including English) are selectable, plus Use device language.
  New or untranslated text falls back to English. See TRANSLATING.md
  for the exact inherited sources and partial translation coverage.
- The launcher is an original paintbrush and coloured stroke, with legacy,
  adaptive and themed variants, editable SVG, generated hashes and AGPL credit.
- CI uses bounded asynchronous device tests and a separate, strict native
  compiler cache. Measured cache reuse and its limits are recorded in CI.md.

## Verification status

Release verification is in progress. The final signed APK report will be recorded after build and packaging checks complete.

The implementation entries above are not Android test results. API 35 checks
run independently of APK delivery; API 30 is a separate optional matrix choice.
Previous delivery reports are in verification/HANDOFF_LOCAL20.md and
verification/HANDOFF_LOCAL21.md. Their results must not be reported as fresh
verification of local.22.

## Remaining verification boundaries

No physical phone is attached. Physical installation, ARM runtime performance,
manufacturer picker behaviour, live gallery downloading and sharing to third-party
phone apps have not been verified on a phone. Test reports distinguish substituted
HTTPS transport from a real WebView interaction and from live service use.

The working canvas and exports are opaque 8-bit SDR sRGB. Supported high-bit-depth,
wide-gamut and HDR imports are converted to that document format; see
CODEC_SUPPORT.md for supported colour models and format limits. GIF necessarily
quantizes colours. Animation, layers and HDR output are not part of this editor.

Language choices include inherited partial translations, not newly completed
translations of every AN Paint feature. English fallback is intentional and
identified in the language picker.

Dubai and the file labelled STC remain excluded. The exact-file and public
upstream-history review did not establish an additional grant covering AN Paint.
This does not establish what permission Catrobat relied on. See
FONT-LICENCE-REVIEW.md.
