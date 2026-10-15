# Empty credit text is misreported as no gallery-image insertion

**Status:** Open shared source-context diagnostic bug; documentation-only tracking PR. No fix is applied. **Baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`. Independently reviewed static paths and complete English/French/Japanese values; no runtime/provider/native incident, outage or security vulnerability is claimed. Faithful translations share the source mismatch. [Board](https://github.com/c933103/AN-Paint/pull/39) · [French review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182795516) · [Japanese review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182776352).

## Expected and actual

Expected: Copy all reports that no image credit text is available when the current credit text is empty, without making an unsupported assertion about image insertion history.

Actual: `ui_no_gallery_images_have_been_inserted` says “No gallery images have been inserted.” The gallery Copy all handler selects that message from the combined credit text being blank, not from whether an image was inserted. A user can insert an image, return to the editor, reopen the gallery with the document's credits, blank its only credit in the credit editor, save/finish that edit, and then use Copy all.

Impact: the user receives an inaccurate explanation of an ordinary empty-text state. This report does not allege that insertion failed or that editing a credit removes the image.

## Static path and evidence

- [MediaGalleryActivity.kt L384–392](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L384-L392) returns the downloaded file and finishes the gallery. [ClassicPaintActivity.kt L1218–1233](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1218-L1233) then processes it and supplies its credit to import. A test must wait for successful insertion in the editor, then reopen the gallery: [L886–899](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L886-L899) creates a fresh credit session from `document.imageCredits`, and [MediaGalleryActivity.kt L66–68](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L66-L68) takes that session's credits. The edit cannot happen continuously in the already-finished download activity.

- [GalleryCredits.kt L100–115,L140–142](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L100-L142) accepts and saves the edited field, including empty text. [CreditSessionJson.kt L32–36](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/CreditSessionJson.kt#L32-L36) bounds string memory without requiring nonempty credit text.
- [MediaGalleryActivity.kt L234–239](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L234-L239) adopts the edited credits. [ImageCredit.kt L20](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCredit.kt#L20) filters blank text when constructing the combined output.
- [Copy all L106–109](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L106-L109) equates that blank output with no prior insertion. The same message also serves [empty credit-editor entries, GalleryCredits.kt L85–87](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L85-L87); the replacement must fit both contexts or use distinct resources.
- Current values: [EN L276](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L276), [FR L379](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L379), [JA L427](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L427).

## Bounded fix and acceptance

- Use accurate text-based wording or split the two contexts. Reviewed neutral candidates: EN “No image credit text is available.”; FR “Aucun texte de crédit d’image n’est disponible.” Review equivalent values in every affected locale, including Japanese.
- Exercise the actual source-supported UI sequence: successful image insertion after returning to the editor → reopen gallery with that document's credit session → edit its only credit to empty → Save/Done → Copy all. Assert the message describes unavailable credit text and does not deny insertion.
- Include an initially empty ledger and nonempty-credit controls. Preserve blank-text edit semantics, document association, metadata bounds and the clipboard's existing no-text behavior.
- Re-review every changed complete resource/call site and run focused credit-editor/copy regressions and current-source gates. A source-derived sequence is not an executed test result.

## Next action

Implement the smallest context-accurate message selection, enumerate/localize all affected instances, and verify the real edit/copy sequence before closing. This independent cause is distinct from missing-browser, redirect-classification and native-component diagnostics. Open draft remains documentation only; no count/acceptance or app/resource/test change.
