# Latin image tray, sorting and capacity

Base: `6fa0bac9f86119bc52eea9fa8df360249e560527` on `review/nv-bottom-2038-20261103`.

## Scope and review

Fifteen missing Latin P2 strings cover adding images, thumbnail instructions, filename/modification-time sorting, unavailable timestamps, the 20-image limit and remaining capacity. Independent language/context review accepted all fifteen unchanged. All 453 previous typed resources remain unchanged; the additions give 468 typed resources.

`AssemblyActivity.kt` binds the controls to the horizontally scrolling tray, selection prompts and add-image capacity checks. `ImageAssembly.kt` sorts by filename or modification timestamp; `AssemblyCanvas.kt` displays the add-then-drag-thumbnail instruction. Sorting is described as ordering previews rather than moving placed canvas images. Both total capacity and remaining capacity retain their exact source values/argument. Removal is explicitly from the composition, not deletion of an original file. Modification-time ordering remains distinct from filename ordering, and an unavailable timestamp does not receive an invented date.

## Checks

- 78 existing host tests passed: translation catalogues, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through, and open-review recovery.
- All 171 offered options pass existing structural validation.
- 30 Java format-template checks passed across English and Latin, including the remaining-capacity argument.
- Source attributes, XML/Android escaping, typed arguments, newline escapes, literal 20 limits and A–Z/Z–A ranges are preserved.
- Latin direct priority presence: P0 94/94, P1 249/249, P2 125/305 (previously 110/305), P3 0/71. Remaining priority keys: 251.
- 1,252 materialized source files were checked against expected Git objects and modes; the other 210 non-tree entries remain in the base tree. Publication uses an exact-parent non-force lease, full remote tree comparison and changed-file readback.

## Limits

This is bounded independent AI language/context and host structural review, not whole-catalogue linguistic acceptance or native-speaker certification. Technical Latin is a modern adaptation. No Android build, AAPT, installed layout, device, accessibility, runtime or CI acceptance is claimed. No runtime routing changes, deletions, release, merge or issue-tracker updates are included. Canonical XML owns the text; no permanent language-approval mirror or per-language wording test was added.
