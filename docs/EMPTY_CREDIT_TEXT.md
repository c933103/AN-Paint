# Empty image-credit text

The gallery's **Copy all** action checks the combined current credit text. An
empty result does not establish whether a gallery image was inserted. A credit
can be edited to an empty or whitespace-only value after insertion.

Both Copy all with no nonblank text and the credit editor with no source entries
now use the neutral English message “No image credit text is available.” The
legacy resource key `ui_no_gallery_images_have_been_inserted` is retained for this
bounded wording change. Neither call site's conditions nor document, clipboard,
credit editing, archive, metadata-limit or insertion logic changes.

- Copy all with no nonblank text leaves the clipboard unchanged.
- A source record with blank text remains editable and associated with the image.
- Explicit **Copy credit** inside the editor still accepts and copies an empty
  field; this differs intentionally from Copy all's no-text path.

## Locale scope

The complete replacement value is recorded in
[`gallery_empty_credit_current_wording.json`](../tools/fixtures/current_localization/gallery_empty_credit_current_wording.json)
for default English and every one of the 59 existing exact scoped catalogues.
The [explicit scope](../tools/fixtures/current_localization/locale_contract_scope.json)
identifies all 171 picker options: the other 112 catalogues continue to omit this
key and resolve to default English. Their fallback is unfinished translation.

The resource fixture checks complete messages, XML/Android syntax, placeholders
and exact scope. It does not certify any whole language, native idiom, glyph
rendering or device behavior. The Korean mixed-script and emoji variants remain
canonical inputs to the existing exact-script resource generator.

## Regression coverage and limits

`CommonsCreditFlowTest` uses offline provider fixtures and actual production
handlers to check:

1. The editor launches the gallery with its own document credit session.
2. Successful download finishes that gallery. Its actual result returns to the
   editor, where successful image insertion is awaited and the selection accepted.
3. The editor opens a fresh gallery. Nonempty Copy all copies the stored credit.
4. The source's credit is edited to empty (and separately whitespace), saved, and
   finished. Copy all reports unavailable text while preserving the clipboard.
5. Gallery Done returns its actual result to the editor; the source and raw edit
   remain, and the inserted bitmap is unchanged. Another fresh gallery can edit
   the blank source record.

Additional controls cover an initially empty ledger, the empty credit-editor
message, explicit single-credit Copy of an empty field, and compiled resolution
of the complete message or English fallback for every picker locale.

The persistence scope is disk-backed credit-session acceptance, adoption into the
open document and gallery re-entry. These tests do not prove app-process restart,
saved-project reload, live providers, installed devices, or rendered text.

Run the focused source contracts with:

```sh
PYTHONPATH=tools python3 -m unittest test_gallery_empty_credit_wording test_translations test_locale_font_coverage
./gradlew :Paintroid:testDebugUnitTest --tests '*CommonsCreditFlowTest'
```

The new JVM regressions need an Android/Gradle environment. A source review or a
passing Python contract is not an executed JVM/device result. Keep the diagnostic
tracking PR [#84](https://github.com/c933103/AN-Paint/pull/84) open until the
implementation's exact-source verification is available.
