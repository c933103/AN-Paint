# AN Paint local.22 — expanded formats and page import

Packaged and checked 13 September 2026. Version **2.14.1-local.22**, version code
**75**, package **paint.anpaint.android**.

Application/source commit: [bd146bd8d7c0c711e4d9b1b3c5b95d24aa94b898](https://github.com/c933103/AN-Paint/commit/bd146bd8d7c0c711e4d9b1b3c5b95d24aa94b898).
Build and checks: [run 34734921901](https://github.com/c933103/AN-Paint/actions/runs/34734921901).
This is a development build; completed and pending checks are distinguished below.

## Added formats and import controls

| Request | Available behaviour | Scope and limits |
|---|---|---|
| DIB open/save | Opens validated packed DIB; saves a true packed 24-bit RGB DIB | Export is uncompressed and has no BMP file header. Use BMP when another program requires that header. |
| TIFF open/save | Opens `.tif` and `.tiff`; saves one opaque RGB page with lossless Deflate or no compression | A page selector chooses the page to edit. CMYK, Lab, floating-point/log samples and non-JPEG YCbCr are not supported. |
| ICO open/save | Opens the best supported PNG or classic DIB icon entry; saves one PNG-compressed entry | Choose 16, 24, 32, 48, 64, 128 or 256 pixels. Export centres the proportional image on a transparent square. |
| AVIF open/save | Retains the existing bundled AVIF decoder and encoder | Lossless mode or adjustable quality; editing remains 8-bit sRGB SDR. |
| Base64 text open/save | Decodes supported image data from Base64 text; exports a PNG data URI in `.txt` | Base64 increases file size. It is an image representation, not arbitrary text rendering. |
| ASCII art export | Writes an image rendition using light and dark text characters | Width 40–240 columns and optional inversion. View in a monospaced font. This text cannot restore the original drawing. |
| PDF page import | Choose and preview one page, then open it as an editable image | Rendered at 144 dpi using Android's PDF renderer. Text/vector objects become pixels; this does not edit or save PDF documents. |
| PDF/TIFF page selector | Page number, previous/next controls, preview and selected-page import | Documents may contain 1–4096 pages. One selected page is edited; saving does not rewrite the original multipage document. |
| Animated GIF/PNG/WebP warning | Multi-frame inputs require acknowledgement before still-image import | Opens the first frame, or the separate default image of a PNG when present. Animation is not retained when saving; a scan-limit uncertainty also prompts before import. |

File → Save as offers thirteen choices: PNG, JPEG, JPEG XL, WebP, HEIC, AVIF,
BMP, GIF, DIB, TIFF, ICO, Base64 text and ASCII art. Filename, format and relevant
quality, lossless, dithering, TIFF compression, ICO size or ASCII controls are in
one panel before Android's destination picker. Save and share uses these options.
ICO and ASCII exports do not mark the full drawing as saved and do not complete a pending close/replacement; keep a full image copy too.

The shared import workflow is used for opening, inserting and image assembly,
including page choice and animation warnings. PDF and Base64 text are also
registered with Android's view/edit/share entry points. Inputs are staged in
private temporary files, capped at 512 MiB; device memory limits may require
smaller imported dimensions. The original file is not changed during import.
PDF passwords/encryption and features unsupported by the device renderer fail
with an explanation; no password-entry workflow is included.

TIFF supports classic TIFF and BigTIFF in either byte order, strips/tiles,
contiguous/separate planes, all eight orientations, supported integer
bilevel/palette/grayscale and RGB samples, alpha, and common compression.
Supported RGB/grayscale ICC profiles are converted to sRGB. The precise accepted
layouts, colour limitations and source provenance are documented in
`CODEC_SUPPORT.md` in the corresponding source ZIP. TIFF export is a single
opaque 8-bit RGB page. DIB/BMP/GIF colour-profile restrictions still apply.

## Previous task retained and completed

The local.21 implementation audit is recorded in
[the previous handoff](https://github.com/c933103/AN-Paint/blob/develop/verification/HANDOFF_LOCAL21.md).
Its requested changes remain in this release:

| Earlier request | Implemented state |
|---|---|
| Colour selection panels | The expansion omits repeated FG/BG targets; advanced custom colours use visible slots and explicit save/replace actions. |
| Unified Save as and BMP/GIF | One options panel includes filename, format and applicable controls. The new formats extend that panel. |
| Sticker insertion and credits | Repeated use confirmation is removed. The description and copyable image/all-image credits explain attribution, and image-use buttons follow the app language. |
| Language choice and upstream wording | Settings offers device default and 64 language variants, reusing matching Paintroid terms. Untranslated text falls back to English. |
| Replacement logo | The new simple brush-and-colour icon includes legacy, adaptive and themed variants with editable artwork. |
| Package name | `paint.anpaint.android`. |
| Japanese flip correction | Horizontal is **左右反転**; vertical is **上下反転**. Both compiled values are checked in the signed APK, and generation retains the correction. |

The first expanded-format attempt passed all 77 Android emulator tests and had
zero lint issues. Its local regression suite exposed Android accepting a damaged
embedded PNG in an ICO. The delivered source adds strict bounded pixel-stream
validation, retaining valid packed, 16-bit and Adam7 icons. Earlier-attempt evidence
is saved separately and is not substituted for this build's check results.

## Formats still outside the app

The common still-image interchange formats are covered. SVG raster import is the
most useful remaining general-purpose addition; it would need a vector renderer
and explicit raster-size controls. Layered PSD/Krita documents and camera RAW
would require separate layer or raw-development workflows, so this release does
not claim those capabilities. Animated-image editing/export and multipage
PDF/TIFF saving are also outside the current single-canvas editor.

## Verification for this delivered build

| Check | Actual result |
|---|---|
| Local host checks | **65 passed**, zero failures/errors/skips |
| TIFF native host checks | 142 fixture/crop/encode checks + 44 page/index/chain checks; 0 failures. Android/JNI bitmap calls use host stubs. |
| Android regression suite | **221 passed**, zero failures/errors/skips |
| API 35 emulator | **77 passed**, zero failures/errors/skips |
| Lint | 0 errors, 0 fatal issues, 0 warnings |
| APK compilation | CI APK artifact and recorded checksum verified for the commit above |
| APK signing and upgrade | Valid signature; same certificate as delivered local.21; package unchanged and version code increased from 74 to 75 |
| Japanese and format resources | Compiled Japanese flip labels and the new format/page/animation controls checked against their frozen source values |
| Corresponding source | APK-embedded source and supplied ZIP are byte-identical; repository bytes match the built commit under the documented source-export exclusions |
| Native source and notices | Pinned JPEG XL, WebP, HEIF/AVIF and TIFF/JPEG source trees included; packaged font/legal assets equal the source archive |
| Native builds/alignment | ARM64, ARMv7, x86 and x86_64 include all four codec bridges; APK and ELF segments pass 16 KiB alignment checks |
| API 30 rerun | Not rerun for this build |
| Physical phone testing | Not performed |

Counts above come from this build's verification artifacts. Packaging checks
establish file identity and included resources; they do not substitute for any
pending runtime checks. Detailed machine-readable results and test XML are in
the private backup's `verification` folder.

## Installation and practical limits

Install local.22 over local.21 or local.20. The application ID and signing key are
unchanged, and version code increases to 75. Builds local.15–local.19 used
`io.github.c933103.anpaint` and remain a separate app; export needed images from
those installations and reopen them here. Their private drafts/settings are not
automatically migrated across that older package change.

The canvas is opaque 8-bit sRGB SDR. Supported wide-gamut/HDR inputs are converted
for that canvas; exports cannot restore source layers, vector objects, metadata,
higher precision, HDR headroom or animation. GIF export is one indexed frame.
Large source strips, tiles or PDF documents can exhaust the memory budget even
when a smaller output is requested. Android manufacturer picker behaviour,
live gallery use and third-party sharing remain unverified on a physical phone
unless explicitly recorded above.

The pending-build note inside the frozen source's `HANDOFF.md` is superseded by
this post-build report. The public CI APK uses a temporary CI signing key; install
the separately signed delivery to preserve compatibility with future updates.

## SHA-256

```text
18b41f62da3b3831d0da47542df6fdcf2c98b1dd15a6016536a40a340a19c421  AN-Paint-2.14.1-local.22-development.apk
f0e904da3055019a3d84803075f6e596786e65385cf4a2ba1ac7bbc800486708  AN-Paint-source.zip
```

The private build backup contains the signing key and must not be published.
