# Independent review of qug / quh / quz priority candidates

Source pinned at `b671d870bfe6334689a312eca426d3137e5803fa`, directory `records/localization-review/2026-10-30/qug-quh-quz-priority`.
Review date: 2026-10-30. Paused quy is excluded.

## Result and competence boundary

This is an independent **AI linguistic and semantic screening**, not a native-speaker review or a certificate of Chimborazo, South Bolivian or Cusco fluency. I read the candidate TSV against the English source inventory, regional-comparison record, README, all three XML catalogues and their unresolved-key notes. The authored backtranslations were not used as independent proof. Each of the 594 entries has a disposition in the three JSON files. An identical Southern candidate did not establish the correctness of its counterpart.

| Locale | Accepted | Corrected | Rejected | Uncertain | Total |
|---|---:|---:|---:|---:|---:|
| qug | 47 | 4 | 1 | 146 | 198 |
| quh | 53 | 0 | 0 | 145 | 198 |
| quz | 52 | 1 | 0 | 145 | 198 |

Accepted includes 8 invariant notation rows per locale. Thus accepted prose is 39 qug, 45 quh and 44 quz, **not** 47/53/52 newly certified translations. None of these totals makes the full localization complete. The 143 missing keys per locale remain outside this review and unresolved. In particular, no translation of the omitted high-risk warnings is implied.

Definitions:
- **accepted**: I find the candidate defensible for this source meaning within my actual competence. Not production acceptance, not regional native certification, and not a screen-fit result.
- **corrected**: A specific bounded correction is supplied. Read any residual usage limitation in the rationale; correction does not certify everything around it.
- **rejected**: Concrete semantic objection sufficient to withhold the candidate. No fluent replacement invented.
- **uncertain**: Regional, grammatical or technical-sense uncertainty remains. A bounded proposed repair can appear here without endorsing the whole entry.

The JSON `corrected_wording` fields are human-readable text, not ready-to-paste Android XML; apostrophes would need Android escaping when and if adopted. Blank means no replacement certified, not that the source string should be deleted.

## Specific actionable findings

1. QUG `save20_file_format` / `save20_file_name`: `Kipapak` disagrees with the noun `Kipu` used elsewhere. Conditional repairs are `Kipupak rikcha` and `Kipupak shuti`; both remain uncertain because digital-file and format terminology itself is not settled by this spelling repair.
2. QUG `ui_copy` / `ui_copy_all`: remove duplicated `-ta` in `kikinllatata`: `Kikinllata rurana` / `Tukuyta kikinllata rurana`. The full-text-copied candidate already uses `kikinllata`.
3. QUG `ui_bold`: `Raku`, not object/adverbial `Rakuta`, for the standalone style label.
4. QUG `ui_left`: `Lluki`, not Southern-style `Lluk'i`, under the catalogue's declared Ecuadorian orthography. Likewise the bounded repair `Llukiman sinrishka` for left-aligned; that complete alignment expression remains uncertain. This is not a proposed alteration to QUH/QUZ `Lluq'i`.
5. QUZ `ui_clear_all`: `Llapanta pichay`, consistent with the explicit full-object marking already present in `Llapanta akllay` and `Llapanta rikuchiy`.
6. In all three catalogues, `ui_could_not_complete_the_edit` and `ui_could_not_complete_the_operation` appear to lack complement `-ta` on `tukuchiy`. Specific bounded `tukuchiyta` repairs are supplied but the full impersonal ability sentences remain uncertain.
7. QUG `ui_preview` is rejected: `Ñawpaman rikuy` directs looking forwards/ahead rather than clearly naming a preview of pending image changes. I do not certify a replacement.
8. Draft `ñawpa/ñawpaq` image is uncertain in all three: earlier/previous/front image is not automatically an unsaved recovery draft.
9. QUH `llankhay` touch-gesture forms are not accepted simply because they differ from QUZ `llamiy`. Regional spelling, touch versus work, and tap versus press must be checked. No global Southern replacement is proposed.
10. Crop constraints distinguish canvas from image and preserve intended positive-dimension/at-least-one logic in broad meaning, but their complete regional grammar remains uncertain. They must not be accepted merely because the backtranslation restates the English.
11. Palette=colours, invert=turn colours, front/back colour slots, zoom=enlarge and file=kipu remain technical-sense questions. This review does not demand a published exact UI sentence; a competent regional composer can resolve them directly.
12. Draw again and Redo remain separate review targets. Recognizing do-again is insufficient to certify the history command, especially while Undo is outside the proposed candidate set.

## Checks performed

[
  {
    "locale": "qug",
    "entries": 198,
    "missingCandidateKeys": [],
    "xmlTsvMismatches": [],
    "placeholderMismatches": [],
    "unresolved": 143
  },
  {
    "locale": "quh",
    "entries": 198,
    "missingCandidateKeys": [],
    "xmlTsvMismatches": [],
    "placeholderMismatches": [],
    "unresolved": 143
  },
  {
    "locale": "quz",
    "entries": 198,
    "missingCandidateKeys": [],
    "xmlTsvMismatches": [],
    "placeholderMismatches": [],
    "unresolved": 143
  }
]

These are bounded evidence checks, not a full build/test run: the 198 source/candidate records per locale match the XML values after Android apostrophe unescaping; no missing candidate key or format-token mismatch was detected. Existing unresolved arrays have 143 keys each. No production resource was edited, no full tests run, no PR or merge performed.

## Narrow lookup, not a source-hunting replacement for review

A limited lookup addressed only the QUG left/bold spelling and QUH touch-verb ambiguity. Search surfaced the Ecuador Ministry dictionary at https://www.educacion.gob.ec/wp-content/uploads/downloads/2013/03/RK_diccionario_kichwa_castellano.pdf and the Bolivian dictionary at https://www.illaa.org/pirwa/diccionarios/DicQuechuaBolivia.pdf . The Ecuador PDF fetch timed out; search snippets are not claimed as inspected primary-source confirmation. An Otavalo teaching result is not Chimborazo validation. No dictionary is presented as attesting these full UI sentences. The bounded spelling/morphology findings above are reviewer judgments; the unresolved regional lexical questions remain explicitly uncertain.
