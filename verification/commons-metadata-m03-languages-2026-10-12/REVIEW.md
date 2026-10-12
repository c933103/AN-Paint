# M03: independent review of Commons response-size translations

Key: `commons_metadata_response_too_large`
English: `Commons metadata exceeds the response limit`
Review date: 2026-10-12 UTC

## Decision

Accept the three exact strings below as source-assisted, contextual UI paraphrases, with moderate confidence. This is an actual independent linguistic review and a usable recommendation, not a claim of native-speaker approval. No mandatory human-review gate is asserted. The Ainu pair is one linguistic translation in two checked writing systems.

The recommendation is specific to the existing error path. These are not standardized translations of HTTP terminology and should not be reused indiscriminately for other errors. No source XML was edited and nothing was published by this reviewer.

## Independent checklist

Established before evaluating complete translator proposals:

1. Preserve literal `Commons`.
2. The data is descriptive information about the image, not the original image/file bytes, an upload, or the dimensions of the picture.
3. The problem is excess overall received-data size. Do not suggest a limit on a single text field, the number of metadata fields, or attribution length.
4. A received-information paraphrase can represent a response, but must keep its descriptive identity. Receipt wording must not imply that successful full download is required before the error can occur.
5. Any comparison must be between a quantity and its permitted/fixed amount. Avoid an independently unsupported finite verb built from an adverb/postposition.
6. Trace each modifier to its head; do not let “received from Commons” accidentally modify “image.”
7. Check language-specific script, segmentation and romanization independently. Orthographic agreement is not proof of idiomaticity.
8. Disclose any semantic compression and modern terminology extension rather than labeling them fully attested.

The implementation was read independently. In `CommonsAttribution.fetch`, `bytes.size().toLong() + count > MAX_RESPONSE` throws before that buffer is appended; MAX_RESPONSE is 2 × 1024 × 1024 bytes. Thus “received/being received” is a reasonable UI paraphrase, whereas “successfully downloaded metadata” would overstate completion. The separate field-size exception is not this key.

## ain-Latn

`Commons or wa a=uk tatum (noka oruspe) anak poro kaspa wa a=uk eaykap.`

Independent backtranslation: “The data being received from Commons (information/matters concerning the image) is too big, so it cannot be received.”

Parse: `[Commons or wa a=uk] tatum (noka oruspe)` is the topic NP; `anak` marks the topic; `poro kaspa` predicates excessive size; the final clause predicates inability to receive. The preceding location phrase is within the relative expression that modifies data, not within the image-information parenthesis.

Accepted because the parenthesis supplies descriptive identity while `tatum` preserves the data object. The whole topic is called too large; no word suggests an individual text field. The generic, non-past-specific Ainu receiving expression does not force completed receipt. This is a Saru-based grammatical frame with modern computing vocabulary, not a claim to a uniformly traditional technical register.

Exact semantic compression: “exceeds the response limit” is rendered functionally as “too large to receive.” The existence of a configured allowance, as distinct from a physical inability to receive, is contextual rather than lexically explicit. Neither bytes nor 2 MiB are added, consistent with their absence from the English string. This is acceptable for the checked error path, but not a full standalone specification of the limit.

## ain-Kana

`Commons オㇿ ワ アウㇰ タトゥㇺ (ノカ オルㇱペ) アナㇰ ポロ カㇱパ ワ アウㇰ エアイカㇷ゚.`

Same linguistic decision and backtranslation as ain-Latn. All thirteen space-delimited tokens align with the Latin proposal. `tu` is written トゥ under the museum's Saru-oriented convention, giving タトゥㇺ. The modern glossary's displayed タツ゚ㇺ is a different kana convention, not evidence that the Latin word must change. Final k, s, m and p are consistently represented with the expected small kana; the p representation is ㇷ plus combining handakuten. Morphological spelling is retained rather than forcing optional cross-word sandhi. NFC checks pass; no hidden controls occur.

### Ainu evidence and rejected alternatives

- [Tamura's Saru grammar, hosted by the National Ainu Museum](https://ainugo.nam.go.jp/pages/ainu_basic.html): pre-head modification, ordinary verb-final ordering, indefinite-person expressions, auxiliary `eaykap`, and possession support the parse. This validates constructions, not an attested technical sentence.
- [Museum dictionary, `suy` results](https://ainugo.nam.go.jp/dic?word=suy): the `kaspa` entry directly gives `poro kaspa` for excessive size. Its caution about restricted `kasu` use counsels against blindly retaining the older catalogue's `pakno kasu` chain.
- [Museum dictionary, `pe` results](https://ainugo.nam.go.jp/dic?word=pe): possessed `oruspe(he)` concerns a matter/story about its possessor. This independently supports the composition `noka oruspe` as descriptive information about the image; it is not claimed as a standardized metadata noun.
- [Museum dictionary, `Tan` results](https://ainugo.nam.go.jp/dic?word=Tan): `wa` sense 4 permits the causal reading between excessive size and inability.
- [Museum orthography guide](https://ainugo.nam.go.jp/pages/guide.html): supports the chosen tu and final-consonant kana spellings.
- [Itak-uoeroskip `tatum`](https://itak.aynu.org/tatum): directly publishes `tatum` as computing data. This is modern glossary evidence. It does not establish broad usage or a traditional term. Its attribution to Oota must not be misreported as Oota directly attesting this form: the translator checked Oota's draft and found `dáta`, which the glossary adapts/references. Retaining tatum avoids changing technical vocabulary and orthographic systems solely for perceived dictionary prestige.
- [Modern Ainu Dictionary](https://ss1.xrea.com/toracatman.s324.xrea.com/ainu/dictionary.html): explicitly labels `pororu` a coinage. It is not needed here.

The first translator draft omitted `(noka oruspe)`. I did not accept that version: “data from Commons” alone can include the image download. The parenthetical revision addresses that concrete objection without inventing a nested technical compound.

## mnc-Mong

`ᠨᡳᡵᡠᡤᠠᠨ ᡳ Commons ᠴᡳ ᠠᠯᡳᠮᡝ ᡤᠠᡳᡥᠠ ᠮᡝᠵᡳᡤᡝ ᡳ ᡠᡥᡝᡵᡳ ᡴᡝᠮᡠᠨ ᡨᠣᡴᡨᠣᡥᠣ ᡴᡝᠮᡠᠨ ᠴᡳ ᡶᡠᠯᡠ.`

Romanization: `nirugan i Commons ci alime gaiha mejige i uheri kemun toktoho kemun ci fulu.`

Independent backtranslation: “The total amount of the image-information received from Commons is more than the fixed amount.” In this error context: “The total size of the image's metadata received from Commons exceeds the set limit.”

Parse: `[[nirugan i] [Commons ci alime gaiha] mejige] i [uheri kemun]` is the subject; `[toktoho kemun] ci fulu` is the comparative predicate. The first `ci` marks the source; the second marks the comparator. `uheri` makes the aggregate quantity explicit. The comparison is to a fixed allowance; it does not say the image is too wide/high or that its descriptive text has too many characters.

I revised the translator's initial order `Commons ci alime gaiha nirugan i mejige ...`, which risked putting the received modifier on the image. Moving `nirugan i` before the received modifier brings the latter immediately before `mejige` and makes the intended analysis cleaner. This is a grammatical inference from established modifier ordering, not an attested complete sentence.

Residual semantic extension: `mejige` is ordinary information/news extended to digital descriptive information; `kemun` is measure/amount extended to data volume. The unit “bytes” and a standardized network-response noun remain implicit. The configured response allowance is conveyed by fixed amount within this receiving-data context. `alime gaiha` characterizes information already arriving/received without asserting successful full completion of the stream. Moderate confidence is warranted; natural contemporary technical usage is less well evidenced than the grammar.

### Manchu evidence

- [Möllendorff, A Manchu Grammar, 1892](https://en.wikisource.org/wiki/A_Manchu_Grammar): genitives and participles precede their head; `ci` supports both source and comparison; `gaimbi` has the participial form `gaiha`. These support the revised parse and comparison, not native approval of the full string.
- [Kuribayashi's index to the Qing triglot dictionary](https://gerel.net/articles/roncho/A47All.pdf): PDF pp. 180, 324, 365, 398, 508, 527 respectively support fulu, kemun, mejige, nirugan, toktoho/toktombi and uheri. The dictionary is historical, not a source for HTTP vocabulary.
- [Watanabe's edition of a Manchu arithmetic manuscript](https://www.sciamvs.org/files/SCIAMVS_06_177-264_Watanabe.pdf): actual primary-text `ton ci fulu` comparison, `toktoho ton`, and `uheri` establish quantitative/fixed/total uses. See PDF pp. 5–7 and 82.
- [Elliott's constructions handout](https://www.manchustudiesgroup.org/wp-content/uploads/2020/07/Handout-8-Constructions-with-ci.pdf): a historical monetary-amount example independently illustrates comparative `ci ... fulu`.
- [Saksaha 19 primary memorial edition, p. 94](https://journals.publishing.umich.edu/saksaha/article/id/4215/download/pdf/): indexed primary text and translation pair `ukanju i mejige` with information about fugitives. I verified the indexed passage; direct PDF opening returned a site access error. It supports “information about X,” not specifically image metadata.
- [Onuma, Documents from Kazakh Sultans to the Qing Dynasty, p. 25](https://www.battle-of-qurman.com.cn/literature/Onuma-2010.pdf): primary text and translation give `alime gaiha` modifying the received diploma.
- [Manchu Studies Group, Muwa Gisun, section three](https://www.manchustudiesgroup.org/translations/muwa-gisun/muwa-gisun-section-three/): discourse 11 directly supplies a bare `ci fulu` predicate without an expressed copula, independently checked after reading the translator’s final evidence.
- [Unicode Mongolian code chart](https://www.unicode.org/charts/PDF/U1800.pdf): character identity reference. The Manchu letters decode exactly to the romanization above; no Mongolian e/i/u/r substitutes or hidden controls occur. This mechanical check is separate from a device-font rendering test, which was not performed.

I did not accept a finite `dabaliha` formed by extending the catalogue's wording. Attested comparative grammar removes that avoidable morphological uncertainty.

## Scope of acceptance

All three recommendations preserve the user-facing error's essentials through supported compositional paraphrase. They are suitable candidates for the parent to integrate, with the exact limitations recorded above. This does not certify fluent native style, every possible dialect, broad technical terminology standardization, or Android font layout. `script-check.json` records the mechanical verification separately.

Final-artifact verification: both translator JSON proposals were parsed and exact-string matched to this review. See `translator-artifact-match.json` for the hashes at review time.

Provenance reconciliation (2026-10-12 01:02 UTC): the Manchu translator recorded completed acceptance in the proposal’s `status` and `independent_review` fields after the initial receipt. Restoring only those two metadata fields exactly reproduces initial SHA-256 `33d893ff410a861fc23654bcebb97861364d9f1314bcf0b3d42f854f02892cf1`. The current SHA-256 is `9f0acf4ffb6662671d740f5b1014cd0d27727b7bc7b0ee296519b90572fecd7a`. Translation, romanization, rationale, sources, and every other field are unchanged. The receipt now pins the current file and retains the earlier hash and exact verification method. No new translation review or source edit was needed.
