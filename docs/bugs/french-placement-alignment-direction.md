# French assembly instruction confuses placement direction with edge alignment

**Status:** Open semantic-language bug; documentation-only issue-style tracking PR. No correction is applied. Keep open/draft pending separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Evidence boundary:** independent full-entry linguistic/static-source review, not runtime/device, rendering or whole-language acceptance. [Project board](https://github.com/c933103/AN-Paint/pull/39) · [Translation tracker](https://github.com/c933103/AN-Paint/pull/56). Issues remain disabled; settings/visibility are unchanged.

## Expected and actual

Expected: French placement guidance distinguishes putting an image to the right with its top edge aligned, from putting it below with its left edge aligned.

Actual: `ui_drop_at_a_highlighted_edge_right_top_aligned` says “Déposez sur un bord surligné : aligné à droite/en haut ou en dessous/à gauche.” This conflates placement direction with alignment, suggesting right/top alignment rather than placement on the right with top edges aligned.

Impact: users can predict the wrong snapped location/aligned edges. This is a semantic direction/alignment problem; the underlying coordinate calculation is not alleged broken.

## Static evidence

- [French resource L302](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L302) and [English L163](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L163) bind the complete drag-status message.
- [AssemblyCanvas.kt L100–104](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyCanvas.kt#L100-L104) emits this status when a drag begins with available targets.
- [ImageAssembly.kt L170–176](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L170-L176) computes RIGHT as `x=parent.right, y=parent.top`, and BOTTOM as `x=parent.left, y=parent.bottom`. The two concepts are distinct in the actual layout.
- [Independent French review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182571039) agrees on the correction.

Proposed complete replacement, not applied:

> Déposez sur un bord surligné : à droite avec les bords supérieurs alignés, ou en dessous avec les bords gauches alignés.

## Same-cause dormant occurrence

The [French long legacy-help resource L464](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L464), `ui_the_arrow_on_the_left_directly_below_the`, repeats “…pour les aligner à droite/en haut ou en bas/à gauche”. No direct reference was found in the inspected 97 main Kotlin/Java files; current main help uses `ui_help23`. Track its direction correction as dormant resource consistency only, without claiming another active UI path. The active drag-status finding above is independently sufficient.

## Bounded fix and acceptance

- Apply unambiguous French wording preserving both placement alternatives and their aligned edges; audit repeated help text for the same defect and track confirmed occurrences together.
- Verify the actual drag-status resource used for a RIGHT target and a BOTTOM target with differently sized images, so top-versus-left alignment is observable.
- Retain ghost preview, commit/cancel, coordinate and collision behavior. This is a text repair, not a reason to change the established placement algorithm.
- Independently review the entire changed resource and any confirmed repeated help passage, preserving other instructions/placeholders/line breaks.
- Run structure/resource checks and focused source-bound assembly status/layout tests; record runtime/layout findings only if actually executed.

## Next action and dependencies

Apply the bounded French direction correction and any same-cause confirmed help occurrence, then exact-value context re-review and current-source review/test gates. Keep source comparison with active assembly PR67 explicit. Distinct from the crop attached-image referent bug and count-agreement bug. This PR contains documentation only.
