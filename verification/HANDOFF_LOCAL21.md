# AN Paint local.21 — Japanese correction and request audit

Verified 13 September 2026. Version **2.14.1-local.21**, version code **74**,
package **paint.anpaint.android**.

Application/source commit: [cf2a95522f9f7f978f9656d639ad74fcbfbe85e8](https://github.com/c933103/AN-Paint/commit/cf2a95522f9f7f978f9656d639ad74fcbfbe85e8).
Build and checks: [run 34731555352](https://github.com/c933103/AN-Paint/actions/runs/34731555352).

## Japanese flip correction

| Operation | Corrected label | Operation performed |
|---|---|---|
| Horizontal flip | 左右反転 | Left and right swap |
| Vertical flip | 上下反転 | Top and bottom swap |

The compiled APK resources contain the corrected Japanese values. The generator
also applies the correction, so regeneration cannot restore the swapped labels.
It checks the original values before applying a correction, requiring review if
the upstream translation changes. Original upstream XML and its provenance hashes
remain intact; the coverage inventory distinguishes the two local corrections.

## All quoted requirements checked

| Request | Implementation confirmed |
|---|---|
| Remove repeated FG/BG from expanded side panel | The pinned indicator contains the colour targets; the expansion contains swatches and recent colours. |
| Improve advanced custom-colour selection | Sixteen visible slots, selected-slot outline and heading, empty-slot + signs, and explicit Save to slot / Replace slot. Clicking a saved slot loads its colour. |
| Unified Save as panel | One File-menu entry opens filename, format and applicable quality/lossless/dithering controls together, followed by Android's destination picker. Save and share uses the same panel. |
| BMP and GIF | Both are included among PNG, JPEG, JPEG XL, WebP, HEIC, AVIF, BMP and GIF. BMP exports 24-bit RGB; GIF exports a single frame of up to 256 colours with optional dithering. |
| Remove repeated sticker confirmation | Gallery image/download actions start insertion directly. The dedicated regression checks absence of the confirmation dialog. |
| Attribution at top and copyable credit | A scrollable description above the gallery explains source notices, attribution, modification descriptions and ShareAlike. Per-image Copy credit plus Copy all/Edit credits provide reusable attribution. Saved-image credits are accessible from Help. |
| Localize gallery image-use buttons | The app replaces the relevant German website download captions using its current language resources and adds localized credit controls. |
| User-selected language and upstream vocabulary reuse | View → Settings → App language offers device default and 64 language variants. The inventory maps 42 common terms and verifies all 73 original upstream translation files. Android 13 system-language settings are integrated. |
| New simple all-age logo | The manifest uses the new rounded brush and coloured strokes, with editable SVG plus legacy, adaptive and themed variants. The actual launcher PNG was visually reviewed; aesthetic preference remains subjective. |
| Package name | Application ID is paint.anpaint.android. |

The audit examined implementation, relevant regression coverage and rendered
colour, Save as and launcher images. No quoted feature remains unimplemented.
This does not mean all languages are fully translated or every live-device
interaction has been tested.

## Verification of local.21

| Check | Result |
|---|---|
| Local host checks | 23 passed, including translation regeneration/provenance checks |
| Android regression suite | **201 passed**, zero failures/errors/skips |
| API 35 emulator | Pending at packaging; previous-build results are not substituted |
| Lint | 0 errors, 0 warnings |
| Compiled Japanese flip strings | Correct horizontal and vertical labels verified in the signed APK |
| APK signing | Valid signature; same certificate as delivered local.20 |
| Corresponding source | APK-embedded source and supplied source ZIP are byte-identical and match the built Git commit under the documented source-export rules |
| Packaging | Package/version/provider identity, fonts, legal notices and launcher pixels checked |
| Native builds/alignment | ARM64, ARMv7, x86 and x86_64 included; APK and ELF segments pass 16 KiB alignment checks |

## Installation and limits

Install local.21 over local.20: the package and signing certificate are unchanged,
and version code increases from 73 to 74. Builds local.15–local.19 used
io.github.c933103.anpaint and remain a separate app. Save needed images from those
older installations as PNG and open them here; private drafts/settings are not
automatically migrated across that older package change.

Translations remain partial, with English fallback. Copied gallery credits include
the available title, publisher, source and licence; edit them to describe your
changes or name a separately credited creator when the source requires it.
BMP is uncompressed 24-bit RGB; GIF is a single indexed frame. The editor's canvas
and exports remain opaque 8-bit sRGB SDR. Supported wide-gamut/HDR imports are
converted to that canvas format.

API 30 was not rerun for this label correction. No physical-phone/ARM runtime test
was performed; manufacturer picker behaviour, live gallery use and sharing to
third-party phone apps remain unverified on a phone.

The pending-build note inside the frozen source's HANDOFF.md is superseded by
this post-build verification report. The public CI APK uses a temporary CI signing
key; use the separately signed delivery for consistent future updates.

## SHA-256

```text
48489cb28b22c89426c4419c15ac2395863e3cbfc94f7f45b4ec00aaf589aaf2  AN-Paint-2.14.1-local.21-development.apk
e821cb6530ceef60bb9ed16f865cb7e2a74c20fd1bf8ae5ec50fbf9af00e8d91  AN-Paint-source.zip
```

The private build backup contains the signing key and must not be published.
