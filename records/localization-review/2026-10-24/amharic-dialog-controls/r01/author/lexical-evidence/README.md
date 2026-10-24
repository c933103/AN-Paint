# Amharic common dialog controls: lexical author packet

Four original author decisions are prepared for independent review, not accepted or implemented:

- `ui_ok`: OK → **እሺ**
- `ui_done`: Done → **ተከናውኗል**
- `ui_cancel`: Cancel → **ይቅር**
- `ui_apply`: Apply → **ተግብር**

All four have `author_status: review`. Done deliberately has medium overall confidence: exact Android generic-button evidence is strong, but the completed-result wording must not suggest that a failed operation succeeded. An independent reviewer may hold it without blocking the other three. No review result or native-reader agreement is asserted here.

## Review map

`draft-candidates.json` contains the complete candidate decisions, confidence, variants, limitations, key-specific current consumer context and pinned links. Its current source is `../consumer-context.json`, with 36 direct exact-key occurrences in 17 callers and a 29-file supplied context packet. That corpus is bounded, not an exhaustive fresh repository search. The canonical English XML matches the parent's current source snapshot at commit `66be61df27c5359bffc32d56db21f3949899f873`.

The distinct roles are essential:

- OK acknowledges the displayed message, including errors; it does not assert success.
- Done finishes an interaction. Some views only close, drawing settings update live, GalleryCredits saves and validates before dismissal, and failed-save notices also use Done. Neither always-save nor always-no-save is accurate.
- Cancel abandons the current interaction, sometimes with operation-specific cleanup or color-preview restoration. It is neither deletion nor global undo.
- Apply requests the validated numeric, position, or dimension operation. Invalid input can keep the dialog open. It does not inherit acceptance from Apply to all, nor confer acceptance on other Apply phrases.

## Evidence and alternatives

`sources.json` inventories six complete retained snapshots, each with its pinned URL, byte count, local path, reused-source path and SHA-256. Four are paired AOSP English/Amharic XML snapshots, one is LibreOffice Amharic cui PO, and one is project English XML. Reuse is explicitly disclosed; no new retrieval is claimed. `exact-records.json` contains 16 line-bound exact records. `all-android-label-matches.json` records all 61 command-label matches in the two retained AOSP applications, including special-purpose variants rather than hiding them.

AOSP's exact generic labels support all four selections. Gallery2 corroborates OK, Done and Cancel but is not an unrelated translation authority. LibreOffice agrees on OK and supplies noun-style Cancel/Apply alternatives. These alternatives remain visible and are not treated as incorrect merely because they were not selected.

`bounded-glossary-reference.json` adds three visually verified word pairs with original paraphrases. The document attributes itself to ICT Development Office/ELRC but is hosted on a public mirror, and its creation metadata is from 2011. This is not an authenticated publisher endpoint or immutable publisher revision. The packet contains no full PDF, extracted full text, page images or inferred permission to republish those materials. Its conflicting Cancel and OK choices remain explicit. The exact Apply entry is distinct from Apply to all.

## Scope and verification

`english-source-records.json`, `search-limits.json`, `validation.json` and `SHA256SUMS` make the input, search bounds and static integrity checks inspectable. Full snapshots preserve raw records, including LibreOffice accelerator markers; display comparisons do not rewrite source files.

Prior 69 ready drafts and 11 holds are excluded. No production resource file was changed. No Work-side task, build, CI, runtime or accessibility exercise, release, remote publication or native-speaker consultation occurred. Independent review must decide whether to accept, revise or hold each exact candidate.
