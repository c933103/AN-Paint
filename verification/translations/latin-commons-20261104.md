# Latin Commons diagnostics

## Scope and review

Seventeen missing Latin resources cover Commons credit-copy failures, metadata diagnostics, original-file identity checks and blank-map conversion. The technical SVG size-limit label remains unchanged. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`. Independent review accepted all entries unchanged.

Reviewed against English resources, `MediaGalleryActivity` and `CommonsAttribution`. Credit-only copying is distinct from image downloading. Unclear file identity, selected-original attribution mismatch, invalid file or attribution pages, response and field limits, retention failure and download redirection remain distinct. HTTP arguments, format names and the 32 MiB bound are preserved.

## Verification

- 615 prior typed resources and attributes preserved; 17 strings added, yielding 632 typed Latin resources.
- XML, Android escaping, ordered typed arguments, newline escapes and source numerals checked.
- 78 host tests passed; structural validation passed for all 171 offered language options.
- 34 Java resource-render checks passed across English and Latin.
- Base-tree verification checked content hashes and executable modes for all 1,252 materialized files; 219 other entries retained through the base tree.
- Priority coverage: P0 94/94, P1 249/249, P2 274/305 and P3 15/71. There are 87 priority keys still missing in Latin.

## Limits

This is a bounded translation and host-structure review, not Android compilation, AAPT, device, layout, accessibility-runtime, CI or specialist linguistic certification. No issue 1 action was retried.
