# Crop guidance misnames attached images and overstates guaranteed movement

**Status:** Open crop-guidance bug: a definite French attached-image referent defect plus a shared-source movement-qualification refinement; documentation-only issue-style tracking PR. No correction is applied. Keep open/draft pending separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Evidence boundary:** independent full-entry linguistic/static-source review, not runtime/device, rendering or whole-language acceptance. [Project board](https://github.com/c933103/AN-Paint/pull/39) · [Translation tracker](https://github.com/c933103/AN-Paint/pull/56). Issues remain disabled; settings/visibility are unchanged.

## Expected and actual

Expected: French assembly help and crop preview explain that cropping a parent image can move the images attached to it, while attachment relationships remain intact.

Actual: the long assembly help says “Les fixations existantes se déplacent lorsque leur image parente est recadrée.” Both crop-preview plural forms say “Recadrer des images placées repositionne leurs fixations.” These phrases describe repositioned attachment links/fixings, obscuring that other attached images move as the cropped parent's geometry changes.

Impact: users can misunderstand the consequential movement of other images when cropping. The referent error spans two French resource keys, not separate bugs per plural form. The proposed warning must also avoid implying that every crop moves attached images. No broken crop/layout/undo behavior is alleged.

## Affected-key checklist and static evidence

- [ ] `string/ui_add_up_to_20_images_with_android_s`: [FR L188](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L188), [EN L21](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L21); displayed by [AssemblyActivity.kt L341](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L341). Replace only the affected sentence with the independently reviewed candidate: “Les images rattachées peuvent se déplacer lorsque leur image parente est recadrée.” Re-review the entire long entry and preserve all other behavior.
- [ ] `plurals/ui_crop_preview_images`, both `one` and `other`: [FR L676–679](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L676-L679), [EN L489–492](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L489-L492); [ImageCropDialog.kt L90–93](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt#L90-L93) selects the quantity and passes dimensions/count. Candidate warning in both forms: “Le recadrage des images placées peut déplacer les images qui leur sont rattachées.” Preserve each form's preceding preview/apply text and `%1$d`, `%2$d`, `%3$d`.
- [ImageAssembly.kt L138–143](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L138-L143) changes crop geometry, retaining attachment metadata. [L162–180](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L162-L180) recomputes attached-image coordinates from the parent's right/bottom/left/top edges. [L190–195](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L190-L195) preserves validated history behavior.
- [Independent French full-entry/plural review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182571039) supports these coordinated corrections.

## Movement qualification after review

[Codex review](https://github.com/c933103/AN-Paint/pull/75#discussion_r4278246947) identified that the initial proposed French sentences were too categorical. Both independent language/source reviewers agree with the qualified candidates now shown above. A RIGHT-attached child's position can remain unchanged when only its parent's height changes; a BOTTOM-attached child's position can remain unchanged when only its parent's width changes. [ImageAssembly.kt L170–176](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L170-L176) establishes those dependencies.

The English help also says “Existing attachments move when their parent is cropped”; qualify the source alongside the referent correction. Proposed EN help sentence: “Attached images may move when their parent is cropped.” Proposed EN plural warning: “Cropping placed images may move their attached images.” Preserve all surrounding full-entry/plural text, dimensions and quantity slots. Audit faithful counterparts for the same categorical implication; this is not permission to rewrite unrelated translations or claim whole-language acceptance.

## Bounded fix and acceptance

- Update the two French referents with qualified movement wording, coordinate the English source qualification, and review affected localized counterparts. Do not change attachment metadata or crop/layout code just to match old wording.
- Verify both singular and multiple-image crop previews preserve placeholders, quantities and the correct attached-image referent; read the full long-help entry in its source context.
- Exercise a placed parent with attached descendants, crop it, and verify descendants move according to the established layout while relationships remain intact; Undo/Redo restore the corresponding geometry.
- Include unchanged-position controls: vertical-only parent crop with a RIGHT child, horizontal-only crop with a BOTTOM child, and a no-attached-image case. Do not claim every crop necessarily moves every image.
- Run current resource/plural structure tests and focused assembly/crop regressions; independently review final exact French values before replacing receipts. Preserve separate count-agreement and placement/alignment findings.

## Next action and dependencies

Apply the bounded French semantic corrections with source/locale movement qualification, then actual crop-preview/help resource checks and current-source code review/testing. Coordinate with active assembly work (including PR67) against its final integration baseline; evidence here remains pinned to develop. Update PR56 only after changed values/context are verified. No application/resource/test modification or runtime acceptance is made by this PR.
