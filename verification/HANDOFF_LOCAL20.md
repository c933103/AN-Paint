# AN Paint local.20 — completed delivery

Verified 13 September 2026. This report supersedes the pending verification text in the source snapshot's HANDOFF.md.

- Version: **2.14.1-local.20**; version code **73**.
- Android package: `paint.anpaint.android`.
- Built application/source commit: [8a11d029537a5e7fe9046f55fec2cfe7fab7e456](https://github.com/c933103/AN-Paint/commit/8a11d029537a5e7fe9046f55fec2cfe7fab7e456).
- [GitHub Actions run 34708564178](https://github.com/c933103/AN-Paint/actions/runs/34708564178): all three jobs completed successfully.
- Final signed APK: `AN-Paint-2.14.1-local.20-development.apk` (143,536,764 bytes).

## Installation

The new package installs beside local.15–local.19, whose package was `io.github.c933103.anpaint`. It cannot update that installation despite retaining the same signing certificate. Save needed images as PNG in the old app and open them in the new app. Private drafts, clipboard, undo history and settings are not automatically migrated; keep the old app until the transfer is complete.

## Requested changes included

| Request | Delivered behaviour |
|---|---|
| Colour side panel | FG/BG controls appear only in the pinned indicator; its extension holds swatches. |
| Custom colours | Select a visible slot, edit the colour, and explicitly save or replace it. Slots remain available in the advanced picker. |
| Save as | One panel for filename, format and relevant quality/lossless/dithering settings. PNG, JPEG, JPEG XL, WebP, HEIC, AVIF, BMP and GIF are offered. |
| Catrobat gallery | Direct insertion, attribution guidance at the top, copyable credits and localized image actions. Saved-image credits are accessible from Help. |
| App language | View → Settings → App language, with device-language fallback and 64 selectable language variants. Common terms reuse upstream translations; coverage remains partial. |
| Launcher | New brush and coloured-stroke artwork, including adaptive/themed variants and editable SVG source. |
| Package name | `paint.anpaint.android`. |
| Final fixes | Locale override now preserves rotation and text scaling. Save-dialog instrumentation checks the actual destination-picker request and cancellation. |

## Verification

| Check | Result |
|---|---|
| Regression suite | **201 passed**, zero failures/errors/skips |
| Android 15 / API 35 emulator | **47 passed**: 39 native/codec tests and 8 installed-app tests; zero failures/errors/skips |
| Lint | **0 errors, 0 warnings** |
| APK signing | Signature verifies; certificate matches the previously delivered AN Paint key |
| Corresponding source | APK-embedded and delivered ZIPs are byte-identical; 600 packaged repository files match their Git blobs at the built commit |
| Offline native sources | 4,584 additional files included under the three documented codec-source directories |
| Packaging | Application ID/version, provider identity, 10 bundled fonts, legal notices and launcher PNG pixels checked |
| CPU and page alignment | ARM64, ARMv7, x86 and x86_64 included; APK and native ELF segments pass 16 KiB alignment checks |

The source bundle intentionally omits two .gitignore files and one IDE code-style file under the existing build rules. No application source mismatch was found. No new Android build or emulator run was necessary during recovery; the already-completed exact-commit artifacts were downloaded, their published digests verified, and the universal APK was signed privately. The public CI artifact uses its temporary CI certificate, so use the separately signed delivery for consistent future updates.

## Known issue and verification limits

- Japanese horizontal-flip and vertical-flip menu labels are inherited in reverse. The underlying operations are correct. This is recorded as an outstanding translation correction, not fixed in this APK.
- Language choices include partial upstream translations; new untranslated text falls back to English.
- This build was not rerun on API 30. No physical phone or ARM device runtime test was performed. Manufacturer pickers, live gallery downloads and sharing to third-party phone apps still need physical-device checks.
- BMP saves 24-bit RGB; GIF saves one indexed frame with up to 256 colours. The canvas is opaque 8-bit sRGB SDR. Supported high-bit-depth, wide-gamut and HDR imports are converted to that format. Animation, layers and HDR output are outside the current editor.

## SHA-256

```text
36a9f4f287945487b1f1cae2a99b7a59a9479c58e5e11ba54b4d4b00553f8199  AN-Paint-2.14.1-local.20-development.apk
d2c014f8ae2a98ccf9b25d042d630d65e61df89031525a940f65ec5dae7e7916  AN-Paint-source.zip
```

Signing-certificate SHA-256: `f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`.

The private build backup includes the signing key and must not be published. Program source remains available at the exact commit above; this completion report is post-build documentation.
