# Chamorro / Shan / Tai Nüa priority translation candidates — 30 October 2026

## Result and status

This is **partial candidate work, not a complete P0+P1 delivery** and not independently accepted production wording. Base verified through the GitHub connector: `develop` = `420cb76fb1fc02a53a5b6296505be193eaa3bb2f`.

- Chamorro: 95 candidate values, 23 P0 and 72 P1; 246 keys unresolved.
- Shan: 176 candidate values, 50 P0 and 126 P1; 165 keys unresolved.
- Tai Nüa: no new semantic candidate; all 341 keys unresolved for linguistic acceptance.
- Independent acceptance: zero for all three. No production resources changed, no merge, no CI/full test run, no device/font/render claim.

The JSON files enumerate **every one of the 341 priority keys per locale** with its current English source. `target: null` is an explicit unresolved translation, not English fallback disguised as a completed translation. XML files contain only the non-null candidate wording. They must **not overwrite a canonical catalogue** as if complete; existing keys not in a partial candidate have not been approved for deletion.

## Review method and limits

These are direct model-authored translations from actual UI semantics, followed by a same-author meaning check, not independent backtranslation or native-speaker certification. Every candidate has an English backtranslation and, where relevant, a particular terminology concern. Labels and multi-sentence warnings are both covered. A matching published UI phrase was not required.

Chamorro is tentative especially for contemporary computing terminology and inflection. `fail`, `fotmat`, `app`, `data`, and `pixels` are explicit proposed loans, **not claims of established Chamorro terminology**. The phrase `Såtba` is proposed for digital save; general-language dictionary evidence does not prove that this is the preferred computing verb. Mixed technical English in the invalid-filename warning is explicitly marked and needs resolution before acceptance. Two weak formulations for “Keep editing” and “Reset to black/white” were removed rather than counted as translated.

Shan uses Shan-script wording, not Burmese or Tai Nüa. Specific provisional terminology includes frame, pixel, memory, draft, resolution, compression, decoder and encoder. In particular, the draft word `ပိူင်ယၢင်ႇ` needs scrutiny for whether it means draft here rather than example/model, and `ၵမ်ၵႅမ်ႈ` for pencil must be checked rather than accepted on this author's authority. Technical-warning candidates marked in the row notes must be reviewed as complete propositions, not approved merely because every placeholder survived.

Tai Nüa: the author cannot reliably compose or independently assess the complete technical UI in Tai Le orthography. No transliteration from Shan, invented grammar or generic “needs a published source” gate is supplied. A competent Tai Nüa translator must supply the unresolved target values. This is a language-competence limitation, not a tool denial.

## Existing Shan entries: nine-row review

| Key | Assessment |
|---|---|
| `ui_brush` | Existing `မၢၵ်ႇတႅမ်ႈ` not accepted: insufficient confidence in the tool noun. No replacement invented. |
| `ui_save` | `သိမ်း` conveys save/keep. Retained as a candidate, not independently accepted. |
| `ui_cancel` | `ယႃႇႁဵတ်း` means do not do; plausible cancel action. Retained candidate; review UI naturalness. |
| `ui_save_a5d0d9` | Existing alias to `ui_save` loses the source's dialog-opening ellipsis. Candidate `သိမ်း…` preserves it. |
| `ui_menu_help` | `ၸွႆႈထႅမ်` help/assist fits help menu. Outer Android quoting is serialization, not a semantic defect. |
| `ui_ok` | `ဢူဝ်ႇၶေႇ` phonetic OK. Retained candidate. |
| `ui_menu_edit` | `မႄးထတ်း` edit/revise. Retained candidate. |
| `ui_undo` | Existing `ၶိုၼ်ၶိုၼ်း` not independently understood well enough to confirm single-action Undo semantics; explicitly unresolved, not silently approved. |
| `ui_done` | `ယဝ်ႉ` finished/done. Retained candidate. |

## Existing Tai Nüa entries: seven-row review

| Key | Assessment |
|---|---|
| `ui_cancel` | Existing `ᥟᥛᥱ ᥞᥥᥖᥱ`: Tai Le-script input retained in the evidence file; cancel meaning not certified. |
| `ui_menu_edit` | Existing `ᥛᥨᥢᥳ ᥛᥥᥰ`: edit meaning/word order not certified. |
| `ui_ok` | Existing `ᥟᥨᥝᥱ ᥑᥥᥱ`: plausible phonetic acknowledgement is not sufficient for author to certify Tai Nüa. |
| `ui_save` | Existing `ᥔᥤᥛᥰ ᥘᥩᥒ ᥘᥦᥐ ᥘᥣᥭ`: semantic scope and spelling need competent Tai Nüa review; no claimed backtranslation. |
| `ui_undo` | Existing `ᥑᥪᥢᥴ ᥑᥪᥢᥰ`: Undo semantics not certified. |
| `ui_save_a5d0d9` | Source `Save…`, existing alias `@string/ui_save`: independently supportable structural defect is loss of ellipsis. Appending an ellipsis alone would not validate the underlying wording. |
| `ui_menu_help` | Existing `ᥓᥩᥭ ᥗᥦᥛᥴ`: help meaning not certified. Outer quotes are valid Android serialization. |

All 16 existing entries are individually accounted for above; review does **not** mean accepted. Exact snapshots are included as `shn-existing-input.xml` and `tdd-existing-input.xml`.

## Safety/meaning checks and examples

- Shan animation candidates distinguish still output, first-frame-only import, separate PNG default image, and uncertain multiple-frame detection. No claim that animation survives Save.
- Shan export-created warning still directs the user to Save/Save as before proceeding; export is not presented as saving the current full image.
- Shan sharing explanation keeps the current Save destination unchanged.
- Shan unsupported-file warning retains all 13 format names including Base64; no invented new format support.
- Current full-image memory warning retains the OR condition (budget exceeded OR allocation failed), editing a resized **copy**, and original-file preservation. The technical wording still requires independent linguistic review.
- Chamorro discard/clear candidates are removal actions, not hiding; current-image unsaved-change warning remains affirmative and save confirmation remains a question.
- All format arguments, source attributes including `formatted="false"`, and escaped newline counts are preserved for candidate entries. ASCII apostrophes are escaped for Android XML.
- Validation is bounded XML/key/placeholder/newline checking, **not** a test of linguistic accuracy or Android resource compilation.

## Reference used for one ambiguity

The [2024 English–Chamorro Finder List](https://escholarship.org/uc/item/0098k2nh) lists possible general-language save vocabulary. It was consulted only for the choice of save verb; it does not supply a complete UI translation or establish digital terminology. No dictionary lookup was used as a substitute for translating the supplied UI meaning.

## Remaining work

The JSON `unresolved` rows are the exact remaining scope (not a proposed scope reduction). Complete them using sufficient language competence, and independently review all candidates, especially the row-specific technical terms above. Then integrate only accepted values into canonical XML with language-qualified reviewers and applicable project checks. This evidence ref carries no production acceptance credit.
