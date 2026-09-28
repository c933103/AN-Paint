# Localization discussion and source reconciliation — 28 September 2026

**The overall localization task is incomplete.** Two concrete translation defects
remain, and the recorded semantic review has identifiable coverage gaps. Several
other tasks described as pending in the original discussions were implemented
later. They must not be carried forward as if no work had happened.

This report reconciles the eight branch handoffs (#3–#9 and #12), their shared
base #2, the integration discussion, and summary PR #15. It includes discoveries
and updates outside GitHub review comments. Completing the other 81 locales is
outside this task.

## Evidence and limits

The application snapshot inspected is
`50395ad05be90d9b19ef7223289760fa448bb581`, tree
`4f9bc377504a76f43d128041a2f1794815940832`.

Evidence consists of recovered, timestamped conversation summaries/excerpts;
the integration discussion's reported discoveries; GitHub reviews and current
branch heads; actual XML and application source; and the named regression tests
and semantic-review records. The historical audit documents are claims to check,
not independent proof of their own completion assertions.

**Complete latest transcripts for all eight threads were not recovered.** Targeted
history retrieval returned excerpts rather than full tails; searches for matching
conversation exports did not locate them. Consequently, this is the complete
inventory of the obligations and updates recovered in this audit, not a claim
that an unseen later message cannot add or change an obligation. The times below
identify the latest relevant recovered handoffs, not verified final-message times.

“Implemented” below means the specified behavior or repair is present in source.
“Recorded review” means a substantive review is documented, with concrete changes;
it does not claim that this reconciliation independently retranslated every string.
An evidence limitation is not automatically a translation defect or a new acceptance
requirement. Native-speaker certification and corpus attestation of every Korean
term are not imposed as additional requirements.

## Work still to be done

| ID | Outstanding work | Evidence and completion condition |
| --- | --- | --- |
| R1 | Finish reconciling the genuinely latest conclusions of all eight threads when their full tails can be obtained. | Current retrieval supplies branch-specific excerpts, not all latest messages. Match any additional user correction, unfinished instruction or later conclusion to a source change or an explicit open item. Do not substitute the retrospective handoff ledger for those messages. This remains an access/evidence gap. |
| R2 | Repair the two malformed Malay smoothing labels. | `values-ms/strings.xml`: `ui_smooth_freehand_strokes` contains `Pakiniskan sapuan bebas`; `ui_smooth_pixel_edges_anti_aliasing` contains `Pakiniskan tepi piksel (antialias)`. Correct the Malay wording in both #3 and integration, preserving the distinction between stroke smoothing and edge antialiasing. No repair is claimed by this report. |
| R3 | Restore the Traditional Mongolian legacy manual's assembly capacity clause. | `values-b+mn+Mong/strings.xml`: `ui_the_arrow_on_the_left_directly_below_the` omits the source's “up to 20 images.” The separate assembly help retains 20 and does not close this omission. Repair the actual reviewed legacy resource in #8 and integration; compare the complete source paragraph for any companion omission. The shorter active `ui_help23` is not the source of this specific missing clause. |
| R4 | Complete the identified semantic-review gaps within the requested locale scopes. | The #3/#4 review explicitly covered Malay/Indonesian manuals and non-manual entries **longer than 100 characters** (62 Malay / 66 Indonesian at that snapshot). Review the excluded short controls and messages; the surviving Malay defect is in this excluded set. For the other #4 languages the recorded evidence establishes selected shared repairs, not a complete sentence-by-sentence pass. Establish the remaining review coverage from the original obligations and record what was actually read. Existing full Ainu/Manchu/Jeju/Okinawan reviews should not be relabelled as never attempted. |
| R5 | Apply each newly established shared defect to every affected use and locale, including discoveries outside PR comments. | Compare active and legacy manuals, duplicate hints, labels, plurals, source defaults, script pairs and app behavior where relevant. The earlier gallery, Show all, paste-route and selection-caption findings show why fixing one originating PR or one resource is insufficient. Propagate defects shown by comparison; do not assume every language shares a linguistic error. |
| R6 | Validate and publish the resulting source repairs, then update conclusions to match the evidence. | Preserve each original PR's scope and shared integration behavior. Verify intended/published trees, run relevant structural/semantic/resource checks and obtain Android checks for changed application/resource source as required. Existing CI is green; these are checks for future repairs, not an outstanding failure of the current runs. Keep completion claims bounded by R1 and R4. No merge is part of this reconciliation. |

R2 and R3 are confirmed source defects. R4 is a demonstrated review-coverage
gap. R1 is incomplete history access. R5–R6 describe the remaining propagation
and acceptance work for newly established repairs. They are not assertions that
every previously repaired feature is broken.

The documentation corrections made with this report are already done: the
Manchu progress figure is corrected, the residual #8 finding is reopened in the
review ledger, and broad handoff-completion claims are replaced with this bounded
status. These documentation changes do not fix R2 or R3.

## Eight branch handoffs and the shared base

Resource paths in this section are under `Paintroid/src/main/res`. Each of the
57 requested locale catalogues contains 669 strings and the plural resource.
That establishes key coverage, not semantic correctness.

| Scope / latest relevant recovered handoff | Original conclusion or unfinished instruction | What later source and discussion establish | Current disposition |
| --- | --- | --- | --- |
| Shared base #2; 22 Sep 03:16–03:18, 04:19 and 06:18 UTC | Use direct locale XML; upstream translations are references, not authority. Finish Japanese, Hong Kong/Taiwan Chinese, then Mainland Chinese and Cantonese Han/Jyutping. | `TRANSLATING.md`, `crowdin.yml` and `tools/translation_catalogues.py` implement direct XML. The old translation generator is absent. Six catalogues have coverage; Japanese flip controls and Cantonese Fit/italic/line-spacing readings were repaired. `localization-base-caption-audit.md` records contextual readings and actual menu routes. | Workflow and named repairs implemented. No new #2 defect established here; counts and selected reading checks are not whole-catalogue certification. |
| #3 Tagalog, Cebuano, Malay, Indonesian; 22 Sep 06:54 | Mechanical Cebuano conversion had corrupted words; the assistant reported rewriting all 669 entries. Indonesian Malay leakage was reported removed. | Indonesian `nyahaktif` is absent and disabling labels use Indonesian wording. Later independent Cebuano review repaired working draft versus initial work and positive-width/height PDF crop meaning. Later help/navigation/zoom repairs are present. Malay `Pakiniskan` survives in two short controls. | Specific later repairs implemented; R2 and the #3 portion of R4 remain open. The reported “ready” status does not survive the current source finding. |
| #4 Swahili, Finnish, Hungarian, Afrikaans, Dutch, Estonian, Latvian, Lithuanian; 23 Sep 00:40 | Eight catalogues reported complete, with deliberate retention of valid technical/borrowed English matches; CI had not run on the old stacked base. | Dutch tool captions and decoder-memory condition, shared Show all/Fit/Swap routes, placement and selected zoom clauses were repaired. Lithuanian `few` and Android apostrophes are fixed. Dutch Menu/Pixels/Canvas and Afrikaans Radius are deliberate retained terms, not automatic defects. Current CI passes. | Named findings implemented. Recorded review is selected shared repairs; its limits belong in R4. Historical CI absence is closed. |
| #5 Spanish variants, French, German, Russian, Arabic, Esperanto; 23 Sep 03:12–03:23 | Finish remaining language tails and terminology; Russian four / Arabic six plural categories; Esperanto cursor and control meanings; CI pending. | All seven catalogues have coverage. Russian one/few/many/other and Arabic zero/one/two/few/many/other exist. Arabic affected-count meanings were repaired. French Star, Esperanto Fit/foreground/background/cursor text and shared actual-caption routes are present. | Concrete recovered tasks implemented; no additional current #5 defect established by this reconciliation. Current CI passes. |
| #6 Literary Chinese, Hakka Han/PFS, Taiwanese Han/POJ, Wu; 23 Sep 17:20, with earlier 02:51, 05:23 and 08:29 updates | Resolve Hakka Han/Latin synonym mismatch and wrong regional readings; inspect Ministry Sixian evidence and map to PFS; resolve dictionary gaps; clean Wu conversion/register; finish paired review, validation and publication. | 保存 now corresponds to `Pó-sùn`; all 58 Han entries containing 保存 have the corresponding Latin term. The missing remembered-choice clause appears in both scripts. Contextual system uses `ne-thúng`. Official dictionary entry IDs/hash and 47 decisions are recorded. Actual changes also exist in Literary Chinese, Taiwanese and Wu; Wu strikethrough and PDF error prose are corrected. All six complete-resource checks pass. | Substantive implementation confirmed. The raw dictionary was not replayed in this audit; selected source checks do not certify every sentence. Neither limitation by itself proves an unfinished translation. |
| #7 English variants, Portuguese variants, Italian, Greek, Turkish; 23 Sep 03:02 and 05:24 | Default-English language note explicitly deferred; twelve catalogues reported ready; duplicate pt-PT and stacked CI unresolved. | Default `values/strings.xml:language20_translation_note` now refers to AN Paint resources. Only `values-b+pt+PT` remains. All twelve catalogues have coverage; source and translated menu routes were repaired. Later Brazilian Portuguese terminology work is recorded in the integration discussion and `localization-integration-review.md`; it was not independently reread in full here. | Recovered deferred tasks implemented. Current CI passes. No additional current #7 defect established here. |
| #8 Tibetan, Dzongkha, both Mongolian scripts; 23 Sep 00:54, 05:26 and 05:34 | Tibetan had a remaining codec/export/gallery/cursor tail; Dzongkha Keep editing and further format/gallery/save/import work remained before the final completeness claim. | Keep editing was already repaired in original `6d591aa6f` at 05:31:43. All four tails are structurally present. Later source/credit, save-before-sharing, destination, menu-caption and dithering repairs are present. The Traditional Mongolian legacy capacity clause remains missing. | Historical tail/Keep editing tasks are not newly open. R3 disproves the broad meaning-completeness claim; review of that exact manual must be completed. |
| #9 Jeju, Manchu, Ainu Latin/Kana, Okinawan; 23 Sep 00:44, 05:31, 08:37 and 08:53 | Finish Jeju grammar; finish Manchu's remaining 44 of 669 entries, Unicode checks and other minority-language work; repair stale cju test. | The correct Manchu status was **625 complete / 44 remaining**, not 44 complete. All five now have coverage. `jje` is current and `cju` only migrates. Full source-assisted Ainu/Manchu readings, Jeju full-clause/predicate review and Okinawan full/short-action grammar reviews are documented. Later Ainu meaning and Okinawan connected-polygon/selection-caption findings were repaired. | Concrete work and review records present. No new #9 defect established here. No invented native-speaker approval gate is added. Full latest-tail reconciliation remains subject to R1. |
| #12 Korean variants, Korean mixed script, Vietnamese and Nôm; 23 Sep 05:43, 13:33 and 17:02 | User required `ko-Kore-KR`, not Hanja-only. Finish reviewed Hangul/Hanja inventory, general-domain evidence beyond Bible-only sources, and eight explicit UI concept decisions; validate five catalogues. | Correct mixed-script tag is registered. All 97 inventory examples match current XML; 91 have exact dictionary evidence and six explicit editorial evidence. External literary and civic records support 47 distinct accepted pairs. The eight concept decisions appear in actual XML. North Korean “too cursor” corruption and Nôm contextual homophones were repaired; Nôm UI font rebuilt for actual used characters. | Inventory, bounded corpus work, script registration and named repairs implemented. No new #12 defect established. Raw corpus and Gazette sources were not independently replayed in this audit; that limit does not make the other 50 pairs automatically wrong. |

Supporting review records are linked from
[the integration review](localization-integration-review.md). The scoped
Malay/Indonesian cutoff is explicitly documented in
[the PR3/4 handoff review](localization-pr3-pr4-handoff-review.md).

## Findings and updates outside PR review comments

These must remain part of the reconciliation even though they are not among the
15 inline GitHub findings. “Present” refers to inspected source or the named
review/test evidence, with the distinction recorded above.

| Discussion discovery or requirement | Later implementation / evidence | Disposition |
| --- | --- | --- |
| Direct per-locale XML; no live translation generation or preferred upstream authority | `TRANSLATING.md`, direct Crowdin XML mapping, XML-reading validator; historical JSON is provenance. | Present. |
| Indonesian and Brazilian Portuguese needed substantive meaning fixes, including clipboard terminology | The integration discussion and `localization-integration-review.md` record those rewrites. Later Indonesian navigation/zoom and help repairs were inspected in current XML. | Recorded repairs preserved in current catalogue versions; the whole Indonesian/Portuguese rewrite was not independently reread in this audit. |
| Cebuano mechanical corruption and a test rejecting legitimate File borrowing | Authored prose and subsequent independent meaning checks; tests permit legitimate technical loanwords instead of requiring every caption to differ from English. | Present. |
| Cebuano draft incorrectly implied initial work; PDF crop incorrectly implied visible content | `values-b+ceb`: draft terminology and explicit positive width/height crop condition. | Present. |
| Hakka inconsistent Han/Latin synonyms, wrong regional readings, guessed character mappings, missing remembered choice | Han/PFS source pairs, Ministry entry-level evidence and contextual decisions; actual matching Save and remembered-choice entries. | Named repairs present; raw dictionary replay not performed here. |
| Cantonese readings depended on context, including rows versus walking | `localization-base-caption-audit.md`; actual italic and line-spacing forms and matching control references. | Checked repairs present. |
| Taiwanese, Wu and Literary Chinese substitutions changed meaning | `NAN_WUU_LZH_HANDOFF_REVIEW.md`, Sinitic audit and substantial actual XML deltas; not merely punctuation changes. | Recorded language-specific review and checked repairs present. |
| Jeju Korean-like substitutions and finite-predicate grammar | `JEJU_GRAMMAR_REVIEW.md` documents full reading, then predicate and memory corrections. | Recorded substantive review present. |
| Okinawan Japanese grammar in short actions; later rewrite omitted connected polygon segment and named the wrong aspect-ratio control | `OKINAWAN_GRAMMAR_REVIEW.md`; actual captions and polygon/selection text, plus shared selection regression. | Recorded repairs present; final findings must remain in the history. |
| Ainu file count versus size and Select all instruction placement; Manchu lexical and Unicode problems | `AINU_SEMANTIC_AUDIT.md`, `MANCHU_SEMANTIC_AUDIT.md`, actual paired Ainu/manchu catalogues and glyph checks. | Recorded repairs present; no new concrete defect found here. |
| Korean general-domain evidence, not merely script presence or Bible evidence | `KOREAN_CORPUS_OCCURRENCES.tsv`: 42 literary occurrences, 41 accepted and one rejected. `KOREAN_PARALLEL_PROSE.tsv`: 12 civic spans. Accepted union: 47 distinct app pairs. `verify_korean_corpus_evidence.py` checks source hashes, IDs, offsets and text. | Implemented bounded evidence; 254 MB raw corpus absent locally, so fresh source replay not claimed. |
| Korean eight concept decisions and corrupted North Korean PDF wording | Current mixed-script XML uses 이미지, 色相, 設定, 貯藏, 選擇, 編輯, 파일 and 메모리 as decided. KP dimensions warning now uses 너무 커서. | Present; all inventory example references checked against current XML, including plurals. |
| Nôm contextually unrelated homophones; font had to follow semantic edits | `NOM_CONTEXT_REVIEW.md/.tsv`; recorded 404-string semantic batch and later final source changes; font covers 622 used ideographs, 157 supplementary. | Repairs/font rebuild preserved. A final comparison against the older baseline counts 405 changed values; this differs from the earlier batch count, not evidence of lost work. |
| Credits were app-wide / added before insertion committed | `PaintDocument`, `ImageCredit`, `RasterHistory`, `HistoryArchive`; `ImageCreditLifecycleTest` checks document ownership, commit/cancel, undo/redo, clipboard, repeated insert, clearing/new document and draft/history restoration. | Shared implementation and regression coverage present in integration. |
| Gallery credit edits disappeared after recreation | `MediaGalleryActivity` persists credit result and edit flag; `GalleryImportTest` checks edited and untouched exits. | Present. |
| Save and Export need collapsed, selectable credits with Copy all, preserving original credit language | `SaveOptionsDialog`; `ExportFormatDialogTest.saveAndExportOfferCollapsedSelectableCreditsAndCopyThemWithoutStartingSave`. | Present for both dialogs. |
| Mongolian/Manchu vertical UI, Literary Chinese opposite column direction, English/emoji test locales | `VerticalText.uiDirection`, locale registrations, layout/picker tests and persistence/round-trip tests for `en-XV` / `qaa-Zsye-XV`. | Present. Mong-script columns advance left to right; Literary Chinese right to left. |
| BMP emoji such as checkmark/gear rotated sideways; variation selectors and subdivision flags split | `VerticalText.upright` and `clusters`; `ViewportAndVerticalTextTest` checks mixed symbols, selectors/keycaps and subdivision tags during measurement/wrapping. | Present; this is later discussion work beyond the original Manchu PR finding. |
| App-injected web-gallery buttons bypassed native fonts and vertical layout | `GalleryTypography` embeds fonts and scopes styles to AN Paint controls; corresponding tests check selectors, bytes and direction. | Present in #12 and integration. |
| Locale font application crashed on untagged controls | `LocaleTypography.apply` handles nullable tags; test includes untagged and newly added controls. | Present in #12 and integration. Historical failure is closed. |
| Nôm UI font appeared in drawing-font choices; weakening font test would hide missing assets | `FontCatalog` excludes `ui_only`; typography test preserves selected drawing fonts. `NativeCodecTest.everyAdvertisedBundledFontLoadsItsActualFontFile` still loads/hashes every font. Wu fallback is also integrated. | Present; actual-asset verification retained. |
| Hakka Taiwan tags and migration from earlier preferences | `AppLanguageTest`, `app_language_tags.xml`, `app_locales.xml`; migrations covered on pre-/post-platform-locale preference paths. | Present. |
| Literal percent regressions despite valid XML; local Kotlin/Maven access failure | Validator distinguishes static `formatted="false"` from runtime `%%`; regression checks and resource compilation retained. Full Android validation is supplied by published CI. | Percent repairs present. Local dependency access is not a remaining source defect. |
| Shared gallery route test missed active resources and final copyright paragraph | `tools/test_localized_help.py` reads all relevant XMLs and checks three active gallery resources plus final copyright text separately. | Present. The recorded first 54 failing subchecks were repaired; they are historical discoveries, not 54 current failures. |
| Nonexistent Show all changes caption; shortened Fit/Swap/Navigate controls and stale File/Draw routes | Current actual captions, active and legacy help; global localized-help regressions. | Recorded repairs present; #8's distinct missing capacity clause remains open under R3. |
| Cursor-settings help missing outside originating languages | `localization-cursor-help-followup.md`; Armenian, Serbian Cyrillic/Latin, Hebrew, Polish, Thai repairs and alias-aware global check. | Present. This specific shared repair does not expand the task to completing 81 locales. |
| Retained duplicate copy/paste hint still named obsolete File → Insert image route | Both hint resource names checked in `test_localized_help.py`; affected entries use reviewed active wording. | Present. Fixing only the active hint would not have closed this. |
| Selection tooltip quoted resize-dialog checkbox; also affected Japanese, Russian and Swahili | Actual Lock proportions control used; regression rejects the identified wrong-caption substitution while allowing native paraphrases. | Present across identified affected locales. |
| Workspace restored an old snapshot and unpublished audit work was missing | Recovery/checkpoint commits `1c924c6178`, `7309e1b1b`, `0c8ac3fe6`; published original heads included in current integration. All 57 owned XML files now match originals exactly. | Recovered published work is preserved. This does not recover missing conversation transcripts. |
| Earlier completion summaries treated counts, resolved flags and CI as linguistic completion | Current report distinguishes concrete defects, implementation, recorded review and missing history. The handoff/review summaries are corrected with this documentation change. | Status corrected; source completion still blocked by the open items above. |

## Inline PR findings and current publication

The [PR review ledger](../translations/PR_REVIEW_AUDIT.md) records all 15 inline
findings, seven submitted review bodies and eleven issue-discussion records.
The review bodies do not add substantive findings beyond their inline comments.
The current dispositions of those 15 findings are:

- #4: Android apostrophes and Lithuanian plural category — repairs present.
- #5: corrupted French Star — repair present.
- #6: Base64 prefix, CC BY-SA identifier, GIF numeric limit and Literary Chinese
  image-replacement meaning — repairs and relevant guards present.
- #7: duplicate pt-PT configuration — removed, equivalent-qualifier guard present.
- #8: truncated legacy manual — **partially repaired; R3 remains**. Separate
  assembly operational clauses and Irasutoya conditions received recorded repairs.
- #9: stale cju assertion and Manchu vertical UI — repairs present.
- #12: Nôm font coverage and Korean regex escaping — repairs present; the later
  semantic/corpus work is separately accounted for above.

All 15 threads being marked resolved does not close R3. #2 and #3 had quota
notices instead of submitted code reviews. #15 had no submitted review at the
recorded retrieval. None of these old reviews is a fresh review of the repaired
current heads; this fact is not invented as a new mandatory review gate.

All owned locale XMLs were compared directly between current original heads and
the integration snapshot: **57/57 are byte-identical, with no missing or duplicate
owned-locale paths**. Shared application changes deliberately live in integration;
their absence from an unrelated original language branch is not missing behavior
in the combined app.

| PR | Inspected head | Owned locales matching integration | Android run, checked 28 Sep |
| --- | --- | ---: | --- |
| #2 | `8cf4ed2e5` | 6/6 | [36175227320](https://github.com/c933103/AN-Paint/actions/runs/36175227320), passed |
| #3 | `8a3a17ca1` | 4/4 | [36175252567](https://github.com/c933103/AN-Paint/actions/runs/36175252567), passed |
| #4 | `c07dfb366` | 8/8 | [36175278920](https://github.com/c933103/AN-Paint/actions/runs/36175278920), passed |
| #5 | `aeec0d053` | 7/7 | [36175302649](https://github.com/c933103/AN-Paint/actions/runs/36175302649), passed |
| #6 | `d7de53e33` | 6/6 | [36175454796](https://github.com/c933103/AN-Paint/actions/runs/36175454796), passed |
| #7 | `b528c9d2a` | 12/12 | [36175478621](https://github.com/c933103/AN-Paint/actions/runs/36175478621), passed |
| #8 | `72aa3bd2c` | 4/4 | [36175503191](https://github.com/c933103/AN-Paint/actions/runs/36175503191), passed |
| #9 | `97e511dc6` | 5/5 | [36175529316](https://github.com/c933103/AN-Paint/actions/runs/36175529316), passed |
| #12 | `3d674096f` | 5/5 | [36175559899](https://github.com/c933103/AN-Paint/actions/runs/36175559899), passed |
| #15 | `50395ad05` | Combined | [36175711603](https://github.com/c933103/AN-Paint/actions/runs/36175711603), passed |

This reconciliation changes documentation only. It does not rerun Android tests
or present the above runs as tests of new source repairs. `CI.md` and the workflow
exclude Markdown/historical-verification-only changes from automatic rebuilds.
The earlier 109 host checks and strict resource compilation remain evidence for
their stated source snapshot. No PR has been merged.
