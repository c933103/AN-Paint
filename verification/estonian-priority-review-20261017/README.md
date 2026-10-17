# Estonian P0/P1 complete-value review — 17 October 2026

Source base: `b6a99b41c4390ca6a412e3a1938eb913c59509fb` (develop, including merged PR125). Review scope is the current 92 P0 + 249 P1 entries, not whole-language acceptance. `estonian-p0-p1-review.json` contains every complete English/Estonian pair, attributes, source links, consumer references, an individual linguistic/context rationale, confidence/limits, preserved prior receipts, hashes and disposition.

## Outcome

- 296 unchanged values accepted in the inspected static consumer context.
- 32 values accepted for wording only; no current consumer or dormant flow limits runtime judgment.
- 7 explicit uncertain judgments remain open: GIF dithering terminology, sampled-decoding terminology, generic busy/draft source mismatch, foreground/background compact abbreviations, unconsumed third palette placeholder and the terse hexadecimal label.
- 6 P0/P1 values corrected. One P2 width accessibility template is a separately authorized dependency of the same shared-unit composition. There is no broader P2/P3 review; 375 other canonical entries remain outside the full review.

The seven full values restore the picker heading/maintenance/fallback paragraph, match the actual Save as command in export guidance, make pixel count wording neutral for 1 and larger counts, and compose all four accessible dimension labels naturally: Laius/Kõrgus pikslites/protsentides. The standalone unit buttons and visible unit labels remain unchanged.

`independent-review.json` is the unchanged independent challenge assessment, including source-backed full-value judgments and boundaries. `candidates.json` is proposal history: its initial isolated `piksel` proposal is superseded by the final atomic four-resource composition. `corrections.json` is the final decision.

## Selection and existing evidence

Swedish's 103 present / 238 fallback finding was selection context only. It is outside the current scoped catalogue set; no Swedish strings were reviewed or filled. Estonian is scoped, with all 341 priority entries present. Current branch pages, recent PRs and the current PR56 entry evidence were inspected before selecting Estonian; see `claim-check.json`. Nine earlier Estonian receipts are retained verbatim as historical input, one overlapping this priority list. No duplicate credit is claimed. PR56 remains read-only/upload-held and was not changed.

All Indonesian, Malay, Japanese and Hong Kong processing-label holds and all other explicit pauses remain unchanged. No tracker counters were uploaded.

## Validation and limits

Compact host tests compare full values/attributes/format tokens/newlines, reject corruptions and old full values, validate all four compositions and preserved holds. Added Robolectric tests exercise actual DimensionControls unit switching and pixel summaries, the actual AppLanguage picker title/cancel path, and compiled export guidance plus Save/Save as labels. The export-after-save branch is statically inspected, not executed by the added test. No claim of TalkBack or on-device Estonian layout/font-scale acceptance is made.

See `test-summary.json` and raw logs for exact local outcomes. The local full Gradle attempt failed before build at the distribution download because the network is unavailable. AAPT2 compiled/linked all resources and exact-script mirrors. Supplementary Kotlin compilation uses freshly generated resource symbols and existing dependency classes, not a full build or runtime result. Hosted exact-head checks are tracked separately through terminal completion while the PR remains draft.

The separate evidence ref is additive to the complete application tree. Every parent file/content/mode is retained, and full remote source-tree verification precedes CI. The archive contains no credentials, unrelated private data or signing material. Earlier rejected/withdrawn audits remain withdrawn. This is bounded model-based linguistic/source review, not native-speaker certification, all-language completion or release acceptance.
