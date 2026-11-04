# Latin typography controls and help

## Scope and review

Twenty-four missing Latin resources cover font-family captions, strikethrough, background fill, text direction and vertical-character orientation, alignment, placement help and the font-licence heading. The multilingual preview sample is retained exactly rather than translated. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`. Independent review accepted all entries unchanged.

Reviewed against English resources and `FontCatalog`, `TextStyleDialog`, `TextPreview` and `VerticalText`. Font weight, width, serifs and equal character spacing remain distinct. The wording preserves top-to-bottom text with either column order, sideways joining including Mongolian, combining marks retained with their characters, and intact emoji sequences. Background fill applies to the text area. The licence heading does not change licence bodies.

## Verification

- 537 prior typed resources and attributes preserved; 24 strings added, yielding 561 typed Latin resources.
- XML, Android escaping, typed arguments, newline escapes and source numerals checked; the mixed-script sample remains exact.
- 78 host tests passed; structural validation passed for all 171 offered language options.
- 48 Java resource-render checks passed across English and Latin. These strings contain no dynamic arguments; the checks cover valid rendering of static templates.
- Base-tree verification checked content hashes and executable modes for all 1,252 materialized files; 215 other entries retained through the base tree.
- Priority coverage: P0 94/94, P1 249/249, P2 205/305 and P3 13/71. There are 158 priority keys still missing in Latin.

## Limits

This is a bounded translation and host-structure review, not Android compilation, AAPT, device, layout, accessibility-runtime, CI or specialist linguistic certification. No issue 1 action was retried.
