# Latin colour controls and sampling

## Scope and review

Twenty-four missing Latin resources cover advanced colour selectors, honeycomb accessibility descriptions, colour presets, numeric component ranges and foreground sampling. Ten language-neutral numeric range labels remain exactly as in English. Existing recent-colour entries remain untouched. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`. Independent review accepted all entries unchanged.

Reviewed against English resources and `AdvancedColourDialog`, `ColourSurface`, `HoneycombPalette`, `ClassicPaintActivity` and `PaintDocument`. The wording distinguishes hue and saturation from HSL lightness and HSV value, preserves the right-hand controls, honeycomb arrangement and greyscale row, and retains foreground sampling. Standard RGB/HSV/HSL labels, degree and percent signs, ranges and hexadecimal width/case are unchanged.

## Verification

- 561 prior typed resources and attributes preserved; 24 strings added, yielding 585 typed Latin resources.
- XML, Android escaping, ordered typed arguments, newline escapes and source numerals checked.
- 78 host tests passed; structural validation passed for all 171 offered language options.
- 48 Java resource-render checks passed across English and Latin: 40 formatted-template checks and eight literal checks for resources marked formatted=false.
- Base-tree verification checked content hashes and executable modes for all 1,252 materialized files; 216 other entries retained through the base tree.
- Priority coverage: P0 94/94, P1 249/249, P2 228/305 and P3 14/71. There are 134 priority keys still missing in Latin.

## Limits

This is a bounded translation and host-structure review, not Android compilation, AAPT, device, layout, accessibility-runtime, CI or specialist linguistic certification. No issue 1 action was retried.
