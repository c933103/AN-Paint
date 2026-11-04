# Interlingua assembly sizing, output and errors

Base: `646c7fd6581eeed8161095803faaf4b7b2342a8f` on `review/nv-bottom-2038-20261103`.

Added 41 missing P2 resources to the canonical Interlingua catalogue and corrected one existing attachment term. The catalogue now contains 560 typed resources. The other 518 previous resources and their attributes remain unchanged.

## Scope and review

The batch covers common width/height, percentage and pixel sizing, restoration of original dimensions, output creation and memory estimates, completed-image progress, preview failures and placement/attachment errors. Normalization preserves each image's aspect ratio, original files and crop settings. Percentage sizing uses the largest current dimension on the selected axis. Snapping rejects overlap; anchor-image errors remain distinct from missing or unplaced selected images.

Independent review checked all 41 additions. Five percentage terms were corrected to `percentage`; six attachment terms were corrected to `attachar`, `attachate` or `attachamento`. The same attachment correction changes only `attaccar` to `attachar` in the existing workspace caption. References: [percentage usage](https://www.interlingua.com/linguistic/pro-cento-e-non-pro-centos/) and [lexical corrections](https://www.interlingua.com/archivos/Qualque%20observationes%20lexical%20pro%20usatores%20de%20Interlingua.pdf).

Of the additions, 33 have exact direct production references in the assembly activity, canvas, model, renderer, normalization dialog or editor. Eight retained priority-manifest resources have no direct production reference and were reviewed against canonical English only: the older generic same-dimension, common-unit, percentage, dimension-range and width-list captions, plus the preview-memory error. No runtime-use claim is made for those eight. No implementation, English wording, other locale, font or licence body changed. Canonical Android resources own the wording; no full-prose approval mirror or permanent per-batch test fixture is introduced.

## Verification

- 78 affected host tests pass after the final review corrections: translations, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary priority follow-through and open-review recovery.
- All 171 offered options and the priority manifest pass structural validation.
- All 84 English/Interlingua resource-render checks pass for the 41 additions and one corrected resource. XML/Android escaping, source attributes, ordered argument types, escaped newlines and numerals are preserved.
- All 1,252 materialized base files match the freshly verified remote tree's Git blob hashes and executable modes. Its 231 unmaterialized non-tree entries are retained unchanged.
- Direct priority presence: P0 94/94, P1 249/249, P2 208/305, P3 9/71. Remaining: 159 keys (97 P2 and 62 P3), down from 200. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, installed layout, device, accessibility/runtime, CI or native-speaker certification is claimed. Publication uses the exact expected parent and a non-force lease, with final remote tree and changed-file readback verification required before reporting success. Remaining crop controls, gallery/credit messages, format options and help text are candidates for subsequent coherent batches.

