# Image format controls and diagnostics: Old English and Old Norse

Base: `eea893ba3c2f89e2926827ce6dc35e8fd97f30f2` on `review/nv-bottom-2038-20261103`.

Added 20 strings per locale in `values-b+ang` and `values-b+non`: 17 P2 controls/diagnostics plus three P3 descriptions for ICO, Base64 and TIFF. Canonical wording remains in Android resources without approval-text fixtures.

## Context and review

Consumers inspected: `SaveOptionsDialog.kt`, `ImageExporter.kt`, `IcoCodec.kt`, `DibCodec.kt`, `BitmapFileCodec.kt`, `TextImageCodec.kt`, `ImportSelection.kt` and GIF encoding in `LegacyImageEncoder.java`.

- Quality retains its literal percent sign and `formatted="false"` attribute. Lossless labels retain their dynamic format argument. TIFF compression remains lossless Deflate, with possible size reduction and the option to disable it.
- The GIF-only dithering label follows the existing explanation of arranging differently coloured pixels to smooth colour transitions. It does not describe blur or editing source pixels.
- ASCII width counts characters, and inversion swaps light/dark character mapping. Base64 text and ASCII imagery remain separate formats.
- The Base64 description retains the exact `data:image/png;base64,` prefix, lossless PNG storage, reopening guidance and larger encoded size.
- ICO output remains one PNG-compressed image, with proportions preserved and centred on a transparent square. The range is 16–256 pixels, and the selectable list is exactly 16, 24, 32, 48, 64, 128 or 256.
- The ICO dimension error concerns the container's declared image-directory dimensions, not a filesystem folder. The Norse comparison was clarified during review. ICO decode errors retain the image-memory limit.
- BMP/DIB errors retain file-size limits. GIF retains 65,535 pixels per side, not total area. The frame-count fragment remains a lower bound, not an exact count.

Independent semantic and linguistic review accepted all 40 strings after the Norse dimension-comparison clarification. Existing catalogue terminology and functional paraphrases are used; historical computing vocabulary is not claimed.

## Validation and coverage

- All 78 repository host tests passed after the final clarification.
- All 171 offered-language structural checks passed.
- XML parsing, unique typed keys, Android escaping, source attributes, exact placeholder ordering and newline escapes passed. Numeric limits, size lists, Deflate, Base64 prefix and the percent attribute were checked.
- All 501 previous resources and their original bytes per locale are unchanged. Each catalogue now contains 521 typed resources: 520 strings and one plural resource.
- Direct references in the ICO, DIB, bitmap and text codecs, plus the shared import chooser, are now present in both catalogues. Save options still has separate BMP/DIB descriptions and credit labels outside this batch; that whole dialog is not claimed complete.
- Per locale, P2 coverage rises from 154 to 171 of 305; P3 from 4 to 7 of 71. P0 remains 94/94 and P1 249/249.
- All 1,276 materialized base files match remote Git identities/modes. The 166 unmaterialized research/verification records are preserved through the base tree. Only two catalogues and this evidence record are intended publication changes.

No Android build, device/rendering, actual codec execution, runtime plural-routing, external CI or historical-language specialist certification is claimed. No issue1 action was attempted.
