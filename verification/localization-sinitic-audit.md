# Sinitic catalogue audit

This audit covers the complete 670-entry catalogues for Literary Chinese
(`lzh-Hant`), Taiwan Hakka in Han and Latin script (`hak-Hant-TW`,
`hak-Latn-TW`), Taiwanese in Han and Latin script (`nan-Hant-TW`,
`nan-Latn-TW`), and Shanghainese Wu (`wuu-Hans`). The comparison baseline is
integration commit `28ed84f65`. Japanese, Mandarin and Cantonese are reviewed
separately in the integration work.

The earlier audit claimed every entry and both script pairs had been reviewed.
The recovered branch handoff and a fresh comparison disproved that completion
claim: the Sixian pronunciation audit and Han/Latin manual alignment still had
unfinished work. The September 25 follow-up below records concrete source checks
and repairs; resource coverage is not evidence of linguistic completion.

## Repairs

- Rename the Taiwan Hakka resource qualifiers to include `TW`. Locale menu
  metadata and preference migration are handled with the layout integration.
- Repair changes that had replaced characters inside unrelated words:
  saturation/softness compounds, Hakka 主要/內容/目的地, Taiwanese 內容/內置,
  and Wu 現在. A language particle is not a safe global replacement for a
  Mandarin character.
- Expand the abbreviated Literary Chinese help to retain the original
  features and instructions, and distinguish image assembly from foreground
  colour. Rewrite the main and assembly help in Hakka and Taiwanese using
  their own sentence constructions; repair the corresponding Latin text.
- Preserve whether an operation restores a draft, undoes an edit, moves a
  placed image back to the tray, changes only view zoom, or changes output
  dimensions. Restore descendant attachment restrictions and source-memory
  explanations.
- Repair context-dependent readings in the Latin catalogues. Examples include
  Hakka modal 會 versus the readings in lexical 會/匯, and Taiwanese 旋 in
  rotation versus a hair whorl, 行 in line spacing versus walking, and 重 in
  reset versus weight. Repair malformed search, file-picker, metadata and
  PDF messages.
- Keep technical names and copyable examples intact, including
  `data:image/png;base64,`, `CC BY-SA 4.0`, `65,535`, `canvas.png`, hexadecimal
  colours and `Ctrl+A`. Restore the whole Catrobat licensing requirement,
  including attribution and sharing adaptations under the same licence.

## Language evidence

The following primary references informed specific choices. They do not
constitute verification of the whole catalogue.

- Taiwan Ministry of Education, Hakka dictionary:
  [抑係](https://hakkadict.moe.edu.tw/search_result/?accent=1&id=250),
  [毋罅](https://hakkadict.moe.edu.tw/search_result/?accent=1&id=11924),
  [會](https://hakkadict.moe.edu.tw/search_result/?accent=1&id=16036), and
  [系統](https://hakkadict.moe.edu.tw/search_result/?accent=1&id=12651).
  The earlier text incorrectly said Sixian `ne-thúng` was retained: the XML
  still contained `he-thúng`. The September 25 repair applies `ne-thúng`
  to all three occurrences, following the Sixian dictionary entry. For 會, modal `voi` is distinguished
  from lexical `fi`. Han/Latin Hakka remains Taiwan-oriented; this audit does
  not introduce a Mainland Hakka pronunciation convention.
- Taiwan Ministry of Education, Taiwanese dictionary:
  [保存](https://sutian.moe.edu.tw/zh-hant/su/4716/),
  [搜揣](https://sutian.moe.edu.tw/zh-hant/su/27308/),
  [貼](https://sutian.moe.edu.tw/und-hani/su/9041/),
  [等](https://sutian.moe.edu.tw/zh-hant/su/8817/), and
  [旋](https://sutian.moe.edu.tw/zh-hant/tshiau/?lui=tai_su&tsha=%E6%97%8B).
  Dictionary Tai-lo spellings are represented in the catalogue's existing
  Peh-oe-ji convention, rather than mixed into it. For example, 保存 is
  `pó-tsûn` in Tai-lo and `pó-chûn` in Peh-oe-ji; 搜揣 is represented as
  `chhiau-chhōe`. The 保存 labels and their help references were aligned in
  both scripts.
- [The Surprise Factor: A Semantic Theory of Mirativity](https://ecommons.cornell.edu/bitstreams/3b49c84a-dd5b-459f-95fa-f1a388cb2285/download),
  section 4.3.2, documents Shanghainese `𠲎` as a polar-question particle and
  `辣辣` as a progressive form. Those are intentional Wu forms, not corrupt
  characters or repeated text. The supplementary character `𠲎` remains in
  the save question and needs font coverage.

## Verification and limits

All six catalogues pass `validate_catalogue(tag, require_complete=True)`:
complete key coverage, valid XML and matching Android format placeholders.
`git diff --check` also passes. An additional comparison against English
finds no missing occurrences of the format names, colour-model names,
licence identifier, numeric GIF limit, data URI prefix, recovery filename,
keyboard shortcut or hexadecimal examples listed above.

These checks establish resource integrity and preserve technical semantics;
they cannot establish native fluency or settle every regional spelling and
romanization preference. Hakka, Taiwanese and Wu still benefit from review
by speakers of the stated varieties, especially the long technical manuals.
No generated transliteration script or dictionary definition is shipped as
part of these changes. Combined Android builds and application behaviour are
verified in the integration branch.

## Reopened Sixian handoff — September 25, 2026

The original branch promised a Sixian dictionary check, manual treatment of
dictionary gaps, and comparison of the Han and Pha̍k-fa-sṳ catalogues. That was
not established by the earlier key-count audit. The official [Sixian ODS](https://hakkadict.moe.edu.tw/static/resource/客語資源下載/本辭典的文字/四縣腔詞條詞目文字.ods)
was retrieved again: 18,370 entries; SHA-256
`a19d2e07fd5213f26bc2d4db9be0301418208d207c8e74f4df01278940ac0380`.
The following IDs are the ODS **序號** column, not website search-result IDs.
Definitions and example sentences are not redistributed.

| Word/context | ODS ID | Sixian reading | Catalogue decision |
| --- | --- | --- | --- |
| 系統 | 11600 | ne55 tung31 | `ne-thúng`, replacing `he-thúng` |
| 保存 | 5403 | bo31 sun11 | `pó-sùn`, replacing `pó-chhùn` throughout |
| 記憶 in memory warnings | 7698 | gi55 id2 | `ki-yit`, restoring the final stop |
| 說明 | 4314 | sod2 min11 | `sot-mìn`, replacing the unrelated 明 reading |
| 刪忒 | 18064 | xien24 ted2 | `siên-thet`, including Remove and help references |
| 比 in ratios | 5282; 比例 951 | bi31; bi31 li55 | `pí`, not side-by-side `pè` (ID 5231) |
| 好 in OK/completion | 8933 | ho31 | `hó`; `hau55` (ID 8623) means liking |
| 行 in line spacing | 9033 | hong11 | `hòng`, not walking `hàng` (ID 8587) |
| 你 | 11522, 11628, 12078, 16115 | n11, ng11, ni11, ngi11 | Keep attested `ǹ`; do not force one regional variant |
| 存 by itself | 6280, 13900 | cun11, sun11 | Keep attested independent `chhùn`; compound 保存 uses `sun11` |

The historical 51-decision scratch audit was lost before publication; this is a
newly reconstructed decision record, not a claim that that file was recovered.
The following source commits complete the recovered pair/manual review; the
sections below state its evidence and limits.

### Pair and manual follow-up

The 670 Han/Latin resources were compared in source order, including the plural
item, both large help texts, import/export, recovery, selection, rendering,
licensing and colour messages. This comparison is a semantic/reading audit, not
a dictionary-derived translation pipeline or a native-speaker certification.
The handoff's missing remembered-choice clause now says that the user's panel
choice is remembered in both scripts. The legacy manual now names the actual
ribbon tabs, Draw → Insert → Other images, File → Image assembly, and File →
About/licences/credits; the old standalone Help panel description was removed.
The current Show all and Edit in Paint captions are used in the manual.

Additional contextual reading decisions from the same ODS:

| Word/context | ODS ID | Sixian reading | Decision |
| --- | --- | --- | --- |
| 像 in images/pixels | 15179 | xiong55 | `siong`; `qiong55` (12871) is the verb “resemble” |
| 具 in 工具 | 9896 | ki55 | `khi`; keep aspiration and correct the tone (ODS `k` is aspirated) |
| 清 in clearing | 12783 | qin24 | `chhîn`; `qiang24` (12689) has another context |
| 靜 in still images | 12839 | qin55 | `chhin`, consistently in codecs and import labels |
| 明 in light/dark | 11236 | min11 | `mìn`, not the next/following-day reading |
| 較 before dimensions | 9806 | ka55 | `kha`, not the verb reading `gau31` (7604) |
| 頭 | 14115 | teu11 | `thèu`, normalize the misplaced eu tone mark |
| 後 (time) | 8657 | heu24 | `hêu`; the separate spatial reading is `heu55` (8674) |
| 標 | 5246; 12327 | beu24; peu24 | `pêu` / `phêu`, retain attested variants |
| 搜 | 13261 | seu24 | `sêu`, normalize eu tone placement |
| 少 (quantity) | 13288 | seu31 | `séu`, normalize eu tone placement |
| 行 (rows/line breaks) | 9033 | hong11 | `hòng`; do not change 行 in executable/feasible compounds |
| 抑係 | 249 | ia55 he55 | Keep `ia-he` as the alternative conjunction |
| 會 (modal) | 14771 | voi55 | Keep `voi`; do not replace with lexical `fi` |
| 匯 | 7128 | fi55 | Keep `fi` in import/export compounds |
| 自家 | 1767 | cii55 ga24 / qid5 ga24 | Keep both attested formal/colloquial forms |
| 揀取 | 7866; 12636 | gien31 qi31 | Keep `kién chhí` |
| 毋罅 | 10904 | m11 la55 | Keep `m̀ la` for insufficient memory |
| 脣項 | 13909 | sun11 hong55 | Keep `sùn-hong`; it is a Hakka side/edge expression |
| 這下 | MOE appendix | ia31 ha55 | Keep `yá-ha` for the current state |

For completed-state messages, the [MOE function-word appendix](https://hakkadict.moe.edu.tw/appendix/)
specifically assigns 誒 `e11` to Sixian and 咧 `le53` to Hailu (Dabu has
`le33`). Some official learning pages also display 咧 in examples, so its mere
appearance was not treated as proof of Mandarin copying. The five completion
messages were aligned explicitly as 誒 / `è` for this Sixian catalogue. No
unrelated character occurrence was replaced. The [Hakka Affairs Council PFS
literature study](https://www.hakka.gov.tw/File/Attach/46366/File_97551.pdf),
pp. 8–9, provides contemporary Taiwanese spellings such as `thèu` and `chhêu`;
eu tone marks were normalized without changing the underlying tone category.

### Final dictionary-gap pass

The ODS does not contain every modern software compound. For those gaps, the
existing Hakka wording was compared with each constituent's contextual sense;
a first-match Han character converter was not used. Additional explicit choices:

| Context | ODS ID | Source reading | Decision |
| --- | --- | --- | --- |
| 析 in resolution 解析度 | 15010 | xid2 | `sit`, replacing the slice/side sense `sak` (12966) |
| 支 in software support 支援 | 15441 | zii24 | Literary `chṳ̂`; classifier `gi24` (7636) is not this sense |
| 援 in 支援 | 9296 (also 9274) | ien11 (also ien24) | `yèn`, consistently; this is a compound not directly listed in the ODS |
| 兩 in two fingers/corners | 10616 | liong31 | `lióng`; weight unit `liong24` (10600) is not the UI sense |
| 清楚 in attribution edits | 3318 | qin24 cu31 | `chhîn-chhú`, matching the existing general clear/sharp wording |
| 取消 | 2051 | qi31 seu24 | `chhí-sêu`, the same spelling in button and quoted help |
| 完整 | 1884 | van11 ziin31 | Retain `vàn-chṳ́n` in preservation/recovery messages |
| 聲明 | 13120 | sang24 min11 | Retain `sâng-mìn` in notices |
| 形狀 | 8842 | hin11 cong55 | Retain `hìn-chhong`; not Mandarin-tone transliteration |
| 這下 | 3403 | ia31 ha55 (also lia31 ha55) | Retain `yá-ha`, supported by the complete word entry |

The correction to 具 explicitly keeps aspiration: MOE `ki55` corresponds to PFS
`khi`, whereas MOE `gi55` would correspond to `ki`. An intermediate follow-up
commit incorrectly removed the aspiration; this pass fixes that error and the
explanation. The corpus/constituent source decisions above remain editorial
choices for software senses and must not be presented as dictionary quotations
of whole translated sentences.

### Count words and warning syntax

The remaining homophone pass found the image classifier 張 had taken the
“threaten/make difficulties” reading (ODS 6663, `diong24`). Image counts now use
`chông` from the flat-object classifier (15729, `zong24`), including assembly
counts and both manuals. Amount 量 uses `liong55` (10635), and numeric 數 uses
`su55` (13825), instead of the unrelated/overgeneralized readings.

The paired dimension/PDF warnings were also rewritten as Hakka clauses: native
`m̀-hó` restrictions (毋好, 10903), `m̀ la` insufficiency (毋罅, 10904), and
`ia-he` alternatives (抑係, 249). The required positive sizes, nonempty PDF,
512 MiB maximum, nonzero rectangular crop, Android coordinate range, and
integer-pixel/percentage choices were checked against English after rewriting.
These changes address sentence structure as well as pronunciation. Shared
technical nouns remain where they express the intended software concept.

All Hakka changes are stored directly in the two Android XML catalogues. No
translation generator or runtime dictionary dependency was introduced.
