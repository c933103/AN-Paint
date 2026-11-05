# Interlingua crop controls, import memory and output formats

Base: `c1c3e4f21a1255c5a41b48b27cc937a8846bf617` on `review/nv-bottom-2038-20261103`.

Adds 33 missing priority resources to the canonical Interlingua catalogue: 27 P2 controls/errors and six P3 explanations. All 560 previous typed resources and their attributes remain unchanged; the catalogue now contains 593 typed resources.

## Scope and review

The batch covers grouped cropping and source preservation, import-size memory estimates, ASCII and Base64 options, DIB/BMP/ICO/TIFF descriptions and failures, the GIF dimension ceiling, tagged-colour conversion advice, and JPEG XL/WebP/HEIC/AVIF save captions. Numeric limits, format identifiers, `data:image/png;base64,`, typed placeholders and escaped newlines are preserved. TIFF compression remains optional and lossless; its file-size reduction is conditional. Import estimates still distinguish variable actual memory use, definite detail loss for smaller copies, and unchanged source files.

Independent linguistic and semantic review checked all 33 entries against canonical English and available production consumers. The GIF limit uses `65.535`, preserving the integer 65535 with Interlingua grouping rather than a comma that Interlingua reads as a decimal separator; see the [UMI cardinal-number grammar](https://www.interlingua.com/grammatica/grammatica/cardinales/).

The raw megapixel cap explicitly excludes decoder overhead; the estimate is not a guarantee that an input fits after decoding costs.

Twenty-seven additions have exact direct production references in the crop/resize/output dialogs, image assembly, editor or codecs. Six retained manifest entries have no exact direct production reference and were checked against canonical English only: the older tagged-colour warning, generic import-memory explanation, lossless JPEG XL caption and three format-specific save captions. No runtime-use claim is made for those six. No implementation, English resource, other locale, font or licence body changed. No permanent per-batch test fixture or copied prose approval mirror is introduced.

## Verification

- 116 affected host tests pass: localization structure/contracts/boundaries/priority follow-through and relevant crop, memory, TIFF, ICO, DIB and animation-warning regressions. This is the named affected subset, not the entire repository test suite.
- All 171 offered options and the priority manifest pass structural validation.
- All 66 English/Interlingua Java resource-format checks pass for the 33 additions. Source attributes, ordered argument types, escaped newlines, numeric values and protocol tokens are preserved.
- All 1,252 materialized base files match the freshly verified remote tree's Git blob hashes and executable modes. Its 232 unmaterialized non-tree entries are retained unchanged.
- Direct priority presence: P0 94/94, P1 249/249, P2 235/305, P3 15/71. Remaining: 126 keys (70 P2 and 56 P3), down from 159. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, installed-layout, device, accessibility/runtime, CI or native-speaker certification is claimed. Publication uses the exact expected parent and a non-force lease, followed by final remote tree and changed-file readback verification. Gallery/credit messages and the remaining drawing/help text are candidates for subsequent coherent batches.
