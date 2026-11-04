# Latin cursor drawing and magnified views

Base: `c24034c97fb1e6ba381c5508e8cf2f3752c3266a` on `review/nv-bottom-2038-20261103`.

## Scope and review

Twenty missing Latin P2 entries cover cursor-mode controls, drawing start/stop, marker shape and size, cursor position, pan/tap instructions, pixel grids and magnified previews. Independent language/context review accepted all twenty unchanged. The x/y caption deliberately retains its language-neutral source text. All 413 previous typed resources remain unchanged; the additions give 433 typed resources.

`ClassicPaintActivity.kt` and `PaintCanvas.kt` distinguish enabling cursor mode from starting or stopping inking. The two pan instructions retain their distinct purposes: beginning drawing and positioning the cursor. Marker size means the visible sign rather than ink width. Existing Latin drawing, preview, magnification, settings, panning and pixel terminology is reused. Both 800%+ grid labels and the marker-size percent retain their literal-percent flags; x and y remain ordered indexed integers.

Six related source captions have no direct production Kotlin `R.string` occurrence in the inspected snapshot: the older disable-cursor caption, hide/show grid captions, magnified-preview caption with ellipsis, draw-with-cursor caption and cursor-settings caption. These are translated from their retained source without declaring them unused. Nothing is removed or rerouted. No fit-to-view command is included.

## Checks

- 78 existing host tests passed: translation catalogues, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through, and open-review recovery.
- All 171 offered options pass existing structural validation.
- 40 Java resource-render checks passed across English and Latin: 34 format templates, including indexed x/y arguments, and six literal-percent resources with `formatted="false"`.
- Source attributes, XML/Android escaping, ordered typed arguments, newline escapes, numeric boundaries and literal percent signs are preserved.
- Latin direct priority presence: P0 94/94, P1 249/249, P2 90/305 (previously 70/305), P3 0/71. Remaining priority keys: 286.
- 1,252 materialized source files were checked against expected Git objects and modes; the other 208 non-tree entries remain in the base tree. Publication uses an exact-parent non-force lease, full remote tree comparison and changed-file readback.

## Limits

This is bounded independent AI language/context and host structural review, not whole-catalogue linguistic acceptance or native-speaker certification. Technical Latin is a modern adaptation. No Android build, AAPT, installed layout, device, accessibility, runtime or CI acceptance is claimed. No runtime routing changes, deletions, release, merge or issue-tracker updates are included. Canonical XML owns the text; no permanent language-approval mirror or per-language wording test was added.
