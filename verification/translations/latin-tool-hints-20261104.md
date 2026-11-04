# Latin tool gestures and canvas bounds help

## Scope and review

- Base: `d405edbc0241060519c908b23516d8458db1045b` on `review/nv-bottom-2038-20261103`.
- Add 19 P3 Latin resources: 18 production drawing-tool hints and the canvas expansion/trimming hint. All 663 previous Latin resources remain unchanged.
- Independent linguistic and UI-context review accepted all 19 unchanged. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`.
- Inspected `PaintTool` hint mappings in `PaintDocument.kt`, actual option/help and canvas-bounds consumers in `ClassicPaintActivity.kt`, and gesture stages, selection transforms and rounded-radius limits in `PaintCanvas.kt`.
- Preserve the initial curve line plus two bend drags, early commit, polygon finishing versus closure, selection transforms and confirmation, background-colour erasure, pencil width 1–100, brush tip/size, watercolor strength and each rectangle's half-shorter-side radius limit.
- Canvas help distinguishes outward expansion, inward trimming, moving bounds from inside, pinch/Fit view space and background filling newly added canvas space. Quoted commands match existing Latin captions.

## Validation

- 78 host translation/localization tests passed.
- Structural validation passed for all 171 offered language options.
- 38 Java resource render checks passed across English and Latin. These strings contain no format arguments; the check verifies that each selected resource renders without a formatting error.
- New entries preserve source attributes, typed-argument absence, numeric literals and newline structure. XML parses and all previous resources are unchanged.
- Base snapshot verified: 1,252 materialized files and modes match the parent tree; 222 unmaterialized base entries are retained through the unchanged Git base tree.
- Latin now contains 682 typed resources: P0 94/94, P1 249/249, P2 296/305 and P3 43/71. The remaining priority gap is 37 keys.

## Limits

This is bounded translation and structural evidence, not whole-catalogue linguistic acceptance, native-specialist certification, Android/AAPT compilation, device or emulator testing, layout/accessibility runtime verification, or CI acceptance. Modern technical Latin includes adaptations. No issue 1 retry was made.
