# Sinitic catalogue audit

This audit covers the complete 670-entry catalogues for Literary Chinese
(`lzh-Hant`), Taiwan Hakka in Han and Latin script (`hak-Hant-TW`,
`hak-Latn-TW`), Taiwanese in Han and Latin script (`nan-Hant-TW`,
`nan-Latn-TW`), and Shanghainese Wu (`wuu-Hans`). The comparison baseline is
integration commit `28ed84f65`. Japanese, Mandarin and Cantonese are reviewed
separately in the integration work.

Every catalogue entry was read, including the general help, full tool manual,
assembly instructions, licensing, attribution, import/export and recovery
messages. The two writing systems of each Taiwan language were compared for
meaning. This is an editorial and technical review, not independent native
speaker certification of every sentence or pronunciation.

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
  The Sixian reading of 系統 is retained as `ne-thúng`; it must not be
  changed to a Mandarin-influenced guess. For 會, modal `voi` is distinguished
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
