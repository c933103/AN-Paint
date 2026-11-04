# Latin image memory estimates

## Scope and review

Six missing Latin strings cover original-image and selected-copy memory estimates, safe editing budgets, a named-preview failure and retained general import guidance. Canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`. Independent review accepted all entries unchanged.

Reviewed against English resources, `ImageResizeDialog`, `ClassicPaintActivity` and `ImportMemoryRequirements`. The wording preserves original versus selected-size copy, RGBA storage at four bytes per pixel, estimates rather than guarantees, and the exclusion of additional decoder memory from the megapixel figure. The retained guidance preserves variable actual use, smaller-copy detail loss, selected opaque import background and the unchanged original file. Retained resources without direct current calls were not declared unused.

## Verification

- 585 prior typed resources and attributes preserved; six strings added, yielding 591 typed Latin resources.
- XML, Android escaping, ordered typed arguments, decimal precision, multiline and trailing newline escapes, and source numerals checked.
- 78 host tests passed; structural validation passed for all 171 offered language options.
- 12 Java resource-render checks passed across English and Latin, including indexed floating-point arguments.
- Base-tree verification checked content hashes and executable modes for all 1,252 materialized files; 217 other entries retained through the base tree.
- Priority coverage: P0 94/94, P1 249/249, P2 233/305 and P3 15/71. There are 128 priority keys still missing in Latin.

## Limits

This is a bounded translation and host-structure review, not Android compilation, AAPT, device, layout, accessibility-runtime, CI or specialist linguistic certification. No issue 1 action was retried.
