# Arabic, Russian and Brazilian Portuguese: current P0/P1 context review

2026-10-29. Source commit `47d5e64e8e20ef3e13641a05ee83c61203316a82`, tree `e480662481ba9f5eea2122296d18382d82f628d4`. Native chat-side work; no Work task or delegated subtask.

## Result

All **341 complete P0/P1 pairs per language** (92 P0 + 249 P1, 1,023 pairs total) were read against canonical English and current direct caller context. All are present. No mandatory priority-value change was found. Nineteen essential companion identities per language were also read; only **three companion containers** need correction: Arabic page count, Brazilian Portuguese page count, and Brazilian Portuguese crop preview (both quantities). Russian remains source-unchanged, review-only. `corrections.json` binds the complete before/source/after values and specific callers.

These are fresh model judgments, independent of the historical author-ledger pass—not a native-human certificate. Broad priority review and three authored corrections are separate scopes. Existing exact historic receipts are carried, never counted a second time as newly translated or independently accepted work.

## Review-only inventories and limits

`scope.json` gives one shared complete priority identity inventory and a separate per-language disposition inventory. Defaults and explicit exceptions partition every key; catalogue values are referenced by immutable source/blob, not duplicated as application test oracles.

| Language | Retained model/context review | Wording only, no direct caller | Holds | Mandatory priority edits | Companion corrections |
|---|---:|---:|---:|---:|---:|
| ar | 311 | 29 | 1 | 0 | 1 |
| ru | 309 | 29 | 3 | 0 | 0 |
| pt-BR | 309 | 29 | 3 | 0 | 2 |

Thirty keys have no current direct `R.string` reference; that is not proof of no runtime route. Twenty-nine receive wording-only disposition. The remaining combined foreground/background/palette label stays held because its third state argument is unestablished. Brazilian Portuguese's historical FG/BG visible-label/fit holds remain held; Russian's identical English-derived abbreviations have the same unresolved local-short-label/fit question. Neither is declared a demonstrated mistranslation. Arabic's already accepted مقدمة/خلفية remain exact; the 132×88 dp swatch and shrink-to-width drawing code do not establish native readability, bidi/shaping or all-screen fit.

Direct callers were inspected through 104 deduplicated windows and complete essential boundaries: destructive confirmation versus keep editing; Save versus export/copy/share; recovery ZIP and canvas.png; sampled decoder/assembly memory limits; errors from import/colour codecs and providers; canvas/selection transforms; numeric dimensions/units; tool categories and selected tool; touch gestures; colour state and palette; crop counts/attachments; PDF/TIFF pages and animation composition; typography and export controls. File bindings are inputs, not claims that every line in every bound file was reviewed. Existing generic navigation tests and layout source were inspected, not rerun or converted into locale-specific render evidence.

No full-language, physical-device, native-speaker, universal fit, screen-reader, shaping/bidi, legal-adequacy or whole-P2/P3 claim. Known unrelated holds and paused lanes remain untouched.

## Historical carry reconciliation, not duplicate credit

- **Arabic:** [prior reconciliation](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6358421602) had A300/W30/I1/C8/M2 in priority scope. Exact current comparison with that 5b9811 snapshot has only the eight PR163 target corrections and the two PR165 warning successors changed; all other 331 complete pairs remain identical. The eight are `formats22_animation_message`, `save20_gif_description`, `ui_bg`, `ui_fg`, `ui_d_d_px_d_pixels_2f_mp`, `ui_hex_rrggbb`, `ui_invalid_selection_outline`, and `ui_trim_amounts_must_fit_inside_each_image_use`. The pre-existing sampled-memory independent receipt remains bounded; older unrecovered historical chains are not retroactively declared recovered.
- **Russian:** [prior ledger](https://github.com/c933103/AN-Paint/blob/9118814b8437a76237bc90c0bccce4332b9734e6/records/localization-review/2026-10-23/123-ru/r01/ledger.json) has U333/Q4/D2/I2 in priority scope. All 341 complete source/target raw-value hashes still match. Q4 (two dimension summaries and two tool-category descriptions), D2 (sampled memory/unsupported colour), and I2 warnings keep their historic provenance; this new context review does not pretend that old Q/D were independent full-value receipts.
- **Brazilian Portuguese:** [prior ledger](https://github.com/c933103/AN-Paint/blob/28d2db63bfb0ba034c1971d972990fdf80f55b24/records/localization-review/2026-10-23/115-pt-BR/r01/ledger.json) has A297/W29/P8/H3/N2/C2 in priority scope. Exactly 339 complete source/target raw-value pairs match; only the two warning successors differ, now integrated through PR165. PR117's eight adopted values retain public-attested provenance; raw independent review outputs are still not recovered. N2 sampled-memory/unsupported-colour old delta scopes are not promoted retrospectively. The H3 questions above remain explicit. No pt-PT acceptance transfers.

Old full Help and narrow non-priority acceptance remain separate; no new review credit is claimed for them. The crop plural is one companion container, not two separate accepted keys.

## Corrections versus optional wording

1. Arabic page description: replace the fixed singular count phrase with `عدد الصفحات: %3$d.`. The defect concerns counts such as 3–10, not all counts; the count-label construction avoids new plural/call-site logic.
2. Brazilian Portuguese page description: `Número de páginas: %3$d.` handles the caller's valid count 1 without `1 páginas`.
3. Brazilian Portuguese crop preview: `pode mover as imagens conectadas a elas` restores conditional movement. The old `também reposiciona` overpromises; cropping metadata and attachment-edge coordinates do not guarantee every attached image moves.

All placeholder positions/types, raw Android newline escapes, plural quantities and resource attributes are preserved. No percent wording was converted to conceal string handling.

“Draw again” in Navigate remains defensible because the visible context is navigation and its action returns to the drawing tool. Alternatives `العودة إلى الرسم`, `Вернуться к рисованию`, and `Voltar a desenhar` are optional clarity only, not mandatory defects: no source or test churn for them. The longer RU/PT-BR alternatives have no exact rendered-fit evidence.

## Focused validation and source delta

Only five application-tree files change: two locale XML files, three finite rows appended to the existing shared fixture, its hash/scope metadata, and the existing test's finite scope/semantic loops. No new helper, test suite, per-language package, test method, whole-catalogue fixture, resource type, call-site logic or application behavior. The scope-test identity maps from `test_exact_three_option_six_container_scope_and_current_values` to `test_exact_five_option_nine_container_scope_and_current_values`; it is renamed, not removed.

`PYTHONPATH=tools python -m unittest test_ordinary_priority_followthrough test_translations.TranslationCatalogueTests.test_eight_arabic_corrections_remain_exact test_brazilian_portuguese_priority_wording -v`: **22 passed**. Existing `validate_catalogue(tag, require_complete=True)` for ar/ru/pt-BR: zero structural errors. `git diff --check`: passed. An initial focused run's completion output was not retained; the recorded run above is the one counted. No full local suite/aggregate cycle, device run or build was performed. Technical checks are not linguistic certification.

Parent chat reviewer independently read the complete three-pair packet, caller behavior and all five file diffs before source publication. Exact-head Codex and standard hosted CI remain separate gates, not implied by these local checks. This records branch is evidence only and must never merge into application branches.

Source branch published at `53403c18f2ad477b16786e4f0e5692ce3f462807`; its tree `8ab9cd529620ab1dddf23fdbcd811d2360ac64c2` exactly matches the locally reviewed five-file tree. Publication is not merge or CI acceptance.
