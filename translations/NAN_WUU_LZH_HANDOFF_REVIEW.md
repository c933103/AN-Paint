# PR #6 remaining handoff review — 25 September 2026

This review resumes the Sinitic thread's unfinished Wu register work and the
Southern Min and Literary Chinese catalogue review. It does not replace the
separate Hakka dictionary audit. The working base was published integration
`7939f1292`, with the shared gallery-route repair applied before this work.

All four catalogues were read in context, including their short tool labels,
accessibility instructions, selection and assembly operations, recovery and
memory warnings, format descriptions, credits, active help, legacy long help,
and crop plural. The Han and Pe̍h-ōe-jī Southern Min versions were compared as a
pair. This is an editorial and source-assisted review, not native-speaker
certification. Resource counts and successful builds do not establish fluency.

## Concrete repairs

| Catalogue | Entries changed after the shared gallery repair | Repairs |
| --- | ---: | --- |
| Literary Chinese (`lzh-Hant`) | 29 | Actual Brush category, Show all, crop and Edit in Paint captions; Save destination; crop-preview resizing; conditional memory fallback; concise classical clause structure |
| Shanghainese-based Wu (`wuu-Hans`) | 99 | Complete result, instruction and warning clauses; disposal/topic structure, completion and potential negatives; decoding and crop constraints; strikethrough label; actual manual controls |
| Southern Min Han (`nan-Hant-TW`) | 82 | Paired native instructions and conditions, progress and recovery messages, vertical directions, memory and file-format constraints, native ellipse term, actual manual controls |
| Southern Min POJ (`nan-Latn-TW`) | 150 | The same semantic rewrites, contextual word readings and POJ spelling, synchronized quoted captions |

Counts describe the patch relative to its base; they are not a quality score.
Technical nouns shared with other Sinitic languages were retained where
appropriate. Prose was revised at the clause level: replacing individual
Mandarin characters with local pronunciations is not a translation method.

Both long manuals now use the actual insertion path **Draw → Insert → Other
images** and assembly path **File → Image assembly**. Their final copyright
paragraphs name **File → About, licences and credits**. The obsolete generic
Menu / Android submenu-arrow clause was removed without losing the adjacent
landscape-control and centred-filename description. The separate **Draw again**
control remains. Quoted labels were compared with the relevant catalogue's
actual controls; paired toolbar captions such as Cut/Copy are intentional.

The old long help resource is not the currently displayed quick-help resource.
It was still reviewed because the original review request covered it. No claim
is made that every description of a historical layout is a current runtime
feature. Active quick help and paste routes use the current ribbon controls.

## Southern Min reading decisions and evidence

The Ministry dictionary distinguishes literary and colloquial readings and
explicitly warns that some have different meanings or fixed word combinations:
[editorial conventions](https://sutian.moe.edu.tw/und-hani/piantsip/piantsip-thele/).
Its transcriptions are Tâi-lô; this catalogue keeps the corresponding POJ spelling.
No transliteration generator was added to the repository or application.

| Context | Decision | Primary evidence |
| --- | --- | --- |
| 像 in 像素 | `siōng`, rather than the reading for “resemble” | [MOE 像](https://sutian.moe.edu.tw/zh-hant/su/10372/) |
| 觸 in 筆觸 | POJ `chhiok`, rather than literal collision `tak` | [MOE literary 觸](https://sutian.moe.edu.tw/zh-hant/siannuntiau/un/iok/_/tshiok4/觸/) |
| 恢復 | POJ `khoe-ho̍k`; the old text lost initial `kh` | [MOE 恢復](https://sutian.moe.edu.tw/zh-hant/su/4957/) |
| 單 in 單詞 | `tan`, not the sheet/list reading | [MOE literary 單](https://sutian.moe.edu.tw/zh-hant/siannuntiau/siann/t/an/tan1/單/) |
| 長按 | Duration reading `tn̂g`, not an elder/leader reading | [MOE 長](https://sutian.moe.edu.tw/zh-hant/su/4493/) |
| 指 in one/two fingers | POJ `chí`, not `cháiⁿ` | [MOE 指 readings](https://sutian.moe.edu.tw/zh-hant/tshiau/?lui=tai_su&tsha=指) |
| 上 in upper surface, above and limit | `siōng`, not the music-note reading `siāng` | [MOE 上](https://sutian.moe.edu.tw/zh-hant/su/166/) |
| 量 in crop amount | Noun `liōng`, not measuring verb `niû` | [MOE noun 量](https://sutian.moe.edu.tw/zh-hant/su/9136/) |
| 行 in toolbar rows | `hâng`, not walking `kiâⁿ` | [MOE 行 search](https://sutian.moe.edu.tw/zh-hant/tshiau/?lui=tai_su&tsha=行) |
| 組合 | Retain documented tone 1, POJ `cho͘-ha̍p` | [MOE exact compound](https://sutian.moe.edu.tw/zh-hant/su/7740/) |
| 桿 in slider | POJ `koáiⁿ`, retaining the nasal diphthong | [MOE 桿](https://sutian.moe.edu.tw/zh-hant/su/7442/) |
| Ellipse | Paired native `長株圓` / `Tn̂g-tu-îⁿ` | [NTNU Taiwanica 23, scientific terminology table](https://www.tcll.ntnu.edu.tw/twnica/downloadfile.php?issue_id=27&locale=zh&paper_id=182) |

The NTNU table documents the shape term in “elliptical galaxy”; applying that
shape adjective to an ellipse drawing tool is an editorial choice. It avoids
certifying the former unsourced `tó îⁿ` reading.

The review also corrected misplaced POJ tone marks in the tray and translucent
preview text, residual Tâi-lô `tsia` and `tshuì` spellings, and caption synonyms
that differed between the button and its manual. Native progress, comparison,
quantity, recovery-purpose and “more” clauses were authored in both scripts.
It did **not** force every literary reading into a colloquial one: `nôa` for
欄, `san-tî` for 刪除, `liâu` as a slender-object classifier, and `tiông` for
repetition in 重設 have dictionary support and were retained.

Dictionary entries support particular reading decisions, not every newly
composed technical phrase. The pair review checks meaning and control names;
it does not certify one pronunciation as universal across Taiwanese varieties.

## Wu register evidence

Wu remains explicitly Shanghainese-based. The repaired prose uses complete
clauses with local topic/disposal constructions, result and potential
complements, time expressions and demonstratives. The “strikethrough” label
was restored as a technical noun; mechanically inserting the result marker
meaning “off” into that noun obscured its meaning.

The existing progressive **辣辣** was retained deliberately. Linguist Qian
Nairong's signed [primary explanation of its spelling and functions](https://wap.xinmin.cn/content/19434141.html)
distinguishes locative, progressive and persistent-state uses. It is not an
accidental doubled character and should not be removed by a generic cleanup.
The same author's [written-Wu orthography discussion](https://xmwb.xinmin.cn/lab/xmwb/html/2015-01/18/content_27_1.htm)
supports the established Shanghai forms; the latter was retrieved through the
search index because its page intermittently returned an error.

These sources inform the register and specific grammatical choices. They are
not presented as attestations of our newly written software instructions.

## Verification

- `test_translations.py`: all 27 tests passed after the final XML changes.
- `test_locale_font_coverage.py`: all 3 tests passed. The published Wu font
  subset already covers the revised catalogue; no font asset, inventory or
  licence hash changed.
- Shared localized-help assertions, restricted to these four catalogues:
  all 3 passed (active gallery routes, final copyright paragraph, known
  Show all corruption). The combined integration must run them globally.
- Actual quoted control captions were checked in active help, assembly help
  and the legacy manual, including saved-draft status and paired controls.
- AAPT2 35.0.0 compiled the complete `Paintroid/src/main/res` directory.

No merge or remote publication was performed from this worktree. Integration
and scoped original-PR publication belong to the parent task.
