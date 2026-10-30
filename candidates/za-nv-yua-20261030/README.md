# ZA / NV / YUA priority candidates — partial, not accepted

Baseline: `420cb76fb1fc02a53a5b6296505be193eaa3bb2f` (merge of #235).
Author: AI draft translation pass, 30 October 2026. No independent language reviewer has approved these drafts.

## Actual deliverables

| Locale | New P0 drafts | New P1 drafts | Undrafted P0 | Undrafted P1 |
|---|---:|---:|---:|---:|
| za — Standard Zhuang, Latin | 8 | 45 | 82 | 197 |
| nv — Diné bizaad, Latin | 0 | 14 | 92 | 235 |
| yua — Yucatec Maya, Latin | 13 | 66 | 79 | 183 |

146 new candidate entries, not 146 accepted translations. The 868 remaining missing priority messages are explicitly listed in `*-remaining.json` with exact keys and a pinned English-source reference. These counts exclude the 9 existing ZA priority entries (2 P0, 7 P1), all preserved unchanged. #235 completed a bounded ZA contribution, not the language.

`*-candidate.xml` contains actual proposed Android string values, **outside the application resource tree**. Do not install or merge it into production without independent linguistic review. `*-drafts.json` pairs every value with its exact key, tier, English source and author backtranslation. Those backtranslations explain intended meaning, not independent validation. `checks.json` records only performed structural checks. No full tests, builds, review requests, PR or production merge are part of this batch.

## Semantic context inspected

- `ClassicPaintActivity.kt:859`: Clear image applies the pending operation then clears the document. It is not a command to close a file or erase disk storage.
- `AssemblyActivity.kt:101`: Clear all empties the assembly. Clear-all drafts mean erase/delete all, not deselect all.
- `ClassicPaintActivity.kt:1079`: Keep editing is the negative dismissal of an unsaved-changes dialog. Two initial wordings that risked meaning finish/edit again were removed, rather than submitted as translations.
- `TextStyleDialog.kt:35`: Type text is the text-entry hint, not the typography/style selector.
- `AdvancedColourDialog.kt:211`: Selected color labels a chosen-colour sample. A Zhuang draft with uncertain participial meaning was removed.
- Existing ZA Save/Cancel/Brush, help/edit/undo/all/file entries and its Save alias remain byte-for-byte unchanged.

## Focused independent review needed

### Zhuang

`Cunz` is retained from the accepted catalogue. The save-as family uses `Cunz baenz …`; check that the result/complement construction is idiomatic for choosing the output format, not converting the currently open document in place. `ui_save_png` retains the PNG identifier. Check the noun order of `Mingz vwnzgen` (file name).

Colour drafts use `saek`, text drafts `vwnz`, width/height `gvangq`/`gau`; the review should verify these exact UI senses. In particular check `Fuzci` for clipboard copying, `siengsoq` for pixel, `bak faen` for percentage, `Gij senj` for an active selection, and `Dingh hoiz` for resetting rather than undoing. These are proposed lexical choices, not claimed established AN Paint terminology. Short labels and commands still need a fluent reviewer.

The remaining long warnings need consistent vocabulary for raster images, retained drafts versus recovery copies, undo cache, colour profiles, encoding versus decoding, and failure versus deliberate pausing. This author cannot reliably compose those distinctions in Standard Zhuang, so no invented full warnings were supplied.

### Navajo

`ui_cancel`, help/edit, image, preview and undo were checked against the corresponding MediaWiki Navajo labels, not mechanically imported as a catalogue. Image here means any editor raster image, not only a photograph; confirm that `Eʼelyaaígíí` is broad enough. The edit label uses the existing first-person UI convention (I change it), unlike an English imperative. Confirm whether that convention is appropriate throughout AN Paint. `Dooleełígíí` means what it will be; review its fit for the preview surface. `Saad` can denote words/language; review whether the plural language-menu caption needs a more explicit form.

`Tʼáá ałtso`, `Ádin`, the black/white label, new, and pencil are author drafts; no external matching software label is claimed. In particular verify the orthography of `Bee akʼeʼelchíhí` and the standalone new-label form `Ániidí`.

All P0 warnings remain undrafted. The blocker is this author's inability to reliably produce Navajo verb morphology, aspect/negation and technical relational clauses for data-safety messages. A source dictionary would not establish those whole sentences. None of this is a claim that Navajo lacks such wording or needs an exact published sentence before translation.

### Yucatec Maya

The save family uses `Líikʼs` in the keep/store sense; independent review must confirm its software sense versus its raise/lift sense **before any P0 use**. This is the highest-priority lexical gate. `Maʼ béeychaj …` drafts intend past inability, not a permission prohibition. The save-changes question asks about retaining changes and must not be approved merely because its tokens parse.

Review `oochel` for a general image, `boon` for the drawing/painting action, `boonil` for colour, and `tsʼíib` for editable text. Check `píixel`/`píixeloʼob` as a technical borrowing, `xook` as numeric input, the imperative forms, and Yucatec orthographic choices (not another Maya language). `ui_enter_positive_dimensions` and `ui_enter_a_positive_size` deliberately say greater than 0, preserving the mathematical condition. The trim-amount message explicitly allows 0. `ui_type_text` was revised to avoid a form that could imply writing *to me*.

Review especially: `ui_underline` (must denote a line under text, not text placed underneath); `ui_enter_valid_dimensions` (must express valid input, not moral good/bad); `ui_use_colour` (must be the colour action, not a general instruction to work); `ui_eraser` (tool name); width/height measurement labels. These drafts are kept visible for correction, not silently treated as accepted wording.

The remaining complex warnings require reliable scope of negation, unchanged-original guarantees, memory-budget causality, selection/clipboard distinctions and codec terminology. They are not replaced with shorter summaries that would omit safety information.

## Targeted reference checks

These references resolve particular lexical ambiguities only, not completion or approval:

- [MediaWiki Navajo current catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/nv.json): cancel/help/edit/image/preview/undo conventions. GPL-2.0-or-later, contributors credited in upstream metadata. Consult the repository's existing MediaWiki licence file when accepting adapted labels.
- [MediaWiki Zhuang current catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/za.json): view/remove/main/show conventions; no change to retained AN Paint choices.
- [La Jornada Maya, native Maya text](https://www.lajornadamaya.mx/k%27iintsil/166007/bentley-bacalar-kiis-buuts-ch-a-ab-u-yool-ti-u-yaak-alil-ukp-eel-u-boonil): actual colour/image vocabulary in context; not copied prose.
- [Christian Lehmann, Maya causative](https://www.christianlehmann.eu/ling/sprachen/maya/gramatica/semas/verbo/verb_tema/causativo.php): confirms the raise/lift sense underlying the specific `Líikʼs` ambiguity. Does not certify software Save.

## Next action

Have competent reviewers correct the actual drafts and translate the specifically enumerated remaining messages. Recheck whole messages against consumers, then placeholders/XML and UI rendering. This partial batch is an inspectable starting point, not completion of the assigned three-language P0+P1 scope. No request to spawn another task is implied or executed.
