# AN Paint local.17 continuation

Updated 12 September 2026. Development resumed after the explicitly unfinished
local.16 handoff. The previous snapshot and its failed JPEG XL test remain
recorded in [HANDOFF_LOCAL16.md](verification/HANDOFF_LOCAL16.md).

Target package: `io.github.c933103.anpaint`, version `2.14.1-local.17`, version
code `70`, using the existing AN Paint signing identity.

## Completed implementation

- Corrected the JPEG XL 2048-pixel callback failure with streaming output and
  valid rectangle handling. Tests now cover larger tall/wide images, crops,
  lossless pixels, lossy encoding and exhausted-memory recovery.
- Added HEIC and AVIF import/export with bundled source-built codecs, and true
  lossless/adjustable-quality WebP export on all supported Android API levels.
  [CODEC_SUPPORT.md](CODEC_SUPPORT.md) records controls and format limitations.
- Unified Save as/Save and share format options. HEIC has adjustable quality;
  JPEG XL, WebP and AVIF also offer lossless output.
- Added decoder-specific HEIC/AVIF memory estimates to the resize prompt,
  admission check and decoder allowance, including source/tile work that cannot
  be removed by choosing a tiny output.
- Corrected the five previously reported lint issues in launcher resources and
  Android backup rules. Kept physical sidebar/palette geometry coherent in RTL
  layouts and added numeric-input/RTL layout regression checks.
- Rechecked the original editor's standalone functions and every requested
  consolidation item in [EDITOR_PARITY.md](EDITOR_PARITY.md). No further
  standalone editing command was identified without a retained equivalent or
  an explicit requested removal.
- Finished exact Dubai/STC identity and licence investigation. The old STC file
  is Boutros GE SS Text Light; neither font can be restored under the terms
  found. See [FONT-LICENCE-REVIEW.md](FONT-LICENCE-REVIEW.md) and the retained
  [binary metadata](verification/legacy-font-metadata.json). The old fallback
  test names were misleading; current font tests use the actual catalogue.
- Added installed-app emulator checks for document-picker intents, real
  FileProvider imports/exports, sharing, format choices, drawing controls,
  cursor/magnifier/Fit and gallery launch.
- Included the pinned native codec sources and complete notices in the offline
  source export, with scripts for modification and relinking.

## Verification status

The combined local.17 Android build and tests are in progress. A release
verification report will replace this paragraph after the final APK is checked.
No intermediate CI checkpoint is a verified release.

## Physical-device and external-service limits

No physical ARM phone is attached to this workspace. A four-architecture build
and emulator tests do not establish physical-phone runtime verification. Actual
phone installation/update, the system picker, sharing to third-party apps,
performance on large images and live gallery downloading should be exercised
on a physical device. Gallery launch tests intercept the remote activity and do
not establish the live service's availability or every gallery item's behavior.

Translation preparation is complete for the requested scope: resource strings,
plurals, stable identifiers, locale-aware input, and layout guidance. Human
translations into unspecified languages are not claimed. They can be added and
reviewed when target languages are chosen.

Dubai/STC research is complete under the terms located. Restoration requires
additional documented permission, not another missing-metadata check. No rights
holder was contacted and no licence was purchased.
