# Six scoped cursor-help entries: new source/context check

The six entries implicated by HELP-018–HELP-023 were read anew at integration
source `a6b5956b0`: Armenian, Serbian Cyrillic, Serbian Latin, Hebrew, Polish and
Thai `ui_cursor_help31`. This is a bounded check of these entries and their
current command destinations, not completion of those languages.

| Locale | Actual Draw caption | Actual Drawing category caption | Current help finding |
| --- | --- | --- | --- |
| `hy` | Նկարել | Նկարչական գործիքներ | Position, button activation, drawing motion, stop and settings route are present |
| `sr-Cyrl` | Цртање | Алати за цртање | Same operation sequence; settings identify brush and strokes |
| `sr-Latn` | Crtanje | Alati za crtanje | Same wording/sequence as the Cyrillic pair |
| `he` | ציור | כלי ציור | Position, drawing-button activation, drag, stop and brush/line settings route are present |
| `pl` | Rysowanie | Narzędzia rysowania | Position, drawing-button activation, drag, stop and brush/drawn-line settings route are present |
| `th` | วาด | เครื่องมือวาด | Position, button activation, drawing drag, stop and brush/line settings route are present |

The Thai wording describes the drag as starting drawing after enabling it with
the button. This is not evidence that dragging toggles the mode, and no change
is made solely for that wording preference. No confirmed missing operation or
wrong destination was found in this bounded reading; native-speaker certification
and exhaustive grammatical review are not claimed.

The source trace was checked independently of the old report:

- `ClassicPaintActivity.menuTitle` uses `ui_draw26` for the Draw tab.
- `ToolCategory.BRUSH` uses `ui_drawing23`; the current Drawing group contains
  Pencil/Brush/Watercolor/Airbrush. Its options expose Drawing settings.
- `ClassicPaintActivity` creates `cursor_draw_toggle`, wired directly to
  `PaintCanvas.toggleCursorDrawing`; `updateStatus` switches its Start/Stop
  label and accessible description.
- In `PaintCanvas`, motion offsets the cursor, and draws only when
  `cursorDrawing` is enabled. A short tap near the cursor separately toggles
  the mode without committing a stroke. The separately displayed
  `ui_cursor_tap_hint37` describes that additional interaction in all six
  catalogues.

The existing `test_cursor_help_includes_the_actual_settings_route` checks
localized captions with resource-alias resolution; it cannot prove the verbs
or complete operation sequence. Its source was inspected. Kotlin
`tappingTheCursorTogglesInkWithoutPaintingAndDraggingItStillDraws` asserts
mode notifications, pixel preservation on taps, an actual stroke on drag and
undo; device `tappingCursorWithAndroidInputTogglesDrawingWithoutLeavingADot`
asserts real input, state, accessible Start/Stop label and unchanged white pixels.
Finding these assertions is source-coverage evidence, not a new device pass.
Current execution results are recorded separately with their exact CI runs.

No translation, application code, test or unrelated locale was changed by this
check. The broader help, typography and original conversation review remains open.
