# Independent model review — Shan batch C and notation-only templates

## Result

- **Batch C: 29 exact accepted missing lexical rows (4 P0 + 25 P1); 1 P0 hold.**
- Held `save20_encoding_budget` uses the same unresolved **ၶဝ်ႈၶူတ်ႉ** encoding term as four held A rows. Its other propositions are good; there is no new objection to the buffer or memory-limit phrase.
- **Seven additional P1 format-only values accepted unchanged**, recorded separately in `shan-review-format-invariants-independent-20261030.tsv`. They are valid missing-value additions but not seven newly authored lexical translations.
- Exact C decisions: `shan-review-batch-c-independent-20261030.tsv`.

Before the two B trim corrections are second-checked, cumulative A/B/C lexical decisions are **80 exact accepts (14 P0 + 66 P1)**, **6 holds (5 P0 + 1 P1)** and **2 correction proposals (P1)** across **88 missing lexical targets**. Add the **7 notation-only P1 accepts** as a separate category. Existing unchanged Undo and corrected Brush are separate existing-value reviews, not missing-key additions. No prior PR237 accepted row or six existing SHN accepted decisions is recounted.

## Source and primary lexical evidence

Frozen C source was `../author/batch-c.tsv`, supplemented by `review-c.md`, `format-invariant-review.tsv` and `brush-reassessment.tsv`. Canonical binding remains the recorded unchanged-file assurance for develop **96681f687671a1fdffe134a325843919c1543401**, tree **39bb7351fa5532194e2c0430432b2f0cc6358a86**, materialized checkout `baseline resource snapshot`. No independent local Git HEAD claim.

Independently retrieved primary references on 2026-10-30:

- [Unicode CLDR49 Shan summary](https://unicode.org/cldr/charts/49/summary/shn.html): percent rows 4703–4704 give **ဝၢၵ်ႈ**; rectangle rows 8680–8685 give **သီႇၸဵင်ႇသိုဝ်ႈ**, distinct from square; artist-palette rows 7084–7085 and artist keyword rows support **ပၢၼ်ႉသီ**. Pencil and paintbrush rows independently inspected during A review remain valid noun evidence for C. Each full compound/sentence was then assessed, not certified wholesale by CLDR.
- [MediaWiki primary Shan catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/shn.json): `collapsible-collapse` uses **တူပ်ႉဝႆႉ**; expand-all messages use **ၶႂၢၵ်ႈ** constructions. Distinct hide/show labels support the visibility, rather than deletion, meaning. Pixel and Undo lexical evidence was already independently checked in A.

The web renderer's exact Shan `find` sometimes produced unrelated excerpts. For percent and palette, I used inspectable English-aligned chart ranges; a mismatching excerpt was not treated as evidence. No requirement for a perfect matching published sentence was imposed on transparent canvas/toolbox/control/cache compositions.

## Source-context findings

- `RasterHistory.kt:22,51`: cache creation failure occurs when a filesystem directory cannot be created. Free-device-storage instruction is therefore not a request to free working RAM.
- `RasterHistory.kt:60–62,79–97`: damaged cache and unexpected trailing data are distinct diagnoses; accepted strings do not accuse the source image of corruption.
- `SaveOptionsDialog.kt`: ordinary Save reuses name, destination, format and settings. Compression paraphrase says **file** gets smaller, not dimensions, and promises neither losslessness nor guaranteed output size.
- `ClassicPaintActivity.kt:604–619`: click sets foreground and long-click sets background. Both gesture instructions preserve that mapping and the literal hex prefix.
- `ToolCategoryButton.kt:27`: placeholders are category then selected tool; both translated descriptions preserve selected state and their separate expand/collapse action.
- `ClassicPaintActivity.kt:1541–1564`: magnified preview and magnification values change view/magnifier state, not the saved image dimensions. Canvas-zoom labels similarly preserve view-only meaning.

### Pencil rationale repair

The author's C note says the PENCIL tool is one-pixel. That is outdated: current `ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` and `ui_pencil_crisp_adjustable_strokes` both say **Pencil keeps crisp edges at any selected width.** Noun **ၵမ်ၸိုၼ်း** remains accepted, but the old behavioral claim is not carried into the review evidence. This is a rationale correction, not an allegation of a defect in the translated noun.

## Invariant review

Manually compared the C strings and all seven notation-only targets with canonical English resources. Preserved indexed argument types/order, `%3$,d` grouping, `%4$.2f` precision, zero/one-decimal float formats, degree signs, `%`, hash, multiplication sign, middle dots, parentheses, px/MP, and literal escaped newlines. `formatted=false` is retained for C magnification and notation-only 100%. Embedded-string translations in notation templates are outside the invariant's acceptance; this does not claim complete locale coverage.

## Resolution reported during review

The recorded author second-check independently accepts the exact existing Brush replacement **ယူႈယွမ်ႉသီ**, after checking CLDR and BRUSH/PENCIL/SPRAY context. The existing Brush correction can therefore be considered dual-reviewed when that author acceptance is bound to the exact proposed bytes. The earlier A artifact intentionally preserves its initial proposed-correction status; this note records the later resolution. This is positive evidence for a suitable replacement, not proof that old **မၢၵ်ႇတႅမ်ႈ** was erroneous. No production change occurred here.

## Limits

Independent AI/model review, not native-human certification or UI-fit proof. No implementation or test result is asserted. The 14 draft-object holds remain outside this acceptance, and official residual numbers do not change merely because these artifacts exist.
