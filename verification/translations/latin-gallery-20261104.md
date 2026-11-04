# Latin online gallery controls

## Scope and review

Nineteen missing Latin strings cover online-gallery navigation, search, image use and load diagnostics, including the retained Catrobat-specific rejection. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`. Independent review accepted all entries unchanged.

Reviewed against English resources and `MediaGalleryActivity`. The Use image instruction matches its injected action caption exactly. English-or-Japanese search, selected-source boundaries, artwork-page prerequisite, unsupported URL and redirect limits remain distinct. File-size, inspection-memory and missing-component failures retain their meanings, including the explicit statement that no image was imported. Connection checking and retrying remain present. A retained resource without a direct current call was not declared unused.

## Verification

- 632 prior typed resources and attributes preserved; 19 strings added, yielding 651 typed Latin resources.
- XML, Android escaping, ordered typed arguments, newline escapes and source numerals checked.
- 78 host tests passed; structural validation passed for all 171 offered language options.
- 38 Java resource-render checks passed across English and Latin: 28 formatted-template checks and ten literal checks for resources marked formatted=false.
- Base-tree verification checked content hashes and executable modes for all 1,252 materialized files; 220 other entries retained through the base tree.
- Priority coverage: P0 94/94, P1 249/249, P2 292/305 and P3 16/71. There are 68 priority keys still missing in Latin.

## Limits

This is a bounded translation and host-structure review, not Android compilation, AAPT, device, layout, accessibility-runtime, CI or specialist linguistic certification. No issue 1 action was retried.
