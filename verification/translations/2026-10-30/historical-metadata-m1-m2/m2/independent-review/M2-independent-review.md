# Independent M2 review — final two metadata clauses

## Exact recommendations

Both exact proposals receive **ACCEPT M** as bounded experimental wording under the already scoped M1 modern metadata convention. This records the independent recommendation before any later adoption overlay; it does not rewrite prior held variants or frozen ledgers.

| Locale / source key | Tier | Exact English | Exact M2 target | Decision |
|---|---|---|---|---|
| ang / colour_invalid_metadata | P1 | The image has invalid or unsupported colour metadata. | Seo anlicnes hæfþ unriht hiwsidegewritu oþþe swilc þe þis weorctol ne onfehþ. | ACCEPT M |
| non / colour_truncated_metadata | P1 | The image ends inside its colour metadata. | Myndritit endisk innan viðbótarrita sinna um liti. | ACCEPT M |

Moderate confidence reflects the historical grammar evidence plus deliberate modern technical extensions, not native-human certification or measured spontaneous comprehension. No other held value is resolved by these two recommendations.

## ANG: factual unsupported-state relative

The single change is `onfo` → `onfehþ`. B–T directly attests `onféhþ` in both material/non-material reception and acceptance contexts. Omitting the length accent follows the declared ANG normalization; it does not create a different conjugation. The dictionary also documents several object cases, so no exclusive genitive-government rule is being imposed. [B–T on-fón](https://bosworthtoller.com/24545).

Glasgow §67 supports indeclinable `þe` in object relatives and indicative as the ordinary relative-clause mood. Here `þis weorctol` is the singular subject; `swilc` is the alternative neuter plural matrix object referring to the same colour records. `Ne onfehþ` directly states present non-acceptance by the application. [*Essentials of Old English*, §67](https://stella.glasgow.ac.uk/eoe/plus-sentence-structure-3.html).

The new software sense is functional input acceptance/support, not user permission or refusal. `Oþþe` preserves **invalid OR unsupported**, without saying that all unsupported metadata is invalid. Nothing asserts that the metadata is missing or that a damaged file has been repaired. The prior `onfo` may have a generic/modal subjunctive analysis: it is **not declared impossible**. M2 chooses the more directly evidenced factual clause and resolves the specific review uncertainty.

## NON: historical middle and reflexive possession

The single change is `endar` → `endisk`. C–V ENDA II.1 supplies the come-to-an-end sense and exact `endisk` with overt nominative subjects. The proposal therefore need not depend on the earlier neuter's case ambiguity or import a modern nominative-subject intransitive construction. It does not mean the file intentionally destroys itself; the attested middle has an ordinary event-ending sense. The separate last-out/endure sense is not the intended contextual reading. [C–V ENDA II–III](https://norroen.info/dct/cleasby/e.html).

Sweet §130 supports historical `-sk` middle morphology. His possessive table gives genitive plural `minna`, and §110 applies the paradigm to `sinn`; thus `sinna` agrees with plural possessed `viðbótarrita`, not with the number of the possessor. `Myndritit` is the singular file subject to which this reflexive possessive refers. [Sweet, *An Icelandic Primer*, possessive table, §§110 and 130](https://www.gutenberg.org/files/5424/5424-h/5424-h.htm).

C–V SINN independently supports subject reference, while also documenting other antecedent patterns; no universal subject-only rule is inferred. [C–V SINN](https://norroen.info/dct/cleasby/s.html).

The file comes to an end within its own colour-record span. The already-reviewed genitive containment phrase and the M1 definition of embedded/associated structured records preserve **file truncation**, not a visible picture edge, normal completion of metadata, or successful saving. The prior `endar` is **not declared impossible**: a case-syncretic neuter could support an impersonal reading. M2 removes reliance on that unsettled analysis and supplies a clear local antecedent for `sinna`.

## Provenance and data-only checks

- Author M2 snapshot SHA-256: `10ce9baef42c5beab6fdb6195778b87589132b5f3c34cbee4e2a26f7074fc930`.
- Frozen review ledger SHA-256: `6e6f8ad79d3243c7e41c75e0c401abf2f23d0eb01e7ff383abfe66fb9df43eb2`.
- Exact English was independently rechecked read-only at `Paintroid/src/main/res/values/strings.xml`, lines 553–554, in the supplied baseline workspace. Supplied develop commit `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`; no independently resolved local HEAD claim.
- Each proposal changes exactly one word form relative to its previous held target. All other characters are retained. Both English and target values have no interpolation placeholders or numeric limits.
- Historical components/constructions do not attest medieval metadata, software support or byte-stream ranges. Those remain explicitly modern extensions under M1.
- The frozen 449 adoption receipt and M1 adoption receipt hashes were checked unchanged. No implementation or project test result is asserted.

Any later project adoption is recorded separately; this review file remains the recommendation-stage record.
