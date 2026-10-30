# Independent Batch A candidate review — 30 October 2026

Reviewed **all 271 proposed values** against the actual English resource at `420cb76fb1fc02a53a5b6296505be193eaa3bb2f`, not merely the candidate author's backtranslations. Candidate evidence: `d3109827e3ac0679f10159f1b9534ec74b0a04f4`.

| Locale | Accepted | Corrected proposals | Rejected | Uncertain |
|---|---:|---:|---:|---:|
| Chamorro (95) | 63 | 5 | 1 | 26 |
| Shan (176) | 152 | 4 | 4 | 16 |

**215 accepted as written; nine stronger replacement proposals; five rejected; 42 uncertain.** These are independent model judgments, not native-human certification or production readiness. Corrected proposals still need independent review. [Full per-key dispositions, exact source/candidate/replacement text, reasons and structural checks](ch-shn-tdd-independent.json).

## Actionable corrections

- Chamorro `ui_height`, `ui_height_in`, `ui_heights`: **Tinekcha' means fruit, not height.** Replace with `Attura (%1$s)`, `Attura gi %1$s`, `Attura siha`.
- Chamorro `ui_original_size34`: `Urihinåt na mineddong`.
- Chamorro `ui_choose_at_least_one_image`: `Pili putlumenus unu na imåhen.`
- Shan `language20_settings`: `ၵၢၼ်တင်ႈ`; remove the anomalous suffix in the Android file-picker recovery instruction as well.
- Shan `ui_choose_at_least_one_image`: `လိူၵ်ႈႁၢင်ႈၼိုင်ႈႁၢင်ႈ ဢမ်ႇၼၼ် လိူဝ်ၼၼ်ႉ။` explicitly says one image or more instead of using `ယၢမ်ႈသုတ်း`.
- Shan `ui_trim_amounts_must_be_zero_or_greater`: `တၢင်းၼမ်ဢၼ်တေတတ်းဢွၵ်ႇ တေလႆႈပဵၼ်သုၼ် ဢမ်ႇၼၼ် ယႂ်ႇလိူဝ်သုၼ်။` explicitly names the amount cut off and retains zero-inclusive constraint.

Height/fruit and original/minimum vocabulary were cross-checked against [Chung's 2024 finder list](https://people.ucsc.edu/~schung/finderlist.12.2024.pdf); height also against [Kumisión's word list](https://kumisionchamoru.guam.gov/wp-content/uploads/2024/07/ListanPalabra.pdf). The settings noun appears in [SIIT's Shan computing instructions](https://shaniit.org/blogs/naek-tsam-tii-naa-tsau-iphone-sae-tae-haet-hue-thai-screenshot). These narrow checks do not substitute dictionary matching for whole-message translation.

## Meaning holds, not a blanket source gate

- Reject four Shan draft status/retry candidates: `ပိူင်ယၢင်ႇ` identifies an example/model, not reliably the user's editable draft. No replacement invented beyond competence.
- Reject Chamorro invalid-filename message as a **complete translation**: slashes/control characters remain untranslated English.
- Hold Shan separate-default-image APNG warning and image-resolution preservation warnings: basic image and image-data size do not securely convey the specific technical meanings.
- Hold Chamorro Save/Save-as constructions where digital-save idiom is not sufficiently secure. Short clear/remove and other independently understood labels are not blocked on that unrelated question.
- Shan export-created versus Save/Save-as instruction, saved-but-sharing-failed warning, and sharing-copy/unchanged-Save-destination message retain their complete distinctions. The memory-budget message retains OR allocation failure, resizing a copy, and unchanged original file—not a guarantee about unsaved work.
- Tai Nüa has **zero new candidates and zero semantic acceptances**. All seven existing entries are accounted for structurally; the Save… alias loses its ellipsis. Appending an ellipsis would not certify the underlying language.

## Verification and remaining scope

All 271 source fields match the canonical English resource; all 271 XML values match candidate JSON after text decoding; all format placeholders match. No full tests, Android compilation, device/font check, production edits, merge or Work task.

The original null targets remain unresolved: **246 CH, 165 SHN, 341 TDD**. Reviewed does not mean complete. Accepted entries alone must not overwrite a whole catalogue or delete unlisted existing entries.
