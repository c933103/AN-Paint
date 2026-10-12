# M04 linguistic review recovery

Recovered on 2026-10-12 after executor filesystem replacement. This is a recovery of the completed review, not a new translation review or a new source-research pass.

## Ready to use

`accepted-and-proposed-values-v4.json` contains all **59 final exact values** and matches the independently recorded pre-replacement SHA256:

`00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d`

This establishes exact complete-file byte recovery. The six added values also independently match their previously recorded individual UTF-8 hashes, including the Manchu U+180E and traditional Mongolian U+202F controls.

`decisions-v4.json` contains all 59 final decisions: **57 acceptable bounded model proposals and two usable proposed revisions**. It is reconstructed by reapplying the exact surviving final decision-generation code to the earlier verified decision file. No pre-replacement whole-file v4 decision hash survives, so it is not labeled independently hash-verified byte recovery. Its newly calculated SHA256 is recorded separately in `DECISION-RECOVERY-MANIFEST.json`, not misrepresented as an old hash.

## Other exact history recovered

- `decisions-v3.json` matches its pre-replacement SHA256 `3812a15c62eb16a10ae895d7938e71b9323ac7bcd431378a964de2777e4ece48`.
- `accepted-and-proposed-values-v3.json` matches its pre-replacement SHA256 `63a86f15801b295e8284ecad8d93d66fb0f5d6fc57d03b1570055f0c3c8fad54`.
- The initial 53-value file and original 59-tag decision file are copied byte-for-byte from the parent’s frozen surviving contents. Their provenance and current hashes are recorded by the recovery manifests.
- The v2 value file and three small successor-value files were recreated with the recorded original JSON serialization and insertion order. Their values are verified, but no independent prior whole-file hashes are available for these particular files.

## Final successor decisions retained

| Tag | Final decision and boundary |
|---|---|
| ain-Latn | Accept the `Tatum (noka oruspe) anak Commons a=konu eaykap.` sentence. The documented two-object inquiry verb, topic structure and inability construction resolve the initial valency hold. Medium semantic/grammatical confidence, lower idiomatic confidence. |
| ain-Kana | Accept the corresponding Kana value with Saru-oriented トゥ and small final consonant signs. Same linguistic limits as Latin. |
| mnc-Mong | Accept `Commons de nirugan i mejige be fonjime mutehekū.` in the exact Manchu-script value with three U+180E separators. Addressee/content case frame and information-about relation have source support. Medium contextual confidence; Android rendering unverified. |
| bo | Accept the inquiry-to-Commons nominalized clause and past non-success predicate. Image-information is a contextual attribution-metadata paraphrase. Medium confidence; predicate composition is not claimed as an exact corpus quotation. |
| mn-Mong | Accept the explicit request-to-inquire clause and past verbal noun plus negative. Preserve three U+202F legacy suffix gaps. Valid legacy encoding does not establish Android compatibility. Medium contextual confidence. |
| ryu | Accept `Commonsんかい メタデータ たぬむしぬ ないはんちゃん。` at medium confidence. The explicit request clause resolves the earlier `sirabi` examination/lookup ambiguity. Regular `tanumu-shi` formation is supported by a primary m-type paradigm; it is not falsely claimed as an independently attested primary full token. |

All remain **model/source-assisted proposals**, not native-speaker certification. The two earlier revised values, ko-KP and mn-Cyrl-MN, remain unchanged from the frozen base. No earlier rejected wording has silently become accepted.

## Reconstructed evidence, with preserved limits

`SUCCESSOR-SOURCES-RECONSTRUCTED.json` restores 33 source IDs and their support/retrieval limits from surviving tool outputs and review-generation code. It is a new recovery document, not a claim to reproduce the original source-registry bytes. Every source ID referenced by the six successor decisions resolves there.

Important limits remain explicit:

- Ainu’s computing noun is documented in a modern glossary, without established broad community adoption. The full UI sentence remains compositional and Saru-oriented, with an Ishikari-marked picture-word entry among its lexical evidence.
- Manchu’s palace-memorial genitive phrase was checked in indexed primary text; the direct journal PDF had an Anubis denial. No bypass or full-PDF retrieval was claimed.
- Tibetan’s composed negative success predicate is accepted by grammatical composition; no exact full-predicate corpus quotation was recovered.
- The Mongolian thesis’s relevant pages were independently rendered and visually inspected before replacement. The primary PDF bytes are not recovered here.
- Okinawan’s nominalization table and practical dictionary were checked in official indexed primary excerpts, not full-PDF page images. The Arts University recorded-speech page was independently rendered and visually inspected before replacement. Its original PDF hash is retained, but the PDF itself is not recovered here.
- `MANCHU-SHAPING-EVIDENCE-RECONSTRUCTED.json` preserves the earlier host HarfBuzz suffix-i distinction and original font hash. This was not rerun, and is not Android shaping/layout certification.

Raw source PDF/workbook/HTML caches and the original full successor-report/source-registry files are not represented as recovered binaries. No new network requests, translation research, production edits, GitHub actions, authentication actions or Work tasks occurred in this recovery.

## Semantic and integrity checks

The source message remains exactly “Commons metadata query failed”. The trigger is presence of any top-level parsed JSON `error` key, including null, false and empty object. Accepted paraphrases do not assign HTTP/network, absent/invalid-data, parsing, byte-limit or image-download causes.

All 59 recovered value entries agree with the final decision objects and pass XML roundtrip and Commons preservation checks. Exact recovered text has not been normalized or changed to make validation pass. See `RECOVERY-VALIDATION.json`, `RECOVERY-MANIFEST.json`, and `DECISION-RECOVERY-MANIFEST.json` for the exact recovery distinctions.
