# Independent Amharic Edit-operation review

## Result

Seven RETAIN recommendations, no supported revisions, and one HOLD: Crop to selection. No production changes. Retain means recommend the original draft unchanged as a reviewed candidate, not certify native usage or assert an exact phrase attestation.

Reviewed source: `66be61df27c5359bffc32d56db21f3949899f873`, tree `870c5a584120d92710be516af0dc3b3847b183d9`.
Input manifest seal: `d48a3077f25680253db7606296e56c4021fff184688cd48ec7388dc026c1f59e`.

## Verified evidence

- All32 input manifest entries match; all12 complete production files hash to their recorded Git blob IDs and to the fresh full recursive-tree response. The fresh develop ref and commit response match the pinned revision.
- All8 English keys/source hashes/proposal hashes match, all8 exact Amharic keys are absent, and all8 proposed XML elements parse. No placeholders are introduced.
- All126 extracted PO records exist verbatim in their supplied snapshots, with matching fuzzy flags. The selected LibreOffice evidence is nonfuzzy; misleading GIMP exact-looking Crop/Delete/Invert records remain excluded.
- Coverage recomputes as719 string keys minus3 nontranslatable strings plus1 plural resource =717 translatable units. The Amharic catalogue contains12, leaving705 missing. The new8 are disjoint from the previous29 candidate inventory.
- Additional direct-form evidence: Android Settings `double_twist_for_camera_mode_title` pairs “Flip camera for selfie” with “ለራስ ምስል ካሜራን ገልብጥ”. This supports the imperative form, not semantic identity with reflection or inversion. See supplemental-evidence.json for both exact XML lines, source hashes and pinned URLs.

## Per-key decisions

### string/ui_flip_horizontal — RETAIN

English: Flip horizontal

Proposed body: "በአግድም ገልብጥ"

Confidence: source semantics high; translation/UI medium.

The horizontal modifier and flip family are explicitly paired in a nonfuzzy LibreOffice reflection command. The supplied imperative is a sound grammatical composition, not a translation of rotation or orientation. Newly located Android Settings evidence directly attests the imperative form ገልብጥ in another flip construction, reducing the form-only evidence gap. It does not directly attest this complete image-editing phrase.

Source meaning: The signed X scale reflects the full bitmap left/right; Y is unchanged. applyPending first commits pending edits and floating content. A reflection is not a 180-degree rotation.

Limit: Joined በ prefix and the assembled directional imperative are editorial composition. No direct full-phrase or native-speaker attestation was established; short-label layout remains untested.

Primary evidence:
- [.uno:FlipHorizontal / Label](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po): Flip Horizontally → በ አግድም መገልበጫ.
- [double_twist_for_camera_mode_title](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml#4479): Flip camera for selfie → ለራስ ምስል ካሜራን ገልብጥ. Imperative form only; camera switching is not raster reflection.

Consumer source: [ClassicPaintActivity.kt#L854-L854](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L854-L854), [PaintDocument.kt#L453-L459](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L453-L459).

### string/ui_flip_vertical — RETAIN

English: Flip vertical

Proposed body: "በቁመት ገልብጥ"

Confidence: source semantics high; translation/UI medium.

The vertical modifier and reflection noun are paired in a nonfuzzy LibreOffice command. Using the same imperative as the horizontal command preserves the operation pair and contrasts with the rotation verb. Android Settings independently supports the imperative form, though in a different operation.

Source meaning: The signed Y scale reflects the full bitmap top/bottom; X is unchanged. This is not a turn, orientation setting, or selected-content-only transform.

Limit: በቁመት is a composed directional modifier here, not a claim that LibreOffice provides this exact imperative. UI naturalness and fit remain medium-confidence judgments.

Primary evidence:
- [.uno:FlipVertical / Label](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po): Flip Vertically → በ ቁመት መገልበጫ.
- [double_twist_for_camera_mode_title](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml#4479): Flip camera for selfie → ለራስ ምስል ካሜራን ገልብጥ. Imperative form only.

Consumer source: [ClassicPaintActivity.kt#L855-L855](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L855-L855), [PaintDocument.kt#L453-L459](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L453-L459).

### string/ui_rotate_90_clockwise — RETAIN

English: Rotate 90° clockwise

Proposed body: "90° ወደ ቀኝ አሽከርክር"

Confidence: source semantics high; translation/UI medium-high.

The Android Gallery2 rotate-right imperative is directly attested. Adding the exact 90° angle is independently supported by the LibreOffice 90-degree-right label and preserves the intended quarter-turn. In an explicit rotation command, right denotes the clockwise turn rather than translating the image to the right. Prefer the attested አሽከርክር over a shorter, less directly supported alternative solely for brevity.

Source meaning: setRotate(90f) applies to the entire bitmap after pending edits are committed, then the view is fitted. The positive screen-graphics rotation convention is clockwise, corroborated by the Skia reference; no on-device measurement was performed.

Limit: The full phrase combines sources; it is not an exact quotation. Keep ASCII 90 and the degree sign. LibreOffice mnemonic ~ is not part of the proposal. No width/glyph testing.

Primary evidence:
- [rotate_right](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#88): Rotate right → ወደ ቀኝ አሽከርክር.
- [.uno:RotateRight / Label](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po): Rotate 90° ~Right → ማዞሪያ 90° ወደ ~ቀኝ.
- [setRotate](https://api.skia.org/classSkMatrix.html): setRotate. Technical rotation convention, not Amharic lexical evidence.

Consumer source: [ClassicPaintActivity.kt#L856-L856](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L856-L856), [PaintDocument.kt#L453-L459](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L453-L459).

### string/ui_rotate_180 — RETAIN

English: Rotate 180°

Proposed body: "180° አሽከርክር"

Confidence: source semantics high; translation/UI medium-high.

The directly attested Android imperative matches the adjacent quarter-turn command, and LibreOffice independently supports the 180° amount. Omitting a direction follows English and avoids adding a distinction that has no effect for a half-turn.

Source meaning: setRotate(180f) transforms the entire bitmap after applyPending. A half-turn is distinct from either single-axis reflection.

Limit: The angle-plus-imperative remains an original composition. No direction or extra object is needed merely to mirror another label’s length.

Primary evidence:
- [rotate_right](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#88): Rotate right → ወደ ቀኝ አሽከርክር. Evidence for the rotate imperative, not the complete 180° string.
- [.uno:Rotate180 / Label](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po): Rotate 1~80° → ማዞሪያ 1~80°.

Consumer source: [ClassicPaintActivity.kt#L857-L857](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L857-L857), [PaintDocument.kt#L453-L459](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L453-L459).

### string/ui_invert_colours — RETAIN

English: Invert colours

Proposed body: "ቀለሞችን ገልብጥ"

Confidence: source semantics high; translation/UI medium.

The explicit colour object gives ገልብጥ its colour-inversion sense. LibreOffice’s nonfuzzy GraphicFilterInvert label and help sentence establish this lexical family specifically for colour values, and Android Settings independently uses the inversion noun. Replacing this with swap/change terminology would introduce foreground/background exchange or arbitrary colour modification not present in the source.

Source meaning: Every bitmap pixel has its low 24 RGB bits complemented while its high 8 alpha bits are retained, after pending edits and the selection are committed. This is neither spatial reflection nor colour-swatch exchange.

Limit: The exact plural-object imperative is composed. The lexical sources support the operation category, not AN Paint’s byte-level RGB/alpha implementation. Same verb as flip is acceptable with this explicit object; it is not evidence that the operations themselves are identical.

Primary evidence:
- [.uno:GraphicFilterInvert / Label](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po): Invert → መገልበጫ.
- [24010000.xhp / par_id3145345](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/02.po): Inverts the color values of a color image → የ ቀለም ዋጋዎች መገልበጫ.
- [accessibility_display_inversion_switch_title](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml#2341): Use color inversion → የቀለም ግልበጣን ተጠቀም.

Consumer source: [ClassicPaintActivity.kt#L858-L858](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L858-L858), [PaintDocument.kt#L467-L476](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L467-L476).

### string/ui_clear_image — RETAIN

English: Clear image

Proposed body: "ምስሉን አጽዳ"

Confidence: source semantics high; translation/UI medium.

Android Gallery2 attests አጽዳ for clearing effects, while nonfuzzy LibreOffice Clear Contents supports content-clearing semantics for the same family. The image object distinguishes scope, and the chosen verb remains distinct from the deletion command. There is insufficient evidence for changing to a deletion verb; no specific mistranslation is established.

Source meaning: The current image is filled with the current background colour without changing canvas dimensions or deleting a saved image file. Pending/floating edits are committed first; image credits are then cleared. It does not promise transparency, new-document creation, or clipboard clearing.

Limit: Neither source attests the full clear-image phrase. A generic clean/clear verb is context-dependent; this review supports its command reading but does not certify that native users could never interpret it as image cleanup. No unsupported stronger wording is substituted.

Primary evidence:
- [clear_effects](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#348): Clear effects → ማሳመሪያዎች አጽዳ.
- [.uno:ClearContents / Label](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po): Clear Contents → ይዞታዎችን ማጽጃ.

Consumer source: [ClassicPaintActivity.kt#L859-L859](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L859-L859), [PaintDocument.kt#L478-L478](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L478-L478).

### string/ui_crop_to_selection — HOLD

English: Crop to selection

Proposed body: "በምርጫው መጠን ከርክም"

Confidence: source semantics high; translation/UI low-medium for phrase; high for hold.

The crop imperative is attested, but the added selection-size phrase is not. መጠን foregrounds size/extent and does not settle the precise relation between keeping selected content and replacing the canvas. It risks suggesting a dimension-based operation rather than a selection-bound crop. That is a translation precision concern, not a demonstrated English defect. The alternative according-to-selected construction in the draft is also unverified and is not accepted merely because it avoids size.

Source meaning: cropSelection obtains the transformed selected-content bitmap, including transformed bounds and mask, then finishes the selection and replaces the canvas as an edit. Transparent margins flatten over the background in replace. The operation requires a selection and keeps the selected result; it is not deletion of selected pixels or resizing an unchanged full image.

Limit: No independently supported full replacement is established. Keep both author proposals out of an implementation set. Resolve selected-content versus dimensions and naturalness in a focused language review; do not delete selection scope by shortening to the bare Crop verb.

Primary evidence:
- [crop_action](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#94): Crop → ከርክም.
- [.uno:Crop / Label and TooltipLabel](https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po): Crop / Crop Image → መከርከሚያ / ምስል መከርከሚያ.

Consumer source: [ClassicPaintActivity.kt#L852-L852](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L852-L852), [PaintDocument.kt#L349-L364](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L349-L364), [PaintDocument.kt#L461-L465](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L461-L465), [PaintDocument.kt#L197-L218](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L197-L218).

### string/ui_delete_selection — RETAIN

English: Delete selection

Proposed body: "የተመረጠውን ሰርዝ"

Confidence: source semantics high; translation/UI medium.

የተመረጠውን nominalizes what is selected and makes it the object of the directly attested ሰርዝ imperative. This is a better fit for deleting selected content than an instruction to clear the abstract selection state. Android’s selected-item confirmation supports the grammatical construction but is not equated with pixel deletion.

Source meaning: For nonfloating content, the selected rectangle or mask is filled with background after a checkpoint; for already-floating content, that content is discarded without committing it. The selection object is cleared in either case. It is not mere deselection, file deletion, or a promise of a fresh separate undo checkpoint for the floating branch.

Limit: The exact nominalized object plus imperative is new composition. Its selected-content reading is supported by grammar and context, not by native-speaker testing or a direct exact-match catalogue entry.

Primary evidence:
- [delete](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#52): Delete → ሰርዝ.
- [delete_selection / one](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#53): Delete selected item? → የተመረጠው ንጥል ይሰረዝ?. Selected media-item vocabulary and syntax only; not an image-region operation.
- [deselect_all](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#65): Deselect all → ሁሉንም አትምረጥ. Contrast only, not a proposed translation.

Consumer source: [ClassicPaintActivity.kt#L850-L850](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L850-L850), [PaintDocument.kt#L373-L377](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L373-L377).

## Shared source and scope limits

- All eight full phrases are compositions/adaptations, not independently attested complete AN Paint labels. The seven retain judgments are reviewer recommendations, not assertions of direct phrase attestation.
- No native-speaker, runtime, glyph, layout, screen-reader, lifecycle, application build/test, CI, production edit, Work task, deployment or release occurred.
- Only the twelve supplied production source files were inspected for consumer semantics. The independently retrieved full tree binds their identities but is not an exhaustive repository consumer search.
- Exact candidate XML parses and contains no formatting placeholders; Android resource compilation and rendering were not run. Surrounding XML text quotes are resource syntax, not a recommendation for visible quote marks.
- Nonfuzzy LibreOffice records and nonempty Android entries are lexical evidence, not infallible or native-certified translations. GIMP fuzzy, empty or obsolete exact-looking records remain excluded.
- New Android Settings camera-flip evidence supports imperative morphology only. It is not proof that camera switching, bitmap reflection and colour inversion are the same operation.
- No English source defect is established in this bounded review. If a source defect later is established, correct English first, flag every affected language, and review them individually rather than silently compensating in Amharic.
- Previous29 candidate recommendations, the12 production entries, and unrelated Palette/Horizontal/Help holds remain separate and unchanged. Coverage remains12 present/705 missing of717 translatable units.
- Fresh GitHub branch, commit and full recursive-tree reads plus local Git blob hashes establish the pinned source identity. A current remote branch observation is not a promise that it will remain unchanged.
- The complete input dossier is retained under input/ with its original manifest and seal; review conclusions live only in review.json and REVIEW.md.

## Artifact contents

review.json provides machine-readable exact recommendations and hashes. verification.json records source/resource/evidence checks. supplemental-evidence.json preserves the added lexical evidence and technical corroboration. The branch, commit and complete tree receipts are included. input/ preserves the entire draft dossier, twelve complete source files and eight complete lexical snapshots. prior-candidate-separation.json records inventory-only disjointness without merging earlier reviews. MANIFEST.json hashes every other payload file; its separate SHA-256 is the bundle seal.
