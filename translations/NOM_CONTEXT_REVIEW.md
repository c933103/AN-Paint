# Vietnamese Chữ Nôm contextual review, 2026-09-25

This review resumes the Korean/Vietnamese branch's unfinished script review. It
compares all 669 string entries and the plural against the Vietnamese catalogue,
then checks the app sense of repeated words in controls, notices, errors, and the
three manuals. Nôm is written Vietnamese: Vietnamese word order, function words,
and technical/product names remain Vietnamese. Chinese meanings alone are not a
valid way to judge a Nôm spelling.

The previous catalogue repeatedly selected an unrelated homophone. Examples are
`徑` in a magnifying lens (now `鏡`, while radius retains `徑`), `療` in data
(now `料`), the year `𢆥` for five star points (now `𠄼`), and the falcon `𪁄`
for cutting (now `割`). Arrow `箭` and filename `𠸜` are kept distinct, as are
instrumental `憑` and equality `平`, inside `𥪝` and transparent `沖`, copying
`抄` and a star `𣇟`, colour `色` and sharpness `銫`, and a word `詞` versus
from `自`. These changes were applied throughout the catalogue, not only to the
short tool labels.

`NOM_CONTEXT_REVIEW.tsv` records the reviewed forms and their app contexts. The
counts describe the first repair pass; `contextual` rows describe subsequent
whole-phrase decisions. This is a review ledger, not a transliteration dictionary
or a generator. XML remains canonical. Modern combinations such as undo,
estimated memory, decoder buffers, and tolerance are editorial technical
compositions using the attested constituent senses; the ledger does not claim
that the complete AN Paint sentences occur in a historical corpus.

## Evidence and orthographic scope

The primary lexical evidence is the RCV project's *Công Cụ Tra Cứu Chữ Hán Nôm
Chuẩn*, published by Uỷ Ban Phục Sinh Hán Nôm Việt Nam:

- https://hannom-rcv.org/Lookup-CHNC.html
- https://www.hannom-rcv.org/NS/bchnctd%20300623.pdf
- https://html.cafe/xdca90f3a — accessible reproduction of the publisher's lookup,
  consulted 2026-09-25; the publisher site returned HTTP 403 to direct retrieval.

Lookup entries include kích (dimensions), kính (lens versus radius), dùng (use
versus broth), mẫu (sample), vùng (area), và (conjunction), ghi (record), cắt
(cut versus falcon), tên (name versus arrow), năm (five versus year), hồ sơ,
kiểm soát, tọa độ, phục hồi, kim/đồng hồ, and the contextual distinctions above.
The app-specific compounds use these entries; copied dictionary example
sentences and definitions are not included here.

A second reference is the frequency-based spelling proposal and word list from
chunom.org, which draws on Nôm texts:

- https://chunom.org/pages/standard/
- https://chunom.org/pages/standard-list/?max=2000&download=1
- Download SHA-256 on 2026-09-25:
  `3e707c05180c198e8abc78cdcbede6b6c71485a52eeca8e221eb22c4df119b01`

Both are spelling proposals, not an official universal Nôm standard. Attested
variants and phonetic loans must not be confused with semantic errors. For
example, `劍` is explicitly listed as a variant of native *kiếm* (search), so the
choice of `檢` is an orthographic preference, not proof that every prior search
label meant sword. `紙法` (giấy phép), `通信` (thông tin), `互助` (hỗ trợ),
`風` (phông), `扔` (nhưng), and `吻` (vẫn) are retained. The brush uses the
transparent Vietnamese synonym *bút lông* (`筆𣯡`), airbrush *bút phun* (`筆噴`),
and sticker *hình dán* (`形𥻂`); these are editorial descriptions rather than
claims that an unverified dictionary homophone names those tools.

This is a source-assisted semantic and consistency review, not certification by
an independent native Nôm reader. The references support lexical choices; they
do not establish community-wide preferences for every modern software term.

## Controls, manuals, and glyph coverage

The old generic Android submenu description has been replaced with the five
actual tabs. Manuals now direct image insertion through Draw → Insert → Other
images, show Assembly under File, quote the complete About caption for legal
notices/source, and distinguish Show all from changing the output dimensions.
The current short help quotes the actual swap-colour, fit-image, source-picker,
and About labels. The three live gallery help routes retain the CI review fix.

The font preview now samples Nôm rather than Japanese kana. Rebuild the renamed
font with `tools/build_nom_ui_font.py` and its existing pinned Nom Na Tong/Gothic
Nguyen inputs. `fonts/inventory.json` records the regenerated asset hash; source
licenses and modification notices remain unchanged. The coverage test checks
all actual catalogue ideographs, including newly introduced supplementary ones.
