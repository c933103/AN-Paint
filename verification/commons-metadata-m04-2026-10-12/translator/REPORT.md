# AN Paint M04: Commons metadata query failed

Prepared 59 explicit proposals for `commons_metadata_query_failed`: 36 high, 15 medium and 8 low model-confidence proposals. These are proposals, not linguistic acceptance or native-speaker certification. No production or GitHub changes were made.

## Meaning and scope

The branch is `JSONObject.has("error")`, including an error member whose value is null, false or an empty object. Each proposal expresses failure of the Commons metadata query/request. No HTTP, network, missing-data, response-size or image-download cause is added. The exact English default is preserved. All 59 exact tags are matched against the provided M03 test scope.

## Deliverables

- `proposals.json`: exact values, backtranslations, rationale, confidence, review limits, readings and linked source registry for every tag.
- `values.json`: extraction convenience only; it is not a production catalogue.
- `font-coverage.json`: exact bundled-font character checks with hashes.

## Material unresolved language questions

- `ain-Kana`: Commons オㇿ タ ノカ オルㇱペ アコピシ エアイカㇷ゚. — Unresolved: whether kopisi with the stated locative/topic arguments is the best construction for a machine query.
- `ain-Latn`: Commons or ta noka oruspe a=kopisi eaykap. — Unresolved: query argument structure and whether noka oruspe adequately denotes metadata.
- `mnc-Mong`: Commons ᠴᡳ ᠨᡳᡵᡠᡤᠠᠨ ᡳ ᠮᡝᠵᡳᡤᡝ ᠪᡝ ᡶᠣᠨᠵᡳᠮᡝ ᠮᡠᡨᡝᡥᡝᡴᡡ. — Unresolved: natural Manchu syntax for an API inquiry and the source relation with ci.
- `bo`: Commons ཀྱི་མེ་ཊ་གནས་ཚུལ་འདྲི་ཞིབ་བྱེད་པ་ལམ་ལྷོངས་མ་བྱུང་། — Unresolved: standard Tibetan computing terminology for metadata and query.
- `dz`: Commons གི་མེ་ཊ་གནས་སྡུད་འདྲི་དཔྱད་འབད་མ་ཚུགས། — Unresolved: appropriate Dzongkha term for metadata and computing-query noun.
- `ko-KP`: Commons 메타자료 조회에 실패하였습니다. — Unresolved: North Korean computing preference for 메타자료 and 조회 was not independently corroborated in this pass.
- `mn-Mong`: Commons ᠤᠨ ᠮᠧᠲ᠋ᠠ ᠥᠭᠭᠦᠭᠳᠡᠯ ᠦᠨ ᠬᠦᠰᠡᠯᠲᠡ ᠠᠮᠵᠢᠯᠲᠠ ᠦᠭᠡᠢ ᠪᠣᠯᠪᠠ᠃ — Unresolved: full traditional orthography, inflection and technical loan spelling require specialist review.
- `ryu`: Commonsぬメタデータぬ問い合わせー、ないびらんたん。 — Unresolved: whether this nominal query construction is natural Shuri/Okinawan rather than a Japanese calque.

## Other targeted review notes

- Hakka Han/PFS use the same Sixian sentence; official 查 caˇ supports PFS chhà. Failure is Hakka sṳt-phai, distinct from Taiwanese sit-pāi. The metadata compound still needs terminology review.
- Taiwanese Han/POJ use the same wording. POJ chhâ-sûn and chu-liāu are not Tâi-lô tshâ-sûn/tsu-liāu or Mandarin transcription.
- Cantonese Han/Jyutping align, preserving lexical tone numbers.
- Vietnamese Hán/Nôm follows Vietnamese word order and readings, including 𧵑 của and 與料 dữ liệu. It is a modern composed sentence, not a claimed historical standardized phrase.
- Jejueo completed polite ending is attested; the full technical phrase remains a modern synthesis requiring review.
- English entries intentionally repeat English. qaa intentionally uses the symbolic convention; neither is presented as a missing translation.

## Font evidence

- `vi-Hani`: anpaintnomui.ttf lacks 追 U+8FFD, 問 U+554F and 。 U+3002. Do not silently alter a good translation to conceal missing font support.
- `mnc-Mong` and `mn-Mong`: every non-space character in these proposals is in notosansmongolian.ttf. This does not prove correct shaping or layout.
- `wuu-Hans`: the bundled Wu font is supplemental and lacks ordinary CJK/Latin; actual fallback-chain testing is needed before claiming a display defect.

## Evidence limits

Primary dictionaries/corpora were preferred for low-resource morphology and requested scripts. Some official terminology pages/PDFs were not retrievable; those entries are labelled review leads rather than validating evidence. High-confidence ordinary-language proposals are model-generated and semantically checked, not individually externally attested. A separate review must decide linguistic acceptance; script presence and a count of 59 cannot do that.

## Selected sources

- [National Ainu Museum dictionary: kopisi](https://ainugo.nam.go.jp/dic?word=kopisi): Tamura and Kayano entries support ask/question and distinguish short answers from substantive inquiry. Does not attest a computing sentence.
- [Ainu Culture Foundation radio course, 2022 volume 3, lesson on ability](https://www.ff-ainu.or.jp/web/learn/language/files/2022AinugoradioVol.3_a4.pdf): eaykap after a verb expresses inability; source supports morphology, not a technical metadata term.
- [P. G. von Möllendorff, A Manchu Grammar (1892), negative verbs](https://en.wikisource.org/wiki/A_Manchu_Grammar): Historical primary grammar: converb -me, perfective -he, akū negation and ci source postposition. Historical spelling conventions are not a modern UI standard.
- [The Historical Phonology of Manchu Dialects, Cornell dissertation, p.121](https://ecommons.cornell.edu/server/api/core/bitstreams/dafbcc0b-b09d-41ba-99b2-41eabe98a3b4/content): Comparative table gives written Manchu mejige as news/information; this is not an attested term for metadata.
- [Hakka Affairs Council, Sixian intermediate vocabulary, entry 4-20 查, p.131](https://elearning.hakka.gov.tw/hakka/files/downloads/317.pdf): 查 caˇ = query/investigate, with a dictionary-lookup example. PFS chhà is orthographic conversion, not Mandarin transliteration.
- [Taiwan Ministry of Education Taiwanese dictionary: 查 phonological index](https://sutian.moe.edu.tw/und-hani/siannuntiau/siann/tsh/_/tsha5/%E6%9F%A5/): Includes 查詢 tshâ-sûn. Convert Tâi-lô tsh to POJ chh, retaining tone marks.
- [Taiwan Ministry of Education Taiwanese dictionary: 失敗](https://sutian.moe.edu.tw/zh-hant/su/1759/): sit-pāi describes an action not succeeding; spelling is shared by POJ and Tâi-lô here.
- [Jejueo Research Institute, 2018 Jejueo school teaching material](https://www.jejueo999.kr/index.php/contents/notice/class?act=view&bd_bcid=notice_class&page=6&seq=755): Uses 헷수다 as completed polite declarative. Does not attest failure/query/metadata vocabulary in a software context.
- [National University of Mongolia Open Data: About](https://data.num.edu.mn/en/about): Mongolian description explicitly explains мета-өгөгдөл as data about data.
- [Mongolian explanatory dictionary: хүсэлт I](https://mongoltoli.mn/dictionary/detail/118450): Request noun and traditional form ᠬᠦᠰᠡᠯᠲᠡ / küselte.
- [Journal of the Japanese Association of Sociolinguistic Sciences 28(1), p.170–185 (2025)](https://www.jstage.jst.go.jp/article/jajls/28/1/28_170/_pdf): Primary corpus discussion attests ちゃーん ない びらん たん, with negative past polite interpretation; no computing phrase attestation.
- [Ủy ban Phục sinh Hán Nôm, Bảng chữ Hán Nôm chuẩn thường dùng, 2023](https://www.hannom-rcv.org/NS/bchnctd%20300623.pdf): Printed p.165 gives 與料 dữ liệu. This supports the Vietnamese character sequence, not Mandarin 資料.
- [Thi Viện Hán Nôm dictionary: 問](https://hvdic.thivien.net/whv/%E5%95%8F): Lists truy vấn 追問 under Vietnamese readings and compounds; digitized dictionaries, not AI explanation.
- [Chunom.org dictionary: U+27D51 𧵑](https://new.chunom.org/pages/27D51/): Gives của, of/belonging to, with historical occurrences. Does not certify a modern sentence.
- [Linguistic Society of Hong Kong Jyutping scheme](https://lshk.org/jyutping-scheme/): Official Jyutping orthographic convention, including tone numbers. Word readings also checked against lexical entries.
