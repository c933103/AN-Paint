# AN Paint M04 independent language review

Review date: 2026-10-12 UTC. Source default: `Commons metadata query failed`.

## Result

All 59 exact tags reviewed: **51 acceptable bounded model proposals, 2 revisions, 6 unresolved**. The consolidated file has 53 usable accepted/proposed values. The unresolved entries have null recommended values; their original non-English candidates are preserved only for further review. No English substitutes were inserted.

This is independent model/source-assisted linguistic review, not native certification. No acceptance was inferred from M03 or withdrawn catalogue conclusions. No production, fonts or GitHub were changed by this reviewer.

## Actual operation

Read the actual `CommonsAttribution.kt`, `MediaGalleryActivity.kt` and `TRANSLATING.md`. `parse` throws `QueryFailureException` whenever the parsed top-level object has an `error` key, regardless of whether its value is null, false, empty or otherwise. The UI maps that typed exception to M04. HTTP failure, response size, missing file metadata, attribution mismatch and image download are distinct situations. Every accepted/proposed sentence describes only query/request failure; there are no variables.

## Immediate decisions

- Retain vi-Hani exactly: **追問超與料𧵑 Commons 失敗。** It reads “Truy vấn siêu dữ liệu của Commons thất bại.” The Han/Nôm syntax and character mapping are appropriate as a modern bounded composition. Retain **追 U+8FFD, 問 U+554F and 。 U+3002**; all three are required by this exact candidate. Do not distort wording to evade the licensed font extension. Punctuation alternatives are conceivable, but the existing ideographic full stop is appropriate, so there is no linguistic reason to remove it.
- Revise ko-KP to **Commons 메타자료 요청에 실패하였습니다.** The primary mirrored DPRK computing text supports the metadata term and request vocabulary. The original lookup term is not proven wrong; the revision closes the previously unsupported regional terminology choice using request semantics explicitly allowed by the operation.
- Revise mn-Cyrl-MN to **Commons-ын мета өгөгдлийн хүсэлт амжилтгүй боллоо.** The change is the genitive suffix after Commons: ordinary back-vowel pronunciation takes -ын under official foreign-word suffix rules.
- Accept the original dz candidate at medium bounded confidence. Independent source checks establish its metadata loan and inquiry noun; the 2018 DDC glossary also provides alternative terminology. The complete sentence is model-reviewed, not externally attested.
- Keep ain-Kana, ain-Latn, mnc-Mong, bo, mn-Mong and ryu unresolved. Specific reasons and the next evidence required are recorded below and in `decisions.json`.

## Eight originally flagged candidates

### ain-Kana: unresolved

The Kana and Latin spellings correspond, including final consonant signs and handakuten, but script correctness does not validate the clause. The dictionary treats kopisi principally as asking someone; the bare noka oruspe phrase does not independently establish an about-metadata argument. That paraphrase may also mean image story/information rather than metadata. Do not accept a word-for-word assembled sentence without resolving both issues.

Recommended value: none. Keep the candidate outside the accepted implementation set.

### ain-Latn: unresolved

The a= notation is a valid Ainu person-prefix convention, not an English fallback. The same kopisi argument-structure and noka oruspe metadata-specificity questions remain as in ain-Kana. The inability predicate is plausible, but does not alone validate the full message.

Recommended value: none. Keep the candidate outside the accepted implementation set.

### mnc-Mong: unresolved

The text is genuinely Manchu-script and the ability/negative morphology is compositionally plausible. The primary grammar supports asking but uses de for the person asked in one worked example; ci as the source of this API inquiry still needs checking. nirugan i mejige is broader image information/news and has not been shown to identify metadata. Suffix-i shaping/spacing also requires actual-script review.

Recommended value: none. Keep the candidate outside the accepted implementation set.

### bo: unresolved

The failure-to-succeed predicate is plausible Tibetan, but the proposed meta-plus-information term and computing inquiry phrase were not substantiated well enough. The upstream Tibetan MediaWiki catalogue offers a different metadata term; it is evidence of variation, not grounds to copy it. Full sentence naturalness remains uncertain.

Recommended value: none. Keep the candidate outside the accepted implementation set.

### dz: acceptable bounded model proposal

Independent lexical evidence now supports both terms: the older primary computer glossary has the query noun and MediaWiki’s actual image-metadata label uses the same meta-plus-data loan. The Dzongkha gi possessive and འབད་མ་ཚུགས inability-after-attempt predicate coherently yield “Could not query Commons metadata.” The 2018 DDC glossary supplies alternative terms, so no exclusive official standard is claimed.

Recommended value: Commons གི་མེ་ཊ་གནས་སྡུད་འདྲི་དཔྱད་འབད་མ་ཚུགས།

### ko-KP: revise

Replace 조회 with 요청 to use a source-grounded request noun. A mirrored DPRK Education Ministry computing text explicitly uses 메타자료 and 자료요청. The new phrase is ordinary Korean formal completed failure morphology and remains within query/request failure semantics. This is a regional evidence improvement; the original 조회 is not proved ungrammatical. Full sentence remains model composition.

Recommended value: Commons 메타자료 요청에 실패하였습니다.

### mn-Mong: unresolved

The traditional-script proposal cannot be accepted merely by converting the Cyrillic meaning. The technical loan spelling, traditional lexical forms and full inflection remain insufficiently checked. Ordinary spaces before suffixes also bypass script-sensitive suffix shaping. Unicode 17 describes MVS for this role and legacy NNBSP compatibility, so a blind whitespace replacement is not enough.

Recommended value: none. Keep the candidate outside the accepted implementation set.

### ryu: unresolved

The proper name and modern loans remain recognizable and nu is plausible, but the nominal 問い合わせー plus ないびらんたん construction has not been established as a natural failed-query sentence. Generic negative/past examples do not validate the nominal connection or rule out a Japanese calque. The exact negative-form example cited by the proposer could not be independently recovered from the extractable paper text.

Recommended value: none. Keep the candidate outside the accepted implementation set.

## Tag/script review

All exact tags are retained. Hakka Han/PFS and Taiwanese Han/POJ pairs remain aligned without Mandarin transliteration. Jyutping keeps tone numbers. Mixed-script Korean retains the proper Hanja. Literary Chinese permits the existing modern technical term. Wu remains explicitly Shanghainese-basis Simplified writing. Latin proper name Commons is permitted in script-specific locales.

Both Mongolian-block candidates require further suffix-shaping scrutiny. Ordinary spaces are not sufficient evidence of proper suffix forms. Unicode 17 describes U+180E MVS for separated suffixes and legacy U+202F compatibility. This review does not prescribe a blind replacement without this Android renderer’s behavior.

## Font evidence and boundaries

Reviewed the supplied cmap report. Its recorded pre-extension vi-Hani subset lacks exactly the three retained characters above. Full bundled cmap coverage of the Manchu and Mongolian proposals does not establish correct language, contextual shaping or layout. The one-character Wu supplemental font is not expected to cover all ordinary Han/Latin text; the actual fallback chain must be tested. This reviewer did not alter or retest fonts.

## Per-tag decisions

| Tag | Decision | Confidence | Recommended exact value |
|---|---|---|---|
| ain-Kana | unresolved | low | Unresolved; no accepted value |
| ain-Latn | unresolved | low | Unresolved; no accepted value |
| mnc-Mong | unresolved | low | Unresolved; no accepted value |
| af | acceptable bounded model proposal | high | Die navraag vir Commons-metadata het misluk |
| ar | acceptable bounded model proposal | high | فشل الاستعلام عن بيانات Commons الوصفية |
| bo | unresolved | low | Unresolved; no accepted value |
| ceb | acceptable bounded model proposal | medium | Wala molampos ang pagpangayo sa metadata gikan sa Commons |
| de | acceptable bounded model proposal | high | Die Abfrage der Commons-Metadaten ist fehlgeschlagen |
| dz | acceptable bounded model proposal | medium | Commons གི་མེ་ཊ་གནས་སྡུད་འདྲི་དཔྱད་འབད་མ་ཚུགས། |
| el | acceptable bounded model proposal | high | Το ερώτημα για τα μεταδεδομένα του Commons απέτυχε |
| en-001 | acceptable bounded model proposal | high | Commons metadata query failed |
| en-AU | acceptable bounded model proposal | high | Commons metadata query failed |
| en-CA | acceptable bounded model proposal | high | Commons metadata query failed |
| en-GB | acceptable bounded model proposal | high | Commons metadata query failed |
| en-IN | acceptable bounded model proposal | high | Commons metadata query failed |
| en-SG | acceptable bounded model proposal | high | Commons metadata query failed |
| en-US | acceptable bounded model proposal | high | Commons metadata query failed |
| en-XV | acceptable bounded model proposal | high | Commons metadata query failed |
| eo | acceptable bounded model proposal | high | La peto pri metadatenoj de Commons malsukcesis |
| es-419 | acceptable bounded model proposal | high | Falló la consulta de metadatos de Commons |
| es-ES | acceptable bounded model proposal | high | Falló la consulta de metadatos de Commons |
| et | acceptable bounded model proposal | high | Commonsi metaandmete päring ebaõnnestus |
| fi | acceptable bounded model proposal | high | Commons-metatietojen kysely epäonnistui |
| fr | acceptable bounded model proposal | high | La requête de métadonnées de Commons a échoué |
| hak-Hant-TW | acceptable bounded model proposal | medium | 查 Commons 个中繼資料失敗。 |
| hak-Latn-TW | acceptable bounded model proposal | medium | Chhà Commons ke chûng-ki chṳ̂-liau sṳt-phai. |
| hu | acceptable bounded model proposal | high | A Commons metaadatainak lekérdezése sikertelen |
| id | acceptable bounded model proposal | high | Kueri metadata Commons gagal |
| it | acceptable bounded model proposal | high | La richiesta dei metadati di Commons non è riuscita |
| ja | acceptable bounded model proposal | high | Commonsのメタデータの問い合わせに失敗しました |
| jje | acceptable bounded model proposal | medium | Commons 메타데이터 질의가 실패헷수다. |
| ko-KP | revise | medium | Commons 메타자료 요청에 실패하였습니다. |
| ko-KR | acceptable bounded model proposal | high | Commons 메타데이터 조회에 실패했습니다. |
| ko-Kore-KR | acceptable bounded model proposal | medium | Commons 메타데이터 照會에 失敗했습니다. |
| lt | acceptable bounded model proposal | high | „Commons“ metaduomenų užklausa nepavyko |
| lv | acceptable bounded model proposal | high | Commons metadatu vaicājums neizdevās |
| lzh-Hant | acceptable bounded model proposal | medium | 查詢 Commons 中繼資料未成。 |
| mn-Cyrl-MN | revise | medium | Commons-ын мета өгөгдлийн хүсэлт амжилтгүй боллоо. |
| mn-Mong | unresolved | low | Unresolved; no accepted value |
| ms | acceptable bounded model proposal | medium | Pertanyaan metadata Commons gagal |
| nan-Hant-TW | acceptable bounded model proposal | medium | 查詢 Commons 的中繼資料失敗。 |
| nan-Latn-TW | acceptable bounded model proposal | medium | Chhâ-sûn Commons ê tiong-kè chu-liāu sit-pāi. |
| nl | acceptable bounded model proposal | high | De aanvraag voor Commons-metadata is mislukt |
| pt-BR | acceptable bounded model proposal | high | Falha na consulta aos metadados do Commons |
| pt-PT | acceptable bounded model proposal | high | A consulta aos metadados do Commons falhou |
| qaa-Zsye-XV | acceptable bounded model proposal | medium | ⚠️ Commons 🗂️ 🔎 ❌ |
| ru | acceptable bounded model proposal | high | Запрос метаданных Commons завершился ошибкой |
| ryu | unresolved | low | Unresolved; no accepted value |
| sw | acceptable bounded model proposal | medium | Ombi la metadata ya Commons halikufaulu |
| tl | acceptable bounded model proposal | high | Nabigo ang kahilingan para sa metadata ng Commons |
| tr | acceptable bounded model proposal | high | Commons meta verileri sorgusu başarısız oldu |
| vi | acceptable bounded model proposal | high | Truy vấn siêu dữ liệu của Commons thất bại |
| vi-Hani | acceptable bounded model proposal | medium | 追問超與料𧵑 Commons 失敗。 |
| wuu-Hans | acceptable bounded model proposal | medium | Commons 个元数据查询失败。 |
| yue-Hant | acceptable bounded model proposal | medium | Commons 嘅中繼資料查詢失敗。 |
| yue-Latn | acceptable bounded model proposal | medium | Commons ge3 zung1 gai3 zi1 liu6 caa4 seon1 sat1 baai6. |
| zh-CN | acceptable bounded model proposal | high | Commons 元数据查询失败 |
| zh-HK | acceptable bounded model proposal | high | Commons 中繼資料查詢失敗 |
| zh-TW | acceptable bounded model proposal | high | Commons 中繼資料查詢失敗 |

## Evidence registry

Source-specific verification boundaries matter: indexed entries count only as lexical evidence; failed direct retrieval is not described as a read PDF. An upstream catalogue supplies usage evidence, not automatic acceptance. The mirrored DPRK book’s printed institutional attribution is visible, but official hosting/authenticity was not independently established.

See `sources.json` for each source’s exact support and retrieval status. Main sources:

- [National Ainu Museum dictionary: kopisi](https://ainugo.nam.go.jp/dic?word=kopisi): Distinguishes asking a short question of someone from a substantive inquiry. Also documents impersonal a= and the differing argument structure of konu. Does not validate this API-query sentence.
- [P. G. von Möllendorff, A Manchu Grammar (1892)](https://en.wikisource.org/wiki/A_Manchu_Grammar): Documents asking with fonjimbi, the -me converb, ability verb mutembi and negative formations. A worked passage uses gucuse de fonjici for asking friends. This is a primary historical text in a public transcription, not a modern computing authority.
- [CTA Tibetan Terminology](https://tibterminology.net/): Review lead only. No lexical validation claimed.
- [MediaWiki Tibetan source catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/bo.json): The metadata key uses a different Tibetan term, རྒྱུ་གཞི་གྲངས།. This establishes a terminology alternative, not correctness of either full AN Paint sentence. Other apparent problems in the catalogue mean it is not accepted blindly.
- [Dzongkha Computer Terms, DzongkhaLinux project / CRULP](https://panl10n.cle.org.pk/outputs/DCT.pdf): Printed p.157 maps Query to འདྲི་དཔྱད། and shows forms built with འབད. Supports the proposal query noun and verb combination.
- [DDC, English-Dzongkha Basic Computer Terminology (2018)](https://www.dzongkha.gov.bt/uploads/files/publications/1.computer_term_text_e53071b6528a9081cabd770fda7a26c4.pdf): Uses the alternative metadata term བརྡ་དོན་གནས་སྡུད and query དྲི་བཀོད. Shows terminology variation. The search extraction has typographic noise; do not mechanically transplant the extracted text.
- [MediaWiki Dzongkha source catalogue](https://github.com/wikimedia/mediawiki/blob/master/languages/i18n/dz.json): The metadata key uses the same loan-plus-data term as the candidate, མེ་ཊ་གནས་སྡུད. Its metadata-help context concerns image/file metadata. This is lexical evidence; it does not certify the new complete sentence.
- [JAVA자료기지프로그람작성법, attributed in the book to 교육성 교육정보쎈터](https://mirror.adversec.com/dprk/dprk-34c4/DPRK-34C3-PDFs/RedStarBooks/05_JDBP.pdf): Printed p.141 explicitly defines 메타자료(MetaData); p.5 uses 자료요청 for logical requests to a data system. Supports 메타자료 and request wording. Does not attest original 조회 or the complete new sentence.
- [Official Mongolian orthographic rules, §49.5–6](https://toli.gov.mn/r): Foreign words containing back vowels take back-vowel suffixes; words without them take front-vowel suffixes. Applied to the ordinary pronunciation of Commons, this supports Commons-ын rather than Commons-ийн.
- [National University of Mongolia Open Data: About](https://data.num.edu.mn/en/about): Explains мета-өгөгдөл as data about data. Supports metadata semantics, not exact traditional-script spelling.
- [Mongolian explanatory dictionary: хүсэлт](https://mongoltoli.mn/dictionary/detail/118450): A source lead for traditional request spelling; not counted as independently verified in this pass.
- [Unicode 17.0, §13.5.1 Mongolian](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-13/): Separated suffixes require special shaping. Unicode 16+ uses U+180E MVS for this role; U+202F NNBSP remains for backward compatibility. Ordinary space is not a substitute. Which convention works with this Android renderer must be checked. Manchu and Mongolian are separate writing systems despite sharing the block.
- [Shinzato and Arakaki, Okinawan Natural Conversation Corpus, 2025](https://www.jstage.jst.go.jp/article/jajls/28/1/28_170/_pdf): Confirms corpus dialect scope, transcription methodology and past tan. Does not establish the proposal nominal-query plus ability/failure construction. The proposer cited an example whose exact typography could not be rechecked here.
- [NINJAL Okinawa-go Dictionary Database](https://mmsrv.ninjal.ac.jp/okinawago/en/index.html): Establishes the Shuri dictionary source and downloadable lexical data, not the modern technical sentence.
- [Hakka Affairs Council, Sixian intermediate vocabulary, entry 4-20](https://elearning.hakka.gov.tw/hakka/files/downloads/150.pdf): 查 caˇ is an inquiry/lookup verb. PFS chhà follows the Sixian pronunciation rather than Mandarin.
- [Taiwan MOE Hakka dictionary: 失敗](https://ecenter8.moe.gov.tw/search_result/?accent=2&id=1229): Defines failure as not succeeding/meeting an aim; the relevant Sixian-family form is siid pai. PFS sṳt-phai is the matching orthographic rendering.
- [Wiktionary: 資料](https://en.wiktionary.org/wiki/%E8%B3%87%E6%96%99): Lists Sixian PFS chṳ̂-liau; used only as secondary orthographic corroboration, not a terminology authority or native certification.
- [Wiktionary: 繼](https://en.wiktionary.org/wiki/%E7%B9%BC): Lists Sixian PFS ki and Taiwanese POJ kè. Used as secondary reading corroboration; neither whole metadata compound is claimed to be a universal written standard.
- [Taiwan MOE Taiwanese dictionary: 詢 index / 查詢](https://sutian.moe.edu.tw/zh-hant/poosiu/poosiu/149/%E8%A9%A2/): Attests Taiwanese 查詢 tshâ-sûn. The corresponding POJ is chhâ-sûn, retaining tones while converting the orthographic tsh.
- [Jejueo Research Institute, 2018 language-school materials](https://www.jejueo999.kr/index.php/contents/notice/class?act=view&bd_bcid=notice_class&page=6&seq=755): Attests 헷수다 as a completed polite form of 하다/허다 in the lesson. The technical subject and compound failure verb remain model synthesis.
- [Jeju government language education: oral records](https://www.jeju.go.kr/jedu/map/record.htm?page=2188): Corroborates 헷수다 in oral Jejueo. Does not establish a conventional translation of metadata/query.
- [Ủy ban Phục sinh Hán Nôm, Bảng chữ Hán Nôm chuẩn thường dùng (2023), p.165](https://www.hannom-rcv.org/NS/bchnctd%20300623.pdf): Provides 與料 dữ liệu. It supports this character mapping rather than Chinese 資料; not the entire modern sentence.
- [Thi Viện, Hán Nôm dictionary: 問](https://hvdic.thivien.net/whv/%E5%95%8F): Lists truy vấn 追問 and the vấn reading. The historic lexeme does not alone establish its modern computing use; the modern Vietnamese sentence is model-reviewed.
- [Chữ Nôm dictionary, U+27D51 𧵑](https://new.chunom.org/pages/27D51/): Gives của and possessive/of examples, supporting the Vietnamese syntactic link.
- [Linguistic Society of Hong Kong, Jyutping scheme](https://lshk.org/jyutping-scheme/): Supports the romanization and tone-number convention; individual word readings are also model-reviewed. It does not certify the whole sentence.

## Artifacts

- `decisions.json`: every exact tag, decision, original/recommended value, backtranslation, rationale, confidence, script notes and source IDs.
- `accepted-values.json`: 51 unchanged accepted bounded proposals.
- `proposed-revisions.json`: 2 source-grounded revisions.
- `accepted-and-proposed-values.json`: 53 consolidated usable values.
- `unresolved-candidates.json`: 6 candidates held out; recommendation is null.
- `sources.json`: independent evidence registry and retrieval limits.
- `validation.json`: scope, placeholder and brand checks with input fingerprints.

`accepted-values-initial.json` and `initial-decision.json` were the earlier 44-tag partial handoff; the complete files above supersede them. Runtime/UI validation and durable project publication remain the parent task’s responsibility.
