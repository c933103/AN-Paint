# Draft candidates: Chamorro, Zhuang and Standard Moroccan Tamazight

These are **unapproved draft hypotheses**, not production resources or linguistic certification. Do not merge this evidence branch into an application branch. Candidate presence does not count toward completed translation coverage.

Pinned AN Paint source: `428f9f2a203116c4d11a279ea2c1cfb3093059c0`.

- Chamorro: 184 authored; 10 explicitly rejected, 3 revised but still awaiting re-review, and 4 short labels received bounded primary-source lexical review. Other retained prose remains linguistically unapproved.
- Zhuang: 33 provisional candidates, no independent linguistic approval.
- Standard Moroccan Tamazight: 40 provisional candidates, no independent linguistic approval. This is zgh, not Kabyle or a claim to cover all Amazigh varieties.
- Total: 257 authored; 247 retained candidates and 10 rejected candidates. This does not complete the 875 missing P2/P3 entries across these three catalogues.

## Evidence and limits

`checks.json` records key existence, absence from pinned target, matching placeholder multisets and literal newline counts. These structural properties do not validate meaning or fluency. Candidate JSON contains raw prose, not Android-escaped XML.

`ch-accepted.patch` contains only four short proposed canonical labels: quality, top, tool option and wheel. It is for accumulation into a larger reviewed integration batch, not a separate micro-PR. Six translation-boundary tests and 34 translation tests passed locally against this patch. Android compilation, runtime layout, exact-head Codex review and hosted CI have not run for this patch. They remain required as applicable for the integrated batch.

The independent Chamorro review explicitly rejected mistranslations of light as afraid, handles as dream, fits as near, non-empty as not coming, and query failure as not thinking; an unsupported wasp-box honeycomb metaphor; and restricting horizontal to left-to-right. The rejected values and reasons are retained in `ch.json` so they cannot silently be revived. `pinsét` was revised to attested `pensét`, and dimension joining changed to `×`; those complete revised strings are not thereby accepted.

## Terminology sources

- Kumisión i Fino’ CHamoru specialized-list index: https://kumisionchamoru.guam.gov/listan-palabra-word-lists/listan-espesi%C7%BBt-specialized-lists/
- Official 2026 Technology Terms: https://drive.google.com/file/d/1HXKyTmacblJDYmIfo_YrcpiwK5zyoT8V/view
- Official legal list (does not supply the needed copyright/licence/attribution equivalents): https://drive.google.com/file/d/1l87vuLLSr-NtM5rkdzt9SzP80FAaS6H_/view
- Guam 2024 orthography: https://kumisionchamoru.guam.gov/wp-content/uploads/2025/02/Utugrafihan-CHamoru-GuA%C2%A5han-3rd-Ed-2024_KumisiA%C2%B3n-i-Fino-CHamoru_Digital.pdf
- Revised Chamorro-English dictionary: https://natibunmarianas.org/i/ and https://natibunmarianas.org/r/ ; its CNMI orthography must not silently be treated as Guam orthography.
- MediaWiki terminology reference for za and zgh, pinned revision `377002822b34077904f4e83c21faaf69d1bfea9a`: https://github.com/wikimedia/mediawiki/tree/377002822b34077904f4e83c21faaf69d1bfea9a/languages/i18n . This source is GPL-2.0-or-later; project/contributor notices are preserved in the reference files. It provides terminology evidence, not approval for whole newly composed phrases. Check attribution and applicable existing source notices before integrating derived wording.
- IRCAM primary lexicon portal located, not used to assert that these whole phrases have been verified: https://tal.ircam.ma/dglai/index.php

## Next work

Review the remaining candidates independently against actual UI call sites and reliable language evidence, correcting or rejecting rather than approving wholesale. Continue the remaining complete source catalogue, including technical/legal and full help bodies. Keep uncertain prose here; integrate adequately checked values only in a larger combined batch. Exact-head Codex and CI gates remain unchanged.
