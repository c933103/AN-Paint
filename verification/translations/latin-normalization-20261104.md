# Latin equal image dimensions and normalization

Base: `ecfe83bee388e28f924e3855402c4d58ec374668` on `review/nv-bottom-2038-20261103`.

## Scope and review

Twenty missing Latin P2 entries cover equal width/height, normalization instructions and status, percentage input, smallest/largest presets, apply/reset, the Android-range diagnostic and related generic templates. Independent language/context review accepted all twenty unchanged. All 433 previous typed resources remain unchanged; the additions give 453 typed resources.

`NormalizeImagesDialog.kt` uses the current placed sizes for its largest-dimension denominator, not original file sizes or the new target. The translations retain each image's own aspect ratio, unchanged original files and crop settings, the opposite-axis range, and reflow of placed images to make room. `ImageAssembly.kt` preserves source/crop metadata while normalizing and enforces Android's dimension range. The error translation does not narrow the range check to only oversized images.

Seven retained generic templates/captions belong to the same normalization family. The generic information and percent-of-pixels resources have explicit test consumers. These resources are translated without claiming that every retained generic key is currently called by production UI. No resource is declared unused, removed or rerouted. Parenthesized injected dimension labels avoid imposing grammatical case changes; placeholder order remains exact.

## Checks

- 78 existing host tests passed: translation catalogues, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through, and open-review recovery.
- All 171 offered options pass existing structural validation.
- 40 Java format-template checks passed across English and Latin, including all seven indexed string arguments of the generic information template and the typed integer templates.
- Source attributes, XML/Android escaping, ordered typed arguments, newline escapes, numeric literals and range order are preserved.
- Latin direct priority presence: P0 94/94, P1 249/249, P2 110/305 (previously 90/305), P3 0/71. Remaining priority keys: 266.
- 1,252 materialized source files were checked against expected Git objects and modes; the other 209 non-tree entries remain in the base tree. Publication uses an exact-parent non-force lease, full remote tree comparison and changed-file readback.

## Limits

This is bounded independent AI language/context and host structural review, not whole-catalogue linguistic acceptance or native-speaker certification. Technical Latin is a modern adaptation. No Android build, AAPT, installed layout, device, accessibility, runtime or CI acceptance is claimed. No runtime routing changes, deletions, release, merge or issue-tracker updates are included. Canonical XML owns the text; no permanent language-approval mirror or per-language wording test was added.
