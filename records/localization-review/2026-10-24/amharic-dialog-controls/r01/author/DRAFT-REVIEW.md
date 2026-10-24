# Amharic common dialog controls: original draft dossier

Production 66be61df27c5359bffc32d56db21f3949899f873; tree 870c5a584120d92710be516af0dc3b3847b183d9. Twenty-nine complete source copies are supplied, exact Git blobs checked against freshly retrieved production tree.

No independent acceptance or implementation. Prior69 ready/eleven held remain separate.

## string/ui_ok

English: OK

Proposed XML: `<string name="ui_ok">"እሺ"</string>`

Status: review

Confidence: {'lexical': 'high', 'contextual': 'high', 'overall': 'high for independent review; not release approval'}

Use the exact AOSP generic OK label, corroborated by AOSP Gallery2 and LibreOffice stock _OK. Current AN-Paint message helpers attach it to a positive message-acknowledgement button with no application-specific mutation callback. It acknowledges or closes the message; it does not promise success, saving, or acceptance of terms.

Positive acknowledgment button on informational/error/help messages, null callback dismisses dialog (ClassicPaintActivity.message, AssemblyActivity.message). Not proof an operation succeeded and not a separate Save/Apply action. Full Help text itself excluded.

['Original author draft for independent review only; not production-ready acceptance, native-reader sign-off, or evidence that an Android rendering/accessibility test passed.', 'Static current caller inspection supports the stated role but no runtime interaction or layout validation was performed.', 'Other ready drafts and held keys are excluded; no prior acceptance is inherited.', 'Gallery2 ok is an operation-control context; it corroborates the label, not the AN-Paint acknowledgement semantics.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1587, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L120

## string/ui_done

English: Done

Proposed XML: `<string name="ui_done">"ተከናውኗል"</string>`

Status: review

Confidence: {'lexical': 'high', 'contextual': 'medium', 'overall': 'medium; special independent semantic review required for error notices'}

Retain the exact generic Android Done convention, separately present as an exact label in Gallery2 after a selection interaction. In AN-Paint the common role is finishing the current interaction: some callers only close a screen, drawing settings already change live, GalleryCredits saves and validates before dismissal, and failure notices also use Done. The selected source convention must therefore be reviewed as a completion/exit button, never as an assertion that the failed operation succeeded or that every caller saved.

Generic finish/close-interaction label. Used to close about/legal/language views, exit gallery/legacy screens, dismiss vertical feedback and failure notices. Drawing-setting toggles have already applied live. IMPORTANT GalleryCredits overrides Done to save() then dismiss only on success, so not universally dismissal-only or universally-save. Error notice Done does not certify success.

['Original author draft for independent review only; not production-ready acceptance, native-reader sign-off, or evidence that an Android rendering/accessibility test passed.', 'Static current caller inspection supports the stated role but no runtime interaction or layout validation was performed.', 'Other ready drafts and held keys are excluded; no prior acceptance is inherited.', 'The Amharic form is morphologically completed-result wording. Its exact Android generic-button attestation is strong, but the author cannot independently certify native-reader interpretation on a failed-save notice. Reviewer may hold this key without blocking the other three.', 'No numbered Done headword was found in the locally searched glossary; absence is limited to that extraction.', 'Done is not always dismissal-only, always-save, or always-successful.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L239, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L892, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1572, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/LegacyImageCreditsActivity.kt#L127, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/LegalInfo.kt#L122, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalFeedbackView.kt#L73, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt#L166, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L63, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L114, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L135

## string/ui_cancel

English: Cancel

Proposed XML: `<string name="ui_cancel">"ይቅር"</string>`

Status: review

Confidence: {'lexical': 'high', 'contextual': 'high', 'overall': 'high for independent review; not release approval'}

Use the exact AOSP generic Cancel control and Gallery2 corroboration. It can dismiss a pending dialog, abort import/save workflow callbacks, exit trim, or restore a color preview, according to the caller. It does not mean global undo or deletion. Prefer this recognizable cancel label over glossary ሰርዝ because both retained AOSP applications separately use ሰርዝ for Delete.

Cancel current interaction, caller-specific semantics. Many negative buttons dismiss before pending changes commit. AdvancedColourDialog restores preview(original) on Cancel; trim_cancel clears trim and refits viewport; ImportSelection cancellation cleans up/calls cancellation path; SaveOptionsDialog invokes supplied cancellation callback; ImageResizeDialog onDismiss cancels if not accepted. Does not guarantee global undo, no side effects, rollback of prior changes or deletion of user source files.

['Original author draft for independent review only; not production-ready acceptance, native-reader sign-off, or evidence that an Android rendering/accessibility test passed.', 'Static current caller inspection supports the stated role but no runtime interaction or layout validation was performed.', 'Other ready drafts and held keys are excluded; no prior acceptance is inherited.', 'Do not describe Cancel as merely dismissal in all callers: AdvancedColourDialog explicitly runs preview(original).', 'Do not imply all changes are rolled back: previously committed settings or palette actions are outside a generic cancel guarantee.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt#L190, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageResizeDialog.kt#L38, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L96, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L116, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L824, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L909, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L992, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1009, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1018, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1054, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1162, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NumericSlider.kt#L71, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyPlacementDialog.kt#L70, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/LegalInfo.kt#L120, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L38, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt#L197, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt#L142, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L308, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt#L305, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt#L345, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt#L99

## string/ui_apply

English: Apply

Proposed XML: `<string name="ui_apply">"ተግብር"</string>`

Status: review

Confidence: {'lexical': 'high', 'contextual': 'high', 'overall': 'high for independent review; not release approval'}

Use AOSP’s exact generic Apply imperative, independently corroborated by glossary entry 149 for putting selected settings or changes into effect. Current exact-key callers validate entered numbers, placement settings, or dimensions before invoking their operation. Apply is an action request, not a completed-success report; invalid values may keep the dialog open.

Confirm/apply current validated input: NumericSlider parses integer/range then changes progress and calls setting callback; ClassicPaintActivity dimensions validates size/budget then creates/resizes canvas and fits view; AssemblyPositionDialog validates nonnegative integral coordinates and changes placement. Invalid values can keep dialog open. Not file Save or unconditional success. Existing Apply to all acceptance does not transfer automatically.

['Original author draft for independent review only; not production-ready acceptance, native-reader sign-off, or evidence that an Android rendering/accessibility test passed.', 'Static current caller inspection supports the stated role but no runtime interaction or layout validation was performed.', 'Other ready drafts and held keys are excluded; no prior acceptance is inherited.', 'Only exact key ui_apply is covered. ui_apply_to_all, ui_apply_crop, ui_apply_bounds, and ui_apply_to_these_images are separate strings and must not inherit this result.', 'A successful click is not guaranteed to complete if validation or an operation fails; translation does not add a success or persistence promise.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1018, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NumericSlider.kt#L71, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyPlacementDialog.kt#L71

## Shared scope and evidence limits

Seventeen direct caller files plus supporting dialog/formatting/document source are complete and current-tree-bound. EditorDialogBuilder in VerticalUi preserves caller-specific button callbacks; VerticalFeedbackCard also calls dismiss directly. Labels are generic affordances, not promises of universal success, save or rollback. Full current methods available; lookup list alone is not the entire review.

No English defect established. Preserve distinct generic interaction meanings and caller-specific side effects. Any real defect found later must be fixed in English first and tracked across languages, not silently compensated in Amharic.

Four plain labels have no placeholders or explicit units. Dialog titles/messages, validation strings, full Help and operation-specific buttons remain outside translation scope.

Full lexical reasoning, exact records, source snapshots and retrieval/reuse limitations are in lexical-evidence/. Nonfuzzy is a record flag, not proof of correctness. Component and cross-context evidence does not establish exact full-phrase native acceptance.

Original drafts only; independent linguistic/context checking required.

Bounded current consumer corpus discovered from historical source, not exhaustive fresh repository search.

No native-reader, rendered, speech, lifecycle, app-execution or release validation.

Prior69 ready/11holds and all inherited uncertainties remain excluded.

Production remains12 present/705 missing of717. No production changes, builds, CI, release or Work task.
