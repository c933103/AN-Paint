# AN Paint 0.0.22 — version-name update

Prepared 13 September 2026. The displayed version changes from
**2.14.1-local.22** to **0.0.22**. The application ID remains
**paint.anpaint.android**, Android version code remains **75**, and the signed
APK uses the same certificate as the correctly signed previous local.22 release.

Source: [736458728b5a87d04a5ff9164013796db1be4d70](https://github.com/c933103/AN-Paint/commit/736458728b5a87d04a5ff9164013796db1be4d70).
Current build: [run 34736090966](https://github.com/c933103/AN-Paint/actions/runs/34736090966).

The published change modifies only `build.gradle`, `README.md` and `HANDOFF.md`; there are no deleted files. The saved remote-tree comparison records the before/after blob hashes. Packaging also compares
353 application source/resource files
with the previous APK's embedded source and requires identical bytes.

## Completed features retained

The previous UI, colour-panel, custom-colour slots, unified Save as, sticker
credits/copy controls, gallery-button translation, language selection, replacement
logo and package-name work remains included. Japanese horizontal and vertical
flip labels remain **左右反転** and **上下反転**, respectively; the signed APK's
compiled labels are checked again.

The thirteen Save as choices remain PNG, JPEG, JPEG XL, WebP, HEIC, AVIF, BMP,
GIF, DIB, TIFF, ICO, Base64 text and ASCII art. DIB/TIFF/ICO/Base64 open and save,
PDF raster import, PDF/TIFF page selection, and animated GIF/APNG/WebP warnings
remain included. AVIF open/save remains available.

TIFF edits one selected page and saves one RGB page with lossless Deflate or no
compression; unsupported CMYK/Lab/float variants remain outside the decoder.
PDF pages are rasterized at 144 dpi, with a selector for documents of up to
4096 pages; this does not add PDF export. ICO saves one PNG-compressed entry at
16–256 pixels. Base64 text exports a PNG data URI. ASCII art offers 40–240 columns
and inversion. ICO/ASCII exports do not mark the full drawing as saved.
Animation is not retained when an image is opened and saved. The complete format
scope and limits remain in `CODEC_SUPPORT.md` in the corresponding source ZIP.

## Checks for this 0.0.22 build

| Check | Actual result |
|---|---|
| Current host tests | **63 passed**, 2 skipped, zero failures/errors |
| Current Android regression suite | **221 passed**, zero failures/errors/skips |
| Current API 35 emulator | Pending/not downloaded |
| Current lint | 0 errors, 0 fatal issues, 0 warnings |
| APK compilation and identity | CI artifact checksum matches the recorded build; package, version name, code and provider identity checked |
| Signing | Valid signature; certificate matches the previous local.22 release; version code remains 75 |
| Corresponding source | Delivered and APK-embedded source ZIPs are byte-identical and match the frozen Git tree under the documented export exclusions |
| Native codecs | JPEG XL, WebP, HEIF/AVIF and TIFF bridges present for ARM64, ARMv7, x86 and x86_64 |
| Alignment and assets | APK/ELF 16 KiB alignment, launcher pixels, fonts, legal notices and compiled format/page/animation resources checked |

Pending or absent current-run evidence is labelled above; previous results do
not replace it. The CI host suite skips two optional Pillow image checks when
Pillow is unavailable; the skip count is reported above. No physical-phone test
is claimed for this version-name update.
The machine-readable report and available test XML are in the private backup.

## Previous release results, kept separate

The earlier **2.14.1-local.22** release was built from
[bd146bd8d7c0c711e4d9b1b3c5b95d24aa94b898](https://github.com/c933103/AN-Paint/commit/bd146bd8d7c0c711e4d9b1b3c5b95d24aa94b898) in
[run 34734921901](https://github.com/c933103/AN-Paint/actions/runs/34734921901).
Its results are historical evidence only and are not counted as results of the
new version-name build.

| Previous-release check | Recorded result |
|---|---|
| Host tests | **65 passed**, zero failures/errors/skips |
| Android regression suite | **221 passed**, zero failures/errors/skips |
| API 35 emulator | **77 passed**, zero failures/errors/skips |
| Lint | 0 errors, 0 fatal issues, 0 warnings |

## Installation

Install this separately signed APK to replace the previous local.22 development
build. The package, version code and signing certificate match, so the version
name itself does not represent a version-code downgrade. Device-specific
installer behaviour has not been tested on a physical phone. The public CI APK
uses a temporary signing key; use this delivery for continuity with earlier
signed development builds.

This post-build report supersedes pending-build wording inside the frozen
source's `HANDOFF.md`. The private backup contains the signing key and must not
be published.

## SHA-256

```text
4dc7df0464186a2caefff8c7c51f85717e783928ef02cc86fb8712f87c55f48e  AN-Paint-0.0.22-development.apk
9a8f43f6dfbf790a69e05481e0b256e708631b0e462b51c165660bc7e53e629b  AN-Paint-source.zip
```
