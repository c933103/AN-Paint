# Latin assembly placement and workspace

Base: `edd66d5d776821518791c4f1bd0ff2200c33b303` on `review/nv-bottom-2038-20261103`.

## Scope and review

Twenty-one missing Latin strings cover assembly placement, workspace gestures, snap alignment, placed/unplaced states, exact X/Y coordinates and associated view/gesture help. Seventeen entries are P2 and four are directly connected P3 help strings. Independent language/context review accepted all twenty-one unchanged. All 468 previous typed resources remain unchanged; the additions give 489 typed resources.

`AssemblyActivity.kt`, `AssemblyCanvas.kt` and `AssemblyPlacementDialog.kt` bind the translated labels and instructions. `ImageAssembly.kt` confirms right/top alignment and below/left alignment for snapping, while exact placement permits overlap and preserves other images' positions. `AssemblyRenderer.kt` confirms that later-imported images draw on top. The draft retains top-left whole-pixel coordinates, zero origin, the exact maximum integer, canvas expansion, and unchanged crops/sizes. Unplace removes placement rather than deleting an image. Show-all and pinch/pan descriptions concern the view rather than resizing image/output data. The drag ClipData label describes an image for composition in AN Paint.

## Checks

- 78 existing host tests passed: translation catalogues, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through, and open-review recovery.
- All 171 offered options pass existing structural validation.
- 42 Java format-template checks passed across English and Latin, including all four ordered arguments of the thumbnail accessibility caption.
- Source attributes, XML/Android escaping, ordered typed arguments, newline escapes and numeric coordinate bounds are preserved.
- Latin direct priority presence: P0 94/94, P1 249/249, P2 142/305 (previously 125/305), P3 4/71 (previously 0/71). Remaining priority keys: 230.
- 1,252 materialized source files were checked against expected Git objects and modes; the other 211 non-tree entries remain in the base tree. Publication uses an exact-parent non-force lease, full remote tree comparison and changed-file readback.

## Limits

This is bounded independent AI language/context and host structural review, not whole-catalogue linguistic acceptance or native-speaker certification. Technical Latin is a modern adaptation. No Android build, AAPT, installed layout, device, accessibility, runtime or CI acceptance is claimed. No runtime routing changes, deletions, release, merge or issue-tracker updates are included. Canonical XML owns the text; no permanent language-approval mirror or per-language wording test was added.
