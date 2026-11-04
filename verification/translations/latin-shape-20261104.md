# Latin shape tools and stroke controls

Base: `8f15caf4ac52d96155f6b54006d018c32b8b2fea` on `review/nv-bottom-2038-20261103`.

## Scope and review

Twelve missing Latin P2 strings cover finishing polygons and curves, closing a polygon, fill-plus-outline, round/square/calligraphic tips, corner and spray radii, watercolor strength and two distinct smoothing controls. Independent language/context review accepted all twelve unchanged. Existing Latin shape names and all 401 previous typed resources remain unchanged; the additions give 413 typed resources.

`ClassicPaintActivity.kt` binds these labels to production controls. `PaintCanvas.kt` distinguishes committing a pending shape from closing a polygon path. `PaintDocument.kt` confirms that fill-plus-line means background fill plus foreground outline. Round and square captions work both for brush tips and the cursor marker. Stroke-path smoothing remains distinct from pixel-edge anti-aliasing. Pixel units, literal percent and the technical anti-aliasing label are retained.

## Checks

- 78 existing host tests passed: translation catalogues, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through, and open-review recovery.
- All 171 offered options pass existing structural validation.
- 24 Java resource-render checks passed across English and Latin: 22 format-safe templates and two literal-percent resources with `formatted="false"`. This block has no indexed arguments.
- Source attributes, XML/Android escaping, typed argument signatures, newline escapes and numeric literals are preserved.
- Latin direct priority presence: P0 94/94, P1 249/249, P2 70/305 (previously 58/305), P3 0/71. Remaining priority keys: 306.
- 1,252 materialized source files were checked against expected Git objects and modes; the other 207 non-tree entries remain in the base tree. Publication uses an exact-parent non-force lease, full remote tree comparison and changed-file readback.

## Limits

This is bounded independent AI language/context and host structural review, not whole-catalogue linguistic acceptance or native-speaker certification. Technical Latin is a modern adaptation. No Android build, AAPT, installed layout, device, accessibility, runtime or CI acceptance is claimed. No runtime routing changes, deletions, release, merge or issue-tracker updates are included. Canonical XML owns the text; no permanent language-approval mirror or per-language wording test was added.
