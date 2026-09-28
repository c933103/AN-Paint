# Shared cursor-help settings route — claims withdrawn

**Localization status reset — 28 September 2026: all previous progress, completion, repair, verification and no-defect conclusions for PRs #2–#9, #12 and #15 are withdrawn. Every item requires a full recheck; no previous progress is accepted.**

See the [individual recheck register](https://github.com/c933103/AN-Paint/blob/review/localization-integration/verification/localization-recheck-register.md). The rejected delivery is additional material to check, not an accepted audit. Historical source, test outputs and evidence classifications remain available as inputs. They carry no current completion credit. Completing the other 81 locales is outside this task.

Every assertion in the record below is a **withdrawn prior claim requiring full recheck**, including any statement that work was reviewed, implemented, repaired, complete, verified, preserved, or free of further defects. Prior lexical acceptance labels and test outcomes are historical inputs, not current task status.

[Original record at its previous commit](https://github.com/c933103/AN-Paint/blob/e51ab25c0fd4bfe10a8b4907ac3b7b9e30b42a26/verification/localization-cursor-help-followup.md).

<details>
<summary>Withdrawn historical claim record — no accepted progress</summary>

# Shared cursor-help settings route

The existing Armenian (`hy`), Serbian Cyrillic/Latin (`sr-Cyrl`, `sr-Latn`),
Hebrew (`he`, Android `values-iw`), Polish (`pl`) and Thai (`th`) cursor-help
strings stopped after the start/stop drawing instructions. They omitted the
current source sentence explaining where to change brush and stroke settings.

Each existing instruction is preserved. A localized sentence now directs users
to the actual `ui_draw26` → `ui_drawing23` captions in that catalogue. This follows
`ClassicPaintActivity.showCursorHelp` and the brush category in
`ToolCategoryButton.kt`; it does not introduce a new tool or navigation action.
The default `ui_cursor_help31` already describes this route.

The six new sentences use each language’s own syntax. Serbian Cyrillic and Latin
represent the same Serbian text in their respective scripts. This small shared
help correction does not complete or certify the rest of those catalogues.

Validation: all 27 existing translation checks passed, strict AAPT2 compilation
of the entire resource tree passed, and a source/caption comparison confirmed the
six routes use their resolved live labels while preserving the previous text.
The shared `ui_cursor_help31` entry is included when these repairs are backported
to existing original-PR catalogues.

</details>
