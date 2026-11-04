# Drawing controls and focused help: Old English and Old Norse

Base: `47df02c9fb5371b2eb4b3fc85f2db85e02e61c78` on `review/nv-bottom-2038-20261103`.

## Change and review

Adds ten missing string resources per locale: three P2 controls and seven related P3 help entries. Each locale has nine authored text entries plus the preserved `ui_cursor_help29` alias to `ui_cursor_help31`, not ten independent prose translations. Canonical Android XML owns the wording.

Independent review accepted the batch with one correction: the Old English option title uses `Toles cyre`. The remaining entries are unchanged. The corrected integration was revalidated. The noun is already used for choice in the catalogue and is independently attested as choice/option: https://bosworthtoller.com/42461 .

Fullscreen is distinguished from fitting the canvas or resizing the image. The toolbox caption covers collapse or expansion without assuming a fixed arrow direction. Tool option is the settings-choice dialog title. Selection corners/edges resize, while the round handle rotates. Cursor help preserves positioning, drawing-button tap, pan-to-draw and tap-again-to-stop order. Marker enlargement does not change painted brush size. Pencil crispness applies at every selected width. Grid visibility remains at 800% zoom or higher, and rulers measure image-pixel positions.

The embedded Draw → Drawing captions exactly match the existing locale labels, including the catalogue's Old Norse Teikna → Teikna. New screen terminology is a modern technical adaptation; the Old English display-board compound is distinct from the established canvas term. No historical computer vocabulary claim is made.

## Checks

- Actual `ClassicPaintActivity` and `ActionButton` consumers were inspected. Every added resource has a production Kotlin reference; the resource alias resolves to the translated help.
- XML uniqueness, Android escaping, source attributes, ordered typed placeholders and newline escapes pass. The 800% literal and its `formatted="false"` flag are unchanged. All 634 previous typed resources and bytes per locale are preserved; exactly ten strings are appended.
- 78 host tests passed after the correction in 10.463 seconds: translation, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through and open-review recovery.
- All 171 offered language options passed structural validation with `require_complete=False` after the correction.
- The base integration was checked against the Git tree: 1,276 materialized files matched content and executable mode. The 173 unmaterialized research/verification records remain through the verified base tree. Only the two locale files change in the application tree.

## Resource presence per locale

P0: 94/94; P1: 249/249; P2: 278/305 to 281/305 (24 missing); P3: 13/71 to 20/71 (51 missing). Total typed resources increase from 634 to 644: 643 strings and one plural resource. These counts describe direct resource presence, including the preserved alias, not whole-catalogue linguistic acceptance.

## Limits

No Android build, device/emulator, rendering, accessibility, runtime, CI or specialist/native certification is claimed. No issue tracker update is included.
