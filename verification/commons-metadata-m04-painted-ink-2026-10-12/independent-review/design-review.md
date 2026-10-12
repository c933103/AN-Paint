# Provisional painted-ink oracle design review

This starts a separate review; the d802 first-run and 4ff7 diagnostic-source/artifact reports remain frozen.

Parent authorized an evidence-supported test-oracle successor after the diagnostic finding. No production, translation, font or tolerance change is supported. Final implementation and hosted execution have not been reviewed.

## Accepted design direction, conditional on code and controls

- Replace only the short-landscape horizontal advance-width proxy with strict actual painted-ink containment. Preserve complete text/accessibility/UTF-16 line coverage, ellipsis, height, parent visibility and scroll reachability checks, and the vertical route.
- Preserve the old exact failed oracle/source/evidence via new narrowly pinned inverse projections. Advance values remain diagnostics. Do not relabel previous failed runs as passes.
- Allocate reference raster using the full API35 `Layout.computeDrawingBoundingBox()` unioned with every line extent, outward integer rounding and a raster safety border. Fail closed on unsupported features, nonfinite/oversized geometry or edge contact. The border is not a content-width allowance.
- Guard the helper's narrow plain-horizontal scope rather than changing the live view: no spans/custom drawing, background/foreground/compound drawable, shadow/decorative paint effects, shifted start-overhang or unexpected alignment/gravity/scroll. Derive actual text origin from compound padding and baseline geometry.
- Independently draw the entire same native Layout on a transparent expanded canvas and the actual TextView on an equivalent transparent native canvas. Compare exact unmasked ARGB values, with no new tolerance. Never obtain the expected image by cropping an already clipped actual view.
- Inspect every alpha>0 reference pixel, including glyph ink outside nominal line boxes. Nominal line-height slicing alone can omit overhanging marks.
- Native negative controls must prove intact fixtures pass and real overflow, completely displaced ink and clipped first/last glyph ink fail across RTL, combining, Han and Latin profiles at both scales. Mutating saved pixels alone is not sufficient. Clipping must leave the complete reference unchanged; integer translation shifts the independent full reference by the same delta so actual geometric overflow is exercised without losing reference glyphs.

## Primary-source check

The official [Android Layout API](https://developer.android.com/reference/android/text/Layout#computeDrawingBoundingBox()) identifies this API as available from API35 and distinguishes actual glyph drawing bounds from nominal first/last line metrics. That supports glyph-bound-based reference allocation for the explicitly guarded scope. The [AOSP implementation](https://android.googlesource.com/platform/frameworks/base/+/a9ec5dbf9bb17a96cf2eb2b182f9972a7ba7ef79/core/java/android/text/Layout.java) iterates lines and incorporates glyph metrics and baselines. This source consultation does not establish that the proposed helper compiles or that native negative controls pass.

The earlier finite-margin-only diagnostic remains useful observed evidence but is not by itself a universal reference-completeness proof. The API35 geometry contract plus explicit scope restrictions addresses that design objection, subject to final code and native execution.

## Final source follow-through

The frozen candidate and resolved cached-RectF correction are assessed in `README.md`; this design note alone is not native-runtime acceptance. The additional Android35 source was successfully inspected at https://android.googlesource.com/platform/prebuilts/fullsdk/sources/+/refs/heads/androidx-constraintlayout-release/android-35/android/text/Layout.java (blob c674968bba8a7b3ffc854167b46db36385e461ab).
