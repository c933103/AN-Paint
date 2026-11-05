# Zhuang numeric-entry instructions

Base: `2b208ee27eaaf2202f01aca5ef544c85779f8ddb` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 resources: a number-range error, a whole-number range instruction and the numeric button's type-a-number accessibility description. All 159 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent language and consumer review retained the number/whole-number distinction and added explicit singular `ndeu` after the classifier–noun groups. This makes one number explicit; the shorter draft was not established as ungrammatical. The lexical entries for [soq](https://en.wiktionary.org/wiki/soq#Zhuang), [cingjsoq](https://en.wiktionary.org/wiki/cingjsoq) and [aen](https://en.wiktionary.org/wiki/aen#Zhuang) support number, integer and the general classifier with a following singular marker. The [1984 dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) corroborates integer; `cingjsoq` must not be confused with positive-number `cingqsoq`.

The entries for [daj](https://en.wiktionary.org/wiki/daj#Zhuang) and [daengz](https://en.wiktionary.org/wiki/daengz) support from/to, including paired usage. The composition keeps the source's lower-bound then upper-bound order and introduces no exclusive comparison.

Search-indexed primary text of the [23 October 2024 newspaper PDF](https://www.guangximinzubao.cn/szbzw/page/21/2024-10/23/03/2024102303_pdf.pdf) pairs `diemj ok` with clicking/opening network settings in parallel Zhuang/Chinese prose. Direct PDF retrieval failed; bytes and visual alignment were not independently checked. Applying the activation verb to this tappable entry button is an editorial extension from digital click/open usage. Independent review accepted that evidence with the retrieval limitation, rather than substituting a physical-button press verb.

The composed instructions have medium confidence. Complete UI sentences, device-specific gesture idiomaticity and screen-reader delivery are not independently attested or tested. Native-speaker certification is not claimed.

## Consumer and targeted checks

- All three keys are consumed only by `NumericSlider.kt`. Its `contentDescription` formats the arbitrary setting name then current integer value; it does not replace the button's separate visible value text.
- The entry dialog formats minimum then maximum in the whole-number instruction. The error uses the same ordered limits when `toIntOrNull()` fails or the value is outside inclusive `minimum..maximum`. Updating the slider and dismissing occur only in the valid branch.
- These are integer controls, not decimal-entry consumers. The generic-number error remains distinct from the explicitly whole-number instruction, as in English. No accepted range or parser behavior changes.
- 62 host tests pass: translations, translation boundaries, priority accounting, current localization contracts and numeric-entry source coverage. All 171 offered catalogues and the priority manifest pass structural validation.
- Sixteen English/Zhuang Java render checks pass: distinct lower/upper values, a negative bound, equal zero bounds, and accessibility labels containing percent, XML-sensitive characters, quotes, a newline and placeholder-like text. These test substitution, not actual UI input acceptance.
- Missing-only integration preserves attributes, typed/ordered placeholders, newlines, escaping, earlier values and XML prefix bytes. Temporary Kotlin checks verify the actual bindings and inclusive integer guard; they do not execute Android input or screen readers.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 251 other non-tree entries are retained. Publication uses an expected parent and non-force branch lease, with full-tree and changed-file verification.

Zhuang direct presence becomes 162 resources: P0 68/94, P1 94/249, P2 0/305 and P3 0/71. Global P1 gaps become 1,397; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed numeric-entry operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
