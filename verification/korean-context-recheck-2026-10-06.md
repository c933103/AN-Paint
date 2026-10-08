# Korean context and evidence recheck — 6 October 2026

This is a new, bounded recheck of PR #12 at
`a92d5a2a03cd4090335bb9bcac786ec6acd56040`, with the XML repairs described below.
It does not reinstate the withdrawn September claims or mark the full PR complete.
The latest eight conversation transcripts were not available in full. Other
locales, including Vietnamese/Nôm, are outside this particular semantic recheck.

## Corrections in the current catalogues

The recovery-export result in `ko-KR` and `ko-Kore-KR` still directed the user to
`이미지 불러오기`, while the actual File command is `이미지 열기…`. The assembly
output error in all three Korean catalogues used the descriptive name
`이미지 조합` / `화상 조합` instead of the available command
`이미지 합치기…` / `화상 합치기…`.

Both messages now give the complete, literal File → command route in each
locale. The recovery message also states separately that the ZIP includes draft
settings and includes a floating selection **when one exists**. The previous
Korean clause left the scope of that condition ambiguous. These are two edited
resources per locale; `ko-KP` retains `화상`, `령역` and `리용`.

The same current-source check found `language20_translation_note` claiming that
all translatable interface text was included, in all three Korean variants.
That did not translate the English source's language heading or its explanation
that new/untranslated text appears in English. Each Korean note now preserves
the heading, resource-maintenance explanation and English-fallback condition.
The title agrees with `language20_app_language`, including `응용프로그람 언어`
for `ko-KP`. This adds one edit per locale: **nine XML values total**. It does not
claim the same defect is resolved across every locale.

The evidence is the actual command map in
[`ClassicPaintActivity.kt`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt)
(`menuActions`, `exportRecoveryTo`, assembly result handling), and
[`AutosaveStore.kt`](../Paintroid/src/main/java/org/catrobat/paintroid/classic/AutosaveStore.kt)
(`write`: unconditional `draft.json` and `canvas.png`, conditional `floating.png`).
The language note's source is `res/values/strings.xml`, displayed by
`AppLanguage.kt` in the language chooser.
No application command or drawing behavior was changed.

The reported North Korean PDF corruption is absent in the inspected source:
`formats22_pdf_dimensions` says `너무 커서 가져올 수 없습니다` in its size
explanation, with no `지시자` substitution. This is a fresh check of this one
warning, not a completion finding for North Korean.

## Eight concept decisions

The current English and Korean resources were read in their app contexts:
buttons, menus, import/export warnings, drawing/selection help, assembly help,
save settings and the crop-count plural. The table records the editorial
decisions for these eight concepts. It does not label them all corpus-attested.

| Concept | Retained `ko-Kore-KR` wording | Actual resource contexts and decision |
| --- | --- | --- |
| Image | 이미지 | `ui_image`, `ui_new_image`, `gallery_use_image`, `formats22_animation_message`, `ui_crop_preview_images/other`: the bitmap/artwork being opened, edited or counted. Retain the Korean loan and its Korean particles; do not silently change the underlying word to 畫像. Recovery and assembly command routes were corrected above. |
| Colour | 色相; existing 색 and native colour names remain | `ui_colour_tab23`, `ui_swap23`, `ui_wheel`, `colour_invalid_metadata`, `save20_unsupported_tagged_colour`: visual colour values and colour-management metadata. The [AKS 빛깔 article](https://encykorea.aks.ac.kr/Article/E0025316) explicitly pairs 색상 with 色相 in its colour discussion. Its technical discussion also distinguishes hue from the broader colour concept: this does not justify converting every occurrence of native 색 into 色相 or treating every colour as HSV hue. The existing hue/value/saturation labels retain their distinctions. |
| Settings | 設定 | `language20_settings`, `ui_drawing_settings`, `ui_save_explanation23`, `ui_cursor_help31`: configurable app/drawing/export parameters, not a sexual homograph. Dictionary line 201514 is 設定/설정; line 130565 is the unrelated 泄精/설정. [NIKL 온용어 entry 2491042](https://kli.korean.go.kr/term/trgtWord/indexTrgtWord.do?trgtWordNo=2491042) independently shows 設定 in a technical compound. Its definition is initialization of a medium, so it supplies spelling/technical-domain support, not the definition of this app's Settings menu. |
| Save | 貯藏 | `ui_save`, `save20_title`, `ui_draft_saved`, `colour20_save_slot`, `ui_export_did_not_save23`: persist image/draft/palette data. Dictionary line 207759 is 貯藏/저장; the other 저장 rows 15025 (低張) and 189016 (苴杖) are inapplicable. `ui_help23`, `ui_save_explanation23`, `ui_share_explanation34` and `ui_export_explanation23` keep Save's remembered destination, sharing's copy and export's unchanged Save destination distinct. This is an editorial technical application of dictionary spelling; the inaccessible old basic-dictionary page is not counted as a fresh source check. |
| Select | 選擇 | `ui_select_all`, `ui_category_selection`, `ui_commit_selection`, `formats22_page_description`, `ui_delete_selection`: choosing an item or operating on the selected region. Dictionary line 220023 is 選擇/선택. The independently published civic pair in Article 15 is a component of 직업선택/職業選擇, not an image-editor example. Korean particles and verbal endings remain Hangul; no claim that civic usage validates every UI sentence. |
| Edit | 編輯 | `ui_menu_edit`, `ui_keep_editing23`, `ui_could_not_complete_the_edit`, `gallery_edit_credits`, `ui_edit_in_paint`: modifying the image or credit text. Dictionary line 175938 is 編輯/편집, not 偏執/편집 at 19465. The [AKS 비선형 편집 article](https://encykorea.aks.ac.kr/Article/E0074626) gives 編輯 and discusses manipulation of digital images. This supports the relevant editing sense rather than an unrelated homograph. |
| File | 파일 | `ui_menu_file`, `save20_file_name`, `save20_file_format`, `formats22_pdf_file_size`, `ui_you_can_add_more_images_select_fewer_files`: computer files and their names, sizes and count. This loan stays Hangul. The pinned dictionary's 파일 homographs 八日 (25536) and 破日 (160960) are not computer-file spellings. No new claim of a directly replayed loanword dictionary entry is made. |
| Memory | 메모리 | `ui_estimated_memory_current_working_budget`, `ui_no_resize_fits_decoder_memory`, `ui_assembly_source_memory_floor`, `formats22_pdf_memory`: decoding and editing memory, not persistent file size or human recollection. [NIKL 온용어 entry 202078](https://kli.korean.go.kr/term/trgtWord/indexTrgtWord.do?trgtWordNo=202078) records English `memory` and a computer-storage-device sense. Keep the established loan; this does not require replacing it with a different Sino-Korean expression. The decoder-floor messages still say reducing output dimensions cannot always solve source decoding memory. |

The eight lexemes also underwent an occurrence comparison across current
`ko-KR` and `ko-Kore-KR`, including plural items. Counts are equal per resource,
with the following totals after the repairs. These are **mechanical coverage
counts**, not scores of linguistic correctness. Compounds count as occurrences;
native synonyms such as 색 are not included in the 색상 count.

| Lexeme pair | Resources per catalogue | Occurrences per catalogue |
| --- | ---: | ---: |
| 이미지 / 이미지 | 144 | 212 |
| 색상 / 色相 | 20 | 29 |
| 설정 / 設定 | 18 | 32 |
| 저장 / 貯藏 | 61 | 91 |
| 선택 / 選擇 | 62 | 104 |
| 편집 / 編輯 | 30 | 44 |
| 파일 / 파일 | 44 | 69 |
| 메모리 / 메모리 | 26 | 30 |

These choices concern `ko-KR`/`ko-Kore-KR`; they do not overwrite `ko-KP`'s
different lexical choices. Registration still uses `ko-Kore-KR` in
`translations/language-options.json` and `res/xml/app_locales.xml`, and the
catalogue actually combines Hangul grammar/loans with Hanja. Device language
selection and typography were not run during this recheck.

## Dictionary evidence replayed

Downloaded the [pinned Gukhanmun TSV](https://raw.githubusercontent.com/dahlia/gukhanmun/fb9d665bef5aee48532111534912dbac20bc6a0c/crates/gukhanmun-stdict/data/stdict.tsv)
on 6 October. Its SHA-256 is
`4e3796dfc85a16345b7c4395d89f68e23a5606fd03f62da5d197c77dc75c438a`.
This is Gukhanmun's derived NIKL Standard Korean Language Dictionary data,
not a newly downloaded original NIKL JSON dump. The source identities and
CC BY-SA 2.0 KR attribution to NIKL/Gukhanmun recorded with the existing
inventory still apply; no dictionary prose is added here.

All **91 exact pairs** match the precise recorded TSV lines. The component
coordinates for the **six editorial choices** also match. In particular,
다시 실행 → 再實行 is a synonym choice: line 27646 gives 재/再, not a Hanja
reading of the native word 다시. The other five are transparent compositions
for 무손실, 미배치, 배경색, 전경색 and 회색조. Checking their components does not
make any of the six exact dictionary headwords or corpus-attested expressions.

All **97 inventory examples** occur in the current corresponding XML resource
in both scripts, including plural text where applicable. This does not prove
that the historical inventory exhausts every possible Hanja choice. Reproduce:

```sh
python tools/verify_korean_dictionary_evidence.py /path/to/stdict.tsv
```

The checker validates the external hash, exact ordered Hanja/Hangul columns,
explicit component coordinates and actual current example text. It never
rewrites XML. An altered input fails before any positive report.

## Corpus findings and specific remaining source limits

The [OKHC publisher repository](https://github.com/seyoungsong/OKHC) and
[dataset card](https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus)
were re-opened. The publisher describes an archive collection containing
multiple domains and mixed-script text, not a Bible-only corpus. That establishes
the source's intended breadth, not the validity of the selected occurrence rows.

The pinned 254,638,515-byte `gongu.jsonl` could not be downloaded: the execution
environment returned HTTP 403, including a CONNECT-tunnel rejection. Both Hub
resolve URL forms, raw access, a datasets-server request and an explicit network
permission request failed. The dataset card also reports an unavailable full
viewer caused by `DatasetGenerationError`. The small publisher sample at
Git commit `0a7d82fa01ea4896064dae1a14eb7ba684619220` was retrievable:
344 records, SHA-256
`52805f56a08e86d9536cf0e8a4801c25ae76a446653b6d82cae35de4348993ed`.
It supplies no exact annotated match for the 97 inventory pairs under either
the existing Hangul(Hanja) rule or the checked reverse annotation form. It is
**not** substituted for the missing full-file replay.

Consequently, the old 42 literary rows, their offsets, the claimed 41 accepted
occurrences, record totals and the 47-pair cross-source union remain unverified
in this recheck. The existing corpus checker now calls `accepted_occurrence`
and `rejected_ui_sense` **historical TSV labels** in its output. Its hash and
coordinate assertions remain intact. Successful mechanical replay would not
restore the withdrawn semantic acceptance.

The [published paired Constitution page](https://ko.wikisource.org/wiki/대한민국헌법_(한자혼용))
was accessible through its title URL; its footer identifies revision **407869**.
The selected twelve civic pairs were re-read in both columns: Article 5(2)
안전/安全, 7(1) 전체/全體, 11(1) 영역/領域, 15 선택/選擇, 53(3) 수정/修正,
53(6) 확정/確定, 56 변경/變更 and 추가/追加, 82 문서/文書, 114(7) 범위/範圍,
124 품질/品質 and 127(1) 정보/情報. This is evidence of the published
transcription's usage in civic prose. Compound boundaries in the original table
remain important; in 53(6), only 확정법률 is written 確定法律, whereas two other
occurrences of 확정 remain Hangul.

This does **not** close primary-Gazette verification. The [National Archives
viewer](https://theme.archives.go.kr/viewer/common/archWebViewer.do?singleData=N&archiveEventId=0052442367)
and [scan's file description](https://ko.wikisource.org/wiki/파일:Gwanbo,_vol._10771-2.pdf)
were located, but the PDF exceeded the web tool's size limit and execution
downloads of the PDF/page image were denied with HTTP 403. The scan was not
visually inspected. The original clause hashes were not replayed from an exact
downloaded text snapshot, and a main-page revision does not freeze transclusions.
Attribution for the paired transcription remains Wikisource contributors under
CC BY-SA 4.0; no new complete clauses are reproduced here.

The old NIKL basic-dictionary URLs for 이미지 and 저장 were also inaccessible
in this run. Their historical citations are not presented as freshly verified.
The accessible AKS and 온용어 sources above, dictionary row checks and direct
application contexts support the bounded editorial decisions, while complete
literary/source-image attestation remains open.

## Validation and snapshots

Validation on the final edited source:

- `python -m unittest discover -s tools -p 'test_*.py'`: **104 passed**.
- `/tmp/an-paint-aapt2/aapt2 compile --dir Paintroid/src/main/res -o /tmp/an-paint-pr12-resources.zip`:
  passed, with no legacy-mode option.
- Dictionary replay: 91 exact rows, component rows for six editorial choices,
  and 97 current XML examples passed. Deliberately altered source bytes were
  rejected by the hash check; a controlled wrong-homograph fixture was also
  rejected at the expected line by the pair check.
- `git diff --check`: passed.

These checks validate resources, source coordinates and route consistency, not
native-speaker approval or device rendering. The full literary-corpus verifier
was not run against the unavailable 254 MB source. Source XML SHA-256 after the
nine repairs:

| Catalogue | SHA-256 |
| --- | --- |
| `values-b+ko+KR/strings.xml` | `b5605527ec6dd272388f446e2cc65c55d51b488bcfcf72ed7a0c12d96703c6dc` |
| `values-b+ko+KP/strings.xml` | `e47fcf06fefc22a9b500fd6c8e900fdbcb78aa598c89813a0189122b10256b82` |
| `values-b+ko+Kore+KR/strings.xml` | `ca3e5ff80452c3629fa033283c26ea9bac2f4811342bbb340201d0a44b4f57de` |

The unchanged `KOREAN_HANJA_REVIEW.tsv` hash is
`d467b64fabed1d30070aee0a858c775c0c9dd908bbfc82307d7a4341eb1a2ff8`.

Register coverage: new evidence for P12-002 (static registration only),
P12-008–011 (example/coordinate arithmetic, not full semantic acceptance),
P12-025–032 (bounded concept/context decisions), P12-033 (the one PDF warning),
and partial P12-012–023 source observations. Complete Korean catalogue review,
full literary replay, Gazette-image checks, Nôm and Android runtime checks remain
open. No pending register row is silently declared complete by this document.
