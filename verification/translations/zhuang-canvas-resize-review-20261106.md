# Zhuang canvas resizing warning and label review, 6 November 2026

## Scope and language outcome

Base: `5322d1ec4fe3955e8cde62aae4407a01d5a1156c`, tree `71ac39b6cff80f121f7a8c50ad2e843a44951d7d`, on `review/nv-bottom-2038-20261103`. The preceding lossless-guidance publication was reconciled with no pending or uncertain write. Develop remained `412aab0c604060fb66fbd2edc6bb05572d10b56d`. This does not change develop or disjoint Navajo work.

Adds missing P0 `ui_keeps_pixels_at_the_top_left_smaller_canvas`, preserving all 320 existing typed resources for a total of 321. Only canonical Zhuang XML and this report change. The warning is a functional description of image content rather than an unverified technical compound for pixels: the picture stays at the upper-left corner; shrinking drawing-area dimensions discards the image portions beyond the right or bottom edge; Undo can restore those portions.

Independent review identified that the initial generic image phrase could mean whole images rather than portions. The final wording explicitly uses `bouhfaenh` for parts/portions in both the discard clause and restoration object. This resolves that scope ambiguity. The unchanged top-left origin, non-scaling operation, clipped right/bottom portions and recoverability through Undo are preserved. The warning does not say the entire image or its saved source file is deleted, nor promise persistence of undo after closing or reopening.

The complete revised meaning received moderate-to-high confidence, with high confidence in the actual consumer/behavior mapping. This remains an authored functional paraphrase, not a standardized Zhuang pixel term or native-user certification. Full-paragraph idiomatic polish and on-device presentation are unverified, not silently certified or imposed as native-human approval gates.

Four existing complete values were independently reviewed and retained:

- `ui_canvas_size`: drawing-area dimensions, with the existing ellipsis indicating a dialog.
- `ui_canvas_size_30460e`: the corresponding complete dialog title, without an ellipsis.
- `ui_canvas_bounds`: drawing-area edges/boundaries, appropriate for interactive bounds adjustment rather than crop-only behavior.
- `ui_edit_canvas33`: drawing area, appropriate for the Canvas command group.

These are descriptive software labels, not independently standardized canvas terminology. This bounded cohort contributes to [the all-translated-string review plan](p0-p1-release-plan-20261106.md), without claiming the complete locale has been reviewed. The quoted Undo name matches the existing Android display spelling after its XML outer quotes are removed.

## Evidence

- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently checked, supports dimensions, area, drawing, corner, edge, direction, change, discard and beyond constructions. The right/bottom and left senses are directly present in B15–16. It is an OCR lexical source, not evidence that a whole software sentence is idiomatic.
- [Bilingual mathematics-teaching prose, 22 April 2020](https://www.guangximinzubao.cn/szbzw/html/2020-04/22/content_35282.htm), directly re-read at line 27, explicitly distinguishes total from portions using `bouhfaenh`. This supports the part/whole meaning, rather than a whole-image plural reading.
- The independent reviewer also retrieved [bilingual physical-material prose](https://gxmzb.gxrb.com.cn/sy/mzwx/379519.html), where the same part/portion word describes some soil being compacted. Integration's repeat retrieval timed out and the older hostname was inaccessible. This supporting physical-use attestation is reviewer-verified, not a claimed successful second retrieval. The independently retrieved mathematical source remains available.
- [Guangxi Minzu Bao, 29 November 2023, page 3](https://www.guangximinzubao.cn/szbzw/page/21/2023-11/29/03/2023112903_pdf.pdf), bilingual ecological-restoration passage, Zhuang lines 107–109 versus Chinese 23–24, supports `hoizfuk` for restoration of a nonhuman state. Applying it to clipped image portions is an authored technical extension, not a claim of attested image-editor prose.

## Actual consumers

`ClassicPaintActivity` binds the Canvas size command to `dimensionsDialog(false,false)`. The complete new hint appears only for an existing-image, non-stretch operation. The dialog chooses the canvas-size title in that branch. New-image creation omits both resize hints, and image stretching has a distinct hint/title.

Confirmation validates dimensions and memory, applies pending work, and calls `PaintDocument.resize` with `stretch=false`. It creates a new background-filled bitmap, copies the existing bitmap at `(0,0)` without scaling, clips overflow and retains background where dimensions expand. The stretch branch instead draws into a scaled rectangle. `replace(next,true)` checkpoints the previous bitmap before replacement; Undo restores through the existing disk history path. This is not a guarantee against unrelated memory/storage or corrupted-history failures.

The separate Canvas bounds command opens the interactive bounds preview. That operation can expand, crop or translate bounds and is not the consumer of this top-left-only hint. The Canvas group label is resolved through `EditGroup.CANVAS` and the group button builder, covering bounds, dimensions, image resizing, invert and clear commands. No bitmap, history, menu, cancellation or layout code changes.

## Verification and limits

- All 171 offered-option structural catalogue checks and the importance manifest pass. Existing nodes, attributes, placeholders, numerals, literal tokens and escapes are preserved.
- Four localization host modules: **61 tests passed in 5.528 seconds**.
- **10 English/Zhuang Java XML-template cases** pass for the new warning and four retained labels. The quoted Undo reference was separately checked against the current command resource. This is not Android resource compilation.
- Temporary token-aware source checks verify **five direct resource bindings**, the nonfresh/nonstretch hint route, distinct titles, unscaled origin copy and checkpoint-before-replacement behavior. Static checks are not Android bitmap execution.
- Inspected but not run: `SizingAndTrimTest.canvasAndStretchHintsRemainDistinctAndCanvasCropIsUndoable` checks the two real dialogs, canceled stretch, retained top-left pixels, discarded right/bottom content and exact restored ARGB samples after Undo. Its new-image tests separately check omission of preservation/Undo promises. These existing tests are not counted as newly passing.
- `git diff --check` passes. All **1,593** base file bytes and executable modes match the complete remote tree. Publication uses only the two-file overlay, exact expected parent and non-force lease, followed by full remote-tree and changed-file readback. No permanent per-edit wording test or approval mirror is introduced.

Zhuang presence is P0 **79/94**, P1 **158/249**, P2 **81/305**, P3 **3/71**. Global missing counts are **152 / 1,333 / 30,048 / 7,478**, with 46 complete-presence options. Presence is not linguistic acceptance, completed full-string review or permission to fill excluded fallback-only catalogues.

Android SDK/Kotlin compiler are unavailable. Android compilation, Robolectric, real resize/Undo/storage paths, device layout and TalkBack were not executed. Exact-head Actions status is checked after publication and reported separately. No merge, release or CI-pass claim is made; conditional release gates remain open.
