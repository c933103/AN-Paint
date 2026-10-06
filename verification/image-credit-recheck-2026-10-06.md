# Image-credit lifecycle recheck, 6 October 2026

This is a fresh, bounded source review of the integration snapshot
`a6b5956b0ae8f8082fafc2ff21d63e337f3a85af`, followed by the changes recorded here.
It does not restore the withdrawn September completion claims or close the
full localization register. Canonical translations were not changed.

## Two defects found and repaired

1. **Copy/cut of a pending insertion borrowed unrelated canvas credits.**
   `PaintDocument.copySelection()` copied `imageCredits`, the union of the
   committed canvas ledger and pending selection ledger. With credited artwork
   A on the canvas and a newly inserted blue artwork B still floating, copying B,
   creating a new image, and pasting attributed the blue image to both A and B.
   An uncredited pending image likewise inherited A. The selection now carries
   its own source set; selecting already flattened canvas pixels captures the
   conservative canvas ledger, while pasted images retain their supplied set.
   Copy and cut transfer the selection's source set only.
2. **Assembly replacement kept credits for the replaced canvas.**
   The assembly return path deliberately replaces all pixels as an undoable
   edit, but the generic `replace(..., asEdit=true)` also retained the old
   canvas's credits. Imported replacement content now explicitly clears the
   current ledger after the undo snapshot is captured. Undo restores the old
   pixels and credits; redo restores the composite and its empty ledger. Canvas
   resize, crop and transform continue retaining their conservative provenance.
   This does not infer attribution from externally supplied assembly files.

New drafts include `selection_sources_known`. Legacy drafts did not distinguish
an uncredited pending insertion from a lifted canvas selection with an empty
source list. For those legacy drafts the reader conservatively retains the old
canvas sources, matching the prior clipboard behavior. It cannot reconstruct
which old source contributed pixels. New drafts preserve an explicitly empty
selection source list without borrowing canvas sources.

## Current-source checks against the credit register

Source references below are
[`PaintDocument`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt),
[`ClassicPaintActivity`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt),
[`MediaGalleryActivity`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt),
[`SaveOptionsDialog`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt),
[`ImageCredit`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCredit.kt),
[`AutosaveStore`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/AutosaveStore.kt)
and [`HistoryArchive`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/HistoryArchive.kt).
These are source findings and reviewed assertions, **not a report that the
Kotlin tests have executed for this change**.

| Register row | Fresh source finding and assertion coverage |
| --- | --- |
| CR-001 | Credits live on a `PaintDocument` instance. New/open replacement clears the ledger; assembly replacement needed the explicit repair above. |
| CR-002 | `paste` checkpoints committed state and attaches incoming credits to `Selection`. New multi-source test checks committed/floating JSON separately. |
| CR-003 | `finishSelection` composites pixels then transfers selection credits. Existing lifecycle tests inspect the committed image; new copy/cut tests inspect pixel and source together. |
| CR-004 | `deleteSelection` clears pending content without transferring its sources. New multi-source test checks that A remains while cancelled B is absent. |
| CR-005 | `moveHistory` restores credits from the selected raster entry. Existing lifecycle test and enhanced assembly test assert restored credit and pixel state. |
| CR-006 | Redo snapshots include visible floating pixels through `finishSelection`. Existing lifecycle and new independent-replacement tests assert matching sources and pixels. |
| CR-007 | Defect repaired: pending image copy/cut previously copied unrelated committed sources. New tests cover copied B, cut B, uncredited insertion, ordinary canvas selection, lifted canvas selection and restored floating selection. |
| CR-008 | `imageCredits` deduplicates by source and committed ledger keys are source URLs. Existing repeated-paste test requires one credit. |
| CR-009 | `clear` commits pending content, snapshots it, clears pixels and ledger. Existing test asserts clear removes the credit and undo restores it. |
| CR-010 | `newImage` uses non-edit replacement; source and existing tests show current credits/history cleared while the internal clipboard remains usable. |
| CR-011 | Activity restores pixels, optional floating pixels, history, then current credit metadata. New archive round-trip test covers A committed plus B floating and subsequent isolated clipboard transfer. Legacy/known-empty distinction has a separate test. |
| CR-012 | `HistoryArchive` indexes exact `ImageCredit` values, preserving source/text variants, and restores ordered undo/redo stacks. Existing draft lifecycle test writes an undone document, reloads it and redoes the credited image. |
| CR-013 | `editImageCredit` amends committed, floating, clipboard and both history lists, then calls `changed`, which schedules autosave. Existing test asserts edited text survives undo/redo. This is metadata amendment, not a separate undoable raster edit. |
| CR-014 | Gallery saves edited result and the `creditsEdited` flag in instance state; `onCreate` republishes the edit result. Existing gallery recreation test edits through Done before recreating. Unconfirmed editor typing across recreation is not covered by that test. |
| CR-015 | Unedited gallery does not set `RESULT_OK`; existing recreation test checks `RESULT_CANCELED` for the untouched path. |
| CR-016 | Save options creates credit details with `View.GONE`; existing activity-level test and new direct-dialog language test assert this. |
| CR-017 | Export options uses the same collapsed panel; both tests exercise Export separately. |
| CR-018 | Save credit text uses native `TextView.setTextIsSelectable(true)`; both tests assert the property. Actual drag-selection on a device remains unverified here. |
| CR-019 | Export uses that same selectable view; the new test also traverses the vertical Mongolian dialog layout. |
| CR-020 | Save Copy all sends the complete supplied text to Android's clipboard. New test supplies two credits in different original scripts. |
| CR-021 | Export Copy all uses the same action; tests assert the clipboard string exactly. |
| CR-022 | Copy callback only invokes `GalleryCredits.copy`. Existing test asserts no picker activity; new direct-dialog test asserts confirm callback count stays zero and dialog stays open. |
| CR-023 | Credit text is stored literally in JSON and history; display joins strings without retranslating them. New Japanese and Mongolian UI test asserts unchanged Han/Cyrillic text and URLs in both dialogs and clipboard. |
| CR-024 | Existing and new test methods were inspected individually; execution limits are recorded below. Their existence is not runtime acceptance. |

Flattened canvas selections intentionally carry a conservative source set: the
model does not track per-pixel provenance and cannot safely remove an attribution
merely because pixels were cropped or painted over. Credit text copying is
separate from copying image pixels. No credit file or metadata is automatically
embedded in an exported image by these changes.

## Verification and remaining work

- `python3 -m unittest discover -s tools -p 'test_*.py'`: **110 passed** in
  26.712 seconds. These host checks cover localization/codec tooling and do not
  execute the Android credit lifecycle.
- `git diff --check`: passed.
- Kotlin/Robolectric tests were added or strengthened in
  [`ImageCreditLifecycleTest`](../Paintroid/src/test/java/org/catrobat/paintroid/local/ImageCreditLifecycleTest.kt),
  [`AssemblyActivityTest`](../Paintroid/src/test/java/org/catrobat/paintroid/local/AssemblyActivityTest.kt)
  and [`ExportFormatDialogTest`](../Paintroid/src/test/java/org/catrobat/paintroid/local/ExportFormatDialogTest.kt).
  Existing gallery tests are in
  [`GalleryImportTest`](../Paintroid/src/test/java/org/catrobat/paintroid/local/GalleryImportTest.kt).
  The local workspace has no Android SDK, so compilation and execution remain
  pending the integration CI run. Historical CI results do not cover this patch.
- Device interaction, gallery network behavior, visual glyph quality, selectable
  text gestures and accessibility traversal were not runtime-verified here.
- The register stays pending where full runtime or user acceptance is required.
  This review does not claim all latest conversation requests were retrieved.
