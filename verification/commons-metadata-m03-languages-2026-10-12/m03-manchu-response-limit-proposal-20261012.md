# Manchu M03 response-limit proposal

ᠨᡳᡵᡠᡤᠠᠨ ᡳ Commons ᠴᡳ ᠠᠯᡳᠮᡝ ᡤᠠᡳᡥᠠ ᠮᡝᠵᡳᡤᡝ ᡳ ᡠᡥᡝᡵᡳ ᡴᡝᠮᡠᠨ ᡨᠣᡴᡨᠣᡥᠣ ᡴᡝᠮᡠᠨ ᠴᡳ ᡶᡠᠯᡠ.

nirugan i Commons ci alime gaiha mejige i uheri kemun toktoho kemun ci fulu.

Back-translation: The total amount of information about the image received from Commons is greater than the set limit.

Status: Source-assisted proposal; independent reviewer recommends acceptance as a contextual paraphrase.

Confidence: moderate-source-assisted-paraphrase; not a claim of native competence or attested modern terminology

## Rationale
This translates the error through a received-data paraphrase. The head noun is mejige, information; nirugan i specifies information about the image, while Commons ci alime gaiha specifies its source and receipt. The comparative bounds that received information's total amount. Initial nirugan i, followed by the receipt modifier immediately before mejige, avoids presenting the image itself as the received head. uheri emphasizes the aggregate rather than an individual metadata field. No invented metadata, HTTP-response or byte word is asserted. The English source contains neither a numeric limit nor a byte unit, so no numeric threshold or unit is added. Commons is unchanged.

## Constituents
- nirugan: image/picture (S1)
- i: genitive linking image with information; here information about the image (S2, S3)
- Commons: provider name, preserved literally (T1)
- ci: ablative: from (S2)
- ali-me gai-ha: received; converb plus perfect participle, modifying information (S2, S4)
- mejige: information; ordinary historical word, contextually extended to transmitted image information (S1, S3)
- i: genitive attaching the complete received-information phrase to its amount (S2)
- uheri: total/aggregate (S1, S5)
- kemun: measure/amount; a contextual extension to received-data size (S1, S6)
- tokto-ho: set/established; perfect participial modifier of the second measure (S2, S5)
- kemun: limit/measure (S1, S6)
- ci fulu: greater than/in excess of; predicate comparison without an invented verb form (S2, S5, S7)

## Limits
- The composed sentence is new. Historical lexical and grammatical evidence supports its constituents; it does not attest HTTP or JSON vocabulary in contemporary Manchu.
- The byte-size interpretation is contextual: the sentence explicitly measures the total received image information, but does not literally name bytes. This mirrors the English source's absence of a byte unit. Information-size rather than information-quality is the intended reading of kemun and fulu here.
- The paraphrase identifies metadata as information about the image; it does not claim mejige alone is a standardized translation of metadata.
- The receipt phrase modifies mejige, with nirugan i placed first after independent reviewer feedback. Final full-sentence naturalness remains less certain than the supported constituent meanings.
- A Unicode/transliteration check is provided separately. Android shaping and visual rendering have not been tested for this proposal.

## Sources
- S1: [Kuribayashi: Manchu index to the Qing Manchu-Mongolian-Chinese dictionary](https://gerel.net/articles/roncho/A47All.pdf). Full PDF text inspected. nirugan: picture; mejige: information; kemun: measure/standard; fulu: surplus; uheri: total. The index separately records exceed-related vocabulary.
- S2: [P. G. von Möllendorff, A Manchu Grammar (1892)](https://en.wikisource.org/wiki/A_Manchu_Grammar). Public-domain primary grammar transcription inspected. Genitive i, ablative/comparative ci, perfect gaiha, and pre-head genitive/participle syntax support the sentence. This supports a compositional analysis, not an attested complete UI sentence.
- S3: [Monggo Yamun and Tulergi Golo be Dasara Jurgan, Saksaha 19 (2023), palace-memorial transcription](https://journals.publishing.umich.edu/saksaha/article/id/4215/download/pdf/). Indexed primary-text excerpt inspected; direct retrieval returned an anti-bot page. The original ukanju i mejige is translated as information about fugitives, supporting X i mejige as information about X.
- S4: [Noda Jin and Onuma Takahiro, A Collection of Documents from the Kazakh Sultans to the Qing Dynasty (2010)](https://www.battle-of-qurman.com.cn/literature/Onuma-2010.pdf#page=32). Full scholarly primary-document edition inspected. alime gaiha directly precedes a received document head, with the edition's translation confirming receipt.
- S5: [Junsei Watanabe, A Manchu manuscript on arithmetic, SCIAMVS 6 (2005), 177–264](https://www.sciamvs.org/files/SCIAMVS_06_177-264_Watanabe.pdf). Full primary-manuscript transcription and scholarly translation inspected. Established numerical values, greater-than comparison in arithmetic, and total/summed quantities independently support the proposed modifier, predicate and aggregate wording.
- S6: [H. T. Toh, Manchu transcription and glosses in Victor H. Mair, Soldierly Methods, Sino-Platonic Papers 178 (2008)](https://sino-platonic.org/complete/spp178_art_of_war.pdf#page=122). Full primary-text transcription and scholarly glosses inspected. Explicit limit-related glosses for kemun provide independent support for the upper-bound noun.
- S7: [Manchu Studies Group, Muwa Gisun Section Three, discourse 11](https://www.manchustudiesgroup.org/translations/muwa-gisun/muwa-gisun-section-three/). Full original transcription and translation inspected. A bare ci fulu predicate occurs with no expressed copula. This supports the error sentence's concise predicate form.
- S8: [Mark Elliott, Manchu S-A, Postpositions](https://www.manchustudiesgroup.org/wp-content/uploads/2020/07/Handout-5-Postpositions.pdf). Full handout inspected. dabali is classified as a postposition and mejige appears as the object of information gathering. Used to avoid blindly reusing catalogue morphology.
- T1: [AN Paint CommonsAttribution byte-limit check](https://github.com/c933103/AN-Paint/blob/79b1f990a98eaf44c28351cd02c20157c70d8dff/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L79). Local source inspected; stable URL from the prior research record. Technical meaning of the response-limit error, not language evidence.

## Verification
Unicode-to-romanization roundtrip, literal Commons, NFC, absence of hidden controls and XML text roundtrip passed. No implementation or publication changes. Android rendering was not tested.

## Independent review
The separate reviewer recommends the reordered sentence with uheri as an acceptable contextual paraphrase with moderate confidence. The reviewer independently verified its romanization and primary-document receipt and information-about constructions. This is not native-speaker certification or Android rendering validation.
