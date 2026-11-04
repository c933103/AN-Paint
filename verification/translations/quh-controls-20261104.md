# South Bolivian Quechua editor controls — 4 November 2026

Base: `3515719038e0c8a9aa09b333b4e733998f938e5e`.
Scope: 31 missing canonical quh resources: 30 P1 controls/settings and one P0 canvas-boundary warning. This is an independent model/context review, not native-speaker certification.

## Review outcome

28 candidates retained and three directly revised. Font-family wording now names the family of letters; line spacing explicitly means distance between text lines; the smaller-canvas warning explicitly identifies either the right or bottom edge. No semantic deferrals in this batch.

The warning retains the top-left anchor, deletion beyond the reduced bounds, and the existing Undo label. View fitting and image placement remain distinct: `fitSelectionToCanvas` changes floating geometry, retaining source pixels. Aspect-lock labels are identical and resize help quotes the same label. The technical loan `proporcion` remains subject to fluent-user preference. RGB inversion describes complementing each channel, distinct from swapping foreground/background colours; implementation preserves alpha. Navigate and its accessibility reference match. Text direction remains broad enough for horizontal and both vertical column modes. Historical labels without a recovered active caller are not represented as tested live routes.

Reviewed callers: `ClassicPaintActivity.kt`, `PaintCanvas.kt`, `PaintDocument.kt`, `DimensionControls.kt`, and `TextStyleDialog.kt` at the base above. Lexical reference consulted by reviewer: https://www.illaa.org/pirwa/diccionarios/DicQuechuaBolivia.pdf . Composed UI sentences are not claimed to be dictionary-attested.

## Static verification

- 31 unique previously absent keys; all 302 previous resource values and attributes unchanged.
- Exact reviewed values, source attributes, indexed placeholders and newline counts.
- XML parsing and existing Android-escaping, format, placeholder and literal-token helpers.
- Exact Navigate, Undo and aspect-lock references; two literal percentage labels retain `formatted=false`.
- Catalogue 302 to 333; P0 86 to 87 of 92; P1 216 to 246 of 249. Eight priority gaps remain. Coverage is presence, not linguistic certification.

## Outstanding checks

No Android build, hosted CI, native-speaker acceptance, device/layout test, merge, deployment or release is claimed. The long RGB-inversion label especially requires rendered-device layout checking. This review is evidence, not a permanent wording freeze. The canonical XML owns current text.
