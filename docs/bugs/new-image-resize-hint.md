# New image incorrectly promises pixel preservation and Undo

**Status:** Open bug; documentation-only issue-style tracking PR. This is not an implementation or fix claim. Keep the PR open/draft until the defect is resolved through separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Verification:** independent linguistic/static-source review only. No runtime, device, rendering, CI, native-speaker or whole-language acceptance is claimed. Repository Issues are disabled; this open PR is the durable bug record. [Project board](https://github.com/c933103/AN-Paint/pull/39).

## Expected and actual

Expected: File > New image describes creating a blank document and does not promise to preserve the previous canvas or recover it with Undo. Canvas size may retain its accurate top-left/cropping/Undo guidance.

Actual: New image uses the canvas-resize hint: “Keeps pixels at the top left. Smaller canvas dimensions discard pixels beyond the right/bottom edge; Undo restores them.” Applying New image instead creates a blank replacement and clears Undo and Redo history.

Impact: the user can misunderstand the destructive replacement as a reversible canvas resize. The existing unsaved-change confirmation remains separate; this report does not claim that confirmation is absent. This is a shared call-site defect, not separate French/Japanese translation bugs.

## Static reproduction and evidence

1. [File > New, ClassicPaintActivity.kt L828](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L828) calls `dimensionsDialog(false,true)`.
2. [Dialog selection and action, L1003–1016](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1003-L1016) choose the resize hint whenever `stretch == false`, including `fresh == true`, then call `document.newImage` for that fresh path.
3. [PaintDocument.kt L197–220](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L197-L220) implements `newImage` as a blank replacement with default `asEdit=false`; L208–210 clear undo/redo.
4. [Canvas resize L423–431](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L423-L431) instead preserves top-left pixels and invokes `replace(next,true)`, retaining undo history.
5. Resource `ui_keeps_pixels_at_the_top_left_smaller_canvas`: [English L253](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L253), [French L366](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L366), [Japanese L414](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L414). [French review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182425420) and [Japanese review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182427427) independently identify the same context defect.

## Bounded fix and acceptance

- Restrict existing resize guidance to non-fresh canvas resizing. On New image, omit the inapplicable hint or provide separately localized, accurate blank-document guidance. Do not change New into Resize merely to match the text.
- Exercise the actual File > New dialog branch using a nonblank edited canvas with undo/redo history. Assert that no retention/Undo promise is shown, applying creates the requested blank dimensions, and the existing new-document history/reset behavior is preserved.
- Exercise the actual Canvas size branch: guidance remains accurate, top-left content is retained, right/bottom cropping occurs as described, and Undo restores the previous content/dimensions.
- Keep stretched image resizing distinct and retain its scaling guidance. Cover cancellation without document/history mutation.
- Verify resource selection in English, French and Japanese, plus every affected locale/fallback through the shared call-site change. If new text is introduced, enumerate and review all required localized values; do not infer language acceptance from resource presence.

## Next action and dependencies

Implement the smallest branch-specific hint selection, then add actual dialog/document regressions and perform the repository's current-source review/test gates. Coordinate with the ongoing translation tracker so the held shared-context entries gain credit only after the fix and exact-value/context re-review. No dependency on the other newly identified bugs; no app code or tests are changed by this tracking PR.
