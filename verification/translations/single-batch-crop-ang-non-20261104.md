# Single and batch image cropping: Old English and Old Norse

Base: `a4cd515a7b276e4f26144ef5a17aa505833586a4` on `review/nv-bottom-2038-20261103`.

Added nine string resources and one plural resource per locale, with both `one` and `other` forms: 20 P2 resource keys and 22 text forms across `values-b+ang` and `values-b+non`. Canonical wording remains in the Android XML resources, without duplicated approval-text fixtures.

## Context and review

Source consumers checked: `ImageCropDialog.kt`, `CropOverlay.kt`, `AssemblyThumbnail.kt` and the crop entry point in `AssemblyActivity.kt`.

- Batch labels describe cropping multiple images, not merging them. The image checkboxes determine the affected set; the preview-image selector is distinct.
- Trim amounts are relative to the original edges. Handle wording describes the visible corner/edge markers, matching the eight-handle overlay. Source files remain unchanged.
- Pixel/percentage descriptions insert the existing standalone directional labels. A separator avoids requiring grammatical changes to the inserted left, top, right or bottom caption.
- The preview resource preserves dimensions, selected-image count and the warning that cropping placed images may move their attached images. Possibility is retained rather than implying movement always occurs.
- Both plural forms use count-neutral wording for the number of images to crop. This is grammatical without depending on runtime singular/plural categorization for these historical language tags. Source quantities and argument signatures are preserved; no plural-routing code change is included.

Independent semantic and linguistic review accepted both locales unchanged. Existing terminology for images, crops, previews, pixels and percentages is reused. Historical-language computing terms remain catalogue adaptations, not claims of ancient computing usage.

## Validation and coverage

- All 78 repository host tests passed against the accepted candidate.
- All 171 offered-language structural checks passed.
- XML parsing, unique typed resource identities, Android escaping, source and plural-item attributes, ordered typed placeholders and exact newline escapes passed.
- All 483 previous resources and their original bytes per locale remain unchanged. Each catalogue now has 493 typed resources: 492 strings and one plural resource with two text forms.
- All 24 distinct resource references in `ImageCropDialog.kt`, plus the thumbnail's reference, are now directly present in both catalogues. This is crop-workflow coverage, not whole-catalogue completion.
- Eight direction/unit combinations and both quantity forms at counts 0, 1 and 2 were materialized for inspection without changing runtime behavior.
- Per locale, P2 direct coverage increases from 136 to 146 of 305. P0 remains 94/94, P1 249/249 and P3 4/71.
- All 1,276 materialized base files match remote Git identities/modes. The 164 unmaterialized research/verification records are preserved through the base tree. Only the two catalogues and this evidence record are intended publication changes.

No Android build, device rendering, screen-reader run, runtime plural-routing certification, external CI result or historical-language specialist certification is claimed. No issue1 action was attempted.
