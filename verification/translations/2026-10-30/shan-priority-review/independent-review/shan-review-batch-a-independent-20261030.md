# Independent model review — Shan priority batch A

## Result

- **37 missing candidates:** accept **32** exact supplied values (**5 P0 + 27 P1**); hold **5** (**4 P0 encoding-family terms + 1 P1 clockwise label**).
- **Existing ui_undo:** accept unchanged `"ၶိုၼ်ၶိုၼ်း"`; this is review credit, not a missing translation addition.
- **Existing ui_brush:** proposed exact correction **ယူႈယွမ်ႉသီ** (paintbrush), requiring independent author second-check before acceptance. Existing **မၢၵ်ႇတႅမ်ႈ** is not accepted by this review; do not change production from this proposal alone.
- All **39** targets have individual decisions, exact text, backtranslations, rationales and confidence in `shan-review-batch-a-independent-20261030.tsv`.

## Binding and review boundary

Reviewed `../author/batch-a.tsv`, `review.md`, and `existing-review.tsv` against selected English and Shan resource files at `baseline resource snapshot`. Declared canonical develop **96681f687671a1fdffe134a325843919c1543401**, tree **39bb7351fa5532194e2c0430432b2f0cc6358a86**, and unchanged-selected-file assurance. No independent local Git HEAD attestation is claimed. Existing PR237 acceptances and six unchanged SHN decisions remain untouched and earn no new credit from term reuse.

This is an independent **AI/model linguistic and semantic review**, not native-human certification, renderer/device/UI-fit proof, or an automated localization test. This artifact records linguistic review only, not implementation.

Manual source comparison confirmed the supplied English text and attributes for this batch. `%1$s` and `%2$s`, PNG, the 1–1024 range, 180°/90° degree signs, arrows, slash, parentheses, source-specific ellipses, and the two `formatted=false` attributes are retained. Shan sentence punctuation replacing English full stops is intentional. The quoted Undo value remains exactly serialized as supplied.

## Primary reference findings, retrieved 2026-10-30

1. [Unicode CLDR Shan source annotations](https://raw.githubusercontent.com/unicode-org/cldr/main/common/annotations/shn.xml), `🖌` lines 3223–3224, explicitly names the paintbrush **ယူႈယွမ်ႉသီ**. [Unicode's English/Shan comparison chart](https://unicode.org/cldr/charts/49/summary/shn.html) independently exposes the English sense beside the same value (paintbrush row 7412). Its separate toothbrush row uses **ယူႈသီၶဵဝ်ႈ**. This is concrete evidence for the paintbrush noun in this app; it does not justify adopting an entire upstream catalogue.
2. [MediaWiki Shan catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/shn.json) has `editundo` **ၶိုၼ်ၶိုၼ်း**, with matching reversal use in `undo-nochange` and revision summaries. [Help:Diff/shn](https://www.mediawiki.org/wiki/Help:Diff/shn) links this label to the reversion action. The app's `PaintDocument.kt:230–244` restores the last history entry, supporting this same software sense. Upstream messages are not uniformly reliable: I did not import neighboring complete warnings or treat every message as certified.
3. The same primary MediaWiki source's `show-big-image-size` supports the exact pixel loan **ၽိၵ်ႉသႄႇလ်**, and preview compounds support **တူၺ်းလူင်ႈၼႃႈ**. Each complete pixel/preview candidate was reviewed compositionally rather than accepted solely because an isolated term occurs upstream.
4. Unicode CLDR's clockwise/counterclockwise circular-arrow descriptions distinguish **လိဝ်ၶႂႃ** and **လိဝ်သၢႆႉ**; its rotating-arrow vocabulary also uses the **ပၼ်ႇ** stem. This supports rotational meaning but does not resolve my idiomatic confidence in the proposed **ၶဵမ်မူင်း** clock-hand compound. A full replacement should be independently composed/reviewed, not assembled mechanically from emoji keywords.

## Why the five holds remain

The four encoding-family clauses have correct negation and preserve PNG/image/selection/autosave distinctions, but **ၶဝ်ႈၶူတ်ႉ** is a new technical calque in this batch. I cannot confidently decide its software-encoding sense as distinct from entering a code. An accepted decode term does not automatically license its inferred opposite. Targeted source lookup did not resolve that competence limit. Absence of a search result is **not** evidence that the phrase is wrong; neither is fluent-looking syntax sufficient evidence to certify it.

The 90° clockwise candidate has the right angle and intended direction. The hold concerns whether its exact clock-hand compound is idiomatic and unambiguous enough for a geometric command, not a demand for an identical published UI sentence. The simpler rotate and 180° labels do not depend on that compound and are accepted.

The failed Liktai direct retrieval was not used as lexical evidence. Secondary dictionary mirrors and machine-looking commercial Shan pages were not treated as validating references.

## Semantic checks that support acceptance

- Destination error describes a completed temporary image failing replacement at its save destination; `BitmapFileCodec.kt` confirms encoding is complete before `renameTo` fails.
- Derived-export warning still says the full drawing has unsaved changes and requires a full-image copy before replacement. Export success is not equated with saving that drawing.
- Autosave missing pixels and unreadable pixels remain different failures; `AutosaveStore.kt:147–158` confirms missing archive entry versus decoding failure. Recovered-image label does not imply undo-history restoration.
- Resize acts on dimensions; zoom explicitly acts on viewing; copy-resize identifies the copy rather than the original.
- Strictly positive dimension remains greater than zero, matching `ImageAssembly.kt`.
- Font-family label fits a font selector separate from style controls; preview is a section label in `TextStyleDialog.kt`.
- Paste hint retains OR and the exact currently accepted menu labels; tap-to-type matches the actual number button opening numeric entry.
- Foreground/background swap includes reciprocal exchange, not an ordinary single-color edit.

## Next action

The review recommends freezing the **32 accepted missing rows plus unchanged Undo** against the canonical source, without counting prior accepted terminology again. Route **ယူႈယွမ်ႉသီ** for independent second-check before converting the Brush correction to acceptance. Keep the five held rows outside the accepted manifest until their exact wording is resolved. This artifact does not change residual counts itself.
