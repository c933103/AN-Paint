# Independent model review — Shan priority batch B

## Result and cumulative state

- Batch B's **21 missing candidates**: **19 exact accepts (5 P0 + 14 P1)** and **2 P1 corrections pending independent second-check**. No additional B holds.
- Exact per-target wording, backtranslation, rationale and confidence: `shan-review-batch-b-independent-20261030.tsv`.
- Together with batch A: **51 exact accepted missing rows (10 P0 + 41 P1)**, **5 holds (4 P0 + 1 P1)**, and **2 P1 corrections pending second-check**, covering all **58 A/B missing candidates**.
- Existing Undo is separately accepted unchanged. Existing Brush has a separately proposed correction; neither should be counted as a missing-key addition. Prior PR237 acceptances and six unchanged SHN decisions earn no duplicate credit.
- The 14 entries in `draft-term-holds.tsv` are separate unresolved work. They contain no accepted new target values in this review and must not be counted as drafted/accepted additions.

## Exact correction proposals

1. `ui_enter_a_trim_amount_for_every_edge`: **သႂ်ႇတၢင်းၼမ်ဢၼ်တေတတ်းဢွၵ်ႇတႃႇၶွပ်ႇၵူႈၽၢႆႇ။**
2. `ui_enter_all_four_trim_amounts`: **သႂ်ႇတၢင်းၼမ်ဢၼ်တေတတ်းဢွၵ်ႇတင်းသီႇဢၼ်။**

Both original B candidates used **ၸမ်းတတ်း**, with a claim of reuse from the accepted trim constraint. The actual canonical accepted `ui_trim_amounts_must_be_zero_or_greater` uses **တၢင်းၼမ်ဢၼ်တေတတ်းဢွၵ်ႇ**. I cannot validate the new short noun as amount; the replacement uses the securely accepted quantity-to-trim phrase while preserving each/all-four requirements. These exact corrections require a separate second-check. They are not accepted merely because this reviewer proposed them.

## Source binding and evidence

Reviewed frozen `../author/batch-b.tsv` and the related draft-hold log. The recorded source binding remains develop **96681f687671a1fdffe134a325843919c1543401**, tree **39bb7351fa5532194e2c0430432b2f0cc6358a86**, selected files unchanged in `baseline resource snapshot`. English sources and canonical Shan terminology were manually inspected. No independently resolvable local Git HEAD is claimed.

The primary references used to resolve pixel and Undo vocabulary remain [MediaWiki Shan software catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/shn.json) and [Help:Diff/shn](https://www.mediawiki.org/wiki/Help:Diff/shn), independently inspected during A review. Those isolated lexical attestations do not certify entire B sentences. Canvas, recovery copy and crop phrases are accepted on their complete compositional semantics and app context, not on a requirement to find an identical published UI sentence.

Read-only app evidence:

- `EditorDraftRecovery.kt:36–45`: successful separate preservation produces the retained-copy message; failure instead pauses autosave. The accepted wording does not collapse those states.
- `ClassicPaintActivity.kt:849–852,1016–1018`: canvas bounds, canvas size, image scaling and crop-to-selection are distinct actions. Drawing-area paraphrase refers to the bounded image surface, and the top-left warning preserves destructive right/bottom clipping plus Undo.
- `PaintDocument.kt:435`: crop rectangle must be inside the bitmap; this supports the canvas-containment condition.
- `ImageAssembly.kt:29,223`: positive crop extent and source-image containment are separate requirements; their translated conditions remain distinct.
- `ImageCropDialog.kt:88,125,141,146–149`: all edge margins are required; reset restores full image bounds; single-image title receives the image name; crop-application failure is generic. Crop wording is appropriate to this spatial image-cutting context, not the clipboard Cut command.

## Detailed safety/meaning findings

- Recovery-copy labels say export, not normal Save. The purpose phrase means a copy for recovery and does not promise every piece of history can be restored.
- The long recovery instruction retains separately kept copy, successful preservation, File menu path, ZIP saving, exact `canvas.png` extraction, loading the extracted image, and optional normal resizing. It does not imply the ZIP imports as a fully editable project.
- Top-left pixel placement is preserved. Reduced canvas dimensions discard pixels beyond right/bottom; they are not merely hidden. Undo restores them. No left/right or top/bottom reversal occurred.
- Canvas is transparently the drawing area, not fabric or the whole device display. Crop-to-selection explicitly says that selected content remains, preventing the destructive opposite reading.
- At least one pixel is expressed as one or more. Image-contained crop and canvas-contained crop are not merged.
- All supplied attributes are name-only. `%1$s`, literal `canvas.png`, `ZIP`, source-specific ellipses, right/bottom slash and the single escaped newline are retained. The recovery-path `>` is shown decoded in the TSV; retain the source's `&gt;` convention during XML serialization. This is a serialization instruction, not a claim that a bare `>` is universally illegal XML text.

## Limits and next step

Independent AI/model review only: no native-human certification, UI-fit proof or implementation is asserted.

Freeze the 19 B accepts against exact source/candidate bytes subject to final acceptance of this review. Independently second-check the two correction proposals before counting them or integrating their replacement text. Keep all original A holds and draft-term holds outside the accepted manifest. This artifact itself changes no official residual counts.
