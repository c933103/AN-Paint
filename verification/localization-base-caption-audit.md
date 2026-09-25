# Shared base and Cantonese review — 25 September 2026

The #2 handoff's script/coverage checks did not establish correct pronunciation
or current editor instructions. The resumed pass repairs Japanese, Hong Kong,
Taiwan and Mainland Chinese, plus both Cantonese catalogues directly in XML.

## Instruction and caption repairs

- The assembly button is Show all, not Show all changes. It changes viewport
  zoom, never output dimensions. Japanese had mistranslated this in both manuals.
- Quoted controls now follow their actual resource captions, including Open,
  Export as, Fit, Swap colours, Other images, Original size and Image assembly.
  Cantonese Draw and Drawing are distinct captions and remain distinct.
- Obsolete generic Menu/Android-submenu instructions are removed while the
  preceding bounded-panel, remembered-choice and landscape instructions remain.
- Image assembly opens from File. Inserted images use Draw → Insert → Other
  images, with device files, Catrobat, Irasutoya and Openclipart. Source-specific
  insertion instructions and retained credits are preserved.
- Both the active paste hint and the older equivalent resource name the current
  insertion route. Draw again remains a real control; it was not replaced merely
  because its wording differs from Draw.

## Contextual Jyutping decisions

Eighty-one resources received pronunciation corrections in the resumed reading
pass, in addition to caption alignment. These are inspected word/sentence
contexts, not the output of a character-first transliteration pipeline.

| Context | Repair / distinction | Primary dictionary evidence |
| --- | --- | --- |
| 調整 / adjustable | `tiu4`, not the transfer/assignment reading `diu6` | [Words.hk 調整](https://words.hk/zidin/調整) |
| 處理 | `cyu2 lei5`; keep source/place 處 as `cyu3` | [CUHK 處](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=處), distinct homophone groups and example compounds |
| Row / line versus action | `hong4` for row/newline; `hang4` for 另行/可行; not walking `haang4` | [Cantonese Dictionary 行](https://cantowords.com/dictionary/行) |
| Integer, pixel count, redirect count | Noun 數 `sou3`, not counting verb `sou2` | [Words.hk 數](https://words.hk/zidin/數) |
| File header, text file, colour profile | 檔 `dong2` | [Words.hk 檔案](https://words.hk/zidin/檔案) |
| This/these | Demonstrative 呢 `ni1`; `ne1` is a different particle. Attested `nei1` is not declared invalid. | [Cantonese Dictionary 呢](https://cantowords.com/dictionary/呢) |
| Amount / vector | 量 `loeng6`; the inspected entries are nouns, not the measuring verb | [CUHK loeng6 group](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/pho-rel.php?s1=l&s3=6) |
| Conversion | 轉換 / converted to uses `zyun2`; rotation retains `zyun3` | [CUHK 轉](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=轉) |
| Above, upper limit, previous | `soeng6` in positional/prior contexts; preserve 貼上 and 噴上 `soeng5` | [Cantonese Dictionary 上](https://cantowords.com/dictionary/上) |
| Move/drag/save to a destination | 到 `dou3`; unsuccessful/ability expressions retain `m4 dou2` | [Cantonese Dictionary 到](https://cantowords.com/dictionary/到) |
| For every edge / for all inputs | Benefactive 為 `wai6`; 作為/設為/儲存為 remain `wai4` | Contextual grammatical distinction; no global replacement of the character |

Italic 斜體 is corrected to `ce4 tai2` (CantoDict compound evidence). Accepted
variants such as 距 `geoi6` and the alternate readings of 桿 are not rejected just
because another reading is more common. The paired Fit image to canvas caption
now uses the same 範圍 wording, and New image/Open/Export labels are consistent
with their Han counterparts.

The comparison checks operational meaning and selected ambiguous readings. It
does not claim a fresh independent native-speaker certification of all prose,
nor does a syllable-count or script test establish correct tone choice. No
dictionary definitions or example sentences are copied into application text.

Validation: 27 host translation tests pass after these edits. Final combined
font/resource/host checks and exact-head Android results are recorded in the
integration review, separately from this linguistic evidence.
