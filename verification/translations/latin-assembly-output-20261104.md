# Latin assembly constraints and output

Base: `91399375409068fd36d40aa576cb7dcdd92f6480` on `review/nv-bottom-2038-20261103`.

## Scope and review

Twenty missing Latin P2 entries cover attachment/cycle/coordinate diagnostics, output sizing, memory estimates and limits, processing progress, unavailable output and preview/crop decode failures. Independent language/context review accepted all twenty unchanged. All 489 previous typed resources remain unchanged; the additions give 509 typed resources.

`ImageAssembly.kt` and `AssemblyCanvas.kt` distinguish missing and unplaced attachment targets, cycle errors, snap-overlap errors and coordinate limits. Overlap guidance offers another edge or removing placement, not deleting source files. `AssemblyActivity.kt` and `AssemblyRenderer.kt` separate per-image processing progress from output completion, preserve original-size editing/render memory estimates, and label approximate memory needs. Failed-preview guidance still permits trying to save without promising success. `ClassicPaintActivity.kt` uses the exact localized assembly-menu caption for reopening unavailable output. `ImageResizeDialog.kt` also consumes the budget-fit caption, which remains a budget statement rather than guaranteed allocation.

## Checks

- 78 existing host tests passed: translation catalogues, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through, and open-review recovery.
- All 171 offered options pass existing structural validation.
- 40 Java format-template checks passed across English and Latin.
- Source attributes, XML/Android escaping, ordered typed arguments and newline escapes are preserved, including the memory template's trailing newline. The reopen instruction quotes the exact existing localized caption.
- Latin direct priority presence: P0 94/94, P1 249/249, P2 162/305 (previously 142/305), P3 4/71. Remaining priority keys: 210.
- 1,252 materialized source files were checked against expected Git objects and modes; the other 212 non-tree entries remain in the base tree. Publication uses an exact-parent non-force lease, full remote tree comparison and changed-file readback.

## Limits

This is bounded independent AI language/context and host structural review, not whole-catalogue linguistic acceptance or native-speaker certification. Technical Latin is a modern adaptation. No Android build, AAPT, installed layout, device, accessibility, runtime or CI acceptance is claimed. No runtime routing changes, deletions, release, merge or issue-tracker updates are included. Canonical XML owns the text; no permanent language-approval mirror or per-language wording test was added.
