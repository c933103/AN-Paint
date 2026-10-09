# Commons import-change notes: independent review of 48 proposed pairs

Review date: 9 October 2026. Input manifest SHA-256: `8de8cabfb1c756128d575e243b4781bad37f65900df49c8b5c15ee5768e2e2f9`. Source commit recorded by that manifest: `8a75b825131f0b24c55a40a3636e9e70792037a8`.

## Result

- Read all 96 messages across the 48 proposed locale pairs. Recommend no SVG-message change.
- Recommend seven raster-message clarity revisions: Esperanto, Estonian, Finnish, Indonesian, Malay, Cyrillic Mongolian and Vietnamese. These improve explicitness; they are not seven proven translation errors.
- Recommend retaining the other 41 pairs in this bounded text review. That is not native-speaker acceptance or a whole-language completion claim.
- All required literal tokens survive in every original pair. None of the raster strings introduces SVG/PNG conversion or the vector-only setting tokens.
- No production catalogue or manifest was edited. The 11 blocked tags and 81 unscoped tags were excluded.

## Semantic baseline and evidence distinction

Alpha compositing combines source/background pixels according to transparency. It is not merely an opacity-setting change, channel deletion, or rasterization. [GIMP’s algorithm documentation](https://developer.gimp.org/core/algorithm/compositing/) and [ImageMagick’s compositing documentation](https://imagemagick.org/compose/) support this technical baseline. They do not establish any target-language phrase’s fluency.

The notice is intentionally a compact metadata list. Its localized size fragment need not be expanded into a sentence. A raster parenthesis can explain transparency-based combining without coining an alpha-plus-composition term. No unsupported promise about transparency retention, losslessness, color space or layer preservation should be added.

## Recommended raster wording

| Locale | Recommended full message | Reason |
| --- | --- | --- |
| eo | AN Paint: background=#FFFFFF (kunmetado laŭ travidebleco). | Prefer an explicit combining-according-to-transparency explanation over a tentative technical compound. ReVo does not prove the original is erroneous. |
| et | AN Paint: background=#FFFFFF (ühendamine läbipaistvust arvestades). | The dense alfakomposiitimine coinage was not established by consulted lexical sources. The proposed phrase says combining while accounting for transparency. |
| fi | AN Paint: background=#FFFFFF (yhdistäminen läpinäkyvyyden perusteella). | The short compound alfakoostaminen is understandable as a construction but not established here as standard graphics terminology. The paraphrase explicitly names combining and transparency. |
| id | AN Paint: background=#FFFFFF (penggabungan berdasarkan transparansi). | Prefer combining based on transparency over the tentative pengomposisian alfa nominalization. The vendor source supports the technical meaning and transparency vocabulary. |
| mn-Cyrl-MN | AN Paint: background=#FFFFFF (тунгалаг байдлыг харгалзан нэгтгэх). | Prefer combining with consideration of transparency over the weakly supported альфа нийлүүлэлт, whose result noun also commonly denotes supply. Grammar/register is a model judgement with constituent dictionary support. |
| ms | AN Paint: background=#FFFFFF (penggabungan mengikut ketelusan). | Prefer combining according to transparency over penggubahan, which can suggest artistic composition or arrangement. This is a clarity recommendation, not proof that a specialist never uses that term. |
| vi | AN Paint: background=#FFFFFF (ghép ảnh theo độ trong suốt). | Prefer combining images according to transparency over the generic synthesis/aggregation noun tổng hợp. It does not say to change the transparency value. |

All seven phrases above are editorial paraphrases, not verbatim dictionary quotations. The Mongolian phrase particularly remains a model grammar/register judgement with dictionary-supported constituents; the traditional-script counterpart must be reviewed independently.

## Paired-script and register checks

- Taiwanese: 原本大細 ↔ goân-pún tōa-sè; 照透明度合成 ↔ chiàu thàu-bêng-tō͘ ha̍p-sêng. MOE gives Tâi-lô thàu-bîng, ha̍p-sîng and tōo. The proposed Latin locale uses the project’s POJ bêng, sêng and tō͘. Do not “correct” these to Tâi-lô solely to match the dictionary display.
- Cantonese: 按透明度合成 ↔ on3 tau3 ming4 dou6 hap6 sing4. 粵典 supports the transparency and combining readings. These are grammatical technical fragments, but dictionary entries do not constitute external acceptance of the complete notice.
- Korean: 알파 합성 ↔ 알파 合成 retains the same operation; the mixed-script variant is still Korean. The DPRK pair’s exact local technical register is not independently established.
- Literary Chinese and written Wu: the transparency-based clauses convey the technical meaning. This does not certify an ancient Literary Chinese term or a pan-Wu standard.
- Arabic: the logical string keeps conversion direction and literal tokens. Actual RTL/LTR display ordering remains a UI test, not something this source-text review can certify.
- English regional tags preserve exact English because the two fragments have no relevant regional contrast. en-XV and qaa-Zsye-XV are layout fixtures; the emoji hints do not count as natural-language translations.

## Per-locale whole-message review

| Locale | Outcome | SVG message | Raster message |
| --- | --- | --- | --- |
| af | No required edit found | oorspronklike grootte identifies the original dimensions; the adjectival agreement is ordinary for this fragment. | alfa-samestelling denotes alpha composition; it does not assert alpha removal. Exact specialist-term preference was not independently attested. |
| ar | No required edit found | الحجم الأصلي is a definite original-size noun phrase; source-to-destination SVG arrow and all setting tokens remain literal. | تركيب ألفا denotes alpha composition. Mixed RTL/LTR rendering still needs an actual display check; no text-level reversal is found. |
| ceb | No required edit found | orihinal nga gidak-on retains the original-size meaning and the nga linker. | paghiusa pinaagi sa alpha expresses combining by means of alpha. No false claim of changing opacity or rasterizing the bitmap is added; specialist idiomaticity is not certified. |
| de | No required edit found | Originalgröße is a suitable original-dimensions label in this technical list. | Alpha-Komposition is semantically legible. There is no requirement to copy GIMP’s preferred wording to be accurate. |
| el | No required edit found | αρχικό μέγεθος keeps the original/initial dimensions rather than file weight. | σύνθεση άλφα expresses alpha composition; no removal or opacity-setting verb is introduced. |
| en-001 | No required edit found | Exactly equals the supplied English source, including the original-size clause. | Exactly equals the supplied English source. No regional vocabulary distinction is required by either message. |
| en-AU | No required edit found | Exactly equals the supplied English source, including the original-size clause. | Exactly equals the supplied English source. No regional vocabulary distinction is required by either message. |
| en-CA | No required edit found | Exactly equals the supplied English source, including the original-size clause. | Exactly equals the supplied English source. No regional vocabulary distinction is required by either message. |
| en-GB | No required edit found | Exactly equals the supplied English source, including the original-size clause. | Exactly equals the supplied English source. No regional vocabulary distinction is required by either message. |
| en-IN | No required edit found | Exactly equals the supplied English source, including the original-size clause. | Exactly equals the supplied English source. No regional vocabulary distinction is required by either message. |
| en-SG | No required edit found | Exactly equals the supplied English source, including the original-size clause. | Exactly equals the supplied English source. No regional vocabulary distinction is required by either message. |
| en-US | No required edit found | Exactly equals the supplied English source, including the original-size clause. | Exactly equals the supplied English source. No regional vocabulary distinction is required by either message. |
| en-XV | No required edit found | Exactly equals the supplied English source, including the original-size clause. | Exactly equals the supplied English source. Vertical-English layout fixture; this pass does not test its layout. |
| eo | Clarity revision proposed | origina grando is a grammatical adjectival size fragment. | alfa-komponado is interpretable, but a transparent explanation is preferable for this short notice. |
| es-419 | No required edit found | tamaño original is neutral Latin-American Spanish and works as a fragment in the semicolon list. | composición alfa communicates the intended operation; no regional distinction is needed in this phrase. |
| es-ES | No required edit found | tamaño original is also suitable for Spain; no tense or address form occurs. | composición alfa communicates the intended operation; same text as es-419 is justified by this specific wording. |
| et | Clarity revision proposed | algne suurus is a grammatical original-size phrase. | Recommend the explicit transparency-based combination paraphrase instead of relying on the tentative dense coinage. |
| fi | Clarity revision proposed | alkuperäinen koko is a grammatical original-size phrase. | Recommend the explicit transparency-based combination paraphrase; no inference that the old compound is categorically invalid. |
| fr | No required edit found | taille d’origine preserves original size; the typographic apostrophe does not need Android ASCII quote escaping. | composition alpha is a clear nominal description; it does not mean removing the alpha channel. |
| hu | No required edit found | eredeti méret keeps original dimensions; no comparative or resized meaning is introduced. | alfa-kompozitálás is semantically recognizable technical wording; this pass does not settle publisher-specific hyphenation preferences. |
| id | Clarity revision proposed | ukuran asli is a grammatical original-size fragment and does not use the Malay saiz form. | Recommend the plain combining-based-on-transparency phrase; retain Indonesian berdasarkan/transparansi wording. |
| it | No required edit found | dimensioni originali uses a natural plural for dimensions, preserving original size. | composizione alfa communicates alpha composition; pluralizing the SVG dimensions does not require changing this operation noun. |
| ja | No required edit found | 元のサイズ is a normal original-size fragment. | アルファ合成 conveys alpha compositing. It does not use an opacity-change or channel-deletion expression. |
| ko-KP | No required edit found | 본래 크기 preserves original size. Regional dictionary/technical-register acceptance for DPRK is not established by this model pass. | 알파 합성 conveys the intended combination at the Korean semantic level; regional register and spacing conventions remain qualification points. |
| ko-KR | No required edit found | 원래 크기 is a grammatical original-size fragment. | 알파 합성 communicates the intended operation; the Korean label contains no unsupported rasterization claim. |
| ko-Kore-KR | No required edit found | 원래 크기 is shared with the Hangul variant, retaining Korean grammar. | 合成 corresponds to 합성, so 알파 合成 preserves the ko-KR operation while following the existing mixed-script convention; no Chinese syntax is introduced. |
| lt | No required edit found | pradinis dydis retains original/initial size in the terse list. | alfa komponavimas is interpretable as alpha composition. The GIMP page’s English fallback is not treated as Lithuanian language evidence; exact specialist preference remains unverified. |
| lv | No required edit found | sākotnējais izmērs is a grammatical original-size fragment. | alfa kompozīcija conveys alpha composition at the nominal level; this is not independently established as the preferred Latvian graphics term. |
| lzh-Hant | No required edit found | 原寸 is a compact original-size expression suited to the project’s technical Literary Chinese register. | 依透明度合成 explicitly says to combine according to transparency. Modern technical vocabulary in a literary-style interface is not evidence of historical classical attestation. |
| mn-Cyrl-MN | Clarity revision proposed | анхны хэмжээ retains original size and is a grammatical noun phrase. | Recommend the dictionary-assisted transparency-based combination paraphrase; do not infer approval of the separate traditional-script locale. |
| ms | Clarity revision proposed | saiz asal is Malay original-size wording and remains distinct from Indonesian ukuran asli. | Recommend the plain combining-according-to-transparency phrase; do not treat penggubahan as an independently attested graphics standard. |
| nan-Hant-TW | No required edit found | 原本大細 is paired with goân-pún tōa-sè, retaining the Taiwanese size expression. | 照透明度合成 is semantically paired with the POJ expression. Dictionary entries establish constituent readings, not whole-message native acceptance. |
| nan-Latn-TW | No required edit found | goân-pún tōa-sè is the POJ counterpart of 原本大細; the diacritics and hyphenation remain intact. | chiàu thàu-bêng-tō͘ ha̍p-sêng matches 照透明度合成. Do not change bêng/sêng to bîng/sîng solely from MOE’s Tâi-lô display; the project uses POJ. |
| nl | No required edit found | oorspronkelijke grootte uses the expected inflected adjective in the original-size label. | alfacompositie is semantically transparent; no necessity to substitute English alpha compositing or alpha removal. |
| pt-BR | No required edit found | tamanho original is suitable in Brazilian Portuguese. | composição alfa is grammatical and retains the technical operation; no BR-specific change is necessary here. |
| pt-PT | No required edit found | tamanho original is also suitable in European Portuguese. | composição alfa retains the technical operation; this exact terse phrase does not require a regional difference. |
| qaa-Zsye-XV | No required edit found | The size emoji supplements the exact English phrase; it does not replace the original-size meaning. | The puzzle emoji supplements exact English alpha compositing. This tag is a layout fixture, not a natural-language translation. |
| ru | No required edit found | исходный размер correctly refers to source/original size. | альфа-композиция is semantically understandable. GIMP explains the same concept with совмещение; that difference alone is not a defect. A stylistic альфа-смешивание change is unnecessary. |
| sw | No required edit found | ukubwa asili carries original size in a short label; no claim of scaling or changing dimensions is added. | uchanganyaji kwa alfa states combining by alpha. Exact specialist terminology and the terse size-label style lack independent native review. |
| tl | No required edit found | orihinal na laki retains original size with the na linker. | pagsasama gamit ang alpha means combining using alpha; no deletion, opacity-change, or vector-conversion claim is introduced. |
| tr | No required edit found | özgün boyut retains the original-size concept in this context; the source-format arrow fixes the conversion direction. | alfa birleştirme denotes combining using alpha. No compelling semantic reason to replace the existing size label was found. |
| vi | Clarity revision proposed | kích thước gốc is a natural original-dimensions phrase. | Recommend the explicit combining-images-by-transparency phrase rather than relying on generic tổng hợp; no opacity alteration is claimed. |
| wuu-Hans | No required edit found | 原来大小 retains original size in the project’s simplified written Wu convention. | 照透明度合成 is an explicit transparency-based combining phrase. Shared technical Han vocabulary alone does not establish a pan-Wu standard or independent dialect fluency. |
| yue-Hant | No required edit found | 原本大小 preserves original dimensions and pairs with Jyutping jyun4 bun2 daai6 siu2. | 按透明度合成 explicitly describes combining according to transparency and pairs with the checked Jyutping constituents. |
| yue-Latn | No required edit found | jyun4 bun2 daai6 siu2 preserves the Han counterpart’s size phrase and the project’s spaced Jyutping convention. | on3 tau3 ming4 dou6 hap6 sing4 matches 按透明度合成. Dictionary evidence supports the new transparency/combine readings; full-message acceptance remains a separate claim. |
| zh-CN | No required edit found | 原始大小 retains source/original dimensions in Simplified Chinese. | 阿尔法合成 is a comprehensible alpha-compositing expression; the operation is not described as deleting the alpha channel. |
| zh-HK | No required edit found | 原本大小 is an appropriate original-size fragment in Hong Kong Traditional Chinese. | Alpha 合成 preserves a technical Latin loan plus the compositing noun; retaining Alpha does not make the whole notice an English placeholder. |
| zh-TW | No required edit found | 原始大小 is an appropriate original-size fragment in Taiwan Traditional Chinese. | Alpha 合成 conveys alpha compositing with a customary technical Latin loan; no action concerning opacity settings is added. |

## Sources and their limits

- [gimp-compositing](https://developer.gimp.org/core/algorithm/compositing/): Technical meaning: pixels from layers and their backgrounds are combined using alpha values; not a statement about deleting a channel. Limit: Fluency or the preferred translation in any target language.
- [imagemagick-compositing](https://imagemagick.org/compose/): Technical meaning: pixel opacity affects each pixel color’s contribution when composited. Limit: The project’s implementation or target-language terminology.
- [revo-komponi](https://reta-vortaro.de/revo/art/kompon.html): komponi includes artistic composition and putting constituents together; kunmeti is used in the explanation. Limit: That alfa-komponado is wrong, or that the proposed full Esperanto clause is externally approved.
- [eki-transparency](https://sonaveeb.ee/search/unif/est/eki%2Cesterm/l%C3%A4bipaistvus/1/est): The literal see-through meaning and inflected forms of läbipaistvus, including läbipaistvust. Limit: An established Estonian alpha-compositing term or the whole proposed sentence.
- [gimp-fi-layers](https://docs.gimp.org/2.10/fi/gimp-image-combining.html): Finnish image-combining vocabulary and explanations of transparency and colors being combined with lower layers. Limit: An attested term alfakoostaminen; the glossary examined separately largely falls back to English.
- [microsoft-id-alpha](https://learn.microsoft.com/id-id/windows/win32/gdi/alpha-blending): Indonesian vendor explanation connects transparency components and alpha blending; uses transparansi and perpaduan alfa. Limit: Native-speaker verification or endorsement of the proposed penggabungan phrase.
- [dbp-gubahan](https://prpmv1.dbp.gov.my/Search.aspx?k=gubahan): Lexical composition/arrangement contexts for gubahan. Limit: A specialized Malay compositing standard. The direct compositing lookup was inaccessible.
- [microsoft-ms-transparency](https://explore.microsoft.com/ms-my/edge/features/edge-for-game-bar?form=MT0160): Malay ketelusan is used for a widget whose transparency reveals the game behind it. Limit: The complete proposed Malay raster clause or any preferred alpha-compositing name.
- [mongol-supply](https://mongoltoli.mn/dictionary/detail/62248): нийлүүлэлт is a result noun with supply-related examples; this explains possible ambiguity in the tentative phrase. Limit: That нийлүүлэлт can never mean combination.
- [mongol-combine](https://mongoltoli.mn/dictionary/detail/65225): нэгтгэх has the sense of making separate things one. Limit: A conventional graphics term or full-sentence acceptance.
- [mongol-transparent](https://mongoltoli.mn/dictionary/detail/89712): тунгалаг has a literal see-through/clear sense. Limit: A complete computing-register translation.
- [adobe-vi-vocabulary](https://helpx.adobe.com/vn_vi/photoshop/desktop/text-typography/get-started-with-text/update-cjk-text-layers.html): Adobe’s Vietnamese navigation uses ghép ảnh and độ trong suốt in image-editing contexts. Limit: An exact alpha-compositing equivalent. This is constituent vocabulary evidence only.
- [taiwanese-transparent](https://sutian.moe.edu.tw/zh-hant/siannuntiau/tiau/3/au/thau3/%E9%80%8F/): MOE gives 透明 as Tâi-lô thàu-bîng; the project’s POJ thàu-bêng is an editorial orthographic conversion. Limit: Verbatim MOE endorsement of POJ or the whole technical phrase.
- [taiwanese-combine](https://pedia.cloud.edu.tw/Entry/Detail?search=%E5%90%88%E6%88%90&title=%E5%90%88%E6%88%90): Education Cloud’s MOE Taiwanese entry gives 合成 as Tâi-lô ha̍p-sîng, corresponding to project POJ ha̍p-sêng. Limit: Full technical-clause fluency.
- [taiwanese-degree](https://sutian.moe.edu.tw/zh-hant/su/4859/): 度 tōo includes degree or extent; POJ tō͘ preserves that reading. Limit: An attested whole entry for 透明度 in the proposed clause.
- [cantonese-according](https://words.hk/zidin/%E6%8C%89%E7%85%A7): 按 on3 in 按照 has the according-to sense. Limit: A graphics-specific usage example.
- [cantonese-transparent](https://words.hk/zidin/%E9%80%8F%E6%98%8E%E5%BA%A6): 透明度 is tau3 ming4 dou6 and has a literal transparency sense. Limit: The whole phrase’s independent acceptance.
- [cantonese-combine](https://words.hk/zidin/%E5%90%88%E6%88%90): 合成 is hap6 sing4 and can describe combining media, including images. Limit: A specialized alpha-compositing standard.
- [gimp-ru-compositing](https://docs.gimp.org/3.0/ru/gimp-layer-new.html): Russian explanation distinguishes blending from compositing and describes combining with regard to each pixel’s transparency. Limit: That only one Russian term is acceptable; no replacement is required solely because GIMP uses совмещение.

## Negative and insufficient lookups

- The direct DBP compositing query was inaccessible; it is not counted as term evidence.
- The Finnish glossary and Lithuanian new-layer documentation contain relevant English fallback passages. A locale code in a URL is not evidence that the passage supplies a local term.
- The attempted GIMP Vietnamese and Indonesian glossary pages were inaccessible. The Microsoft Vietnamese alpha-blending page exposed an English article under a Vietnamese shell; it is not Vietnamese terminology evidence.
- No matching lexical source was found for every remaining short technical compound. Lack of a search hit is not a defect finding.

## Files and limitations

- `independent-review-48.json`: full original and recommended messages, all 48 locale rows, bounded outcomes, source IDs and limitations.
- `proposed-clarity-revisions.json`: seven sparse raster replacements for the coordinator to consider; not applied.
- `literal-checks.json`: reproducible input-snapshot checks for 48 pairs/96 messages, exact tokens, key set, English identity and blocked-tag exclusion.
- This pass provides independent model-assisted text review only. It does not claim native fluency, comprehensive linguistic verification, compilation, CI success, device rendering, or completion of other localization work.
