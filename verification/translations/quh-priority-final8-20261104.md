# South Bolivian Quechua remaining priority entries — 4 November 2026

Base: `1fdc81dadc278598a40d9a94d12094096ae948e7`.
Eight missing canonical quh entries: five P0 safety/format messages and three P1 tool labels. Independent model/context review retained seven and revised sampled-decoding wording to describe decoding the whole image at reduced dimensions. No native-speaker certification is claimed.

## Semantic review

- ASCII export remains plain text using light/dark characters, equal-width characters for viewing, and a visual rendition that cannot reopen as the original image.
- PDF preserves 144 dpi and conversion of text/vector objects to pixels.
- GIF preserves still-image output, at most 256 colours, dithering's gradient smoothing, and first-frame-only animation import.
- Memory warning preserves four indexed numeric slots, whole-image memory, transformation/selection reserve, available-memory bound, stopping before allocation, and no automatic resizing.
- Resize estimate includes canvas, clipboard, reduced-dimension decoding and editing buffers; variable actual memory, detail loss and unchanged original remain explicit.
- Elipse is a precise geometry loan; colour tolerance describes permitted colour difference, not geometry; watercolor is a tool noun.

Current callers inspected: `ImportSelection.kt`, `SaveOptionsDialog.kt`, `ImageMemoryPolicy.kt`, `ImageResizeDialog.kt`, and `ScanlineFill.kt`. Existing reviewed editor/tool consumers remain unchanged. Technical loans and long memory explanations still need fluent-user and rendered-device feedback.

## Checks and direct coverage

XML parse, eight unique missing-only keys, exact reviewed values, source attributes, indexed placeholders, Android apostrophe escaping, format and literal-token helpers passed. All 333 previous values and attributes remain unchanged. Counts use the canonical resources and `translations/string-importance.json` fetched at the base above, not historical credit.

- P0: 92/92 direct strings, zero missing.
- P1: 249/249 direct strings, zero missing.
- Full catalogue: 341/717. P2: 0/305; P3: 0/71.

This closes direct P0/P1 coverage only. It does not establish full-catalogue completion, native-language acceptance or UI rendering quality. No Android build, hosted CI, device/layout test, merge, deployment or release claimed. Canonical XML owns current wording; this evidence is not a wording freeze.
