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
